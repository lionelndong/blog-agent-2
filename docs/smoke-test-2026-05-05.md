# Smoke Test — 2026-05-05

Branch: `claude/smoke-test-pipeline-o1D7G`
Goal: validate the pipeline scaffold without burning Semrush / OpenRouter / Replicate quota, and inventory which integrations are actually wired up in this environment.

## What was checked

| Check | Method | Result |
|---|---|---|
| Integration auth | `python scripts/_smoke_integrations.py` | 0 / 4 PASS — all four providers report no key in env |
| Slugify helper | `python scripts/slugify.py "smoke test pipeline"` | OK → `smoke-test-pipeline` |
| Pipeline status helper | `python scripts/pipeline_status.py smoke-test-pipeline` | OK — renders all 11 stages |
| Whiteboard / auto-publish-check | `--help` smoke | Both parse and surface usage |
| `.mcp.json` validity | `json.load` | Valid (single Semrush HTTP MCP) |
| `content-pipeline/` scaffold | `ls` | All 9 numbered subdirs + `audit/`, `images/`, `optimization/`, `quality-checks/` present |
| SKILL.md frontmatter (34 skills) | YAML parse + `name` / `description` required | 1 issue: `capture-visuals` missing `name:` |
| Skill dir vs `name:` consistency | parse + compare | OK once capture-visuals is fixed |
| Python syntax across `.claude/skills/**/*.py` + `scripts/**/*.py` | `ast.parse` | 0 syntax errors |
| Cross-references in SKILL.md (paths to scripts / files) | regex + `Path.exists` | All script paths resolve once you account for them living under `.claude/skills/<skill>/scripts/` |

## Issues found

### Code (fixed in this commit)

1. **`.claude/skills/capture-visuals/SKILL.md` was missing `name:` in YAML frontmatter.** Every other skill declares `name:` explicitly; the harness fell back to the directory name so discovery still worked, but the inconsistency would silently break any tooling that keys off the YAML. Fixed.
2. **`.claude/skills/optimize-content/SKILL.md` description referenced `scripts/contentshake_optimize.py`** but the script lives at `.claude/skills/optimize-content/scripts/contentshake_optimize.py`. Cosmetic doc drift — the SKILL body itself uses the right path. Fixed in the description so the skill listing matches reality.

### Environment (not fixed — flagged for the operator)

3. **No API credentials in this environment.** All four providers `_smoke_integrations.py` checks (`OPENROUTER_API_KEY_BLOG_AGENT`, `REPLICATE_API_TOKEN`, `BROWSER_USE_API_KEY`, `GITHUB_TOKEN`) report no key in env. `SEMRUSH_API_KEY_BLOG_AGENT` and `STRAPI_API_TOKEN` are also unset. Doppler isn't installed. A real end-to-end `/blog-pipeline <keyword>` run would fail at stage 1 (`/research` calls Semrush MCP + OpenRouter).
4. **`requirements.txt` deps not installed.** `markdown`, `playwright`, `Pillow`, `matplotlib`, `replicate` are all declared but missing from the active Python env. `/preview` (markdown), `/optimize-content` (markdown), `/generate-visuals` (all of playwright/Pillow/matplotlib/replicate) would crash on a real run. Fix: `pip install -r requirements.txt && python -m playwright install chromium`.

### Confirmed false positives (no action needed)

- The 31 "missing path" hits from the cross-reference linter were almost entirely output directories that get created lazily on first run (`content-pipeline/0-context/`, `content-pipeline/0-keywords/cache/*`, `content-pipeline/updates/*/`) — not real broken refs. The linter would need to be aware that those are *destinations*, not *inputs*.

## What we did NOT smoke-test

A true end-to-end `/blog-pipeline <keyword>` run was not attempted because:
- No Semrush / OpenRouter credentials in env (would fail at stage 1).
- Visual deps (playwright, matplotlib, Pillow, replicate) not installed (would fail at stage 9).
- Real run costs ~30+ min and meaningful API spend; not appropriate for a scaffold-level smoke test in an unconfigured env.

When credentials and deps are loaded, the recommended next-pass smoke is `/blog-pipeline "test keyword" --context "smoke test, ok to skip publish"` and observe each stage's output file lands on disk.
