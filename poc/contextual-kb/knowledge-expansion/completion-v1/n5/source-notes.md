# Remaining validation, messages and reactive labels

Pinned Formly 6.3.12 source inspection only. No upstream tests, browser probes or sealed evaluations executed. Existing full source evidence counts toward baseline support.

## message-precedence

FormlyValidationMessage selects the first own error encountered in the control errors object and returns one message. It starts with the global message for that error, then truthy overrides apply in order: the error object message, field.validation.messages, the named sync validator message, and the named async validator message. A selected function is called with the error value and field. [K38](sources.md#k38)

## routed-message-suppression

When the selected error value is an object with a truthy errorPath, FormlyValidationMessage returns undefined before evaluating message overrides. It does not continue to another error in that call. The validation extension can route an error to a child control and strips the returned error payload errorPath from the child payload. [K38](sources.md#k38) [K08](sources.md#k08)

## observable-message

FormlyValidationMessage recomputes the selected message initially, on control statusChanges and on matching field expressionChanges events for validation properties or its predefined templateOptions validator paths. It uses switchMap to consume a selected Observable message, otherwise wraps the result with of; its template renders through async. A message function can therefore return an Observable of strings. [K38](sources.md#k38)

## routed-error-cleanup

The validation extension runs a previous child-error cleanup callback using the configured validator name before handling its next result. Routed errors and cleanup callbacks are stored under each returned error key. An anonymous validators.validation function has no configured name; a returned key such as match therefore need not match the cleanup lookup. A named match expression or registered validator returning the same match key aligns lookup and storage. [K08](sources.md#k08)

## group-async-placement

Formly initializes validators and asyncValidators separately. An Angular-style async group rule belongs in asyncValidators.validation, while a named async expression belongs under asyncValidators with its boolean-validity contract. The form extension composes _asyncValidators with Validators.composeAsync and attaches them through setAsyncValidators when the control has no existing asyncValidator. The official matching-fields example demonstrates group placement and an application-defined fieldMatch registration, but that example is synchronous. [K08](sources.md#k08) [K43](sources.md#k43) [E04a](sources.md#e04a) [E04b](sources.md#e04b)

## translation-stream-example

The official i18n example assigns translate.stream results directly to expressions['props.label'] and changes the selected language through a props.change callback. This instantiates the core direct-Observable expression mechanism; it does not wrap the stream in an ordinary expression callback. [E13a](sources.md#e13a) [K07](sources.md#k07)

## affirmative-consent-boundary

Formly's predefined required prop delegates to Validators.required, not Validators.requiredTrue. For an explicit must-be-true rule, a named Formly expression such as control => control.value === true supplies true for valid and false for invalid, rejecting false, null and undefined by that expression. A required marker or generic required setting alone does not establish this explicit application consent predicate. [K08](sources.md#k08)

