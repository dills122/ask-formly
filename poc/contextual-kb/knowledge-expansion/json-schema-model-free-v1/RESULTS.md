# JSON Schema model-free qualification

The corrected comparison passes the frozen semantic and protocol gates. No installed promotion or publication has occurred.

## Independently audited result

| Repeat | Installed 93-fact DB | Isolated 99-fact candidate | Candidate controls |
| --- | --- | --- | --- |
| 1 | 5/15 usable | 15/15 usable | 5/5 |
| 2 | 5/15 usable | 15/15 usable | 5/5 |
| 3 | 5/15 usable | 15/15 usable | 5/5 |

No critical unsupported claims or baseline-supported regressions were found.
Both the semantic gate and mechanical audit pass. The 30 unique authored answers
were separately adjudicated and identical repeat evidence was verified before
applying the same judgments to the 90 observation slots.

Initial semantic support was **14/15 candidate versus 5/15 baseline** per repeat.
The full initial citation text already supported C02 (resetOnHide:false) and J10's
bounded rejection of universal reference/rendering coverage, even without their
canonical fact IDs. Those later fetches supplied explicit detail but were not
necessary to establish that support. J09 needed the conversion-result-shape fetch
in addition to its initial customization/order facts. Fact-ID coverage alone would
have understated initial support.

This qualifies the six-fact addition for a separate guarded promotion decision;
it is not a whole-library accuracy claim, independent-generation benchmark or
permission to overwrite the installed DB. The recommended next step is reviewed
promotion of this exact candidate and coordinated manifest updates for both modes.

## Scope and unchanged baseline

The branch `codex/json-schema-model-free` starts from merged main `15cb3e4`.
The existing isolated candidate has **99 facts / 22 documents**, adding six facts
to the installed **93 facts / 21 documents**:

- JSON Schema conversion API, cloning and result shape.
- Conversion versus renderer registration, with the Bootstrap/Material boundary.
- `widget.formlyConfig`, props aliasing and `map` ordering.
- The `map` return contract.
- Local reference resolution and its limits.
- Remote reference rejection rather than fetching.

Candidate SHA256: `8487ca97dde24daff0a9dc655111e0066b7f3ce0dccf7c65d81f6f6087fa3c6c`.
Installed SHA256: `a0f102f1bad83dfec7c91148925187644e3092a3ca08cdaa88f586a7e1a0c106`.

Both hashes, candidate inputs/source offsets, eight-table baseline superset and
exact 6.3.12 applicability were verified before testing. No DB was rebuilt.
Both runtime implementations and models remain byte-preserved; evaluation is sealed.

## What actually ran

The original 15 visible development requests were retained: ten JSON Schema asks,
three existing-library controls and two honest-gap controls. Each arm used the same
complete-request plan, with batches of five and three repetitions. The experiment
injected only the DB path/hash into the existing model-free service factories.
Actual MCP SDK stdio calls ran under the existing test-only offline guard. There
were no server model calls, external caller CLIs, application inspection or native
candidate-client reconfiguration.

The root calling agent read results, selected discoveries/fetches and authored
30 distinct answers. Repeats retained answers only after verifying exact fresh
full-fact/citation equality. **90 observation slots are not 90 independent answer
generations.** This is a fixed-plan data comparison and repeat-consistency check;
it does not newly qualify open-ended planning or generalization. The author had
seen the visible case criteria. Separate-context answer review does not erase that
limitation. Sealed evaluation was not used.

## Retained failure and correction

The first complete run made 165 calls with no operational errors, but candidate
J10 fetched with an omitted adapter after a Material-scoped lookup. That same
caller mistake occurred in each repeat. The delivered fact was core-scoped, but
same-scope protocol failed. Its mechanical audit remains `passed:false`, with
three scope failures. Nothing was removed from its denominator or overwritten.

A new caller-only helper copies the actual resolved version and adapter. Two TDD
checks cover this correction. Independent review instance 2 approved one complete
fresh run with unchanged facts, plans, discovery budgets and grading criteria.
See [correction](CORRECTION.md); the initial run remains under `test-output/r1`–`r3`.

The corrected run is separately stored under `test-output/corrected`. It made
**165 calls: 84 lookups, 66 discovery calls and 15 full-fact fetches**, with zero
operational/delivery errors, zero missing planned calls and zero scope mismatches.
There are six explicit no-call observations for the private application-path
control, which are not counted as successful MCP deliveries.

All quoted/cited records were checked against the selected DB. Fetch IDs had been
observed in that case's real results; citations required full delivery. The same
records and citations appeared across repeats. Tool timings exclude caller
reasoning and startup, so no end-to-end speedup is claimed.

## Verification and review

- Eleven experiment helper tests passed after recorded TDD failures.
- Pre-run review caught and resolved the isolated guarded-entry import bug.
- Full project maintenance passed before and after the run.
- 846 preservation entries and the original/correction freezes remain unchanged.
- No tracked runtime files changed; all new work stays in this experiment directory.
- Pre-run review: [instance 1](REVIEW-1.md), Ready for testing.
- Correction review: [instance 2](REVIEW-2.md), Ready for the corrected run.
- Final semantic/provenance review: [instance 3 of 3](FINAL-REVIEW.md). The independent grades and combined decision are retained under test-output/corrected.

The earlier model-backed JSON Schema delivery failures remain failures in their
original records. This experiment does not claim that those provider issues were
fixed; the tested server path makes no such internal hosted calls.
