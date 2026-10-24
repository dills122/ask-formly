# Independent review
Review instance: 1 of 3. Verdict: **Ready** for the bounded local POC integration.

## Findings

No actionable blocking or non-blocking code defect established. This is a bounded readiness verdict, not production hosting or broad Formly-answer accuracy approval.

The preliminary review was recorded before reading AUTHOR-EXPLANATION.md and author grading. This reviewer had a fresh task context containing the review bootstrap and scope, not implementation conversation. Scope is new mcp_v1 on dirty main c3091328f49d53de6b41a49c4fe5aa8f1c45e516; unrelated repository changes were excluded. The October 16 graph has no tracked coverage for reviewed POC code; all material structural conclusions use direct source inspection.

## Plan Review

The implementation satisfies the bounded plan: one raw-request MCP tool, unchanged foundation contract and structural validation, advisory extraction using retained adapters, unchanged full-question retrieval, complete original candidate facts, separately attached stored citations, and calling-agent answer assessment. Persistent index/worker ownership is confined to a serialized executor. Known integrity failures propagate and latch; ordinary optional-extractor unavailability remains explicit. Invalid input/plan is rejected before backend loading. The stdout capture order is exercised by the real SDK transport regression.

The server imports runtime code only from this POC and third-party libraries. The locked DB is opened read-only; no corpus/index migration or checkpoint training occurs. The new environment is separate. README supplies setup, client configuration, timeouts, model/provider prerequisites, logging disclosure, knowledge limits and the distinction between candidate evidence and a verified answer. No global registration or deployment is claimed.

The fixed 10-case panel was repeated three times with adapters 1701/1702/1701, preserving failures and excluding tuning. It supports integration readiness and safe handling of gaps. It cannot establish general accuracy, sub-percentage tolerance, or an adapter quality ranking. The task checklist may be closed by the author after recording this review; no extra review instance or architecture pivot is needed.

## Author-Claim Reconciliation

| Author claim | Evidence inspected | Status / consequence |
| --- | --- | --- |
| Raw request preserved; frozen planner configuration | planner.py, service.py, frozen schema/contract, all 30 planner request/event/receipt chains | Confirmed; no completed planner tool calls found. |
| Genuine MCP delivery | server.py, SDK smoke, all three caller JSONL streams and server audit records | Confirmed: 30 exact client/server structured-packet matches, ten calls and answers each round. |
| Original full queries and whole facts preserved | backend.py, frozen AdvisoryLookup/bridge/PilotIndex, audit_results.py and all replay rows | Confirmed by original-environment replay for 30/30 plans. Reviewer inspected replay implementation/results without rerunning models. |
| Both retained native adapters unchanged | per-packet runtime receipts and preservation chains | Confirmed: expected seed each round, 30 parameter-check receipts true; DB checks true. |
| Citations are stored provenance | citations_for and independent read-only SQL comparison | Confirmed for 216 returned mappings, including complete evidence JSON; no external-source freshness claim. |
| 10/10 usable per round | cases/PROTOCOL before results; all 30 plans, answers, attached records/quotes; semantic-grades and stability | Confirmed under the frozen safe-gap rubric, with the support breakdown below. |
| Foundation/data/prior evidence unchanged | preserve.snapshot compared to protected-before; qualification freeze hashes | Confirmed: 50 protected entries and 17 frozen files unchanged. Sealed evaluation handled by hash only. |

## Semantic Review

Every case was reviewed across all three repetitions. Wording and decomposition vary; only the out-of-scope plan is byte-identical across all three, while requested meaning and support status remain stable.

| Cases | Independent assessment across all three rounds |
| --- | --- |
| M01 | Custom name tax-id and registration/use retained. Illustrative component/model-key names do not claim application facts; no invented SSN validation. Supported registration/use answer. |
| M02 | Existing-field and Material context bound to relevant questions. Decoration/insertion/Material shell advice supported; absent wrapper-selection recipe explicitly disclosed. Partial. |
| M03 | Both required-property dependency and evaluation-context needs retained with shared no-subscription restriction. Returned packet lacks the requested recipe/context; limited expression-check timing statement and disclosed gap are warranted. Partial. |
| M04 | Both API names, version and no-substitution restriction retained. Callback distinction and model scope supported. Round 2 string-expression bindings are explicitly present in the returned authored-source table. Supported. |
| M05–M06 | Sync configuration/message and async/comparison needs preserved. Unrelated retrieved matches are not promoted into validator advice. Not supported. |
| M07 | Separate model and control outcomes retain hidden/resetOnHide:false context. Answer preserves control-unregistration qualifications and does not equate retained model value with active control retention. Supported. |
| M08 | Both exact APIs and post-edit/version context retained. Baseline capture versus restoration correctly distinguished. Supported. |
| M09 | Formly 7 guarantee remains a question, not an accepted premise. Caller explicitly declines extrapolation from 6.3.12. Not supported. |
| M10 | Empty questions/bindings/facts and explicit application-scope refusal. No application investigation. Out of scope. |

Per round: **4 supported, 2 partial, 3 not supported, 1 out of scope**. All ten satisfy the predeclared usability rubric because honest partial/gap responses count. Total: **12 supported, 6 partial, 9 not supported, 3 out of scope**. No material intent error observed. This is not 30 complete answers or 100% general answer accuracy.

## Verification Performed

Executed without native model/provider reruns:

- `poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/mcp_v1 -p 'test_*.py'`: 11 passed. Citation test emits an unclosed in-memory SQLite ResourceWarning; this does not indicate a production connection leak.
- `poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/agent_contract/advisory_lookup_v1 -p 'test_*.py'`: 35 passed.
- Independent raw-event/audit/answer/row reconciliation and read-only SQL provenance comparison: all 30 calls and 216 citation mappings pass.
- Initial and final protection/freeze checks pass. The completed results freeze also matches all 175 entries; RESULTS.md accurately states the supported/partial/gap distinction. Results retained in test-output/review-preservation.json and test-output/review-evidence.json.

The original-environment 30-plan retrieval replay was executed by the author; reviewer inspected its source and retained results, not a redundant embedding/model execution. Semantic review is separate from parity checks.

## Open Questions And Residual Risks

The planner alias is not an immutable model revision; provider availability, latency and usage remain operational dependencies. The sample is small, synthetic and development-only. Five of the nine library cases lack full support, reflecting the deliberately bounded corpus/retrieval. Candidates still require a careful caller. Stored provenance is not a fresh independent source audit. Serial local stdio serving does not demonstrate remote security, concurrency scale or production reliability.

Planner timeout cleanup is implemented, but a timeout skips planner receipt.json creation; event/stderr artifacts and the server error/timing audit remain. This is a diagnostic limitation rather than a demonstrated acceptance failure. Direct new Backend failure-path coverage is narrower than its native success coverage; inherited integrity/availability tests plus the service latch tests reduce but do not eliminate that residual uncertainty.

## Verdict

**Ready** for the authorized bounded local MCP POC. All hard integration gates have supporting evidence and the frozen usability target is met in each round. No heavy pivot, new workstream, code fix, or additional review instance is required by this review.

## Recommended Next Actions

Author should close the task checklist, retain this report and all frozen/raw artifacts, and report both usability and full-support counts to the user. Keep the foundation/data/model boundary unchanged. Any later serving changes need their own relevant qualification rather than relabeling these runs.
