# Registering and selecting a custom field type

In the pinned introduction demo, `FormlyModule.forRoot` registers a type named
`custom` with `component: CustomFieldType`. A field then selects it with
`type: 'custom'` [E15a](sources.md#e15a), [E15b](sources.md#e15b).

The same field has `key: 'custom'`, but `key` and `type` serve different
purposes: the public field config describes `key` as linking the field value
to the model, while a string `type` chooses a registered field type name.
Their equal strings in this example are incidental [E15b](sources.md#e15b),
[K01](sources.md#k01).
