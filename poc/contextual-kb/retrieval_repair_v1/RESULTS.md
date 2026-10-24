# Bounded retrieval repair results

The targeted retrieval miss is repaired in all three saved M03 plans. Conditional retrieval regression checks pass; the original overall qualification gate does not pass. This is an opt-in candidate, not a replacement of the accepted MCP foundation.

## What changed

Original full-question retrieval and its eight-slot packet run unchanged. The new stage acquires lexical and dense depth-20 candidates using the same question text, then asks a separate semantic selector for at most two paired replacements. A new fact must supply missing requested support; a removed fact must support none of the requested aspects. Existing corroborating support is protected by the selector instructions. Structural validation enforces bounds, membership and exact evidence quotes, but does not prove semantic relevance. Invalid or failed selection falls back explicitly; integrity failures remain hard failures. No training, knowledge changes, or GLiNER changes.

## Fixed packet experiment

84 scheduled slots: 12 original diagnostic plans, 36 historical labeled plans, and 12 fresh requests with three selector repetitions each. Fresh foundation outputs were generated once and frozen before selection. There were 77 actual selector calls, four empty-plan bypasses, and three unavailable slots from one upstream failure.

- All three original M03 failures gained `modern-callback-field-argument`, replacing the unrelated `props-generic-scope` fact.
- Across 81 valid-plan slots: no labeled relevant baseline facts lost, no previously covered required groups lost, and no unsupported-case replacements.
- Nine packets changed, each by one slot. Three historical packets gained a labeled relevant fact. The remaining changes include the three targeted diagnostics and three semantically relevant additions outside historical gold labels.
- The six valid fresh callback repeats retained callback evidence already present in baseline. They are retention evidence, not six additional recovery successes. All valid fresh packets were unchanged.
- Selector median latency was 4.87 seconds (3.42–10.91 seconds), with three concurrent jobs. This is not whole-MCP latency.

Fresh F01 failed the unchanged foundation validator: its ledger excerpt `props.disabled to track model.isLocked` was not copied into its question, which said `props.disabled be configured to track model.isLocked`. The first output and all three failed scheduled slots remain in the evidence. It was not retried, repaired, or excluded from the overall gate. Consequently the strict overall gate is false. Historical R26 also retains its pre-existing semantic scope problem; this experiment measures retrieval conditional on the supplied plans.

The original coarse group-count assessment could hide a lost group if a different group was gained. Independent review identified that accounting risk. A separate tested assessment compares group identities; it confirmed zero lost groups. Original scores remain preserved. See ASSESSMENT-ADDENDUM.md and test-output/panel/final-gate.json.

## Real calling-agent MCP checks

Two real calling-agent runs used the new stdio server with frozen extractor seeds 1701 and 1702, each asking M03 (expressions), M05 (validators), and M07 (hiding). All six calls completed. Read-only replay verified exact original foundation retrieval and full-query parity, client/server packet identity, original stored fact/citation identity, eight-slot bounds, unchanged model parameters, and unchanged DB.

Both runs answered M03 partially with correct callback context and an explicit missing `props.required` recipe; M05 was unsupported because validator/message knowledge is absent; M07 was supported with the value-retention versus control-registration distinction. These fresh live M03 plans already retrieved callback context in the original packet. All six selectors returned unchanged. Thus the native checks prove integration and evidence handling, not live replacement execution or a causal improvement in final answers. The saved-plan experiment above establishes the replacement gain.

Native request latency was 28.34–31.29 seconds for the first expression request, including cold model setup, and 10.39–16.51 seconds for subsequent requests. Selection accounted for 3.69–8.74 seconds per request. This extra model call is a material latency cost.

## Verification and limits

11 new tests pass (seven policy, two integration, two group-identity assessment); the independent reviewer also ran the original 11 MCP and 35 advisory tests, plus mocked selector lifecycle and server-wiring checks. See REVIEW.md for the independent verdict.

This does not add the missing required/validator recipes, establish whole-library answer coverage, or prove a 90% end-to-end answer rate. Both extractors and the foundation remain unchanged. Protected manifests and DB hashes match; sealed evaluation was not read. The accepted MCP remains the default. The bounded candidate is available through the launcher documented in README.md, with the overall qualification failure explicitly retained.

Evidence: test-output/panel/{inputs.json,all-decisions.json,per-group-audit.json,final-gate.json}; test-output/native/{1701,1702}; test-output/native/audit-summary.json; design/fresh/input freeze manifests.
