# Independent vocabulary challenge authorship

Authored 22 October 2026. Gold is ready for independent review; this note does not claim a completed independent audit or a scored result.

The author read only the POC AGENTS.md and STEERING.md, narrow_contract/CONTRACT.md, and narrow_contract/pilot/contract.py. No training examples, earlier evaluation examples, experimental outputs, failure analyses, extraction implementation, application code, database, or old sealed evaluations were consulted. The contract's own worked examples were visible as part of the allowed contract read. The supplied task established required API breadth and family themes.

fresh.json contains 40 caller-preserving narrow-mentions-v1 envelopes, with eight families of five questions. families.json maps each question ID to its family string. All gold envelopes use status ok and empty issues; disputed meanings were avoided during authorship. Questions request documentation or clarification and do not assert runtime behavior or API existence.

Coverage after author validation:

| Item | Count |
| --- | ---: |
| Questions | 40 |
| Families | 8 |
| Empty mention lists | 6 |
| api_reference mentions | 41 |
| registration_name mentions | 9 |
| model_key mentions | 8 |
| value mentions | 5 |
| version mentions | 9 |
| ui_adapter mentions | 8 |

The six empty questions are va-f04-q01 and all five conceptual_and_negative questions. Plain API coverage includes validators, asyncValidators, wrappers, expressions, expressionProperties, parsers, and focus. Class coverage includes FieldType, FieldWrapper, FieldArrayType, and FormGroup. deferLeafRefresh is intentionally hypothetical and explicitly presented as a possible API whose existence is in question.

Registration names reserved from training: 'juniper-entry', 'cedar-frame', 'quartz-check', 'willow-choice', 'harbor-shell', and 'cobalt-entry'. The names 'Material' and 'Bootstrap' are reserved in the registration_name role only; their ordinary ui_adapter use may occur in training. Reserved model-key spellings: 'applicant.postalCode', 'delivery.zone', 'profile.alias', 'invoice.reference', 'household.count', 'shipment.code', 'contact.region', and 'consent.accepted'. The hypothetical API deferLeafRefresh is also reserved from training. These reservations were communicated to the implementation lead before handoff.

Boundary checks: all mentions are source ordered and non-overlapping, each raw value equals question[start:end] using Python Unicode offsets, Markdown backticks are excluded, syntactic quotes are retained, bracketed paths are complete maximal spans, and the opaque arrow expression is one value without nested API mentions. Every envelope passed narrow_contract/pilot/contract.py validate. Family sizes, total question count, empty count, and minimum role counts were checked programmatically. No inference or training ran during authorship.

A separate reviewer must audit gold before freeze or scoring. Any revision should be recorded before the freeze; preserve the final reviewed fixture and its hash alongside subsequent results.
