# Preliminary independent review

Review instance: 1 of 3.

Blind first pass completed before author explanation. Scope verified: HEAD d5a82fac7d03136137fbafa7c7faeeb15dbfa1c2, branch codex/versioned-knowledge, sole untracked implementation directory versioned_knowledge_v1. Read candidate plan, canonical proposal, all candidate implementation and tests. Graph coverage reports candidate files untracked; direct source is the evidence.

Initial concerns to verify (not yet final findings):

- Replacement overlap checking is pairwise per edge. Verify transitive replacement chains cannot expose conflicting ancestors for one scope.
- Applicability evidence release labels are independently authored catalog metadata; verify the legacy provenance projection preserves enough source identity and quotation checks, including multi-release sources.
- Migration marks every legacy fact direct. Verify accepted baseline relationships and provenance genuinely map, and the exported six semantic tables match.
- Candidate Context routes by adapter only and Backend fixes release 6.3.12. This fits the deliberately single-release provisioned catalog, but verify catalog growth alone cannot silently route a newly accepted release to this backend.
- Synthetic tests cover filtering at Index but do not directly exercise selector admission/repaired citations. Inspect inherited retrieval and selector consumers for bypasses.
- Live receipts, complete baseline preservation, native checks and rollback rehearsal remain to be verified. Passing unit tests alone will not close these requirements.

No implementation changes made. No sealed evaluation accessed.
