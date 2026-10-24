# Preliminary independent review

Review instance: 1 of 3. Recorded before reading AUTHOR-EXPLANATION.md.

Scope is the untracked refinement_v4 candidate in a dirty main checkout; unrelated changes are excluded. Reviewed protocol, ledger rules, contract, tests, candidate, preservation wrapper, all cases/rubrics, all 48 question texts/reasons/scopes/bindings. Graph coverage reports candidate/test/preservation files untracked; conclusions use direct complete source reads.

Preliminary findings:
- D12 runs 1–3 retain the no-substitution exclusion but omit the rubric-mandatory existence contingency from the ledger. Question 1 preserves contingency semantically by paraphrase, so useful text is not a complete ledger.
- F01 runs 1–3 similarly omit the mandatory `If it exists` contingency binding, despite preserving it in meaning-question text.
- F07 run 1 binds `goes from visible to hidden` to both questions; the frozen rubric assigns that transition locally to model-value question 0. The second question still correctly asks about becoming visible again. This is a ledger-attachment failure under the strict predeclared rubric, with a reasonable semantic ambiguity because prior hiding is also background to becoming visible again.
- F03 includes `as 'postalEntry'` as an additional binding. The name is correctly paired with registration/use, grounded and active; policy says names are not automatically extra conditions, rather than categorically prohibiting such relationship excerpts. This does not independently warrant failure.
- No observed text-usefulness failures. The full candidate gate cannot pass with the clear contingency omissions even if the F07 ambiguity were resolved favorably.

Pending verification: execute tests, preservation chain and hash freezes; reconstruct records from raw files; verify projection invariance; reconcile author claims. No code/data/output changes or semantic sealed-data inspection performed.
