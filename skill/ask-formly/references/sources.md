# Pinned evidence index

Baseline: ngx-formly v6.3.12, commit `5f099fddea6426b46a453866adf0fede5be0bcd7`. Accessed 2026-10-15.

Every entry below was read as source. `test-source` means an upstream test was inspected, not executed. This index supports the accompanying notes; it is not a claim that entire upstream files or APIs were audited. Full-file hashes and excerpt bounds are in [evidence.json](evidence.json).

Use the exact installed version when it differs. Examples are learning material, not automatically qualified application recipes.

## K01

Field configuration and options API — api.

[src/core/src/lib/models/fieldconfig.ts:1–287](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/models/fieldconfig.ts#L1-L287)

## K02

Public core exports — api.

[src/core/src/lib/core.ts:1–26](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/core.ts#L1-L26)

## K03

NgModule setup and default extensions — implementation.

[src/core/src/lib/core.module.ts:19–78](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/core.module.ts#L19-L78)

## K04

Registry defaults and type merging — implementation.

[src/core/src/lib/services/formly.config.ts:28–151](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/services/formly.config.ts#L28-L151)

## K05

Model scope, defaults, aliases and reset — implementation.

[src/core/src/lib/extensions/core/core.ts:21–168](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/extensions/core/core.ts#L21-L168)

## K06

Builder lifecycle — implementation.

[src/core/src/lib/services/formly.builder.ts:15–106](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/services/formly.builder.ts#L15-L106)

## K07

Expression evaluation and hiding — implementation.

[src/core/src/lib/extensions/field-expression/field-expression.ts:20–302](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/extensions/field-expression/field-expression.ts#L20-L302)

## K08

Validator adapters and error paths — implementation.

[src/core/src/lib/extensions/field-validation/field-validation.ts:9–168](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/extensions/field-validation/field-validation.ts#L9-L168)

## K09

Form control creation and reuse — implementation.

[src/core/src/lib/extensions/field-form/field-form.ts:14–103](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/extensions/field-form/field-form.ts#L14-L103)

## K10

Field hook subscription lifecycle — implementation.

[src/core/src/lib/components/formly.field.ts:83–177](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/components/formly.field.ts#L83-L177)

## K11

Form changes, formState and modelChange — implementation.

[src/core/src/lib/components/formly.form.ts:30–165](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/components/formly.form.ts#L30-L165)

## K12

Array operations — implementation.

[src/core/src/lib/templates/field-array.type.ts:14–102](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/templates/field-array.type.ts#L14-L102)

## K13

Material aggregate module — implementation.

[src/ui/material/src/lib/ui-material.module.ts:1–22](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/ui/material/src/lib/ui-material.module.ts#L1-L22)

## K14

Material select binding and equality — implementation.

[src/ui/material/select/src/select.type.ts:8–130](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/ui/material/select/src/select.type.ts#L8-L130)

## K15

Select option mapping — implementation.

[src/core/select/src/select-options.pipe.ts:6–137](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/select/src/select-options.pipe.ts#L6-L137)

## K16

Material FieldType integration — implementation.

[src/ui/material/form-field/src/field.type.ts:1–143](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/ui/material/form-field/src/field.type.ts#L1-L143)

## K17

Material form-field wrapper properties — implementation.

[src/ui/material/form-field/src/form-field.wrapper.ts:27–105](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/ui/material/form-field/src/form-field.wrapper.ts#L27-L105)

## K18

Datepicker registration — implementation.

[src/ui/material/datepicker/src/datepicker.module.ts:1–32](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/ui/material/datepicker/src/datepicker.module.ts#L1-L32)

## K19

Datepicker props and bindings — implementation.

[src/ui/material/datepicker/src/datepicker.type.ts:16–109](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/ui/material/datepicker/src/datepicker.type.ts#L16-L109)

## K20

JSON Schema mapping API and defaults — implementation.

[src/core/json-schema/src/formly-json-schema.service.ts:94–202](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/json-schema/src/formly-json-schema.service.ts#L94-L202)

## K21

JSON Schema customization order — implementation.

[src/core/json-schema/src/formly-json-schema.service.ts:508–565](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/json-schema/src/formly-json-schema.service.ts#L508-L565)

## K22

JSON Schema reference resolution — implementation.

[src/core/json-schema/src/formly-json-schema.service.ts:632–662](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/json-schema/src/formly-json-schema.service.ts#L632-L662)

## K23

Preset setup and usage — documentation.

[docs/formly-field-presets.md:1–67](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/docs/formly-field-presets.md#L1-L67)

## K24

Extension guidance and priorities — documentation.

[docs/custom-formly-extension.md:1–124](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/docs/custom-formly-extension.md#L1-L124)

## K25

Expression callback and observable tests — test-source.

[src/core/src/lib/extensions/field-expression/field-expression.spec.ts:217–270](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/extensions/field-expression/field-expression.spec.ts#L217-L270)

## K26

Validator contract tests — test-source.

[src/core/src/lib/extensions/field-validation/field-validation.spec.ts:117–198](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/extensions/field-validation/field-validation.spec.ts#L117-L198)

## K27

Array default/hide tests — test-source.

[src/core/src/lib/templates/field-array.type.spec.ts:500–584](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/templates/field-array.type.spec.ts#L500-L584)

## K28

Material select rendering and values tests — test-source.

[src/ui/material/select/src/select.type.spec.ts:15–104](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/ui/material/select/src/select.type.spec.ts#L15-L104)

## K29

Late v6 patch history — documentation.

[CHANGELOG.md:1–230](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/CHANGELOG.md#L1-L230)

## K30

Core field type and strict control types — api.

[src/core/src/lib/templates/field.type.ts:1–69](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/templates/field.type.ts#L1-L69)

## K31

Wrapper insertion point — api.

[src/core/src/lib/templates/field.wrapper.ts:1–13](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/templates/field.wrapper.ts#L1-L13)

## K32

Material input registrations — implementation.

[src/ui/material/input/src/input.module.ts:1–49](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/ui/material/input/src/input.module.ts#L1-L49)

## K33

Slider implementation selection — implementation.

[src/ui/material/slider/src/slider.module.ts:1–36](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/ui/material/slider/src/slider.module.ts#L1-L36)

## K34

JSON Schema fixture setup and type tests — test-source.

[src/core/json-schema/src/formly-json-schema.service.spec.ts:1–93](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/json-schema/src/formly-json-schema.service.spec.ts#L1-L93)

## K35

Extension priority sorting — implementation.

[src/core/src/lib/services/formly.config.ts:246–267](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/services/formly.config.ts#L246-L267)

## E01a

Repeating fields — example-source.

[demo/src/app/examples/advanced/repeating-section/app.component.ts:1–37](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/demo/src/app/examples/advanced/repeating-section/app.component.ts#L1-L37)

## E01b

Repeating fields — example-source.

[demo/src/app/examples/advanced/repeating-section/app.module.ts:1–22](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/demo/src/app/examples/advanced/repeating-section/app.module.ts#L1-L22)

## E01c

Repeating fields — example-source.

[demo/src/app/examples/advanced/repeating-section/repeat-section.type.ts:1–23](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/demo/src/app/examples/advanced/repeating-section/repeat-section.type.ts#L1-L23)

## E02a

Cascaded selects: adaptation caveat — example-source.

[demo/src/app/examples/other/cascaded-select/app.component.ts:1–112](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/demo/src/app/examples/other/cascaded-select/app.component.ts#L1-L112)

## E03a

Promise and Observable validation — example-source.

[demo/src/app/examples/validation/unique-value-async-validation/app.component.ts:1–63](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/demo/src/app/examples/validation/unique-value-async-validation/app.component.ts#L1-L63)

## E04a

Cross-field validation — example-source.

[demo/src/app/examples/validation/matching-two-fields/app.component.ts:1–50](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/demo/src/app/examples/validation/matching-two-fields/app.component.ts#L1-L50)

## E04b

Cross-field validation — example-source.

[demo/src/app/examples/validation/matching-two-fields/app.module.ts:1–42](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/demo/src/app/examples/validation/matching-two-fields/app.module.ts#L1-L42)

## E05a

JSON Schema registrations — example-source.

[demo/src/app/examples/advanced/json-schema/app.module.ts:1–92](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/demo/src/app/examples/advanced/json-schema/app.module.ts#L1-L92)

## E06a

Material addon extension — example-source.

[demo/src/app/examples/other/material-prefix-suffix/addons.extension.ts:1–11](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/demo/src/app/examples/other/material-prefix-suffix/addons.extension.ts#L1-L11)

## E06b

Material addon extension — example-source.

[demo/src/app/examples/other/material-prefix-suffix/config.module.ts:1–57](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/demo/src/app/examples/other/material-prefix-suffix/config.module.ts#L1-L57)

## E07a

Reset and initial values — example-source.

[demo/src/app/examples/form-options/reset-model/app.component.ts:1–41](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/demo/src/app/examples/form-options/reset-model/app.component.ts#L1-L41)

## E07b

Reset and initial values — example-source.

[demo/src/app/examples/form-options/reset-model/app.component.html:1–6](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/demo/src/app/examples/form-options/reset-model/app.component.html#L1-L6)

## E08a

Conditional visibility — example-source.

[demo/src/app/examples/field-options/hide-fields/app.component.ts:1–38](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/demo/src/app/examples/field-options/hide-fields/app.component.ts#L1-L38)

## E09a

Extending input defaults — example-source.

[demo/src/app/examples/advanced/extending-field-types/app.component.ts:1–39](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/demo/src/app/examples/advanced/extending-field-types/app.component.ts#L1-L39)

## E09b

Extending input defaults — example-source.

[demo/src/app/examples/advanced/extending-field-types/app.module.ts:1–33](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/demo/src/app/examples/advanced/extending-field-types/app.module.ts#L1-L33)

## E10a

File value accessor boundaries — example-source.

[demo/src/app/examples/other/input-file/file-value-accessor.ts:1–26](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/demo/src/app/examples/other/input-file/file-value-accessor.ts#L1-L26)

## K36

Global configuration and extension contracts — api.

[src/core/src/lib/models/config.ts:1–105](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/models/config.ts#L1-L105)

## K37

DOM attributes, focus and event bridge — implementation.

[src/core/src/lib/templates/formly.attributes.ts:25–221](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/templates/formly.attributes.ts#L25-L221)

## K38

Message precedence and observable rendering — implementation.

[src/core/src/lib/templates/formly.validation-message.ts:17–83](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/templates/formly.validation-message.ts#L17-L83)

## K39

Key paths, model assignment and default merging — implementation.

[src/core/src/lib/utils.ts:14–116](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/utils.ts#L14-L116)

## K40

Clone boundaries and deep observation — implementation.

[src/core/src/lib/utils.ts:153–262](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/utils.ts#L153-L262)

## K41

Rendering lifecycle, expression subscriptions, parsers and debounce — implementation.

[src/core/src/lib/components/formly.field.ts:120–377](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/components/formly.field.ts#L120-L377)

## K42

Control registration, disabled synchronization and validity updates — implementation.

[src/core/src/lib/extensions/field-form/utils.ts:1–123](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/extensions/field-form/utils.ts#L1-L123)

## K43

Validator composition and shared controls — implementation.

[src/core/src/lib/extensions/field-form/field-form.ts:90–169](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/extensions/field-form/field-form.ts#L90-L169)

## K44

Preset replacement and priority — implementation.

[src/core/preset/src/preset-substitution.extension.ts:1–33](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/preset/src/preset-substitution.extension.ts#L1-L33)

## K45

Public testing component factories — implementation.

[src/core/testing/src/component-factory.ts:1–118](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/testing/src/component-factory.ts#L1-L118)

## K46

FAQ for templates, select pipe, standalone integration — guide.

[docs/faq.md:1–124](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/docs/faq.md#L1-L124)

## K47

Material input contract — implementation.

[src/ui/material/input/src/input.type.ts:1–50](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/ui/material/input/src/input.type.ts#L1-L50)

## K48

Material checkbox contract — implementation.

[src/ui/material/checkbox/src/checkbox.type.ts:1–106](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/ui/material/checkbox/src/checkbox.type.ts#L1-L106)

## K49

Material multicheckbox value shapes — implementation.

[src/ui/material/multicheckbox/src/multicheckbox.type.ts:1–70](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/ui/material/multicheckbox/src/multicheckbox.type.ts#L1-L70)

## K50

Material radio contract and focus — implementation.

[src/ui/material/radio/src/radio.type.ts:1–68](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/ui/material/radio/src/radio.type.ts#L1-L68)

## K51

Material textarea and autosize — implementation.

[src/ui/material/textarea/src/textarea.type.ts:1–52](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/ui/material/textarea/src/textarea.type.ts#L1-L52)

## K52

Material toggle contract — implementation.

[src/ui/material/toggle/src/toggle.type.ts:1–46](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/ui/material/toggle/src/toggle.type.ts#L1-L46)

## K53

Material legacy slider contract — implementation.

[src/ui/material/slider/src/slider.type.ts:1–66](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/ui/material/slider/src/slider.type.ts#L1-L66)

## K54

Material MDC slider integration — implementation.

[src/ui/material/slider/src/slider-mdc.type.ts:1–62](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/ui/material/slider/src/slider-mdc.type.ts#L1-L62)

## K55

Material native select contract — implementation.

[src/ui/material/native-select/src/native-select.type.ts:1–44](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/ui/material/native-select/src/native-select.type.ts#L1-L44)

## K56

JSON Schema parsers, dependencies, arrays and enums — implementation.

[src/core/json-schema/src/formly-json-schema.service.ts:203–510](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/json-schema/src/formly-json-schema.service.ts#L203-L510)

## K57

JSON Schema composition, selection and references — implementation.

[src/core/json-schema/src/formly-json-schema.service.ts:531–801](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/json-schema/src/formly-json-schema.service.ts#L531-L801)

## K58

Public testing exports — api.

[src/core/testing/src/public_api.ts:1–1](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/testing/src/public_api.ts#L1-L1)

## K59

Template rendering and safeHtml behavior — implementation.

[src/core/src/lib/templates/field-template.type.ts:1–29](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/templates/field-template.type.ts#L1-L29)

## K60

String expression evaluator — implementation.

[src/core/src/lib/extensions/field-expression/utils.ts:1–15](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/extensions/field-expression/utils.ts#L1-L15)

## K61

JSON Schema number conversion helpers — implementation.

[src/core/json-schema/src/formly-json-schema.service.ts:1–94](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/json-schema/src/formly-json-schema.service.ts#L1-L94)

## K62

Material checkbox registration — implementation.

[src/ui/material/checkbox/src/checkbox.module.ts:1–35](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/ui/material/checkbox/src/checkbox.module.ts#L1-L35)

## K63

Material public base-class export — api.

[src/ui/material/src/lib/ui-material.ts:1–3](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/ui/material/src/lib/ui-material.ts#L1-L3)

## E11a

Material tabs example — example.

[demo/src/app/examples/advanced/tabs/tabs.type.ts:1–28](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/demo/src/app/examples/advanced/tabs/tabs.type.ts#L1-L28)

## E12a

Observable options example — example.

[demo/src/app/examples/other/observable-select/app.component.ts:1–33](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/demo/src/app/examples/other/observable-select/app.component.ts#L1-L33)

## E12b

Observable options service — example.

[demo/src/app/examples/other/observable-select/data.service.ts:1–14](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/demo/src/app/examples/other/observable-select/data.service.ts#L1-L14)

## E13a

Reactive translation labels — example.

[demo/src/app/examples/advanced/i18n/app.component.ts:1–53](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/demo/src/app/examples/advanced/i18n/app.component.ts#L1-L53)

## K64

Zoneless detection, field marking, and Angular version predicate — implementation.

[src/core/src/lib/utils.ts:354–387](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/utils.ts#L354-L387)
