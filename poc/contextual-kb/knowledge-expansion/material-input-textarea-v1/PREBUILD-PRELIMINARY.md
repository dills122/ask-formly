# Independent preliminary review

Review instance: 1 of 3. Recorded before reading REVIEW-AUTHOR.md.

Reviewed branch `codex/material-input-textarea`, HEAD `e5027e77c4807636db3ea943ff8edd561065d6cf`. The target is the new untracked batch directory only; numerous unrelated untracked files remain outside scope. No tracked implementation diff was present.

Read the plan, cases, calls, source decisions, draft facts, candidate builder, transport/server, results auditor and all four test modules. Graph lookup returned no symbols; coverage reported all eight Python paths untracked, so conclusions use direct full-source inspection rather than graph completeness.

The five mappings agree with retained K47/K51 implementation: input type getter falls back to text and number uses its own branch; both branches forward the listed properties; textarea defaults rows/cols to 1 and forwards the three CDK autosize inputs plus class. Required is correctly described as the `required` binding rather than asserted to be a direct props binding. Explicit limitations avoid parsing, payload, layout and browser guarantees. Both retained source SHA256 values match the catalog. The authored quotes match the designated guide rows; detailed claims require the upstream implementation evidence, not those summary rows alone.

The builder checks for a freeze before output creation, uses exclusive isolated directories and copies authored inputs, preserves rows across eight tables, checks foreign keys and quote offsets, and invokes eligibility validation. Production paths are not build outputs. Transport calls unchanged model-free factories under the offline guard with separate settings. Candidate DB hash is appropriately pending at this prebuild stage.

All 18 batch unit tests passed. They exercise preservation rejection, missing freeze, count mismatch, wiring drift, offline startup, reservation collisions, error receipts, observed-ID fetch restrictions, frozen calls/scope, citation membership and repeat differences. No candidate build or qualification run was performed.

Preliminary concerns to retain for final review: results.py audits provenance and equality but does not itself enforce page/fetch size budgets or semantically grade answers; those must be inspected in the final packet audit. Repair language in PLAN.md must not be interpreted as permission to alter frozen initial calls, which the auditor correctly rejects. Existing input evidence may already support input questions; baseline scoring must credit delivered source excerpts rather than require newly authored IDs. A source/claim review is not runtime or final-answer qualification.

No blocking source or build-safety defect identified in this preliminary pass.
