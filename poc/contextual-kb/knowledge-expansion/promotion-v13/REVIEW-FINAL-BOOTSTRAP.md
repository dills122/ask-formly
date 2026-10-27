# Fresh Review Bootstrap
Review instance: 2 of 3

## Objective
Independently review installed192promotion, actual stable-launcher smoke answers, source packaging andpublicationreadiness before commit/push/PR14update. Userauthorizesallbut no merge; runtimes/modelsunchanged/evaluationsealed. Inspecttarget/code/tests/receipts beforeAUTHOR, recordpreliminarythenreconcile.

## Repository and scope
/Users/dsteele/repos/ask-formly; HEAD250f83da2d93aababf27f169078807ff66f183ee oncodex/n1-radio-native-promotion. PR14baseorigin/mainf3f4fdd116facts; currentturnpromotesinstalled124to192. Stagedpublicationpaths listedpromotion-v13/publication-paths.json (plusitselffile); finalreviewmetadata willbeaddedafterreview. No commit yet. Gitindexincludesreviewedcompletion/Q1/publicAPI/fourcontractsrecords, nineauthoredfiles,catalog/manifests/sourcepins,currentdocs,limiteddiagnostichistoryreports. Unrelateduntrackedconfigs/oldexperiments excluded. Rawtest-output,DB/models/privatearchives/evaluationexcluded.

## Primary scope
promotion-v13/promote.py,test_promote.py,installed_smoke.py,test_installed_smoke.py,spec/pins/MECHANISM/PLAN/RESULTS/CHECKLIST/BACKED-ASSESSMENT/installed-answers/preservation-summary; two runtimejsonmanifestdiffs/catalog/newauthored/sourcepins/docs. Priorverifiedinputchains reused; static source/promotionguard mustproveexactreviewedDB. Preapplyreview1Ready, installationalreadyapplied. No rollbackorapplyduringreview.

## Checks and evidence
UseexactMCPpython: poc/contextual-kb/mcp_v1/.venv/bin/python -B .../promotion-v13/promote.py --verify-installed
Unittests: samepython -m unittest discover -s .../promotion-v13 -p 'test*.py'
Fullmaintenance python3 tools/project.py check; logsretained. Installedprivateoutputs test-output/installed/{preflight,receipt}.json,snapshotjournal; installed-free-r1/{calls,receipt,equivalence}; installed-backed-1701/1702 actualcalls/receipts; installed-answers.json holdsactualcallerresponses. Public-source-check.log passesonstagedexport withexistingtestenvsymlinks, noDB/models/copiedrawassets. Do not callhistoricalapi-contracts report main afterpromotion (itsoldinstalled124guard correctlyfails); verifysealedcalls directly or usepreflightrecomputationandpostcheckcontract. Global evaluation/qualificationarchives sealed.

## Author packet
REVIEW-FINAL-AUTHOR.md afterblindpass. WriteREVIEW-FINAL.md only; no code/source/answer/stage edits, no furtherreviewers. ReturnfindingsfirstandReady/Notreadyforpublication. Clarifyboundedmodelbackedsmoke/degradedhints andfixedplanqualificationlimits.
