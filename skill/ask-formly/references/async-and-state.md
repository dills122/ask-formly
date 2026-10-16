# Async data, dependencies, and state ownership

Baseline: 6.3.12. Recommendations below combine inspected code and explicitly attributed conversations. Networking recipes are design guidance unless a runtime result is named.

## Expressions: a stream is not a function returning a stream

The evaluator recognizes an Observable supplied as the expression value. It does not flatten an Observable returned by an ordinary expression callback. Use `expressions: { 'props.disabled': disabled$ }`, or construct the config in a factory that can select the right stream. Do not use `() => disabled$` and expect equivalent behavior. [K07](sources.md#k07), [I3541](bug-ledger.md#i3541); direct-stream behavior is checked in R06.

A closure over an external component property is not automatically a reactive dependency. V6 defaults to expression checks on model changes. For changing external state, a direct Observable is explicit; formState is also observed in the 6.3.12 host, with an important 6.3.11 fix boundary. A blanket change to `checkExpressionOn: 'changeDetectionCheck'` can increase work and should be a deliberate compatibility choice. [I3820](bug-ledger.md#i3820), [I4018](bug-ledger.md#i4018), [K11](sources.md#k11)

## Dependent remote selects

Establish these policies before assembling operators:

1. **Dependency:** read the actual sibling/ancestor control in the correct model scope. Include the initial edit-mode value; a valueChanges subscription alone may miss it.
2. **Request lifetime:** newer parent selection should supersede stale results where appropriate. `switchMap` is a suitable pattern for that behavior; avoid unmanaged nested subscriptions.
3. **Invalidation:** decide whether an unavailable child is cleared, marked invalid, or retained as an historical object. Formly does not choose this business policy for you. [I3131](bug-ledger.md#i3131)
4. **Empty parent:** emit the empty options state and apply the clearing policy. Filtering null parent values out can leave old options and selections visible.
5. **Failure:** distinguish request failure from a successful empty result. Blindly converting every error to `[]` can erase a legitimate edit-mode selection.
6. **Ownership:** identify who subscribes. An options stream consumed by a hidden, lazily unrendered select may have no active UI subscriber. Critical state transitions should not depend solely on that renderer subscribing. [I3808](bug-ledger.md#i3808), [K41](sources.md#k41)

Use `options.fieldChanges` when the dependency is an expression/visibility transition, filtering event type, field, and property. Guard against feedback loops if the handler changes another expression dependency. A form's control-value stream does not describe every visibility transition. [K07](sources.md#k07), [I3808](bug-ledger.md#i3808)

Do not clear the existing child eagerly during the first loading emission unless that is the desired edit-mode policy. Test A → B parent changes with responses arriving B → A, initial valid child data, parent clearing, errors, hide/show, and repeated subscriptions. The official small Observable-options demo uses `of(...)`, so it establishes the binding shape rather than HTTP race handling. [E12](examples.md#e12)

## Debounced lookups and immediate invalidation

Keep Formly normalization separate from request timing. In 6.3.12, a positive `modelOptions.debounce.default` can bypass parsers; see [API contracts](api-contracts.md). Consume a normalized `(modelChange)`/application-model boundary, or explicitly normalize the chosen input stream. A raw control emission is not proof that the root model has already been updated. If preserving typed casing matters, keep a draft representation: an ordinary uppercase parser can update both control and visible text.

Define when a response becomes stale. `debounceTime(250), switchMap(lookup)` cancels the old inner subscription only when the next **debounced** value reaches `switchMap`. It can still deliver the old response during that 250 ms window. If every new normalized query must invalidate prior work immediately, use an outer `switchMap` that owns both the delay and request. The following is a composition sketch, not a complete Angular component:

```ts
normalizedQueries$.pipe(
  distinctUntilChanged(),
  switchMap(query => query === ''
    ? of({ kind: 'idle' })
    : concat(
        of({ kind: 'waiting', query }), // supersede previously displayed results
        timer(250).pipe(
          switchMap(() => lookup(query)),
          map(value => ({ kind: 'ready', query, value })),
          catchError(error => of({ kind: 'error', query, error })),
        ),
      )),
  takeUntil(destroy$), // owner emits on destroy; completing destroy$ alone is insufficient
);
```

Keep one owner subscription or an async-pipe consumer, and use a signal/Angular notification for application-owned results in zoneless mode. With `takeUntilDestroyed`, pass the owner's `DestroyRef` where injection context is unavailable. Do not place cleanup only before the outer `switchMap`, because completion of the outer source can leave its active inner subscription running. Case-only edits may deliberately deduplicate after normalization. Feed load/reset through the same model boundary; choose whether they should perform a lookup. Cancellation prevents delivery to this subscription, not already executed server work or side effects outside it.

The stale-window, immediate-supersession and teardown behaviors were checked with RxJS 7.8.1 virtual time, independently of Angular/HTTP. No network cancellation or complete application recipe is certified. Source: [RxJS switchMap 7.8.1](https://github.com/ReactiveX/rxjs/blob/7.8.1/src/internal/operators/switchMap.ts#L95-L119), [debounceTime 7.8.1](https://github.com/ReactiveX/rxjs/blob/7.8.1/src/internal/operators/debounceTime.ts#L63-L108); accessed 2026-10-15, source publication dates not established. See [pilot evidence](evaluation-lessons.md).

## Validation dependencies

A leaf validator depending on a sibling is not automatically reevaluated by changes to that sibling. Place a relational rule on their common group, or explicitly manage revalidation dependencies. For group async validation, place the function under `asyncValidators.validation`, not synchronous `validators.validation`. Maintainer guidance in I4022 directs the reporter toward the matching-fields/group pattern. [I4022](bug-ledger.md#i4022), [E04](examples.md#e04)

If unrelated invalid fields suppress a group async check, inspect the grouping and Angular validation scheduling. A smaller keyed subgroup can represent the actual dependency set. Do not copy the reporter's claim that async validators run only on an INVALID → VALID transition as a general Angular rule. Keep async results separate from manual `setErrors` state and define how server errors clear. [I4022](bug-ledger.md#i4022)

Async validators should settle according to their contract and the application should handle pending status. A never-ending input stream is not automatically an appropriate validator result. Networking failures need an explicit domain decision; do not silently equate failure with valid or unavailable data. Verify cancellation and completion using the installed Angular/RxJS versions.

## Translation and messages

For live language switching, the official i18n demo supplies translation streams directly to label expressions. A one-time translated string is sufficient only when the label need not change during the form's lifetime. Do not require a particular translation library for the pattern. [E13](examples.md#e13)

Validation messages can be functions returning strings or Observable strings in 6.3.12. The type clarification was released in 6.1.2; that issue was not evidence that runtime Observable rendering had been removed. The message component switches to the selected message Observable. [K38](sources.md#k38), [I3601](bug-ledger.md#i3601)

Message precedence for the first selected error is global registration → error object's message → field `validation.messages` → named sync validator message → named async validator message. An error carrying `errorPath` is handled specially. Do not promise every error is rendered simultaneously. [K38](sources.md#k38)

## State and payload boundaries

Use formState for shared UI context, with a deliberate size/lifetime. Keep payload decisions explicit. In an enabled group, disabled controls may be absent from `form.value` while present in `getRawValue()` and Formly's model; R04 demonstrates that case. Hidden-value retention is a separate setting from disabled state and validation. See [patterns](patterns.md) and [runtime evidence](runtime-evidence.md).

## Angular 21 executed boundary

External timer/Observable expressions, formState changes and Promise validation passed browser checks without manual change detection. Replacing a select's sole active option while its panel is open exposed a keyboard-selection failure that also reproduces with bare Material; close/reopen recovery passed. Read [Angular 21 qualification](angular21-qualification.md) before treating async option rendering as proof that keyboard/model behavior is correct.
