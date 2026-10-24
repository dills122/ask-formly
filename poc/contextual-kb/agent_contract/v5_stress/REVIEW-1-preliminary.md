# Preliminary independent review
Review instance: 1 of 3. Recorded before opening AUTHOR-EXPLANATION.md.

Reviewed all 72 response objects alongside all 24 source requests and frozen rubrics, plus v5 CONTRACT/LEDGER-RULES, protocol, data-review and plan. Dirty main is the stated boundary; unrelated working-tree changes excluded. No candidate/output changes.

Preliminary concerns:
- T03 runs 2–3 retain single-field invocation eligibility but do not ask whether single-field support exists; unlike run 1 there is neither an ungated support question nor an explicit support-check clause.
- T11 all runs omit the corrected required dependency from the standalone message question and its bindings.
- T17 all runs omit the outer async-support contingency from the final named-message lookup and ledger. The message-support condition remains, but the independently required nested eligibility is absent.
- T18 run 3 preserves unresolved versions in question/ledger but drops them from global formly_version.
- T21 run 2 retains the custom-rule exclusion in both questions but omits its ledger binding.

No failure assigned merely for extra grounded context, excerpt segmentation, optional same-field history, or a question-count difference. Question meaning and ledger meaning will be evaluated separately; stable mistakes do not count as correct responses. Remaining work: source/harness and preservation verification, optional-hint probes, author-claim reconciliation and final machine-readable grades.
