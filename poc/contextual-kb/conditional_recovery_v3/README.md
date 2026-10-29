# Conditional warning and evidence selection comparison

This public development comparison protects library warnings when a proposed
application design uses the relevant behavior. It retains the original G2 plan
and its historical eight-ID diagnostic, while requiring the hide/control-lifetime
warning and detailed key-path support for the branches that plan actually asks
about. It does not turn a custom wizard into an admitted library recipe.

## Frozen inputs and boundaries

Revision 1 froze ten cases and fifteen essential facets before matching changes
or evaluation. Its inputs remain in `history/revision1/`. Revision 2 preserves
those cases, facets, gates and selectors but narrows G2’s second recovery focus
to the unmet key-path syntax distinction after revision 1 failed that facet. The cases include the broad G2 plan, two hide/control paraphrases,
the shared-key hide exception, detailed key parsing, a visual-layout question
that explicitly does not use Formly hide, and the existing hide, uniqueItems,
compareWith and unsupported-version controls. Prior v1 and v2 inputs remain
byte-identical. Help/CALLER guidance was edited before this freeze; that prose
is not a controlled treatment in the deterministic ranking comparison.

The conditional G2 warning is required initially. All fifteen essential facets
must be delivered after at most four follow-ups, first-pass facets must not
regress, and critical controls must retain initial support. Version, complete
provenance, transport, no-oracle fetch and repeat-stability checks remain separate.
A fact returned on a negative branch is not automatically wrong: manual review
must determine whether the answer applied its conditions correctly.

## Comparing caller selection separately

Both caller policies use the same frozen question/focus sequence. Each allows
two discovery/fetch rounds, sixteen candidate summaries per page and at most four
selected facts per fetch. The broad case first addresses the hiding/control
branch, then model/key-path distinctions. Identical focus/question selectors
advance using next_offset; changing them restarts at zero.

The novelty policy reuses v2's uncovered-token reward. The experimental claim-first policy
counts focus terms in the claim before context and title, with modest plural
normalization and stable discovery ties. It excludes already-delivered IDs and
never receives the grading rubric. This is a deterministic relevance heuristic,
not semantic understanding or a recommended mandatory production algorithm.
The production caller remains responsible for checking claims and qualifications.

Both policies are also evaluated on each exact observed discovery page with the
same delivered records. These shadow selections isolate preference differences
from differences caused by earlier calls. A shadow ID is not fetched evidence and
is never credited as recovered support. Grading starts only after all actual and
shadow decisions have been saved.

The factorial has two source versions, two caller policies, ten cases and three
repeats: 120 actual MCP case executions. The unchanged prior comparisons are run
separately. Their original assumptions remain visible: v2's identical-first-packet
gate was specific to its focus-only change and can fail after intentional ranking
changes; such failures are retained, not silently converted to passes.

## Run

Use an existing MCP Python environment and the unchanged pinned database:

```sh
python poc/contextual-kb/conditional_recovery_v3/run.py \
  --baseline-poc /absolute/path/to/baseline/poc/contextual-kb \
  --candidate-poc /absolute/path/to/candidate/poc/contextual-kb \
  --database /absolute/path/to/knowledge.sqlite \
  --sha256 f65802b58ec4f1c2719efd8dc1e391d7e250643a94c96b7a71d446ae67fe1b09 \
  --output test-output/conditional-recovery/factorial-new
```

The source-only harness tests require no installed assets:

```sh
python -B -m unittest discover -s poc/contextual-kb/conditional_recovery_v3
```

Revision 2 is an explicit development iteration informed by the recorded failed
run, not a fresh held-out result. These known public cases do not establish
held-out generalization or autonomous
answer quality. Fresh callers and downstream installation/setup testing require
separate protocols. Facts, authored evidence, compiler and installed DB stay
unchanged throughout this comparison.

## Results and retained failure

Revision 1 failed on the final runtime: the candidate restored the G2 hide warning
initially, but both lexical selectors still missed key-parser support under the
broad focus. Candidate claim-first recovered 14/15 essential facets. The failure
is retained in `test-output/conditional-recovery/factorial-final/report.json`;
it was not relabelled as a pass. The earlier interim run remains separately
recorded in `factorial-1/` because the runtime guard was refined before finalization.

Revision 2 changed only the policy revision and G2's second focus from the broad
scope/binding wording to “How are string keys and array key segments interpreted
as model paths?” Cases, rubric, gates and both selection algorithms stayed the
same. This is a narrower unmet distinction, not new evidence or larger budgets.
All 120 revision-2 executions passed the unchanged gates. Per repeat:

| Source and caller | Total recovered facets | G2 initial / recovered facets | G2 historical IDs recovered |
| --- | ---: | ---: | ---: |
| Baseline novelty | 14/15 | 2/4 → 3/4 | 5/8 |
| Baseline claim-first | 15/15 | 2/4 → 4/4 | 6/8 |
| Candidate novelty | 15/15 | 3/4 → 4/4 | 6/8 |
| Candidate claim-first | 15/15 | 3/4 → 4/4 | 6/8 |

The runtime change restores the control-lifetime warning in the initial packet.
On the same baseline discovery page, claim-first selects that warning whereas
novelty does not. However, neither selector recovered the key parser under the
revision-1 broad focus. Both select it after the revision-2 focus refinement.
The parser gain therefore belongs to improved focus choice, not a demonstrated
semantic breakthrough in claim-first scoring. Broad lexical selection remains
an explicit limitation.

The two remaining historical G2 omissions are named-component registration and
type-registration options. This policy prioritizes the hiding and key-path
branches; it does not establish exhaustive support for every custom-component
choice in the broad plan. The class-versus-alias distinction remains an important
separate check when such a route is recommended.

Maximum SDK result was 29,990 bytes. No errors, scope violations, undiscovered-ID
fetches or repeat instability occurred. The unchanged prior v1 comparison passed
90 executions (maximum 29,897 bytes), and v2 passed 24 (maximum 29,775 bytes).
All frozen input hashes and the DB digest matched after runs. Six asset-free
harness tests passed. Fresh answers and clean installation remain separate
qualification evidence.

Final reports: ignored `test-output/conditional-recovery/factorial-revision2/`,
`original-v1-final/` and `original-v2-final/`. The final runtime source hashes are
recorded beside them. No facts, compiler inputs or installed DB were changed.

The claim-first function is an evaluation policy, not an automatic service-side
answer selector. Production help/caller instructions advise the calling agent to
assess claims and narrow an unmet distinction; that agent still selects evidence.
Narrow-focus guidance was refined during this development iteration. Recorded
source-hash timing distinguishes current documentation from earlier run bytes;
the tested final matching implementation remained unchanged.
