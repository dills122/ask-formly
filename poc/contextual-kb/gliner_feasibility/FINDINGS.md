# GLiNER2 development feasibility findings

Status: independently reviewed. The reviewer found no harness or API/schema wiring defect and accepted the negative feasibility findings; this configuration is not ready for a full comparison. This is a bounded extraction probe, not a completed question planner or a comparison against A.

## Recommendation

Do not proceed to a full comparison with this configuration. Source-span mechanics work, but the pretrained model plus fixed schema did not supply the semantic pieces needed to assemble faithful plans. The three multi-ask gates D01/D02/D10 all fail. No plan adapter was built, no A/B code or configuration changed, and no held-out case was read for this check.

## What was tested

GLiNER2 package 2.1.0, local boundary checkpoint fastino/gliner2.5-base-v1, revision 54785d51df8d86a0d8f2eb212fec15871aad2c4d. This is the GLiNER2 family's current boundary architecture, selected to avoid fixed-width limits on requested-outcome phrases. Eight described span types, two relation types, and clear/ambiguous classification used one schema. Threshold 0.5, CPU four threads, no training, no prompt/schema iteration, no fallback or generative repair. The 12 existing development questions each ran three times. All code, new dependencies, downloaded models, caches and evidence are confined to gliner_feasibility inside this POC.

The library provides trained extraction, classification, offsets and relations. We supply a semantic schema and mechanically validate native spans. There is no evidence here that the pretrained checkpoint was trained to decompose technical questions. Library support for relations is not proof it recognizes our requires_context relation.

## Observations

- 36/36 calls completed without backend/span-validation errors.
- All 81 emitted span occurrences across repeats exactly match the original question at their returned offsets. This says nothing about missed text or semantic role correctness.
- No requires_context or refers_to links in any call.
- Six requested_outcome spans over five first-pass cases; several are incomplete nouns or verbs. Seven cases return none. These counts are not aspect recall.
- No identifier or unresolved_reference spans on any case. Some API spellings appeared under other labels, so this is not a claim that no API text was ever extracted.
- Ambiguity detection: one of two genuine ambiguity cases detected (D12); three false positives among ten clear cases (D01/D05/D07). Precision 1/4, recall 1/2. No explanatory unresolved-reference span was extracted even for D12.
- Native outputs, including confidence scores, were identical across the three passes for each question. Model confidence is not calibrated task accuracy.

## Case assessment

| Case | Native evidence and implication |
| --- | --- |
| D01 | No requested outcomes; resetOnHide: false appears as condition/negative constraint but no hiding-to-value/control links. Incorrect ambiguous classification. Fails multi-ask gate. |
| D02 | register a renderer is useful; second outcome is only configure. wrapper is a separate subject with no link to configure. Cannot assemble both focused requests without another semantic decision. Fails gate. |
| D03 | No outcome. Negative constraint span removing its control omits without, losing polarity if used alone. |
| D04 | No outcome or identifiers for the expression API comparison. |
| D05 | props.placeholder appears as outcome/literal; version and adapter scope absent. Incorrect ambiguous classification. |
| D06 | No comparison outcome or defaultValue identifier; 0 is a literal, false labelled condition/negative constraint without its model-value role. |
| D07 | wrapper subject only, no requested location. Incorrect ambiguous classification. |
| D08 | options.formState labelled outcome/literal and browser restart condition, but persistence action and their relationship absent. |
| D09 | Misses genuine ambiguity. hook incorrectly tagged negative constraint; no unresolved reference explanation. |
| D10 | answer is the only outcome; retain-control outcome absent. Hidden-field condition extracted but unlinked. Fails multi-ask gate. |
| D11 | type a custom prop extracted, but FormlyFieldConfig<MyProps> missing. |
| D12 | Correct ambiguous label, but no reference span identifying that setting. |

These are manual author assessments against the existing development rubric. No complete-plan score is assigned: there is no retrieval-plan adapter, and partial extraction is not a plan.

## Timing and setup

Exploratory extraction plus validation median 196.4 ms, nearest-rank p95 205.9 ms, maximum 250.6 ms across 36 samples. The first inference is included; there was no warmup. Import/model loading took 10.62 s separately. Model has 193,581,591 parameters. This is CPU development timing, not a qualified latency comparison with A's earlier held-out run, and not end-to-end retrieval timing.

PyTorch 2.14.1, Transformers 5.20.2, Python 3.12.13; transitive dependencies pinned in env/uv.lock. Native load logs include Transformers model-type warnings and a torch.jit deprecation warning. Loading and inference completed, but warnings remain in evidence rather than being suppressed.

The initial manifest-writing command had a relative-path error; the shell still launched the run. The manifest was corrected after launch without changing code/schema. This is disclosed development evidence, not a prospectively frozen benchmark. The schema was written before inference and was not tuned after outputs. A 60-second Python signal alarm is a diagnostic bound, not a hard native-code timeout. No call approached it. Offline env and an audit hook restrict inference reads/network; the hook is defense in depth, not an OS sandbox, and is installed after local model loading.

## Integrity and verification

Eight tests passed after two retained red stages: Unicode/codepoint offsets, non-mutating native output preservation, invalid or rewritten spans, required relation endpoints, development-only fixture guard, forbidden network/knowledge access, and no retry on backend error. These prove harness behavior, not semantic quality.

All 60 protected entries (38 locked source/data/DB files plus 22 prior freeze entries) match their original hashes after the run. A's implementation and prior environment declarations/lock are unchanged. Existing unrelated repository modifications were left alone. No compiler, DB query, retrieval, answer assembly, old data test suite, A execution, or held-out input was used.

## Interpretation and next decision

Extractive output prevents fabricated wording only when the model selects the right complete span. It can still drop negation, miss requested outcomes, or assign wrong semantic roles. This checkpoint/schema has not demonstrated that core capability. A remains the unchanged baseline; this check cannot show that C is better or worse overall.

Changing schema wording or adding supervised task examples might help, but that is an untested follow-up, not a result. A full comparison is premature. Any supervised training or substantial new architecture should be explicitly proposed and reviewed first. The present task stops at reviewed feasibility findings.

## Independent review disposition

[Review instance 1 of 3](evidence/independent-review.md) reproduced the aggregates, passed all eight tests, and verified all 60 protected and 13 probe/model hashes. No actionable findings. Accepted the reviewer’s conclusion and provenance limitation. No fixes, model reruns, full comparison or further review instance is needed for this bounded check.

## Evidence

- [Plan](PLAN.md), [fixed schema](schema.json), [probe](probe.py), [runner](run.py), [tests](tests/test_probe.py)
- [Raw 36 outputs](evidence/raw.jsonl), [summary](evidence/summary.json), [runtime](evidence/runtime.json), [load/run log](evidence/05-run.txt)
- [Input/code/model hashes](evidence/probe-freeze.json), [protected-before](evidence/protected-before.json), [protected-after](evidence/protected-after.json)
- [Initial red](evidence/01-red.txt), [first green](evidence/02-green.txt), [observation red](evidence/03-observe-red.txt), [eight-test green](evidence/04-green.txt)

Official sources: https://github.com/fastino-ai/GLiNER2 ; https://github.com/fastino-ai/GLiNER2/blob/main/tutorial/6-relation_extraction.md ; https://huggingface.co/fastino/gliner2.5-base-v1 ; https://pypi.org/project/gliner2/2.1.0/ .
