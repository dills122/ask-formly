# Independent promotion and publication review

Review instance: 1 of 3. Verdict: **Ready**.

Scope: working tree on `codex/material-input-textarea`, base/head `e5027e77c4807636db3ea943ff8edd561065d6cf`, and the explicit 60 paths in `test-output/public-files.json`. Unrelated untracked experiments and local settings are excluded. PRELIMINARY-REVIEW.md was written before AUTHOR.md was opened. The prior admission review was read as a closed candidate decision; this review independently checks promotion and installed delivery.

## Findings

No actionable blocking or non-blocking defect found in the reviewed promotion/publication scope.

The guarded replacement changes exactly the new authored document, installed DB, two knowledge manifests and source-preservation manifest. Existing runtime/model file maps are unchanged except for the DB hash. The helper rejects an already-promoted baseline by design. Recovery snapshots and the reused transaction provide rollback for ordinary exceptions and interruption; documentation correctly avoids claiming crash-atomic replacement across files.

All ten retained model-backed answers were checked against actual requests, generated question plans, returned facts and citation objects for seeds 1701 and 1702:

| Case | Independent answer assessment |
| --- | --- |
| Q02 | The delivered input-kind fact supports separate number/text branches. Answers reject a locale-independent parsing inference. The second planner question is hypothetical, not evidence that the branches are shared. |
| Q04 | Both input branches forward readonly; the answer does not infer disabled state or payload omission. |
| Q07 | Autosize, minimum and maximum row properties map to the three CDK bindings; no resizing-time or conflicting-bound guarantee is asserted. |
| Q10 | Textarea readonly forwarding is supported, with disabled/payload semantics explicitly left unsupported. |
| C04 | Both calls return unsupported_version for Formly 7 with no substituted v6 answer. |

Each supported answer cites a full fact actually delivered. The citation objects retain K47/K51 evidence identity, pinned release and implementation URL, exact authored-source quote offsets and matching source hash. Advisory status is available in all eight supported calls. These are bounded installed-mode smoke results, not a fresh broad planner or model-backed qualification.

## Plan Review

The implementation follows PLAN.md: data-only promotion, both manifests updated together, unchanged runtime/model implementations, exact canonical reproduction and baseline preservation, stable-launcher installed tests, current docs, and review before publication. Existing authored inputs, catalog, compiler and reference bytes remain protected. The source checklist retains exclusions. Numeric parsing, disabled/payload equivalence, CSS geometry, hidden-container measurement and hydration are not silently promoted into supported claims.

The documentation consistently reports 116 facts/25 documents, foundation13/discovery5, exact Formly 6.3.12 scope and the provisioned-checkout limitation. Candidate 15/15 versus baseline 9/15 is correctly described as repeated fixed scenarios, crediting recovered baseline input evidence rather than 90 independent generations. Existing clients must restart; fresh-process tests do not establish UI reload.

The explicit publication list contains 60 unique source/documentation/test/manifest paths and excludes DBs, models, environments, raw transport output, local configs/settings and sealed archives. Local Markdown link targets in those files resolve within the tracked tree or proposed public set. No credential-pattern matches were found in the proposed files. Public historical receipts contain hashes/path metadata, not the private artifacts themselves.

## Author-Claim Reconciliation

| Author claim | Evidence checked | Status |
| --- | --- | --- |
| Exact reviewed 116/25 DB installed | Installed/candidate SHA256, disposable canonical build, read-only SQL | Confirmed |
| Old knowledge and protected inputs preserved | Saved 111-fact snapshot, eight-table superset, 321 baseline pins | Confirmed: 317 identical, exactly four authorized existing changes |
| Both runtime/model pin maps retained | HEAD manifest comparison and every current file hash | Confirmed: 95 backed and 17 free pins match; only DB entry changed |
| Qualification/freeze/review evidence retained | 18 source-freeze, 197 final-freeze, 3 wiring entries, review pins and raw read_run audit | Confirmed |
| 15 installed free calls equal qualified candidate | Saved whole-result equality and independent fresh stable-launcher run | Confirmed |
| Ten bounded backed answers supported | Both raw five-call sets, plans, facts, citations and answer text | Confirmed with limits above |
| Four promotion, 18 admission tests and maintenance pass | Reviewer reruns | Confirmed |
| 60 public paths exclude private runtime artifacts | Exact path list, extension/path checks and local-link audit | Confirmed |

## Verification Performed

- `python3 tools/project.py check`: exit 0; source/provenance, compiler/package/regression checks and both doctors passed. No hosted inference or sealed evaluation was used by this command.
- Existing compiler environment, `python -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/promotion-v11 -p 'test_*.py'`: 4 tests passed.
- Same command targeting `material-input-textarea-v1`: 18 tests passed.
- Independent disposable canonical build from current authored inputs: SHA256 `417e30ce3465b6d97bd0f013ef06db2fc35963236d983b6a4c9b88858c97bb09`, exactly equal to installed and qualified candidate bytes. All eight knowledge tables equal, foreign keys clean, 116 facts/25 documents. Temporary DB removed afterward.
- Read-only saved baseline snapshot SHA256 `bb16595be949dc46e93f0918f270525ada825e3c70b8fabc9cd9b3a010c729f0`: every row in all eight tables remains in the installed DB.
- Independently checked 321 baseline paths, both current runtime manifests, source-preservation manifest, new authored/draft byte equality, source/final/wiring freezes and promotion review pins. No historical pin was rewritten.
- `read_run` and answer validation against all three repeats in each arm: exact repeated structured packets, 31 baseline calls and 15 candidate calls per repeat, 138 total; 9/15 baseline and 15/15 candidate completed judgments. The existing admission semantic review remains the closed candidate evidence.
- Fresh existing-MCP-environment command: `python -B poc/contextual-kb/knowledge-expansion/promotion-v11/installed_smoke.py --mode model-free --name reviewer-free-1`: exit 0, 15 successful calls and exact full-result equality. Evidence retained under `test-output/reviewer-free-1`.
- Reviewed the source of promote.py, test_promote.py, installed_smoke.py, the reused guarded transaction, results.read_run and current compiler interface. Graph lookup returned no new promotion symbols and coverage marked relied-on paths untracked; direct source reads, execution and hashes are the evidence, not graph absence.

## Open Questions And Residual Risks

No publication-blocking question remains. Model-backed evidence is the retained ten calls; this reviewer made no new hosted calls. Broad planner quality, whole-library compatibility and browser behavior remain unqualified. Sealed evaluation content was not opened. Historical maintenance helpers intentionally reject the newly promoted baseline; their refusal is not an installation regression. Multifile promotion is not crash-atomic, and running clients are not automatically restarted.

## Verdict

**Ready** for the authorized bounded 116-fact promotion and publication of the explicit reviewed source/documentation set. Runtime implementations and models remain unchanged. This verdict does not approve merging or expand compatibility claims.

## Recommended Next Actions

Return this report to the implementation task, record completion in the promotion results, and publish only the explicit reviewed paths under the existing authorization. Keep raw evidence/recovery snapshots private and preserve historical failures. No implementation changes, production writes, staging, commits, publication, sealed-archive access or additional agents occurred during this review.
