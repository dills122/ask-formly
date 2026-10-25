# Proposed custom-type knowledge source

Status: draft for review; not installed. Formly 6.3.12. Statements below are authored summaries, not upstream quotations. Exact upstream excerpts and archive verification are in source-evidence.json. Conditions and limits travel in the accompanying draft facts.

## custom-control-template

The pinned custom-input example extends FieldType<FieldTypeConfig> and binds its input to the Formly-provided formControl with [formControl]="formControl" and to the field with [formlyAttributes]="field". [K65](sources.md#k65) [K66](sources.md#k66)

## attributes-directive-purpose

The formlyAttributes directive links field HTML attributes and events, such as id, name, focus and blur, to a DOM element. [K67](sources.md#k67)

## ngmodule-declaration-and-imports

The pinned introduction NgModule imports ReactiveFormsModule and FormlyModule.forRoot configuration, declares CustomFieldType, and registers its string alias in types with component: CustomFieldType. [K68](sources.md#k68)

## scalar-and-group-control-types

FieldTypeConfig narrows formControl to FormControl, while FieldGroupTypeConfig narrows it to FormGroup; both make props non-nullable. [K69](sources.md#k69)

## component-reference-or-alias

A field configuration can pass the component class directly as type, or use a registered string alias; a string alias must be registered, while the direct component route does not require that alias. [K70](sources.md#k70) [K71](sources.md#k71)

## root-and-child-configuration

FormlyModule.forRoot and forChild both accept ConfigOption and contribute FORMLY_CONFIG; forRoot additionally provides FormlyConfig, and the module constructor adds the supplied configurations to the injected configuration service. [K72](sources.md#k72)

## unknown-string-type

For an unregistered string type name, FormlyConfig.getType returns null by default and throws a registration error when throwIfNotFound is true. [K71](sources.md#k71)

## registered-wrapper-fallback

In getMergedField, registered type wrappers are copied to field.wrappers only when field.wrappers is falsy; an existing empty array does not take that fallback. [K73](sources.md#k73)

## material-input-pattern

The pinned Material input extends FieldType from @ngx-formly/material/form-field, uses matInput with formControl and formlyAttributes bindings, and its module registers input with the form-field wrapper. [K74](sources.md#k74) [K75](sources.md#k75)

## public-registration-type

The core public barrel exports ConfigOption but does not export TypeOption; the element type for registrations can be derived as NonNullable<ConfigOption['types']>[number]. [K76](sources.md#k76) [K77](sources.md#k77) [K78](sources.md#k78)
