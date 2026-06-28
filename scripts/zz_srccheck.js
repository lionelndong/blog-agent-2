const { Client } = (function(){ const fs=require("fs"),path=require("path"); try{return require("pg");}catch{} const base="/app/node_modules/.pnpm"; const dir=fs.readdirSync(base).find(d=>/^pg@\d/.test(d)); return require(path.join(base,dir,"node_modules","pg")); })();
const CO="d11fb003-42e2-4b84-8d88-e1242ad09a70";
(async()=>{
  const c=new Client({host:"localhost",port:54329,user:"paperclip",database:"paperclip"});
  await c.connect();
  const dist=await c.query("SELECT source_type, count(*)::int n FROM company_skills WHERE company_id=$1 GROUP BY source_type ORDER BY n DESC",[CO]);
  console.log("=== source_type distribution (this company) ===");
  for(const r of dist.rows) console.log(`  ${r.source_type}: ${r.n}`);
  console.log("\n=== sample rows: blog skill vs paperclip-native vs other imports ===");
  const samp=await c.query("SELECT slug, source_type, source_locator, metadata->>'sourceKind' AS kind FROM company_skills WHERE company_id=$1 AND slug IN ('blog-pipeline','brand-reference','diagnose-why-work-stopped','paperclip-dev','paperclip-create-plugin','firecrawl','hormozi-pricing','querying-posthog-data') ORDER BY slug",[CO]);
  for(const r of samp.rows) console.log(`  ${(r.slug||'').padEnd(26)} type=${(r.source_type||'').padEnd(12)} kind=${(r.kind||'-').padEnd(10)} locator=${(r.source_locator||'').slice(0,60)}`);
  console.log("\n=== columns on company_skills ===");
  const cols=await c.query("SELECT column_name, data_type FROM information_schema.columns WHERE table_name='company_skills' ORDER BY ordinal_position");
  console.log("  "+cols.rows.map(r=>r.column_name).join(", "));
  await c.end();
})().catch(e=>{console.error("ERR",e.message);process.exit(1);});
