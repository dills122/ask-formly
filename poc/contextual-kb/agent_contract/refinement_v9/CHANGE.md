### Exact source excerpts and shared context (v9)

Select each ledger excerpt by copying a contiguous span from the ORIGINAL request,
not from the generated question or from a mental paraphrase. Preserve word order,
case, punctuation, API spelling and literals. Do not turn a source interrogative
into an affirmative condition: “can a wrapper be reused” is not the source string
“a wrapper can be reused”. A source phrase such as “If yes” can express eligibility;
copy that phrase exactly and resolve what “yes” means outside the quoted span in
the question. The resolved explanation need not itself become a ledger excerpt.

Keep two distinct strings in mind: the verbatim source span and the surrounding
natural question wording. They serve different purposes. Copy the span into the
question unchanged, then assign its index. Immediately before returning, check
every condition string character-for-character against the original request and
every assigned question. If a span was rewritten, choose an actual meaningful
source span and update both its question copy and ledger together. Never repair
by deleting an applicable condition, silently changing the request, reducing it
to an uninformative keyword or replacing a conditional gate with an assertion.
This is a pre-submission check, not permission to repair saved test outputs.

Shared context is not the same thing as an eligibility gate. Distinguish:
- Explicit shared scenario: carry supplied settings, values, dependencies and
  applicable setup to every relevant lookup about that scenario.
- Explicitly different or independent scenario: keep scenario-specific events and
  prerequisites local, while retaining any scope/method limits explicitly shared.
- Same referent continuation (“that field”, “the same select”): it can retain the
  described field context as identification or history. A question about a later
  disabled state may mention that the same select previously received options.
  Such grounded context is not automatically an invented eligibility gate.

For a same-referent continuation, both a self-contained new-event question and a
question retaining relevant earlier context are acceptable when the source does
not force one reading. Preserve the requested outcome. Do not state that the new
behavior occurs only if, because of, or conditional on the earlier event unless
that relationship is supplied. Do not assert unprovided causal effects or carry
history from a different field. If scope genuinely remains unresolved, preserve
that uncertainty rather than selecting a causal or eligibility interpretation.

A phrase such as “for the select whose options arrived later” can identify the
same described select. Its grounded context may be bound to that question without
claiming that later arrival is necessary for disabled behavior. An explicit “only
if those options arrive” requirement is different: it requires source eligibility.
An explicit instruction to consider the disabled case independently of option
arrival overrides same-referent context. Method restrictions still attach to their
specified operations; same entity does not make local restrictions global.

These attachment rules clarify prospective v9 interpretation; old contracts and
grades remain unchanged. They do not relax exact-source validation, event coverage,
conditional ancestry, or independence of explicitly separate follow-ups.

