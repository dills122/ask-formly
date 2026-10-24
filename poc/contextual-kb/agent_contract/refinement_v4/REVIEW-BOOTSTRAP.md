# Fresh Review Bootstrap
Review instance1of3.

## Objective and boundary
Independently review new v4 candidate, plan and actual generation evidence. Root /Users/dsteele/repos/ask-formly, dirty main working tree; no staging/commits. In scope only poc/contextual-kb/agent_contract/refinement_v4. Prior v3 and v3_stress are frozen dependencies/evidence, not edits. Other dirty repository work is unrelated. User authorized ledger clarification/missing-exclusion fix, testing and independent review; both extractors,A,v2,v3,data/DB and sealed evaluation unchanged.

## Ground truth before author rationale
Read applicable root/POC instructions, PROTOCOL.md, LEDGER-RULES.md, test_candidate.py, candidate.py, CONTRACT.md and data/rubrics. Record preliminary concerns before AUTHOR-EXPLANATION.md. Verify candidate differs only by ledger instructions and new prompt selector; v3 transport reused within POC. No claimed mechanical semantic-completeness detector.

## Verification
From candidate directory: PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest -v test_candidate
python3 -B preserve.py
Verify input/raw freeze and reconstruct records from six raw batches. Validate all48 responses and optional-hint projection. Inspect every question and binding against original request and frozen rubric. Fixed policy requires scenario transitions AND controlling dependencies; no posthoc ambiguity on those categories now. Bare operation/target alone not extra constraint. Exclusions must have meaningful source excerpt binding in every applicable question. Quoted/retracted/background instructions are not active restrictions. Preserve local attachment and correction precedence.

## Review artifacts
Only write own artifacts in refinement_v4: REVIEW-1-preliminary.md, REVIEW-1.md and test-output/semantic-review.json containing48 rows {id,run,semantic_pass:boolean,binding_pass:boolean,notes:string}. Write stability-review.json containing16 rows {id,equivalent_across_runs:boolean,notes:string}. Semantic text usefulness separate from ledger compliance. Do not generate alternate responses, edit candidate/data/output or spawn subagents/review instances. No reading sealed case contents or loading weights/DB; preservation byte hashing only.

## Report
Grade every response, identify concrete failures and reasonable rubric ambiguities; never infer correctness from declared binding validation. Verdict for evidence/implementation and separate full candidate gate. No answer/retrieval/latency/production qualification. Test author and native generation independence is context separation, not vendor independence. Maximum3 review instances only for material fixes, not to overturn negative evidence. No review recursion.

Author explanation is AUTHOR-EXPLANATION.md. Use independent-review skill in reviewer mode, inspect first and reconcile author claims afterward. Relevant code-review-and-quality skill also applies. Return evidence-backed verdict and exact artifacts.
