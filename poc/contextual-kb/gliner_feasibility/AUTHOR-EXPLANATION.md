# Author Explanation

Intent: test whether pretrained GLiNER2 extraction can supply semantic spans and links before investing in a planner. The plan intentionally stops before plan assembly if extraction prerequisites fail.

Flow: fixed original 12-case dev fixture -> fixed schema -> offline pinned boundary model CPU -> untouched native extraction and measured duration -> exact offset checks -> raw JSONL. Test inputs are synthetic span examples, not model-generated evidence.

probe.py owns dev allowlist/hash, native span validation, runtime access audit and one-attempt observation. run.py owns local setup, three passes and retained evidence. schema.json describes outcomes, condition/negation, exact tokens, scope, subjects and unresolved references plus two relations and ambiguity labels. env declarations isolate new package versions from A.

No retrieval plan adapter was built because all three multi-ask feasibility gates failed. No fallback, regex semantic reconstruction or post-hoc threshold tuning was added. FINDINGS.md contains manual first-pass interpretation and exact automated aggregate observations; repeated native outputs identical.

TDD: 01 missing probe red ->02 six green;03 missing observe red ->04 eight green.36real calls allvalidated;60protectedentriesunchanged. No full existing suite or DB test run.

Deviations: manifest shell snippet failed path resolution before launch and was corrected after launch (code/schema unchanged); explicit in findings/progress. Signal alarm is not hard native deadline. Audit guard installed after local model load, offline flags set beforehand; defense in depth only. Native model-type/deprecation warnings retained. No claim of independent semantic double-grading, benchmark superiority or answer accuracy.

Costs: another local environment and193.6Mparametercheckpoint, 8spanlabels/2relations/2classes, approximately200msdevcalls. No changes to existing serving path.

Challenge the schema/API wiring, whether a library limitation could instead be a probe bug, validity of no-links/no-identifiers and ambiguity counts, span offsets, run provenance, guard scope, and conclusions. No claim all extractive models fail.
