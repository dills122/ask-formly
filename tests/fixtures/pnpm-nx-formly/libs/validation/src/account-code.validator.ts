import { AbstractControl } from '@angular/forms';
export function accountCodeValidator(control: AbstractControl): boolean { return /^[A-Z]{3}$/.test(control.value); }
