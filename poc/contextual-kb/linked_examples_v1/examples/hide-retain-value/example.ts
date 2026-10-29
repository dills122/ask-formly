import { FormGroup } from '@angular/forms';
import { FormlyFieldConfig, FormlyFormOptions } from '@ngx-formly/core';

// Mount with <formly-form [form]="form" [model]="model" [fields]="fields"
// [options]="options" /> and FormlyMaterialModule.
export function hideRetainValue() {
  const form: FormGroup = new FormGroup({});
  const model = { name: 'Ada' };
  const options: FormlyFormOptions = { formState: { hidden: false } };
  const fields: FormlyFieldConfig[] = [{
    key: 'name', type: 'input', props: { label: 'Name' },
    resetOnHide: false,
    expressions: { hide: field => field.options?.formState.hidden === true },
  }];
  function setHidden(hidden: boolean) {
    options.formState.hidden = hidden;
    // Call after mounting, when Formly has populated its update operations.
    options.detectChanges?.(fields[0]);
  }
  return { form, model, fields, options, setHidden };
}
