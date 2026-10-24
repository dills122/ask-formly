## Ledger rules v7

The ledger records the supplied circumstances and limits of a library lookup.
It is not an inventory of every noun or a second list of requested operations.
The question text must independently preserve every requested aspect, even when
that aspect needs no ledger entry. These rules apply prospectively to v7; they
do not change the grades or contracts of earlier experiments.

### Required conditions versus requested information

Required conditions are:
- Supplied scope, including version/adapter and unresolved scope alternatives.
- Supplied scenario states, events and transitions: hidden, disabled, becoming
  invalid, later property changes, existing values, return transitions. An event
  remains a condition when it is the event being observed. “Observe changes”
  therefore needs the change-event excerpt in the ledger as well as its question.
- Specified configuration/value pairings and dynamic dependency relationships,
  including a controlling model/form-state path. A value setting continues to
  govern dependent configuration/use questions, not just a preceding meaning ask.
- Applicable setup, explicit prerequisites and absent setup relevant at that stage.
- Active exclusions and method restrictions, with their precise local/shared scope.
- Eligibility for contingent follow-ups, including all governing ancestor gates.
- Unresolved scenario alternatives, negation and comparisons, without choosing a side.

Mere requested information is not, by itself, another required condition:
- “What arguments?”, “read the current model from this callback”, “register a type”,
  a named API, or a custom registration name alone describe targets/operations.
- Do preserve those targets in the question. Do not require a redundant ledger
  entry merely for “current model from the callback” when no extra execution limit
  is supplied. By contrast, “only inside this callback” is an explicit method
  restriction; “after the model changes” is an event/prerequisite and must bind.
- A method request such as configuring a message is not a state transition.
  Observing when the field becomes invalid is: the invalid transition must bind.
- Response-format instructions, directives to keep scenarios separate, application
  destinations, quoted instructions and retracted constraints are not conditions.
  Obey separation/corrections without turning them into artificial ledger entries.

### Which question owns a condition

For each source condition, identify its subject/scenario AND the operation it
qualifies. Shared field context can propagate to multiple operations, but a local
method restriction cannot propagate merely because the same field is involved.
Explicit “both/all” assignments govern. Explicit “only this question” assignments
exclude the other questions. Keep unrelated fields and scenarios separate.

A dependency that defines the behavior belongs in configuration and related
message/observation/behavior questions. Resolve “the same field/property” into that
actual supplied relationship. An observation event belongs in the observation
question's ledger even if a dependency entry is already present: dependency and
event are distinct requirements unless one meaningful excerpt covers both.

For “whether X is supported; if supported, how to use X without Y”, the support
question is unrestricted by “without Y”; that phrase limits use only. Never move
it backward into the support check to make the questions seem more helpful.
If the user instead asks “whether X is supported without Y”, the support check
itself is restricted. If the user explicitly applies the limit to both, retain it
on both. If genuine attachment ambiguity remains, preserve it rather than silently
strengthening a support check. A legitimate compound question may contain both
clauses, provided its wording keeps the restriction on the correct clause.

### Support and conditional dependencies

A requested support check must be an actual interrogative clause. Mentioning a
capability in an “if” clause does not ask whether it exists. Do not add support
questions where none are justified, but never omit an explicitly requested check.
An existence/support check is not gated on its own result. A narrower support
check can depend on a distinct earlier existence check. Every descendant lookup
retains all applicable outer and inner eligibility conditions; logical implication
of an outer gate by an inner gate does not replace the source excerpt audit.
Resolve “if so/it/that” to the relevant capability in each standalone question;
never turn a presumed positive result into an established Formly fact.

### Time and setup

Use the setup appropriate to the stage being asked about. If a type is currently
unregistered and the user requests registration THEN use, bind the unregistered
state to registration. In the use question, make prospective use after registration
clear. Do not require a second binding of the obsolete unregistered state there.
That original state may remain as explicitly historical context without implying
use while unregistered. A supplied explicit temporal clause (“after registration”)
is a required source condition for use. An inferred dependency between requested
registration and use belongs in wording but does not invent a new source excerpt.
Already-completed setup that still applies (such as an already registered wrapper)
remains a required condition on the applicable lookup.

For same-field return transitions, a self-contained “visible/enabled again” excerpt
can retain the return meaning without a duplicate prior-event entry. Explicit
“after X” prerequisites must bind. Do not import unrelated events, assert causal
relationships, or change which event's outcome is being asked about.

### Construct question text and ledger together

Internally prepare each requested aspect with its applicable source conditions.
For each condition assigned to that aspect, choose a meaningful verbatim excerpt,
put it into the question naturally with resolved antecedents, and record that
question's index for that same excerpt. Treat the text copy and index assignment
as one paired action. Never write text first and later reconstruct a ledger from
memory. This is internal preparation, not additional emitted reasoning fields.

After all questions are drafted, merge identical excerpts into one ledger entry
with every applicable index. Distinct conditions may share a larger excerpt if
its entire meaning applies to every bound question. Split excerpts when scopes
differ. Preserve case/spelling. No isolated keywords in place of relationships.
The excerpt must occur verbatim in source AND each bound question.

Check all three directions before returning:
1. Requested aspects -> actual question clauses: support, meaning, use and distinct
   outcomes are covered, without unsupported extra questions.
2. Active source conditions -> question and ledger: specifically inspect transition
   events, value settings, dependencies, ancestor gates and exclusions. Their
   presence in prose alone does not count as a complete ledger.
3. Each question/ledger assignment -> source scope: reject local restrictions moved
   onto support checks or unrelated operations, stale setup and cross-field leakage.

The global scope audit is separate: supplied uncertain versions remain grounded
uncertain strings; unspecified values are null. Heterogeneous per-question scope
uses null globally with explicit question scopes. Explicit core-only uses adapter
"none", unknown adapter uses null. Do not silently default to the KB version.

Keep the existing three-field JSON schema. Empty questions imply an empty ledger;
no applicable conditions also permits an empty ledger. Harmless grounded redundant
context is not a failure unless it changes scope, meaning or stage. These rules
clarify semantics; the unchanged structural validator cannot detect undeclared
omissions or prove proper attachments. Independent semantic testing is required.
