## Condition-ledger rules (v4)

A question is the information being sought. A ledger entry is a source-grounded
restriction on that question's scenario, permitted approach, or interpretation.
The ledger audits the question text; it is not a list of every noun/API mention,
a retrieval filter, or a substitute for the standalone question.

### What must be audited

Include every active, applicable item in these categories, even for a single question:

1. Scope: supplied Formly version and UI adapter restrictions.
2. Scenario: states and transitions under which behavior is asked about, including
   hiding/showing, disabling, existing/default values and their API/literal pairings.
   A transition remains a scenario when grammatically inside the requested operation
   (for example, asking about model behavior on hiding). It must have a binding.
3. Dependency: a specified source or predicate controlling a requested property,
   including a model/form-state path. Audit the dependency relationship, not just
   isolated names. This is required even when it is the configuration goal itself;
   do not invent an unspecified truth value or expression.
4. Prerequisite: relevant already-completed setup or deliberately absent setup.
5. Exclusion or method restriction: active user limits on the lookup, such as not
   substituting a different option, not polling, or not adding persistence work.
   An exclusion is not optional because the question already paraphrases it.
6. Uncertainty/comparison: unresolved competing scenario settings or uncertain
   scope; retain the alternatives and uncertainty without choosing a side.

An operation alone (implement/register/use), a target API name alone, a custom
name alone, or a requested output noun is not automatically an extra condition.
Bind supplied values when they constrain a scenario or configuration relationship,
not simply to inventory every token. Relevant API names still stay in question text.
Do not bind irrelevant app background, quoted instructions, response-format requests,
retracted conditions, or app investigation requests excluded by this contract.
A quoted library claim requested for verification stays a neutral verification;
only its actual scenario and scope are conditions, not an asserted claim of truth.

### Attachment and excerpts

Resolve corrections before building the ledger. Apply a local condition only to
its local question(s). Carry shared conditions to every applicable question.
Explicit both/all assignments override a guess that a condition is useful only
for one outcome. Ordinary language and explicit restatements determine attachment;
do not spread a locally qualified observation method to unrelated configuration
merely because both are mentioned in one sentence. If scope remains unresolved,
retain that uncertainty in the focused question rather than guessing it away.

Each entry uses a meaningful verbatim source excerpt and zero-based question_indexes.
The exact excerpt, including case, must appear in each assigned question. Include
needed nouns in the question to resolve an excerpt's pronouns. Excerpts can overlap
or cover several related conditions; split them when they have different scopes.
Combine identical excerpts into one entry with all applicable indices. Do not use
isolated keywords instead of a meaningful relationship. A version/adapter name can
stand alone as a scope excerpt if its role is clear in the assigned question.

### Source-first exclusion and completeness check

Before finalizing, inventory the active source constraints by the six categories
above and assign them to requested aspects. Draft the focused questions and ledger
from that inventory. This is internal checking, not additional output fields.

Then perform these two checks:
- Source to output: for EVERY active constraint, locate both its meaningful source
  excerpt in the ledger and the same excerpt in every assigned question. Check
  negative restrictions explicitly, including exclusions near the end of the
  request and exclusions shared by an existence question and its contingent meaning
  question. If an exclusion is paraphrased in text but absent from the ledger, replace
  that paraphrase with a natural sentence containing its source excerpt and add the
  binding. Do not drop the exclusion or silently accept a text-only copy.
- Output to source: every binding is grounded, still active, meaningful and correctly
  attached. Remove no-longer-applicable constraints and do not spread local ones.

Do this within the single response before returning; do not emit a repair workflow.
Empty questions imply an empty ledger. No applicable conditions also permits an empty
ledger. Keep the existing three-field JSON schema. The validator checks declared
entries only: it cannot prove this source-first inventory is complete. Independent
semantic tests remain required. Optional role hints never change this contract.
