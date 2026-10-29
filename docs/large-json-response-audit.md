# Large JSON response and client boundary audit

Read-only investigation on 2026-10-28 against source runtime
`formly-model-free-discovery-16+00b3331851e8` and the unchanged 192-fact installed
database. This is a response delivery audit, not a new knowledge slice or a
release qualification. Recipe storage remains deferred.

## Client distinction

The reported client is **Kiro IDE**. Its separate [CLI terminal UI documentation](https://kiro.dev/docs/cli/terminal-ui/#large-tool-results-in-v3)
says CLI V3 saves large tool results with the session and gives the model a short
preview. That CLI behavior is background only and does not establish the cause
of the IDE incident. The IDE version and relevant size threshold are not
established. No IDE-specific behavior or requirement to use Python has been
demonstrated. Neither `kiro-cli` nor `kiro` was available on this test host's
PATH; no client installation or user settings were changed.

Codex is a comparison client. Its [configuration reference](https://developers.openai.com/codex/config-reference)
documents an MCP per-tool output token limit. Server JSON byte limits therefore
do not establish a universal client-safe size. Complete raw tool events also do
not establish exactly what the model saw. Auditor shell-output truncation is a
separate boundary from caller MCP truncation.

## Measured payloads

Real SDK calls used unchanged source and data. The deterministic cases contain
no synthetic padding. Sizes below are UTF-8 bytes, not token estimates.

| Case | Task | JSON text bytes |
| --- | --- | ---: |
| P01 | Explain one compact fact with conditions and limits | 2,946 |
| P02 | Compose a qualified answer from ten compact facts | 26,442 |
| P03 | Compose a qualified answer from sixteen full facts | 38,724 |
| P04 | Exact counts and provenance joins for the same packet as P02 | 26,442 |

The ten-fact packet occupies 28,096 bytes in the measured MCP envelope. The
sixteen-fact full packet occupies 41,630 bytes. The latter is below the 48 KB
server limit and is not claimed to reproduce that limit.

For the same ten facts, full JSON is 26,915 bytes: compact saves only 473 bytes
in this case. In the compact packet, serialized fact values account for 9,211
bytes while citations, sources and evidence account for 15,750. Formatting
accounts for 771 bytes. These value sizes exclude object keys and separators;
they are contributions, not additive promises of removable bytes. The packet
contains 24 references to 19 distinct referenced values. Exact audit work must
join those references. Provenance dominates this packet; changing indentation
alone will not solve its size or reading burden.

## Comparison protocol

Four fixed tasks each run in two fresh Codex sessions: an actual MCP request and
an explicitly supplied file containing the identical frozen response text.
The supplied file is created by the harness. It is not a captured Kiro spill or
proof that Codex automatically saves large MCP responses. Local parsing is
available but neither Python nor a parser is recommended. Expected answers are
kept separate from caller inputs. This is a controlled delivery comparison,
not a blind question-generation experiment or an estimate of real-world
incident frequency.

The rubric separates answer accuracy, parser choice, observable truncation,
extra retrieval, and access to the full result. Choosing Python is not itself a
failure or proof that Python was necessary. Python cannot reconstruct evidence
that was neither delivered nor made accessible in a complete saved result.

## Observed caller behavior

All eight sessions completed without quality retries or budget excesses. Each
native MCP session made one fetch and no local command. Each file session first
read the supplied JSON; P03 and P04 then independently chose Python.

| Case | Native MCP | Supplied file |
| --- | --- | --- |
| P01 | One fetch; no local parser | One read; no parser |
| P02 | One fetch; no local parser | One read; no parser |
| P03 | One fetch; no local parser | Read, then Python extraction excluding citations |
| P04 | One fetch; no local parser | Read, then Python counts and reference joins |

P03's extraction produced 19,140 bytes and P04's produced 8,040. The P03 caller
reported that its initial display was truncated, but the recorded command output
contained the full 38,724-byte packet without a truncation marker. P04's MCP
caller also described processing retained output; no separate parser or local
command was recorded. Those statements do not independently establish the
model-visible transformation. The P03 MCP caller also reported truncation
without a corresponding clipping marker. Python use is observed in two supplied-file
sessions; Python necessity and the original Kiro IDE incident are not reproduced.

All eight actual MCP/file inputs matched their frozen packet hashes. The 68 raw
result files are frozen separately from derived observations. Six local commands
were recorded across file sessions and four MCP fetches across native sessions;
no repeated discovery or help calls occurred. These prescribed one-packet tasks
do not measure normal retrieval efficiency.

Independent grading found all eight answers supported by their supplied packets.
Both exact-inventory answers preserved all ten fact rows, six explicit condition
entries, fourteen limit entries, nine evidence records across fourteen
fact/evidence associations, and five shared-evidence relationships. They
distinguished authored offsets from absent authored line ranges. The Python
steps preserved answer accuracy; they were additional processing work rather
than evidence of missing facts. This small fixed comparison does not establish
a general success rate.

## Recommended next experiment

Prioritize the response contract over adding more facts for this issue. Prototype
a smaller answer-oriented view that retains complete claims, conditions, limits,
scope and stable citations, with detailed provenance available separately. Keep
an explicit completeness signal so callers cannot confuse omitted provenance
with missing facts. Compare answer quality, provenance accuracy, response size
and extra fetches against the current complete-evidence contract before deciding
whether to adopt it. This is a proposal, not an implemented contract change.

Capture a fresh Kiro IDE reproduction with its version, exact request, saved
result/preview if any, and parser command. That is needed to locate its actual
boundary; the CLI documentation and Codex controls cannot substitute for it.
Do not set a universal byte threshold from these four packets.

## Evidence and preservation

Raw packets, SDK measurements, official documentation receipts, frozen prompts,
caller traces and grading live in ignored `test-output/large-json-audit-v1/`.
Earlier audits and failures are retained. No authored facts, installed database,
isolated knowledge candidate, runtime behavior or recipe storage changed.
All 103 protected paths matched their before hashes after the investigation.

Source validation passes for 130 preserved files and authored-fact lint.
`python3 tools/project.py check` remains blocked by the missing worktree compiler
environment; this investigation does not qualify a complete installed runtime.
