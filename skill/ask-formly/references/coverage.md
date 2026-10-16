# Coverage and confidence

Baseline: ngx-formly **6.3.12**, source commit `5f099fddea6426b46a453866adf0fede5be0bcd7`, accessed 2026-10-15. The expanded corpus combines source inspection, 25 issue conversations, four reviewed fix patches, 17 original behavior probes in Zone-based and zoneless modes, and scoped strict AOT/Chromium execution. It is not a claim of universal expertise.

## Evidence map

| Area | Current depth | Remaining boundary |
| --- | --- | --- |
| API/configuration | Declarations, setup, registries, key/model/control scope, merging, clone behavior, parsers/updateOn/debounce, events | App factories and other patches need their own context |
| Expressions/lifecycle | Evaluator, stream ownership, field versus type lifetime, state observation, version changes, executed disabled-path migration comparison | Complex cross-field cycles and all lifecycle combinations unqualified |
| Validation | Return contracts, messages, async guidance; named/anonymous routed-error cleanup probe | Real HTTP error/cancellation and server error lifetime unqualified |
| Arrays | Builder/add/remove/default paths, historical fixes, falsy initial-value probe | Arbitrary row identity/reordering and complex branches need browser/app tests |
| Customization | Types/wrappers, priority, presets, attributes; public registration type AOT correction | Complex composite controls and recursive preset composition unqualified |
| Material | Input, textarea, select, checkbox, multicheckbox, radio, toggle, datepicker, legacy/MDC slider, native-select source contracts | Native en-US dates, selected focus and layout checks executed; open-select option replacement fails; other adapters and full accessibility/visual behavior unqualified |
| JSON Schema | Full converter paths read, including parsers, dependencies, composition, enum, arrays, refs; basic conversion/rejection and selected pattern/enum/composition probes executed | Not a Draft 7 conformance suite or a guarantee of nullability/branch semantics |
| Patterns | 24 choices with anti-patterns and concrete verification scenarios | Recommendations are contextual, not universal upstream requirements |
| Bug history | 25 cases, 85 comments, four exact fix diffs read; version contradictions retained | No exhaustive issue census; most reported reproductions not run |
| Examples | 13 official walkthroughs across 20 source files | Walkthroughs are source-read, not complete verified application recipes |
| Runtime | 17 Zone-based + 17 zoneless JIT probes pass; strict AOT passes; 12/14 Chromium cases pass on Angular 21.2.25 / Material 21.2.14 / Formly 6.3.12; three supplemental JIT and three RxJS virtual-time checks pass | Two retained select failures; close/reopen recovery passes; no full cross-browser/HTTP qualification |
| Answer quality | Initial pilot: both 8/8. Source-only-designed blind follow-up: both 5/6; both custom Material answers fail an unavailable TypeOption import. Public-type repairs and a fresh custom control pass AOT/browser; two additional corrected-topic variants pass source review | No demonstrated comparative advantage; small development samples, partial masking, no unseen consuming-project validation |

The source manifest has **84 records across 74 unique files**: 64 API/implementation/guide/test excerpts and 20 example-file records. Counts measure traceability, not completeness. [Evaluation lessons](evaluation-lessons.md) route tested corrections; [evaluation-evidence.json](evaluation-evidence.json) retains compact observations and artifact hashes. Full audits stay outside the portable skill.

## Evidence levels

- **Source-read:** declaration, implementation, guide, spec, or example inspected. A test source establishes an assertion, not a passing execution. The source manifest keeps this status even when a related custom probe ran.
- **Conversation report/advice:** distinguish reporter observations, community suggestions, maintainer guidance, and released fixes. Use exact comment links and dates where available; closure is not a fix claim.
- **Inference/recommendation:** derived design guidance with scope and alternatives. Do not silently upgrade it to an upstream rule.
- **Executed observation:** tied to the named R01–R17 probes or B01–B14 browser cases and explicit environment. See [runtime evidence](runtime-evidence.md) and [Angular 21 qualification](angular21-qualification.md). R11/R14 characterize limitations; passing means those limitations were observed.

The [E2E analysis workflow](e2e-analysis.md) is proposed guidance for an invoking test builder. End-to-end test generation speed, first-run success and repair effort on unfamiliar consuming-project forms have not been measured.

## Important unresolved work

The owner's application and exact dependencies remain unknown. Full browser behavior, accessibility, appearance, performance benchmarks, date adapters beyond the selected native en-US case, real HTTP races, SSR/hydration, complex array identity, JSON Schema conformance, all v6 patches, and custom application components are not qualified. Source knowledge covers some of these areas, but source inspection is not execution. The comparisons do not establish better answers or lower effort. Earlier C03/C08 sketches were not separately compiled; later tests do not retroactively certify them.

## Maintenance

1. Preserve the immutable baseline. Add a separate version boundary when evidence differs instead of silently changing old citations to a moving branch.
2. Read matching declarations/implementation and relevant tests/examples for a new rule. Record commit/path/line bounds/hash/access date/status in evidence.json and its readable index.
3. For a conversation, retain issue metadata, precise comment links, known/reported versions, fix evidence, and unresolved contradictions. Do not retain full copied conversations in the portable skill.
4. Write a concise operational lesson: when it applies, what to do/avoid, and which transition would verify it. Keep generic framework tutorials out of the entrypoint.
5. Run source/hash/link/package checks. Promote a behavioral claim only with explicit execution evidence on declared versions.
6. Keep private project knowledge in a project-owned overlay. A source graph is optional; use direct reads/search for excluded docs, examples, and tests.

Primary navigation: [patterns](patterns.md), [API contracts](api-contracts.md), [bug ledger](bug-ledger.md), [runtime evidence](runtime-evidence.md).
