# Independently authored fresh questions and candidate probes

Author: `/root/contrast_fresh`, with blind semantic review by `/root/contrast_review`.

The author read the repository AGENTS.md, contextual-kb STEERING.md, and the narrow CONTRACT.md plus pilot contract validator to establish the six-role output shape. No prior question, gold, training, model prediction, result report, or new implementation was read. Filename inventory was used only to find the contract. No network, model inference, or training was used in authorship. Questions ask about Formly rather than asserting behavioral answers or API existence.

`fresh.json` is a list of 40 full `narrow-mentions-v1` envelopes. `families.json` maps question IDs to family names. All gold spans use Python Unicode codepoint offsets, with the end exclusive; repeated spellings are distinct occurrences. Gold spans were built by concatenating individually marked text segments, never searching for repeated substrings. There are 106 gold mentions and five empty successful envelopes (one lifecycle paraphrase plus four dedicated empty cases).

`probe_candidates.json` has one `candidates` array using the agreed harness shape. Each entry has question_id, kind (`gold_valid` or `malformed`), start, end, text, expected_role, invalid_family and diagnostic reason. It contains 106 gold-valid candidates with their six-role expected label; 40 invalid source-exact candidates with expected_role `no_entity`, ten each `clipped_api`, `merged_api_literal`, `quote_nested`, and `prose`; and four transport probes explicitly separated by invalid_family `mid_identifier_transport`. Semantic and transport failure counts must remain separate; an unrepresentable candidate is not a successful semantic rejection. Valid gold spans must be counted in their own retention denominator.

Fresh coverage includes complete bracketed API paths; API/literal boundaries; quoted and nested object/array literals; quoted strings containing API spellings; registration versus model key versus value versus UI adapter; repeated identical words in different roles; negated/contrasted behavior in realistic library questions; and empty extraction cases. The semantic-negative candidates intentionally violate one complete-mention boundary or identify ordinary prose. They do not change the source question or imply a correct Formly answer.

Blind review before freezing corrected an omitted explicit `props` API mention, two surplus array brackets, and a callback-fragment negative whose boundary would have been inside a word. The replacement negative is a complete nested expression inside the opaque supplied callback. Transport candidates were changed from structurally malformed envelopes to source-exact in-bounds substrings with unavailable word-token boundaries.

Status: frozen after independent semantic review and read-only installed WhitespaceTokenSplitter alignment verification. All 40 semantic negatives and all 106 gold candidates are source-exact and aligned; all four transport candidates are source-exact and unaligned as intended. No model outputs have been inspected by the author or reviewer. The final shape conversion changed no question, span, or expected semantic result.


Frozen SHA-256:

- `fresh.json`: `9c0baf7b4568522e74909c3044010c51e38fccb68b34ede87e99af31e1ebb2c2`
- `families.json`: `bfda7bb23081387ef706c4e021ee6458e032448aa630985a8f52ac4ebe729685`
- `probe_candidates.json`: `7803ace490d3a2f2d19dc8433f6b77532dd27b53d89e8b811c54f1293e52694f`
