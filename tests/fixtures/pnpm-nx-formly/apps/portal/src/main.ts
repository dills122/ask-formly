import { Component } from '@angular/core';
import { FieldType, FormlyModule } from '@ngx-formly/core';
@Component({selector:'portal-type', template: 'Portal-only field'})
export class PortalAccountType extends FieldType {}
export const portalSetup = FormlyModule.forRoot({types: [{name:'account-code',component:PortalAccountType}]});
export const portalFields = [{key:'portalOnly',type:'account-code'}];
