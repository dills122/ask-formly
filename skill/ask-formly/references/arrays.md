# Arrays and repeatable sections

Scope: source-checked at 6.3.12; upstream tests read, not executed.

`fieldGroup` is the current child-field collection; `fieldArray` is the template or function used to create item fields. A `FieldArrayType` implementation registers a FormArray, sizes its fieldGroup to the model array, clones each item config, and assigns index keys when applicable [K12](sources.md#k12).

A working repeater requires a rendering component and a registered type. The official example's `type: 'repeat'` is registered to `RepeatTypeComponent`, which extends `FieldArrayType`; core does not make that particular name universally available [E01](examples.md#e01), [K03](sources.md#k03).

Use the array type's `add(index?, initialModel?, options?)` and `remove(index, options?)` when implementing its UI. These operations update model/field collections, rebuild, emit changes, and normally mark the control dirty. Manually splicing only fieldGroup bypasses some of that coordination [K12](sources.md#k12).

Important exact-version detail: this implementation tests `initialModel` for truthiness before cloning it. Do not assume passing false, zero, or an empty string to `add` preserves that scalar unchanged; establish the intended model shape and verify that use case [K12](sources.md#k12).

Default values and hide/show behavior interact with item creation. The inspected test section covers default array values, hiding/showing, and insertion at a specific index. These tests supply useful regression scenarios but were not run here [K27](sources.md#k27). Earlier patches need separate checking against [patch history](sources.md#k29).

When adapting the official repeater to Material, preserve the array component logic and registration, replace Bootstrap layout/button assumptions, and test add/remove/reset/hide on the exact target stack. Do not just copy the example's `type: 'repeat'` field into a Material app and omit its component.
