# Official example catalog

All entries refer to the pinned v6.3.12 source commit. These are **source-read walkthroughs**, not compiled or browser-tested recipes. Read the linked component plus its registration/setup where provided. Adapt UI-specific templates deliberately: several official examples use Bootstrap, while this skill's first target is Material.

## E01

**Repeatable section.** [Fields](sources.md#e01a), [module registration](sources.md#e01b), [repeat type](sources.md#e01c).

Shows a registered `repeat` type extending `FieldArrayType`, a `fieldArray` template, and add/remove controls. `repeat` is an example's registered name, not an assumed core built-in. Transfer the model/array mechanism; replace Bootstrap-specific presentation with the consuming Material design. Check insertion, deletion, defaults, validation, and hide/show behavior. See [arrays](arrays.md).

## E02

**Cascaded select.** [Component](sources.md#e02a).

Shows parent `valueChanges`, initial emission, distinct values, filtered child options, and downstream clearing. It is useful for understanding dependencies but should not be copied blindly. Source inspection found the team-option retention check comparing the parent `sportId` to an option's ID; the player section has an analogous comparison. That may fail to express the intended question, “is the currently selected child still available?” This is a source-level concern, not a reproduced runtime defect.

Define the application's retention policy explicitly. Test an existing valid child, an invalid child after the parent changes, cleared parents, and initial edit-mode values. Compare the current child selection with the new child options if retention is intended. Async fetching additionally needs application-specific cancellation, loading, and error handling absent from this small demo.

## E03

**Unique-value async validation.** [Component](sources.md#e03a).

Shows named validators returning a Promise or Observable of a validity boolean. The sample checks an in-memory user list; its timer is not a real server interaction. Transfer the validator contract, not an invented HTTP error policy. Check valid, invalid, pending, dependency changes, and the application's response to failed requests. See [validation](validation.md).

## E04

**Matching two fields.** [Group configuration](sources.md#e04a), [validator registration](sources.md#e04b).

Shows a group validator referenced through `validators.validation`, with `errorPath` targeting `passwordConfirm`. The registered Angular-style function returns null for its valid cases and an error object for mismatch. Both the group placement and registration matter. Check mismatch → match transitions when either sibling changes and confirm where the message appears.

## E05

**JSON Schema rendering setup.** [Module and custom registrations](sources.md#e05a).

Shows the structural renderer registrations needed around schema conversion, including object, array, null, and multischema. This catalog entry covers setup, not a complete audit of every schema in the demo. Read [JSON Schema](json-schema.md) before assuming conversion alone supplies a Material UI. Check representative nested data and branch/required behavior on the exact schemas being used.

## E06

**Material prefix/suffix extension.** [Extension](sources.md#e06a), [configuration module](sources.md#e06b).

Shows an extension conditionally adding an addons wrapper, with a duplicate guard. Use it to understand responsibility and registration. The two indexed files are not the entire component/template bundle; retrieve the referenced wrapper before implementation. Check repeated builds, fields with no addon, and the expected prefix/suffix template behavior.

## E07

**Reset and initial value.** [Component](sources.md#e07a), [template actions](sources.md#e07b).

Shows `options.resetModel()` and `options.updateInitialValue()` as separate actions. Updating the initial value changes what a later reset restores; it is not interchangeable with resetting. Check the sequence used by the application, especially save → continue editing → reset. See [configuration](config-and-model.md).

## E08

**Conditional visibility.** [Component](sources.md#e08a).

Shows an expression controlling visibility from model state. A hiding example does not decide whether an application's hidden data should be retained. Read the effective `resetOnHide` behavior and test the required model/control transitions. See [expressions](expressions-and-lifecycle.md).

## E09

**Type inheritance.** [Fields](sources.md#e09a), [registration and defaults](sources.md#e09b).

Shows a password type extending `input` with defaults and field-level use of that registered name. Reuse this mechanism when the underlying renderer already meets the requirement. Check resulting props, explicit field overrides, wrappers, and validation in the consuming UI adapter.

## E10

**File value accessor.** [Directive](sources.md#e10a).

Shows an accessor bridging a file input's change and blur events to Angular forms. Its `writeValue` is a no-op and the inspected directive does not implement `setDisabledState`. This is an educational fragment, not a production-complete upload control. Check disabled/reset behavior, value shape, surrounding type/template, and the application's upload lifecycle before reuse.

## E11

**Material tabs / staged forms.** [Tab type](sources.md#e11a).

Shows a custom layout type rendering groups as Material tabs and recursively checking validity before enabling later tabs. The example is not a complete wizard contract: decide how pending validation, inactive content, retained drafts, back navigation, and final submission should work. Do not apply default hide-reset behavior to steps when the requirement is preserving entered values.

## E12

**Observable options.** [Component](sources.md#e12a), [service](sources.md#e12b).

Shows options supplied by a service Observable with valueProp/labelProp mapping. The service returns `of` over local data. It does not demonstrate request cancellation, error recovery, stale-response handling, or loading states. Use [async/state](async-and-state.md) for those design decisions.

## E13

**Live translation labels.** [Component](sources.md#e13a).

Shows direct translation-stream expressions for labels and an explicit language-change callback. Transfer the reactive dependency pattern; check the actual translation-library version and missing-key behavior in the consuming application. Validation-message streams are a separate supported path; see [I3601](bug-ledger.md#i3601).

## Selecting further examples

Start from the exact-release official demo tree, then inspect imports, registrations, component/template, services, and associated tests. Record the source revision and whether execution occurred. External projects can reveal useful architecture but must be checked for Formly major, UI adapter, licensing, and maintenance before promotion into this v6 catalog.
