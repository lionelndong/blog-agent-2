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

### Code (also fixed — second pass)

5. **`render_preview.py` and `generate_visuals.py` treated `--help` as a slug** because they read `sys.argv[1]` directly. Replaced with `argparse` so `--help` works while keeping the same positional-argument call shape — no behavioral regression for the existing callers (verified: no-arg invocation still exits 2 with usage, just like before).

### Environment (partially fixed — rest needs operator input)

6. **`requirements.txt` deps now installed.** Ran `pip install -r requirements.txt` — `markdown`, `playwright`, `Pillow`, `matplotlib`, `replicate` all import cleanly. `/preview`, `/optimize-content`, `/generate-visuals` will no longer crash on import. ✅
7. **Playwright Chromium browser NOT installed.** `python -m playwright install chromium` fails with a network 403 in this sandbox — Chrome for Testing CDN is not reachable. `/generate-visuals` will work for matplotlib charts and Replicate images but Playwright-based screenshots will fail until the browser binary is installed in an env with outbound HTTPS. **Needs operator action** in the deploy env.
8. **Doppler CLI NOT installed.** `cli.doppler.com` and `api.github.com` both return 403 from this sandbox. **Needs operator action** in the deploy env (`brew install dopplerhq/cli/doppler` on Mac, or apt repo on Linux).
9. **No API credentials** — unchanged. `OPENROUTER_API_KEY_BLOG_AGENT`, `REPLICATE_API_TOKEN`, `BROWSER_USE_API_KEY`, `GITHUB_TOKEN`, `SEMRUSH_API_KEY_BLOG_AGENT`, `STRAPI_API_TOKEN` all unset. **Needs operator action** — set up Doppler with these secrets, then run `doppler run -- claude` to launch sessions with creds loaded.

### Confirmed false positives (no action needed)

- The 31 "missing path" hits from the cross-reference linter were almost entirely output directories that get created lazily on first run (`content-pipeline/0-context/`, `content-pipeline/0-keywords/cache/*`, `content-pipeline/updates/*/`) — not real broken refs. The linter would need to be aware that those are *destinations*, not *inputs*.

## What we did NOT smoke-test

A true end-to-end `/blog-pipeline <keyword>` run was not attempted because:
- No Semrush / OpenRouter credentials in env (would fail at stage 1).
- Playwright Chromium not downloadable in this sandbox (would partially fail at stage 9).
- Real run costs ~30+ min and meaningful API spend; not appropriate for a scaffold-level smoke test in an unconfigured env.

When credentials and the Chromium browser are loaded, the recommended next-pass smoke is `doppler run -- claude` then `/blog-pipeline "test keyword" --context "smoke test, ok to skip publish"`, observing each stage's output file lands on disk.

## Verification of fixes (re-run after each change)

| Fix | Verification command | Result |
|---|---|---|
| capture-visuals `name:` | `python -c "import yaml,re; t=open('.claude/skills/capture-visuals/SKILL.md').read(); m=re.match(r'^---\n(.*?)\n---', t, re.DOTALL); print(yaml.safe_load(m.group(1))['name'])"` | `capture-visuals` |
| optimize-content description path | YAML re-parse | references `.claude/skills/optimize-content/scripts/contentshake_optimize.py` |
| Frontmatter sweep across all 34 skills | YAML parse + `name`/`description` required | 0 issues |
| Python deps importable | `python -c "import markdown, playwright, PIL, matplotlib, replicate"` | All OK |
| `--help` on render_preview / generate_visuals | run with `--help` | argparse usage prints, exit 0 |
| No-arg regression on render_preview / generate_visuals | run with no args | exit 2 with usage (unchanged) |
| Python syntax across skills + scripts | `ast.parse` all `.py` | 0 errors |
