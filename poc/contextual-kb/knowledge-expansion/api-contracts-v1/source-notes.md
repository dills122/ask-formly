# Four bounded API contract source notes

Formly 6.3.12 only; pinned commit 5f099fddea6426b46a453866adf0fede5be0bcd7. All upstream bytes were fetched afresh and matched catalog hashes. Claims are source-derived paraphrases; exact source excerpts follow.

## field-type-accessor-relationships

FieldType.model returns this.field.model, and FieldType.formControl returns this.field.formControl with a TypeScript NonNullable cast; the getter does not construct a control or read formControl.value. FieldType.props returns this.field.props || {}: it returns the existing truthy props object by reference, or a new empty object on each access when props is falsy. The fallback is not assigned back to field.props. [K30](sources.md#k30)

Limit: These are core FieldType accessors for Formly 6.3.12. The model getter exposes the field model scope; it does not itself select model[field.key] or return the control value.
Limit: The formControl cast does not create a missing runtime value. A missing field.formControl can still be undefined; the props fallback does not initialize the field configuration.

## update-initial-value-optional-model

FormlyFormOptions declares updateInitialValue?: (model?: any) => void. Core root-option initialization installs options.updateInitialValue = (model?: any) => (options._initialModel = clone(model ?? field.model)) and immediately calls it without an argument. Calling the installed callback with no argument, undefined or null snapshots the root field.model through Formly clone; a supplied non-nullish value is cloned instead, including false, 0 or an empty string. This updates the stored initial model used by resetModel() when its model argument is nullish; updateInitialValue itself does not assign the live model, rebuild the form or reset controls. [K01](sources.md#k01) [K05](sources.md#k05) [K40](sources.md#k40)

Limit: This describes the callback installed during core root-option initialization, not a guarantee that an unbuilt options object already has the optional method.
Limit: Formly clone is not a universal deep-isolation guarantee: arrays and ordinary object values recurse, but several special values are returned unchanged, Set and Map are shallow copied, and AbstractControl becomes null. The public callback type is void; no public return-value contract is claimed.

## wrapper-lookup-missing-name

FormlyConfig.getWrapper(name: string | Type<FieldWrapper>): WrapperOption takes one argument. A component class accepted by the Type branch returns { component: name, name: name.prototype.constructor.name }; a registered string returns this.wrappers[name]. An unknown string throws a Formly Error saying the wrapper could not be found and should be registered through FormlyModule. getWrapper has no throwIfNotFound or error-suppression parameter. In contrast, getType(name, throwIfNotFound = false) returns null for an unknown type by default and throws when its second argument is true. [K150](sources.md#k150) [K71](sources.md#k71)

Limit: Do not transfer getType(name, false) to getWrapper(name, false): the latter is not the declared TypeScript API, and the wrapper implementation unconditionally throws on an unknown string.
Limit: The class-input branch does not establish that arbitrary values or application components satisfy the FieldWrapper contract.

## missing-preset-substitution-boundary

With PresetSubstitutionExtension installed, prePopulate only processes string field.type values beginning with '#'. It looks up the name matched by /^#(.+)$/ in FormlyConfig.presets. When that named preset is absent, the if (preset) body is skipped: substitution itself neither throws nor assigns to the field, so the original '#name' type remains. This does not guarantee successful rendering. Ordinary FormlyConfig.getType('#name') looks up that exact string in the type registry; it does not expand a preset or strip '#', returns null if the literal type is absent by default, and throws with throwIfNotFound true. The renderer uses getType(f.type, true) when no matching inline template is found, so an unresolved literal '#name' then fails type lookup unless that exact type is registered. [K44](sources.md#k44) [K71](sources.md#k71) [K41](sources.md#k41)

Limit: This is an absent named-preset substitution contract, not a promise that unknown presets are valid field types or silently render. A matching inline template is a separate renderer branch.
Limit: The substitution behavior requires the preset extension; ordinary type lookup alone never performs preset substitution. A registered literal type name beginning with # and a named preset are separate registry entries.

## Exact upstream excerpt K30 (lines 1–69)

```typescript
import { Input, Directive, QueryList, ViewChildren } from '@angular/core';
import { FormControl, NgControl, FormGroup } from '@angular/forms';
import { FormlyFieldConfig, FormlyFieldConfigCache } from '../models';
import { FieldWrapper } from './field.wrapper';

export interface FieldTypeConfig<T = FormlyFieldConfig['props']> extends FormlyFieldConfig<T> {
  formControl: FormControl;
  props: NonNullable<T>;
}

export interface FieldGroupTypeConfig<T = FormlyFieldConfig['props']> extends FormlyFieldConfig<T> {
  formControl: FormGroup;
  props: NonNullable<T>;
}

@Directive()
export abstract class FieldType<F extends FormlyFieldConfig = FormlyFieldConfig> {
  @ViewChildren(NgControl) set _formlyControls(controls: QueryList<NgControl>) {
    const f = this.field as FormlyFieldConfigCache;
    f._localFields = controls
      .map((c) => (c.control as FormlyFieldConfigCache['formControl'])._fields || [])
      .flat()
      .filter((f: FormlyFieldConfig) => f.formControl !== this.field.formControl);
  }

  @Input() field: F = {} as F;
  defaultOptions?: Partial<F>;

  get model() {
    return this.field.model;
  }

  get form() {
    return this.field.form;
  }

  get options() {
    return this.field.options;
  }

  get key() {
    return this.field.key;
  }

  get formControl() {
    return this.field.formControl as NonNullable<F['formControl']>;
  }

  get props() {
    return (this.field.props || {}) as NonNullable<F['props']>;
  }

  /** @deprecated Use `props` instead. */
  get to() {
    return this.props;
  }

  get showError(): boolean {
    return this.options.showError(this);
  }

  get id(): string {
    return this.field.id;
  }

  get formState() {
    return this.options?.formState || {};
  }
}
```

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

## Exact upstream excerpt K40 (lines 153–262)

```typescript
export function clone(value: any): any {
  if (
    !isObject(value) ||
    isObservable(value) ||
    value instanceof TemplateRef ||
    /* instanceof SafeHtmlImpl */ value.changingThisBreaksApplicationSecurity ||
    ['RegExp', 'FileList', 'File', 'Blob'].indexOf(value.constructor?.name) !== -1
  ) {
    return value;
  }

  if (value instanceof Set) {
    return new Set(value);
  }

  if (value instanceof Map) {
    return new Map(value);
  }

  if (value instanceof Uint8Array) {
    return new Uint8Array(value);
  }

  if (value instanceof Uint16Array) {
    return new Uint16Array(value);
  }

  if (value instanceof Uint32Array) {
    return new Uint32Array(value);
  }

  // https://github.com/moment/moment/blob/master/moment.js#L252
  if (value._isAMomentObject && isFunction(value.clone)) {
    return value.clone();
  }

  if (value instanceof AbstractControl) {
    return null;
  }

  if (value instanceof Date) {
    return new Date(value.getTime());
  }

  if (Array.isArray(value)) {
    return value.slice(0).map((v) => clone(v));
  }

  // best way to clone a js object maybe
  // https://stackoverflow.com/questions/41474986/how-to-clone-a-javascript-es6-class-instance
  const proto = Object.getPrototypeOf(value);
  let c = Object.create(proto);
  c = Object.setPrototypeOf(c, proto);
  // need to make a deep copy so we dont use Object.assign
  // also Object.assign wont copy property descriptor exactly
  return Object.keys(value).reduce((newVal, prop) => {
    const propDesc = Object.getOwnPropertyDescriptor(value, prop);
    if (propDesc.get) {
      Object.defineProperty(newVal, prop, propDesc);
    } else {
      newVal[prop] = clone(value[prop]);
    }

    return newVal;
  }, c);
}

export function defineHiddenProp(field: any, prop: string, defaultValue: any) {
  Object.defineProperty(field, prop, { enumerable: false, writable: true, configurable: true });
  field[prop] = defaultValue;
}

type IObserveFn<T> = (change: { currentValue: T; previousValue?: T; firstChange: boolean }) => void;
export interface IObserver<T> {
  setValue: (value: T, emitEvent?: boolean) => void;
  unsubscribe: Function;
}
interface IObserveTarget<T> {
  [prop: string]: any;
  _observers?: {
    [prop: string]: {
      value: T;
      onChange: IObserveFn<T>[];
    };
  };
}

export function observeDeep<T = any>(source: IObserveTarget<T>, paths: string[], setFn: () => void): () => void {
  let observers: Function[] = [];

  const unsubscribe = () => {
    observers.forEach((observer) => observer());
    observers = [];
  };
  const observer = observe(source, paths, ({ firstChange, currentValue }) => {
    !firstChange && setFn();

    unsubscribe();
    if (isObject(currentValue) && currentValue.constructor.name === 'Object') {
      Object.keys(currentValue).forEach((prop) => {
        observers.push(observeDeep(source, [...paths, prop], setFn));
      });
    }
  });

  return () => {
    observer.unsubscribe();
    unsubscribe();
  };
}
```

## Exact upstream excerpt K150 (lines 51–282)

```typescript
  addConfig(config: ConfigOption) {
    if (config.types) {
      config.types.forEach((type) => this.setType(type));
    }
    if (config.validators) {
      config.validators.forEach((validator) => this.setValidator(validator));
    }
    if (config.wrappers) {
      config.wrappers.forEach((wrapper) => this.setWrapper(wrapper));
    }
    if (config.validationMessages) {
      config.validationMessages.forEach((validation) => this.addValidatorMessage(validation.name, validation.message));
    }
    if (config.extensions) {
      this.setSortedExtensions(config.extensions);
    }
    if (config.extras) {
      this.extras = { ...this.extras, ...config.extras };
    }
    if (config.presets) {
      this.presets = {
        ...this.presets,
        ...config.presets.reduce((acc, curr) => ({ ...acc, [curr.name]: curr.config }), {}),
      };
    }
  }

  /**
   * Allows you to specify a custom type which you can use in your field configuration.
   * You can pass an object of options, or an array of objects of options.
   */
  setType(options: TypeOption | TypeOption[]) {
    if (Array.isArray(options)) {
      options.forEach((option) => this.setType(option));
    } else {
      if (!this.types[options.name]) {
        this.types[options.name] = <TypeOption>{ name: options.name };
      }

      (['component', 'extends', 'defaultOptions', 'wrappers'] as (keyof TypeOption)[]).forEach((prop) => {
        if (options.hasOwnProperty(prop)) {
          this.types[options.name][prop] = options[prop] as any;
        }
      });
    }
  }

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

  /** @ignore */
  getMergedField(field: FormlyFieldConfig = {}): any {
    const type = this.getType(field.type);
    if (!type) {
      return;
    }

    if (type.defaultOptions) {
      reverseDeepMerge(field, type.defaultOptions);
    }

    const extendDefaults = type.extends && this.getType(type.extends).defaultOptions;
    if (extendDefaults) {
      reverseDeepMerge(field, extendDefaults);
    }

    if (field?.optionsTypes) {
      field.optionsTypes.forEach((option) => {
        const defaultOptions = this.getType(option).defaultOptions;
        if (defaultOptions) {
          reverseDeepMerge(field, defaultOptions);
        }
      });
    }

    const componentRef = this.resolveFieldTypeRef(field);
    if (componentRef?.instance?.defaultOptions) {
      reverseDeepMerge(field, componentRef.instance.defaultOptions);
    }

    if (!field.wrappers && type.wrappers) {
      field.wrappers = [...type.wrappers];
    }
  }

  /** @ignore @internal */
  resolveFieldTypeRef(field: FormlyFieldConfigCache = {}): ComponentRef<FieldType> {
    const type: TypeOption & { _componentRef?: ComponentRef<any> } = this.getType(field.type);
    if (!type) {
      return null;
    }

    if (!type.component || type._componentRef) {
      return type._componentRef;
    }

    const { _viewContainerRef, _injector } = field.options;
    if (!_viewContainerRef || !_injector) {
      return null;
    }

    const componentRef = _viewContainerRef.createComponent<FieldType>(type.component, { injector: _injector });
    defineHiddenProp(type, '_componentRef', componentRef);
    try {
      componentRef.destroy();
    } catch (e) {
      console.error(`An error occurred while destroying the Formly component type "${field.type}"`, e);
    }

    return type._componentRef;
  }

  setWrapper(options: WrapperOption) {
    this.wrappers[options.name] = options;
    if (options.types) {
      options.types.forEach((type) => {
        this.setTypeWrapper(type, options.name);
      });
    }
  }

  getWrapper(name: string | Type<FieldWrapper>): WrapperOption {
    if (name instanceof Type) {
      return { component: name, name: name.prototype.constructor.name };
    }

    if (!this.wrappers[name]) {
      throw new Error(
        `[Formly Error] The wrapper "${name}" could not be found. Please make sure that is registered through the FormlyModule declaration.`,
      );
    }

    return this.wrappers[name];
  }

  /** @ignore */
  setTypeWrapper(type: string, name: string) {
    if (!this.types[type]) {
      this.types[type] = <TypeOption>{};
    }
    if (!this.types[type].wrappers) {
      this.types[type].wrappers = [];
    }
    if (this.types[type].wrappers.indexOf(name) === -1) {
      this.types[type].wrappers.push(name);
    }
  }

  setValidator(options: ValidatorOption) {
    this.validators[options.name] = options;
  }

  getValidator(name: string): ValidatorOption {
    if (!this.validators[name]) {
      throw new Error(
        `[Formly Error] The validator "${name}" could not be found. Please make sure that is registered through the FormlyModule declaration.`,
      );
    }

    return this.validators[name];
  }

  addValidatorMessage(name: string, message: ValidationMessageOption['message']) {
    this.messages[name] = message;
    if (typeof ngDevMode === 'undefined' || ngDevMode) {
      const deprecated = { minlength: 'minLength', maxlength: 'maxLength' } as any;
      if (deprecated[name]) {
        console.warn(
          `Formly deprecation: passing validation messages key '${name}' is deprecated since v6.0, use '${deprecated[name]}' instead.`,
        );
        this.messages[deprecated[name]] = message;
      }
    }
  }

  getValidatorMessage(name: string) {
    return this.messages[name];
  }

  private setSortedExtensions(extensionOptions: ExtensionOption[]) {
    // insert new extensions, grouped by priority
    extensionOptions.forEach((extensionOption) => {
      const priority = extensionOption.priority ?? 1;
      this.extensionsByPriority[priority] = {
        ...this.extensionsByPriority[priority],
        [extensionOption.name]: extensionOption.extension,
      };
    });
    // flatten extensions object with sorted keys
    this.extensions = Object.keys(this.extensionsByPriority)
      .map(Number)
      .sort((a, b) => a - b)
      .reduce(
        (acc, prio) => ({
          ...acc,
          ...this.extensionsByPriority[prio],
        }),
        {},
      );
  }

  private mergeExtendedType(name: string) {
    if (!this.types[name].extends) {
      return;
    }

    const extendedType = this.getType(this.types[name].extends);
    if (!this.types[name].component) {
      this.types[name].component = extendedType.component;
    }

    if (!this.types[name].wrappers) {
      this.types[name].wrappers = extendedType.wrappers;
    }
  }
```

## Exact upstream excerpt K71 (lines 98–116)

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

## Exact upstream excerpt K44 (lines 1–33)

```typescript
import { FormlyConfig, FormlyExtension, FormlyFieldConfig, ɵreverseDeepMerge } from '@ngx-formly/core';
export class PresetSubstitutionExtension implements FormlyExtension {
  constructor(private formlyConfig: FormlyConfig) {}

  prePopulate(field: FormlyFieldConfig): void {
    if (!(typeof field.type === 'string') || field.type[0] !== '#') {
      return;
    }
    const configId = new RegExp(/^#(.+)$/).exec(field.type)?.[1];
    const preset = this.formlyConfig.presets[configId];

    const { type: _, ...fieldConfigWithoutType } = field;
    if (preset) {
      const merged = ɵreverseDeepMerge(
        fieldConfigWithoutType,
        'getConfiguration' in preset ? preset.getConfiguration() : preset,
      );
      Object.assign(field, merged);
    }
  }
}

export function registerLibraryConfigReplacementExtension(formlyConfig: FormlyConfig) {
  return {
    extensions: [
      {
        name: 'libraryConfigReplacement',
        extension: new PresetSubstitutionExtension(formlyConfig),
        priority: -300,
      },
    ],
  };
}
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

## Verification limits

Graph coverage was checked for all seven relied-on source files. The graph generation is 2026-10-25T14:19:41Z and each new path is not_tracked; all behavior conclusions instead use direct reads of the fetched pinned sources. This package adds four facts only. No build, runtime, model, installed data, sealed evaluation or baseline changes were performed.
