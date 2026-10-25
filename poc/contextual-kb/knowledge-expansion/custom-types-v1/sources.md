# Proposed evidence references

Immutable upstream commit: 5f099fddea6426b46a453866adf0fede5be0bcd7. These are source-inspection findings, not newly executed Angular runtime tests.

## k65

[docs/custom-formly-field.md](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/docs/custom-formly-field.md#L22-L39)

Exact excerpt:

```markdown
  ### 1. Defining the Field Type class and its template:

  First you have to create a component representing the field which extends `FieldType` class.

  ```typescript
  import { Component } from '@angular/core';
  import { FieldType, FieldTypeConfig } from '@ngx-formly/core';

  @Component({
    selector: 'formly-field-input',
    template: `
      <input type="input" [formControl]="formControl" [formlyAttributes]="field">
    `,
  })
  export class InputFieldType extends FieldType<FieldTypeConfig> {}
  ```

  > We passed a `formControl` instance which is created by Formly to the `input`, to let Formly know that this is the input that you want to associate with your model.
```

## k66

[demo/src/app/examples/introduction/custom-field.type.ts](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/demo/src/app/examples/introduction/custom-field.type.ts#L1-L12)

Exact excerpt:

```typescript
import { Component } from '@angular/core';
import { FieldType, FieldTypeConfig } from '@ngx-formly/core';

@Component({
  selector: 'formly-field-custom-input',
  template: ` <input [type]="type" [formControl]="formControl" [formlyAttributes]="field" /> `,
})
export class CustomFieldType extends FieldType<FieldTypeConfig> {
  get type() {
    return this.props.type || 'text';
  }
}
```

## k67

[src/core/src/lib/templates/formly.attributes.ts](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/templates/formly.attributes.ts#L16-L27)

Exact excerpt:

```typescript
/**
 * Allow to link the `field` HTML attributes (`id`, `name` ...) and Event attributes (`focus`, `blur` ...) to an element in the DOM.
 */
@Directive({
  selector: '[formlyAttributes]',
  host: {
    '(change)': 'onHostChange($event)',
  },
})
export class FormlyAttributes implements OnChanges, DoCheck, OnDestroy {
  /** The field config. */
  @Input('formlyAttributes') field: FormlyFieldConfig;
```

## k68

[demo/src/app/examples/introduction/app.module.ts](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/demo/src/app/examples/introduction/app.module.ts#L1-L22)

Exact excerpt:

```typescript
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { FormlyModule } from '@ngx-formly/core';
import { FormlyBootstrapModule } from '@ngx-formly/bootstrap';

import { AppComponent } from './app.component';
import { CustomFieldType } from './custom-field.type';

@NgModule({
  imports: [
    CommonModule,
    ReactiveFormsModule,
    FormlyBootstrapModule,
    FormlyModule.forRoot({
      validationMessages: [{ name: 'required', message: 'This field is required' }],
      types: [{ name: 'custom', component: CustomFieldType, wrappers: ['form-field'] }],
    }),
  ],
  declarations: [AppComponent, CustomFieldType],
})
export class AppModule {}
```

## k69

[src/core/src/lib/templates/field.type.ts](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/templates/field.type.ts#L6-L14)

Exact excerpt:

```typescript
export interface FieldTypeConfig<T = FormlyFieldConfig['props']> extends FormlyFieldConfig<T> {
  formControl: FormControl;
  props: NonNullable<T>;
}

export interface FieldGroupTypeConfig<T = FormlyFieldConfig['props']> extends FormlyFieldConfig<T> {
  formControl: FormGroup;
  props: NonNullable<T>;
}
```

## k70

[docs/custom-formly-field.md](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/docs/custom-formly-field.md#L52-L104)

Exact excerpt:

```markdown
  ### 3. set an aliase for `InputFieldType` component (Optional):

  > Note: This step is required only for JSON powered forms (see "Method-2" below).

  ```typescript
  import { InputFieldType } from './input-field.type';

  @NgModule({
    imports: [
      FormlyModule.forRoot({
        types: [
          { name: 'input', component: InputFieldType },
        ],
      }),
    ],
  })
  export class AppModule {}
  ```

  > `types: [ ... ]` allows you to specify a custom type which you can use in your field configuration.
  >
  > A typical Type requires two properties:
  > 1. `name`: The name of the component type. You use this in the `type` option of a field.
  > 2. `component`: the component that Formly should create when this type is set.

  ### 4. Use the created custom type in the form config:
  * Method 1: Pass the `InputFieldType` component to the field config.

    ```typescript
    import { InputFieldType } from './input-field.type';

    export class AppComponent {
      fields: FormlyFieldConfig[] = [
        {
          key: 'firstname',
          type: InputFieldType,
        },
      ];
    }
    ```

  * Method 2: Pass the `InputFieldType` alias (defined in `FormlyModule.forRoot`) to the field config.

    ```typescript
    export class AppComponent {
      fields: FormlyFieldConfig[] = [
        {
          key: 'firstname',
          type: 'input',
        },
      ];
    }
    ```
```

## k71

[src/core/src/lib/services/formly.config.ts](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/services/formly.config.ts#L98-L116)

Exact excerpt:

```typescript
  getType(name: FormlyFieldConfig['type'], throwIfNotFound = false): TypeOption {
    if (name instanceof Type) {
      return { component: name, name: name.prototype.constructor.name };
    }

    if (!this.types[name]) {
      if (throwIfNotFound) {
        throw new Error(
          `[Formly Error] The type "${name}" could not be found. Please make sure that is registered through the FormlyModule declaration.`,
        );
      }

      return null;
    }

    this.mergeExtendedType(name);

    return this.types[name];
  }
```

## k72

[src/core/src/lib/core.module.ts](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/core.module.ts#L47-L78)

Exact excerpt:

```typescript
export class FormlyModule {
  static forRoot(config: ConfigOption = {}): ModuleWithProviders<FormlyModule> {
    return {
      ngModule: FormlyModule,
      providers: [
        { provide: FORMLY_CONFIG, multi: true, useFactory: defaultFormlyConfig, deps: [FormlyConfig] },
        { provide: FORMLY_CONFIG, useValue: config, multi: true },
        FormlyConfig,
        FormlyFormBuilder,
      ],
    };
  }

  static forChild(config: ConfigOption = {}): ModuleWithProviders<FormlyModule> {
    return {
      ngModule: FormlyModule,
      providers: [
        { provide: FORMLY_CONFIG, multi: true, useFactory: defaultFormlyConfig, deps: [FormlyConfig] },
        { provide: FORMLY_CONFIG, useValue: config, multi: true },
        FormlyFormBuilder,
      ],
    };
  }

  constructor(configService: FormlyConfig, @Optional() @Inject(FORMLY_CONFIG) configs: ConfigOption[] = []) {
    if (!configs) {
      return;
    }

    configs.forEach((config) => configService.addConfig(config));
  }
}
```

## k73

[src/core/src/lib/services/formly.config.ts](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/services/formly.config.ts#L148-L151)

Exact excerpt:

```typescript
    if (!field.wrappers && type.wrappers) {
      field.wrappers = [...type.wrappers];
    }
  }
```

## k74

[src/ui/material/input/src/input.type.ts](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/ui/material/input/src/input.type.ts#L1-L50)

Exact excerpt:

```typescript
import { Component, ChangeDetectionStrategy, Type } from '@angular/core';
import { FieldTypeConfig, FormlyFieldConfig } from '@ngx-formly/core';
import { FieldType, FormlyFieldProps } from '@ngx-formly/material/form-field';

interface InputProps extends FormlyFieldProps {}

export interface FormlyInputFieldConfig extends FormlyFieldConfig<InputProps> {
  type: 'input' | Type<FormlyFieldInput>;
}

@Component({
  selector: 'formly-field-mat-input',
  template: `
    <input
      *ngIf="type !== 'number'; else numberTmp"
      matInput
      [id]="id"
      [name]="field.name"
      [type]="type || 'text'"
      [readonly]="props.readonly"
      [required]="required"
      [errorStateMatcher]="errorStateMatcher"
      [formControl]="formControl"
      [formlyAttributes]="field"
      [tabIndex]="props.tabindex"
      [placeholder]="props.placeholder"
    />
    <ng-template #numberTmp>
      <input
        matInput
        [id]="id"
        [name]="field.name"
        type="number"
        [readonly]="props.readonly"
        [required]="required"
        [errorStateMatcher]="errorStateMatcher"
        [formControl]="formControl"
        [formlyAttributes]="field"
        [tabIndex]="props.tabindex"
        [placeholder]="props.placeholder"
      />
    </ng-template>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class FormlyFieldInput extends FieldType<FieldTypeConfig<InputProps>> {
  get type() {
    return this.props.type || 'text';
  }
}
```

## k75

[src/ui/material/input/src/input.module.ts](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/ui/material/input/src/input.module.ts#L11-L26)

Exact excerpt:

```typescript
@NgModule({
  declarations: [FormlyFieldInput],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatInputModule,

    FormlyMatFormFieldModule,
    FormlyModule.forChild({
      types: [
        {
          name: 'input',
          component: FormlyFieldInput,
          wrappers: ['form-field'],
        },
        { name: 'string', extends: 'input' },
```

## k76

[src/core/src/lib/core.ts](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/core.ts#L1-L26)

Exact excerpt:

```typescript
export { FormlyForm } from './components/formly.form';
export {
  FormlyFieldConfig,
  FormlyTemplateOptions,
  FormlyFormOptions,
  FormlyFieldProps,
  ConfigOption,
  FormlyExtension,
} from './models';
export { FormlyField } from './components/formly.field';
export { FormlyAttributes as ɵFormlyAttributes } from './templates/formly.attributes';
export { FormlyGroup as ɵFormlyGroup } from './templates/formly.group';
export { FormlyTemplate as ɵFormlyTemplate } from './components/formly.template';
export { FormlyValidationMessage as ɵFormlyValidationMessage } from './templates/formly.validation-message';
export { FORMLY_CONFIG, FormlyConfig } from './services/formly.config';
export { FormlyFormBuilder } from './services/formly.builder';
export { FieldType, FieldTypeConfig, FieldGroupTypeConfig } from './templates/field.type';
export { FieldArrayType, FieldArrayTypeConfig } from './templates/field-array.type';
export { FieldWrapper } from './templates/field.wrapper';
export { FormlyModule } from './core.module';
export { defineHiddenProp as ɵdefineHiddenProp } from './utils';
export { reverseDeepMerge as ɵreverseDeepMerge } from './utils';
export { getFieldValue as ɵgetFieldValue } from './utils';
export { clone as ɵclone } from './utils';
export { observe as ɵobserve } from './utils';
export { hasKey as ɵhasKey } from './utils';
```

## k77

[src/core/src/public_api.ts](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/public_api.ts#L1-L5)

Exact excerpt:

```typescript
/*
 * Public API Surface of core
 */

export * from './lib/core';
```

## k78

[src/core/src/lib/models/config.ts](https://github.com/ngx-formly/ngx-formly/blob/5f099fddea6426b46a453866adf0fede5be0bcd7/src/core/src/lib/models/config.ts#L62-L68)

Exact excerpt:

```typescript
export interface ConfigOption {
  types?: TypeOption[];
  wrappers?: WrapperOption[];
  validators?: ValidatorOption[];
  extensions?: ExtensionOption[];
  validationMessages?: ValidationMessageOption[];
  extras?: {
```
