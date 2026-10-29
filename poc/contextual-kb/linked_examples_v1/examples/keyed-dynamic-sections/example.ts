import { FormGroup } from '@angular/forms';
import { FormlyFieldConfig, FormlyFormOptions } from '@ngx-formly/core';

// Give each independent section a distinct model key. Repeated child names
// then resolve under separate section paths; DOM ids do not provide isolation.
export function keyedDynamicSections() {
  const form: FormGroup = new FormGroup({});
  const model = { billing: { name: 'Ada' }, shipping: { name: 'Grace' } };
  const options: FormlyFormOptions = {};
  const fields: FormlyFieldConfig[] = ['billing', 'shipping'].map(section => ({
    key: section,
    fieldGroup: [{
      key: 'name', id: `${section}-name`, type: 'input',
      props: { label: `${section} name` },
    }],
  }));
  return { form, model, fields, options };
}
