# Preliminary independent review

Review instance: 1 of 3. Base d5a82fac7d03136137fbafa7c7faeeb15dbfa1c2; working-tree promotion plus candidate inspected before author explanation. Source fallback used because graph generation 2026-10-25T14:19:41Z predates changes and new modules are unindexed.

- Confirmed defect candidate: runtime recovery allowlist now includes versioned compiler/index, but omits kbcompiler/structured_source.py, which compiler imports at module load and index imports transitively. Copying exactly allowlisted Python files into a clean temporary directory and importing versioned_knowledge_v1.compiler fails ModuleNotFoundError. This is newly a runtime dependency even though full compiler provenance sources deliberately need the source checkout. Needs complete runtime import closure or an explicitly tested overlay recovery contract.
- Source/runtime guards, canonical compiler exclusive publication, exact applicability conversion, pre-ranking eligibility, cross-scope citation rejection and unsupported-release gate appear sound in inspected code/tests.
- Need verify complete rollback evidence: data replacement journal omits changed launcher/server code by design; before snapshot exists, but the coordinated restoration/rehearsal and recorded operational instructions have not yet been inspected.
- Current docs still describe foundation8/legacy compiler; documentation is reportedly being prepared, so defer final assessment until author packet.
- Need independent local checks, canonical semantic comparison and completed stable-launcher smoke receipts before readiness verdict. Test_active factory test only checks planner type, so it alone does not prove installed backend routing.

No implementation edits, commits, sealed archives or hosted calls made. Awaiting separate author packet.
