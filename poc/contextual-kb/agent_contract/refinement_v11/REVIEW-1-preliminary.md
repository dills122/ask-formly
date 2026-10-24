# Independent preliminary review
Review instance: 1 of 3. Recorded before reading AUTHOR-EXPLANATION.md. Fresh reviewer context contained bootstrap and task, not parent semantic grades.

Scope is refinement_v11 on dirty main at c3091328f49d53de6b41a49c4fe5aa8f1c45e516; inherited unrelated changes are outside this review. Read protocol, change, delivery, tests before implementation, contract, all 30 requests/rubrics and all 90 raw outputs. No producer execution or sealed semantic reads.

Definite failure: V04 run 1 adds the separately requested options.formState.locked dependency to the observation question and binds it to index 0. The frozen rubric explicitly forbids that back-propagation. Runs 2 and 3 keep the questions separate. This defeats the fresh all-three gate even with successful JSON delivery.

Interpretation issue to resolve explicitly: V24 run 3 adds “if that dependency is supported” to configuration, where the source's narrower support gate explicitly introduces observation. The contract permits prerequisite lookups, but prohibits invented eligibility. I lean toward a text-semantic failure for the added gate; its ledger remains correctly attached to observation only. The other runs do not add this configuration gate.

Other inspected outputs preserve requested aspects, scope and meaningful exact bindings. V14 global “version 6 or version 7” retains unresolved alternatives rather than choosing a version. V17 run 1's “it becomes visible again” preserves the return event, with “after” in question text; no additional duplicate hide binding is required. C12 run 3 repeats the support interrogative within its use question; this is redundant but does not change requested meaning. U22 all runs explicitly identify requested/prospective setup and pass the prospective criterion; this is not causal improvement over older grading.

Pending: independent tests, strict parsing/exact excerpts, AST-to-byte delivery verification, packet and preservation manifests, hint invariance, and author-claim reconciliation. Preliminary verdict: Not ready for the predeclared fresh acceptance gate.
