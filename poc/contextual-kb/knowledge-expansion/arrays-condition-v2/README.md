# Premise-binding planner qualification

Read PLAN.md before execution. This separate candidate selects condition_candidate_v2 and the unchanged arrays-v1 85-fact DB. It does not build, install, or promote anything.

Run local checks from the repository root:

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/arrays-condition-v2 -p 'test_*.py'
```

After input freeze, qualification uses `experiment.py agents --cases` with this directory's absolute `qualification-cases.json` path, `--name qualification-1 --repeats 3 --batch-size 5`. Assess with `knowledge-expansion/admission/assess_run.py --implementation arrays-condition-v2 --root` pointing to this directory's `test-output/qualification-1`, the same `--cases`, and `--repeats 3 --arms candidate`. Run `evaluate.py --root` against that output for the unchanged numeric gate.

Separately run each of the twelve planner-cases.json requests three times through condition_candidate_v2 wrapped by unchanged CapitalizingPlanner, retaining every raw attempt. All 36 plans require structural and independent semantic passes. Inspect all three original Q20 plans from the answer run for premise-ledger attachment and premise retention in the query. Both gates are mandatory beyond the numeric evaluator. Old 18-probe evidence remains historical. No retries or post-freeze changes.

Original v1 ended Not ready because all three Q20 plans omitted the supplied premise, despite passing numeric answers and 18 probes. This revision preserves that rejection and does not claim success before fresh results and independent review.

Completed qualification: see [RESULTS.md](RESULTS.md) and [REVIEW-FINAL.md](REVIEW-FINAL.md). The candidate remains isolated; no promotion is implied.
