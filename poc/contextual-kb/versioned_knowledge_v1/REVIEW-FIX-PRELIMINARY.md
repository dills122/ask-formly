# Preliminary independent review

Review instance: 2 of 3.

Inspected the neutral bootstrap, canonical proposal and candidate plan before the author explanation. The assignment disclosed the prior transitive-overlap finding and claimed remediation, so this is fresh source verification rather than a completely blind review.

Ground truth: branch codex/versioned-knowledge, HEAD d5a82fac7d03136137fbafa7c7faeeb15dbfa1c2; sole untracked scope versioned_knowledge_v1. Read candidate compiler, all tests, index/backend/context/server, qualification, verification and smoke scripts. Graph Tier 2 has no candidate symbols and reports all 11 candidate Python files untracked; direct source is the basis for conclusions.

No actionable defect found in the first pass. The DFS now computes and memoizes the full ancestor set, detects cycles before memoization and checks applicability overlap against all predecessors. The regression uses exact 6.3.12 -> major 7 -> major 6 and asserts rejection without publication. Existing direct overlap/cycle and valid disjoint-chain coverage remains. All 13 candidate unit tests passed.

Whole candidate review: schema 2 publication is exclusive; migration preserves exact scopes; source validation delegates to the preserved compiler; eligibility restricts dense vectors, SQL lexical candidates, links, selector candidates and citations. Accepted catalog gates the opt-in backend to 6.3.12. Installed integration is deliberately excluded. The plan explicitly defers ambiguous overlapping replacement boundaries and promotion.

Pending before verdict: verify author claims against raw live/native receipts, independent preservation and semantic comparisons, and maintenance outcome. Operational smoke is not answer-quality or unseen-evaluation proof. Promotion and broader release coverage remain separately authorized work.
