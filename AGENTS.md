# ask-formly — agent guidance

Read README.md and docs/development.md before changing behavior. This repository owns the portable Formly skill and its qualification evidence.

- Canonical portable source: skill/ask-formly/. Keep it self-contained and selectively loaded.
- Ground semantic claims in pinned Formly v6 source; Material first. Angular 21 qualification does not establish universal compatibility.
- Indexing writes only the consuming project's .agents/ask-formly/ context. Distinguish source inventory, static candidates, reviewed conclusions and runtime evidence; do not execute application factories during discovery.
- Preserve source freshness and explicit unresolved scope. Keep custom registration names scope-qualified.
- Active index regressions live in tests/project-index/. Keep qualification/ and evaluation/ as ignored local archives; CI must work without them. Run npm run check for indexing/packaging changes. Use affected Angular fixtures for behavior changes, following docs/development.md. Never hide the two known browser failures or rewrite frozen audit evidence to claim a pass.
- Historical reports, raw logs and manifests remain provenance. Current setup and handoff live in docs/ and README.md. Record new results separately under test-output/ and compact durable docs.
- AI Central links are local and excluded via .git/info/exclude. Project instructions and steering are real files; never edit shared link targets.
- Do not stage, commit, push, tag, create a remote or publish unless requested. Local Git initialization and local bundle generation are not publication.
