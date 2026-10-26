# Bounded caller-scope correction

The first three-repeat run remains untouched under test-output/r1,r2,r3. Its 165 MCP calls had no operational errors, but candidate J10 fetched with ui_adapter:null after a Material lookup in all three repeats. The exact returned fact is core-scoped; no evidence corruption or unsupported adapter assertion was observed. Nevertheless same-scope protocol failed3times, so this run is NOT qualified. mechanical-audit.json records passed:false. Do not replace these failures with later results.

The defect is in this conversation's hand-authored fetch arguments, not either runtime or the data. New test-only scope.fetch_arguments copies the resolved version/adapter from each actual lookup; two TDD tests catch omission of Material. No production change, revised fact, changed plan, expanded search budget or altered semantic criterion. The original freeze stays intact; a separate correction freeze covers the new caller helper/audit and bounded new run.

After independent correction review, perform one complete fresh comparison in test-output/corrected/r1,r2,r3. Identical cases, original frozen plans, DB hashes, batch layout, semantic gate and discovery decisions. Every actual call executes again. Fetch IDs must have been seen in that case's delivered/discovery records and scope comes from that run's lookup packet. Preserve all 90 observation slots, six honest out-of-scope no-call decisions and every failure. No failed call retry or mid-run tuning.

The root caller authored30 distinct answers after reading first-pass packets. Identical fresh full evidence is checked before retaining the same answer. This is 15fixed semantic scenarios per arm with repeat consistency, NOT90independently generated answers, an independent question-planner benchmark, or a statistical generalization estimate. Final fresh reviewer audits answer meaning and provenance separately; first-generation shared-context/oracle visibility remains a limitation.

A semantic gate pass alone is insufficient: mechanical-audit passed must also be true. Publication/promotion remain unauthorized. Review budget stays max3: pre-run1, correction2, final3.
