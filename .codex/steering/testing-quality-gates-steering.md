# Quality gates

Run npm run check for indexer or packaging changes: current skill/docs validation, indexing regressions, packaging regressions and extracted-bundle smoke. Missing TypeScript or skipped graph tests are failures. For Formly behavior changes, run the focused runtime/AOT/browser fixtures described in docs/development.md. The broad browser suite has two known ordinary failures; report exact outcomes, never suppress them. Preserve frozen historical manifests; retain new results separately.
