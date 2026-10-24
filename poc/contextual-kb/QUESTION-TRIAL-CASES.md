# Source-format question trial: frozen prompts

These are developer-style questions for checking whether the **seeded facts**
carry enough accurate information to answer. This is a data-answerability check,
not a retrieval, ranking, MCP, or latency test. Assess each question from database
rows and their evidence, and report missing coverage rather than filling gaps from
general knowledge.

1. What is the best way to set a static default in Formly, and what changes when
   the model already has a value or the default is dynamic?
2. In Formly v6, how should I conditionally hide or disable a field, and what
   happens to the model value and control when a field is hidden?
3. I built a custom field component. How do I register and use it in a form, and
   is the field's `key` the same thing as its `type`?
4. Can I add my own property to `props` and expect a Material control to use it
   automatically?
5. Does `resetOnHide: false` keep the hidden control registered?
6. What differs between `options.resetModel()` and calling Angular's
   `form.reset()` directly?
7. If I return an Observable from a Formly `onInit` hook, who unsubscribes? What
   if I call `.subscribe()` myself?
8. Why might changing an expression from `templateOptions.disabled` to
   `props.disabled` alter behavior under a disabled parent?
9. Can I use a registered type's defaults and inheritance while overriding only
   one `props` value?
10. When do I need a Formly wrapper instead of a custom field type?

The original three user questions are represented by 1–4. Prompts 5–10 exercise
conditions and distinctions that a developer or coding agent could plausibly
look up. A pass requires all material qualifications, not just a matching title.
