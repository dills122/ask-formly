# Isolated MCP reliability candidate

This opt-in candidate addresses MCP availability and source-initial article capitalization. It **does not replace the working setup or installed DB**. It uses the prior isolated56-fact custom-types candidate unchanged, with the accepted planner contract, advisory extractor weights, retrieval and evidence selector.

## Changes

- `capitalization.py`: restore a unique request-opening article's exact capitalization in existing ledger/question copies, then run the original strict validator. No API/literal case folding, missing-condition insertion or general paraphrase acceptance. Automatic repair is limited to single-line prose without code/markup markers; accepted-valid plans remain unchanged.
- `transport.py` and `CALLER.md`: make Formly startup required, wait for its initial catalog, and tell the real caller to invoke the actual exposed namespaced tool. One sequential exact request per call; no retries or other tools.
- `server.py`: isolated composition and startup/stderr evidence. Original runtime modules are imported unchanged; candidate DB identity and foundation assets remain checked.
- `run.py`: fresh output directories and the original strict caller-output audit. Failed/missing results remain in denominators.

## Evidence and limitations

[Diagnosis](DIAGNOSIS.md) records unsuccessful hypotheses as well as successful startup controls. The original outage's exact cause remains unproven. Required startup does not force model tool use; actual MCP events are the success criterion. Fixture markers are transport tests, not Formly answers.

[Plan](PLAN.md) freezes90 exposed regression requests and18 fresh targeted requests before inference. The earlier30-case qualification is now regression material. Existing sealed evaluation is never read. The runs overlap, so latency is descriptive rather than a controlled performance result.

Review1 identified quoted-literal rewriting; review2 identified double-backtick rewriting. Both were reproduced and corrected conservatively. Review3 independently checked the final17-test guard, all108 answers, delivery and preservation. Its final verdict is [Ready for this isolated candidate](REVIEW-3.md).

Development also replayed the actual failed raw Q20 plan through real MCP for both frozen seeds, retrieving the typing fact. Offline final-adapter comparison covered all175 saved raw plans:173 accepted plans unchanged and both old grounding failures repaired. These checks do not replace the repeated live test.

## Reproduce with new output names

From the repository root, use `poc/contextual-kb/mcp_v1/.venv/bin/python -B` with:

```text
-m unittest discover -s poc/contextual-kb/knowledge-expansion/reliability-v1 -p 'test_*.py'
poc/contextual-kb/knowledge-expansion/reliability-v1/run.py --cases poc/contextual-kb/knowledge-expansion/custom-types-v1/qualification-cases.json --name NEW-REGRESSION-NAME --repeats 3 --batch-size 5
poc/contextual-kb/knowledge-expansion/reliability-v1/run.py --cases poc/contextual-kb/knowledge-expansion/reliability-v1/fresh-cases.json --name NEW-FRESH-NAME --repeats 3 --batch-size 3
```

Hosted runs require the existing authenticated Codex CLI and local model assets. Generated files stay under ignored `test-output/`; never use a prior output name. `test-output/freeze.json` pins62 behavior/evidence files before the current run. Original project checks and final preservation passed. Live results: regression30/30 in each of three repeats; fresh6/6 in each of three repeats; zero critical failures and zero delivery errors across108 calls. See [results](RESULTS.md) for limitations and final review status.
