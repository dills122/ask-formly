# Train/development annotation qualification findings

Status: 96 additional training questions and30 development questions prepared and
qualified within the observed pilot/train/dev scope. The120 training artifact
includes the unchanged24 pilot rows. Full training has not started. External
custody/historical contamination and scoring-workflow readiness remain pending.

## Results

| Check | Finding |
| --- | --- |
| Final training |120 questions,148 aspects;24 unchanged pilot +96 new |
| Final development |30 questions,35 aspects |
| Primary strata |Six strata,20 training and5 dev questions each |
| Independent raw annotation, newtrain sample24 |Span/attachment F1 .925373; aspect-count agreement100%; ambiguity agreement100% |
| Independent raw annotation, final dev30 |Span/attachment F1 .909836; aspect-count agreement100%; ambiguity agreement100% |
| Remaining72 newtrain audit |64 accepted,8 corrected; every row has a case-specific audit rationale |
| Native preprocessing |All150 rows preserve record fields, typed entity occurrences and explicit relation pairs; no failures |
| Source/span validation |All150 canonical rows valid; zero partial-alphanumeric-token findings |
| Test suite |10 qualification/data tests pass, no skips |
| Protected integrity |225 existing paths unchanged, including pilot, A, data/DB and prior implementation/evidence |
| Model execution |Local checkpoint loaded for preprocessing only; zero prediction calls, backward calls or optimizer steps |

Agreement uses maximum-overlap one-to-one aspect alignment rather than assuming
record order or collapsing shared anchors. Exact source offsets/roles, entities
and relation endpoint pairs contribute features; counts and status are reported
separately. The raw pools pass the predeclared .90 F1/.90 count/.90 status gates.
Adjudicated gold is not used to inflate those agreement scores. Final development
raw panels and their per-row source provenance are retained alongside originals.

## Findings addressed before qualification

Initial independent family audit found expression-observation overlap between
train/dev, model-property-read overlap, and shared unresolved-reference templates.
The conservative closure replaced D013,D014,D018,D021,D022,D025,D030. D022 was
revised again after the first replacement still repeated a validator-configuration
scenario. No model predictions or performance influenced replacements. All draft
questions, raw labels, audits and initial agreement results remain preserved.

The final family auditor found no remaining cross-split conflict within the
observed24 pilot +96 newtrain +30dev questions. Same-split paraphrases/minimal pairs
were grouped with transitive merges; metadata records57 train and27 dev families.
This is conservative scenario/template grouping, not proof of independent natural
language generation. Related topics still occur across splits; topic overlap alone
is not treated as a duplicate. The regular paired training prompts mean120 rows
are not120 independent scenarios.

Parent adjudication resolved residual disagreements without model outputs:
shared targets versus operation words (notably computed-summary formatting and
recomputation), interrogative target phrases, temporal versus request cues,
reference attachment, supplied names/literals and nested configuration value
pairing. Eight independent audit corrections and eleven explicit disagreement
choices are recorded in adjudicated-v1/decisions.json. See the raw sources for
alternative readings; these are agent annotations, not expert-human ground truth.

Development contains two needs_clarification cases; training has ten including
pilot. Development ambiguity evidence is therefore sparse. This does not replace
the future sealed evaluation's explicit ambiguity coverage quota or justify a
claim of reliable reference handling. No model quality was scored here.

## Artifact locations and readiness boundary

Final canonical artifacts:

- ../full_training/data/train.json
- ../full_training/data/dev.json
- dataset-manifest.json: hashes, family/stratum maps, annotation evidence and
  explicit pending external gates. It is NOT a runnable training authorization.

The existing pilot file and every pilot annotation object remain unchanged.
No training-manifest.json is created: the training worker cannot mistake this
partial readiness state for qualified custody or a complete experiment freeze.

Before full training, still complete the frozen scorer and blinded
adjudication/grade-to-checkpoint binding; verify independent expected model,
package, schema/config and parameter manifests; reconcile the readiness evidence.
Separate custody must validate contamination against sealed evaluation and all
historically exposed cases without exposing evaluation to implementation. Those
sets were not read in this task. Even though train/dev labels and their observed
split now pass, full isolation from those other sets is NOT yet established.

A remains unchanged and was not executed. Knowledge/DB/corpus/compiler/index were
not edited or semantically inspected. Native worker audit policy denies DB,
network, subprocess and other project-input reads. All artifacts remain in this
POC; no outside project code was reused. No engineering-review budget was reset:
annotation and family audits implement the already-agreed data qualification
protocol, not a seventh engineering review.

## Evidence and reviewed decision

- questions.json, questions-v2.json, questions-v3.json and question-replacements.json
  retain authored/repaired question provenance. D022 final revision is also in
  family-final-audit.json and its separately frozen v3 annotations.
- agreement-v1.json and agreement-final-development.json retain raw agreement.
- remaining-training-audit.json records all72 audit decisions; raw author labels
  and independent annotations are untouched.
- family-audit.json, family-repair-audit.json and family-final-audit.json retain
  initial failures, repair reasoning and final limited-scope finding.
- adjudicated-v1 contains canonical rows, decision ledger, external metadata and
  empty boundary-findings.json. Source rationale alternatives remain in raw rows.
- native-transport-v1/report.json and03-native-transport.txt retain actual strict
  processor verification. Loader warnings remain; no failing rows were omitted.
- 01-red.txt,02-green.txt,04-final-checks.txt and test_qualification.py/test_dataset.py
  distinguish TDD utility checks from final artifact assertions.
- integrity-after.json and final-freeze.json freeze the completed evidence.

Reviewed outcome: accept these train/dev artifacts for the next experiment
preparation stage, with the external-isolation and agent-gold limitations above.
Do not run full training or open evaluation based on this result alone.
