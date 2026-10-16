# Material control contracts and integration checks

Scope: inspected Formly 6.3.12 renderers. Angular Material 21.2.14 with Angular 21.2.25 was used for selected [runtime probes](runtime-evidence.md) and [AOT/browser qualification](angular21-qualification.md); this is not a compatibility matrix.

## Common and secondary entry points

| Type | Important contract | Evidence |
| --- | --- | --- |
| input | HTML input kind comes from `props.type`; number has a dedicated template branch. Forwards readonly, required, error matcher, control, attributes, name, placeholder | [K47](sources.md#k47) |
| textarea | Adds rows/cols and autosize/min/max rows; readonly is explicitly bound. Default rows and cols are 1 | [K51](sources.md#k51) |
| select | Options stream, mappings, groups, multiple, compareWith, panelClass, select-all. No readonly input is bound in this renderer | [K14](sources.md#k14), [K15](sources.md#k15) |
| checkbox | Boolean-oriented control; indeterminate display depends on a nullish control value and enabled indeterminate prop. Its own label and required marker interact with wrapper defaults | [K48](sources.md#k48), [K62](sources.md#k62) |
| multicheckbox | Default path produces a Boolean map keyed by option values; `props.type: 'array'` produces selected-value arrays. Choice affects the payload contract | [K49](sources.md#k49), R15 |
| radio | Options use the shared mapping pipe; each option can be disabled. Group focus/keyboard handling differs from an input | [K50](sources.md#k50) |
| toggle | Separate `@ngx-formly/material/toggle` entry point. Binds required, labelPosition, color, control and attributes; own label with wrapper label hidden by default | [K52](sources.md#k52) |
| datepicker | Separate entry point; adapter choice and nested `datepickerOptions` matter | [Material](material.md), [K18](sources.md#k18), [K19](sources.md#k19) |
| slider | Separate entry point with legacy/MDC implementation selection. The MDC variant places the control on `input matSliderThumb` | [K33](sources.md#k33), [K53](sources.md#k53), [K54](sources.md#k54) |
| native-select | Separate entry point; native option values use ngValue and support optgroups. A source readonly binding alone does not establish a functional browser readonly interaction contract | [K55](sources.md#k55) |

The umbrella module's common imports are recorded in [K13](sources.md#k13). Additional registration names/aliases must be checked in the matching module. Do not substitute a raw Material component's API for the Formly adapter's forwarded props.

## Select details

`compareWith` defaults to strict equality. `labelProp`/`valueProp` define mapping, while comparison determines selected-option identity; these are distinct responsibilities. Native-select and mat-select are not interchangeable adapters with identical props. [K14](sources.md#k14), [K15](sources.md#k15), [K55](sources.md#k55)

Select-all flattens groups, excludes disabled options, and caches its value list by the options-array reference. Its state calculation compares lengths. For unusual dynamic/partial/stale selections, test behavior rather than assuming semantic set equality or expecting in-place option mutations to invalidate every cache. Replacing the options array is a useful explicit update boundary. [K14](sources.md#k14)

The select reads aria-label and aria-labelledby from props.attributes, with a wrapper-label fallback. Check accessible names when labels are visually hidden. Overlay presentation uses the forwarded panelClass; a field host class is not automatically the overlay panel class. [K14](sources.md#k14)

## Custom Material controls

For typed registration, use the [public ConfigOption-derived type](customization.md#types-and-registration); v6.3.12 does not publicly export TypeOption.

There are three separate contracts:

1. **Angular value access:** how programmatic values, user values, touched, and disabled state reach the form control.
2. **Formly type integration:** the field's control, props, hooks, registration and attributes.
3. **Material form-field integration:** error/focus/empty/label behavior and a suitable MatFormFieldControl.

Passing one does not establish the others. Formly's Material `FieldType` is publicly re-exported from `@ngx-formly/material` and bridges the form-field control. In I3512 the maintainer specifically points to this base rather than the core base. Use it for the matching design, while still supplying proper control/value-accessor behavior. R09 exercises a simple matInput custom type; it does not certify composite widgets. [K16](sources.md#k16), [K63](sources.md#k63), [I3512](bug-ledger.md#i3512)

If a widget already owns its own mat-form-field or is a standalone button/layout, decide whether a Formly form-field wrapper is appropriate. Avoid double decoration. A composite value should be modeled either as a grouped set of child fields or as an intentional single control with a coherent value accessor; do not silently mix both ownership models. [K31](sources.md#k31), [I3572](bug-ledger.md#i3572)

## Required markers, validation, and read-only presentation

Required state is behavior as well as decoration. A future-required asterisk with currently optional validation is a custom presentation rule; maintainers recommend a custom wrapper/type for that requirement. Do not invent a built-in `showAsterisk` prop from the issue's proposal. [I3855](bug-ledger.md#i3855), [K17](sources.md#k17)

For affirmative consent, explicitly validate true. For read-only review screens, distinguish an input's readonly binding from controls such as select that lack it. Disabled affects control validity/value aggregation; the retained Formly model is a separate payload source. [K47](sources.md#k47), [K14](sources.md#k14), R04/R12

## Appearance, dates, and upgrades

The Material 15 checkbox styling discussion contains user CSS workarounds and a report about a custom base-class error. Neither proves that all Material >15 is unsupported or that copying private MDC selectors is the best fix. Check effective wrapper defaults, theme, and target Material version first. [I3558](bug-ledger.md#i3558)

A datepicker must be checked with the selected adapter's actual values, locale, parsing, and serialization policy. A date-looking JSON string does not become a compatible Date value merely by naming the type. Test min/max/filter, invalid input, reset, and time-related payload requirements; R01–R17 did not test datepicker; [browser qualification](angular21-qualification.md) covers selected native en-US date behavior, not all adapters/time zones. [K19](sources.md#k19)

For SSR/hydration, I3824 is a specific textarea fix released in 6.3.0. The current template avoids the reported inter-tag whitespace. This is not proof that all custom templates, all controls, or all hydration configurations are supported. [K51](sources.md#k51), [I3824](bug-ledger.md#i3824)
