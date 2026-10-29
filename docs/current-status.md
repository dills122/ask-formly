# Current project status

Updated 2026-10-29 after retrieval follow-up PR #23 merged. This page distinguishes what
users can install from source changes and opt-in experiments. The
[backlog](knowledge-completion-backlog.md#current-priority-fact-and-retrieval-refinement)
is the authority for next work; historical reports retain their original scope.

| Layer | Current state |
| --- | --- |
| Published package | `v0.1.0-rc.1`, model-free discovery8. Use the [release guide](releasing.md) and [installer instructions](../poc/contextual-kb/alpha/README.md). Later source changes are not in this archive. |
| Default source runtime | `formly-model-free-discovery-16`. Retrieval, recovery, help/batching and build identity refinements were merged in PR #23. A source checkout does not install them into an existing package. |
| Smaller-answer candidate | `answer-response-v1+be2719ed135a`, explicitly launched from [answer_response_v1](../poc/contextual-kb/answer_response_v1/README.md). Separate detailed provenance, excerpt guidance and selection-first behavior remain isolated; no launcher promotion. |
| Knowledge | Installed foundation15: 192 facts / 36 documents, Formly 6.3.12 core/Material. Authored inputs and installed DB unchanged. |
| Draft knowledge | [Material error/reset candidate](material-errors-reset-candidate.md) remains isolated and unpromoted. |
| Future slices | [Examples, standards/patterns and repository knowledge](knowledge-direction.md) deferred. Three-example prototype retained; recipe storage deferred. |

The latest [selection comparison](selection-first-followup.md) used four new
question pairs and a separately reported historical callback pair. Both arms
retained required support on the new questions; calls fell 31→30 and result bytes
13.2%. The historical callback-input question remains unresolved, and redundant
refocus/provenance work remains. This is a small development comparison, not a
universal efficiency rate or Kiro IDE qualification.

Source checks pass 348 tests; the isolated answer suite passes 27. Full local
maintenance cannot run in this worktree without its compiler environment.
Source tests do not qualify installed DB execution, model-backed inference or
all client/platform combinations. See [readiness](readiness.md) and
[development](development.md) for the boundaries and commands.

Completed reports and failed attempts are reachable through the
[audit history](history/caller-retrieval-audits.md). They are not competing setup
instructions. No merge, release, fact admission or candidate promotion is implied
by this status page.
