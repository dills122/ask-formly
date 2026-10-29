import { FormGroup } from '@angular/forms';
import { FormlyFieldConfig, FormlyFormOptions } from '@ngx-formly/core';
import { Subject, tap } from 'rxjs';

// The model is ready before build. defaultValue only supplies a missing value.
// The hook is a separate example of managed subscription ownership, not an
// alternative asynchronous initialization recipe.
export function initializationChoices() {
  const form: FormGroup = new FormGroup({});
  const model: { supplied: string; fallback?: string } = { supplied: 'Computed before build' };
  const options: FormlyFormOptions = {};
  const events = new Subject<string>();
  const observed: string[] = [];
  const fields: FormlyFieldConfig[] = [
    { key: 'supplied', type: 'input', defaultValue: 'Unused fallback', props: { label: 'Supplied' } },
    { key: 'fallback', type: 'input', defaultValue: 'Default for undefined', props: { label: 'Fallback' },
      hooks: {
        // Return the Observable itself; do not manually subscribe here.
        onInit: () => events.pipe(tap(value => observed.push(value))),
      },
    },
  ];
  return { form, model, fields, options, events, observed };
}
