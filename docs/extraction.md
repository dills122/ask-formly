# Standalone extraction — 2026-10-15

The owner requested the same standalone-repository treatment as Angular Usage Lookup. Target: /Users/dsteele/repos/ask-formly. Research Depot retains its pre-extraction snapshot; ongoing work belongs here. No source Git history could be split because the source files were uncommitted.

All 452 original source/evidence files were copied, excluding only Python bytecode caches. Their pre-extraction hashes are in [the source manifest](extraction-source-manifest.json). The current graph test's default compiler path was adapted to this repository's node_modules; original skill and runtime fixture sources are unchanged. Historical raw paths, logs, scorecards, failed cases and hashes remain untouched.

Added current onboarding/development/handoff documentation, project-owned instructions, a root TypeScript development lock, deterministic ZIP tooling, packaging tests, optional AI Central setup and prepared CI/draft-release workflows. Copied the pinned upstream source cache into ignored local storage. Large old dependency/build folders stay in Research Depot; the standalone root initially reused TypeScript 5.9.3 for validation, then successfully performed a clean locked npm ci with lifecycle scripts disabled using the existing offline npm cache. No network or global installation was needed.

The extraction does not change Formly/Angular/Material dependencies or semantic behavior. It does not install the skill globally, migrate the workplace app, select a new license, commit, create a remote or publish.

## Validation

The machine-readable [relocation result](extraction-validation.json) records actual final-path checks. Earlier AOT/browser/agent results remain historical; they were not rerun merely to copy files. The browser suite's two failures remain visible. Hosted GitHub Actions and the draft-release workflow have not executed.
