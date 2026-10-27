# JSON Schema scalar, parser, enum and format boundaries

Candidate-only source synthesis for Formly 6.3.12; not installed and no execution or conformance score claimed. Pinned upstream commit: 5f099fddea6426b46a453866adf0fede5be0bcd7. All converter and test lines were read. Historical evaluation/probe observations were not used.

## numeric-parser

For JSON Schema number and integer fields, the converter installs a parser using toNumber: empty string or undefined becomes undefined, null is initially retained, numbers are retained, and other values use parseFloat with an unparseable value retained. When the result is null and a field is supplied, an existing input selected by field.id whose validity.badInput is false changes the result to undefined; a differing control value is written with emitModelToViewChange:false. [K61](sources.md#k61), [K56](sources.md#k56)

Limit: This is converter and control-update logic, not a guarantee of how every browser, value accessor or custom renderer emits an empty or invalid number. The parser does not round to an integer.

## numeric-constraints

For number and integer schemas, minimum and maximum map to props.min and props.max. exclusiveMinimum and exclusiveMaximum map to props and strict greater-than/less-than validators that accept empty values. multipleOf maps to props.step and a validator using a decimal-place multiplier and rounded integer remainder; that validator accepts empty values, non-number values, zero, and nonpositive divisors without rejecting them itself. [K56](sources.md#k56), [K61](sources.md#k61)

Limit: Type and required validation remain separate. This algorithm is not a guarantee of arbitrary-precision decimal arithmetic or a general schema-validity check.

## type-nullability

The converter records guessed types in its type validator, permits undefined, and permits null when null is listed. For the first guessed type it checks string, integer, number, object or array using the corresponding runtime test; integer uses Number.isInteger or a floor-based fallback. A two-type list containing null is reordered to put the non-null type first. Other type lists are not implemented as a general union validator: after the null allowance the switch checks only the first type. [K20](sources.md#k20), [K57](sources.md#k57), [K61](sources.md#k61)

Limit: An integer alias in a Material module alone is different from this JSON Schema integer validator. Undefined passing the type validator does not imply that required validation passes.

## string-empty-length

For string schemas, minLength, maxLength and pattern are copied to props. The string parser maps empty string, null and undefined to null when null is among the guessed types. Otherwise, with a supplied field whose props.required is false or unset, it maps only empty string to undefined; a required non-nullable string retains empty string. [K56](sources.md#k56), [K61](sources.md#k61)

Limit: The nullable branch precedes the required check; numeric empty/null normalization follows different code. These mappings do not prove server payload policy.

## pattern-handoff

The converter copies a JSON Schema string pattern directly to props.pattern; Formly predefined validation passes that value to Angular Validators.pattern. The converter does not compile a RegExp or add a separate JSON Schema substring-matching validator. Angular documents anchoring string patterns with missing ^ and $; this differs from JSON Schema pattern substring matching. A map callback can supply a RegExp for the intended substring semantics. [K56](sources.md#k56), [K08](sources.md#k08), [K21](sources.md#k21)

Limit: The anchoring distinction is based on the linked Angular and JSON Schema documentation, not execution of a browser probe in this package. Avoid global/sticky RegExp flags because Angular documents stateful repeated validation. Verify any custom renderer behavior separately.

## enum-options-membership

The converter recognizes schema.enum, oneOf or anyOf whose alternatives are const or one-item enum definitions, and uniqueItems arrays with a non-tuple enum item schema. It changes the field type to enum, creates options and sets multiple for an original array type. Plain enum values are also labels; const/one-item alternatives use title or value and set disabled for readOnly alternatives. The enum validator accepts undefined; multiple selection requires an array and checks each member with includes, while single selection uses includes directly. [K56](sources.md#k56), [K57](sources.md#k57), [K20](sources.md#k20), [K61](sources.md#k61)

Limit: Object and array values therefore require the same references as generated enum option values, not merely structurally equal JSON. Conversion clones the supplied schema, so original input-schema object identity must not be assumed. These are converter validators, not membership guarantees from ordinary Material options alone.

## const-identity

For a schema with its own const property, the converter sets props.const and adds a validator using value === schema.const. When no field type has been inferred it also sets defaultValue to that const; an explicitly typed const field does not receive that special default assignment. [K56](sources.md#k56), [K20](sources.md#k20)

Limit: Structural equality of separately allocated objects or arrays is not enough. The schema is cloned before conversion, so the comparison is against the converted schema value.

## format-boundary

The full inspected FormlyJsonschema implementation has no dedicated format mapping or format validator. A string schema with format date or email does not by that keyword alone select a Material datepicker or install an email validator; explicit application mapping and validation are separate responsibilities. [K20](sources.md#k20), [K56](sources.md#k56), [K57](sources.md#k57), [K21](sources.md#k21)

Limit: This is a scoped absence in the pinned 6.3.12 converter, not a claim about every release, extension or consuming application. It does not certify full JSON Schema conformance.

## External contract context for pattern-handoff

The Formly call chain is pinned above. [Angular Validators.pattern](https://angular.dev/api/forms/Validators#pattern) documents string anchoring and stateful g/y flags; [JSON Schema string patterns](https://json-schema.org/understanding-json-schema/reference/string#regexp) document substring matching. These pages were read on 2026-10-26 as supplemental contract documentation, not as evidence for other Formly releases, Angular compatibility, or an executed browser result.
