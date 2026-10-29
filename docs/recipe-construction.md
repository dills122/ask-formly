# Recipe construction and storage direction

**2026-10-28 — proposed contract; implementation remains deferred.** Recipes
belong with the examples slice in the [four-slice direction](knowledge-direction.md).
They are not a fifth primitive or a prerequisite for answering a new question.
No schema, compiler, retrieval API or installed DB changes are authorized by this
note. The existing [example storage proposal](linked-examples.md) remains the
starting point.

## What we would store

A fact states a supported library mechanism. A recipe proposes a sequence for a
goal, including ordering, assumptions and application choices. An example
implements an approach in concrete code. Correct individual facts do not prove
that a composition works.

A reusable recipe needs a stable ID, immutable behavior revision, goal, scope,
ordered steps, alternatives and limitations. Each step needs:

- An action and dependencies on earlier steps.
- Mechanism claims linked to exact fact revisions or a pinned fact snapshot,
  explaining which clause each fact supports and inheriting its conditions.
- Application choices distinguished from library contracts.
- Required context and assumptions, including model shape, initialized state,
  dependency versions and project-specific implementation requirements.
- Expected results and links to the precise assertions that have tested them.

External dependency evidence, project observations and team standards must retain
separate authority and scope. A Formly fact does not qualify every Angular version
or custom widget. Composition scope must satisfy all relevant conditions; combining
fact scopes must not broaden compatibility. Conflicts require explicit branches
or rejection.

## Review, execution and promotion are different

Keep authored maturity, execution evidence, release state and freshness separate.
A reviewed recipe can be unexecuted. A passing fixture does not imply installation
or universal compatibility. Avoid a single verified flag.

Execution records should bind exact dependency versions, platform, code/fixture
hashes, command, individual assertions and results. Preserve failures. A rerun of
unchanged content appends evidence; it need not change the recipe's content ID.
Changing ordering, assumptions, scope, linked semantics or code creates a new
behavior revision. Changed dependencies flag affected recipes for review and
relevant retesting, without rewriting old evidence.

## Storage and retrieval

Prefer reviewable authored manifests, explanatory text and optional code files in
Git, compiled into an immutable release snapshot. The existing proposal favors
a combined fact/example snapshot; recipes can extend that design when resumed.
Choose the precise file/schema split during implementation design. Do not add
ad-hoc tables to the installed schema2 DB.

Validate reference targets, support maps, dependency guards, safe paths, hashes
and execution bindings. Search indexes and reverse fact-to-recipe links are
derived data. A separate knowledge pack would need an exact fact-snapshot binding.
Do not mix recipe text into fact ranking without a separate measured design.

Ordinary fact responses should contain small scoped references. Retrieve selected
recipe detail and example code separately, with bounded responses and explicit
revisions. Never silently truncate a step or file. Package portable verification
summaries; large external logs can be referenced by digest. Serving must not depend
on machine-local audit paths.

## Curation boundary

A caller can propose a one-off solution without storing a recipe. Do not
persist every generated answer: it may contain private context, unsupported
assumptions or duplicate advice. Curate a reusable candidate only for a recurring
need or deliberate coverage goal, removing private details and reviewing support,
scope and execution evidence before promotion.

For now, test whether callers can compose unfamiliar answers from existing facts.
Recipe storage must not become a way to memorize the audit questions. Further
implementation remains deferred until the facts/retrieval work has clear
outcomes and the slice is explicitly resumed.
