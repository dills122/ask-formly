# Question plan contract — A/B design v1

Status: preimplementation review target, 21 October 2026. Governed by
[STEERING.md](STEERING.md). No planner implementation is authorized by this
document alone. The comparison protocol is [QUESTION-PLAN-EVALUATION.md](QUESTION-PLAN-EVALUATION.md).

## Boundary

Input is one complete question. Output describes requested information and
search requests, never retrieved facts, evidence support, or Formly answers.
Planning reads no database, authored facts, catalog, or corpus. Existing
retrieval and the data/DB layer remain untouched. All new project code must
live inside this POC; third-party packages are permitted, other project code
is not imported or copied.

Arm A uses spaCy's trained dependency parser and syntactic relationships.
Arm B uses LlamaIndex's standalone LLMQuestionGenerator with an explicitly
configured local model and one search-tool description. No query engine,
retriever, agent loop, or response synthesizer is instantiated. Tool metadata
describes a search capability, not corpus contents or inferred answerability.
The exact library and model versions are frozen after compatibility checks
on development examples only, before the held-out run.

## Input

`question`: string, preserved byte-for-byte when UTF-8 serialized. Accept
1–8,000 Unicode codepoints and reject whitespace-only text. No normalization
of the original string. The original wording is available to every request.
No default version or adapter is inserted into the user's question.

## Output shape

This is a language-neutral specification, not implemented types. All fields
are required unless explicitly nullable. Unknown fields are rejected.

| Field | Type and meaning |
| --- | --- |
| `schema_version` | Literal `1`. |
| `question` | Exact original string. |
| `status` | `planned`, `ambiguous`, or `failed`. Describes planning only. |
| `aspects` | List of 0–8 aspect objects. |
| `requests` | List of 0–8 search-request objects. |
| `ambiguities` | List of 0–8 ambiguity objects. |
| `failure` | Null or `{code, detail}`. Codes: `invalid_input`, `capacity_exceeded`, `timeout`, `backend_error`, `invalid_output`. Detail is bounded to 1,000 codepoints. |

Aspect: `{id, requested_information, source_spans}`. IDs are `a1` through `a8`
in output order; requested_information is a nonempty string of at most 2,000
codepoints describing an ask, without answering it. `source_spans` is a list
of 0–16 half-open `[start, end]` Unicode-codepoint offsets into the question.
Spans, when supplied, must be exact and in bounds; they are optional evidence
of attribution, not a requirement to copy literal fragments as aspects.

Search request: `{id, aspect_ids, query, context}`. IDs are `q1` through `q8`;
aspect_ids is a nonempty list of existing aspect IDs; query is a nonempty
natural-language string of at most 2,000 codepoints; context equals the whole
original question. Each aspect has at least one request. One request may
serve multiple aspects only if it explicitly covers them. The context field
is mandatory for both arms and is not a claim that context was interpreted.

Ambiguity: `{description, aspect_ids}`. Description is nonempty, at most 1,000
codepoints; aspect_ids may be empty for whole-question ambiguity. Record
uncertainty about meaning, not absence of supporting facts. Alternatives may
be described here without inventing an answer or silently choosing one.

`planned` requires 1–8 aspects, 1–8 requests, no failure, and no ambiguities.
`ambiguous` requires at least one ambiguity, no failure, and may contain
bounded aspects/requests for unambiguous portions. `failed` requires a failure
and empty aspects, requests, and ambiguities. Partial diagnostic output goes
in the run trace, never a successful plan. Capacity overflow must fail, not
truncate. Input rejection echoes the input but does not bypass input validation.

## Semantic obligations, separate from structural validity

For every aspect and query, its wording together with original context must
preserve the intended target, relevant conditions, negation, comparisons,
relationships, exact API names, and literal values. Merely placing the full
question in `context` earns no semantic credit: graders inspect the focused
query for omission, contradiction, and ambiguous reference.

The focused query must restate the material conditions and exact identifiers
needed to stand alone. It may paraphrase ordinary language, resolve an
unambiguous pronoun, or repeat shared context. It may not add a Formly
prescription, convert a question's premise into established truth, or guess
an unmentioned API. A supplied identifier cannot be silently corrected.
An identifier needed by multiple requests must be preserved in each.

Do not require a particular number or wording of aspects if an alternative
partition preserves all distinct requested information. Gold rubrics identify
independently searchable outcomes and permissible combinations. Independently
searchable outcomes require distinct aspects and focused requests; a request
may combine outcomes only where the rubric marks them inseparable. A single
verbatim whole-question echo fails a multi-ask case requiring separation, as
does repeating the broad question under several IDs. A single-aspect
question should not gain invented subquestions.

Example (exposed design example, never held out):

Question: “If I hide a field with resetOnHide: false, what happens to its value
and its FormControl?”

- Aspect 1: effect on model value; query: “When a field is hidden with
  resetOnHide: false, what happens to its model value?”
- Aspect 2: effect on control; query: “When a field is hidden with
  resetOnHide: false, what happens to its FormControl?”

These are target outputs for evaluation, not observed library outputs. They
make no claim about the answers. `source_spans` may be empty for either arm.

## Fair adaptation and execution

Both arms use the same nonsemantic serializer/validator. It may assign IDs,
copy original context, enforce bounds, validate references, and reject
malformed output. It cannot repair a missing condition or add an aspect.

Arm A must use actual trained parse relationships to construct requests;
no import of existing regex/word-pair/literal-span planners, and no growing
Formly synonym or question-specific rule table. General syntax-to-request
rules are arm A's implementation and must be disclosed and reviewed.

Arm B uses the native SubQuestion fields with one recognized tool name,
`formly_search`. The prompt requires `sub_question` to start with exactly
`SEARCH: ` or `AMBIGUITY: `. A deterministic decoder removes this prefix.
SEARCH text becomes one aspect/request; AMBIGUITY text becomes a whole-question
ambiguity with empty aspect_ids. Any ambiguity entry sets status to ambiguous.
This transport supports ambiguity-only and mixed outputs without semantic
inference in the decoder. Reject missing/unknown prefixes, empty payloads,
wrong tool names, and more than eight entries of either kind; never truncate.
Both arms use the same common contract; A may produce ambiguity entries from
its own analysis. This tagged transport is a proposed POC adaptation, not a
built-in LlamaIndex feature. Development smoke tests must demonstrate both
search and ambiguity outputs against pinned versions before freezing the arms.
If the generator cannot satisfy it, stop and report incompatibility.
Its prompt may ask for self-contained searches retaining conditions and exact identifiers, but
the wrapper must not perform a second semantic generation pass. Reject
unrecognized tool names. Preserve native output and any parse errors in trace.
If the library cannot expose enough information for the contract, report the
incompatibility rather than secretly introducing another planner.

No semantic fallback to the old planner or the other arm. Initial comparison
uses one model generation attempt, no validation retries and no SDK transport
retries. Configuration must demonstrate this; hidden defaults invalidate the
timing comparison. A hard request deadline of 10 seconds is an experiment
safety bound, not a product latency acceptance criterion. Failure handling
must preserve timeout versus invalid-output versus backend-error distinctions.

No generated SQL or FTS expression crosses this contract. Queries target the
existing natural-language search interface. Actual execution is excluded
from the primary comparison. A later, separately approved read-only retrieval
diagnostic could consume them without changing this contract or the retriever.

## References checked during research

- [spaCy token relationships](https://spacy.io/api/token)
- [spaCy dependency parsing](https://spacy.io/usage/linguistic-features#dependency-parse)
- [LlamaIndex standalone query transforms](https://developers.llamaindex.ai/python/examples/query_transformations/query_transform_cookbook/)

These document library primitives, not measured performance on our questions.
