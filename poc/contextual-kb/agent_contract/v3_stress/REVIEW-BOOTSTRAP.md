# Fresh Review Bootstrap

Review instance: 1 of3. Independent semantic grading and engineering audit of frozen v3 repeated development testing.

## Review objective
Verify actual retained responses, correctness of scoring and experiment limits, and unchanged protected components. User asks v3 tested on fresh realistic requests in3–5 repeats per batch and independent review; evaluation sealed, both extractors/A/v2/data/DB unchanged.

## Repository and worktree
/Users/dsteele/repos/ask-formly, main, dirty pre-existing repository. No commits/staging. Review working-tree boundary only poc/contextual-kb/agent_contract/v3_stress. Frozen candidate lives in sibling refinement_v3; do not edit it. Read applicable root/POC instructions. Full root git status may contain unrelated work; exclude it.

## Canonical requirements and plan
Read PROTOCOL.md, data-review.md, task_plan.md, test_assess.py, assess.py, data/cases.json, data/rubric.json, frozen candidate CONTRACT.md/candidate.py. Generation used packets data/batch-1..3.json. Test-output input-freeze/raw-freeze identify inputs and raw responses. Do not read AUTHOR-EXPLANATION.md until preliminary independent concerns recorded.

## Exclusions
Never inspect sealed evaluation contents, DB data, trained weights, or other experiment cases. Read manifest maps and hash bytes only for preservation. No production accuracy, retrieval or latency qualification. No candidate fixes, no new workstreams/subagents or review instances. You may write only review reports and semantic grades in this new directory. Everything else read-only.

## Verification
From v3_stress: PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest -v test_assess
Read-only audit: python3 -B audit.py
Validate raw responses using frozen candidate; inspect every output against source request/rubric rather than mechanical token tests. Test-output/structure.json is author-generated, independently verify it. Record any failing cases and smallest concrete examples, not just counts.

## Semantic assessment format
Write test-output/semantic-review.json as an array of72 rows with id,run,semantic_pass:boolean,binding_pass:boolean,notes:string. Semantic pass requires justified and complete separately searchable aspects, standalone applicable conditions and polarity, exact identifiers/value pairings, scope and no application investigation/advice. Binding pass separately requires complete meaningful active-condition coverage, correct attachment, no retracted/local leakage. Natural equivalent question wording and grouping accepted per contract. Rubric is prior author testimony: flag ambiguity or rubric defects, don't mechanically penalize reasonable alternatives. No structural pass implies semantic pass. Keep semantic and binding findings distinct even if a response fails both.

Write test-output/stability-review.json with24 rows {id,equivalent_across_runs:boolean,notes:string}: assess equality of meaning/coverage and conditions across3, allowing wording changes. Identical recurring errors may be semantically stable but unusable; explain that distinction.

## Author explanation
AUTHOR-EXPLANATION.md, to read only after preliminary pass. Reconcile material author claims against evidence. Verdict covers bounded test evidence and separate candidate gate. 'Not ready' candidate is not reason to reject honest evidence. Report residual validity limits including generated cases/native agent delivery and no deployed pinned model.

Use $independent-review in reviewer mode. Review instance1of3. Start here, record preliminary concerns before explanation, verify code, plan, every raw response and aggregate results. Return evidence-backed verdict; no fixes or recursive review.
