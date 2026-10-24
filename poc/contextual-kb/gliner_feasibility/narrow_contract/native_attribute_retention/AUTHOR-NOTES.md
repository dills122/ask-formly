# Independent retention fresh packet author notes

Authored only from root AGENTS, contextual-kb AGENTS/STEERING and the narrow mention contract. No earlier questions, gold, training rows, model outputs, prior results or implementation were read. Schema and installed tokenizer entry point were supplied separately by the implementation worker without data examples. No inference was run by this author.

The packet has 40 realistic library questions, 112 complete gold occurrences and four empty questions. It covers all six roles, complete API paths versus clipped fragments, unknown explicit API references, merged API/value spans, opaque expressions, quoted registration names versus plain API mentions, repeated occurrences and same spellings in distinct roles. The first twelve questions deliberately share a controlled interaction template; this is diagnostic coverage, not a natural-distribution estimate.

Probes contain every gold occurrence plus 48 semantic hard negatives: 12 clipped paths, 12 merged API/value candidates, 12 quote-stripped or opaque-expression fragments, and 12 ordinary prose spans. Four additional source-exact spans starting mid-identifier are transport-only probes and must remain outside the semantic-negative denominator.

Questions were built from explicit ordered annotated segments. Mention offsets are Python Unicode codepoints with end exclusive; repeated names retain separate occurrences. All raw/source slices were verified. Unknown explicitly proposed APIs count as references without asserting API existence. Names and string values retain syntactic quotes; opaque expressions retain their full extent.

Blind reviewer retention_review reported no annotation defects across the complete packet before this freeze. Independent installed-tokenizer-only inspection used gliner2.processing.word_splitter.WhitespaceTokenSplitter with lower=False, from gliner_feasibility/env/.venv. All 112 gold spans and all 48 semantic negatives match native token boundaries; all four transport probes fail native alignment as intended. No model weights were loaded for that inspection. An earlier attempt used the general contextual-kb environment and failed to import gliner2; the successful inspection used the specified GLiNER environment.

## Pre-inference freeze

Frozen at 2026-10-22T21:44:12.876825+00:00 after blind semantic review and tokenizer inspection, before this author accessed any inference output.

Gold role counts: api_reference=61, model_key=7, registration_name=10, ui_adapter=6, value=22, version=6.

| Artifact | SHA-256 |
| --- | --- |
| fresh.json | `78e87e296a3b40e88df8eb6e499313b7a5efd2ad47976070b49e6c797efb4b7c` |
| families.json | `eb3d402906b22bfb6af9df06d3ee001e00ae552d4a8165686bb5e16c8938275f` |
| probe_candidates.json | `e221569e978093caa7db42580c310d5373a080947cc43490e07aa78ff2114ff4` |
