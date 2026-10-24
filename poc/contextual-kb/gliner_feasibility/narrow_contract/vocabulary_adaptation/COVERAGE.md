# What expanding vocabulary means in this trial

We teach more exact API references in realistic contexts and counterexamples.
The six extraction roles stay fixed. There is no runtime word list, API
allow-list, regex expansion or imported source-code dependency. API recognition
is distinct from validating that an API exists or supplying facts about it.
Custom wrapper/type names remain registration_name; Angular is a library name,
not a Formly UI adapter. Ordinary field/model/type nouns remain untagged unless
context explicitly names a configuration API. Backticks are formatting, not API
span content. A supplied literal retains its syntactic string quotes.

Known API reference spellings checked read-only against:
- https://raw.githubusercontent.com/ngx-formly/ngx-formly/v6.3.12/src/core/src/lib/models/fieldconfig.ts
- Existing installed @ngx-formly/core package6.3.12 declarations under
  local/gauntlet-browser/node_modules (inspection only; no imports or copying).

Coverage includes validators/asyncValidators/validation.messages; wrappers;
expressions/expressionProperties/hideExpression; hooks and lifecycle paths;
field classes/group/controlreferences; options methods; parsers/focus/get/parent;
formatting and ordinary-noun contrasts. Source names inform annotation examples,
not retrieved answers or a replacement knowledge database. Source behavior is
not being requalified. We don't add compatibility claims or endorse deprecated
APIs by recognizing them in a question.

New training questions use different custom registration names and modelkeys
from the independently authored fresh test. LibraryAPI names legitimately overlap;
this checks contextual transfer within a domain, not unseen-API generalization
across every test. All earlier test questions stay out of the gradient dataset.
