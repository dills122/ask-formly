# Evaluation evidence and operational lessons

Baseline: Angular21.2.25, Material/CDK21.2.14, Formly6.3.12. Executed 2026-10-15. The first eight-case development comparison tied: 8/8 passes in both arms, with no established correctness/effort advantage. A later source-only-designed six-case blind pass scored 5/6 in both arms: both custom Material solutions imported unexported TypeOption. The [public registration type](customization.md#types-and-registration) repair and a fresh control passed AOT/browser. Neither comparison establishes unseen production effectiveness; [coverage](coverage.md) records limits.

Keep operational guidance in its canonical topic:

- [Disabled-path migration](expressions-and-lifecycle.md#disabled-path-migration-can-change-behavior): aliasing does not guarantee equal ancestor behavior or event names.
- [Parser representation](api-contracts.md#value-changes-parsers-and-modeloptions): visible/control/model values can all change; raw display needs an explicit boundary.
- [Request lifetime](async-and-state.md#debounced-lookups-and-immediate-invalidation): delay placement changes when old responses become stale.

The pilot executed three supplemental JIT checks, three RxJS virtual-time checks, and strict AOT/three Chromium scenarios for each of two authored forms. [evaluation-evidence.json](evaluation-evidence.json) retains versions, observations and hashes, including subsequent audit observations. Virtual-time cancellation tests are not real HTTP tests. These results do not erase the two select failures in [Angular21 qualification](angular21-qualification.md).

Full prompts, original answers, masked reviews and raw execution artifacts stay outside the portable skill under `ideas/ask-formly/evaluation/`. Read those when auditing evaluation quality; they are not required context for ordinary Formly help.
