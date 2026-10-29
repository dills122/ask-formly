# Frozen package consumer test results

**2026-10-28 — discovery11 candidate, macOS arm64.** A fresh installation,
actual Codex CLI connection and persistent transport checks passed. Five callers
wrote their own plans in independent client sessions. Independent grading found
no unsupported claims: three answers passed the frozen rubric and two were
partial because of rubric-required details beyond the literal requests.

Facts, the existing installed DB and the frozen package remained unchanged.
This is a local candidate test, not a release or installed-runtime promotion.

## Frozen artifact and environment

| Item | Tested value |
| --- | --- |
| Archive | `ask-formly-discovery11-consumer.tar.gz` |
| Archive SHA-256 | `e7254cfc6a11a9ed31620ef59a3ef728b0d9fd0e9c7bfca320d1b167f6e88a98` |
| Runtime identity | `formly-model-free-discovery-11` |
| Payload | 31 allowlisted files |
| Existing packaging release label | `0.1.0-rc.1`; this is not the published RC archive |
| Platform | macOS 26.6.2, arm64; Python 3.14.6 |
| Consumer client | Codex CLI `0.165.0-alpha.1.2` |
| Model | CLI default, no override; resolved model identity was not established |
| Knowledge SHA-256 | `f65802b58ec4f1c2719efd8dc1e391d7e250643a94c96b7a71d446ae67fe1b09` |

The allowlisted builder used the current pinned runtime and a byte-identical
verification copy of the DB. The installed development DB was not rebuilt,
replaced or used as a writable test fixture. The package was frozen before setup
and was not changed in response to results.

## Fresh installation and client setup

A fresh operator received the archive/checksum and shipped README without
implementation history or grading materials. Installation used a new prefix
containing spaces, a new virtual environment with system site packages disabled,
and actual pinned dependency downloads without the pip cache. Doctor verified
21 runtime files; the shipped startup/catalog/lookup self-test passed.

Two environment interventions were necessary: the first dependency install hit
the outer sandbox's DNS restriction, and the first Codex invocation could not
initialize its client runtime there. Approved escalation retries succeeded.
Both failed attempts remain recorded. There were no package or documentation
repairs. The operator corrected one unused relative scratch-directory creation.
Client-specific mapping from the generated JSON to Codex session configuration
used local CLI help and official client documentation.

The operator derived command/arguments from the installed `mcp-config.json`.
Codex ran with session-local server overrides, ignored user configuration, used
an ephemeral session and an outside-repository scratch directory, and kept its
shell sandbox read-only. No global client configuration or existing installation
was replaced. Existing client authentication and ordinary client runtime metadata
were used; this was not a new operating-system account or physical machine.

The actual client saw all four tools and called help successfully. Initialization
instructions were supplied by the installed server. The existing Pydantic
lifespan warning and Codex runtime-state warnings were retained; neither caused
a test failure.

## Persistent installed transport

A protocol frozen before execution made 14 actual MCP calls across two process
sessions using the exact generated command/arguments and fresh installed SDK.
It tested missing-plan and lost-condition repair, compact provenance references,
discovery/full fetch, schema rejection followed by a valid call, unsupported v7,
separate Material/core project scopes, and a valid call after restart.

All probes passed. Maximum compact serialized SDK response was 29,835 bytes.
Project-scope inheritance was checked within a session; inherited scope after
restart was not separately asserted. Known conformance probes are distinct from
blind answer-quality evidence.

## Blind callers and independent grading

An independent curator froze five ordinary requests and a separate rubric before
assignment. Callers received only their request, installed tools and general
test constraints, including a six non-help-call ceiling. They were not given
plans, expected IDs, previous answers or grading criteria. Each used a new Codex
session and scratch directory. Help was available but none called it.

| Case | Request area | Non-help calls | Frozen rubric result |
| --- | --- | ---: | --- |
| FC01 | Material multi-select, refreshed object identity, Observable options and change callbacks | 2 | Pass |
| FC02 | Save/Discard reset baseline versus Angular reset | 1 | Pass |
| FC03 | Proprietary field input/validator premise and props.attributes boundary | 1 | Pass |
| FC04 | Exact Formly 7.1.0 standalone configuration, with no 6.x substitution | 1 | Partial |
| FC05 | Configuration defaults versus model initialization across falsy values | 1 | Partial |

All five completed without tool errors or repair calls. FC01 fetched a fact ID
disclosed in its own lookup. Every cited fact ID and URL was present in that
case's returned evidence. Traces contain only messages and ask-formly calls:
no shell, filesystem, web or other MCP use was observed, and no cross-case ID
dependence was found. Built-in client tools were not proven absent; blindness
combined separate contexts, restricted instructions and trace inspection rather
than a complete technical filesystem isolation boundary.

The two partials remain partial under the unchanged frozen rubric:

- FC04 correctly disclosed unsupported 7.1.0 coverage and both unverified claims,
  without substituting 6.x. It omitted the rubric's next-step recommendation to
  consult version-matched official sources.
- FC05 correctly distinguished every requested explicit/model value and placed
  computed initialization in the pre-build model. It omitted the rubric's detail
  that source defaults are cloned when merged.

Both satisfy the literal requested decisions. The independent grader accepted
that these omissions may reflect an over-specific rubric rather than consumer
request failures. No scores were retroactively changed, and neither omission is
established as a product defect. The test found no unsupported final claims.

This is one candidate and one caller run per case, not a baseline comparison,
cross-model benchmark or whole-library accuracy score. The model identity is
unobserved, which limits reproducibility. The existing sealed evaluation remained
unopened; exposed cases now belong to development regression evidence.

## Follow-up findings

1. **Make build identity clear before distribution.** The package/README retain
   the rc.1 release label, while the runtime manifest identifies discovery11.
   The handshake reports MCP `1.26.0`, so it cannot identify the retrieval build.
   Keep candidate, release and runtime identities distinguishable in packaging
   and diagnostics. No metadata was changed inside this frozen artifact.
2. **Review rubric relevance before freezing the next bank.** Distinguish required
   user decisions from useful enrichment. Preserve the two strict partial results
   and their interpretation rather than redefining this bank after the outcome.
3. **Extend consumer evidence in a separate run.** Record the resolved caller
   model, repeat independent callers, and test another named client or machine.
   Include recovery-heavy requests and persisted scope after restart. This run's
   callers needed only one lookup or a lookup plus fetch; it does not stress
   prolonged autonomous recovery.

No retrieval or fact change is indicated by these five answers alone. Broader
consumer testing and the previously recorded conditional-recovery limitations
remain relevant. The [testing direction](consumer-testing.md) keeps installation,
transport, recovery and answer quality separate.

## Preservation and artifacts

After testing, the archive digest, all 86 protected source/data hashes, the
existing installed DB, the new consumer DB and the consumer's runtime pins
matched. Synthetic settings were written only into the new test installation.

All raw evidence is retained under ignored `test-output/frozen-consumer/`:
`freeze.json`, `setup/REPORT.md`, `transport/summary.json`, curator freeze and
rubric, five independent client event streams, `grading/independent-report.md`,
`grading/trace-audit.json`, and `preservation-after.json`. The fresh installation
and frozen archive remain available there for reproduction; they were not
published or substituted for the existing installation.
