import { Component } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { FieldType, FieldTypeConfig, FormlyModule } from '@ngx-formly/core';
@Component({selector: 'account-code-type', imports: [ReactiveFormsModule, MatInputModule, FormlyModule], template: '<input matInput [formControl]="formControl" [formlyAttributes]="field" />'})
export class AccountCodeType extends FieldType<FieldTypeConfig> {}
