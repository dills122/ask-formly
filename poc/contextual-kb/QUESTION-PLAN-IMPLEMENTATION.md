# Question planner implementation handoff

21 October 2026. Review instance 3 returned Not ready. Both findings have been
corrected with tests; independent revalidation requires an increased review
budget. Held-out comparison has not run, and the set remains sealed.

## Neutral review bootstrap

Review instance 3 of 3 in the existing independent-review flow. Repository
`/Users/dsteele/repos/ask-formly`, branch `main`, baseline HEAD
`c3091328f49d53de6b41a49c4fe5aa8f1c45e516`. Broad pre-existing dirty working tree;
the POC itself was already untracked. Scope is new `question_planners/*.py`,
`planner_tests/*.py`, `planner_env/pyproject.toml`, `planner_env/uv.lock`, public
development cases and commitments, and this handoff. Exclude vendored environment
and cache contents from code review. Do not open `planner_cases/sealed/`.

Canonical requirements are STEERING.md, QUESTION-PLAN-CONTRACT.md and
QUESTION-PLAN-EVALUATION.md plus the user's authorization to implement A/B
using TDD and get an implementation review before comparison. Data/DB locked;
no other project code reuse; no serving or downstream changes.

Exact implementation hashes are in `planner_cases/implementation-freeze.json`.
Read code/tests before the author explanation below. Review is read only.
Run only the new suite from this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 planner_env/.venv/bin/python -m unittest discover -s planner_tests
```

No DB compilation, old test suite, broad source scan of sealed cases, or
comparison execution. Local-model smoke results already exist under repository
`test-output/question-ab-20261021/`; do not repeat timing during another run.

## Author explanation (read after preliminary review)

The shared strict Pydantic contract validates shape, bounds, references and
status. It does not claim semantic correctness. A uses trained spaCy dependency
coordination projection and original token spans. Its general syntax rules are
documented in syntax.py: top-level coordinated predicates/objects, shared
grammatical context, preserved comparison/disjunction, and unresolved deixis.
No Formly concept lexicon or old planner imports exist. The rule set is limited;
pronoun resolution and complex shared attachments remain weaknesses to measure.

B instantiates only LLMQuestionGenerator with explicit Ollama configuration,
one ToolMetadata description and a recording native output parser. It performs
one generation, with HTTPTransport retries=0; unknown native fields are checked
before Pydantic could discard them. Prefix decoding is nonsemantic. The model
has no executable tools. JSON output, native rows and errors remain in trace.

The parent process imposes a deadline on sending input, receiving output and
validation. A timed-out worker is killed and not automatically retried. Workers
load once; an audit guard prevents question-time reads of KB/data/case paths,
SQLite connections, command execution and nonlocal network connections. The
guard is defense in depth, not an OS sandbox or a guarantee against malicious
installed packages. No database handles enter either planner.

The experiment runner requires a Ready receipt matching the freeze hash before
opening held-out cases. It preserves every sample, alternates paired ordering,
separates startup/model preparation, creates method-blind grading artifacts and
retains invalid partial runs. After the review correction, stopped workers
are replaced before their next scheduled sample; the failed sample is never
retried. Recovery startup, development warmup and total overhead are recorded
separately, and the next sample is marked after recovery. Failed recovery
invalidates the run. This has been tested synthetically, not on held-out cases.

## Verification and limitations

Contract, B adapter, A parser, runner and experiment tests were added before
their modules, with retained red/green outputs. A later regression reproduced
and fixed a blocking-input-write deadline defect. Additional transport tests
exercise actual LlamaIndex/Ollama code with controlled HTTP responses; they
prove single-request handling, not real semantic quality.

Development-only real library/model smoke evidence:

- `10-development-smoke.json` retains the initial run, including excessive B
  paraphrase requests and missed ambiguity. This is not qualification.
- `11-prompt-red.txt` reproduced doubled JSON-example braces; LlamaIndex's
  SafeFormatter does not unescape Python-style doubled braces. Fixed and tested.
- `13-development-compatibility.json` confirms real B search and ambiguity
  outputs after the correction and two generic examples. D01 still merges
  two requested outcomes; this quality failure remains visible. No adapter
  repair or case-specific correction was added.
- `17-final-suite.txt` is the final pre-review suite result. Frozen source/DB
  checks are in `locked-before.json` and `locked-after-implementation.json`.
- `19-recovery-behavior-red.txt` reproduces review finding P1 using synthetic
  samples; `20-review-fixes-green.txt` passes 33 tests after the corrections.

The original reviewed freeze is retained separately under test-output as
`implementation-freeze-reviewed.json`. The current freeze includes corrected
code/protocol and `planner_cases/runtime-environment.json`. That manifest
records host hardware and explicit unavailable server settings; the runner
also captures actual Ollama model/device-memory state at runtime. No Ready
receipt exists for the corrected freeze. The prior review verdict cannot be
treated as approval of these changes.

Dependencies are isolated from the original compiler environment and locked
in `planner_env/uv.lock`: spaCy 3.8.16, en_core_web_sm 3.8.0,
llama-index-core 0.14.25, llama-index-llms-ollama 0.9.1, Pydantic 2.14.1.
The local Qwen model tag and digest are pinned in llama.py and the freeze.
No package installations, source imports or copied implementations came from
other project experiments. Generic library code comes from third-party packages.

Development timings ran alongside occasional unit checks and are not qualified
latency numbers. The experiment's cold worker start is separate from local-model
loading; an already loaded model is not falsely described as a fresh cold load.
Product latency acceptance remains undecided. No answer accuracy is measured.

The sealed case author independently froze 30 cases and returned only metadata
to the implementer. No held-out case or output has been inspected by the author.

## Reviewer challenge points

Check failure classification, strict native parsing, deadline coverage, replay
gates, absence of hidden retries or outside project imports, whether the tests
match the contract, and whether any experimental limitation is concealed.
The three-review flow is exhausted; ask the user to authorize an additional
fresh review before issuing a Ready receipt or executing the comparison.
