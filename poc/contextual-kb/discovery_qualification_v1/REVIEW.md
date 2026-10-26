# Independent review

Review instance: 3 of 3. Verdict: **Ready** for this bounded qualification record; no installed promotion or broad parity certification.

## Findings

No actionable implementation defect or unsupported final-answer claim was found in the reviewed scope. All 30 covered answers are supported and all six controls are safe. These are semantic judgments over claims, conditions and delivered citations, not fact-ID matching scores. The third pass was independently generated but self-graded by this reviewer; only the first 20 covered answers received a separate caller/reviewer assessment.

The fresh runtime pass was completed before reading r1/r2 answers or old-reference results. The reviewer derived its own plans, selected discovery only for evidence gaps, fetched selected records, and froze `test-output/r3-answers.json` before comparison. `r3-preliminary-review.md` records concerns before reading author `RESULTS.md`.

## Scope and ground truth

Repository `/Users/dsteele/repos/ask-formly`, branch `codex/versioned-knowledge`, HEAD `8e8d02e82c01e3f0e6e0b74a31b8c7346ca22830`. The working-tree review boundary is the untracked `discovery_qualification_v1` helper/tests/plans/cases/results plus the additive project MCP configuration; existing discovery/model-free/foundation implementations are frozen dependencies. No tracked diff was present. Other untracked JSON-schema, model-free, native-chat and parity directories existed and are not attributed to this qualification change.

Reviewed `transport.py`, `metrics.py`, their six tests, caller instructions and server schemas, frozen discovery paging/guard implementation, fixed requests and every final answer, submitted tool inputs and raw responses. The knowledge graph returned no helper symbols and marked all nine inspected code paths untracked; direct source reads supplied the evidence. No absence/completeness conclusion depends on graph coverage.

## Plan review

The observable target was at least 9/10 supported covered answers in every pass, safe controls, preserved conditions/scope, bounded lookup/discovery/fetch calls, unchanged runtime/knowledge, and a reference sufficiency comparison after freezing new answers. Those criteria were met.

Execution differs from the initial plan in disclosed ways: pass2 keeps each complete request as one combined question; pass3 has focused questions with the entire attributed request repeated on each, preserving text but overbinding independent/local context and reducing selectivity. This does not prove consistently precise decomposition. Runtime calls were submitted in larger arrays rather than the proposed groups of four. Pass3 used fresh reviewer context rather than a third root-context repeat, improving independence of generation. `RESULTS.md` explains the substantive variant and does not claim independent random repetitions or deterministic planning.

The helpers are small and keep decisions outside the server: transport forwards explicit arguments via MCP SDK and records results; metrics counts calls, errors, bytes and fact delivery without pretending to grade semantics. Existing MCP dependencies and standard-library utilities suffice. No new application behavior, learned retrieval or generalized orchestration was introduced. Tests cover tool/argument shape and key accounting distinctions, while the real 64-call run supplies protocol evidence. Startup/initialization failures, crash recovery and arbitrary transport reuse are not comprehensively unit-tested; all observed sessions completed with receipts. This limitation does not undermine this completed local checkpoint.

## Semantic results

| Case | Each new pass | Material aspects checked | Old reference |
|---|---|---|---|
| D01 | Supported | Material input integration; named registration/use; separate Angular setup; no validation recipe | Sufficient |
| D02 | Supported | False retention through hide branch versus active control; visible shared key exception | Sufficient |
| D03 | Supported | Function field argument versus string bindings; keyed nested scope, no root assumption | Sufficient |
| D04 | Supported | Named boolean versus typed error-map/null; runtime tolerance does not change types | Sufficient |
| D05 | Supported | Zero defined; eligible undefined default; cloned snapshot then reset/rebuild; raw reset distinction | Sufficient |
| D06 | Supported | Falsy insertion versus final build value; model/rebuild/event sequence; omitted versus empty options; no pristine guarantee | Sufficient |
| D07 | Supported | caption/ref mapping versus object identity; no invented application identity key | Sufficient |
| D08 | Supported | Observable/template async versus helper; exact-field event and property-prefix gates; array/helper guard; ownership | Sufficient |
| D09 | Supported | Matching preset prePopulate timing; wrapper insertion; neither mechanism is itself a missing-control/accessor implementation | Sufficient |
| D10 | Supported | Both enabling props; field/event callback; programmatic caveat; nonempty length is not membership | Sufficient |
| D11 | Safe control | Exact 6.4.0 rejected without substitution or follow-up scope downgrade | Unsupported version retained |
| D12 | Safe control | Unrelated candidates rejected; evidence gap not nonexistence | Unrelated evidence, no verified API |

Old reference D03 does not need the dedicated leaf fact to establish that keyed-group children have nested scope. D09's delivered wrapper-insertion citation explicitly includes the authored quotation that wrappers do not substitute for a missing control/value accessor, despite omission of the dedicated limit fact. Counting either as failure solely for a missing designated ID would be incorrect. All ten old covered packets are sufficient; this says nothing about an unobserved old final answering agent.

`test-output/r3-semantic-review.json` retains the case-by-case ledger. No critical invented APIs, wrong-release claims, lost negations or material condition omissions were found in the final answers. The preset/control explanation is an interpretation of configuration reuse and explicit wrapper limits, not a universal claim that a preset cannot contain a correctly configured rendering type.

## Author-claim reconciliation

| Author claim | Evidence inspected | Status / consequence |
|---|---|---|
| 10/10 supported per pass, 2/2 safe controls | All three answer files and corresponding full facts/conditions/citations | Confirmed within this panel |
| 64 calls, no errors/repairs/budget exhaustion | Raw result rows, receipts, input scopes and request/plan identity | Confirmed: 19/23/22 calls |
| Discovery summaries not used alone as citations | Every selected ID checked against same-pass full facts and citation map | Confirmed; zero missing full records/provenance |
| Reference evidence 10/10 sufficient | All 12 reference packets, including citation quotations | Confirmed; no old final-answer score inferred |
| Frozen runtime/knowledge preserved | Rehashed all 813 entries in freeze.json | Confirmed; zero mismatches |
| Six helper tests pass | Independent unittest invocation | Confirmed |
| Maintenance passes | Independent `python3 tools/project.py check` | Confirmed, exit 0 |
| New server runs without models | SDK launcher path, offline guard source and completed runtime | Confirmed for observed guarded sessions; not a general security certification |
| Desktop/native connection not yet qualified | SDK path used; new tool absent from caller catalog | Confirmed limitation, not a completed connection claim |
| Tool times/bytes exclude reasoning/startup | Recomputed result serialization and elapsed-call totals; transport source | Confirmed; cannot establish end-to-end speedup |

## Verification performed

- Fresh caller MCP execution: 12 lookups, five discovery pages, five fetches. No repairs/errors. Full inputs/outputs and receipts retained under r3 names.
- Independent protocol audit: original requests unchanged; discovery plan identical to its lookup; exact scope repeated; all discovery limits at most32 and fetches at most16 IDs; every cited fact and citation delivered. All per-case budgets met.
- Recomputed rounds: 19/23/22 calls, 839010/776658/961330 serialized result bytes, 0.235763/0.280673/0.263855 summed tool seconds. Reference: 12 calls, zero errors, 1094850 bytes, 321.368936 tool seconds. These exclude caller work and startup.
- `poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/discovery_qualification_v1 -p 'test_*.py'`: six passed.
- `python3 tools/project.py check`: passed; detailed output in `test-output/r3-maintenance.txt`. No hosted inference or sealed evaluation used by this command.
- SHA-256 verification of all813 frozen paths: unchanged. No implementation edits, staging, commits, model/DB changes or sealed-question inspection by this reviewer.

## Open questions and residual risks

This is a small familiar 93-fact corpus and one fresh-context caller, with two root-context repetitions and only one reference sample. It does not establish broad parity, unseen accuracy, production readiness, precise error margins, or superiority. No no-discovery ablation separates discovery's marginal contribution. Native app registration still needs an actual catalog-visible lookup/discovery/fetch run. Existing browser B06/B13 historical failures are not requalified. Raw outputs and startup logs are local evidence, not public artifacts approved for publication.

## Verdict

**Ready** to retain and report this bounded qualification checkpoint. The target is met with preserved assets and transparent limitations. No candidate tuning or heavy architectural pivot is justified by this panel.

## Recommended next actions

Keep the installed foundation unchanged. If the user proceeds, verify the app-native connection after catalog refresh and use distinct fresh requests in a bounded real-use pilot. Do not recycle this successful panel as a tuning oracle or claim tool-time savings as overall latency. Review instance3of3 is complete; no further review instance will start in this flow.
