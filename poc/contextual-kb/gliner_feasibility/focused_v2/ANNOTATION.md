# Entity-only evaluation annotation, frozen before prediction inspection

Annotate explicit source occurrences in each supplied question, not implied facts.
This is textual entity extraction, not relevance to a final answer. Include tokens
in quotes/old headings if present; their truth is not being endorsed. No app/code
inspection, library research, model output reading or invented entities.

Each row: {id, entities:{api:[],custom_identifier:[],literal:[],version:[],ui_adapter:[]}}.
Each span: {text,start,end}, exact Python character offsets, end exclusive.
All occurrences count; no deduplication across occurrences. Same span can have
multiple types only where explicitly permitted below. Do not nest api components
inside a full API path.

- api: Explicit code-like Formly or Angular API/property/type names, including
  hypothetical named APIs. Examples: resetOnHide, FormControl, resetModel,
  hideExpression, defaultValue, props.label, expressions['props.required'].
  Include type/key when explicitly presented as configuration property names
  (type 'name', key 'cityId'); not the ordinary nouns 'custom type' or 'model'.
  For a path include the whole path, not just props/expressions. Also annotate explicitly supplied custom names inside a path; a built-in
  property subkey such as props.required is not a custom name.
- custom_identifier: Explicit user registration names, model-key values/path values,
  e.g. 'help-panel', 'accepted', '0'. Include the content, exclude surrounding quote
  delimiters (literal spans separately include those delimiters). Do not include application component/file/service names (OTW,
  CitySelector, fetchCities) in this experiment's entity label: these are not
  supplied Formly configuration names.
- literal: Explicit supplied configuration values or requested literal content.
  Include quoted value content INCLUDING surrounding delimiters, matching the
  existing pilot guide; numbers/booleans
  as their exact tokens. Custom_identifier values also get a literal span at the
  literal offsets including quotes when quoted. Unquoted explicit config values
  have the same offsets for both types. Do not tag version
  numbers, quantities of questions/fields, ordinary 'false' in prose not referring
  to an actual supplied boolean, or quoted narrative claims as configuration
  literals. Repeated references to a supplied default false/0 remain literals.
- version: Exact explicit version token: v6, 6.3.12, 21 etc, without library name.
  Include Angular and Formly version mentions; this taxonomy cannot distinguish
  their attachment, which must not be claimed from these scores.
- ui_adapter: Explicit adapter name, e.g. Material/Bootstrap/PrimeNG including
  excluded/negated mentions. 'none', 'core' and 'UI adapter' are not adapter names.
  Whether the adapter is in positive or negative scope is not an entity metric.

Use judgment to annotate source text once without model predictions. Preserve
actual uncertainty in a separate notes field on each row when needed (optional).
Span validation proves offsets, not correctness. These labels are agent-authored
and not expert-human ground truth. No full-frame gold is implied.
