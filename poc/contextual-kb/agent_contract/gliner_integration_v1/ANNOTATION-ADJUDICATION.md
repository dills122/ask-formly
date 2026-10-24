# Prospective annotation decisions

Decided before either extractor runs; initial gold remains unchanged in gold-initial.json. Final gold.json has44rows and87mentions. No model output informed these decisions.

- P10: add key at58:61 as api_reference because this question explicitly asks about the field configuration key and model path relationship.
- P14: version mentions are numeric tokens6.2 at13:16 and7 at18:19. Comparators remain in the authoritative question, not inside version tokens. This interprets label guidance to include compared versions, not to encode comparison operators in the token.
- P04: retain both quoted registration-name occurrences. Protocol's quoted narrative exclusion means do not treat the surrounding narrative claim as a value. Explicit names inside narrative still count under the registration label. No whole quoted claim is annotated.
- I05: classify bare model.needsReview as value, an explicit supplied dependency expression accessing application model data. For this integration annotation convention, complete paths rooted at named Formly configuration APIs (e.g. options.formState.region and options.formState.busy) remain api_reference; a bare model-data expression is value. This is a prospective adjudication of a real role ambiguity, not an undisputed annotation fact or assertion that such code works. P26's compound model.delivery === 'courier' remains one opaque value. Frozen model labels and weights are unchanged. Report this convention as a limitation; do not call a disagreement on I05 a proven universal role error.

The independent preflight reviewed all44rows and12fresh request outputs before extraction. Gold edits are limited to the changes above; initial annotations retained for provenance. No alternatives remain under this fixed operational convention.
