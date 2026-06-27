#!/usr/bin/env python3
"""Pre-publish component checker for the blog pipeline.

Deterministic validator for the `:::component` fences and inline tokens that
`/draft` emits (the writer's menu is `examples/component-cheatsheet.md`; the full
spec is `examples/ahrefs-components.md`). A malformed or over-decorated article
ships as broken text, so this checker HALTS the pipeline before publish.

Usage:
    python scripts/lint_components.py <path-to-markdown-file>

Behavior:
    - HARD errors  -> exit NON-ZERO; each error printed with a 1-based line number.
    - SOFT issues  -> exit 0; printed as WARN lines (advisory, never blocking).
    - Final line   -> "COMPONENTS_OK" (exit 0) or "COMPONENTS_FAIL (<n> errors)" (exit 1).

Exit codes:
    0   — no hard errors (may carry warnings)
    1   — one or more hard errors (halt and fix)
    64  — usage error (bad arguments / unreadable file)

This validates the *contract*, not taste. The render contract in
`examples/ahrefs-components.md` is the source of truth for fence names and
required attributes; keep the two tables below in sync with it.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

# --- the contract ----------------------------------------------------------

# Every fence name the renderer knows. An opener with any other name is a hard
# error (the renderer would fall back to a plain aside and the writer's intent
# is lost). Keep byte-for-byte in sync with examples/ahrefs-components.md.
KNOWN_FENCES: frozenset[str] = frozenset(
    {
        "nutshell",
        "methodology",
        "key-takeaways",
        "tip",
        "note",
        "warning",
        "important",
        "sidenote",
        "definition",
        "stat",
        "stat-group",
        "stat-list",
        "table",
        "figure",
        "diagram",
        "proscons",
        "feature-matrix",
        "decision-table",
        "preferred-order",
        "entry",
        "verdict",
        "badge",
        "expert",
        "pullquote",
        "tweet",
        "video",
        "further-reading",
        "jumplinks",
        "faq",
        "cta",
        "editor",
    }
)

# fence name -> the attribute that MUST be present on the opener line.
REQUIRED_ATTR: dict[str, str] = {
    "stat": "value",
    "expert": "name",
    "cta": "href",
    "figure": "src",
    "diagram": "src",
    "tweet": "url",
    "video": "src",
    "definition": "term",
    "entry": "name",
    "badge": "kind",
}

# Framing fences that may appear at most once each.
SINGLE_USE_FENCES: dict[str, int] = {
    "nutshell": 1,
    "methodology": 1,
    "key-takeaways": 1,
}
# cta is capped at two (once high, once low).
CTA_CAP = 2

# The callout family — used for the soft "too many callouts" and
# "back-to-back callouts" warnings.
CALLOUT_FENCES: frozenset[str] = frozenset(
    {"tip", "note", "warning", "important", "sidenote", "definition"}
)
MAX_CALLOUTS = 8

# An opener line: optional indent, ':::', name (letters/digits/hyphens, no
# leading space after the colons), then optional same-line attributes.
_OPENER_RE = re.compile(r"^\s*:::(?P<name>[A-Za-z][A-Za-z0-9-]*)\s*(?P<attrs>.*?)\s*$")
# A bare closer: optional indent then exactly ':::' and nothing else.
_CLOSER_RE = re.compile(r"^\s*:::\s*$")
# Attribute pairs on an opener line: key="value" (double-quoted). Bare flags or
# single-quoted values are tolerated (forward-compatible) but only double-quoted
# pairs are read for required-attribute checks — matching the render contract.
_ATTR_RE = re.compile(r'([A-Za-z_][\w-]*)\s*=\s*"([^"]*)"')


@dataclass(frozen=True)
class Issue:
    line: int
    message: str


def _is_fenced_code_delimiter(line: str) -> bool:
    """True for a markdown code-block delimiter (``` or ~~~)."""
    stripped = line.lstrip()
    return stripped.startswith("```") or stripped.startswith("~~~")


def _parse_attrs(attr_text: str) -> dict[str, str]:
    return {m.group(1): m.group(2) for m in _ATTR_RE.finditer(attr_text)}


def lint(text: str) -> tuple[list[Issue], list[Issue]]:
    """Return (hard_errors, soft_warnings) for the given markdown text."""
    hard: list[Issue] = []
    soft: list[Issue] = []
    lines = text.split("\n")

    # Fence stack: list of (name, opening_line_no). A non-empty stack at EOF
    # means an unclosed fence.
    stack: list[tuple[str, int]] = []
    counts: dict[str, int] = {}
    # Track the line number of the last callout fence that *closed* immediately
    # before the current opener, to detect back-to-back callouts.
    prev_closed_callout_line: int | None = None
    last_event_was_close = False
    last_closed_name: str | None = None
    in_code_block = False

    for idx, raw in enumerate(lines):
        line_no = idx + 1

        # Skip the interior of fenced code blocks (``` / ~~~) so a ':::' inside
        # a code sample is never treated as a component fence.
        if _is_fenced_code_delimiter(raw):
            in_code_block = not in_code_block
            last_event_was_close = False
            continue
        if in_code_block:
            continue

        closer = _CLOSER_RE.match(raw)
        if closer:
            if not stack:
                hard.append(Issue(line_no, "closing ':::' with no matching opener"))
                last_event_was_close = False
                continue
            name, _open_line = stack.pop()
            counts[name] = counts.get(name, 0) + 1
            last_event_was_close = True
            last_closed_name = name
            if name in CALLOUT_FENCES:
                prev_closed_callout_line = line_no
            else:
                prev_closed_callout_line = None
            continue

        opener = _OPENER_RE.match(raw)
        if opener:
            name = opener.group("name")
            attrs = _parse_attrs(opener.group("attrs"))

            # Unknown fence name (hard).
            if name not in KNOWN_FENCES:
                hard.append(Issue(line_no, f"unknown fence name ':::{name}'"))

            # Nesting rule: the ONLY legal nesting is :::stat inside :::stat-group.
            if stack:
                parent_name = stack[-1][0]
                if not (parent_name == "stat-group" and name == "stat"):
                    hard.append(
                        Issue(
                            line_no,
                            f"illegal nesting: ':::{name}' inside ':::{parent_name}' "
                            f"(only ':::stat' may nest inside ':::stat-group')",
                        )
                    )
            # A stat-group child that is not stat is caught above; a :::stat NOT
            # inside a stat-group is allowed (a lone hero number is valid).

            # Required attribute (hard).
            req = REQUIRED_ATTR.get(name)
            if req is not None and req not in attrs:
                hard.append(
                    Issue(
                        line_no,
                        f"':::{name}' is missing required attribute '{req}'",
                    )
                )

            # Back-to-back callouts (soft): a callout opener on the line
            # immediately after a callout closer, with nothing between.
            if (
                name in CALLOUT_FENCES
                and last_event_was_close
                and last_closed_name in CALLOUT_FENCES
                and prev_closed_callout_line == line_no - 1
            ):
                soft.append(
                    Issue(
                        line_no,
                        f"two callout fences back-to-back "
                        f"(':::{last_closed_name}' then ':::{name}') — add prose between them",
                    )
                )

            stack.append((name, line_no))
            last_event_was_close = False
            continue

        # Any non-fence, non-blank content line resets the "just closed" state
        # used for the back-to-back check. Blank lines do NOT reset it, so a
        # callout, a blank line, then another callout still counts as adjacent.
        if raw.strip():
            last_event_was_close = False
            prev_closed_callout_line = None

    # Unclosed fences at EOF (hard) — one error per still-open fence.
    for name, open_line in stack:
        hard.append(
            Issue(open_line, f"':::{name}' opened here is never closed before EOF")
        )

    # Caps (hard). counts only reflects *closed* fences; an unclosed fence is
    # already a hard error above, so this never double-penalizes the same block.
    for name, cap in SINGLE_USE_FENCES.items():
        n = counts.get(name, 0)
        if n > cap:
            hard.append(
                Issue(
                    0,
                    f"':::{name}' appears {n} times — at most {cap} allowed per article",
                )
            )
    if counts.get("cta", 0) > CTA_CAP:
        hard.append(
            Issue(
                0,
                f"':::cta' appears {counts['cta']} times — at most {CTA_CAP} allowed per article",
            )
        )

    # Total callouts (soft).
    total_callouts = sum(counts.get(n, 0) for n in CALLOUT_FENCES)
    if total_callouts > MAX_CALLOUTS:
        soft.append(
            Issue(
                0,
                f"{total_callouts} inline callouts (tip/note/warning/important/sidenote/"
                f"definition) — more than {MAX_CALLOUTS}; the page reads as a wall of boxes",
            )
        )

    # Inline token balance (hard), checked outside fenced code blocks.
    hard.extend(_check_inline_tokens(lines))

    hard.sort(key=lambda i: (i.line, i.message))
    soft.sort(key=lambda i: (i.line, i.message))
    return hard, soft


def _check_inline_tokens(lines: list[str]) -> list[Issue]:
    """Balance of `{lead}`/`{/lead}` and `==` highlight markers.

    `{lead}` and `{/lead}` must pair (open before close, both present once-ish);
    `==` markers must be even in number across the document. Checked on the
    non-code body so formulas inside ``` blocks don't trip the `==` count.
    """
    errors: list[Issue] = []
    in_code_block = False
    open_lead_lines: list[int] = []
    eq_total = 0
    first_eq_line: int | None = None
    stray_close_line: int | None = None

    for idx, raw in enumerate(lines):
        line_no = idx + 1
        if _is_fenced_code_delimiter(raw):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # Strip inline code spans (`...`) so a literal `==` or `{lead}` inside a
        # formula chip is not counted.
        body = re.sub(r"`[^`]*`", "", raw)

        for m in re.finditer(r"\{/?lead\}", body):
            if m.group(0) == "{lead}":
                open_lead_lines.append(line_no)
            else:  # {/lead}
                if open_lead_lines:
                    open_lead_lines.pop()
                elif stray_close_line is None:
                    stray_close_line = line_no

        eq_count = len(re.findall(r"==", body))
        if eq_count and first_eq_line is None:
            first_eq_line = line_no
        eq_total += eq_count

    if stray_close_line is not None:
        errors.append(
            Issue(stray_close_line, "'{/lead}' with no matching '{lead}'")
        )
    for ln in open_lead_lines:
        errors.append(Issue(ln, "'{lead}' with no matching '{/lead}'"))
    if eq_total % 2 != 0:
        errors.append(
            Issue(
                first_eq_line or 0,
                f"odd number of '==' highlight markers ({eq_total}) — every "
                "'==text==' highlight must open and close",
            )
        )
    return errors


def _format_line(line: int) -> str:
    return f"line {line}" if line > 0 else "article"


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 64
    path = Path(argv[1])
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        print(f"error: cannot read {path}: {e}", file=sys.stderr)
        return 64

    hard, soft = lint(text)

    for issue in soft:
        print(f"WARN  {_format_line(issue.line)}: {issue.message}")
    for issue in hard:
        print(f"ERROR {_format_line(issue.line)}: {issue.message}", file=sys.stderr)

    if hard:
        print(f"COMPONENTS_FAIL ({len(hard)} errors)")
        return 1
    print("COMPONENTS_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
