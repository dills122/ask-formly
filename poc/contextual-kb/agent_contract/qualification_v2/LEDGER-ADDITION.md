
### Mandatory ledger completion audit

A condition may be part of the requested information and still need a ledger binding. After constructing each question and its paired ledger, inspect the applicable source context for three easily missed categories:

- Stage or timing of the inquiry: initialization, after construction, before/after a stated change, or another supplied stage. Preserve the meaningful stage excerpt and bind it to each question it governs, even when the question already mentions it.
- Supplied method or channel: how the change or operation occurs, such as through a model update rather than a user interaction. Bind the supplied method to that operation; the state binding alone does not cover the method. Do not invent a method when only an outcome is requested.
- Explicit restrictions on the lookup or result: including prohibitions on substituting or correcting a supplied API name, not just restrictions on implementation techniques. Carry the restriction in the standalone question and bind its meaningful exact source excerpt. Merely keeping the target name is not a complete record of an explicit no-substitution restriction.

Treat these as ordinary mandatory conditions under the existing scope rules, not as new fields or separate library questions. A larger verbatim excerpt can cover multiple conditions only when it actually includes their meaning and applies to all listed questions. Check the ledger itself for coverage; a condition present only in prose or a reason is still missing from the ledger. Keep the exact source excerpt in each bound question. Do not manufacture ledger entries for unspecified stages/methods, mere requested target names, corrected-away facts, or irrelevant application work. Preserve all settled shared-context and support-caveat allowances. This internal audit changes no output schema and emits no reasoning transcript.
