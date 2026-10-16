import { FormlyFieldConfig } from '@ngx-formly/core';
export const addressFields: FormlyFieldConfig[] = [{
  key: 'accountCode', type: 'account-code', wrappers: ['section-panel'],
  props: {label: 'Account code', required: true}, validators: {validation: ['accountCode']}
}];
