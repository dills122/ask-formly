# Value propagation and event boundaries

Pinned Formly 6.3.12 source interpretation; fresh source inspection only. No sealed or historical evaluation artifacts were used. Source inspection does not claim execution qualification.

modelOptions.updateOn accepts change, blur or submit, and the form extension forwards it into newly created FormControl or FormGroup options. modelOptions.debounce has the shape { default: milliseconds }, not a bare number. [K01](sources.md#k01) [K43](sources.md#k43)

For a field with formControl and no fieldGroup, the field subscription uses debounce.default only when it is positive and updateOn is absent or change. In that branch it subscribes to control.valueChanges.pipe(debounceTime(debounce.default)), delaying the Formly model-assignment and fieldChanges emission path. [K41](sources.md#k41)

In the ordinary non-debounced leaf-control subscription, Formly passes each emitted value through field.parsers in array order, feeding each result to the next parser. If the final result is not Object.is-equal to the control value, it writes the parsed result back with formControl.setValue(value). [K41](sources.md#k41)

A positive debounce.default with absent/change updateOn replaces the parser/distinctUntilChanged pipeline, including any conditional startWith(control.value) added for an initial model/control mismatch, with raw control.valueChanges.pipe(debounceTime(...)). This branch bypasses those parser, deduplication and initial-value-start operators in the field subscription. [K41](sources.md#k41)

The leaf-control subscription assigns the emitted value through assignFieldValue when the field has a key, then emits options.fieldChanges with { value, field, type: valueChanges }. Keyless leaf controls still emit the field event without that keyed model assignment. [K41](sources.md#k41)

FormlyForm filters options.fieldChanges for keyed valueChanges events, waits for one NgZone stability emission through switchMap in an ordinary zone (or uses an immediate observable for a noop zone), checks expressions, and emits clone(this.model) through modelChange. [K11](sources.md#k11)

formlyAttributes onChange calls props.change(field, event) and marks the formControl dirty; it does not assign a new control value or model value in that handler. A custom widget still needs its control/value-accessor integration. [K37](sources.md#k37)
