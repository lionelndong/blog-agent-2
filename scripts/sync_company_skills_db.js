#!/usr/bin/env node
/**
 * sync_company_skills_db.js — make the Paperclip company-skill library mirror this
 * repo's .claude/skills exactly (for the lionelndong/blog-agent-2 content skills).
 *
 * WHY: Paperclip stores a snapshot of each skill in the `company_skills` DB table
 * (slug, name, DESCRIPTION, markdown, source_ref, file_inventory, trust_level). The
 * UI catalog and the agent's skill-trigger text read the `description` column. When a
 * skill is edited in this repo, that column does NOT auto-refresh (the skills.sh
 * install-update path 404s for this private repo), so the catalog drifts and can end
 * up advertising tools that no longer exist. This script re-derives every column from
 * the repo SKILL.md at the current HEAD and upserts it, then clears the materialized
 * runtime dirs so the next agent wake re-pulls the corrected content.
 *
 * It runs INSIDE the Paperclip container (embedded Postgres on localhost:54329) and
 * reads THIS repo working copy — no network/auth needed (the working copy is already
 * the latest; the agent commits here before pushing).
 *
 * Idempotent. Does NOT touch agent desiredSkills (that's deliberate config). Does NOT
 * delete DB rows that lack a repo dir (warns instead). Generic dev skills (check-pr,
 * greploop) are intentionally excluded from the content library.
 *
 * Run:  node scripts/sync_company_skills_db.js
 * Cron: weekly via host docker exec (see /docker/paperclip-whwi/patches/).
 */
const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");

// pg ships with the Paperclip server; resolve it from the pnpm store.
function loadPg() {
  try { return require("pg"); } catch {}
  const base = "/app/node_modules/.pnpm";
  const dir = fs.readdirSync(base).find((d) => /^pg@\d/.test(d));
  return require(path.join(base, dir, "node_modules", "pg"));
}
const { Client } = loadPg();

const CO = "d11fb003-42e2-4b84-8d88-e1242ad09a70";
const OWNER = "lionelndong", REPO = "blog-agent-2";
const REPO_ROOT = path.resolve(__dirname, "..");
const SKILLS_DIR = path.join(REPO_ROOT, ".claude", "skills");
const RUNTIME = `/paperclip/instances/default/skills/${CO}/__runtime__`;
const EXCLUDE = new Set(["check-pr", "greploop"]); // generic dev skills, not content

function frontmatter(md) {
  const out = {};
  const m = md.replace(/\r\n/g, "\n").match(/^---\n([\s\S]*?)\n---/);
  if (m) for (const line of m[1].split("\n")) {
    const mm = line.match(/^(name|description):\s*(.*)$/);
    if (mm) out[mm[1]] = mm[2].trim();
  }
  return out;
}
function walk(dir, base = "") {
  const out = [];
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.name === "__pycache__" || e.name.endsWith(".pyc")) continue;
    const rel = base ? `${base}/${e.name}` : e.name;
    if (e.isDirectory()) out.push(...walk(path.join(dir, e.name), rel));
    else out.push(rel);
  }
  return out;
}
const classify = (p) => (p === "SKILL.md" ? "skill" : p.startsWith("scripts/") ? "script" : "reference");

(async () => {
  const ref = execSync("git rev-parse HEAD", { cwd: REPO_ROOT }).toString().trim();
  const c = new Client({ host: "localhost", port: 54329, user: "paperclip", database: "paperclip" });
  await c.connect();

  const repoSlugs = fs.readdirSync(SKILLS_DIR, { withFileTypes: true })
    .filter((e) => e.isDirectory() && !EXCLUDE.has(e.name) && fs.existsSync(path.join(SKILLS_DIR, e.name, "SKILL.md")))
    .map((e) => e.name);

  let inserted = 0, updated = 0, unchanged = 0;
  for (const slug of repoSlugs) {
    const dir = path.join(SKILLS_DIR, slug);
    const md = fs.readFileSync(path.join(dir, "SKILL.md"), "utf8").replace(/\r\n/g, "\n");
    const fm = frontmatter(md);
    const inv = walk(dir).sort().map((p) => ({ kind: classify(p), path: p }));
    const trust = inv.some((f) => f.kind === "script") ? "scripts_executables" : "markdown_only";
    const key = `${OWNER}/${REPO}/${slug}`;
    // Paperclip-NATIVE registration: resolve the skill from its local path in this repo
    // (source_type local_path/catalog are the only kinds Paperclip resolves to a local
    // source — see server/src/services/company-skills.ts). No external skills.sh/GitHub fetch.
    const localLocator = path.join(SKILLS_DIR, slug);
    const meta = { ref, repo: REPO, owner: OWNER, skillKey: key, sourceKind: "local_path", trackingRef: "main", repoSkillDir: `.claude/skills/${slug}` };

    const ex = await c.query("SELECT id, description, markdown FROM company_skills WHERE company_id=$1 AND key=$2", [CO, key]);
    if (!ex.rowCount) {
      await c.query(
        `INSERT INTO company_skills (id, company_id, key, slug, name, description, markdown, source_type, source_locator, source_ref, trust_level, compatibility, file_inventory, metadata, created_at, updated_at)
         VALUES (gen_random_uuid(), $1,$2,$3,$4,$5,$6,'local_path',$7,$8,$9,'compatible',$10::jsonb,$11::jsonb, now(), now())`,
        [CO, key, slug, fm.name || slug, fm.description || "", md, localLocator, ref, trust, JSON.stringify(inv), JSON.stringify(meta)]
      );
      inserted++; console.log("INSERT", slug);
    } else {
      const r = ex.rows[0];
      const changed = (r.description || "") !== (fm.description || "") || (r.markdown || "") !== md;
      await c.query(
        `UPDATE company_skills SET name=$1, description=$2, markdown=$3, source_ref=$4, trust_level=$5, file_inventory=$6::jsonb, metadata=$7::jsonb, source_type='local_path', source_locator=$8, updated_at=now() WHERE id=$9`,
        [fm.name || slug, fm.description || "", md, ref, trust, JSON.stringify(inv), JSON.stringify(meta), localLocator, r.id]
      );
      if (changed) { updated++; console.log("UPDATE", slug); } else unchanged++;
    }
    // clear materialized runtime so the next wake re-pulls
    try { for (const d of fs.readdirSync(RUNTIME)) if (d === slug || d.startsWith(slug + "--")) fs.rmSync(path.join(RUNTIME, d), { recursive: true, force: true }); } catch {}
  }

  // warn on DB rows with no repo dir (orphans) — never auto-delete
  const dbRows = await c.query("SELECT slug FROM company_skills WHERE company_id=$1 AND source_locator ILIKE '%blog-agent-2%'", [CO]);
  const orphans = dbRows.rows.map((r) => r.slug).filter((s) => !repoSlugs.includes(s) && !EXCLUDE.has(s));
  if (orphans.length) console.log("WARN orphan DB skills (in library, no repo dir):", orphans.join(", "));

  console.log(`sync @ ${ref.slice(0, 8)}: ${inserted} inserted, ${updated} updated, ${unchanged} unchanged, ${repoSlugs.length} content skills mirrored`);
  await c.end();
})().catch((e) => { console.error("ERR", e.message); process.exit(1); });
