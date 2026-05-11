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

# PLEAA-524: editorial category taxonomy. Strapi is the source of truth for the
# `name` strings — keep this list aligned with /api/categories. The publisher
# pipeline routes a cited draft to a category via three signals (in order):
#
#   1. An explicit `category:` line in the cited draft's frontmatter or
#      `## Editor notes` block. Wins outright when present.
#   2. A slug-pattern heuristic — `*-review*` → Reviews, `*-guide*` → Guides,
#      keyword markers like `uncensored`/`no-filter`/`nsfw`/`dirty` → Uncensored.
#   3. Default: AI Companions (the brand-categorical bucket).
#
# Out of scope here (PLEAA-524): tag taxonomy, multi-category posts, or the
# auto-creation of new categories on Strapi when an unknown name is referenced —
# the resolver in this file silently omits `category` for unknown names rather
# than POSTing a new category. Operators add categories in the Strapi admin and
# the next publish picks them up via the existing /api/categories cache.
CATEGORY_DEFAULT = "AI Companions"
CATEGORY_KNOWN = {"AI Companions", "Reviews", "Guides", "Uncensored"}

# Regex catching `category: <name>` either in YAML-style frontmatter at the top
# of the draft or inside an `## Editor notes` block. Multi-word names are fine
# (the value is everything up to end-of-line, then trimmed).
CATEGORY_FRONTMATTER_RE = re.compile(
    r"^\s*category\s*:\s*(.+?)\s*$",
    re.MULTILINE | re.IGNORECASE,
)


def _slug_to_category_heuristic(slug: str) -> str:
    """Pick a category for a slug when no explicit override is present.

    Lower-cased slug matched in priority order: review → Reviews,
    uncensored / no-filter / nsfw / dirty → Uncensored, guide → Guides,
    everything else → AI Companions. Heuristic is deliberately conservative;
    operators override via `category:` in the draft when this gets it wrong.
    """
    s = slug.lower()
    if "review" in s:
        return "Reviews"
    if any(tok in s for tok in ("uncensored", "no-filter", "nofilter", "nsfw", "dirty")):
        return "Uncensored"
    if "guide" in s or s.startswith("how-to-"):
        return "Guides"
    return CATEGORY_DEFAULT


def resolve_category_name(slug: str, raw_md: str) -> str:
    """Return the human-readable category name to send to Strapi for `slug`.

    Reads an explicit `category: <name>` declaration anywhere in the raw cited
    draft (frontmatter or editor-notes section) before falling back to the
    slug-pattern heuristic. The result MUST be one of CATEGORY_KNOWN — anything
    else is logged and replaced with the heuristic so a typo can't silently
    publish under an unknown bucket. Strapi-side resolution still validates by
    fetching /api/categories; an unknown name is dropped from the payload.
    """
    m = CATEGORY_FRONTMATTER_RE.search(raw_md)
    if m:
        candidate = m.group(1).strip()
        canonical = next(
            (k for k in CATEGORY_KNOWN if k.casefold() == candidate.casefold()),
            None,
        )
        if canonical:
            return canonical
        sys.stderr.write(
            f"warning: cited draft requested unknown category {candidate!r}; "
            f"falling back to slug heuristic. Known: {sorted(CATEGORY_KNOWN)}\n"
        )
    return _slug_to_category_heuristic(slug)


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


def resolve_cover_file_id(body_md: str, media_map: dict[str, dict] | None) -> int | None:
    """Return the Strapi upload id for the article's hero image, or None.

    PLEAA-570 (2026-05-11): on auto-publish, ``article.cover`` was being left
    null because the payload only carried images inside dynamic-zone
    ``shared.media`` blocks. The public blog page kept rendering because
    Next.js resolves the hero from a slug-derived CDN URL convention, but
    every other consumer of ``cover`` (RSS, OG tags, social cards, admin
    preview) saw nothing. We pick the same asset ``extract_cover_image_url``
    would surface — the first uploaded image referenced in the body — and
    attach it as the article's cover relation in :func:`build_payload`.

    Selection mirrors :func:`build_blocks`: the body has already been
    rewritten by :func:`rewrite_image_refs` by the time we get here, so
    image refs are absolute Strapi URLs. Index ``media_map`` by URL and look
    up the first absolute image ref in the body. Returns None when the body
    has no images we uploaded (dry-run, unconfigured Strapi, or article with
    only inline cover URLs we didn't upload) — caller should then omit
    ``cover`` from the payload.
    """
    if not media_map:
        return None
    by_url: dict[str, int] = {}
    for entry in media_map.values():
        url = entry.get("url")
        fid = entry.get("id")
        if url and isinstance(fid, int):
            by_url[url] = fid
    if not by_url:
        return None
    abs_match = re.search(r"!\[[^\]]*\]\((https?://[^)\s]+)\)", body_md)
    if abs_match:
        fid = by_url.get(abs_match.group(1))
        if isinstance(fid, int):
            return fid
    return None


def build_blocks(body_md: str, media_map: dict[str, dict] | None = None) -> list[dict]:
    """Split body markdown into alternating ``shared.rich-text`` and ``shared.media`` blocks.

    The renderer Neo runs (Pleasur.ai blog frontend) only displays media that
    lives inside its own ``shared.media`` block — images embedded inside a
    single rich-text block aren't rendered as ``<img>`` (PLEAA-528 2026-05-08).
    To make every uploaded image actually appear on the published page, we
    walk the body and emit a fresh block whenever an image ref sits on a line
    by itself:

      - whole-line ``![alt](https://media.strapiapp.com/foo.png)`` and the
        URL is one we just uploaded → emit ``shared.media`` with the file id
        and drop the markdown line
      - everything else → accumulate into the current ``shared.rich-text``

    When ``media_map`` is empty or no whole-line image refs match it, this
    function returns a single rich-text block containing the full body —
    same behaviour as the pre-PLEAA-528 emitter, so dry-runs and unconfigured
    Strapi targets keep working unchanged.

    The ``media_map`` is the same one ``upload_to_strapi_media`` returns:
    ``{filename: {"id": <int>, "url": <absolute_url>}}``. We index it by the
    absolute Strapi URL because ``rewrite_image_refs`` has already replaced
    local paths with the absolute Strapi Cloud media URLs by the time we get
    here.
    """
    if not media_map:
        return [{"__component": "shared.rich-text", "body": body_md.strip() + "\n"}]

    # Index by absolute URL (the form rewrite_image_refs leaves in the body).
    by_url: dict[str, int] = {}
    for entry in media_map.values():
        url = entry.get("url")
        fid = entry.get("id")
        if url and isinstance(fid, int):
            by_url[url] = fid

    if not by_url:
        return [{"__component": "shared.rich-text", "body": body_md.strip() + "\n"}]

    # Match a line that is *only* a markdown image — possibly with surrounding
    # whitespace. Avoid matching images embedded inside a paragraph.
    whole_line_image = re.compile(r"^\s*!\[[^\]]*\]\(([^)]+)\)\s*$")

    blocks: list[dict] = []
    buf: list[str] = []

    def flush_text() -> None:
        text = "\n".join(buf).strip()
        buf.clear()
        if text:
            blocks.append({"__component": "shared.rich-text", "body": text + "\n"})

    for line in body_md.splitlines():
        m = whole_line_image.match(line)
        if not m:
            buf.append(line)
            continue
        file_id = by_url.get(m.group(1))
        if file_id is None:
            # Image we didn't upload (e.g. inline cover URL) — leave inline.
            buf.append(line)
            continue
        flush_text()
        # PLEAA-567 (2026-05-11): Strapi v5 silently drops a component-scoped
        # media relation when ``file`` is sent as a bare integer — the row is
        # created but ``file`` populates as null on the next read, so the
        # frontend has nothing to <img>. The fix is to send the relation as
        # ``{"id": <fileId>}`` (the object form Strapi's connect resolver
        # accepts on PUT and POST alike). Verified live by PUTting
        # is-having-an-ai-girlfriend-cheating (documentId
        # ur4ey6i9cuewnfpa9ygx2egb) — all 7 media blocks went from file:null
        # to fully populated after the shape switch.
        blocks.append({"__component": "shared.media", "file": {"id": file_id}})

    flush_text()

    # Defensive fallback: if for some reason every line was an image-only line
    # (or all matched nothing), don't emit an empty block list — Strapi will 400.
    if not blocks:
        return [{"__component": "shared.rich-text", "body": body_md.strip() + "\n"}]

    return blocks


def build_payload(
    slug: str,
    title: str,
    body_md: str,
    *,
    published_at: str | None = None,
    category_name: str = "AI Companions",
    author_name: str = "Pleasur.AI Team",  # noqa: ARG001 — kept for backwards compat with callers; not in v5 schema
    cover_image_url: str | None = None,    # noqa: ARG001 — same as above
    media_map: dict[str, dict] | None = None,
    cover_file_id: int | None = None,
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
    ``cover`` exist as relations to the Author / Media content-types and
    require numeric upload ids (not strings).

    Cover relation (PLEAA-570, 2026-05-11): when ``cover_file_id`` is set,
    the article-level ``cover`` relation is included in the payload so
    consumers that read ``article.cover`` directly (RSS feed, social cards,
    OG tags, admin preview UI) resolve the same hero image the public page
    renders. Before PLEAA-570, auto-published articles left ``cover`` null
    and the public page only worked because Next.js synthesized the hero
    URL from a slug-derived CDN convention. ``cover`` is emitted as a bare
    integer (Strapi v5 single-media field), matching the upload response's
    ``id`` from :func:`upload_to_strapi_media`. Author is still out of
    scope and set manually in admin.

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

    # PLEAA-528 (2026-05-08): when images were uploaded to Strapi, split the
    # body into alternating shared.rich-text + shared.media blocks so the
    # frontend actually renders each image. Falls back to single-block when
    # no media_map (dry-run, unconfigured Strapi, or article with no images).
    blocks = build_blocks(body_md, media_map)

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

    # PLEAA-570 (2026-05-11): attach the article-level cover relation so
    # admin preview / RSS / OG tags / social cards resolve the hero from the
    # canonical ``article.cover`` field instead of relying on the brittle
    # slug-derived URL convention the public page falls back to. Emit only
    # when we have a real upload id — Strapi v5 rejects unknown relations
    # silently (would store null) but accepts a bare integer for single
    # media fields.
    if isinstance(cover_file_id, int) and cover_file_id > 0:
        payload["data"]["cover"] = cover_file_id

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


def upload_to_strapi_media(image_paths: list[Path], base_url: str, token: str) -> dict[str, dict]:
    """POST each image to /api/upload, return mapping of filename -> {id, url}.

    Strapi Cloud rewrites uploaded asset URLs to a separate media subdomain
    (e.g. ``media.strapiapp.com/<file>_<hash>.png``) instead of serving them
    from ``{base_url}/uploads/<filename>``. We must trust the ``url`` field
    that Strapi returns from /api/upload — synthesizing /uploads/ paths
    produces 404s on Strapi Cloud (PLEAA-499 followup, 2026-05-08).
    """
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
    base = base_url.rstrip("/")
    out: dict[str, dict] = {}
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
                    rel_url = first.get("url") or ""
                    # Strapi Cloud returns absolute URLs (https://...media.strapiapp.com/...);
                    # self-hosted returns paths like "/uploads/<file>". Make absolute either way.
                    if rel_url.startswith("//"):
                        full_url = f"https:{rel_url}"
                    elif rel_url.startswith("http"):
                        full_url = rel_url
                    elif rel_url:
                        full_url = f"{base}{rel_url if rel_url.startswith('/') else '/' + rel_url}"
                    else:
                        # Fallback to legacy /uploads/<name> guess; will likely 404 on Strapi Cloud.
                        full_url = f"{base}/uploads/{path.name}"
                    out[path.name] = {"id": int(first["id"]), "url": full_url}
        except Exception as exc:
            sys.stderr.write(f"warning: upload failed for {path.name}: {exc}\n")
    return out


def rewrite_image_refs(md: str, base_url: str | None, media_map: dict[str, dict] | None = None) -> str:
    """Rewrite local image refs to absolute Strapi-served URLs.

    Prefers the ``url`` returned by ``/api/upload`` (correct for Strapi Cloud's
    separate media subdomain). Falls back to ``{base}/uploads/<filename>`` only
    when no upload entry exists for that filename. Without a base URL, leaves
    refs alone so the editor can drag from the publish package's ``media/``.
    """
    if not base_url:
        return md
    base = base_url.rstrip("/")
    media_map = media_map or {}

    def _rewrite(match: "re.Match[str]") -> str:
        alt = match.group(1)
        rel = match.group(2)
        filename = Path(rel).name
        entry = media_map.get(filename)
        if entry and entry.get("url"):
            return f"![{alt}]({entry['url']})"
        return f"![{alt}]({base}/uploads/{filename})"

    return IMAGE_REF_RE.sub(_rewrite, md)


def write_outputs(slug: str, body_md: str, payload: dict) -> Path:
    out_dir = OUT_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "article.md").write_text(body_md.strip() + "\n", encoding="utf-8")
    (out_dir / "article.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    data = payload["data"]
    # PLEAA-567: blocks may start with a `shared.media` (when the draft opens
    # with an uploaded image), which has no `body`. Pull stats from the first
    # `shared.rich-text` block instead of indexing position 0 blindly.
    first_rt = next(
        (b for b in data.get("blocks", []) if b.get("__component") == "shared.rich-text"),
        None,
    )
    body_text = first_rt.get("body", "") if first_rt else ""
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
7. Author: attach manually in admin if desired. Cover relation auto-attached on `--auto-publish` to the first uploaded image (PLEAA-570)
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

    media_map: dict[str, dict] = {}
    if publish_via_api and base_url and token and copied_images:
        media_map = upload_to_strapi_media(copied_images, base_url, token)
        if media_map:
            print(f"uploaded {len(media_map)} images to Strapi media library")
    body = rewrite_image_refs(body, base_url if (base_url and media_map) else None, media_map)

    published_at = datetime.now(timezone.utc).isoformat() if auto_publish else None
    cover_image_url = extract_cover_image_url(body, base_url)
    # PLEAA-570: pick the upload id of the hero image so build_payload can
    # set the top-level ``cover`` relation. Mirrors extract_cover_image_url's
    # selection (first absolute image ref) so the cover stays in sync with
    # what the body shows.
    cover_file_id = resolve_cover_file_id(body, media_map)
    if cover_file_id is not None:
        print(f"cover relation resolved: upload id {cover_file_id}")
    # PLEAA-524: resolve category from the raw cited draft (frontmatter wins,
    # slug-heuristic fallback). `raw` carries the editor-notes block intact —
    # we resolve before strip_editor_notes() above already ran (`raw` is
    # untouched), but downstream `body` is already cleaned, so reach for `raw`.
    category_name = resolve_category_name(args.slug, raw)
    print(f"category resolved: {category_name}")
    payload = build_payload(
        args.slug,
        title,
        body,
        published_at=published_at,
        category_name=category_name,
        cover_image_url=cover_image_url,
        media_map=media_map,
        cover_file_id=cover_file_id,
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
