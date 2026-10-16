import { FormlyFieldConfig } from '@ngx-formly/core';
import { addressFields } from '@acme/form-helpers';
export function buildSupplierFields(): FormlyFieldConfig[] {
  return [{key: 'billing', fieldGroup: addressFields}];
}
