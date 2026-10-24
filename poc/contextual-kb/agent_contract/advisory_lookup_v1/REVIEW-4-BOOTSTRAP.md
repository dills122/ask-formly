# Fresh review bootstrap

Review instance: 4 of 4. The user explicitly authorized this additional independent review of the final reuse-state fix and closing out the integration if it passes. Earlier three-review limits are historical; no fifth review is authorized.

## Objective and scope
Repository: /Users/dsteele/repos/ask-formly. Working-tree boundary: poc/contextual-kb/agent_contract/advisory_lookup_v1 only; dirty main at c3091328f49d53de6b41a49c4fe5aa8f1c45e516. Verify Git state. Review the final reuse-state fix in lookup.py and transport.py against test-output/pre-reuse-fix-source, tests in test_integrity_reuse.py, and surrounding integrity versus availability handling. Read repository guidance, CONTRACT.md, tests, current source and REVIEW-3.md finding first. Save preliminary findings before reading FINAL-STATUS.md or author rationale. Assess the functional local POC, not production or answer accuracy.

## Requirements and plan
Foundation plans retain full-question retrieval; GLiNER annotations are advisory. Ordinary unavailable extraction may degrade with diagnostics; known integrity mismatch must fail and remain failed across reuse. Cleanup must remain correct. Models, DB, previous candidates and evaluation are unchanged. Evaluation remains sealed: never read sealed content; hashing only. Review task_plan.md after preliminary findings, reconciling its historical open signoff with this newly authorized review.

## Frozen target and evidence
Current implementation: test-output/implementation-final-freeze.json. Prior-turn complete snapshot: test-output/final-freeze.json. Do not modify any frozen artifact. Latest actual native CLI: test-output/cli-complete-native.json. Successful native panel: test-output/live-native (48 requests, 70 questions per model). Original test-output/live failed due missing torch and remains failure evidence. Do not rerun native inference or retrieval. Run python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/advisory_lookup_v1 -p 'test_*.py'. Independently verify preserved manifests and the 48 chains using preserve.snapshot compared with test-output/protected-before.json. Use qualified import from agent_contract.advisory_lookup_v1.preserve to avoid module-name collisions.

Historical manifests may bind source archives: failed-environment-source, pre-review-fix-source, pre-integrity-fix-source, pre-reuse-fix-source. Resolve expected hashes against archives explicitly; do not mistake old manifests for current code hashes. Current final-freeze must match all original files directly.

## Reviewer ownership
Write only REVIEW-4-PRELIMINARY.md, REVIEW-4.md, REVIEW-4-DECISION.json and test-output/review4-* within this directory. Do not fix code, alter frozen evidence, create agents, or expand scope. Graph coverage for this POC was not tracked; follow required coverage checks and exact source fallback for relied-on source. Author explanation after preliminary: FINAL-STATUS.md, AUTHOR-EXPLANATION.md, INTEGRITY-FIX.md, RESULTS.md and progress.md.

Use independent-review in reviewer mode and code-review-and-quality. Return an evidence-backed Ready / Ready with non-blocking follow-ups / Not ready / Unable to verify verdict. No further independent pass is authorized.
