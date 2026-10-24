# Question-layer candidate v3

This separate POC candidate adds an auditable condition-to-question map and optional role hints. It does not modify v2 or run a model, retrieval, DB, application investigation or answer assembly.

`candidate.build_messages(request)` packages CONTRACT.md and the verbatim request. After a calling agent produces JSON, `candidate.parse_output(request, text)` validates the candidate structure and declared condition bindings. `candidate.build_plan(request, output, hints=None)` returns:

- `question_plan`: independent copy of complete questions, reasons, global constraints and condition bindings.
- `search_requests`: verbatim question strings as `query` fields; no role filters or rewriting.
- `hint_policy`: `advisory_only`.
- `role_hints`: optional structurally checked hints, each with `usable_as_filter: false`.
- `hint_warnings`: explicit diagnostics for ignored malformed or overlapping hints.

A supplied hint has exactly question_index,start,end,text,role. Indices are zero-based and offsets are Python Unicode code points within that question. Missing hints are allowed. Unknown roles, bad slices, out-of-range indices and all overlapping/duplicate hints are ignored without changing or rejecting a valid core plan. A structurally accepted hint can still have a wrong role or refer to an excluded adapter; it is never an authoritative constraint. Invalid core plans fail validation regardless of hints.

Condition bindings contain an exact source `condition` excerpt and its `question_indexes`. Every declared target must repeat that excerpt. This enforces declared coverage only: omission from the ledger, wrong semantic attachment, trivial excerpts or source retractions require semantic review. The model must identify active shared versus local conditions and resolve corrections; the validator is not a condition extractor.

Run focused tests from repository root:

```sh
python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/refinement_v3 -p 'test_*.py'
```

See PROTOCOL.md and RESULTS.md for the actual generation trial, independent review, limitations and preservation checks. All generated search requests are unexecuted; no retrieval/answer-quality or production guarantee is claimed.
