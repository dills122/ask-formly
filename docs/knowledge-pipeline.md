# Knowledge sources and transpilation

The knowledge pipeline is part of the primary Formly MCP, not retired experimental material. Its inputs and implementation remain byte-preserved during cleanup.

## Preserved components

| Component | Responsibility |
| --- | --- |
| `poc/contextual-kb/authored/` | Twenty-four controlled JSON knowledge documents containing 111 facts, conditions, limits, exact source quotes, evidence IDs and related-fact links. |
| `poc/contextual-kb/corpus/` | Imported source material and the pinned evidence catalog, including additional source documents used by the authored facts. |
| `skill/ask-formly/references/` | Original reference documents at the paths pinned by authored records. These are frozen provenance; their older application-workflow instructions are historical. |
| `poc/contextual-kb/kbcompiler/current_source.py` | Active schema2 lint/build interface, using the versioned compiler for applicability and evidence-release validation. The legacy `structured_source.py` validates an internal content/provenance projection and supports historical fixtures. |
| `poc/contextual-kb/kbcompiler/__main__.py` | Existing `lint`, `build`, `all` and read-only `inspect` CLI. The installed DB remains locked; only lint/inspection is permitted in routine maintenance. |
| `poc/contextual-kb/kbcompiler/pipeline.py` | Preserved Markdown import/transpilation path and its dependencies: source sections, citations, candidate blocks and proposals. This earlier import path is distinct from the controlled authored-fact compiler used by the installed DB. |
| `poc/contextual-kb/import-manifest.json` | Original source-import provenance. It is not permission to overwrite the current corpus. |
| `poc/contextual-kb/build/knowledge.sqlite` | Locked installed knowledge DB consumed by read-only retrieval. |
| `poc/contextual-kb/tests/` | Preserved compiler and earlier POC regressions. Current source checks explicitly run `test_pipeline.py` and `test_structured_source.py`; archived experiment tests are not treated as new qualification. |

The authored-source compiler checks the Formly version against the evidence baseline, rejects missing or changed origins, verifies exact quotes and citations, and validates related-fact targets. Compilation stores documents, facts, conditions, limits, source offsets and evidence relationships. Retrieval and the calling agent retain responsibility for selecting and explaining evidence; compilation does not prove that every possible Formly question is covered.

## Safe verification now

```sh
cd poc/contextual-kb
.venv/bin/python -B -m kbcompiler lint
```

`python3 tools/project.py check` from the repository root also validates these inputs and runs compiler tests against temporary synthetic fixtures. It does not regenerate the installed database. `packaging/source-files.json` pins the preserved source/provenance bytes; the accepted foundation manifest separately pins runtime assets.

Any future knowledge expansion must be an explicitly authorized change with source review, compiler tests, a separately generated candidate database and a comparison against the accepted DB before promotion. The first authorized expansion is now promoted: custom-type/registration coverage,56facts/11documents. See [promotion](../poc/contextual-kb/knowledge-expansion/promotion-v1/RESULTS.md). Further groups are built and compared separately before any installed promotion.

## Current expansion status

| Knowledge set | State | Evidence |
| --- | --- | --- |
| Core/Material plus custom types and registration: 56 facts / 11 documents | Previous foundation2, including reviewed MCP availability and capitalization handling | [Promotion tests and review](../poc/contextual-kb/knowledge-expansion/promotion-v1/RESULTS.md): 24/24 live answers through the stable launcher; canonical source rebuild matches the installed knowledge tables. |
| Model scope: four additional facts, 60 total / 12 documents | Previous foundation3; qualification and independent review passed | [Comparison and review](../poc/contextual-kb/knowledge-expansion/model-scope-v1/RESULTS.md): candidate 15/15 versus baseline 6/15 in each of three repeats; 45 paired-plan replays passed. |

The installed model-scope addition covers built-field links, ordinary keyless groups, keyed nested groups and leaf model scope. These targeted results are not whole-library accuracy. Models remain unchanged and sealed evaluation remains unused. Expressions/notifications was compiled into a 64-fact candidate and tested: 45/45 live answers versus 34/45 for the installed baseline, plus 45 successful paired-plan replays. [Final independent review](../poc/contextual-kb/knowledge-expansion/expressions-v1/REVIEW-FINAL.md) passed; that candidate was installed as foundation4. Extensions/presets now has a qualified 70-fact candidate: 45/45 targeted answers and 90/90 broader answers, independently reviewed. It was installed as foundation5; the rejected mixed-adapter candidate and its partial results are retained.

Previous promotion: the reviewed validation/error-message candidate was installed as foundation6, with 79 facts / 17 documents. Its [candidate comparison](../poc/contextual-kb/knowledge-expansion/validation-v1/RESULTS.md) records 45/45 answers versus 15/45 for the 70-fact baseline and 45 matched-plan replays. Guarded installation reproduced all five knowledge tables and preserved 85 non-DB pins. All 15 installation smoke answers passed independent audit; see the [promotion results](../poc/contextual-kb/knowledge-expansion/promotion-v5/RESULTS.md). The [previous promotion](../poc/contextual-kb/knowledge-expansion/promotion-v4/RESULTS.md) remains historical.

## Current admission session

The reviewed 64-fact expressions candidate was installed as foundation4; canonical rebuild equivalence and maintenance checks passed, and all ten installation smoke answers passed independent review. The 70-fact extensions/presets candidate passed qualification and independent review and was installed as foundation5. Validation/error-message coverage was installed as foundation6; its 15 installation smoke answers passed independent audit. See [session plan](knowledge-admission-session.md), [scripted admission](../poc/contextual-kb/knowledge-expansion/admission/README.md) and [source checklist](../poc/contextual-kb/knowledge-expansion/source-ledger/CHECKLIST.md). Older comparison results retain the baseline versions used at the time.

The [admission runbook](../poc/contextual-kb/knowledge-expansion/admission/RUNBOOK.md) records the exact inventory, build, eligibility, real-agent test, assessment and replay commands. Fact interpretation and exclusions remain reviewed decisions; source hashes, complete section accounting, compiler validation, runtime eligibility and output comparisons are scripted gates. The [broader-source backlog](../poc/contextual-kb/knowledge-expansion/source-ledger/NEXT-SOURCES.md) lists material not yet admitted.

The [qualified candidate checklist](../poc/contextual-kb/knowledge-expansion/source-ledger/CANDIDATE-CHECKLIST.md) closes all 18 imported-guide sections with 42 decisions and explicit exclusions. The [installed checklist](../poc/contextual-kb/knowledge-expansion/source-ledger/CHECKLIST.md) now records all six extension/preset facts as admitted. See [candidate results and limits](../poc/contextual-kb/knowledge-expansion/extensions-v2/RESULTS.md).

The validation batch adds a separate [installed checklist](../poc/contextual-kb/knowledge-expansion/validation-v1/CHECKLIST.md) for its pinned validation source. Its qualified candidate ledger remains frozen. The earlier three-guide checklist retains its own source scope; neither checklist claims coverage of every Formly source.

## Arrays and premise-planner promotion

Foundation7 installed the exact 85-fact/19-document arrays candidate and the qualified supplied-premise planner. Six facts cover array templates/children, coordinated add/remove, falsy initial-model handling, a precisely scoped source-test fixture and repeater registration. Models, catalog and compiler remain unchanged. All five knowledge tables reproduce from canonical authored sources. See the [installation checkpoint](../poc/contextual-kb/knowledge-expansion/promotion-v6/RESULTS.md).

The [installed arrays checklist](../poc/contextual-kb/knowledge-expansion/promotion-v6/CHECKLIST.md) and [ledger](../poc/contextual-kb/knowledge-expansion/promotion-v6/installed-ledger.json) retain seven source-paragraph decisions and explicit exclusions. Prior arrays candidate ledgers and failed runs remain frozen historical evidence. The final isolated setup qualified at 15/15, 14/15, 15/15 answers, with 36/36 fresh planner semantic checks and 3/3 premise-binding checks. A caller-display refusal remains recorded; these are bounded visible cases, not unseen evaluation.

## Material select promotion

Foundation8 installs eight Material select facts, for 93 facts / 21 documents. The additions cover option mappings/groups, strict comparison identity, Observable consumption versus pipe-owned subscriptions, expression-array update gates, multiple/change forwarding and select-all length/cache limits. No planner, model, retrieval, compiler or catalog changes were needed. See the [installation checkpoint](../poc/contextual-kb/knowledge-expansion/promotion-v7/RESULTS.md).

The [installed checklist](../poc/contextual-kb/knowledge-expansion/promotion-v7/CHECKLIST.md) accounts for both Material guides while keeping unrelated controls, presentation and compatibility topics pending. Historical candidate ledgers remain frozen. The candidate passed 44/45 answers versus 15/45 baseline and 45 matched-plan replays; this is bounded coverage, not whole-Material qualification.

## Version-aware foundation9

Foundation9 installed schema2 with the same 93 facts /21 documents and exact6.3.12 coverage.
Canonical authored records now carry applicability; the catalog separately records
exact evidence releases. Request version/adapter eligibility is enforced before
lexical/dense limits, related expansion, selection and citation delivery. No new
release or general-v6 support was added. See the [promotion results](../poc/contextual-kb/versioned_promotion_v1/RESULTS.md).

For subsequent admissions use the active compiler, not the historical schema1
compiler or old candidate runners. `python -m kbcompiler lint` validates schema2;
`python -m kbcompiler build --database /path/to/new-candidate.sqlite` requires a
new isolated output. Source interpretation, applicability and compatibility remain
reviewed authoring decisions; the compiler cannot certify their semantic truth.

## JSON Schema foundation10

Foundation10 installed six reviewed JSON Schema facts, bringing both modes at that stage to99facts/22documents: conversion API/result shape, renderer-registration separation, customization order, map return contract, local references and remote-reference rejection. Applicability remains exact6.3.12; Bootstrap demo evidence does not establish a complete Material renderer recipe. See [promotion](../poc/contextual-kb/knowledge-expansion/promotion-v8/RESULTS.md) and the [installed source checklist](../poc/contextual-kb/knowledge-expansion/promotion-v8/CHECKLIST.md). Earlier failed model-backed delivery and caller-scope runs remain recorded; no sealed evaluation was used.

## Material datepicker foundation11

Five reviewed datepicker facts bring both modes to104facts/23documents: separate registration and date-adapter responsibility, nested date constraints, calendar options and callback arguments. Exact6.3.12 Material applicability; no universal parsing, locale/timezone or model-commit guarantee. The [promotion](../poc/contextual-kb/knowledge-expansion/promotion-v9/RESULTS.md) preserves both runtime implementations/models and includes an [installed source checklist](../poc/contextual-kb/knowledge-expansion/promotion-v9/CHECKLIST.md). Canonical inputs reproduce the installed DB; sealed evaluation remains unused.

## Material choice-controls foundation12

Seven reviewed checkbox, multicheckbox and toggle facts bring both modes to **111 facts / 24 documents**. They cover checkbox registration and display predicates, multicheckbox map/array payloads and disabled options, and toggle forwarding. Toggle module-registration recipes and affirmative-consent validation remain outside this batch. The [promotion](../poc/contextual-kb/knowledge-expansion/promotion-v10/RESULTS.md) preserves both runtime implementations and models; its [source checklist](../poc/contextual-kb/knowledge-expansion/promotion-v10/CHECKLIST.md) retains pending work. Evaluation remains sealed.
