# Proposed source-boundary and role-conflict experiment

Status: proposal only. No code, new inference, training, gold changes or integration.
All future implementation/evidence stays within this POC in a separate directory.
v2, A, prior pilot, data/DB and downstream layers remain unchanged.

## What we learned

The narrow pilot separates several problems:
- Exact quoted model keys score 0/10, but their interiors were recovered with the
  correct role 10/10 bare and 9/10 described. Boundary serialization matters.
- Registration names also have role/recognition problems: only 2/8 interiors have
  the correct role in either schema.
- Complete compound APIs are 1/8 bare and 3/8 described.
- Described outputs conflict/overlap in 16/24 questions.
- Flat entity predictions cannot decide semantic ambiguity reliably.

Proposed architecture: unchanged v2 question → frozen GLiNER raw predictions →
bounded source-syntax normalization → strict narrow envelope and repair log.
This is an explicitly hybrid extractor. Any gain belongs to this combination,
not to improved model learning. Preserve the full question for meaning.

The syntax component recognizes a small declared subset of source text. It does
not infer library facts, business intent, API existence, negation attachment or
property/value relationships for arbitrary prose. It never reads the KB or app.
Unsupported syntax/context remains unresolved; no case-ID-specific rules.

## Fix 1 — quote boundaries, with no role changes

Build a source boundary map for balanced single/double-quoted strings and Markdown
code spans. Respect escape parity: an odd number of preceding backslashes escapes
a quote; an even number does not. Ordinary prose apostrophes must not open strings.
Double quotes inside a single-quoted string are content, and vice versa.

Expand a registration_name/model_key/value prediction only if it matches the
ENTIRE interior of one uniquely identified string literal. Include original
delimiters without decoding escapes or changing offsets elsewhere.
Never expand an arbitrary interior substring to the whole string.
Markdown backticks remain formatting, not string quotes; preserve quotes inside
them if they are part of the value. Unsupported quoting produces review, not repair.
The boundary map alone does not create unpredicted entities.

Example H01: model_key zip → model_key 'zip'.
Example D03: value Sam\'s choice → value 'Sam\'s choice'.
But model_key choice inside that larger string cannot become the whole value.

For a confidently recognized opening literal delimiter without a closing delimiter,
omit the disputed value and mark boundary_ambiguous from its opening delimiter
through question end. Preserve any other sound mentions. A prose apostrophe alone
does not justify this status. This formalizes the pilot's D06 issue extent.

## Fix 2 — complete API paths from API-root evidence

Starting from a predicted api_reference root, extend through immediately adjacent
dot members and balanced bracket-property segments. Initial supported grammar:
identifier followed by dot identifiers and/or brackets containing quoted string
or integer property keys. Retain exact whitespace/spelling inside supported syntax.
Do not cross prose or treat a method call, operator, template string, arbitrary
computed expression or unmatched bracket as a supported property path.

R04: predicted api_reference expressions plus the immediately adjacent
['props.required'] becomes expressions['props.required'].
Discard nested predictions only when this supported parse proves they are internal
components of the accepted whole API path. Log each suppression; retain raw output.

Do not infer a root API from a fragment labeled only value/model_key. Do not extend
a root inside an already established literal payload; boundary ownership comes first.
Do not allow crossing two separate code spans or values to manufacture a path.
Recognition of a syntactically valid path does not prove it is a real Formly API.
Missing APIs with no model root evidence remain misses in this ablation.

## Fix 3 — roles from explicit local syntax, otherwise review

No global precedence such as model_key > value or longest/highest-confidence wins.
Each occurrence is independent, even when spellings repeat.

For this experiment, support only these local forms, outside string payloads:
- type [optional colon or equals] STRING → registration_name for STRING.
- key [optional colon or equals] STRING → model_key for STRING.
- defaultValue [optional colon or equals] STRING/NUMBER/BOOLEAN/null → value.
The property token must be a standalone configuration property in this local form,
not part of another path, negated comparison fragment or ordinary "custom type"
noun phrase. Retain occurrences even in excluded configurations; this assigns
mention roles, not active scope. State exact lexical grammar in the implementation
spec and test negative boundaries before using it.
Do not infer model keys from general language like "model value" or "field name."

The proposed role operation can relabel an existing prediction if one supported,
unambiguous source form determines its role; it can suppress conflicting predictions
for that SAME source occurrence. It cannot add a missing property or missing value
without a model prediction. Such recall expansion would be a separate experiment.
This conservative restriction means the three operations may still fail the gate.

Examples:
- H01: key 'zip' → retain model_key 'zip', suppress value zip.
- H13: key 'false' → model_key 'false'; defaultValue false → value false.
  Later prose "a boolean false default" is outside the initial local grammar.
  If conflicting roles remain there, report role_ambiguous rather than inventing
  a special rule for this known case.
- D01: type 'badge' and key 'badge' get different roles at their distinct offsets.
- D05: no supported binding; conflicting roles for 'badge' → needs_review.
- D03: after an entire quoted value is established, predictions strictly inside
  its payload are internal content, not additional names/keys. Suppress only
  when enclosing syntax and an accepted whole-value prediction justify ownership.
  The separate key 'choice' outside the literal remains eligible.

Prose registration descriptions such as "wrapper named 'audit'" are not resolved
by these initial three bindings. Correct model predictions may pass unchanged;
conflicts stay visible. Do not add examples as rules after inspecting results.

## Conflict and status policy

Order: lexical boundaries → API-root completion → explicit local role resolution →
ownership/conflict check → strict envelope validation.
A literal can own its content only when its role is independently established;
a bracket string inside an established API path is an API component, not a value.
If ownership is ambiguous, neither "outer wins" nor confidence is sufficient.

Merge identical repaired records in the delivered envelope, retaining all original
prediction IDs and a duplicate count in diagnostics. Never collapse multiplicity
before raw error reporting. Unresolved conflicting regions are omitted and marked
role_ambiguous using the smallest enclosing source region covering the conflicting
candidates. Nonconflicting mentions remain present with status needs_review.
Whole-output malformed input remains extraction_error via the hardened adapter.

This detects syntactic conflict/unsupported boundaries only. A single wrong
unconflicted label can still pass structure validation, and semantic ambiguity
without a detected conflict remains a capability gap. Do not claim general
ambiguity detection or a complete implementation of all needs_review semantics.

Every action logs: operation, original prediction IDs/spans, source evidence span,
before/after role and bounds, and reason. No hidden repairs, per-case allowlists,
dictionary of desired answers, confidence-based role tie-breaks, or execution of
quoted instruction text.

## Before training

First replay stored outputs to learn whether generic source rules can help safely.
If they improve boundaries but leave role/API recall low, quantify those residual
errors before proposing targeted supervision. If they repair the wrong spans,
revise the design using development evidence and preserve the failed result.
No training is approved or started by this document.
