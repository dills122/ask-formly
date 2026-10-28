# Using facts to answer design questions

These guides compose the existing **Formly 6.3.12 core/Material** facts. They are
caller guidance, not new admitted knowledge or executable Angular qualification.
Each row separates a backed mechanism from a suggested application decision.
Fetch the named IDs with `get_formly_facts` in the resolved scope, and retain their
conditions and limits when answering. A core fact can apply to a Material request;
that does not establish every Material widget's behavior.

## Hide a field while preserving its value

| Step | Evidence and interpretation |
| --- | --- |
| Separate value retention from control registration | **Backed:** `hiding-and-visibility/reset-on-hide-false` skips the hide handler's value-clearing branch. Its condition and limit explicitly allow the hidden control to leave the active control tree. |
| Explain the normal hide/show path | **Backed:** `hide-unregisters-control`, `hide-can-clear-model-value`, and `show-re-registers` in the same topic describe the control and model effects. `shared-key-control` qualifies the removal rule when other fields share a key/control. |
| Explain defaults | **Backed:** `hiding-and-visibility/reset-on-hide-default` describes the registry default; `show-may-reapply-default` limits when showing reapplies a value. Do not describe showing as an unconditional overwrite. |
| If the control must remain registered, choose a different presentation design | **Design proposal:** investigate presentation-only visibility in the application. `public-field-api/css-host-targets` identifies the class target, but does not qualify arbitrary CSS, focus, accessibility, or a complete visibility recipe. |
| Keep disabling distinct | **Backed mechanism:** `expression-callbacks-and-hooks/conditional-disabled-target`, `props-disabled-ancestor-composition`, and `disabled-expression-path` cover expression behavior. They do not establish that disabling is equivalent to hiding or preserving submitted values. |

The existing array fixture mentions `extras.resetFieldOnHide`, but is explicitly
fixture-scoped. It is not a complete configuration-location or precedence guide.
That guide requires a separately reviewed claim; do not extrapolate it from the
fixture. Likewise, control removal does not by itself establish the application's
submitted payload. Check the actual model, control values, and payload selection.

## Avoid collisions between dynamic sections

| Step | Evidence and interpretation |
| --- | --- |
| Identify the collision | **Backed:** `public-field-api/key-id-name-roles` distinguishes model keys from DOM identifiers/names. Renaming a DOM attribute does not establish a different model path. |
| Consider a keyed group for each independent section | **Backed mechanism:** `model-scope/keyed-group-nested-scope` nests the child model scope; `keyless-group-shared-scope` does not. **Design proposal:** use distinct section keys when the application requires distinct model locations. |
| Preserve key semantics | **Backed:** `core-configuration-lifetime/key-paths` distinguishes dotted strings and literal array segments. `public-field-api/field-get-path-boundaries` warns that `field.get` does not preserve all of those distinctions. |
| Explain existing sharing | **Backed:** `core-configuration-lifetime/shared-control-lookup` describes control lookup, and `shared-validator-ownership` describes participating validators. `hiding-and-visibility/shared-key-control` limits hide/removal conclusions. |
| Do not promise isolation from one flag | **Backed limit:** `shareFormControl: false` is not a guarantee of independent model slots or independently registered parent controls. |
| For repeaters, use the supported operations | **Backed:** `array-operations/template-and-children`, `add-coordination`, and `remove-coordination` describe indexed children and coordinated operations. They do not establish arbitrary reorder/identity policies. |

“Which config wins?” needs a concrete scenario. Duplicate type registrations,
duplicate model paths, and fields sharing one control are different cases.
`public-api-configuration/duplicate-type-registration` addresses the first;
it must not be reused as a universal answer for the other two.

## Compose a stepper or wizard

The admitted set has no complete Material stepper recipe. The following is a
planning guide, with the missing support visible instead of filled by inference.

| Decision | Existing support | Remaining application work |
| --- | --- | --- |
| Shared versus nested step data | `model-scope/keyless-group-shared-scope`, `keyed-group-nested-scope`, `leaf-model-enclosing-scope` | Choose the application's model shape. Keyless layout does not create an independent step scope. |
| Custom component registration | `custom-types-and-wrappers/fieldtype-surface`, `component-needs-registration`, `type-registration-options` | Implement and verify the chosen stepper component/template. These facts do not prove that a built-in stepper type exists. |
| Inactive-step visibility | The hide/show/value facts above | Decide whether navigation should remove controls; do not assume Formly `hide` is presentation-only. |
| Per-step validity and navigation | General control scope and validation facts | Material `stepControl` wiring, keyless-step validity aggregation, focus, lazy rendering, and back-navigation need explicit implementation tests. |

Present any proposed template or navigation policy as a design proposal. Do not
label it an upstream example or an executed recipe unless that exact evidence
has been obtained. The [knowledge backlog](knowledge-completion-backlog.md)
records tabs/steps as contextual application guidance outside the retained-source
milestone.

## Choose an initialization mechanism

| Need | Backed mechanism and fact IDs | Boundary |
| --- | --- | --- |
| A computed value exists before build | `initial-values/model-preferred-for-computed-initial` | Initialize the model; the fact does not prescribe an async strategy. |
| A fallback for an absent value | `initial-values/default-value-is-fallback` | Eligible undefined values only; supplied values are not overwritten. Hidden fields have separate conditions. |
| A later model input | `initial-values/changed-model-input-rebuilds` | The component's change condition and application timing still matter. |
| Per-field lifecycle work | `expression-callbacks-and-hooks/oninit-observable-managed`, `manual-subscribe-cleanup`; `core-configuration-lifetime/hook-render-lifetime` | Returned Observables and manual subscriptions have different cleanup ownership. Hide/show is not automatically outer-field destruction/reinitialization. |
| Reusable default configuration | `extensions-presets/preset-setup-reference`, `preset-substitution-timing`; `public-api-configuration/preset-partial-overrides` | Presets fill defaults through the described merge; they do not unconditionally replace supplied values. |
| Registered/component defaults | `public-api-configuration/defaults-order-before-wrapper-fallback`; `core-configuration-lifetime/reverse-merge-values`, `reverse-merge-arrays` | Read the order and nonblank-value/array rules together. Do not invent recursive inheritance guarantees. |
| Cross-cutting build behavior | `extensions-presets/extension-build-phases`, `extension-priority` | Build phases differ from component lifecycle hooks. |
| Runtime shared expression state | `expressions-notifications/formstate-observation` | Use the returned observation conditions; it is not a general state-store recipe. |

Choose by required timing and ownership rather than calling one mechanism the
universal best option. `core-configuration-lifetime/rebuild-clears-validators`
also matters when field replacement/rebuild could discard ad-hoc validators.

## What execution evidence would add

`candidate_only` describes an evidence packet requiring caller assessment. It is
not a per-fact execution flag. An executable qualification should record the
exact Angular/Material/Formly versions, fixture, assertions and result separately
from source provenance. Useful bounded cases are:

- Hide/show with reset-on-hide enabled and disabled: assert model state and
  parent control registration independently, including a shared-key exception.
- Shared and distinct key paths: assert model locations, control identity and
  validator ownership independently; include `shareFormControl: false`.
- A concrete stepper: assert navigation, inactive-step registration, retained
  values and per-step validity for the chosen keyed/keyless layout.
- CSS visibility and disabling: assert focus/accessibility and payload behavior
  in the actual application rather than infer them from class names.

These are proposed assertions, not passed tests. Historical browser failures
B06/B13 remain failures. Source-only MCP fixture tests do not execute Angular or
extend the supported version/adapter matrix.
