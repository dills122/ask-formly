# Expanded source-format and question trial

## Boundary and method

This trial expanded the controlled source set from two topic files and 13 facts
to seven topic files and 41 facts. The added records cover props, registered
types, a real type-use example, wrappers, Material boundaries, expression
callbacks, disabled paths, and hook subscription ownership. The authored JSON
is the controlled input; the compiler lints it and seeds the SQLite database.
There were no edits to generated database rows.

The ten [frozen developer questions](QUESTION-TRIAL-CASES.md) were assessed by
reading known fact IDs from the seeded database, including claims, conditions,
limits, source quotes, links, and evidence records. This checks whether the data
can support a concise answer. It does **not** test question-to-fact retrieval,
ranking, an MCP response, or an agent's final answer. The [machine report](../../test-output/contextual-kb-expanded-source-trial.json)
records the fact IDs used for each question and the reproducibility checks.

## Build and source checks

- Structural lint accepted all seven authored files. A new regression test first
  reproduced a rejection of descriptive citation labels such as
  `[Fields](sources.md#e09a)`; the validator now checks the exact link target
  regardless of its label and still rejects a wrong target.
- The isolated suite passed **35 tests**. Older fact-trial tests emitted
  `ResourceWarning` messages for unclosed SQLite connections; they still passed.
- The read-only audit found **41 facts**, **41 exact source spans**, **16 cited
  evidence records**, **55 fact-evidence links**, and **25 resolved `see_also`
  links**. SQLite integrity and foreign-key checks passed.
- A second build into an empty temporary directory was logically identical to
  the active database across all six tables. All 16 cited evidence files matched
  their catalog hashes in the pinned local source/reference snapshot.
- The pinned-source check caught two Material facts whose K16/K17 evidence IDs
  were reversed. Their citations were corrected before the final seed and audit.

These checks establish reproducible structure and provenance. The compiler does
not certify that natural-language claims are entailed by source code. For this
trial, the new claims were compared with their exact source passages; the
registration, merge, expression, hook, and Material boundary claims received
targeted checks against pinned Formly v6 code and examples.

A bounded, read-only second-eye check found no concrete defect in the new
source quotes, evidence IDs, compiler citation test, or question ratings. It
was a check of this trial's stated scope, not a full readiness review.

## Question answerability from the seeded records

`Supported` means the selected rows contain the material answer and caveats.
`Partial` means a developer would need additional knowledge beyond this seed.
These are manual data-coverage judgments, **not** measured retrieval or agent
accuracy results.

| Question | Result | What the facts support or lack |
| --- | --- | --- |
| 1. Static versus dynamic defaults | **Partial** | A keyed `defaultValue` applies when the value is undefined and eligible; defined values are retained. The selected seeded records do not provide a sourced dynamic-default strategy. |
| 2. Conditional hide/disable | **Supported** | Modern `expressions` supports `hide` and `props.disabled` targets with a field callback. Hiding can unregister a control and, with reset-on-hide, remove the model value. |
| 3. Register and use a custom type; `key` versus `type` | **Partial** | A component needs `types` registration; a field's `type` selects the registered name, while `key` concerns the model. The seed points to the password registration/use example but does not carry a complete component-registration recipe or an explicit key-to-model explanation in its compact claims. |
| 4. Extra custom `props` | **Supported** | Extra props are permitted by the type shape, but that does not make a Material control consume them; custom Material integration has its own contract. |
| 5. `resetOnHide: false` | **Supported** | It skips the value-clearing branch; it does not promise the hidden control remains registered. |
| 6. Formly reset versus `form.reset()` | **Supported** | `updateInitialValue()` captures a baseline; `resetModel()` restores it or an explicit model, rebuilds, and resets controls. Raw `form.reset()` is not established as equivalent. |
| 7. `onInit` subscription ownership | **Supported** | A returned Observable is managed by Formly's field component; a manually created subscription needs its own cleanup. |
| 8. Disabled expression path migration | **Supported** | In v6.3.12, the evaluator combines ancestor disabled state with `props.disabled`, but not the legacy target path; both paths still update disabled controls. |
| 9. Inherited defaults and partial `props` | **Supported** | Registration supports inheritance/defaults, and reverse deep merge fills missing values. Complex precedence still needs checking against `getMergedField`. |
| 10. Wrapper versus type | **Supported** | A wrapper decorates and needs a field insertion point; it does not provide a missing control. The Material wrapper owns `mat-form-field`. |

**Result: 8 supported, 2 partial, 0 unsupported claims identified in these
question packets.** The two partials are visible source/record coverage gaps;
they are not compiler or database failures. Retrieval and answer generation were
outside this data trial.

The later [direct DB query trial](DB-QUERY-TRIAL.md) adds records addressing
these two content gaps and tests explicit search terms against the rebuilt seed.
The results above remain the frozen seven-file baseline.
