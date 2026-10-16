import { ConfigOption } from '@ngx-formly/core';
import { accountCodeValidator } from '@acme/validation';
import { AccountCodeType } from './account-code.type';
import { SectionPanelWrapper } from './section-panel.wrapper';
export const FORMLY_SETUP: ConfigOption = {
  types: [{name: 'account-code', component: AccountCodeType}],
  wrappers: [{name: 'section-panel', component: SectionPanelWrapper}],
  validators: [{name: 'accountCode', validation: accountCodeValidator}]
};
