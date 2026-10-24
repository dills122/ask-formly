# Frozen narrow pilot execution

Authorized implementation of ../CONTRACT.md and ../TEST-PLAN.md.
24 questions: 18 actual saved v2 strings, six marked developer diagnostics,
four per family. Selection freeze predates annotations; gold freezes before
prediction. No v2/A edits, no data/DB operations, no sealed evaluation content.

Same pinned local base, no prior adapter. Bare six roles vs labels.json described
roles, alternating order, threshold .5, overlap nested unchanged, seed1701,
deterministic CPUfloat32 four threads. 48 calls. Local/offline existing POC env.
Serialized model schemas and raw predictions retained. No post-inference tuning.

Scoring: raw typed-span P/R/F1 is a diagnostic including exact source spans even
from overlapping outputs. Contract-accepted P/R/F1 replaces structurally invalid
outputs with empty predictions, giving zero recall for those questions; report
raw false positives alongside accepted metrics so rejection cannot hide errors.
Overlap/duplicates are structural failures. Sorting for serialization is allowed;
dropping, boundary repairs, role coercion and semantic filters are not.

Flat GLiNER entity schemas do NOT predict needs_review/issue regions. The adapter
does not invent ambiguity handling. It returns ok for structurally valid spans,
including empty spans, or extraction_error for invalid/runtime output. Report the
two gold needs_review cases and status failures explicitly. This is a known
capability gap, not omitted evaluation or inferred success.

Report each role and family/origin separately, exact-set questions split by
gold mentions, status and errors, quoted-boundary and compound API-path misses,
unique per-parent atoms and timing including validation. Include gained/lost true
spans and changed false positives. No-mention FP rate separately for clear empty
and ambiguous empty cases. No claim of trained ambiguity detection or relation,
negation, scope attachment, retrieval or answer quality.

Gate as specified: >=90% P and R overall and every nonempty role, 100% structural
validity; designated critical fixtures R04/1,R04/2,H13/1,H14/1,D02,D03,D04 must
preserve their exact whole paths and supplied value/name/key boundaries. Gate is
a development qualification only. Integrity hashes verify protected prior files.
Independent review before any training. No training authorized or run here.
