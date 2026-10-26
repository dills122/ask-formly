# Dual-mode packaging verification

Both implementations are retained. New launcher defaults to model-free; `--mode model-backed` explicitly selects the unchanged foundation9 implementation. Existing live client configuration is untouched.

- Seven launcher tests passed after initial TDD import failure.
- Both doctor checks passed: model-free 17 pinned files; model-backed 95 pinned files plus existing worker checks. Doctor does not qualify hosted access.
- Model-free stdio smoke passed lookup, discovery and full-fact fetch under the existing test-only import/network/subprocess guard. This is a Python test guard, not an OS security certification.
- Model-backed stdio smoke passed a real lookup, returning facts, citations, advisory metadata and selection metadata through the retained internal model/provider path.
- Full `python3 tools/project.py check` passed. Initial failure was an outdated expected test-suite list, fixed to include the new launcher tests.
- Initial backed smoke failed before lookup because the test expected only lookup, omitting the server's existing get/set project-settings tools. The expectation was corrected; timestamped retry preserved the initial artifact and passed.
- 808 prior freeze entries checked unchanged, excluding seven intentionally edited setup/docs/maintenance-check files. Existing candidates, models, DB and live client configuration unchanged. Sealed evaluation remained unopened.

Receipts and full outputs are in ignored `test-output/`. These smoke checks establish dispatch and transport behavior, not new answer-quality or performance scores. Prior bounded native and paired qualification remains documented separately. No commit, push or live client reconfiguration performed by this change.

Independent review instance 1 of 3: **Ready**, no actionable findings remaining. See [review](REVIEW.md). The smoke output-parent correction was verified by a successful free-mode replay.

## Publication checkpoint

The user subsequently authorized docs, commit/push and PR publication. Current setup is now explained in `docs/runtime-modes.md`; concise history is in `docs/history/model-free-transition.md`. The explicit publication set includes serving dependencies and fixture regressions, excluding private assets, local client config and unfinished JSON Schema experiments.

Full maintenance passed again (183 source tests and 149 existing runtime tests). An exported staged tree passed source checks and 34 additional model-free/repair/discovery tests using existing dependency environments, without private DB/model assets. The initial export attempt used only the MCP environment and lacked the compiler's markdown-it dependency; providing the separate compiler environment resolved that test-setup failure.

Publication review instance 2 of 3 returned **Ready**, no findings: all 16 non-DB runtime pins were present and hash-matched in the index, current links resolved, and no private assets were staged. This packaging does not expand the earlier runtime-quality claims.
