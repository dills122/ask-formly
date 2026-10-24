# Proposed narrow mention contract — revision 1

Status: design for user review. No extractor, annotation migration, training or
integration implemented. This proposal supersedes no frozen contract or evidence.

## Objective and assumptions

Consume one unchanged question string from agent v2 and identify explicit,
source-grounded library/configuration mentions. v2 still derives the questions.
The output supplements the question; it never replaces its meaning with a bag
of tags. This is mention extraction, not a retrieval plan or a verified API list.

Assumptions: no inferred APIs from business purposes; no application investigation;
no property/value relation prediction or request-frame reconstruction in this
first narrow experiment. Those require separately approved contracts and tests.
The current five-label model's output is not silently mapped into this schema.

## Six mutually exclusive occurrence roles

| Kind | Extract | Exclude |
|---|---|---|
| api_reference | Explicit API/property/class/method spelling, including a complete code path. type/key count only when clearly configuration properties. Unknown/hypothetical names still count. | Formly/Angular library names, ordinary model/field/type nouns; fragments nested inside a full path. |
| registration_name | Explicit name supplied for registering/using a field type, wrapper, validator or other named registration. | A business purpose such as an SSN field without a supplied registration name. |
| model_key | Explicit supplied model key/path value in configuration context. | Built-in API property paths; application identifiers. |
| value | Other explicit configuration values or requested literal content, including string, boolean, number, null or an opaque code expression. | Names/keys already assigned their own role; version tokens; quoted behavioral claims. |
| version | Exact explicit version token, including v when present. | Library prefix; nested duplicate of the same token within a larger version span. |
| ui_adapter | Explicit adapter name such as Material or Bootstrap. | Generic core, none or UI adapter phrases. |

A code-shaped token is not automatically an API. Unknown candidate names count
only where the text presents them as library API references, even if existence is
being questioned. Extracting them does NOT establish that Formly provides them.

These are occurrence roles: the same text can have different roles at different
positions. A quoted registration name is not also emitted as value. The schema
separates registration names from model keys but does not yet assign a registration
subtype. Do not invent one to force a label.

## Source fidelity and boundaries

Each mention is {kind, raw, start, end}. Offsets are Python Unicode codepoints,
end exclusive, into the exact input question. raw must equal question[start:end].
No case folding, quote stripping, escape decoding or numeric coercion.

- API reference: whole exact path, including its internal quotes/brackets.
  Surrounding Markdown backticks are formatting and excluded.
- Names, keys and values: retain syntactic string quote delimiters when supplied.
  Thus key 'false' is different from value false; key '0' differs from value 0.
  Surrounding Markdown backticks remain excluded.
- Version: v6, not Formly v6. UI adapter: Material, not Formly v6 Material.
- Repeat separate occurrences; do not deduplicate before returning.
- For a compound API path, return its one maximal complete API span; no nested
  API/name/key fragments from its internal syntax.
- For an opaque value expression, retain the complete explicit expression as one
  value; do not tag apparent APIs inside it in this narrow contract.
- Distinct mentions may not overlap. If a role or boundary genuinely cannot be
  determined from text, omit the disputed mention and mark needs_review; preserve
  the source question. Do not use this mechanism to turn model misses into passes.

No normalization is necessary to make the first experiment work. If a later
consumer wants decoded values, that is a separate deterministic parsing contract
with its own tests; it must retain the original raw span.

## Output envelope

question_id and question are supplied by the caller and copied exactly.
schema_version is narrow-mentions-v1. mentions contains source-ordered records.
The envelope includes status: ok, needs_review, or extraction_error.
issues is an array of {reason, start, end}; span bounds refer to ambiguous source
regions, or are null for a whole-output failure. Reasons are role_ambiguous,
boundary_ambiguous, invalid_output, or runtime_error.

status ok means no detected extraction/representation issue; it is NOT a claim
of semantic completeness or correct Formly behavior. An empty successful mention
list is allowed for a grounded question without explicit names, APIs or values.
An agent abstention with no question never enters this extractor.

GLiNER would predict flat spans; a future adapter would validate and serialize
this envelope. It must not fabricate spans or recover them using per-case regex.
Confidence can be kept in diagnostics, not treated as correctness or used to
silently remove required hard cases. No confidence threshold is proposed here
beyond retaining 0.5 for the first controlled schema comparison.

## Worked examples (raw text shown; implementation must add verified offsets)

Input:
In Formly v6 Material, use type 'city-choice' with key 'cityId' and defaultValue false.

Expected:
- version: v6
- ui_adapter: Material
- api_reference: type
- registration_name: 'city-choice'
- api_reference: key
- model_key: 'cityId'
- api_reference: defaultValue
- value: false

Formly itself is not an API reference. Registration and key strings are not also
value mentions. No claim that city-choice is a built-in registration is made.

Input:
How is expressions['props.required'] set without changing expressions['props.disabled']?

Expected:
- api_reference: expressions['props.required']
- api_reference: expressions['props.disabled']

No props.required/props.disabled fragments, no custom names or values. The
unchanged question preserves "without changing"; these mentions alone do not
encode the negation or authorize modifying the second property.

Input:
Use key '0' with defaultValue 0, and key 'false' with defaultValue false.

Expected, in source order:
api_reference key; model_key '0'; api_reference defaultValue; value 0;
api_reference key; model_key 'false'; api_reference defaultValue; value false.

These spans preserve the possible pairings in source. They do NOT constitute a
validated relation graph; a consumer must not assume nearest-neighbor pairing
always works for arbitrary questions.

Input:
Does Formly v6 provide rebuildOnlyDirtyFields?

Expected:
version v6; api_reference rebuildOnlyDirtyFields.
Existence remains an unanswered question, not a model assertion.

Input:
How is a custom Formly field implemented for an SSN field?

Expected: no mentions, status ok.
The complete question remains useful. Do not infer type 'SSN', a model key, mask
API or application component.

## Scope retention

Do not pass global v2 constraints as synthetic text to this extractor. Preserve
the unchanged v2 envelope upstream. Extract explicit scope mentions even when
negated or compared; never promote a mention into a selected active scope.
Formly v5 versus v6, or "not Material", requires the full question for meaning.
Version-to-library attachment is not claimed by this contract.

## Boundaries and artifacts

All proposed files belong here under gliner_feasibility/narrow_contract/.
Always preserve source questions, old annotations and raw experimental evidence.
Never change A, v2, pilot, data/DB, retrieval, evidence assessment, answer assembly
or MCP. Never read old sealed evaluation content for this experiment.
Additional implementation/training is a next decision, not performed by this spec.

Proposed implementation style: small Python standard-library validator and
unittest tests; existing POC GLiNER environment for inference. snake_case names,
explicit failures, no application-code imports or new dependencies anticipated.
A future test command, once tests exist:
python3 -B -m unittest discover -s poc/contextual-kb/gliner_feasibility/narrow_contract -p 'test_*.py'
No runnable harness is claimed yet. See TEST-PLAN.md for design qualification.
