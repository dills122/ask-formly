# Bounded replay protocol

Implement repair_design proposal with no training/inference or changes to any
prior artifact. Inputs: unchanged 24pilot questions, gold, and 48 predictions.
Independent12counterexamples are generated without implementation/pilot outputs;
their contents stay unread by implementer until implementation freeze.

Four stages per bare/described source: hardened baseline; quotes; quotes+paths;
quotes+paths+roles/ownership. Conflict reporting and duplicate provenance are
generic delivery normalization on repair stages; stage0 reproduces old adapter.
Keep this distinction in the report. Repair stages retain nonconflicting mentions
under needs_review; they are diagnostic only, not accepted successful outputs.

Grammar frozen in repairs.py. Quote starts exclude intraword apostrophes; only
single/double string delimiters are supported. A backtick is a boundary that a
quoted span/path may not cross. Path roots/members use ASCII JS-style identifiers,
bracket keys are quoted strings or signed decimal integers, internal whitespace
permitted. Call/computed/unbalanced path syntax gets boundary_ambiguous on the
original candidate span with no guessed expansion. This clarification was sent
to counterexample author before freeze.

Bindings: type/key/defaultValue optional colon/equals with whitespace; type/key
require quoted literal, defaultValue additionally accepts signed decimal/exponent
numbers, true/false/null. Property inside a string or path, custom type noun
phrases, and identifier-prefix/suffix collisions cannot bind. Quoted value payload
ownership additionally accepts explicit literal text/literal value/exact string
wording plus a predicted whole value. These are source cues, no case-specific names.
Unsupported prose is not guessed. The implementation is deliberately bounded,
not a general JavaScript/Markdown parser or semantic ambiguity classifier.

Each action retains prediction IDs, before/after spans, source evidence, reason.
Input raw rows retained unchanged; replay outputs, duplicates and review regions
separate. No confidence tie-break, percase rules, gold access in repairs.py, or
addition of an entity without prediction support. Repairs may produce a wrong
unconflicted role; quality is measured, never inferred from structural validity.

Primary reporting: diagnostic retained spans and accepted(ok-only) P/R/F1,
per-role/origin/family, exact envelopes/status, error/review/empty outputs,
whole-path/quoted recovery, per-parent unique atoms, repair time separately.
New false positives/lost correct mentions count against retaining a candidate.
Record new wrong delivered spans even on needs_review outputs as safety diagnostic.
Raw baseline and gold remain unchanged. Include counts for counterexamples, no
claim of GLiNER generalization from hand-authored candidate spans.

No post-counterexample or scored-replay tuning in this bounded experiment. Record
failures and make a clear decision. Scoring bugs may be fixed with preserved
first results and regression evidence; they do not justify changing the extractor.
Independent review verifies code, protocol, evidence and decision before training.
