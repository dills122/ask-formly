# N2 pinned Formly 6.3.12 Material source notes

Source interpretation only; no upstream tests or browser probes were executed.

FormlyMatSliderModule registers slider with the form-field wrapper. It selects FormlyFieldMDCSlider when Number(VERSION.major) from @angular/cdk is at least 15, otherwise the legacy FormlyFieldSlider. [K33](sources.md#k33)

The legacy slider binds formControl on mat-slider. The MDC slider binds formControl on its input matSliderThumb; its slider template forwards min, max, step, displayWith and discrete from props.thumbLabel || props.discrete. [K53](sources.md#k53) [K54](sources.md#k54)

Material form-field props prefix, suffix, textPrefix and textSuffix are TemplateRef values rendered with a context containing field. hintStart and hintEnd accept strings or TemplateRef values. The start hint uses truthy props.description before props.hintStart. [K17](sources.md#k17)

The Material form-field wrapper binds props.appearance, props.floatLabel and props.subscriptSizing, and binds color to props.color with a nullish fallback of primary. subscriptSizing is declared fixed or dynamic. [K17](sources.md#k17)

The Material wrapper disables the built-in mat-form-field required marker and renders its own asterisk inside its label when props.required is truthy and props.hideRequiredMarker is not true. The label itself requires a truthy props.label and props.hideLabel not true. [K17](sources.md#k17)

Material select reads aria-label from props.attributes. For aria-labelledby it uses a truthy props.attributes["aria-labelledby"] value, otherwise the associated form-field label ID. [K14](sources.md#k14)

Material select forwards props.panelClass to mat-select panelClass. Its inspected template does not bind a readonly input. [K14](sources.md#k14)

FormlyMatToggleModule registers toggle with FormlyFieldToggle and the form-field wrapper. [K81](sources.md#k81)

