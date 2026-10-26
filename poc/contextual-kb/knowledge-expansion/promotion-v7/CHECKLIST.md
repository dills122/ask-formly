# Source admission checklist

Generated from the reviewed ledger. Mechanical completeness is not proof that every semantic claim was correctly interpreted.

Section counts: admitted=1, excluded=0, existing_support=0, pending=10.

## formly.material

Source: `skill/ask-formly/references/material.md`; SHA-256 `142080d97cf914b24f713f0423f903b071bb1b32737bef8d10d14ee146f40e9b`.

- [ ] **Angular Material adapter** (lines 1–4) — pending. Outside the installed select batch; this section remains pending for separate review.
  - Baseline: Formly 6.3.12. Angular Material/CDK and the application's date adapter must be checked sep — **pending**; facts: none. Outside the bounded select batch; retained for a later Material source review.
- [ ] **Modules and registered controls** (lines 5–10) — pending. Outside the installed select batch; this section remains pending for separate review.
  - `FormlyMaterialModule` imports the form-field integration and input, textarea, radio, checkbox, mult — **pending**; facts: none. Outside the bounded select batch; retained for a later Material source review.
  - Use the consuming application's v6 module setup, including reactive forms and Formly configuration.  — **pending**; facts: none. Outside the bounded select batch; retained for a later Material source review.
- [x] **Select options and identity** (lines 11–18) — admitted. Mapped select claims are installed in foundation8; unrelated decisions remain pending or explicitly excluded.
  - The option conversion pipe supports arrays and Observable sources. Labels, values, disabled state, a — **admitted**; facts: `material-select-options/option-mapping`, `material-select-options/option-groups`, `material-select-options/observable-consumption`, `material-select-options/expression-array-updates`. Exact K15/K14 bytes inspected: mapping/groups and select-owned helper lifecycle; no arbitrary application teardown guarantee.
  - The Material select's default `compareWith` uses strict equality. If the model stores an object and  — **admitted**; facts: `material-select-options/strict-comparison`, `material-select-options/multiple-and-change`. Exact K14/K15 bytes inspected: comparison is separate from mapping, renderer multiple/select-all conditions and callback arguments.
  - The selected upstream tests include rendering options and selection; they were read, not run. For ca — **excluded**; facts: none. Upstream K28 tests inspected, not executed. No extra fact for app-specific cascades or retained/cleared child-value policy; official-demo concern deferred.
- [ ] **Datepicker** (lines 19–26) — pending. Outside the installed select batch; this section remains pending for separate review.
  - Use `FormlyMatDatepickerModule` from `@ngx-formly/material/datepicker` when this entry point is need — **pending**; facts: none. Outside the bounded select batch; retained for a later Material source review.
  - The inspected renderer uses **`props.datepickerOptions`** for options including `min`, `max`, `filte — **pending**; facts: none. Outside the bounded select batch; retained for a later Material source review.
  - Test the actual model value type, parsing, invalid dates, boundaries, disabled state, and reset usin — **pending**; facts: none. Outside the bounded select batch; retained for a later Material source review.
- [ ] **Form-field decoration and custom controls** (lines 27–33) — pending. Outside the installed select batch; this section remains pending for separate review.
  - The wrapper exposes appearance, float label, color, hints, prefix/suffix, and other declared props.  — **pending**; facts: none. Outside the bounded select batch; retained for a later Material source review.
  - Material's `FieldType` implements the form-field control bridge, including focus and error-state coo — **pending**; facts: none. Outside the bounded select batch; retained for a later Material source review.
  - The slider module selects implementations using the CDK major version, with a boundary at 15. This p — **pending**; facts: none. Outside the bounded select batch; retained for a later Material source review.

## formly.material-controls

Source: `skill/ask-formly/references/material-controls.md`; SHA-256 `91f1242209fd56d87f05f4bed2ba08f98926feb4fb2735dc3a429160102df200`.

- [ ] **Material control contracts and integration checks** (lines 1–4) — pending. Outside the installed select batch; this section remains pending for separate review.
  - Scope: inspected Formly 6.3.12 renderers. Angular Material 21.2.14 with Angular 21.2.25 was used for — **pending**; facts: none. Outside the bounded select batch; retained for a later Material source review.
- [ ] **Common and secondary entry points** (lines 5–21) — pending. Outside the installed select batch; this section remains pending for separate review.
  - | Type | Important contract | Evidence | — **pending**; facts: none. Outside the bounded select batch; retained for a later Material source review.
  - The umbrella module's common imports are recorded in [K13](sources.md#k13). Additional registration  — **pending**; facts: none. Outside the bounded select batch; retained for a later Material source review.
- [ ] **Select details** (lines 22–29) — pending. Mapped select claims are installed in foundation8; unrelated decisions remain pending or explicitly excluded.
  - `compareWith` defaults to strict equality. `labelProp`/`valueProp` define mapping, while comparison  — **admitted**; facts: `material-select-options/strict-comparison`. Material equality versus mapping covered; native-select comparison remains outside this batch, not certified as equivalent.
  - Select-all flattens groups, excludes disabled options, and caches its value list by the options-arra — **admitted**; facts: `material-select-all/enabled-values`, `material-select-all/state-and-cache`. Exact K14 bytes inspected: flatten/filter, length-based toggle/state and transformed-options identity cache; no set-equality claim.
  - The select reads aria-label and aria-labelledby from props.attributes, with a wrapper-label fallback — **pending**; facts: none. Accessibility and panelClass are valid adjacent topics but deferred to keep this batch bounded.
- [ ] **Custom Material controls** (lines 30–43) — pending. Outside the installed select batch; this section remains pending for separate review.
  - For typed registration, use the [public ConfigOption-derived type](customization.md#types-and-regist — **pending**; facts: none. Outside the bounded select batch; retained for a later Material source review.
  - There are three separate contracts: — **pending**; facts: none. Outside the bounded select batch; retained for a later Material source review.
  - 1. **Angular value access:** how programmatic values, user values, touched, and disabled state reach — **pending**; facts: none. Outside the bounded select batch; retained for a later Material source review.
  - Passing one does not establish the others. Formly's Material `FieldType` is publicly re-exported fro — **pending**; facts: none. Outside the bounded select batch; retained for a later Material source review.
  - If a widget already owns its own mat-form-field or is a standalone button/layout, decide whether a F — **pending**; facts: none. Outside the bounded select batch; retained for a later Material source review.
- [ ] **Required markers, validation, and read-only presentation** (lines 44–49) — pending. Outside the installed select batch; this section remains pending for separate review.
  - Required state is behavior as well as decoration. A future-required asterisk with currently optional — **pending**; facts: none. Outside the bounded select batch; retained for a later Material source review.
  - For affirmative consent, explicitly validate true. For read-only review screens, distinguish an inpu — **pending**; facts: none. Outside the bounded select batch; retained for a later Material source review.
- [ ] **Appearance, dates, and upgrades** (lines 50–56) — pending. Outside the installed select batch; this section remains pending for separate review.
  - The Material 15 checkbox styling discussion contains user CSS workarounds and a report about a custo — **pending**; facts: none. Outside the bounded select batch; retained for a later Material source review.
  - A datepicker must be checked with the selected adapter's actual values, locale, parsing, and seriali — **pending**; facts: none. Outside the bounded select batch; retained for a later Material source review.
  - For SSR/hydration, I3824 is a specific textarea fix released in 6.3.0. The current template avoids t — **pending**; facts: none. Outside the bounded select batch; retained for a later Material source review.
