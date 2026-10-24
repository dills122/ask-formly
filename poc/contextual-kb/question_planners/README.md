# Isolated question-planning experiment

Arm A uses spaCy dependency relations; arm B uses LlamaIndex's standalone
LLMQuestionGenerator and local Ollama. Neither imports the existing KB compiler,
queries knowledge, retrieves facts, or answers questions.

From `poc/contextual-kb/`, install only the isolated environment:

```sh
uv sync --project planner_env --frozen --cache-dir planner_env/.cache
PYTHONDONTWRITEBYTECODE=1 planner_env/.venv/bin/python -m unittest discover -s planner_tests
```

Do not run the data compiler or the old data test suite for this experiment.
The new suite uses synthetic cases and development examples only, with mocked
HTTP for transport tests. It does not open sealed cases or contact Ollama.

The reviewed contract and protocol live one directory above. Arm B requires
the exact local model digest recorded in its source and freeze. Library and
parser model versions are locked in planner_env/uv.lock. Worker lifetime and
the hard ten-second deadline are managed by PlannerProcess; initialization
is measured separately. Direct planner.plan calls are implementation internals
and do not enforce the supervisor deadline.

The experiment CLI requires --freeze, --review, --locked and --output paths.
The review receipt must have verdict Ready and freeze_sha256 matching the exact
freeze bytes. It must only be issued after independent review approves those
bytes. There is deliberately no Ready receipt yet: review findings were fixed
but require independent revalidation. Do not open planner_cases/sealed or run
the comparison until that gate passes. No claim of answer accuracy or planner
quality follows from the unit tests.
