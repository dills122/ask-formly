Read ../CONTRACT.md and questions.json only for semantics. Do not read model
predictions, historical labels, other annotator files or application code.
Output a JSON list of 24 envelopes in input order:
{question_id,question,schema_version:"narrow-mentions-v1",mentions,status,issues}.
Mention: {kind,raw,start,end}, Python codepoint offsets, end exclusive.
Use exactly the contract's six roles, no overlaps, source order. Include all
occurrences. Keep quotes on names, keys and values; whole API paths with internal
quotes. Use needs_review for genuine ambiguity with issues as contract defines.
You may add a separate rationale map keyed by ID. Validate offsets with Python,
but semantically select spans yourself, not with automatic generic regex labels.
Keep all initial labels unchanged after delivery. No predictions exist yet.
