# Condition planner qualification

Separate runtime candidate on the existing arrays-v1 85-fact DB. Read PLAN.md before execution. Original arrays-v1 files, inputs, DB, and results remain frozen; the installed 79-fact DB is unchanged. No build command exists here.

Run from the repository root with the provisioned POC interpreter:

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/arrays-condition-v1 -p 'test_*.py'
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/arrays-condition-v1/experiment.py agents --cases "$PWD/poc/contextual-kb/knowledge-expansion/arrays-condition-v1/qualification-cases.json" --name qualification-1 --repeats 3 --batch-size 5
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/admission/assess_run.py --implementation arrays-condition-v1 --root "$PWD/poc/contextual-kb/knowledge-expansion/arrays-condition-v1/test-output/qualification-1" --cases "$PWD/poc/contextual-kb/knowledge-expansion/arrays-condition-v1/qualification-cases.json" --repeats 3 --arms candidate
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/arrays-condition-v1/evaluate.py --root "$PWD/poc/contextual-kb/knowledge-expansion/arrays-condition-v1/test-output/qualification-1"
```

Before live execution, freeze this harness, the candidate planner/contract/schema, and planner-cases.json. Run the six separate planner-only cases three times each with the candidate planner wrapped by unchanged CapitalizingPlanner. Save every raw attempt and review each against its semantic_checks, including query-local scope and linked follow-up premises. All 18 must pass; retain failures and do not retry. These checks are additional evidence, not part of the 45-answer score. The 1701/1702/1701 seeds configure retrieval/extraction; hosted planner sampling remains unseeded, as before.

Use the admission assessment command above. The copied original summarizer emits both arm placeholders internally; admission --arms candidate removes unused baseline placeholders without modifying the grader or summarizer. No baseline-supported regression claim can be made from this run. The original baseline-supported-regression field in the byte-identical cases is historical; the new evaluator intentionally applies only the candidate gates frozen in PLAN.md.

A passing evaluator still requires independent semantic audit, planner-scope review, and preservation checks. No promotion follows automatically. The prior arrays-v1 44/45 result remains historical and does not establish causality for a difference in this fresh run.

## Completed checkpoint

The answer gate passed 44/45 with all controls/delivery, and 18/18 fresh planner probes passed. Final independent review is **Not ready**: all three Q20 plans omit the supplied internal-export ledger premise. See [results](RESULTS.md), [review](REVIEW-FINAL.md) and [next-revision proposal](NEXT-REVISION.md). Neither runtime nor DB is promoted.
