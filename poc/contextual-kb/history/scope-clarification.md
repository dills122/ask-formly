# Explicit unknown-scope clarification

## Problem and bounded change

The published-alpha usability check’s U09 correctly disclosed unknown version/UI adapter but offered a conditional default-scope configuration before the user confirmed either. This candidate makes explicit uncertainty a clarification step. Models, installed knowledge DB and evaluation remain unchanged.

The model-free repair-layer plan now accepts optional `unresolved_scope`, containing `formly_version`, `ui_adapter`, or both. The calling agent identifies explicit uncertainty; merely absent scope is not uncertainty. Nonempty declarations return `needs_clarification`, `next_action.type=ask_user`, and `user_input_required=true`, without facts or a base retrieval/settings call. Explicit arguments and saved defaults cannot override the declaration. Discovery uses the same gate. Once the user resolves the scope or authorizes a specific hypothetical scope, the caller retains the original request plus clarification context and clears only resolved dimensions.

This is an additive repair-layer schema. Its metadata is removed before forwarding to the existing retrieval contract; old plans retain their behavior. Only three model-free runtime files changed, with corresponding manifest hash updates. The model-backed runtime and DB/model pins were not changed.

## Verification

- TDD: six failing assertions/subcases reproduced the absent clarification contract before implementation.
- 37 focused tests passed, including real stdio feedback, no backend calls while unresolved, explicit-argument override resistance, malformed declarations, discovery propagation, old-plan behavior, supported retry and unsupported stop.
- Full local maintenance checks passed, including both runtime doctors. No hosted model runs or sealed evaluation in that maintenance command.
- Built an isolated local candidate using the unchanged 192-fact DB and the existing clean release dependency environment. All 27 candidate payload hashes remained intact after calls. This was not a new dependency-install test or a published release.
- Eight fresh Codex conversations and four actual resumed follow-up turns ran against that candidate, without tuning or retries during the fixed batch.

| Case | Required behavior | Observed |
| --- | --- | --- |
| C01 | Unknown version and adapter | Asked for both; no advice or retrieval |
| C02 | Material known, version unknown | Asked only for version |
| C03 | 6.3.12 known, adapter unknown | Asked only for adapter |
| C04 | Both dimensions explicitly unconfirmed | Declared both in lookup; received clarification without facts; asked user |
| C05 | Scope simply omitted | Existing default lookup and cited answer preserved |
| C06 | Confirmed 6.3.12 Material | Cited min/max datepicker guidance |
| C07 | Unknown installed scope but explicitly authorized hypothetical | Answered only the requested hypothetical scope |
| C08 | Explicit unsupported 7.0.0 | Stopped without substituting 6.3.12 |
| C01b | Confirm only version | Asked only for remaining adapter; no advice |
| C01c | Then confirm Material | Retrieved min/max evidence, preserving original request and both clarifications |
| C02b | Confirm unsupported version | Stopped as unsupported |
| C03b | Confirm Bootstrap | Stopped as unsupported |

All twelve turns met the frozen interaction criteria in this single Codex pass. No configuration guidance was given in unresolved turns. No general reliability percentage, cross-client compatibility or compilation claim follows from this small development check.

## Review and limits

Independent review: **Ready — no actionable findings.** A fresh-context reviewer independently reran all 37 focused tests and inspected the actual traces and answers for all twelve Codex turns. Frozen criteria were met; reporting and stateless-fetch limitations were confirmed. Package/DB integrity claims were supported by the author’s recorded checks, not separate reviewer asset reads.

The server enforces **declared** uncertainty; it does not detect arbitrary user prose, prove semantic completeness, or independently authenticate a confirmation. A caller that omits the field can still use defaults. `get_formly_facts` has no request/plan or conversation state, so preventing a direct-fetch bypass remains caller policy. Server instructions explicitly prohibit it during uncertainty.

Published `v0.1.0-alpha.1` assets and currently running connections were not replaced. The candidate passed independent review; it is not a new release. Other connections need refreshed runtime instructions after restart or a future package update. Raw cases, scripts and transcripts stay ignored under `test-output/scope-clarification-v1/`.
