# V11 clarified scope/history and JSON delivery

V11 completed24 fresh requests and6 diagnostics, each repeated3, with independent review. All90 responses are valid structured JSON and all12 batches exactly match standard encoding of their original response objects. All global scope projections pass. Diagnostic18/18 passes cover the earlier unknown-scope, normalization, source-copy, event/gate, and setup-history cases under the declared v11 interpretation.

Strict frozen fresh score is70/72, with two material interpretation ambiguities. The candidate therefore does not pass its predeclared perfect fresh gate and is not promoted. This does not establish two unambiguous user-intent misunderstandings. Retain evidence and alternative readings explicitly rather than silently changing grades.

| Measure | Fresh | Diagnostics |
| --- | --- | --- |
| Scheduled responses | 72 | 18 |
| Structural / literal-copy validity | 72/72 | 18/18 |
| Question text / semantic including globals | 70/72 | 18/18 |
| Complete correct bindings under frozen criteria | 71/72 | 18/18 |
| Joint usable | 70/72 | 18/18 |
| Requests passing all3 repeats | 22/24 | 6/6 |
| Question meaning stable, primary reading | 22/24 | 6/6 |
| Ledger obligations stable, primary reading | 23/24 | 6/6 |
| Exact canonical JSON identical | 2/24 | 0/6 |

Fresh joint per run23/24,24/24,23/24; diagnostic6/6 every run. Combined88/90 joint,28/30 all-three. No excluded slots, salvage, repaired JSON, retries or resampling.

## What changed and held up

Wholly unknown global version is explicitly null; tentative concrete versions/ranges/alternatives retain grounded uncertain strings. Explicit unknown scope still appears in questions and ledger. Prior U10 now returns null3/3; Q19 unknown-adapter ledger diagnostic passes3/3.

Same-field requested starting setup may remain grounded prospective/historical context in a follow-up; local technique limits do not become limits on another operation, and explicit independence overrides context sharing. U22 diagnostic passes3/3 under its prospectively clarified rubric. Other five diagnostic rubrics unchanged. U22's criterion changed, so it is not a pure behavioral improvement over old scores.

New delivery.serialize_batch encodes structured first-response records with standard json.dumps, ensure_ascii=False and allow_nan=False. Every retained producer contains one literal rows assignment and a direct serializer write. AST literal reconstruction, without rerunning producers, proves saved output bytes equal standard encoding for all12packets. Quotes, backslashes and multiline literal values survive delivery. This is enforced experiment serialization, not a claim that a text-only LLM or deployed API always produces valid JSON. No semantic filtering/repair is hidden in the serializer; wrong-but-encodable objects remain available for scoring.

## Two remaining interpretation-sensitive mismatches

**V04 run1:** observation question includes the same field's requested options.formState.locked configuration, and binds it to observation as well as configuration. Frozen rubric interprets “Separately” as keeping that dependency local to configuration. Reviewer retains text/semantic/binding failure. But source also says “same field”, and the inherited contract permits related dependency context; output labels it requested configuration and adds no only-if gate. A broader grounded-context reading is defensible. This is a definite rubric mismatch, not a demonstrated unambiguous misunderstanding.

**V24 run3:** configuration adds “if that dependency is supported”, while source explicitly places the narrower support gate on observation. Frozen strict attachment fails text/semantic; source ledger assignments remain correct. Reviewer also finds a defensible reading as a harmless applicability caveat because dependency support is explicitly requested. Preserve this disagreement rather than assuming either interpretation is uniquely forced.

Separate sensitivities: accepting either interpretation gives fresh71/72 and23/24 all-three; accepting both gives72/72 and24/24 all-three. Diagnostics stay18/18. These are post-review interpretation alternatives, not revised primary grades or a claim of production readiness. No old evidence changed.

## Verification and decision

14v11 tests (8selector/transport plus6delivery),8v10 regressions and8scorer tests pass independently:30/30. TDD red was missing modules; unit tests establish transport/encoding properties, while actual90-response review supplies semantic evidence. Reviewer checked every source/output pair, all four prompt/delivery/request packets,12producer/raw pairs, hint invariance, strict parser rejection of old malformed text, and six local freezes. Review1 verdict Not ready under frozen fresh gate; evidence complete and mechanical checks sound. No replacement reviewer or post-freeze tuning.

The targeted clarification and delivery work is supported in this bounded sample. Remaining uncertainty concerns acceptable cross-question context and prerequisite wording. Before treating further prompt changes as improvements, settle those acceptance distinctions with unambiguous source contrasts; repeating broad prompt growth against ambiguous expectations would not establish better library-question reasoning. This trial ends with v11 preserved, without changing a baseline or wiring a runtime service.

Prompt22,859bytes versus20,999v10; latency/cost unmeasured. Native modelrevision/temperature/seed uncontrolled; correlated policy-informed synthetic development, no contemporaneous causal baseline comparison. No sealed-evaluation, production, retrieval, final-answer or universal compatibility claim. Hashes establish preserved bytes, not unseen attempts or independently proven chronology.

All existing candidates/baselines/data/DB unchanged:39 inherited manifests/38,688 overlapping entries verified. Sealed evaluation remained opaque byte hashes. Only new refinement_v11 files written. Full artifacts: REVIEW-1.md, REVIEW-RESPONSE.md, test-output/aggregate.json, semantic-review.json, stability-review.json, all-questions.md and delivery-verification.json.
