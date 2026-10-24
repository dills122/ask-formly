# Preliminary independent review
Review instance: 1 of 3. Recorded before AUTHOR-EXPLANATION.md.

All 72 raw responses read against the requests. Eight harness tests and inherited byte-hash audit pass. Preliminary concern: structurally valid responses can omit active condition bindings while preserving the conditions in their question text. Concrete example S12 run3 omits the no-substitution exclusion; S16 omits the hiding scenario from all three binding lists; S17 lists scope only and omits the model.needsPermit dependency. The semantic search questions otherwise preserve those meanings, so binding completeness and semantic usefulness must be separated.

Rubric interpretation requires care: S06's model.expedited predicate is natural scenario context for both questions; S19 explicitly allows defaultValue on the control question; S22's no-polling restriction naturally attaches to observing changes, particularly in the request's restatement. Do not mechanically penalize these as leakage or omission. S12's split existence/contingent-meaning lookup is legitimate despite the rubric's preference for one coherent lookup.

Need independently reconstruct records/structure from raw files, verify input/raw freezes, inspect experiment delivery, and reconcile author claims. No protected artifacts changed; no sealed case content inspected.
