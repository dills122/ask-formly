# Source admission checklist

Generated from the reviewed ledger. Mechanical completeness is not proof that every semantic claim was correctly interpreted.

Section counts: admitted=1, excluded=0, existing_support=0, pending=0.

## formly.arrays

Source: `skill/ask-formly/references/arrays.md`; SHA-256 `8148916df949ea755be0e7f246e1242a0b68437b47da650444a6c8726a725c5e`.

- [x] **Arrays and repeatable sections** (lines 1–15) — admitted. All seven source paragraphs accounted for by six source-reviewed candidate facts, reused existing support and explicit limits/exclusions.
  - Version and test-execution limits — **excluded**; facts: none. Exclude any newly executed upstream-test claim; retain exact 6.3.12 scope. Independent source-mapping review pending.
  - Array template and instantiated children — **admitted**; facts: `array-operations/template-and-children`. K12 verified: existing control reuse/new FormArray is keyed; null item keys are retained. Draft bounded construction fact. Independent source-mapping review pending.
  - Repeater component and registration — **admitted**; facts: `array-repeat-example/registered-repeat-renderer`. E01a/b/c and K03 verified. Scope to official repeat string alias; direct component classes do not universally require an alias. Existing general registration facts reused. Independent source-mapping review pending.
  - Coordinated add/remove operations — **admitted**; facts: `array-operations/add-coordination`, `array-operations/remove-coordination`. K12 verified: model mutation, rebuild and event sequence, conditional dirty marking and removal key updates. Valid initialized model/index conditions retained. Independent source-mapping review pending.
  - Falsy initialModel boundary — **admitted**; facts: `array-operations/falsy-initial-model`. K12 verified: undefined insertion branch for falsy initialModel; post-build/default outcomes are not fixed by this branch. Independent source-mapping review pending.
  - Defaults/hiding/insertion and patch boundaries — **admitted**; facts: `array-operations/default-insertion-test-scope`, `hiding-and-visibility/hide-can-clear-array-children`. K27 verified: exact inspected default/hide/insertion test assertions only; reuse installed cleanup support. Exclude earlier patch equivalence, universal ordering and executed tests. Independent source-mapping review pending.
  - Material adaptation limits — **admitted**; facts: `array-repeat-example/registered-repeat-renderer`. E01b/c verify Bootstrap import/classes; retain adaptation caveat, exclude tested/turnkey Material UI and application verification claims. Independent source-mapping review pending.

