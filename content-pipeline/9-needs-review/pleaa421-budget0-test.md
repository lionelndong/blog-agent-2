# QUARANTINED: pleaa421-budget0-test

**Reason:** visuals-adversarial verdict FAIL with revision budget exhausted (0/0).
**Triggered by:** `python scripts/pipeline_gate.py visuals-adversarial pleaa421-budget0-test` exit 1 under `BLOG_AGENT_VISUALS_REVISION_BUDGET=0`.
**Adversarial verdict:** see `content-pipeline/quality-checks/pleaa421-budget0-test-visuals-adversarial.md`.
**Resolve by:** strip the decorative auto-capture + add the missing Reddit-thread visual, then re-run `/generate-visuals` and `/visuals-adversarial` manually.

This file was written as part of the PLEAA-421 acceptance-criterion-3 validation run.
