# Material errors and reset sequence — isolated candidate

This additive candidate contains three new facts in two documents. It compiles
to 195 facts / 38 documents with all 192 existing facts preserved. The canonical
authored set and installed DB remain unchanged at 192 facts / 36 documents.

- [Material error facts](draft-authored/material-error-rendering.json)
- [Reset sequence fact](draft-authored/reset-sequence.json)
- [Pinned source notes](source-notes.md)
- [Source decisions and exclusions](source-decisions.json)
- [Source verification](source-verification.json)
- [Candidate validation and status](../../../../docs/material-errors-reset-candidate.md)

The source files retain their frozen prebuild draft status. The linked status
report records subsequent review/build/testing without changing those frozen
inputs. This is not admission into the installed foundation or permission to
replace its database.

Build and evaluation artifacts are isolated under ignored
`test-output/material-errors-reset-v1/`. The unchanged schema2 compiler used a
separate input-tree copy; build commands and input hashes are in
`knowledge/overlay-manifest.json`, with row preservation in
`knowledge/build-receipt.json`. Follow the [admission process](../admission/RUNBOOK.md)
for any subsequent promotion decision.
