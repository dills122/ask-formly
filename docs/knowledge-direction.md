# Direction for four knowledge slices

**Direction agreed 2026-10-28.** Refine the existing facts and retrieval first.
Examples, standards/patterns and repository knowledge are future slices; their
implementation remains deferred. This direction does not authorize new schemas,
storage, indexing, fact admission or installed DB changes.

## Responsibilities and authority

| Slice | Question it answers | Authority and scope | Status |
| --- | --- | --- | --- |
| Facts | What does Formly do, under which conditions? | Pinned library evidence, with version, adapter, conditions and limits | Active refinement |
| Examples and recipes | How could these capabilities be composed? | A particular implementation linked to supporting facts, assumptions and validation | Planned; isolated three-example candidate retained, further work deferred |
| Standards and patterns | How should our team or project approach this? | Adopted conventions and recommendations with explicit project/team scope, ownership and rationale | Idea; not yet planned, deferred |
| Custom fields and repository knowledge | What does our implementation do, and where is it used? | Repository code, configuration and tests tied to a known revision | Idea; not yet planned, deferred |

An example demonstrates an implementation. A recipe explains how its pieces fit
together. A pattern explains when an approach is useful, its tradeoffs and
alternatives. A team may adopt a pattern as a standard; adoption does not turn
it into universal Formly behavior. Repository observations describe what code
currently does, which can differ from the team's intended standard.

## Handling custom composition questions

A commonly used custom composition need not exist as an exact library fact.
For a stepper-style question, retrieve relevant library mechanisms such as model
scope, registration and validation, then distinguish a proposed application
composition from those supported behaviors. Add team conventions or observations
about the actual custom fields only when that context is available.

The answer should make clear which statements are library-supported, proposed,
project-prescribed or observed in code. A linked fact supports a specific part
of an example, not every line or the whole application. Missing a ready-made
recipe should not force either an invented library guarantee or refusal to help.
Unsupported behavior and assumptions still need to be explicit.

For now, the calling coding agent owns repository inspection and custom-field
analysis. It can combine that evidence with ask-formly's library facts. This does
not revive the retired application-inspection implementation or start a new
repository index inside ask-formly.

## Future retrieval boundaries

Keep the slices distinguishable in retrieval and provenance. Library lookup
should remain useful without project context. Project standards and repository
knowledge require explicit project/repository scope; one team's convention must
not silently become advice for another. A standard cannot override a library
contract, and a conflict between intended standards and observed code should be
reported rather than silently resolved.

Prefer small references in ordinary results and separate retrieval of detailed
examples or repository evidence when needed. The existing
[linked-example proposal](linked-examples.md) explores that direction; storage
choices and new APIs for the other slices remain undecided. Future design work
must address ownership, revision/freshness, access boundaries and validation
appropriate to each source of authority.

## First priority now

The first [library-support audit](https://github.com/dills122/ask-formly/blob/d3dff8f2641810aae39d6b6319f0efecbd43c54f/docs/library-support-audit.md) is complete. Focused
questions retrieved the existing support; the next retrieval work should address
broad-plan conditional coverage and its recorded historical regression. The
scope and evaluation principles below continue to govern that work.

Run a bounded library-support and retrieval audit using the remaining broad
requests. Start with G2's model-scope, registration and key-path distinctions,
using the custom stepper as context rather than requiring a complete stepper
recipe. Include natural-language paraphrases and weak/unknown matches to test
whether callers can find useful evidence and state its limits.

Before tuning, freeze a supplemental rubric that separates:

- Existing essential library support that should be retrieved.
- Conditional evidence needed only for a particular design branch.
- Proposed application composition that should be labelled as such.
- Actual unsupported library behavior or missing project context.

Preserve previous frozen rubrics and failed historical counts. Assess evidence
delivery, bounded recovery cost and fresh-answer quality separately. Success is
finding the required existing facts within agreed budgets, preserving their
conditions and provenance, and avoiding unsupported guarantees. It is not
matching every old expected ID or having a ready-made custom implementation.

Then address measured retrieval losses and propose the small factual-clarification
package already identified: changed-model rebuild conditions and the shared-key
hide exception. Record source evidence and proposed wording before seeking
authorization to change locked facts. Keep the facts and installed DB unchanged
during retrieval work.

Revisit the deferred slices after the remaining fact/retrieval findings have
explicit dispositions and the caller workflow has been reviewed. Resuming one
slice requires a separate scoped decision; completing this audit does not
automatically start all three. See the [current backlog](knowledge-completion-backlog.md).

The [recipe construction and storage contract](recipe-construction.md) refines
step-level support, revision identity and separate review/execution/promotion
states. It remains a deferred design; caller answers are not automatically
stored as recipes.
