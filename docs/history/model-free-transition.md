# Model-free transition and retained model-backed mode

The earlier foundation combined hosted question planning, advisory GLiNER,
lexical/dense retrieval and hosted selection. It remains available. The newer path
moves planning, relevance assessment and answer synthesis into the calling agent,
so the MCP itself needs no local or hosted model inference.

The first model-free candidate provided structured-plan lookup and full-fact fetch.
A repair adapter made missing/invalid plans explicit and returned actionable
feedback. Additive discovery then let the caller inspect omitted candidates and
fetch selected records with full citations. These implementations remain at their
original POC paths to preserve qualified behavior; the stable dual-mode launcher
is the public entry point.

The initial comparison exposed evidence missing from small initial packets;
fetching known IDs was diagnostic, not a blind success score. The later fixed
12-request panel, repeated three times, recorded 30/30 supported answers and 6/6
safe controls. Two passes shared the author conversation; the third used a fresh
reviewer. The old model-backed reference supplied sufficient evidence on its ten
covered questions too. This is bounded evidence, not statistical equivalence.

After client restart, an eight-request native pilot recorded six supported answers
and two safe controls in ten calls. One request required discovery and full-fact
fetch. This pilot was self-assessed and did not establish another independent
accuracy measurement. Reported tool times exclude caller reasoning; they are not
comparable end-to-end latency or a claimed speedup.

The dual-mode packaging then passed seven launcher tests, both prerequisite checks,
real stdio smoke checks for each mode and independent review. Frozen candidates,
models and installed knowledge were preserved; sealed evaluation remained closed.

## Retained evidence

- [Initial model-free results](../../poc/contextual-kb/model_free_v1/RESULTS.md)
- [Caller repair results](../../poc/contextual-kb/model_free_repair_v1/RESULTS.md)
- [Initial parity diagnostic](../../poc/contextual-kb/parity_v1/RESULTS.md)
- [Fixed repeated qualification](../../poc/contextual-kb/discovery_qualification_v1/RESULTS.md)
- [Native connection pilot](../../poc/contextual-kb/native_discovery_pilot_v1/RESULTS.md)
- [Dual-mode verification and review](../../poc/contextual-kb/mcp_runtime/RESULTS.md)

These checkpoint records describe the state at their original run, including then-
pending promotion or publication. Current setup is in [runtime modes](../runtime-modes.md).
Raw runs, private freeze inventories and experimental caller runners remain local;
the PR includes serving dependencies, fixture regressions and concise evidence
records. No unfinished JSON Schema knowledge candidate is promoted by this work.
