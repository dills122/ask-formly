# Independent preliminary review

Review instance: 3 of 3. Saved before reading AUTHOR-EXPLANATION.md. Fresh context included neutral bootstrap and prior preflight findings, not author rationale or prior semantic grades.

Scope: qualification_v2 on dirty main HEAD c3091328f49d53de6b41a49c4fe5aa8f1c45e516. Unrelated changes excluded. Direct reads used for graph-not-tracked POC. Reviewed requirements, policy, candidate contract, code/tests, preflight reviews, all 53 source/rubric records, all 159 outputs and all 53 triplets in bounded batches.

P1 qualification blocker: N21 runs 1/2 omit `without polling` from question index 1 and bind it only to index 0. Source `the observer` means the requested non-polling observer, explicitly confirmed by frozen rubric/case-review. Each question must stand alone. This changes the method scope of the information need and is a text/semantic/binding/material-intent failure, not merely a missing ledger. Run 3 preserves both. N21 is meaning/ledger unstable. No other substantive failures under frozen POLICY.

Fresh structure 144/144; text/semantic/binding/joint 142/144; all-three joint 47/48; groups 24,24,22,24,24,24; meaning/ledger stability 47/48. Diagnostic joint 15/15 and stability 5/5. Two observed material intent errors violate zero-error gate. Strict perfect fails. Exact-object equality fresh 2/48, diagnostic 0/5.

Independent AST parsing and standard JSON encoding match all 21 raw outputs byte-for-byte. All attempts have first-save/completion/stdout/stderr/output; load_attempt reconstructs records exactly. Exactly 21 literal files and attempt directories, no retry directories. Candidate/input/three-round/raw freezes match (17/37/42/42/42/126 entries); 41 inherited manifests and 38,869 overlapping entries preserved using hash-only sealed checks. Contract is qualification1 plus addition exactly. Optional/malformed hints leave current 159 core plans unchanged.

Tests: qualification_v2 20 pass; qualification_v1 8 pass; scorer 8 pass. Evidence: test-output/reviewer-*; semantic-review.json has 159 rows and stability-review.json 53 rows. No production attempt rerun, output repair, criterion changes or protected mutations.

Preliminary verdict: Not ready for experimental foundation eligibility: zero-observed-material-intent-errors gate fails. No production, library-answer correctness, retrieval or causal-improvement claim.
