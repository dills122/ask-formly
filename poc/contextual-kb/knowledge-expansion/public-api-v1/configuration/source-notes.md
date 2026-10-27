# Configuration admission source notes

Pinned Formly 6.3.12, commit 5f099fddea6426b46a453866adf0fede5be0bcd7. Draft candidate only.

## wrapper-nesting-order

For field.wrappers [A, B], Formly creates A first, renders the remaining wrappers inside A.fieldComponent, and renders the field type after the wrappers are exhausted. A is the outer wrapper and B is the inner wrapper. [K41](sources.md#k41)

## defaults-order-before-wrapper-fallback

getMergedField reverse-merges registered type defaultOptions first, then the directly extended type defaultOptions, then optionsTypes defaults in array order, and then resolved component-instance defaultOptions. Registered type wrappers are copied only after those merges and only if field.wrappers is falsy. Thus a wrappers array already supplied by the field or a preceding default, including [], prevents that final fallback. [K150](sources.md#k150) [K151](sources.md#k151)

## duplicate-type-registration

For repeated type registrations with the same name, setType retains the existing registry object and assigns only own component, extends, defaultOptions and wrappers properties present on the later registration. Omitted properties survive; supplied properties replace their previous values, including a whole defaultOptions object or wrappers array. getType then fills falsy component and wrappers from the extended type before returning the effective entry. [K150](sources.md#k150) [K152](sources.md#k152)

## duplicate-wrapper-registration

setWrapper replaces the entire named wrapper registry entry, so getWrapper(name) returns the most recently registered wrapper object. Each supplied types association adds the wrapper name to that type only if absent. Re-registering a wrapper with a different types list does not remove its earlier type associations; looking up an unknown string wrapper name throws. [K150](sources.md#k150)

## duplicate-validator-registration

setValidator replaces the entire registry entry for a validator name; getValidator(name) returns the last registered object, without merging properties from its predecessor. Looking up an unknown validator name throws. [K150](sources.md#k150)

## preset-partial-overrides

When a field type is #name and the named preset exists, preset prePopulate removes the pseudo-type from a copy of the field properties, reverse-merges the preset configuration into that copy, and assigns the result back to the field. Existing nonblank field values override preset defaults; compatible nested objects merge by filling missing values, so overriding props.label can retain other preset props. Null, undefined and empty-string destinations receive defaults; false, zero and existing arrays, including empty arrays, survive. Arrays are not concatenated or merged by index. [K44](sources.md#k44) [K151](sources.md#k151) [K153](sources.md#k153)

