# Model-scope knowledge batch

Isolated60-fact candidate against installed56-fact foundation2. Four source-backed additions explain built field links, keyless group sharing, keyed nested models and leaf enclosing model scope. Existing compiler/retrieval/planner/models unchanged. No sealed evaluation.

[Plan](PLAN.md), [source review](REVIEW-2.md), [authored facts](draft-authored/model-scope.json), [fixed cases](qualification-cases.json). Status: built and tested; candidate 45/45 versus baseline 18/45 across three repeats, with 45 successful paired replays. Independent review: [Ready](REVIEW-FINAL.md). See [results](RESULTS.md). The installed DB remains56facts.

Reproduction uses the existing MCP Python environment. Run test_candidate.py/test_experiment.py via unittest discovery. candidate.py deliberately refuses existing outputs; do not rerun build into existing directories. experiment.py agents --cases qualification-cases.json --name NEW-NAME --repeats 3 --batch-size 5 requires hosted access, and uses fresh outputs. The exact current command is preserved in per-job command.json. Paired replay reuses saved normalized plans and retains the hosted selector. Results are diagnostic, not whole-library accuracy.
