# Independent fresh cross-role cases

These 40 independently authored questions form eight families of five cases.
Every question is a self-contained Formly library question. Custom registration
names and model keys have explicit role context; no application investigation is
requested. Six cases intentionally have no extractable mentions. All six roles
are represented, and all envelopes use status `ok` without unresolved ambiguity.

Authoring inputs were the POC AGENTS.md and STEERING.md, narrow CONTRACT.md, the
TDD skill, and pilot/contract.py. No prior gold, case sets, training data, model
outputs, or inference harness was read. The pilot validator was used only to
validate envelopes. No predictions were generated or inspected. Reserved custom
vocabulary was communicated to the implementation worker without questions.

The cases test occurrence roles, explicit scope, formatting, complete paths, and
opaque expressions. They are ambiguous-looking but intentionally labelable from
local text. They are not selected to guarantee cross-role prediction conflicts;
actual conflict yield must be measured separately. The families describe test
intent, not expected model failure or guaranteed extractor behavior.

Names, keys, and string values retain their syntactic quotes. Markdown backticks
are excluded. Complete API paths and opaque expressions have one span, with no
nested mentions. Repeated occurrences remain distinct. Negated scope references
are retained without treating them as selected scope. Version tokens exclude the
library name. Quoted behavioral claims do not become literal configuration values.

Validation: all 40 envelopes passed pilot.contract.validate, with exact Python
Unicode codepoint offsets, source order, and no overlap. Checked 40 unique IDs,
eight five-case families, six empty cases, and coverage of all six roles. This is
schema/source-fidelity validation, not proof of semantic gold correctness or a
model result. Ready for independent gold review before freeze. No implementation
RED/GREEN claim is made: this deliverable authors static independent tests before
the implementation experiment, and modifies no extractor behavior.
