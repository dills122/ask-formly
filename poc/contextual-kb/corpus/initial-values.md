# Initial values at build time and afterward

The official default-value demo presents initializing the model as the preferred
choice and field `defaultValue` as the other choice. Its `lastName` model value
is present while the field also has a `defaultValue`; the field's `firstName`
uses `defaultValue` with no initial model value [E14a](sources.md#e14a),
[E14b](sources.md#e14b).

Core assigns a field's `defaultValue` only when the keyed model value is
undefined and the field is not hidden under the relevant build conditions.
An application-computed initial value can therefore be placed in the model
before that field is built; `defaultValue` is the undefined-value fallback,
not an override of an existing model value [K05](sources.md#k05).

For a value arriving after the initial build, the Formly form component accepts
a model input and can rebuild when Angular reports a changed model input that
passes its change check. This supports supplying a changed model from
application state; it does not establish
that a field `defaultValue` watches later state or that a hook is required
[K11](sources.md#k11). The consuming app still needs to check timing and
reference-change behavior.
