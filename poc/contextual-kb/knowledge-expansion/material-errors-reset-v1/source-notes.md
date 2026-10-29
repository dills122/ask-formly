# Material error rendering and reset sequence — source notes

Exact Formly 6.3.12, pinned commit `5f099fddea6426b46a453866adf0fede5be0bcd7`. These are source-derived contracts for an isolated candidate; no application/browser execution is established. Existing authored inputs and installed DB are unchanged.

## Stock wrapper error message child

In Formly 6.3.12, the stock Material form-field wrapper places a mat-error element inside its mat-form-field after the field component insertion point; that mat-error contains formly-validation-message bound to the same field. The stock wrapper therefore supplies the validation-message markup for the Material form-field's error area; a compatible field using that wrapper does not need to duplicate that error-message child. [K17](sources.md#k17)

K17 lines 81–83 contain the mat-error and field-bound message child inside the wrapper template. Placement in source identifies the stock Material error area; it does not certify pixels, CSS, animation, accessibility or another adapter. Arbitrary custom controls still need the relevant Material/control integration.

## Material error-state bridge

Formly 6.3.12 Material FieldType connects Material error state to Formly's showError policy. Its errorStateMatcher.isErrorState returns this.field && this.showError. Its errorState getter calls this.options.showError(this), updates the cached error state and emits stateChanges when that value changes, then returns the policy result. Material error state is therefore not a promise to display an error solely because a control is invalid. [K16](sources.md#k16)

The existing default-error-visibility fact separately states the default invalid-and-touched/submitted/validation.show predicate. A configured showError policy may differ. This bridge is not a validator, a pending-submit guard, immediate remote-feedback scheduling or proof that any plain core/custom type supplies MatFormFieldControl integration.

## Root reset sequence

During Formly 6.3.12 core root-option initialization, the installed options.resetModel callback clones the supplied non-nullish model or options._initialModel. If field.model is truthy, it deletes that object's keys and assigns the cloned model or an empty object into it. When !isSignalRequired(), it sets the observed options.parentForm.submitted value to false with notifications disabled. It then calls options.build(field), followed by field.form.reset(field.model). The submission-state operation is conditional and occurs before rebuild and control reset. [K05](sources.md#k05)

This refines the existing baseline/rebuild/reset fact without replacing it. No installed callback is promised on an unbuilt options object. The source delegates dirty/touched/error effects to Angular form reset; it does not promise that invalid restored values become valid or every error disappears. It does not coordinate dependent country/state option streams, HTTP cancellation, user-versus-restore policies, or submission timing. Formly clone retains its existing special-value limitations.
