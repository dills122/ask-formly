## Condition-ledger rules (v5)

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

7. Eligibility for conditional follow-ups: supplied "if", "only if", "unless", or
   equivalent conditions that determine whether a later lookup applies. Existence or
   support of an API is an eligibility condition even when the earlier lookup asks
   whether that API exists. Bind the source contingency to the dependent meaning,
   usage or other follow-up question; do not gate the existence/support check itself.
   A paraphrase in the question is insufficient: include a meaningful verbatim
   source excerpt in both the dependent question and its ledger entry, resolving
   pronouns to the API/capability being checked. Never treat the condition as proof
   that the API exists. If one legitimate compound question contains both checks,
   preserve the gate on the dependent clause only; the binding identifies that
   question without making its existence check conditional on itself.

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

### Preceding events versus requested outcomes

A binding records scenario applicability, not which event's outcome is being asked
about. Keep each question's requested outcome explicit. For the same field's stated
hide-then-show sequence (including "visible again"), earlier hiding can be relevant
history in a question about showing. It is permitted to copy that earlier-event
excerpt into the later question and bind it there as history; this is not leakage
provided the later question still asks only the later outcome. It is also permitted
to use a self-contained return-transition excerpt instead, without duplicating the
prior event in the ledger. Do not penalize these equivalent representations.

When the request explicitly makes an earlier event a prerequisite ("after X"),
that prerequisite is mandatory context and must be bound to the dependent question.
An "again" transition must retain its return meaning. Do not invent prior events,
causal relationships or prerequisites. Never carry an event from a different field
or unrelated scenario into another question. A local method restriction or API
setting is not automatically shared just because two outcomes form a sequence.
Only share it when the request assigns it to the common field/scenario or both asks.

Each entry uses a meaningful verbatim source excerpt and zero-based question_indexes.
The exact excerpt, including case, must appear in each assigned question. Include
needed nouns in the question to resolve an excerpt's pronouns. Excerpts can overlap
or cover several related conditions; split them when they have different scopes.
Combine identical excerpts into one entry with all applicable indices. Do not use
isolated keywords instead of a meaningful relationship. A version/adapter name can
stand alone as a scope excerpt if its role is clear in the assigned question.

### Source-first exclusion and completeness check

Before finalizing, inventory the active source constraints by the seven categories
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
- Conditional-follow-up check: for each dependent lookup, locate its source
  eligibility clause in BOTH the question and ledger. Check this separately from
  the no-substitution exclusion; satisfying one never substitutes for the other.
- History check: distinguish the event whose outcome is requested from earlier
  scenario context. Retain explicit prerequisites and return transitions without
  changing the requested outcome or importing unrelated/local restrictions.
- Output to source: every binding is grounded, still active, meaningful and correctly
  attached. Remove no-longer-applicable constraints and do not spread local ones.

Do this within the single response before returning; do not emit a repair workflow.
Empty questions imply an empty ledger. No applicable conditions also permits an empty
ledger. Keep the existing three-field JSON schema. The validator checks declared
entries only: it cannot prove this source-first inventory is complete. Independent
semantic tests remain required. Optional role hints never change this contract.
