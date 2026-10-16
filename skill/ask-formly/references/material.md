# Angular Material adapter

Baseline: Formly 6.3.12. Angular Material/CDK and the application's date adapter must be checked separately. A Formly peer-dependency range is not a tested compatibility matrix.

## Modules and registered controls

`FormlyMaterialModule` imports the form-field integration and input, textarea, radio, checkbox, multicheckbox, and select modules. It does **not** include every Material entry point. Datepicker and slider have separate modules; do not infer their registration from the umbrella module. [K13](sources.md#k13), [K18](sources.md#k18), [K33](sources.md#k33)

Use the consuming application's v6 module setup, including reactive forms and Formly configuration. Do not introduce a newer-major provider API from an unversioned example. The input module registers `input` and aliases including `string`, `number`, and `integer`; the latter numeric aliases supply input defaults. Custom application names still require registration. [K03](sources.md#k03), [K32](sources.md#k32)

## Select options and identity

The option conversion pipe supports arrays and Observable sources. Labels, values, disabled state, and groups can be mapped with `labelProp`, `valueProp`, `disabledProp`, and `groupProp`; inspect the pipe before inventing an option shape. Its defaults use `label`, `value`, `disabled`, and `group`. [K15](sources.md#k15)

The Material select's default `compareWith` uses strict equality. If the model stores an object and a reload creates new option objects, check identity or provide an appropriate comparator. Confirm whether the model should contain an ID or an object before changing it. The renderer also handles multiple selection and invokes the configured change callback with field and event. [K14](sources.md#k14)

The selected upstream tests include rendering options and selection; they were read, not run. For cascaded selects, test both replacement options and the retained/cleared child value. The official demo has a source-level concern described in [E02](examples.md#e02). [K28](sources.md#k28)

## Datepicker

Use `FormlyMatDatepickerModule` from `@ngx-formly/material/datepicker` when this entry point is needed. It registers the `datepicker` type with the `form-field` wrapper. Inspect the application's compatible date adapter configuration; this Formly module does not itself choose a date adapter implementation. [K18](sources.md#k18)

The inspected renderer uses **`props.datepickerOptions`** for options including `min`, `max`, `filter`, `startView`, `touchUi`, and `startAt`. Do not transpose ordinary numeric input `props.min`/`props.max` to date constraints without checking this contract. Date callbacks include field/event arguments, with additional picker context for month/year selection. Consult the exact declaration and template for a requested option. [K19](sources.md#k19)

Test the actual model value type, parsing, invalid dates, boundaries, disabled state, and reset using the application's chosen adapter. This corpus does not establish timezone or serialization policy for a business application.

## Form-field decoration and custom controls

The wrapper exposes appearance, float label, color, hints, prefix/suffix, and other declared props. Prefix/suffix and text-prefix/text-suffix are template references in the inspected declaration; hints permit text or template references. Do not assume every property accepts raw strings or every native Material input is forwarded by Formly. [K17](sources.md#k17)

Material's `FieldType` implements the form-field control bridge, including focus and error-state coordination. When authoring a custom control, inspect the correct Material base and the application's control/value-accessor wiring. Avoid copying private wrapper/control mutations into ordinary application configuration. [K16](sources.md#k16)

The slider module selects implementations using the CDK major version, with a boundary at 15. This proves that version-specific integration exists; it does not prove every Angular/Material combination works. [K33](sources.md#k33)
