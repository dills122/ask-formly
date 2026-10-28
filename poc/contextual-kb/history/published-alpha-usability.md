# Published alpha install and Codex usability checkpoint

Release: [v0.1.0-alpha.1](https://github.com/dills122/ask-formly/releases/tag/v0.1.0-alpha.1), release commit `060ef8ba667892a35d32b286de890d45e5e1fb00`. Work began from merged PR #19 (`8aa813a`). This is a bounded development check of the published artifact, with no runtime changes or knowledge expansion.

## Frozen method

Twelve fresh requests were fixed before running, with eight library tasks and four boundary controls. Case-file SHA-256: `56ea39d43b33a3a0b55587ce327d0b3702eea573813e58197d7ba4740f742760`. Each request used a separate ephemeral Codex caller session and empty workspace; three sessions ran concurrently. The callers used only the downloaded alpha MCP for evidence, with explicit instructions to cite sources and disclose gaps. No retries, tuning or cross-case fact IDs were supplied. The model default was not pinned; this is a single configured Codex-harness checkpoint, not a model comparison.

The release was downloaded from GitHub, not built from the checkout. Archive SHA-256: `cea989d620158ce82857a191f614f2c55f2502752b3e7235118b5354ee1af35e`. It was extracted and installed outside the repository in a path containing spaces, with a fresh virtual environment and downloaded dependencies. Existing Codex authentication remained in use; no credentials were copied. Codex was the external calling agent; the MCP performed no model inference.

## Installation and transport

- Published checksum verified; fresh installation, dependency checks, doctor and real MCP self-test passed.
- A separate launch passed initialization, tool listing and read-only lookup, exercising a fresh-process relaunch; live-client disconnect recovery was not tested.
- Installing over the existing destination was rejected. All 27 release payload hashes remained intact afterward and after the caller run.
- Both installed and packaged DBs retained SHA-256 `f65802b58ec4f1c2719efd8dc1e391d7e250643a94c96b7a71d446ae67fe1b09` (192 facts / 36 documents).
- Full local maintenance checks passed. The existing Pydantic forward-reference warning appeared on stderr without preventing startup or lookup.

## User-facing results

| Case | Request topic | Assessment |
| --- | --- | --- |
| U01 | Custom tax-reference field implementation, registration and use | Supported; illustrative Material recipe, no invented tax rules |
| U02 | Conditional hide, retained value and control registration | Supported, including shared-key caveat |
| U03 | Disabled expression and change notification payload | Supported, including managed subscription and caching limits |
| U04 | Global validation message and per-field override | Supported, including precedence |
| U05 | Repeat rows and add/remove model effects | Supported core behavior; source example’s Bootstrap presentation disclosed |
| U06 | Select code/description mapping and grouping | Supported; grouping depth and unspecified data noted |
| U07 | JSON Schema conversion and map callback | Supported; callback return and Material renderer-registration limits retained |
| U08 | Checkbox versus multicheckbox, map versus array values | Supported, including representation limits |
| U09 | Datepicker min/max with explicitly unknown version/adapter | **Partial:** conditional 6.3.12/Material example and confirmation warning, but no clarification round trip |
| U10 | Explicit Formly 7.0.0 request | Correct unsupported-version stop; no substitution |
| U11 | Explicit Bootstrap request | Correct unsupported-adapter stop; no claim that feature is absent |
| U12 | Diagnose unavailable internal component | Correctly refused an invented diagnosis; any library check labeled hypothetical |

Eight of eight library answers were supported within returned evidence. Three boundary controls passed; unknown scope was partial under the frozen clarification criterion. Do not combine these into a whole-library accuracy percentage. Every final source URL appeared in that case’s returned evidence. The code examples were not compiled or browser-tested.

All twelve sessions exited successfully. Each library/unknown-scope/application-boundary case used lookup plus full-fact fetch; unsupported cases used one lookup each: 22 MCP calls total. There were no observed plan-repair calls. Median end-to-end session time was 23.05 seconds, range 13.41–34.10 seconds, including caller startup and answer generation under concurrency; this is not isolated MCP latency.

The twelve requests did not invoke discovery, so the predeclared fallback was a separate prompted workflow check (D01): discover and fetch the `FormlyConfig.getType` missing-name contract. It used exactly discovery then full-fact fetch and correctly explained null versus throwing behavior. This is workflow evidence, not an additional item added to the twelve-case score.

## Review and next decision

Independent review used fresh context and inspected actual caller traces, returned evidence, citations, frozen criteria and installation artifacts before the author explanation. Verdict: **Ready with non-blocking follow-ups** for this bounded checkpoint. Review independently verified the archive against its checksum, all 27 archive/installed payload hashes and the current repository DB hash. Download provenance comes from the recorded author operation; there was no independent remote re-download during review. The reviewer recorded preliminary grading before reading the author explanation, but received a short U09 status note during that first pass; the review log discloses this.

Keep the released alpha available for bounded use. Next prioritize clarification when a user explicitly says version/adapter are unknown, then a real target-client installation (Kiro/Claude) when available. The existing server’s default scope was clearly labeled in this run, but that does not satisfy a strict clarify-before-guidance interaction. A future fix should be isolated and tested; no runtime change was made here. Minor documentation friction remains: the root README’s badge still says alpha preparation and its example archive basename differs from the released filename (the text tells users to use their actual filename).

This used the same macOS arm64/Python 3.14.6 host as prior checks, not a separate physical machine. One pass per request does not establish repeatability, other platforms, every client, or spontaneous tool discovery. No new repair-loop qualification was performed. Models, runtime implementations, installed DB and sealed evaluation were unchanged. Raw cases, logs and harnesses remain ignored under `test-output/alpha-usability-v1/`; no private test artifacts are intended for Git.
