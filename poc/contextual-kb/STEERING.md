# Shared vocabulary and working boundaries

Updated: 24 October 2026. This is the current steering agreement for this POC.
Use these names in discussion, plans, code explanations, tests, and reports.
Proposed changes to the agreement must be explicit; historical reports do not
silently change current scope.

## Hard requirements

1. **Self-contained POC.** The implementation boundary is `poc/contextual-kb/`.
   This is a fresh POC, not an integration of earlier implementations. Outside
   code may be inspected for understanding, but must not be imported, copied
   into this implementation, linked, or wired in as a runtime dependency.
   This includes other repository POCs and the portable skill implementation.
   Established third-party libraries remain candidates for the requested
   library-based experiment; that does not authorize reuse of outside project
   code. Existing knowledge provenance is not permission to import code.
2. **Data/DB layer is locked. DO NOT CHANGE OR EDIT IT.** This includes authored
   knowledge, corpus/evidence inputs, compilation and seeding code, schema,
   stored records, generated database, and stored search index. Do not rebuild,
   reseed, migrate, or repair them during this work. Read-only inspection is
   allowed. Report discovered problems; changing them requires explicit user
   authorization. Older text permitting source corrections does not override
   this lock.
3. **Accepted foundation.** This POC is now the primary library MCP. The
   accepted planner, wording adapter, advisory GLiNER extraction, full-question
   retrieval and bounded selection/stdio service remain frozen during cleanup.
   Repository maintenance may update setup, checks and history; it does not
   authorize data/DB changes, retraining or replacement of runtime components.
4. Preserve frozen trial evidence. Write new results separately under the
   repository's `test-output/`, as required by repository guidance.

## Project names and scope

| Term | Meaning here |
| --- | --- |
| ask-formly repository | The repository for this accepted library MCP; older implementations are archived. |
| Portable skill | Retired implementation; remaining reference documents are frozen knowledge provenance. |
| This POC / contextual KB POC | Only `poc/contextual-kb/`. KB means knowledge base. |
| Knowledge baseline | The existing authored Formly 6.3.12 core/Material knowledge. Current reports record 9 documents and 46 facts; this is a bounded sample, not all Formly knowledge. |
| Calling agent | The consumer that asks the knowledge service a question and eventually explains the result to the user. |
| MCP boundary | The accepted local stdio `lookup_formly` interface; bounded existing-checkout qualification, not production or whole-library coverage. |

## Layers and responsibilities

The intended request flow is:

```text
calling agent / MCP input
    -> question layer -> retrieval plan
    -> retrieval -> candidate facts
    -> evidence selection / assessment -> evidence packet
    -> answer assembly -> final answer
```

The data/DB layer supplies stored knowledge to the downstream read path.
These are responsibility boundaries, not a claim that each already has a
separate module or a qualified implementation.

| Layer | Responsibility | Current permission |
| --- | --- | --- |
| Data/DB layer | Knowledge inputs, validated records, compilation, seeding, schema, database, and stored search index. | Locked; read only. |
| Question layer / question planner | Interpret the user's requested information and produce structured search requests while preserving context. | The only active implementation area. |
| Retrieval layer / retrieval engine | Execute searches, rank or rerank matches, and follow configured links to return candidates. | Existing behavior held fixed. |
| Evidence selection | Choose retrieved material for a bounded packet. | Outside current scope. |
| Evidence assessment | Judge whether evidence supports requested aspects, including conditions and gaps. | Outside current scope. |
| Packet construction | Serialize selected original claims, qualifications, and provenance for a consumer. | Outside current scope. |
| Answer assembly | Compose the final explanation from evidence and communicate limitations. | Outside current scope. |

The existing `kbcompiler/question_layer.py` spans more than the agreed question
layer: `QueryPlanner` queries the DB, `QueryProbe` contains fact IDs, and
`QuestionLayer.query` selects retrieved candidates. Its filename is not the
scope definition. The new planner's conceptual output is a retrieval plan,
not selected fact IDs or an answerability verdict. Exact schema remains to be
designed; this vocabulary does not approve an implementation design.

## Question and retrieval terminology

| Term | Meaning here |
| --- | --- |
| Question | The complete original user input, retained verbatim. |
| Requested aspect / ask | One requested piece of information. Prefer “requested aspect”; “ask” is shorthand. Historical trials also call these obligations. |
| Shared question context | Conditions, entities, relationships, and scope applying to multiple aspects. Distinct from a stored fact's search context. |
| Condition | A circumstance under which an aspect is being asked, such as “when hidden” or `resetOnHide: false`. |
| Negation | A negative constraint or proposition whose attachment must be preserved, such as “without application persistence code.” |
| Exact identifier | User-supplied API spelling or code token that must survive planning, such as `options.formState`, `resetOnHide`, or `FormControl`. |
| Literal | A supplied value or code fragment, such as `false`, `0`, or `'passwordBox'`; preserve its relationship to the relevant identifier. |
| Decomposition | Representing distinct requested aspects with their context and relationships. Splitting text alone does not establish correct decomposition. |
| Literal span | An exact substring of the question. A span is not necessarily a meaningful or complete requested aspect. |
| Retrieval plan | Structured question-layer output describing what to search for, with aspects, context, identifiers, and search requests. Contains no generated Formly advice. |
| Search request / query | An executable request to the existing retrieval interface. One aspect can require more than one request. |
| Lexical probe | A focused text-search request. In the current implementation this is an FTS5 expression; the legacy probe object also holds hits. |
| Hybrid retrieval | The existing combination of lexical and dense retrieval. It is downstream of question interpretation. |
| Candidate fact | A retrieved record that may be relevant. A match is not a verified answer. |
| Evidence packet | Selected source-linked facts and their qualifications returned to a consumer. |
| Planning ambiguity | Uncertainty about what the user means. Distinct from an evidence gap, which concerns available support. |
| Evidence gap / unresolved support | A requested aspect for which adequate evidence has not been established. A planner alone cannot establish corpus answerability. |

For “If I hide a field with `resetOnHide: false`, what happens to its value and
its `FormControl`?”, value and control are distinct requested aspects. Both
retain the hiding condition and `resetOnHide: false`. This describes the
question; it does not assert either Formly outcome.

## Formly domain vocabulary

These entries identify what we are discussing, not exhaustive behavioral
claims. Behavioral conclusions must be grounded in pinned Formly source.

| Term | Meaning in our discussions |
| --- | --- |
| Field configuration | The configuration describing a Formly field, commonly represented by `FormlyFieldConfig`. Distinct from its rendered component or Angular control. |
| Model / model value | Application data associated with the form/field. Distinct from the field configuration and control object. |
| Key / model path | The field's configured address into model data. Keep this distinct from its renderer type name. |
| Angular control | A reactive-forms object such as `FormControl`, `FormGroup`, or `FormArray`. “Control” does not automatically mean the visible widget. |
| Field type / renderer | A Formly rendering implementation selected through type configuration. Distinct from a TypeScript type. |
| Type name / registration | A configured name and its registration connecting it to a Formly type implementation/options. User-defined names are not universal Formly APIs. |
| Wrapper | A Formly component surrounding/decorating a field renderer; discuss separately from the renderer and value-accessor bridge. |
| Props | Field properties under `props`; preserve exact property paths when present. |
| Expression | A dynamic field configuration expression. Keep `expressions` and legacy `expressionProperties` distinct. |
| Hook | A configured lifecycle callback. Do not conflate hooks with expressions. |
| Form state | `options.formState`, used as a distinct term from model data or Angular control state. The name alone makes no persistence guarantee. |
| Default value | The `defaultValue` configuration, distinct from a supplied model value. Its application conditions require evidence. |
| Hidden / disabled | Separate field states and separate requested behaviors. Do not treat hiding, disabling, value removal, and control removal as synonyms. |
| UI adapter | A Formly UI integration, such as Material. Core and adapter-specific behavior must remain distinguishable. |
| Value accessor | The Angular control-to-widget value bridge. Keep it distinct from a wrapper. |

## Knowledge and evaluation vocabulary

| Term | Meaning here |
| --- | --- |
| Authored fact | A controlled record containing a claim, conditions, limits, context, and provenance. “Authored” does not itself prove semantic correctness. |
| Claim | The statement a fact makes. |
| Fact context | Stored retrieval-oriented text; not additional authoritative evidence. |
| Qualification | A condition or limit that must travel with a claim. |
| Provenance / citation | A trace to source material. Valid provenance alone does not establish that the source supports a claim. |
| Bake-off / comparison arm | A controlled comparison / one candidate approach within it. |
| New approach | A meaningfully different question-interpretation mechanism using established libraries where useful. More regex tuning, word pairs, or literal splitting does not qualify by renaming it. |
| Diagnostic cases | Previously exposed questions, retained to understand regressions and known failures. |
| Held-out cases | Questions and expected aspects reserved from implementation/tuning for the scored decision. |
| Plan quality | Coverage of requested aspects, preservation of conditions/negation/identifiers/relationships, and usability of search requests. |
| Fact coverage | Whether retrieval found a specified set of records; distinct from plan quality and answer correctness. |
| Answer accuracy | Whether the final explanation is correct, complete, and qualified. Plan scores cannot establish it. |
| Planning latency | Time spent producing the plan; measure cold setup and warm requests separately. |
| End-to-end latency | Time across the complete request-to-final-answer path. The historical 25-second target is not an agreed planner budget. |

The next experiment requires at least two meaningfully different library-based
question approaches, TDD, and independent review checkpoints. Library selection,
the output schema, and the planner latency budget remain open. A library's role
must be stated precisely; adding a dependency is not evidence of better planning.
