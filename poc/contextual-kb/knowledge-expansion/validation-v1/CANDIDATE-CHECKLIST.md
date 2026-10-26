# Source admission checklist

Generated from the reviewed ledger. Mechanical completeness is not proof that every semantic claim was correctly interpreted.

Section counts: admitted=3, excluded=1, existing_support=0, pending=0.

## formly.validation

Source: `skill/ask-formly/references/validation.md`; SHA-256 `a55d59a477967b51e8bb6d82831f02389ed52de858e4313807233a98e1d414cd`.

- [x] **Validation** (lines 1–4) — excluded. All assertions in this section are accounted for by qualified candidate facts or explicit exclusions. This is isolated candidate coverage, not installed or whole-library coverage.
  - Source inspection is not runtime qualification — **excluded**; facts: none. Retain scope and do not claim executed upstream tests.
- [x] **The two return contracts** (lines 5–29) — admitted. All assertions in this section are accounted for by qualified candidate facts or explicit exclusions. This is isolated candidate coverage, not installed or whole-library coverage.
  - named-boolean-expression — **admitted**; facts: `validation-contracts/named-boolean-expression`. The mapped source assertion is represented by these reviewed facts in the isolated79-fact candidate. Source conditions/limits are retained. The candidate passed45/45 answers and45matched-plan replays; no installed promotion is implied.
  - registered-validator-contract — **admitted**; facts: `validation-contracts/registered-validator-contract`. The mapped source assertion is represented by these reviewed facts in the isolated79-fact candidate. Source conditions/limits are retained. The candidate passed45/45 answers and45matched-plan replays; no installed promotion is implied.
  - registered-boolean-tolerance — **admitted**; facts: `validation-contracts/registered-boolean-tolerance`. The mapped source assertion is represented by these reviewed facts in the isolated79-fact candidate. Source conditions/limits are retained. The candidate passed45/45 answers and45matched-plan replays; no installed promotion is implied.
  - message-configuration — **admitted**; facts: `validation-contracts/message-configuration`. The mapped source assertion is represented by these reviewed facts in the isolated79-fact candidate. Source conditions/limits are retained. The candidate passed45/45 answers and45matched-plan replays; no installed promotion is implied.
  - Historical compiler result and application-inspection advice — **excluded**; facts: none. The public typing is admitted as a proposed contract; no historical compiler execution is newly claimed.
  - Application-specific investigation — **excluded**; facts: none. Application investigation is outside the library knowledge service.
- [x] **Built-ins and messages** (lines 30–35) — admitted. All assertions in this section are accounted for by qualified candidate facts or explicit exclusions. This is isolated candidate coverage, not installed or whole-library coverage.
  - builtin-prop-validators — **admitted**; facts: `validation-contracts/builtin-prop-validators`. The mapped source assertion is represented by these reviewed facts in the isolated79-fact candidate. Source conditions/limits are retained. The candidate passed45/45 answers and45matched-plan replays; no installed promotion is implied.
  - length-error-key-compatibility — **admitted**; facts: `validation-contracts/length-error-key-compatibility`. The mapped source assertion is represented by these reviewed facts in the isolated79-fact candidate. Source conditions/limits are retained. The candidate passed45/45 answers and45matched-plan replays; no installed promotion is implied.
  - default-error-visibility — **admitted**; facts: `validation-contracts/default-error-visibility`. The mapped source assertion is represented by these reviewed facts in the isolated79-fact candidate. Source conditions/limits are retained. The candidate passed45/45 answers and45matched-plan replays; no installed promotion is implied.
  - Message configuration surfaces — **admitted**; facts: `validation-contracts/message-configuration`. The mapped source assertion is represented by these reviewed facts in the isolated79-fact candidate. Source conditions/limits are retained. The candidate passed45/45 answers and45matched-plan replays; no installed promotion is implied.
- [x] **Async and cross-field behavior** (lines 36–42) — admitted. All assertions in this section are accounted for by qualified candidate facts or explicit exclusions. This is isolated candidate coverage, not installed or whole-library coverage.
  - Async result contracts — **admitted**; facts: `validation-contracts/async-expression-result`. The mapped source assertion is represented by these reviewed facts in the isolated79-fact candidate. Source conditions/limits are retained. The candidate passed45/45 answers and45matched-plan replays; no installed promotion is implied.
  - Matching-fields example core mechanism — **admitted**; facts: `validation-group-example/group-errorpath-registration`. The mapped source assertion is represented by these reviewed facts in the isolated79-fact candidate. Source conditions/limits are retained. The candidate passed45/45 answers and45matched-plan replays; no installed promotion is implied.
  - Historical routed-error probe and universal cleanup guarantees — **excluded**; facts: none. Historical evaluation artifact remains unopened. No observed probe result is imported; arbitrary routed-error cleanup remains explicitly unguaranteed.
  - Application runtime regression advice — **excluded**; facts: none. Advice is retained as a testing boundary, not a new library behavior fact or executed runtime claim.

