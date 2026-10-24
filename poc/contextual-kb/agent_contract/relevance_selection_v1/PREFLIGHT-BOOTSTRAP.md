# Fresh review bootstrap
Review instance 1 of3. Use independent-review skill in reviewer mode. Objective: prospective labeling and implementation/design review before retrieval/selection.
Repository /Users/dsteele/repos/ask-formly, dirty main HEAD c3091328f49d53de6b41a49c4fe5aa8f1c45e516. Scope ONLY poc/contextual-kb/agent_contract/relevance_selection_v1; unrelated root changes excluded. All earlier POC artifacts immutable. User explicitly authorizes isolated candidate retrieval and relevance selection experiment. No serving/DB/model changes; sealed evaluation byte-hash only.

Read applicable AGENTS and PROTOCOL.md/SELECTOR.md, then tests/code/raw foundation outputs. Author explanation will be AUTHOR-EXPLANATION.md; do not read it until saving preliminary findings.

First independently label data/requests.json against data/catalog-readonly.json BEFORE any retrieval exists. Save data/cases.json: list in request order, each with id,request,batch,relevant_fact_ids,required_groups (nonempty alternative-ID lists for needed aspects),expected_support ('direct','partial','unsupported'), rationale,partial_missing_parts. Unsupported means empty relevant/groups. Relevant includes material corroboration, not generic matching vocabulary. Do not invent support beyond the supplied catalog. Review data/records.json against frozen qualification_v3/CONTRACT.md; save data/semantic-review.json list {id,foundation_pass:bool,issues:[...]}. Do not repair outputs.

Implementation is still being completed. After labels/semantics, notify parent and WAIT for its code-freeze signal before reviewing implementation. Do not run retrieval/selection. Own only above label/review files, PREFLIGHT-PRELIMINARY.md, PREFLIGHT-REVIEW.md,PREFLIGHT-DECISION.json and test-output/preflight-*; code read-only. You are not alone; no other edits.

Graph Tier2 ask-formly index October16 is stale/not watching POC. Parent search_graph PilotIndex/merge_obligations returned0; coverage of question_pilot.py, context_queries_v1/candidate.py, merge_slots_v1/run.py/metrics.py, retrieval_integration_v1/bridge.py, qualification_v2/execution.py,qualification_v3/candidate.py all not_tracked. Exact source fallback used; check coverage for your additional evidence paths and read source directly. Do not reindex.

After code ready: run proportionate tests, independently check label validity and protocol, report before next review. Max3instances total, no new agents or workstreams. Return verdict ready/not ready with evidence and exact blockers. Do not treat failing semantic outputs as code fixes; keep them counted.
