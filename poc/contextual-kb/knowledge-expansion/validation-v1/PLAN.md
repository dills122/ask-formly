# Validation and error messages — admission start

Status: source mappings and nine proposed facts across two draft documents prepared for independent prebuild review. Expected isolated candidate:79facts/17documents. No new authored facts, candidate DB, installed writes or model changes. The accepted baseline is foundation5:70facts/15documents, with the reviewed merged project-settings runtime. Evaluation remains sealed.

## Proposed first batch

1. Named boolean expressions versus Angular-style null/error-map validator contracts.
2. Typed registered validators versus the runtime's boolean tolerance; do not recommend casts to hide a typing mismatch.
3. Built-in required/pattern/minLength/maxLength/min/max adaptation and prop changes; avoid inventing validators for arbitrary props.
4. Validity versus error visibility: invalid plus touched, submitted or validation.show under the default display rule.
5. Field/global message configuration and matching error names. Exact precedence and length-key compatibility need direct pinned-source verification before admission.
6. Promise/Observable boolean expressions versus Angular async return contracts, with no invented network/error/cancellation policy.
7. Group validator placement, registration and errorPath in the matching-fields example.

These are review topics, not a promised fact count. Split into independently useful claims only after evidence review. Existing70facts mention validation as control state but contain no dedicated validator/message contracts, based on canonical authored-record inventory.

## Evidence and exclusions

Inventory validation.md using its unchanged source hash and four direct-heading sections. K04,K08,K26,E03/E03a,E04/E04a/E04b are already in the catalog; their presence is not independent confirmation of each proposed claim. Recheck exact pinned source ranges and public typing before drafting. Preserve the source text and catalog unless an isolated candidate explicitly needs reviewed new evidence.

Exclude application-inspection instructions, domain-specific validation policy, production HTTP behavior and claims of executed upstream tests. The guide's stale routed-error discussion references historical evaluation evidence: do not open that artifact. Defer that claim until it can be established from permitted pinned source or a new bounded public probe. Do not infer all sibling-edit/async transitions from examples.

## Ordered process and gates

1. Complete claim-level source decisions and independently review source mappings/proposed records. Pending decisions stay pending; never mark a section admitted because inventory generation passed.
2. Write development questions and meaningful tests for any newly required admission mechanism using TDD. Reuse current compiler/admission/eligibility mechanisms; no runtime redesign or training planned.
3. Freeze canonical baseline hashes, candidate authored/evidence inputs, and a fresh fixed15-question qualification set before building:10targeted and5old regression/gap controls. No sealed questions. Do not reuse development questions for the decision.
4. Build isolated candidate, lint provenance/quotes/links, verify runtime eligibility and preservation of all five accepted tables; independently review before live inference.
5. Compare baseline and candidate through real calling agents, three repeats with seeds1701/1702/1701 and counterbalanced order. Use the explicitly authorized lookup-only caller policy established by promotion-v4; freeze the harness and criteria before use. Run45 matched-plan retrieval diagnostics separately from answer scoring.
6. Require at least14/15 usable answers per candidate repeat (small-set resolution is93.3%, satisfying the90% goal), all five controls each repeat, no critical/delivery failures, and no regression on baseline-supported cases. Report every failure and per-case stability; do not tune during qualification. If a materially larger set is chosen, freeze the denominator and threshold first.
7. Independent outcome review, hash/reproduction checks and a concise result. Installation is a separate explicit promotion decision; this batch starts with the70-fact installedDB locked.

## Repeatable inventory commands

From repository root:

```sh
python3 -B poc/contextual-kb/knowledge-expansion/admission/ledger.py inventory --manifest poc/contextual-kb/knowledge-expansion/validation-v1/source-manifest.json
python3 -B poc/contextual-kb/knowledge-expansion/admission/ledger.py check --manifest poc/contextual-kb/knowledge-expansion/validation-v1/source-manifest.json --ledger poc/contextual-kb/knowledge-expansion/validation-v1/ledger.json --authored-dir poc/contextual-kb/authored
python3 -B poc/contextual-kb/knowledge-expansion/admission/ledger.py report --manifest poc/contextual-kb/knowledge-expansion/validation-v1/source-manifest.json --ledger poc/contextual-kb/knowledge-expansion/validation-v1/ledger.json --authored-dir poc/contextual-kb/authored
```

Do not overwrite reviewed decisions with a regenerated inventory skeleton. A passing check with complete:false means structurally valid pending work, not qualified knowledge.

## Prepared inputs

See proposed-source.md for source-to-fact decisions and exclusions, source-verification.json for eight pinned upstream hash comparisons, and harnessREVIEW-AUTHOR.md for the isolated runtime composition and10fixturetests. The15qualification cases and five separatedevelopmentcases are fixed before any live experiment. All166protected baseline files and installed70DB are checked by baseline-state.json. No existing candidate, runtime, canonical authored input or catalog has changed.

## Decision command

After all three repeats are assessed, apply the frozen criteria without manual score selection:

```sh
python3 -B poc/contextual-kb/knowledge-expansion/validation-v1/evaluate.py --root poc/contextual-kb/knowledge-expansion/validation-v1/test-output/qualification-1
```

The decision artifact is exclusive and includes failed gates. Baseline quality/critical errors are reported diagnostically; both arms must have complete delivered results for a valid comparison. Candidate quality gates and per-repeat baseline-supported regressions determine qualification. The evaluator adds six red/green tests, bringing batch fixtures to16.
