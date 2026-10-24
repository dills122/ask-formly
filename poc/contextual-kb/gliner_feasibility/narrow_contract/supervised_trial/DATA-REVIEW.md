# Independent pretraining data review

Reviewed 2026-10-22 against `../CONTRACT.md` and `PROTOCOL.md`, before running any inference or training. Reviewer did not author or modify annotations. Scope is the 24 pilot envelopes, 40 new training envelopes, and 24 development envelopes; no old sealed evaluation, DB, A, or v2 content was accessed.

## Finding requiring resolution before freeze

T37 omits the explicit `type` occurrence at [95,99) in “without using the registered type 'consent-badge'”. The pilot H01 and H21 examples label `type` in the same configuration-use construction (“using the already registered type …”). T37 already sets a configuration property and excludes a supplied registration name; the negation is not a reason to suppress the property mention under the contract. Add this API occurrence, or record an explicit contract-based distinction and apply it consistently before freezing training inputs. Do not change the frozen pilot artifact to resolve this.

## Checks and semantic assessment

All 265 annotated mentions in the three supplied files exactly equal their Python codepoint source slices, are source ordered, and do not overlap. All six permitted roles are represented. The pilot contains 22 clear and two needs_review envelopes; omitting D05/D06 from training is correct and does not teach uncertainty handling. Before resolving T37, training has 62 envelopes and 202 mentions; development has 24 envelopes and 62 mentions.

Development support is small: API 24, value 12, version 10, UI adapter 7, registration 5, model key 4. A single missed model key moves recall 25 percentage points; these data cannot establish stable per-role generalization. Development has four empty envelopes; training has six. Both clear negative and positive examples are needed and present.

The remaining reviewed labels have defensible roles and clear boundaries:

- Explicit compound paths remain whole APIs, including internal string syntax; surrounding Markdown backticks are excluded. Hypothetical APIs in T04/V04 are correctly mentions without asserting existence.
- “model key”, “type named”, “type called”, and “type name” are descriptive role phrases, not automatically API tokens. The examples with literal configuration syntax `type …` / `key …` correctly include those properties. Ordinary application names HarborDesk/ConsentPortal are not APIs or registration names.
- Names and keys preserve supplied quote delimiters and are not duplicated as values. V07/V08 distinguish roles by occurrence. Negated and repeated mentions remain present.
- T20/T21 and V10/V11 preserve literal backslashes and quote syntax. Whether the strings would decode into a desired runtime value is outside this raw-span contract. T23/V12 retain opaque expressions as a single value and suppress nested apparent APIs.
- V24's quoted behavioral claim is correctly excluded; empty business-purpose questions do not infer APIs or registrations.

## Split and author-assumption limits

No exact question or question-ID overlap exists between the 62 training and 24 development envelopes. Reserved custom dev names (quartz-entry, copper-shell, memberToken, districtCode) are distinct from the new-training reserved names. This is not a semantic-family holdout: defaultValue comparisons, whole paths, opaque expressions, same spelling in different roles, escapes, scope comparisons and negated mentions appear on both sides. For example, V12/T23 share the opaque callback construction (character SequenceMatcher ratio 0.698), and V09/D02 share defaultValue comparison syntax (0.614). These are related templates, not exact duplicates.

The files cannot independently prove that the development author never saw training content; that is a provenance claim supplied by the orchestration. Both corpora are synthetic and deliberately cover the contract. Conclusions must remain about this small development probe, with no human benchmark or family-disjoint claim. Unseen names alone do not demonstrate robustness to unseen question structures.

## Reviewed input identities

- pilot/gold.json: `11af1aa3e0873729721aaa5ccd00f99685cf077daa65e1cbddeeb8e8f5421bc5`
- train-new.json: `664fb9284c9b4653b3682a2b3e372f135b5cd2971736d8aafb32c03e96afc836`
- dev.json: `9f55be0201394a561525ca306cbb182fd2de0230a49a78a43332aec48e39125d`

Initial verdict was to resolve T37 before training freeze. The author subsequently added the exact [95,99) API span and retained the original in `train-new-original.json`, recording the correction in `ADJUDICATION.md`. This resolves the finding; training now has 203 mentions, including 86 APIs across pilot and new data (50 in the new data). No other annotation blocker found. The hashes above identify the initial reviewed inputs; the run freeze must identify corrected training input. Final native-token receipts and result review remain pending.
