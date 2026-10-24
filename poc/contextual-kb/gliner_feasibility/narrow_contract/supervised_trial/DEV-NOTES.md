# Independently authored development set

Authoring frozen before model predictions. This author read only `../CONTRACT.md` as source material and did not inspect pilot, training, model-prediction, or sealed evaluation content. No application investigation or application code execution occurred.

The set contains 24 clear questions, V01–V24, in six manually authored families with four questions each:

- V01–V04: whole compound API paths, including an explicitly hypothetical API whose extraction does not assert existence.
- V05–V08: registration names versus model keys, including identical text in different occurrence roles.
- V09–V12: quote/value boundaries, zero, false, null, backslashes, escaped quotes, and an opaque expression.
- V13–V16: explicit versions and UI adapters; no compatibility claim is asserted.
- V17–V20: exclusions, comparisons, and repeated occurrences retained separately.
- V21–V24: empty extraction and business-purpose negatives, including a quoted behavioral claim.

Semantic occurrence roles and exact raw spans were authored first. A standard-library authoring script then located those predetermined spans in source order and validated source equality, bounds, and nonoverlap. All envelopes have status `ok` and no issues; that status is a representation judgment, not a claim of model accuracy or library behavior. Offsets use Python Unicode codepoints and exclusive ends. Markdown backticks are excluded; syntactic string quote delimiters and escapes are retained.

Custom names are restricted to quartz-entry, copper-shell, memberToken, and districtCode. Familiar API vocabulary is necessarily shared across the domain. Because the author did not see training data, semantic-family disjointness and absence of accidental wording overlap with training cannot be guaranteed. The family quotas themselves were supplied by the experiment owner. This is a small, clear-case development set, not a sealed generalization test or coverage of genuinely ambiguous cases.

`dev-freeze.json` records the SHA-256 of the exact serialized development bytes at authoring freeze. Predictions must not be used to revise this frozen set. Any later correction requires a separately recorded revision and reason.
