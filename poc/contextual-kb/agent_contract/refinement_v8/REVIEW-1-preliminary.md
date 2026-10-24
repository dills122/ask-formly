# Preliminary independent review

Review instance: 1 of 3. Written before reading AUTHOR-EXPLANATION.md or AUTHOR.md. Fresh reviewer context contains the neutral bootstrap and task assignment, not the author's implementation conversation. Skills: independent-review and code-review-and-quality; codebase-memory coverage was checked and direct source used for not_tracked files.

Scope: new refinement_v8 only, on dirty main. Numerous pre-existing changes are outside this review. Read protocol, contract, change, data-review, all 27 source requests/rubrics and every question, reason, constraint and binding in all 81 outputs. No protected semantic payload read. No changes to candidate, inputs or outputs.

Preliminary findings:
- C12 run 1: the question text preserves conditional restricted wrapper attachment, but the ledger declares `a wrapper can be reused`, absent from the source (`can a wrapper be reused`). This invalid source binding prevents structural acceptance and fails source attachment independently of the good question meaning.
- C14 runs 1–3: the disabled question says `for a select whose options arrive after the field has been initialized`, and binds late arrival to both questions. This is a restrictive scenario qualification, not merely historical context; under the frozen rubric it narrows the independent disabled lookup. There is genuine source ambiguity around `that select`: it could denote the same late-loading select. The frozen rubric and pre-generation clarification explicitly distinguish the scenarios, however, so the narrower generated wording is a failure against that interpretation. Do not silently waive or claim a pristine fresh-panel gate.
- Event-ledger diagnostic F04/F05/F23 responses preserve events, local/shared restrictions and independent post-change value reading in all three runs.

All six v8, six v7 and eight aggregation unit tests independently passed using python3 -B. These validate transport, not semantic sufficiency. Remaining work: verify preservation/freezes/packet and raw reconstruction, check hint invariance across all 81 slots, persist individual grades and stability, then reconcile author testimony.
