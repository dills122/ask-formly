# Small Formly agent contract experiment

Implements the user's approved scope: derive Formly library questions from supplied
requests, with no application investigation. This is a prompt/schema experiment,
not a replacement MCP, trained extractor, retrieval engine, or answer generator.

- CONTRACT.md: reusable agent instruction; no tools or application access needed.
- schema.json: exact portable JSON output shape.
- contract.py: standard-library structural validator and prompt builder.
- cases.json: realistic requests only, safe to supply to a trial agent.
- rubric.json: separately authored semantic obligations and forbidden assumptions.
- test_contract.py: positive and negative structural/prompt tests.
- check_trial.py and test_trial.py: complete-case accounting and structural trial checks.
- test-output/: frozen inputs, unedited trial output, validation and reviewed findings.

Use Python 3.10+; no new dependencies. From the repository root:

    python3 -B -m unittest discover -s poc/contextual-kb/agent_contract -p 'test_*.py' -v
    python3 -B poc/contextual-kb/agent_contract/contract.py prompt --request 'How do I register a custom Formly field type?'
    python3 -B poc/contextual-kb/agent_contract/contract.py validate --output /absolute/path/to/output.json

To recheck saved trial coverage and structure:

    python3 -B poc/contextual-kb/agent_contract/check_trial.py --cases poc/contextual-kb/agent_contract/cases.json --trial poc/contextual-kb/agent_contract/test-output/trial-raw.json

The calling agent receives CONTRACT.md as its instruction and the original user
request as data. The prompt command emits a JSON message envelope with those two
parts. It does not call a model. The validate command checks one returned object,
fails closed on extra fields/duplicate keys, and never repairs the output.

Acceptance: all structural checks pass; semantic trial separately checks coverage,
no application investigation, no invented requirements/causes, exact supplied
API/condition retention, and version/adapter scope. A combined question can cover
multiple obligations. Exact strings or keyword presence alone do not prove success.
No claim about answer accuracy, held-out generalization, or inference latency.

All work stays here. Existing A, pilot, training artifacts and sealed evaluation
are untouched. The data/DB is locked. This focused experiment supersedes older
bake-off requirements for this task only; previous results remain evidence.
