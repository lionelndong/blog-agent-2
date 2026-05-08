#!/usr/bin/env python3
"""Format a cited draft for Strapi publishing.

Produces three files under content-pipeline/8-publish/{slug}/:
  - article.md       (clean markdown body, no H1, no shortcodes, with :::tip / :::note callouts)
  - article.json     (Strapi-shaped payload for API publish or admin paste)
  - README.md        (human-readable summary + what to do next)

Usage:
    python .claude/skills/format-for-publish/scripts/format_for_strapi.py <slug>

To enable direct Strapi API publish later:
  - Set STRAPI_BASE_URL and STRAPI_API_TOKEN env vars (e.g. via `doppler run --`)
  - Pass --publish flag
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DRAFT_DIR = ROOT / "content-pipeline" / "6-drafts-cited"
OUT_DIR = ROOT / "content-pipeline" / "8-publish"
IMAGES_DIR = ROOT / "content-pipeline" / "images"
QC_DIR = ROOT / "content-pipeline" / "quality-checks"
DOCS_DIR = ROOT / "docs"
BUNDLE_VIEWER = ROOT / "scripts" / "bundle_viewer.py"
INDEX_HTML = DOCS_DIR / "index.html"

IMAGE_REF_RE = re.compile(r"!\[([^\]]*)\]\((images/[^)]+\.(?:png|jpg|jpeg|webp|gif))\)")
QC_VERDICT_RE = re.compile(r"\b(PASS|BORDERLINE|FAIL)\b", re.IGNORECASE)


def quality_precondition(slug: str) -> tuple[bool, str]:
    """Read content-pipeline/quality-checks/{slug}.md verdict line.

    Returns (allow_publish, reason). Refuses publish if verdict is FAIL or file missing.
    """
    path = QC_DIR / f"{slug}.md"
    if not path.exists():
        return False, f"quality-check report missing: {path}"
    text = path.read_text(encoding="utf-8")
    head = "\n".join(text.splitlines()[:30])
    m = QC_VERDICT_RE.search(head)
    if m is None:
        return False, f"no verdict line found in {path}"
    verdict = m.group(1).upper()
    if verdict == "FAIL":
        return False, f"quality verdict is FAIL — refusing auto-publish"
    return True, f"verdict={verdict}"


def read_draft(slug: str) -> str:
    path = DRAFT_DIR / f"{slug}.md"
    if not path.exists():
        sys.exit(f"error: cited draft not found at {path}")
    return path.read_text(encoding="utf-8")


def strip_editor_notes(md: str) -> str:
    """Drop the '## Editor notes' section and everything after it."""
    m = re.search(r"^---\s*\n+##\s+Editor notes", md, re.MULTILINE)
    if m:
        return md[:m.start()].rstrip() + "\n"
    m = re.search(r"^##\s+Editor notes", md, re.MULTILINE)
    if m:
        return md[:m.start()].rstrip() + "\n"
    return md


def extract_title(md: str) -> tuple[str, str]:
    m = re.search(r"^#\s+(.+?)\s*$", md, re.MULTILINE)
    if not m:
        return "Untitled", md
    title = m.group(1).strip()
    body = (md[:m.start()] + md[m.end():]).lstrip("\n")
    return title, body


def transform_callouts(md: str) -> str:
    """Convert **Tip:**, **Pro tip:**, **Note:**, **Sidenote:**, **Editor:** paragraphs into :::callout blocks."""
    patterns = [
        (r"\*\*Pro tip:\*\*\s*(.+?)(?=\n\n|\Z)", "tip"),
        (r"\*\*Tip:\*\*\s*(.+?)(?=\n\n|\Z)", "tip"),
        (r"\*\*Sidenote:\*\*\s*(.+?)(?=\n\n|\Z)", "note"),
        (r"\*\*Note:\*\*\s*(.+?)(?=\n\n|\Z)", "note"),
        (r"\*\*Editor:\*\*\s*(.+?)(?=\n\n|\Z)", "editor"),
    ]
    for pattern, kind in patterns:
        md = re.sub(
            pattern,
            lambda m, k=kind: f":::{k}\n{m.group(1).strip()}\n:::",
            md,
            flags=re.DOTALL,
        )
    return md


def first_sentences(text: str, max_chars: int = 160) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    sentences = re.split(r"(?<=[.!?])\s+", text)
    out = ""
    for s in sentences:
        candidate = (out + " " + s).strip() if out else s
        if len(candidate) > max_chars:
            return out if out else s[:max_chars].rstrip() + "..."
        out = candidate
    return out


def extract_excerpt(body_md: str) -> str:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", body_md) if p.strip()]
    intro = ""
    for p in paragraphs:
        if p.startswith("#") or p.startswith(":::") or p.startswith("|") or p.startswith("```"):
            continue
        intro = p
        break
    intro = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", intro)
    intro = re.sub(r"\*\*(.+?)\*\*", r"\1", intro)
    intro = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"\1", intro)
    return first_sentences(intro, max_chars=160)


def truncate_meta_title(title: str, limit: int = 60) -> str:
    if len(title) <= limit:
        return title
    cut = title[:limit]
    last_space = cut.rfind(" ")
    return (cut[:last_space] if last_space > 0 else cut).rstrip() + "..."


def truncate_description(text: str, limit: int = 80) -> str:
    """Strapi v5 `description` is capped at 80 chars. Truncate at the last word
    boundary before `limit`, dropping trailing punctuation/quotes so we never end
    on a half-word or a dangling clause-opener like "include," or "with:". Falls
    back to a hard cut when there's no whitespace in the input.
    """
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= limit:
        return text
    cut = text[:limit]
    last_space = cut.rfind(" ")
    out = cut[:last_space] if last_space > 0 else cut
    # Strip trailing connector punctuation that signals a sentence in progress.
    return out.rstrip(" ,;:.-—–").rstrip()


def extract_tags(body_md: str, max_tags: int = 5) -> list[str]:
    h2s = re.findall(r"^##\s+(.+?)\s*$", body_md, re.MULTILINE)
    tags = []
    for h in h2s[:max_tags]:
        h = re.sub(r"^[\d\.\)\s]+", "", h)
        slug = re.sub(r"[^\w\s-]", "", h).strip().lower()
        slug = re.sub(r"\s+", "-", slug)
        if slug and slug not in tags:
            tags.append(slug)
    return tags[:max_tags]


def compute_read_time(body_md: str, *, wpm: int = 220) -> int:
    """Conservative read-time estimate in whole minutes. Floors at 1.

    Default 220 wpm matches the typical "tech blog reader" benchmark used by
    Medium / Substack — high enough to not feel padded, low enough that a
    skimmer can still trust the number on a quick read.
    """
    words = len(re.findall(r"\b\w+\b", body_md or ""))
    if words <= 0:
        return 1
    return max(1, round(words / wpm))


# Module-level cache for category-name → documentId. Strapi categories are
# small (<50 rows) and rarely change; pulling them once per process avoids
# re-hitting /api/categories for every article in a batch run.
_CATEGORY_DOCUMENT_ID_CACHE: dict[str, str] | None = None


def _load_category_index(base_url: str, token: str) -> dict[str, str]:
    """Fetch /api/categories once and return a {lowercased_name: documentId} map.

    Caches a successful result for the rest of the process lifetime. A transient
    fetch failure (network hiccup, expired token, Strapi restart) is NOT cached —
    we return an empty dict to the caller so it omits `category` for that one
    payload, but the next call retries the fetch. PLEAA-457 (Greptile P1): the
    earlier shape cached the empty dict on failure too, which permanently
    disabled category resolution for the rest of a batch run and silently
    published every later article without a category — exactly the silent-
    failure pattern this PR was written to close.
    """
    global _CATEGORY_DOCUMENT_ID_CACHE
    if _CATEGORY_DOCUMENT_ID_CACHE is not None:
        return _CATEGORY_DOCUMENT_ID_CACHE

    import urllib.request

    endpoint = f"{base_url.rstrip('/')}/api/categories?pagination[limit]=100"
    req = urllib.request.Request(
        endpoint,
        headers={"Authorization": f"Bearer {token}"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        items = data.get("data") if isinstance(data, dict) else None
        index: dict[str, str] = {}
        if isinstance(items, list):
            for entry in items:
                if not isinstance(entry, dict):
                    continue
                name = entry.get("name") or (entry.get("attributes") or {}).get("name")
                doc_id = entry.get("documentId") or (entry.get("attributes") or {}).get("documentId")
                if isinstance(name, str) and isinstance(doc_id, str):
                    index[name.strip().lower()] = doc_id
        _CATEGORY_DOCUMENT_ID_CACHE = index
        return index
    except Exception as exc:
        sys.stderr.write(f"warning: category index fetch failed: {exc}\n")
        # Intentionally do NOT write the cache here — let the next call retry.
        return {}


def resolve_category_document_id(name: str) -> str | None:
    """Resolve a human-readable category name to a Strapi v5 documentId.

    Requires STRAPI_BASE_URL + STRAPI_API_TOKEN (silently returns None if absent
    so dry-runs that just write the JSON package don't fail).
    """
    base_url = os.environ.get("STRAPI_BASE_URL")
    token = os.environ.get("STRAPI_API_TOKEN")
    if not base_url or not token or not name:
        return None
    index = _load_category_index(base_url, token)
    return index.get(name.strip().lower())


def extract_cover_image_url(body_md: str, base_url: str | None) -> str | None:
    """Pick a cover image URL from the body. We prefer the first image whose ref
    we can resolve to an absolute URL — i.e. either already absolute, or under
    `images/` once `base_url` is known so we can rewrite to `<base>/uploads/<file>`.

    Returns None when no image is referenced or no rewrite target is available
    (caller should then omit `cover_image_url` from the payload).
    """
    # Absolute URL in the markdown wins outright. We accept any http(s) URL
    # inside an image-markdown link rather than gating on a known file extension —
    # CDN-hosted images (Cloudinary, imgix, Strapi /uploads/, signed URLs) commonly
    # omit extensions and the previous extension-gated regex silently dropped them
    # (PLEAA-457 Greptile P3).
    abs_match = re.search(r"!\[[^\]]*\]\((https?://[^)\s]+)\)", body_md)
    if abs_match:
        return abs_match.group(1)
    # Otherwise fall back to the first uploaded local image, if we have a base.
    if not base_url:
        return None
    rel_match = IMAGE_REF_RE.search(body_md)
    if not rel_match:
        return None
    filename = Path(rel_match.group(2)).name
    return f"{base_url.rstrip('/')}/uploads/{filename}"


def build_payload(
    slug: str,
    title: str,
    body_md: str,
    *,
    published_at: str | None = None,
    category_name: str = "AI Companions",
    author_name: str = "Pleasur.AI Team",  # noqa: ARG001 — kept for backwards compat with callers; not in v5 schema
    cover_image_url: str | None = None,    # noqa: ARG001 — same as above
) -> dict:
    """Build a Strapi v5 article payload.

    v5 schema (verified end-to-end on 2026-05-07 by live POST/GET/DELETE
    against production Strapi — see ``scripts/_smoke_integrations.py::strapi_v5_shape``):

      - title:        string
      - slug:         string (unique)
      - description:  short summary, hard-capped at 80 chars
      - blocks[]:     component array — at minimum one shared.rich-text with
                      the full markdown body in `body`
      - category:     documentId STRING (not array, not numeric id). Resolved
                      by name from Strapi when STRAPI_BASE_URL + STRAPI_API_TOKEN
                      are set; omitted otherwise so the package still serialises
                      in dry-runs.
      - publishedAt:  ISO timestamp to publish live, null for draft.

    Strict-mode rejection list (PLEAA-457, 2026-05-07): the live Strapi
    rejects unknown keys with HTTP 400 ``Invalid key <name>``. Fields that
    looked plausible but are NOT in the schema and would fail every POST:
    ``author_name``, ``read_time``, ``readTime``, ``cover_image_url``,
    ``coverImage``, ``tags``, ``excerpt``, ``content``. ``author`` and
    ``cover`` exist as relations to the Author / Media content-types but
    require numeric/documentId references (not strings) and are out of
    scope for the auto-publish path — they're set manually in the admin
    when needed.

    SEO metadata (DOD#4, resolved 2026-05-07): the Article content-type
    does NOT expose a ``seo`` field, ``seo`` component, or separate
    ``/api/seos`` collection (verified — populate=seo and /api/seos both
    return 400/404). ``title`` + ``description`` ARE the SEO surface: the
    frontend renders ``<title>`` from ``title`` and ``<meta name="description">``
    from ``description`` (hence the 80-char cap matching Google's mobile
    snippet ceiling). If a richer SEO model is ever needed, add a ``seo``
    component to the Article type in Strapi admin first; do not pre-emit it.

    The ``author_name`` and ``cover_image_url`` parameters are kept on the
    function signature for backwards compatibility with existing callers
    (notably ``main()`` and any orchestrator override) but are intentionally
    NOT emitted into the payload. ``compute_read_time`` is similarly retained
    for callers that want to surface a read-time number in the publish
    package's README, but the value never crosses the wire to Strapi.
    """
    description_source = extract_excerpt(body_md) or title
    description = truncate_description(description_source, limit=80)

    blocks = [
        {
            "__component": "shared.rich-text",
            "body": body_md.strip() + "\n",
        }
    ]

    payload: dict = {
        "data": {
            "title": title,
            "slug": slug,
            "description": description,
            "blocks": blocks,
            "publishedAt": published_at,
        }
    }

    category_document_id = resolve_category_document_id(category_name)
    if category_document_id:
        payload["data"]["category"] = category_document_id

    return payload


def find_image_refs(md: str) -> list[tuple[str, str]]:
    """Return list of (alt, relative-path-from-content-pipeline)."""
    return [(m.group(1), m.group(2)) for m in IMAGE_REF_RE.finditer(md)]


def copy_images_to_publish(out_dir: Path, refs: list[tuple[str, str]]) -> list[Path]:
    """Copy referenced images into <out_dir>/media/, return the absolute paths."""
    if not refs:
        return []
    media_dir = out_dir / "media"
    media_dir.mkdir(parents=True, exist_ok=True)
    copied: list[Path] = []
    for _, rel in refs:
        src = ROOT / "content-pipeline" / rel
        if not src.exists():
            sys.stderr.write(f"warning: missing image {src}\n")
            continue
        dest = media_dir / src.name
        try:
            dest.write_bytes(src.read_bytes())
            copied.append(dest)
        except OSError as exc:
            sys.stderr.write(f"warning: copy failed {src}: {exc}\n")
    return copied


def upload_to_strapi_media(image_paths: list[Path], base_url: str, token: str) -> dict[str, int]:
    """POST each image to /api/upload, return mapping of filename -> media id."""
    if not image_paths:
        return {}
    try:
        import urllib.request
        import uuid
        import mimetypes
    except ImportError as exc:
        sys.stderr.write(f"warning: stdlib missing for media upload ({exc}); skipping\n")
        return {}

    endpoint = f"{base_url.rstrip('/')}/api/upload"
    out: dict[str, int] = {}
    for path in image_paths:
        boundary = uuid.uuid4().hex
        mime = mimetypes.guess_type(path.name)[0] or "image/png"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="files"; filename="{path.name}"\r\n'
            f"Content-Type: {mime}\r\n\r\n"
        ).encode("utf-8")
        body += path.read_bytes() + f"\r\n--{boundary}--\r\n".encode("utf-8")
        req = urllib.request.Request(
            endpoint,
            data=body,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": f"multipart/form-data; boundary={boundary}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            if isinstance(data, list) and data:
                first = data[0]
                if isinstance(first, dict) and "id" in first:
                    out[path.name] = int(first["id"])
        except Exception as exc:
            sys.stderr.write(f"warning: upload failed for {path.name}: {exc}\n")
    return out


def rewrite_image_refs(md: str, base_url: str | None) -> str:
    """If we have a Strapi base URL, rewrite local image refs to absolute Strapi-served URLs.
    Otherwise leave them as-is so the editor can drag from media/ folder."""
    if not base_url:
        return md
    base = base_url.rstrip("/")

    def _rewrite(match: "re.Match[str]") -> str:
        alt = match.group(1)
        rel = match.group(2)
        filename = Path(rel).name
        return f"![{alt}]({base}/uploads/{filename})"

    return IMAGE_REF_RE.sub(_rewrite, md)


def write_outputs(slug: str, body_md: str, payload: dict) -> Path:
    out_dir = OUT_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "article.md").write_text(body_md.strip() + "\n", encoding="utf-8")
    (out_dir / "article.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    data = payload["data"]
    body_text = data["blocks"][0]["body"] if data.get("blocks") else ""
    word_count = len(re.findall(r"\b\w+\b", body_text))
    category_value = data.get("category") or "(unresolved — set STRAPI_BASE_URL + STRAPI_API_TOKEN)"
    read_time_min = compute_read_time(body_text)
    readme = f"""# Publish package — {data['title']}

Generated by /format-for-publish. Strapi v5 schema (PLEAA-457). Two ways to use this:

## Option A — paste into Strapi admin (no API needed)
1. Open Strapi admin → Content Manager → create a new Article
2. Title: {data['title']}
3. Slug: {data['slug']}
4. Description (≤80 chars): {data['description']}
5. Blocks: paste the contents of `article.md` into a `shared.rich-text` block
6. Category (documentId): {category_value}
7. Author / cover: attach manually in admin if desired (relations, not strings)
8. Save as draft, review, then publish

## Option B — direct API publish (when Doppler creds are wired)
```bash
doppler run -- python .claude/skills/format-for-publish/scripts/format_for_strapi.py {slug} --publish
```
Requires STRAPI_BASE_URL and STRAPI_API_TOKEN env vars.

## Files
- `article.md` — clean markdown body (paste in Strapi rich-text block)
- `article.json` — Strapi v5 payload (for API publish)
- `README.md` — this file

## Stats
- Word count: {word_count}
- Description length: {len(data['description'])} chars (cap 80)
- Read time: ~{read_time_min} min (computed at 220 wpm; informational only — not in payload)
- Blocks: {len(data.get('blocks', []))}
"""
    (out_dir / "README.md").write_text(readme, encoding="utf-8")
    return out_dir


def find_existing_article_id(base_url: str, token: str, slug: str) -> str | None:
    """Look up the Strapi v5 article documentId for a slug.

    Strapi v5 routes entity URLs by documentId (string), not numeric id, so
    we return that here. Returns None if not found.
    """
    import urllib.parse
    import urllib.request

    endpoint = f"{base_url.rstrip('/')}/api/articles?filters[slug][$eq]={urllib.parse.quote(slug)}"
    req = urllib.request.Request(
        endpoint,
        headers={"Authorization": f"Bearer {token}"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        items = data.get("data") if isinstance(data, dict) else None
        if isinstance(items, list) and items:
            entry = items[0]
            if isinstance(entry, dict):
                # v5 places documentId at the top level; some Strapi configs
                # still mirror it under attributes.
                doc_id = entry.get("documentId") or (entry.get("attributes") or {}).get("documentId")
                if isinstance(doc_id, str) and doc_id:
                    return doc_id
    except Exception as exc:
        sys.stderr.write(f"warning: lookup of slug {slug!r} failed: {exc}\n")
    return None


def publish_to_strapi(payload: dict, *, update: bool = False) -> None:
    """Push payload to Strapi.

    POST to /api/articles by default. If `update=True`, looks up the existing
    article by slug and PUTs /api/articles/{documentId} instead. Strapi v5
    uses PUT for updates with full-replacement semantics — fields not present
    in the payload are wiped on the server. Callers that want to preserve
    admin-edited fields (e.g. a manually attached cover image) must include
    those fields in the update payload, or POST a brand-new article instead.
    PLEAA-457 (Greptile P2): the original docstring + PR description called
    this "PATCH" which is a v4 idiom and misleads anyone reading the code.

    Update-path safety guard (PLEAA-457 Greptile P1, round 2): on the PUT path,
    if ``payload.data.category`` is missing we abort instead of sending the
    request. Strapi's PUT semantics would otherwise WIPE the article's existing
    category server-side, which is exactly the silent destructive-failure class
    this PR was opened to close. The most common cause is a transient
    ``/api/categories`` fetch failure inside ``_load_category_index``; the
    cache stays ``None`` so the next run retries cleanly, but only if we don't
    let this PUT through. POSTs are still allowed without ``category`` (a
    brand-new article without a category is recoverable in admin; an existing
    one having its category wiped is not).
    """
    base_url = os.environ.get("STRAPI_BASE_URL")
    token = os.environ.get("STRAPI_API_TOKEN")
    if not base_url or not token:
        sys.exit("error: STRAPI_BASE_URL and STRAPI_API_TOKEN env vars required for --publish")
    try:
        import urllib.request
    except ImportError:
        sys.exit("error: stdlib urllib unavailable (impossible on stdlib Python)")

    method = "POST"
    endpoint = f"{base_url.rstrip('/')}/api/articles"
    if update:
        slug = payload.get("data", {}).get("slug")
        if not slug:
            sys.exit("error: --update requires payload to have data.slug")
        existing_doc_id = find_existing_article_id(base_url, token, slug)
        if existing_doc_id is None:
            sys.stderr.write(f"warning: --update set but slug {slug!r} not found in Strapi; falling back to POST\n")
        else:
            # Refuse to PUT when category resolution failed — see docstring.
            if not (payload.get("data") or {}).get("category"):
                sys.exit(
                    "error: --update with missing data.category — refusing to PUT.\n"
                    "  Strapi v5 PUT is full-replacement; sending this would wipe the\n"
                    "  existing article's category server-side. Most likely cause: a\n"
                    "  transient /api/categories fetch failure in _load_category_index.\n"
                    "  Re-run when Strapi is reachable; the category cache resets per\n"
                    "  process so the next run will retry cleanly."
                )
            method = "PUT"
            endpoint = f"{base_url.rstrip('/')}/api/articles/{existing_doc_id}"

    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"{'updated' if method == 'PUT' else 'published'} — {resp.status} {resp.reason}")
            print(resp.read().decode("utf-8"))
    except Exception as e:
        sys.exit(f"error: Strapi {method} failed: {e}")


# ---------- GitHub-Pages whiteboard staging (PLEAA-448) ----------
# After format-for-publish writes the Strapi package, also bake a static
# `docs/run-<slug>.html` viewer and append the slug to the fallback runs
# array in `docs/index.html` so the run shows up at
# https://lionelndong.github.io/blog-agent-2/ as soon as the operator pushes
# `main`. The GitHub-API enumeration path in index.html is rate-limited and
# unreliable, so the static fallback is the source of truth.
#
# This step is best-effort: a failure here must NOT fail the publish run —
# the publish package is the primary deliverable and the operator can
# always run `python scripts/bundle_viewer.py <slug>` manually.

# The fallback runs array is a JS literal on a single line in docs/index.html.
# We match it loosely so we tolerate whitespace/newline drift but require the
# array to be the one inside the `catch` block (the only `return [...]` of
# string-literals followed by `;` in the file).
_FALLBACK_RUNS_RE = re.compile(
    r'(return\s*\[)([^\]]*?)(\]\s*;)',
)


def _update_index_fallback(slug: str) -> tuple[bool, str]:
    """Idempotently append slug to the fallback runs array in docs/index.html.

    Returns (changed, message). Never raises.
    """
    if not INDEX_HTML.exists():
        return False, f"docs/index.html not found at {INDEX_HTML}"
    try:
        html = INDEX_HTML.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"read error: {e}"

    match = _FALLBACK_RUNS_RE.search(html)
    if not match:
        return False, "fallback runs array not found in docs/index.html"

    body = match.group(2)
    # Existing slugs are quoted strings; cheap parse via regex.
    existing = re.findall(r'"([^"]+)"', body)
    if slug in existing:
        return False, f"slug already in fallback runs ({len(existing)} entries)"

    new_list = existing + [slug]
    rendered = ", ".join(f'"{s}"' for s in new_list)
    new_body = match.group(1) + rendered + match.group(3)
    new_html = html[: match.start()] + new_body + html[match.end():]
    try:
        INDEX_HTML.write_text(new_html, encoding="utf-8")
    except Exception as e:
        return False, f"write error: {e}"
    return True, f"appended to fallback runs ({len(new_list)} entries)"


def _bundle_run_viewer(slug: str) -> tuple[bool, str]:
    """Run scripts/bundle_viewer.py to write docs/run-<slug>.html. Never raises."""
    if not BUNDLE_VIEWER.exists():
        return False, f"bundle_viewer.py not found at {BUNDLE_VIEWER}"
    try:
        proc = subprocess.run(
            [sys.executable, str(BUNDLE_VIEWER), slug],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=60,
        )
    except Exception as e:
        return False, f"subprocess failed: {e}"
    if proc.returncode != 0:
        return False, f"bundle_viewer exit {proc.returncode}: {proc.stderr.strip()[:200]}"
    out_path = DOCS_DIR / f"run-{slug}.html"
    if not out_path.exists():
        return False, f"bundle_viewer ran but {out_path} missing"
    return True, f"wrote {out_path.relative_to(ROOT)} ({out_path.stat().st_size:,} bytes)"


def stage_whiteboard(slug: str) -> None:
    """Stage the GitHub-Pages whiteboard artifacts for `slug`.

    Idempotent: re-running for the same slug overwrites the bundle and
    leaves the index untouched if the slug is already in the fallback list.
    Best-effort: failures print a warning but never raise.
    """
    print(f"\n--- whiteboard staging for {slug} ---")
    bundled, bmsg = _bundle_run_viewer(slug)
    print(f"  bundle: {'ok' if bundled else 'skipped'} — {bmsg}")

    if not bundled:
        print(
            "  hint: run `python scripts/bundle_viewer.py "
            f"{slug}` manually to regenerate the static viewer."
        )
        return

    indexed, imsg = _update_index_fallback(slug)
    print(f"  index:  {'updated' if indexed else 'unchanged'} — {imsg}")

    # Best-effort `git add` so the operator just has to commit + push.
    paths_to_stage = [DOCS_DIR / f"run-{slug}.html"]
    if indexed:
        paths_to_stage.append(INDEX_HTML)
    try:
        rels = [str(p.relative_to(ROOT)) for p in paths_to_stage]
        proc = subprocess.run(
            ["git", "add", "--", *rels],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=20,
        )
        if proc.returncode == 0:
            print(f"  staged: {', '.join(rels)}")
            print(
                "  hint: commit + push `main` to surface this run on "
                "https://lionelndong.github.io/blog-agent-2/"
            )
        else:
            # Non-fatal: maybe not a git repo, or git missing. Just tell the
            # operator the file paths so they can stage manually.
            print(
                "  staged: git add skipped — "
                f"{proc.stderr.strip()[:120] or 'non-zero exit'}"
            )
            print(f"  files: {', '.join(rels)}")
    except Exception as e:
        rels = [str(p.relative_to(ROOT)) for p in paths_to_stage]
        print(f"  staged: git add unavailable ({e}); files: {', '.join(rels)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug")
    parser.add_argument("--publish", action="store_true", help="Direct API publish (requires STRAPI_BASE_URL + STRAPI_API_TOKEN)")
    parser.add_argument("--auto-publish", action="store_true", help="Set publishedAt = now (live publish, not draft). Implies --publish. Requires quality-check verdict != FAIL.")
    parser.add_argument("--update", action="store_true", help="PUT the existing Strapi article by slug instead of POST (full-replacement semantics — fields absent from the payload get wiped). For /update-pipeline runs.")
    args = parser.parse_args()

    auto_publish = args.auto_publish or os.environ.get("BLOG_AGENT_AUTO_PUBLISH") == "1"
    publish_via_api = args.publish or auto_publish  # auto-publish implies --publish

    if auto_publish:
        allow, reason = quality_precondition(args.slug)
        if not allow:
            sys.exit(f"error: auto-publish refused — {reason}")
        else:
            print(f"quality-check precondition passed ({reason})")

    raw = read_draft(args.slug)
    no_notes = strip_editor_notes(raw)
    title, body = extract_title(no_notes)
    body = transform_callouts(body)

    # Hard-fail gate: never ship a publish package containing raw [VISUAL:...] /
    # [SCREENSHOT:...] template syntax. Neo, PLEAA-392 (2026-05-06): the visuals
    # stage is responsible for substituting these into ![alt](path) markdown OR
    # routing to manual capture; if any leftover survives to format-for-publish,
    # halt rather than ship template syntax to readers.
    leftover_visuals = re.findall(r"\[VISUAL:[^\]]+\]|\[SCREENSHOT:[^\]]+\]", body)
    if leftover_visuals:
        first = leftover_visuals[0][:140] + ("…" if len(leftover_visuals[0]) > 140 else "")
        sys.exit(
            f"error: refusing to write publish package — {len(leftover_visuals)} naked "
            f"[VISUAL:...] / [SCREENSHOT:...] placeholder(s) in cited draft.\n"
            f"  first: {first}\n"
            f"  fix: re-run /generate-visuals (or /capture-visuals for action-shots) "
            f"so every placeholder produces a real asset and the draft references it via ![alt](path)."
        )

    # Always copy referenced images into the publish folder so the editor can paste manually
    image_refs = find_image_refs(body)
    out_dir = OUT_DIR / args.slug
    out_dir.mkdir(parents=True, exist_ok=True)
    copied_images = copy_images_to_publish(out_dir, image_refs)

    base_url = os.environ.get("STRAPI_BASE_URL")
    token = os.environ.get("STRAPI_API_TOKEN")

    if publish_via_api and base_url and token and copied_images:
        media_map = upload_to_strapi_media(copied_images, base_url, token)
        if media_map:
            print(f"uploaded {len(media_map)} images to Strapi media library")
        body = rewrite_image_refs(body, base_url)

    published_at = datetime.now(timezone.utc).isoformat() if auto_publish else None
    cover_image_url = extract_cover_image_url(body, base_url)
    payload = build_payload(
        args.slug,
        title,
        body,
        published_at=published_at,
        cover_image_url=cover_image_url,
    )
    out_dir = write_outputs(args.slug, body, payload)
    print(f"wrote {out_dir}/article.md")
    print(f"wrote {out_dir}/article.json")
    print(f"wrote {out_dir}/README.md")
    if copied_images:
        print(f"copied {len(copied_images)} image(s) to {out_dir / 'media'}")

    if publish_via_api:
        publish_to_strapi(payload, update=args.update)

    # PLEAA-448: bake the static GitHub-Pages viewer + index entry so the run
    # surfaces at https://lionelndong.github.io/blog-agent-2/ as soon as the
    # operator pushes `main`. Best-effort — never blocks publish.
    if os.environ.get("BLOG_AGENT_SKIP_WHITEBOARD") != "1":
        stage_whiteboard(args.slug)


if __name__ == "__main__":
    main()
