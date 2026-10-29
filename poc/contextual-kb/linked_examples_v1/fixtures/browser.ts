import 'zone.js';
import '@angular/compiler';
import { Component } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { BrowserDynamicTestingModule, platformBrowserDynamicTesting } from '@angular/platform-browser-dynamic/testing';
import { ReactiveFormsModule } from '@angular/forms';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { FormlyModule } from '@ngx-formly/core';
import { FormlyMaterialModule } from '@ngx-formly/material';
import { hideRetainValue } from '../examples/hide-retain-value/example';
import { keyedDynamicSections } from '../examples/keyed-dynamic-sections/example';
import { initializationChoices } from '../examples/initialization-choices/example';

const results: {name: string; passed: boolean}[] = [];
function check(name: string, condition: boolean) {
  results.push({ name, passed: condition });
  if (!condition) throw new Error(name);
}
TestBed.initTestEnvironment(BrowserDynamicTestingModule, platformBrowserDynamicTesting());
async function mount(value: any) {
  class Host { form = value.form; model = value.model; fields = value.fields; options = value.options; }
  Component({ selector: 'test-host', standalone: false, template: '<formly-form [form]="form" [model]="model" [fields]="fields" [options]="options"></formly-form>' })(Host);
  await TestBed.configureTestingModule({ declarations: [Host], imports: [ReactiveFormsModule, NoopAnimationsModule, FormlyModule.forRoot(), FormlyMaterialModule] }).compileComponents();
  const fixture = TestBed.createComponent(Host);
  fixture.detectChanges();
  await fixture.whenStable();
  fixture.detectChanges();
  return fixture;
}
async function run() {
  const hide = hideRetainValue();
  let fixture = await mount(hide);
  check('hide.initial-registration', hide.form.get('name') !== null);
  check('hide.initial-value', hide.model.name === 'Ada');
  hide.setHidden(true); fixture.detectChanges();
  check('hide.retained-model', hide.model.name === 'Ada');
  check('hide.unregistered-control', hide.form.get('name') === null);
  hide.setHidden(false); fixture.detectChanges();
  check('hide.reregistered-value', hide.form.get('name')?.value === 'Ada');
  fixture.destroy(); TestBed.resetTestingModule();

  // Supplementary negative control: resetOnHide true clears the single value.
  const reset = hideRetainValue();
  reset.fields[0].resetOnHide = true;
  fixture = await mount(reset);
  reset.setHidden(true); fixture.detectChanges();
  check('hide.reset-true-clears-value', reset.model.name === undefined);
  check('hide.reset-true-unregisters', reset.form.get('name') === null);
  fixture.destroy(); TestBed.resetTestingModule();

  // Supplementary shared-key exception: a visible sibling retains the control.
  const shared = hideRetainValue();
  shared.fields.push({key: 'name', type: 'input', props: {label: 'Visible alias'}});
  fixture = await mount(shared);
  shared.setHidden(true); fixture.detectChanges();
  check('hide.visible-shared-key-retains-control', shared.form.get('name') !== null);
  check('hide.visible-shared-key-retains-value', shared.model.name === 'Ada');
  fixture.destroy(); TestBed.resetTestingModule();

  const groups = keyedDynamicSections();
  fixture = await mount(groups);
  const billing = groups.form.get('billing.name');
  const shipping = groups.form.get('shipping.name');
  check('groups.distinct-controls', !!billing && !!shipping && billing !== shipping);
  check('groups.billing-scope', groups.fields[0].fieldGroup![0].model === groups.model.billing);
  check('groups.shipping-scope', groups.fields[1].fieldGroup![0].model === groups.model.shipping);
  billing!.setValue('Updated'); fixture.detectChanges();
  await fixture.whenStable();
  check('groups.independent-values', groups.model.billing.name === 'Updated' && groups.model.shipping.name === 'Grace');
  fixture.destroy(); TestBed.resetTestingModule();

  const init = initializationChoices();
  fixture = await mount(init);
  check('init.supplied-preserved', init.model.supplied === 'Computed before build');
  check('init.undefined-defaulted', init.model.fallback === 'Default for undefined');
  init.events.next('mounted');
  check('init.returned-stream-subscribed', init.observed.join(',') === 'mounted');
  fixture.destroy();
  init.events.next('destroyed');
  check('init.returned-stream-disposed', init.observed.join(',') === 'mounted');
  TestBed.resetTestingModule();
  return results;
}
(window as any).__linkedExamples = run().then(assertions => ({status: 'passed', assertions})).catch(error => ({status: 'failed', error: String(error.stack || error), assertions: results}));
