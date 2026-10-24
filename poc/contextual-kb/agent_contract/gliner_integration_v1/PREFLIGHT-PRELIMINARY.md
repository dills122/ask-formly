# Preflight preliminary review
Review instance: 1 of 3. Recorded before reading AUTHOR-EXPLANATION.md.

Scope verified at HEAD c3091328f49d53de6b41a49c4fe5aa8f1c45e516 with preexisting dirty main. Only integration review artifacts writable. Direct source fallback used for all seven relevant Python files; graph generation 2026-10-16 reports not_tracked. No model execution or sealed evaluation semantic access.

13 unit tests pass. All 174 foundation objects validate. All 44 gold rows were read against their question and six-role contract; offsets match exact text. All 12 fresh request/output pairs read, including ledger and constraints. No material fresh foundation semantic failure identified.

Preliminary concerns requiring adjudication before inference:
- I05-q0/q1 model.needsReview is used as the supplied controlling expression, not presented as a library API; recommend value, or explicitly preserve ambiguity rather than fixed api_reference.
- P10-r1-q0 field key is explicitly discussed against model path in Formly configuration; omission of key may be an annotation miss or ambiguous natural-language/property boundary.
- P14-r1-q0 comparison operators included in version spans need explicit boundary rationale under token-only version rule.
- P04-r1-q0 inner registration occurrence sits inside quoted setup narrative; clarify whether protocol excludes only narrative as a whole or also grounded mentions inside it.
- P28/P36 options.formState custom suffix paths can be complete API references or controlling expressions under the current wording; needs a consistent predeclared rule alongside I05.

Code preserves foundation projection and uses frozen optional_hints rejection. Run harness checks ready verdict and frozen hashes before work. No aggregate evaluator yet in scope; alternatives need a concrete representation and scoring semantics before predictions if used. Tentative verdict not_ready pending gold adjudication.
