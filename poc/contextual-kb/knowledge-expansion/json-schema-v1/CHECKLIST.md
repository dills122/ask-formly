# JSON Schema source checklist

Candidate-only decisions; installed foundation9 remains unchanged.

- excluded — paragraph 1: # JSON Schema conversion; Section heading or scope metadata
- excluded — paragraph 2: Baseline: 6.3.12. JSON Schema, Formly configuration, and an application's own JSON form format are different contracts.; Section heading or scope metadata
- admitted_candidate — paragraph 3: `FormlyJsonschema` from `@ngx-formly/core/json-schema` converts a `JSONSchema7` input with `toFieldConfig`. The result is **one field config; json-schema-conversion/conversion-api
- excluded — paragraph 4: ## Conversion is not complete UI registration; Section heading or scope metadata
- admitted_candidate — paragraph 5: The official JSON Schema demo registers renderers for structures such as object, array, null, and multischema. Its setup is part of the exam; json-schema-conversion/renderer-registration
- pending — paragraph 6: Before authoring, inspect the schema's required shapes and the application's matching registrations. A converter result is not proof that th; Outside conversion/registration/customization/reference batch; no coverage inferred
- excluded — paragraph 7: ## Overrides and mapping; Section heading or scope metadata
- admitted_candidate — paragraph 8: The inspected conversion merges `widget.formlyConfig`, aligns the legacy `templateOptions` alias with `props`, then invokes a supplied `map`; json-schema-conversion/customization-order, json-schema-conversion/map-return
- pending — paragraph 9: Application JSON must remain serializable. Runtime callbacks, Observables, templates, and services belong in application code or an explicit; Outside conversion/registration/customization/reference batch; no coverage inferred
- excluded — paragraph 10: ## References and scope limits; Section heading or scope metadata
- admitted_candidate — paragraph 11: The resolver rejects `$ref` values with a remote URI and handles local references. Do not promise remote schema fetching, arbitrary referenc; json-schema-conversion/local-references, json-schema-conversion/remote-references
- pending — paragraph 12: The converter paths were source-read; selected pattern/enum/composition limits now have focused observations in [evaluation evidence](evalua; Outside conversion/registration/customization/reference batch; no coverage inferred
- excluded — paragraph 13: ## Mapping details and failure modes; Section heading or scope metadata
- pending — paragraph 14: - **Numbers and integers:** the converter installs parsers, maps minimum/maximum, and adds exclusive-bound/multipleOf checks. Empty string/u; Outside conversion/registration/customization/reference batch; no coverage inferred
- pending — paragraph 15: The converter has no dedicated `format` mapping/validation path in the inspected full implementation. Do not assume `format: 'date'` selects; Outside conversion/registration/customization/reference batch; no coverage inferred
- pending — paragraph 16: R13 executes basic conversion and remote-ref rejection. Numeric input regressions have separate fix boundaries: I3901 and I3937 point to 6.3; Outside conversion/registration/customization/reference batch; no coverage inferred
- excluded — paragraph 17: ## Focused checks; Section heading or scope metadata
- pending — paragraph 18: For a concrete schema, verify conversion, registration, rendering, required/error behavior, nested array changes, defaults, and submitted mo; Outside conversion/registration/customization/reference batch; no coverage inferred
