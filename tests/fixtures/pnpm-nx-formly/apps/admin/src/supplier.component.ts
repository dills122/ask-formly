import { Component, OnInit } from '@angular/core';
import { FormGroup, ReactiveFormsModule } from '@angular/forms';
import { FormlyModule, FormlyFieldConfig } from '@ngx-formly/core';
import { buildSupplierFields } from '@acme/forms';
@Component({selector: 'supplier-screen', imports: [ReactiveFormsModule, FormlyModule], templateUrl: './supplier.component.html'})
export class SupplierComponent implements OnInit {
  form = new FormGroup({});
  model = {};
  fields: FormlyFieldConfig[] = [];
  ngOnInit() { this.fields = buildSupplierFields(); }
}
