# JSON Schema conversion

Baseline: 6.3.12. JSON Schema, Formly configuration, and an application's own JSON form format are different contracts.

`FormlyJsonschema` from `@ngx-formly/core/json-schema` converts a `JSONSchema7` input with `toFieldConfig`. The result is **one field configuration**, commonly placed in the outer fields array. The converter clones the input and derives field properties such as type and label. Do not present the conversion as a general serializer of arbitrary TypeScript fields. [K20](sources.md#k20)

## Conversion is not complete UI registration

The official JSON Schema demo registers renderers for structures such as object, array, null, and multischema. Its setup is part of the example, not incidental boilerplate. Likewise, the selected converter tests explicitly register types. Importing the common Material module alone does not establish renderers for every converted schema shape. [E05](examples.md#e05), [K34](sources.md#k34)

Before authoring, inspect the schema's required shapes and the application's matching registrations. A converter result is not proof that the form renders correctly or produces the required payload.

## Overrides and mapping

The inspected conversion merges `widget.formlyConfig`, aligns the legacy `templateOptions` alias with `props`, then invokes a supplied `map` callback. If conversion output is surprising, inspect these layers before changing the schema itself. Return the intended field from a mapping callback. [K21](sources.md#k21)

Application JSON must remain serializable. Runtime callbacks, Observables, templates, and services belong in application code or an explicitly designed resolver layer, not unexplained function values inside claimed JSON.

## References and scope limits

The resolver rejects `$ref` values with a remote URI and handles local references. Do not promise remote schema fetching, arbitrary reference resolution, every JSON Schema draft, or complete Draft 7 conformance based on the accepted TypeScript input type. [K22](sources.md#k22)

The converter paths were source-read; selected pattern/enum/composition limits now have focused observations in [evaluation evidence](evaluation-evidence.json). Complex combinations and full schema-validation equivalence remain unqualified.

## Mapping details and failure modes

- **Numbers and integers:** the converter installs parsers, maps minimum/maximum, and adds exclusive-bound/multipleOf checks. Empty string/undefined, null, invalid numeric input, and actual numbers follow different branches. The numeric parser can consult the rendered input's validity. Do not infer browser clearing behavior from conversion alone. [K56](sources.md#k56), [K61](sources.md#k61)
- **Strings:** nullable strings can map empty values to null; optional non-nullable strings can map empty strings to undefined. Do not promise uniform numeric/string nullability. The converter passes `pattern` through as a string, which Angular anchors; JSON Schema patterns match substrings. For `{pattern:'foo'}`, `xxfooxx` failed the generated Angular validator. Mapping it to `new RegExp(schema.pattern)` preserved substring matching in the focused probe; avoid stateful `g`/`y` flags. [K56](sources.md#k56), [I3698](bug-ledger.md#i3698), [Angular pattern](https://angular.dev/api/forms/Validators#pattern), [JSON Schema pattern](https://json-schema.org/understanding-json-schema/reference/string#regexp)
- **Object required/dependencies:** child required state can be computed through parent/model context. Schema dependencies can generate hidden groups. Inspect generated expressions instead of assuming a flat required array fully describes runtime validation. [K56](sources.md#k56)
- **Arrays:** min/max items, uniqueItems, tuple versus homogeneous items, optionality, and defaults have separate branches. Tuple entries can receive required/removable props. For uniqueItems, the implementation compares JSON-serialized values with object keys sorted; do not generalize this to arbitrary non-JSON object equality. [K56](sources.md#k56)
- **Enums/const:** recognized alternatives become `enum`, with multiple selection for suitable arrays. Ordinary Material options alone do not enforce membership. The converter uses `includes`/`===`, so a separately allocated `{id:1}` failed enum/const validators despite equal JSON content; the same reference passed. Do not promise structural equality for object/array values. [K56](sources.md#k56), [K57](sources.md#k57)
- **allOf:** resolution merges required lists and takes stricter min/max bounds for listed properties, then reverse-merges. This is an implementation strategy, not proof of general logical-intersection equivalence. [K57](sources.md#k57)
- **oneOf/anyOf:** branch handling depends on type and enum recognition. Non-enum composition on an explicitly typed scalar can be ignored; `type:'string', anyOf:[{pattern:'^A'},{pattern:'^B'}]` accepted `C` in the probe. The typeless fallback calls oneOf mode even for anyOf; object schemas have separate branches. Where multischema is built, it selects initial branches and resets hidden ones; candidate builds suppress the user map callback. Test the actual generated configuration rather than promising logical equivalence. [K56](sources.md#k56), [K57](sources.md#k57)
- **References:** local resolver follows reference chains and preserves a selected annotation subset; remote references are rejected. Do not promise arbitrary sibling-keyword merging, cycle handling, or JSON Pointer escape support without checking the actual schema. [K22](sources.md#k22)

The converter has no dedicated `format` mapping/validation path in the inspected full implementation. Do not assume `format: 'date'` selects the Material datepicker or that `format: 'email'` supplies a validator. Add explicit mapping/validation and test it against the application's schema contract. [K20](sources.md#k20), [K56](sources.md#k56), [K57](sources.md#k57)

R13 executes basic conversion and remote-ref rejection. Numeric input regressions have separate fix boundaries: I3901 and I3937 point to 6.3.4, while array/default cases I3957/I4002 point to later patches. [Bug ledger](bug-ledger.md)

## Focused checks

For a concrete schema, verify conversion, registration, rendering, required/error behavior, nested array changes, defaults, and submitted model shape. Check both valid and invalid inputs. Schema-to-field conversion is not a substitute for any independent server-side validation the application requires. These checks are proposed, not completed in this draft.
