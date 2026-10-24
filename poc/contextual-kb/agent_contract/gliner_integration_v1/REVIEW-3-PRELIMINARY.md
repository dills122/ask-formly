# Preliminary independent review

Review instance: 3 of 3. Recorded before reading RESULTS-AUTHOR.md or RESULTS-DRAFT.md.

Inspected frozen CONTRACT/PROTOCOL, annotation adjudication, all 44 gold rows and both models' per-case differences, assessment/integration/run code, 22 tests, frozen foundation projection, raw evidence shapes and reported scores. Scope is the untracked gliner_integration_v1 subtree at c3091328f49d53de6b41a49c4fe5aa8f1c45e516; unrelated dirty root changes excluded. October 16 graph has no subtree records, so direct source reads provide coverage.

Preliminary judgment: safe advisory integration appears supported, but neither model meets the predeclared annotation precision criterion. Both have 77 true positives and 10 misses; 1701 has 9 false positives, 1702 has 8. Precision 89.53%/90.59% is below 95%; recall 88.51% exceeds 80%. Both cover 32/34 gold-nonempty questions with no positive predictions on 10 gold-empty controls. Structural acceptance cannot repair semantic/boundary errors. Raw and accepted metrics match on the annotated panel; this is not evidence of semantic validation. Fixed I05 adjudication is a convention, not universal semantic truth.

Before final verdict, independently check all three arms' records, full extraction accounting, each row's raw and accepted scoring, timing sums and quantiles, retained checkpoint hashes, freezes and all 43 protected manifest contents; reconcile author claims only after this preliminary file exists. Pure replay and hashes are allowed; no inference or fixes.
