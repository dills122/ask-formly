# Findings

## Source evidence
Pinned Formly commit: 5f099fddea6426b46a453866adf0fede5be0bcd7. K13 aggregate module excludes datepicker; K18 registers datepicker with form-field wrapper and does not supply a date-adapter implementation; K19 declares/binds nested date options and exact callback arguments. Downloaded full files match catalog SHA256. Initial web fetch returned cache misses; direct HTTPS download of the same public pinned files succeeded and was hash-verified. Frozen references/catalog unchanged.

## Admission boundaries
Five facts, one Material-only exact6.3.12 document. Module registration does not establish adapter/value/locale/timezone compatibility. startAt/calendar view does not prove model assignment. Callback forwarding is not proof of model commit or event order. No new evidence IDs or runtime changes needed.

## Qualification observations
The installed99-fact baseline retrieves related Formly concepts but lacks datepicker-specific contracts for these10requests. Bounded discovery did not repair that gap. The104-fact candidate delivers the necessary evidence directly in9/10datepicker cases; the combined registration/limits/adapter question requires fetching an observed omitted registration fact. All5existing/scope controls retained. This tests evidence delivery and caller judgments, not browser integration or unseen generalization.

## Safety and review
Two prebuild artifact-safety defects in copied batch scaffolding were fixed with tests; existing POC scaffolds/runtimes untouched. The compiler initially rejected K13 evidence because the narrow registration quote cited onlyK18; the corrected exact contiguous quotation includes both source citations. Failed tests and lint diagnosis retained in progress/review history. Final review audits answer semantics separately from mechanical scores.
