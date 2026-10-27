# JSON Schema objects, arrays, composition and reference limits

Candidate-only source synthesis for Formly 6.3.12; not installed and no execution or conformance score claimed. Pinned upstream commit: 5f099fddea6426b46a453866adf0fede5be0bcd7. All converter and test lines were read. Historical evaluation/probe observations were not used.

## object-required

Object schemas produce keyed child fields for properties. When a child is listed in required or has property dependencies, the converter adds a props.required expression while preserving its existing expressions. That expression consults model and parent required state, walks keyless parents, and returns false when there is no model and the parent is not required; otherwise a listed required property becomes required. [K56](sources.md#k56)

Limit: Nested optional objects therefore do not imply unconditional required descendants. This is generated field behavior, not complete object-keyword validation.

## object-dependencies

Array-valued object dependencies are inverted into dependent-field required expressions that test whether any triggering model value is nonempty; empty means empty string, null or undefined, so false and zero are not empty. Schema dependencies generate extra groups hidden while the trigger is empty. If a schema dependency has oneOf alternatives each defining a const or one-item enum for the trigger property, generated groups omit that trigger property, compare trigger values strictly, and use shareFormControl:false and resetOnHide:true. [K56](sources.md#k56), [K57](sources.md#k57), [K61](sources.md#k61)

Limit: These are specific generated expressions and groups, not proof of general JSON Schema dependency equivalence or structural-equality matching.

## array-defaults-bounds

Array schemas map minItems and maxItems to props and validators that permit empty string, null or undefined and otherwise compare value.length. A positive minItems creates an undefined-filled default array when the array is not optional and has no default; an optional nested array does not receive that allocation. When isOptional is explicitly false and there is a single type, missing defaults become null, empty string, empty object or an array (minItems-sized or empty) for those corresponding types. Homogeneous array items are converted with isOptional:false. [K20](sources.md#k20), [K56](sources.md#k56)

Limit: These are default construction rules and length checks, not a promise that an empty or null array passes the separate type/required validators or that every item is already valid. Explicit schema defaults take precedence.

## array-items-tuples

For a non-enum array the converter creates a fieldArray factory based on the current fieldGroup length. A single items schema supplies homogeneous children and ignores additionalItems; missing items yields an empty child config. Tuple items use the schema at the next index or additionalItems when beyond the tuple. Converted tuple children with props are marked required; positions supplied by the tuple are marked removable:false. Without a truthy selected item schema, the factory yields an empty config. [K56](sources.md#k56)

Limit: The removable flag is configuration for a renderer, not a universal UI enforcement guarantee. additionalItems:false producing no schema is not a converter-added rejection validator. Custom array controls remain responsible for rendering and operations.

## array-unique-items

When uniqueItems is present, the array converter adds a uniqueItems prop and validator. Empty values or a false uniqueItems value pass. Otherwise every item is JSON.stringify-serialized with object keys sorted recursively by a replacer, and the number of distinct serialized strings is compared with the array length. [K56](sources.md#k56), [K61](sources.md#k61)

Limit: This is normalized JSON serialization equality, not arbitrary JavaScript object equality. Unlike enum and const, distinct JSON objects with the same keys and values can be duplicates even when key insertion order differs. No cyclic/non-JSON-value safety guarantee follows.

## allof-merge

resolveAllOf rejects an empty allOf array, resolves each member, concatenates required arrays when both sides have them, propagates truthy uniqueItems, takes smaller maxima (maxLength, maximum, exclusiveMaximum, maxItems, maxProperties) and larger minima (minLength, minimum, exclusiveMinimum, minItems, minProperties) when both values are nonempty, then reverseDeepMerge combines the schemas. [K57](sources.md#k57)

Limit: This is a concrete merge strategy, not general logical-intersection equivalence. A keyword taking part in merging does not establish that the converter creates its validation, and arbitrary conflicting types or complex constraints are not proven equivalent.

## composition-dispatch

Object schemas append separate multischema groups for oneOf and anyOf; oneOf passes shareFormControl:false, while object anyOf uses anyOf mode. Recognized const/singleton-enum alternatives use enum conversion instead. After typed conversion, the fallback multischema handling runs only when field.type is absent: both the oneOf fallback and the anyOf fallback call resolveMultiSchema with oneOf mode and shareFormControl:false. An explicitly typed non-object scalar with non-enum alternatives has no corresponding branch-conversion path. [K56](sources.md#k56), [K57](sources.md#k57), [K21](sources.md#k21)

Limit: A typed string plus arbitrary anyOf patterns is therefore not established as an enforced disjunction by this converter. These dispatch paths do not implement a general JSON Schema logical validator.

## multischema-selection

A generated multischema field contains an enum selector initially set to -1 and branch fields converted with resetOnHide:true. anyOf mode makes the selector multiple. Initialization or forced selection ranks branches by temporary field validity and matched model fields; anyOf then keeps populated branches or falls back to one. Hidden state is derived from the selected index or index array. Candidate-validity builds clone the model, suppress defaults with ignoreDefault:true and suppress the application map with map:null. [K57](sources.md#k57)

Limit: Defaults and custom map logic on displayed fields are not identical to candidate-validity testing. Selecting a different branch can reset hidden values; this selection mechanism does not prove exactly-one or at-least-one logical conformance for all schema combinations.

## local-reference-limits

The local resolver splits a reference at #/ and traverses slash-separated property names directly; it does not decode JSON Pointer ~0 or ~1 escapes. On the direct-definition return path it overlays only title, description, default and widget from the referring schema. If a definition itself has $ref, resolution immediately recurses on that definition, so arbitrary siblings on the outer reference are not merged through the chain. The resolver contains no visited-reference cycle guard. [K22](sources.md#k22), [K57](sources.md#k57)

Limit: Do not confuse source tests of lazily expanded recursive array items with a guarantee that direct $ref cycles terminate safely. Remote rejection and missing-definition errors are covered separately.

