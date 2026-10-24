# ask-formly — agent guidance

Read README.md, docs/development.md and docs/knowledge-pipeline.md before changing behavior. The accepted Formly library MCP in poc/contextual-kb/ is the primary implementation.

- Keep implementation self-contained in the POC. Do not import retired application-inspection or knowledge-engine code.
- Preserve authored knowledge, corpus/evidence inputs, compiler/seeding code, schema, DB, stored index, model assets and sealed evaluation. They remain locked unless the user explicitly authorizes a change. Do not rebuild the installed DB during maintenance.
- skill/ask-formly/references/ contains frozen source provenance used by the compiler. Keep its paths and bytes; it is not an active application-inspection product.
- Ground claims in pinned Formly 6.3.12 evidence, Material first. The current 46-fact sample does not establish whole-library or universal compatibility.
- Run python3 tools/project.py check (or npm run check) for local maintenance. CI runs the explicitly narrower source command without private assets. Missing assets must not be reported as a qualified runtime.
- Keep evaluation/ and qualification/ as ignored archives; never open sealed questions for routine checks. Keep known historical failures, including browser B06/B13, visible in history.
- Keep concise current setup/process in docs/, high-level history in docs/history/ and poc/contextual-kb/history/, and generated output in test-output/. Do not restore obsolete runners to the active tree just to reproduce history.
- AI Central links are local and excluded. Never edit shared link targets. For structural exploration use the installed codebase-memory skill and verify source when graph coverage is incomplete.
- Stage, commit and publish only when requested. Keep models, databases, environments, private archives and sealed evaluation out of public Git.
