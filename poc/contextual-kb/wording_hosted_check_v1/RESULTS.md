# Authorized hosted integration results

The full candidate setup completed successfully in this bounded diagnostic. No implementation changes or training were needed. These are exposed development cases, not sealed evaluation or a new broad accuracy qualification.

## Executed setup

Unchanged foundation planner -> wording_candidate_v1 adapter -> unchanged strict validation -> frozen GLiNER advisory extractor -> full-question retrieval -> retrieval_repair_v1 hosted selector -> original fact/citation packet -> real calling agent. Model settings and existing runtime contracts unchanged. Both GLiNER seeds 1701 and 1702 used.

Two saved F01 raw-plan replays deliberately exercised the wording rewrite with the actual hosted selector. Both succeeded, each making one grammatical rewrite and preserving the ledger. Selector decisions kept the baseline packet. These are saved-plan reproductions, not new foundation generations.

Two real calling-agent batches asked F01, M03, M05 and M07 once each through the actual stdio MCP, with no planner/selector substitutions or retries. All eight calls delivered successful packets. Their fresh plans already passed strict validation; none needed the wording rewrite. Together with the saved replays, all ten actual hosted selector calls completed successfully, without fallback.

## Answers and observed selection

| Case | Seed 1701 | Seed 1702 | Evidence interpretation |
| --- | --- | --- | --- |
| F01: disabled dependency, callback argument/model access | supported | supported | Callback receives field; use field.model in its actual scope; ancestor-disabled caveat retained. |
| M03: required dependency without subscription, evaluation context | partial | partial | Callback context supplied, but exact props.required recipe/validation behavior remains unsupported by stored knowledge. |
| M05: synchronous validator and custom message | not_supported | not_supported | Caller acknowledges the knowledge gap, gives no invented implementation. |
| M07: resetOnHide false value and control behavior | supported | supported | Value retention distinguished from control-tree membership; re-registration explained. |

Both live M03 packets added `expression-callbacks-and-hooks/modern-callback-field-argument` in a single-slot replacement. The other eight selector decisions were unchanged. This demonstrates the repair through a real calling agent and MCP. It does not establish the missing required recipe or a higher broad full-answer accuracy rate. The source remains the same bounded knowledge sample.

## Audit and latency

All ten packets passed strict validation, raw/canonical normalization provenance, original baseline full-query replay, stored fact and citation identity, depth-20 full-question query preservation, at-most-eight unique facts/at-most-two replacement bounds, and model/DB integrity checks. The eight caller-delivered packets exactly match server audit records. Actual selector input was reconstructed, matched to persisted hosted input, and its returned decision replayed to the final packet. Fresh planner raw events match retained original-plan provenance. The ten selectors have successful process receipts and raw generation events.

Hosted selector median was 6.70 seconds in this small sequential sample. Native first-request times were 28.28 and 30.27 seconds including cold model setup; later requests were 10.37–16.16 seconds. These are observed diagnostic timings, not an SLA or a repeated stability estimate.

Both preceding candidate final-freeze manifests and all recursive protected chains matched before/after. Evaluation was hash-checked only and remains sealed. Runtime source, models and data/DB unchanged. No new dependencies, default registration, commits or publication. The 66-test regression result from the preceding immutable candidate remains provenance; this turn adds full hosted integration evidence rather than rerunning unchanged unit suites.

Independent review: REVIEW.md and REVIEW-DECISION.json. Raw evidence: test-output/saved, test-output/native, test-output/audit.json. The previous rejected hosted attempt and no-op local evidence remain unchanged in the earlier candidate directory; this separate authorized run supplies the previously missing hosted evidence.
