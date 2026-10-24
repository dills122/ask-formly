## Explicit requested-aspect and attachment audit (v6)

Use the following internal preparation before producing the existing JSON. It is
not an extra output field, a library answer, or an application investigation.

1. Inventory requested information separately from the conditions on it. For each
   requested capability, distinguish existence, support in a stated situation,
   meaning, configuration, use and observation when the request asks for them.
   A sentence of the form “if it supports X, how do I use it?” does not answer or
   replace an explicitly requested “does it support X?” lookup. If the request
   asks to establish support, include that check, even if a later usage question
   contains the same words. Do not add support checks gratuitously when the user
   only requests ordinary configuration. Do not gate a support check on the very
   support it is meant to establish. A check for a narrower capability can remain
   conditional on a distinct, earlier API-existence check.

2. Assign each aspect its source scenario and conditions before wording questions.
   Follow a same-field/same-behavior reference back to its supplied setup, including
   dynamic dependencies and corrected paths. A follow-up about that behavior's
   message or observation must preserve the governing dependency, not become a
   generic message or observation question. “For the same field” alone is not
   standalone context. Keep the actual relationship in the question and ledger.
   Share only conditions assigned to that scenario; never spread a local method
   limit, another field's state, or an unrelated earlier event by association.

3. Follow conditional dependencies through all levels. A lookup under an inner
   condition also retains every outer condition that governs it. Do not omit an
   outer source contingency because an inner capability logically implies it.
   Copy each applicable source eligibility excerpt into the dependent question
   and ledger, resolving each antecedent in ordinary words. An excerpt such as
   “If so” must identify what “so” means in that question. Ancestor support checks
   remain outside their own gate. Conditions apply to the dependent clause of a
   legitimate compound question, not to its prerequisite check. No guessed API
   behavior or presumed positive result may replace a conditional lookup.

4. Audit the question-to-condition attachments as a table internally: rows are
   active source conditions; columns are requested aspects. For every applicable
   cell, require BOTH the meaningful verbatim excerpt in that question and its
   index in the corresponding ledger entry. Reconcile exclusions explicitly,
   including tail-end exclusions and custom-logic limits. Text-only preservation
   is insufficient. A shared condition needs all applicable indices; a local one
   must not spread. Split excerpts with different scopes. Do not turn this table
   into output, and do not include irrelevant app context or retracted conditions.

5. Audit scope separately from wording. A supplied uncertain version/range is
   still supplied scope. Retain that uncertainty in global metadata when it
   applies to the request as a whole; null means absent or genuinely different
   per-question scope, not “not sure which supplied alternative is installed.”
   Preserve the appropriate exact scope and bindings in each question as well.
   Preserve explicit core-only and adapter distinctions under the existing rules.

6. Final coverage pass: match EVERY requested library aspect to an actual question
   clause that asks for it. Seeing its topic inside an “if” clause is not coverage
   of a requested support check. Then match every applicable condition cell to both
   its text and ledger representation. Finally remove unsupported asks and leaked
   conditions. Return only the original three-field JSON object. This internal
   audit is fallible; it does not make structural validation a semantic proof.

