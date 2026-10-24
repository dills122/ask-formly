# Verifier labels v1

This is a supplied-occurrence verifier, not a new extraction vocabulary or Formly
knowledge assertion. Input is original focused question text plus exact half-open
Unicode character offsets. Repeated identical strings are separate occurrences.
Never snap, expand, trim quotes, or guess token-unrepresentable coordinates.

Seven binary targets, in order: complete, api_reference, registration_name,
model_key, value, version, ui_adapter. No no_entity class and no softmax.

complete means: this exact occurrence is one complete mention allowed by the six-role
contract. It does not mean grammatical English, valid JavaScript, a known Formly API,
or a value found in our knowledge base. Every positive role means BOTH complete
boundary AND that role in the given question. Consequently malformed spans have seven
zeros. This deliberately does not teach a role for a malformed fragment.

| Role | Positive target |
|---|---|
| api_reference | Exact supplied API identifier/path, preserving full brackets/member chain; exclude surrounding Markdown backticks. Unknown explicitly named APIs remain references. |
| registration_name | Whole supplied registration literal, retaining its quote delimiters; includes custom renderer/wrapper/validator names when explicitly used as registrations. |
| model_key | Whole configured key/address, retaining quotes when supplied as a quoted key. |
| value | Whole supplied literal or code-value fragment, retaining quotes/delimiters. A string used as registration/key is not also value at that occurrence. |
| version | Exact version string, excluding surrounding prose/backticks. |
| ui_adapter | Explicit UI adapter name, excluding prose/backticks. A quoted custom name 'Material' is a registration when that is its stated use. |

Gold complete mentions: complete=1, exactly one role=1, all other roles=0.
Negative probes: complete=0, all roles=0. Negatives include clipped member paths,
broken quote spans, nested fragments that omit required context/delimiters, and merged
adjacent mentions. A substring is negative only in the annotated occurrence/context;
never globally blacklist its spelling. Existing training-only negative annotations
are inherited; an annotation conflict stops qualification rather than silently repairs
frozen data. New corrections must be separate versioned overlays reviewed before use.

Ambiguous role/context, conflicting gold at same offsets, empty/out-of-range offsets,
incorrect source slice, or incomplete gold inventories are annotation failures: exclude
and report with reason before freezing a run, not default-zero supervision. Unsupported
token boundaries are transport failures: keep in reported coverage denominators, omit
from optimizer tensors, and never count as learned rejection. A supported malformed
span may be longer than one gold mention; exact supplied offsets remain unchanged.

Independent sigmoid decisions are not independent parameters or calibrated probabilities.
The boundary and role tasks still share representations; no immunity to interference
is claimed. No application investigation or claims about downstream answer accuracy.

## Full-inventory convention

The six-role gold inventory is exhaustive within the question, not just marked-code
spans. Plain `type`, `key`, `expressions`, `model`, or `wrappers` is an API reference
when the sentence directly discusses that Formly configuration property. Generic prose
about types of fields, model concepts, or wrapper components is not automatically an
API reference. Annotate a property name and its literal separately: `key` and quoted
model-key value are two occurrences. Ambiguous prose must be rewritten in new calibration
material before freezing, rather than silently choosing a different convention from
training. Repeated explicitly referenced properties receive separate offsets.
