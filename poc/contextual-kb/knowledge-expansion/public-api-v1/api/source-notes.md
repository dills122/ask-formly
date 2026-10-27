# Public field API source notes

Pinned Formly 6.3.12, commit 5f099fddea6426b46a453866adf0fede5be0bcd7. Claims below are bounded source-derived paraphrases, followed by exact upstream excerpts for audit.

## field-get-tree-lookup

For string or dot-joined array paths, with traversed keyed groups also using string or array keys, field.get(key) returns a descendant field configuration rather than an Angular control, or undefined when no descendant matches. It searches fieldGroup children in order, checks a child key for equality first, and recurses through null/undefined-key groups without consuming the requested key or through matching dotted key prefixes after consuming that prefix. [K05](sources.md#k05) [K140](sources.md#k140)

Limit: Scalar numeric-key traversal is not guaranteed: a numeric lookup request can throw when traversal reaches key.indexOf for a keyed child group. The undefined-on-miss statement is limited to the string/dot-joined-array paths described above.

## field-get-path-boundaries

field.get joins array keys with dots for both the request and child keys. Consequently ["a.b"] and ["a", "b"] are indistinguishable to this lookup. Unlike getKeyPath, this lookup does not normalize bracket notation. [K140](sources.md#k140) [K39](sources.md#k39)

## key-id-name-roles

key links a field value to the model; id specifies its field HTML identifier and is generated when not supplied; name is a separately configurable field name. formlyAttributes sets a truthy field.name on its DOM element and, for its single attached element when no directive id input is supplied, applies field.id. [K01](sources.md#k01) [K05](sources.md#k05) [K37](sources.md#k37)

## css-host-targets

className targets the outer formly-field component. fieldGroupClassName targets the built-in formly-group component, whose host class binding uses field.fieldGroupClassName or an empty string. [K01](sources.md#k01) [K41](sources.md#k41) [K141](sources.md#k141)

## array-control-type

The public FieldArrayTypeConfig<T> interface extends FormlyFieldConfig<T>, requires formControl: FormArray and props: NonNullable<T>, and is the default generic configuration for FieldArrayType. [K02](sources.md#k02) [K142](sources.md#k142)

## options-build-default

FormlyFormOptions declares build(field?) returning FormlyFieldConfig. When root builder setup finds no existing options.build, it installs a callback that builds its supplied field, defaults to that root field when omitted, and returns the field that it built. [K01](sources.md#k01) [K06](sources.md#k06)

## Exact upstream excerpt K01 (lines 1–287)

```typescript
import {
  FormGroup,
  FormArray,
  AbstractControl,
  FormGroupDirective,
  ValidatorFn,
  AsyncValidatorFn,
} from '@angular/forms';
import { Subject, Observable } from 'rxjs';
import { FieldType } from '../templates/field.type';
import { FieldWrapper } from '../templates/field.wrapper';
import { ValidationMessageOption } from '../models';
import { Type } from '@angular/core';

type FieldExpression<T = any> = string | ((field: FormlyFieldConfig) => T) | Observable<T>;
type FieldExpressions = { [property: string]: FieldExpression } & {
  className?: FieldExpression<string>;
  hide?: FieldExpression<boolean>;
  'props.disabled'?: FieldExpression<boolean>;
  'props.required'?: FieldExpression<boolean>;
};

export interface FormlyFieldConfig<Props = FormlyFieldProps & { [additionalProperties: string]: any }> {
  /**
   * The key that relates to the model. This will link the field value to the model
   */
  key?: string | number | (string | number)[];

  /**
   * This should be a formly-field type added either by you or a plugin. More information over at Creating Formly Fields.
   */
  type?: string | Type<FieldType>;

  /**
   * Use `defaultValue` to initialize it the model. If this is provided and the value of the model at compile-time is undefined, then the value of the model will be assigned to `defaultValue`.
   */
  defaultValue?: any;

  /**
   * This allows you to specify the `id` of your field. Note, the `id` is generated if not set.
   */
  id?: string;

  /**
   * If you wish, you can specify a specific `name` for your field. This is useful if you're posting the form to a server using techniques of yester-year.
   */
  name?: string;

  /**
   * This is reserved for the templates. Any template-specific options go in here. Look at your specific template implementation to know the options required for this.
   */
  props?: Props;

  /** @deprecated Use `props` instead. */
  templateOptions?: FormlyTemplateOptions;

  /**
   * An object with a few useful properties
   * - `validation.messages`: A map of message names that will be displayed when the field has errors.
   * - `validation.show`: A boolean you as the developer can set to force displaying errors whatever the state of field. This is useful when you're trying to call the user's attention to some fields for some reason.
   */
  validation?: {
    messages?: { [messageProperties: string]: ValidationMessageOption['message'] } & {
      /** @deprecated use `minLength` */
      minlength?: ValidationMessageOption['message'];

      /** @deprecated use `maxLength` */
      maxlength?: ValidationMessageOption['message'];
    };
    show?: boolean;
    [additionalProperties: string]: any;
  };

  /**
   * Used to set validation rules for a particular field.
   * Should be an object of key - value pairs. The value can either be an expression to evaluate or a function to run.
   * Each should return a boolean value, returning true when the field is valid. See Validation for more information.
   */
  validators?: FormlyValidation<ValidatorFn, boolean>;

  /**
   * Use this one for anything that needs to validate asynchronously.
   * Pretty much exactly the same as the validators api, except it must be a function that returns a promise.
   */
  asyncValidators?: FormlyValidation<AsyncValidatorFn, Promise<boolean> | Observable<boolean>>;

  /**
   * Can be set instead of `type` to render custom html content.
   */
  template?: string;

  /**
   *  It is expected to be the name of the wrappers.
   *  The formly field template will be wrapped by the first wrapper, then the second, then the third, etc.
   *  You can also specify these as part of a type (which is the recommended approach).
   */
  wrappers?: (string | Type<FieldWrapper>)[];

  /**
   * Whether to hide the field. Defaults to false. If you wish this to be conditional use `expressions: { hide: ... }`
   */
  hide?: boolean;

  /**
   * Whether to reset the value on hide or not. Defaults to `true`.
   */
  resetOnHide?: boolean;

  /**
   * Conditionally hiding Field based on values from other Fields
   * @deprecated use `expressions: { hide: ... }`
   */
  hideExpression?: boolean | string | ((model: any, formState: any, field?: FormlyFieldConfig) => boolean);

  /**
   * An object where the key is a property to be set on the main field config and the value is an expression used to assign that property.
   * @deprecated use `expressions`
   */
  expressionProperties?: {
    [property: string]: string | ((model: any, formState: any, field?: FormlyFieldConfig) => any) | Observable<any>;
  };

  /**
   * An object where the key is a property to be set on the main field config and the value is an expression used to assign that property.
   */
  expressions?: FieldExpressions;

  /**
   * You can specify your own class that will be applied to the `formly-field` component.
   */
  className?: string;

  /**
   * Specify your own class that will be applied to the `formly-group` component.
   */
  fieldGroupClassName?: string;

  /**
   * A field group is a way to group fields together, making advanced layout very simple.
   * It can also be used to group fields that are associated with the same model (useful if it's different than the model for the rest of the fields).
   */
  fieldGroup?: FormlyFieldConfig[];

  fieldArray?: FormlyFieldConfig | ((field: FormlyFieldConfig) => FormlyFieldConfig);

  /**
   * Whether to focus or blur the element field. Defaults to false. If you wish this to be conditional use `expressions`
   */
  focus?: boolean;

  /**
   * An object with a few useful properties to control the model changes
   * - `debounce`: integer value which contains the debounce model update value in milliseconds. A value of 0 triggers an immediate update.
   * - `updateOn`: string event value that instructs when the control should be updated
   */
  modelOptions?: {
    debounce?: {
      default: number;
    };
    // @see https://angular.io/api/forms/AbstractControl#updateOn
    updateOn?: 'change' | 'blur' | 'submit';
  };

  hooks?: FormlyHookConfig;

  /**
   * Array of functions to execute, as a pipeline, whenever the model updates, usually via user input.
   */
  parsers?: ((value: any) => any)[];

  /**
   * Returns child field by key name
   */
  get?: (key: FormlyFieldConfig['key']) => FormlyFieldConfig;

  /**
   * The model that stores all the data, where the model[key] is the value of the field
   */
  readonly model?: any;

  /**
   * The parent field.
   */
  readonly parent?: FormlyFieldConfig;

  /**
   * The form options.
   */
  readonly options?: FormlyFormOptions;

  /**
   * The parent form.
   */
  readonly form?: FormGroup | FormArray;

  /**
   * This is the [FormControl](https://angular.io/api/forms/FormControl) for the field.
   * It provides you more control like running validators, calculating status, and resetting state.
   */
  readonly formControl?: AbstractControl;

  /** @deprecated */
  optionsTypes?: string[];
}

export type FormlyAttributeEvent = (field: FormlyFieldConfig, event?: any) => void;

/**  @deprecated */
export interface FormlyTemplateOptions extends FormlyFieldProps {
  [additionalProperties: string]: any;
}

export interface FormlyFieldProps {
  type?: string;
  label?: string;
  placeholder?: string;
  disabled?: boolean;
  options?: any[] | Observable<any[]>;
  rows?: number;
  cols?: number;
  description?: string;
  hidden?: boolean;
  max?: number;
  min?: number;

  minLength?: number;
  /** @deprecated use `minLength` */
  minlength?: number;

  maxLength?: number;
  /** @deprecated use `maxLength` */
  maxlength?: number;

  pattern?: string | RegExp;
  required?: boolean;
  tabindex?: number;
  readonly?: boolean;
  attributes?: { [key: string]: string | number };
  step?: number;
  focus?: FormlyAttributeEvent;
  blur?: FormlyAttributeEvent;
  keyup?: FormlyAttributeEvent;
  keydown?: FormlyAttributeEvent;
  click?: FormlyAttributeEvent;
  change?: FormlyAttributeEvent;
  keypress?: FormlyAttributeEvent;
}

export type FormlyHookFn = (field: FormlyFieldConfig) => void;

export interface FormlyHookConfig {
  onInit?: FormlyHookFn | ((field: FormlyFieldConfig) => Observable<any>);
  onChanges?: FormlyHookFn;
  afterContentInit?: FormlyHookFn;
  afterViewInit?: FormlyHookFn;
  onDestroy?: FormlyHookFn;
}

export interface FormlyFormOptions {
  updateInitialValue?: (model?: any) => void;
  resetModel?: (model?: any) => void;
  formState?: any;
  fieldChanges?: Subject<FormlyValueChangeEvent>;
  showError?: (field: FieldType) => boolean;
  build?: (field?: FormlyFieldConfig) => FormlyFieldConfig;
  checkExpressions?: (field: FormlyFieldConfig) => void;
  detectChanges?: (field: FormlyFieldConfig) => void;
  parentForm?: FormGroupDirective | null;
}

export interface FormlyValueChangeEvent {
  field: FormlyFieldConfig;
  type: string;
  value: any;
  [meta: string]: any;
}

interface FormlyValidation<T, R> {
  validation?: (string | T)[] | any;
  [key: string]: FormlyValidatorFn<R> | FormlyValidatorExpressionFn<R> | any;
}
type FormlyValidatorFn<T> = (control: AbstractControl, field: FormlyFieldConfig) => T;

interface FormlyValidatorExpressionFn<T> {
  expression: FormlyValidatorFn<T>;
  message: string | ((error: any, field: FormlyFieldConfig) => string | Observable<string>);
}
```

## Exact upstream excerpt K02 (lines 1–26)

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

## Exact upstream excerpt K05 (lines 21–168)

```typescript
export class CoreExtension implements FormlyExtension {
  private formId = 0;
  constructor(private config: FormlyConfig) {}

  prePopulate(field: FormlyFieldConfigCache) {
    const root = field.parent;
    this.initRootOptions(field);
    this.initFieldProps(field);
    if (root) {
      Object.defineProperty(field, 'options', { get: () => root.options, configurable: true });
      Object.defineProperty(field, 'model', {
        get: () => (hasKey(field) && field.fieldGroup ? getFieldValue(field) : root.model),
        configurable: true,
      });
    }

    Object.defineProperty(field, 'get', {
      value: (key: FormlyFieldConfig['key']) => getField(field, key),
      configurable: true,
    });

    this.getFieldComponentInstance(field).prePopulate?.(field);
  }

  onPopulate(field: FormlyFieldConfigCache) {
    this.initFieldOptions(field);
    this.getFieldComponentInstance(field).onPopulate?.(field);
    if (field.fieldGroup) {
      field.fieldGroup.forEach((f, index) => {
        if (f) {
          Object.defineProperty(f, 'parent', { get: () => field, configurable: true });
          Object.defineProperty(f, 'index', { get: () => index, configurable: true });
        }
        this.formId++;
      });
    }
  }

  postPopulate(field: FormlyFieldConfigCache) {
    this.getFieldComponentInstance(field).postPopulate?.(field);
  }

  private initFieldProps(field: FormlyFieldConfigCache) {
    field.props ??= field.templateOptions;
    Object.defineProperty(field, 'templateOptions', {
      get: () => field.props,
      set: (props) => (field.props = props),
      configurable: true,
    });
  }

  private initRootOptions(field: FormlyFieldConfigCache) {
    if (field.parent) {
      return;
    }

    const options = field.options;
    field.options.formState = field.options.formState || {};
    if (!options.showError) {
      options.showError = this.config.extras.showError;
    }

    if (!options.fieldChanges) {
      defineHiddenProp(options, 'fieldChanges', new Subject<FormlyValueChangeEvent>());
    }

    if (!options._hiddenFieldsForCheck) {
      options._hiddenFieldsForCheck = [];
    }

    options._markForCheck = (f) => {
      console.warn(`Formly: 'options._markForCheck' is deprecated since v6.0, use 'options.detectChanges' instead.`);
      options.detectChanges(f);
    };

    options._detectChanges = (f: FormlyFieldConfigCache) => {
      if (f._componentRefs) {
        markFieldForCheck(f);
      }

      f.fieldGroup?.forEach((f) => f && options._detectChanges(f));
    };

    options.detectChanges = (f: FormlyFieldConfigCache) => {
      f.options.checkExpressions?.(f);
      options._detectChanges(f);
    };

    options.resetModel = (model?: any) => {
      model = clone(model ?? options._initialModel);
      if (field.model) {
        Object.keys(field.model).forEach((k) => delete field.model[k]);
        Object.assign(field.model, model || {});
      }

      if (!isSignalRequired()) {
        observe(options, ['parentForm', 'submitted']).setValue(false, false);
      }
      options.build(field);
      field.form.reset(field.model);
    };

    options.updateInitialValue = (model?: any) => (options._initialModel = clone(model ?? field.model));
    field.options.updateInitialValue();
  }

  private initFieldOptions(field: FormlyFieldConfigCache) {
    reverseDeepMerge(field, {
      id: getFieldId(`formly_${this.formId}`, field, field.index),
      hooks: {},
      modelOptions: {},
      validation: { messages: {} },
      props:
        !field.type || !hasKey(field)
          ? {}
          : {
              label: '',
              placeholder: '',
              disabled: false,
            },
    });

    if (this.config.extras.resetFieldOnHide && field.resetOnHide !== false) {
      field.resetOnHide = true;
    }

    if (
      field.type !== 'formly-template' &&
      (field.template || field.expressions?.template || field.expressionProperties?.template)
    ) {
      field.type = 'formly-template';
    }

    if (!field.type && field.fieldGroup) {
      field.type = 'formly-group';
    }

    if (field.type) {
      this.config.getMergedField(field);
    }

    if (
      hasKey(field) &&
      !isUndefined(field.defaultValue) &&
      isUndefined(getFieldValue(field)) &&
      !isHiddenField(field)
    ) {
      assignFieldValue(field, field.defaultValue);
```

## Exact upstream excerpt K06 (lines 15–106)

```typescript
export class FormlyFormBuilder {
  constructor(
    private config: FormlyConfig,
    private injector: Injector,
    @Optional() private viewContainerRef: ViewContainerRef,
    @Optional() private parentForm: FormGroupDirective,
  ) {}

  buildForm(form: FormGroup | FormArray, fieldGroup: FormlyFieldConfig[] = [], model: any, options: FormlyFormOptions) {
    this.build({ fieldGroup, model, form, options });
  }

  build(field: FormlyFieldConfig) {
    if (!this.config.extensions.core) {
      throw new Error('NgxFormly: missing `forRoot()` call. use `forRoot()` when registering the `FormlyModule`.');
    }

    if (!field.parent) {
      this._setOptions(field);
    }

    disableTreeValidityCall(field.form, () => {
      this._build(field);
      // TODO: add test for https://github.com/ngx-formly/ngx-formly/issues/3910
      if (!field.parent || (field as FormlyFieldConfigCache).fieldArray) {
        // detect changes early to avoid reset value by hidden fields
        const options = (field as FormlyFieldConfigCache).options;

        if (field.parent && isHiddenField(field)) {
          // when hide is used in expression set defaul value will not be set until detect hide changes
          // which causes default value not set on new item is added
          options._hiddenFieldsForCheck?.push({ field, default: false });
        }

        options.checkExpressions?.(field, true);
        options._detectChanges?.(field);
      }
    });
  }

  private _build(field: FormlyFieldConfigCache) {
    if (!field) {
      return;
    }

    const extensions = Object.values(this.config.extensions);
    extensions.forEach((extension) => extension.prePopulate?.(field));
    extensions.forEach((extension) => extension.onPopulate?.(field));
    field.fieldGroup?.forEach((f) => this._build(f));
    extensions.forEach((extension) => extension.postPopulate?.(field));
  }

  private _setOptions(field: FormlyFieldConfigCache) {
    field.form = field.form || new FormGroup({});
    field.model = field.model || {};
    field.options = field.options || {};
    const options = field.options;

    if (!options._viewContainerRef) {
      defineHiddenProp(options, '_viewContainerRef', this.viewContainerRef);
    }

    if (!options._injector) {
      defineHiddenProp(options, '_injector', this.injector);
    }

    if (!options.build) {
      options._buildForm = () => {
        console.warn(`Formly: 'options._buildForm' is deprecated since v6.0, use 'options.build' instead.`);
        this.build(field);
      };

      options.build = (f: FormlyFieldConfig = field) => {
        this.build(f);

        return f;
      };
    }

    if (!options.parentForm && this.parentForm) {
      defineHiddenProp(options, 'parentForm', this.parentForm);

      if (!isSignalRequired()) {
        observe(options, ['parentForm', 'submitted'], ({ firstChange }) => {
          if (!firstChange) {
            options.detectChanges(field);
          }
        });
      }
    }
  }
}
```

## Exact upstream excerpt K140 (lines 331–354)

```typescript
export function getField(f: FormlyFieldConfig, key: FormlyFieldConfig['key']): FormlyFieldConfig {
  key = (Array.isArray(key) ? key.join('.') : key) as string;
  if (!f.fieldGroup) {
    return undefined;
  }

  for (let i = 0, len = f.fieldGroup.length; i < len; i++) {
    const c = f.fieldGroup[i];
    const k = (Array.isArray(c.key) ? c.key.join('.') : c.key) as string;
    if (k === key) {
      return c;
    }

    if (c.fieldGroup && (isNil(k) || key.indexOf(`${k}.`) === 0)) {
      const field = getField(c, isNil(k) ? key : key.slice(k.length + 1));
      if (field) {
        return field;
      }
    }
  }

  return undefined;
}

```

## Exact upstream excerpt K141 (lines 1–16)

```typescript
import { Component, ChangeDetectionStrategy } from '@angular/core';
import { FieldType, FieldGroupTypeConfig } from './field.type';

/** @ignore */
@Component({
  selector: 'formly-group',
  template: `
    <formly-field *ngFor="let f of field.fieldGroup" [field]="f"></formly-field>
    <ng-content></ng-content>
  `,
  host: {
    '[class]': 'field.fieldGroupClassName || ""',
  },
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class FormlyGroup extends FieldType<FieldGroupTypeConfig> {}
```

## Exact upstream excerpt K142 (lines 1–17)

```typescript
import { Directive } from '@angular/core';
import { FormArray } from '@angular/forms';
import { FieldType } from './field.type';
import { clone, assignFieldValue, getFieldValue, hasKey } from '../utils';
import { FormlyFieldConfig, FormlyExtension, FormlyFieldConfigCache } from '../models';
import { registerControl, unregisterControl, findControl } from '../extensions/field-form/utils';

export interface FieldArrayTypeConfig<T = FormlyFieldConfig['props']> extends FormlyFieldConfig<T> {
  formControl: FormArray;
  props: NonNullable<T>;
}

@Directive()
export abstract class FieldArrayType<F extends FormlyFieldConfig = FieldArrayTypeConfig>
  extends FieldType<F>
  implements FormlyExtension<F>
{
```

## Exact upstream excerpt K37 (lines 25–221)

```typescript
export class FormlyAttributes implements OnChanges, DoCheck, OnDestroy {
  /** The field config. */
  @Input('formlyAttributes') field: FormlyFieldConfig;
  @Input() id: string;

  private document: Document;
  private uiAttributesCache: any = {};
  private uiAttributes: string[];
  private focusObserver: IObserver<boolean>;

  /**
   * HostBinding doesn't register listeners conditionally which may produce some perf issues.
   *
   * Formly issue: https://github.com/ngx-formly/ngx-formly/issues/1991
   */
  private uiEvents = {
    listeners: [] as Function[],
    events: ['click', 'keyup', 'keydown', 'keypress', 'focus', 'blur', 'change'],
    callback: (eventName: string, $event: any) => {
      switch (eventName) {
        case 'focus':
          return this.onFocus($event);
        case 'blur':
          return this.onBlur($event);
        case 'change':
          return this.onChange($event);
        default:
          return this.props[eventName](this.field, $event);
      }
    },
  };

  private get props() {
    return this.field.props || ({} as FormlyFieldConfigCache['props']);
  }

  private get fieldAttrElements(): ElementRef[] {
    return (this.field as FormlyFieldConfigCache)?.['_elementRefs'] || [];
  }

  constructor(private renderer: Renderer2, private elementRef: ElementRef, @Inject(DOCUMENT) _document: any) {
    this.document = _document;
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes.field) {
      this.field.name && this.setAttribute('name', this.field.name);
      this.uiEvents.listeners.forEach((listener) => listener());
      this.uiEvents.events.forEach((eventName) => {
        if (this.props?.[eventName] || ['focus', 'blur', 'change'].indexOf(eventName) !== -1) {
          this.uiEvents.listeners.push(
            this.renderer.listen(this.elementRef.nativeElement, eventName, (e) => this.uiEvents.callback(eventName, e)),
          );
        }
      });

      if (this.props?.attributes) {
        observe(this.field, ['props', 'attributes'], ({ currentValue, previousValue }) => {
          if (previousValue) {
            Object.keys(previousValue).forEach((attr) => this.removeAttribute(attr));
          }

          if (currentValue) {
            Object.keys(currentValue).forEach((attr) => {
              if (currentValue[attr] != null) {
                this.setAttribute(attr, currentValue[attr]);
              }
            });
          }
        });
      }

      this.detachElementRef(changes.field.previousValue);
      this.attachElementRef(changes.field.currentValue);
      if (this.fieldAttrElements.length === 1) {
        !this.id && this.field.id && this.setAttribute('id', this.field.id);
        this.focusObserver = observe<boolean>(this.field, ['focus'], ({ currentValue }) => {
          this.toggleFocus(currentValue);
        });
      }
    }

    if (changes.id) {
      this.setAttribute('id', this.id);
    }
  }

  /**
   * We need to re-evaluate all the attributes on every change detection cycle, because
   * by using a HostBinding we run into certain edge cases. This means that whatever logic
   * is in here has to be super lean or we risk seriously damaging or destroying the performance.
   *
   * Formly issue: https://github.com/ngx-formly/ngx-formly/issues/1317
   * Material issue: https://github.com/angular/components/issues/14024
   */
  ngDoCheck() {
    if (!this.uiAttributes) {
      const element = this.elementRef.nativeElement as HTMLElement;
      this.uiAttributes = [...FORMLY_VALIDATORS, 'tabindex', 'placeholder', 'readonly', 'disabled', 'step'].filter(
        (attr) => !element.hasAttribute || !element.hasAttribute(attr),
      );
    }

    for (let i = 0; i < this.uiAttributes.length; i++) {
      const attr = this.uiAttributes[i];
      const value = this.props[attr];
      if (
        this.uiAttributesCache[attr] !== value &&
        (!this.props.attributes || !this.props.attributes.hasOwnProperty(attr.toLowerCase()))
      ) {
        this.uiAttributesCache[attr] = value;
        if (value || value === 0) {
          this.setAttribute(attr, value === true ? attr : `${value}`);
        } else {
          this.removeAttribute(attr);
        }
      }
    }
  }

  ngOnDestroy() {
    this.uiEvents.listeners.forEach((listener) => listener());
    this.detachElementRef(this.field);
    this.focusObserver?.unsubscribe();
  }

  toggleFocus(value: boolean) {
    const element = this.fieldAttrElements ? this.fieldAttrElements[0] : null;
    if (!element || !element.nativeElement.focus) {
      return;
    }

    const isFocused =
      !!this.document.activeElement &&
      this.fieldAttrElements.some(
        ({ nativeElement }) =>
          this.document.activeElement === nativeElement || nativeElement.contains(this.document.activeElement),
      );

    if (value && !isFocused) {
      Promise.resolve().then(() => element.nativeElement.focus());
    } else if (!value && isFocused) {
      Promise.resolve().then(() => element.nativeElement.blur());
    }
  }

  onFocus($event: any) {
    this.focusObserver?.setValue(true);
    this.props.focus?.(this.field, $event);
  }

  onBlur($event: any) {
    this.focusObserver?.setValue(false);
    this.props.blur?.(this.field, $event);
  }

  // handle custom `change` event, for regular ones rely on DOM listener
  onHostChange($event: any) {
    if ($event instanceof Event) {
      return;
    }

    this.onChange($event);
  }

  onChange($event: any) {
    this.props.change?.(this.field, $event);
    this.field.formControl?.markAsDirty();
  }

  private attachElementRef(f: FormlyFieldConfigCache) {
    if (!f) {
      return;
    }

    if (f['_elementRefs']?.indexOf(this.elementRef) === -1) {
      f['_elementRefs'].push(this.elementRef);
    } else {
      defineHiddenProp(f, '_elementRefs', [this.elementRef]);
    }
  }

  private detachElementRef(f: FormlyFieldConfigCache) {
    const index = f?.['_elementRefs'] ? this.fieldAttrElements.indexOf(this.elementRef) : -1;
    if (index !== -1) {
      f['_elementRefs'].splice(index, 1);
    }
  }

  private setAttribute(attr: string, value: string) {
    this.renderer.setAttribute(this.elementRef.nativeElement, attr, value);
  }

  private removeAttribute(attr: string) {
    this.renderer.removeAttribute(this.elementRef.nativeElement, attr);
  }
}
```

## Exact upstream excerpt K39 (lines 14–116)

```typescript
export function getFieldId(formId: string, field: FormlyFieldConfig, index: string | number) {
  if (field.id) {
    return field.id;
  }
  let type = field.type;
  if (!type && field.template) {
    type = 'template';
  }

  if (type instanceof Type) {
    type = type.prototype.constructor.name;
  }

  return [formId, type, field.key, index].join('_');
}

export function hasKey(field: FormlyFieldConfig) {
  return !isNil(field.key) && field.key !== '' && (!Array.isArray(field.key) || field.key.length > 0);
}

export function getKeyPath(field: FormlyFieldConfigCache): string[] {
  if (!hasKey(field)) {
    return [];
  }

  /* We store the keyPath in the field for performance reasons. This function will be called frequently. */
  if (field._keyPath?.key !== field.key) {
    let path: (string | number)[] = [];
    if (typeof field.key === 'string') {
      const key = field.key.indexOf('[') === -1 ? field.key : field.key.replace(/\[(\w+)\]/g, '.$1');
      path = key.indexOf('.') !== -1 ? key.split('.') : [key];
    } else if (Array.isArray(field.key)) {
      path = field.key.slice(0);
    } else {
      path = [`${field.key}`];
    }

    defineHiddenProp(field, '_keyPath', { key: field.key, path });
  }

  return field._keyPath.path.slice(0);
}

export const FORMLY_VALIDATORS = ['required', 'pattern', 'minLength', 'maxLength', 'min', 'max'];

export function assignFieldValue(field: FormlyFieldConfigCache, value: any) {
  let paths = getKeyPath(field);
  if (paths.length === 0) {
    return;
  }

  let root = field;
  while (root.parent) {
    root = root.parent;
    paths = [...getKeyPath(root), ...paths];
  }

  if (value === undefined && field.resetOnHide) {
    const k = paths.pop();
    const m = paths.reduce((model, path) => model[path] || {}, root.model);
    delete m[k];
    return;
  }

  assignModelValue(root.model, paths, value);
}

export function assignModelValue(model: any, paths: string[], value: any) {
  for (let i = 0; i < paths.length - 1; i++) {
    const path = paths[i];
    if (!model[path] || !isObject(model[path])) {
      model[path] = /^\d+$/.test(paths[i + 1]) ? [] : {};
    }

    model = model[path];
  }

  model[paths[paths.length - 1]] = clone(value);
}

export function getFieldValue(field: FormlyFieldConfig): any {
  let model = field.parent ? field.parent.model : field.model;
  for (const path of getKeyPath(field)) {
    if (!model) {
      return model;
    }
    model = model[path];
  }

  return model;
}

export function reverseDeepMerge(dest: any, ...args: any[]) {
  args.forEach((src) => {
    for (const srcArg in src) {
      if (isNil(dest[srcArg]) || isBlankString(dest[srcArg])) {
        dest[srcArg] = clone(src[srcArg]);
      } else if (objAndSameType(dest[srcArg], src[srcArg])) {
        reverseDeepMerge(dest[srcArg], src[srcArg]);
      }
    }
  });
  return dest;
```

## Exact upstream excerpt K41 (lines 120–377)

```typescript
      this.containerRef.clear();
      wrappers = this.field?.wrappers;
    }

    if (wrappers?.length > 0) {
      const [wrapper, ...wps] = wrappers;
      const { component } = this.config.getWrapper(wrapper);

      const ref = containerRef.createComponent<FieldWrapper>(component);
      this.attachComponentRef(ref, f);
      observe<ViewContainerRef & { _lContainer: any }>(
        ref.instance,
        ['fieldComponent'],
        ({ currentValue, previousValue, firstChange }) => {
          if (currentValue) {
            if (previousValue && previousValue._lContainer === currentValue._lContainer) {
              return;
            }

            const viewRef = previousValue ? previousValue.detach() : null;
            if (viewRef && !viewRef.destroyed) {
              currentValue.insert(viewRef);
            } else {
              this.renderField(currentValue, f, wps);
            }

            !firstChange && ref.changeDetectorRef.detectChanges();
          }
        },
      );
    } else if (f?.type) {
      const inlineType = this.form?.templates?.find((ref) => ref.name === f.type);
      let ref: ComponentRef<any> | EmbeddedViewRef<any>;
      if (inlineType) {
        ref = containerRef.createEmbeddedView(inlineType.ref, { $implicit: f });
      } else {
        const { component } = this.config.getType(f.type, true);
        ref = containerRef.createComponent<FieldWrapper>(component as any);
      }
      this.attachComponentRef(ref, f);
    }
  }

  private triggerHook(name: keyof FormlyHookConfig, changes?: SimpleChanges) {
    if (name === 'onInit' || (name === 'onChanges' && changes.field && !changes.field.firstChange)) {
      this.valueChangesUnsubscribe();
      this.valueChangesUnsubscribe = this.fieldChanges(this.field);
    }

    if (this.field?.hooks?.[name]) {
      if (!changes || changes.field) {
        const r = this.field.hooks[name](this.field);
        if (isObservable(r) && ['onInit', 'afterContentInit', 'afterViewInit'].indexOf(name) !== -1) {
          const sub = r.subscribe();
          this.hooksObservers.push(() => sub.unsubscribe());
        }
      }
    }

    if (name === 'onChanges' && changes.field) {
      this.resetRefs(changes.field.previousValue);
      this.render();
    }
  }

  private attachComponentRef<T extends FieldType>(
    ref: ComponentRef<T> | EmbeddedViewRef<T>,
    field: FormlyFieldConfigCache,
  ) {
    this.componentRefs.push(ref);
    field._componentRefs.push(ref);
    if (ref instanceof ComponentRef) {
      Object.assign(ref.instance, { field });
    }
  }

  private render() {
    if (!this.field) {
      return;
    }

    // require Formly build
    if (!this.field.options) {
      this.detectFieldBuild = true;

      return;
    }

    this.detectFieldBuild = false;
    this.hostObservers.forEach((hostObserver) => hostObserver.unsubscribe());
    this.hostObservers = [
      observe<boolean>(this.field, ['hide'], ({ firstChange, currentValue }) => {
        const containerRef = this.containerRef;
        if (this.config.extras.lazyRender === false) {
          firstChange && this.renderField(containerRef, this.field);
          if (!firstChange || (firstChange && currentValue)) {
            this.elementRef &&
              this.renderer.setStyle(this.elementRef.nativeElement, 'display', currentValue ? 'none' : '');
          }
        } else {
          if (currentValue) {
            containerRef.clear();
            if (this.field.className) {
              this.renderer.removeAttribute(this.elementRef.nativeElement, 'class');
            }
          } else {
            this.renderField(containerRef, this.field);
            if (this.field.className) {
              this.renderer.setAttribute(this.elementRef.nativeElement, 'class', this.field.className);
            }
          }
        }

        !firstChange && this.field.options.detectChanges(this.field);
      }),
      observe<string>(this.field, ['className'], ({ firstChange, currentValue }) => {
        if (
          (!firstChange || (firstChange && currentValue)) &&
          (!this.config.extras.lazyRender || this.field.hide !== true)
        ) {
          this.elementRef && this.renderer.setAttribute(this.elementRef.nativeElement, 'class', currentValue);
        }
      }),
    ];

    if (!isSignalRequired()) {
      ['touched', 'pristine', 'status'].forEach((prop) =>
        this.hostObservers.push(
          observe<string>(
            this.field,
            ['formControl', prop],
            ({ firstChange }) => !firstChange && markFieldForCheck(this.field),
          ),
        ),
      );
    } else if (this.field.formControl) {
      const events = ((this.field.formControl as any).events as Observable<any>).subscribe(() =>
        markFieldForCheck(this.field),
      );
      this.hostObservers.push(events);
    }
  }

  private resetRefs(field: FormlyFieldConfigCache) {
    if (field) {
      if (field._localFields) {
        field._localFields = [];
      } else {
        defineHiddenProp(this.field, '_localFields', []);
      }

      if (field._componentRefs) {
        field._componentRefs = field._componentRefs.filter((ref) => this.componentRefs.indexOf(ref) === -1);
      } else {
        defineHiddenProp(this.field, '_componentRefs', []);
      }
    }

    this.componentRefs = [];
  }

  private fieldChanges(field: FormlyFieldConfigCache | undefined) {
    if (!field) {
      return () => {};
    }

    const propsObserver = observeDeep(field, ['props'], () => field.options.detectChanges(field));
    let subscribes = [
      () => {
        propsObserver();
      },
    ];

    for (const key of Object.keys(field._expressions || {})) {
      const expressionObserver = observe<FormlyFieldConfigCache['_expressions']['key']>(
        field,
        ['_expressions', key],
        ({ currentValue, previousValue }) => {
          if (previousValue?.subscription) {
            previousValue.subscription.unsubscribe();
            previousValue.subscription = null;
          }
          if (isObservable(currentValue.value$)) {
            currentValue.subscription = currentValue.value$.subscribe();
          }
        },
      );
      subscribes.push(() => {
        if (field._expressions[key]?.subscription) {
          field._expressions[key].subscription.unsubscribe();
        }
        expressionObserver.unsubscribe();
      });
    }

    for (const path of [['focus'], ['template'], ['fieldGroupClassName'], ['validation', 'show']]) {
      const fieldObserver = observe(
        field,
        path,
        ({ firstChange }) => !firstChange && field.options.detectChanges(field),
      );
      subscribes.push(() => fieldObserver.unsubscribe());
    }

    if (field.formControl && !field.fieldGroup) {
      const control = field.formControl;
      let valueChanges = control.valueChanges.pipe(
        map((value) => {
          field.parsers?.map((parserFn) => (value = (parserFn as any)(value, field)));
          if (!Object.is(value, field.formControl.value)) {
            field.formControl.setValue(value);
          }

          return value;
        }),
        distinctUntilChanged((x, y) => {
          if (x !== y || Array.isArray(x) || isObject(x)) {
            return false;
          }

          return true;
        }),
      );

      if (control.value !== getFieldValue(field)) {
        valueChanges = valueChanges.pipe(startWith(control.value));
      }

      const { updateOn, debounce } = field.modelOptions;
      if ((!updateOn || updateOn === 'change') && debounce?.default > 0) {
        valueChanges = control.valueChanges.pipe(debounceTime(debounce.default));
      }

      const sub = valueChanges.subscribe((value) => {
        // workaround for https://github.com/angular/angular/issues/13792
        if (control._fields?.length > 1 && control instanceof FormControl) {
          control.patchValue(value, { emitEvent: false, onlySelf: true });
        }

        if (hasKey(field)) {
          assignFieldValue(field, value);
        }
        field.options.fieldChanges.next({ value, field, type: 'valueChanges' });
      });

      subscribes.push(() => sub.unsubscribe());
    }

    let templateFieldsSubs: (() => void)[] = [];
    observe(field, ['_localFields'], ({ currentValue }) => {
      templateFieldsSubs.forEach((unsubscribe) => unsubscribe());
      templateFieldsSubs = (currentValue || []).map((f: FormlyFieldConfigCache) => this.fieldChanges(f));
    });

    return () => {
      subscribes.forEach((unsubscribe) => unsubscribe());
      templateFieldsSubs.forEach((unsubscribe) => unsubscribe());
    };
```

