# Promotion author explanation

## Intent and acceptance
Promote only independently reviewed111fact/24document data, update both knowledge manifests, qualify installed paths, document coverage, then commit/push/PR after fresh review. PLAN.md is canonical. Runtime implementation/model bytes and sealed evaluation locked.

## Implementation and choices
promote.py is bounded adaptation of promotion-v9; existing promotion-v7 guarded transaction reused unchanged. Five targets: exact new authored document, exact candidateDB, two manifests(DBpin/id/knowledge only), sourcepinmanifest new entry. It verifies prior104DB, exact reviewedcandidatehash, frozen inputs/results, pinned final admissionreview, allcandidate answercriticalflags, eight-table superset, unchangedcanonicalinputs/catalog and byte-for-byte canonical rebuild. Ordinary failure rollback has tests/snapshots; no crashatomic claim. New answer-assessment.json records manual no-critical findings on15candidateanswers, backed by pinned finalreview, not automatic semanticgrading.

## Tests and flow
Fourpromotion tests started red missingmodule then passed;18admission/audit tests previously passed. Author preflight passed; guardedinstall and postcheck passed. Stablelauncher model-free16calls exactlyequal qualifiedcandidate. Retained model-backed5calls perseed1701/1702,10successful, relevantfacts plus unsupportedv7stop,8advisoryavailable. Ten actualpacket-based calleranswers/citations retained. Full project maintenance passed.320priorprotectedpaths now316identical+4authorizedchanges, all currentruntime/modelpins valid. Sourcequotes/version6.3.12 remain unchanged, no newcoverageversion.

## Documents and publication
README and currentdocs now111/24, foundation12/discovery4. Installed sourceledger marks only sevenchoicecontrolclaims admitted; unrelatedtopics remainpending. Candidate artifacts include reviewedfacts/cases/tests/hashes/conciseanswers/reviews, notrawpackets/DB/modelassets. Exact plannedpublicpaths in test-output/public-files.json; includes finalreview file oncecreated. Unrelateduntracked work/configs excluded. Publication not performed yet.

## Limits and challenge points
Admission oldbaseline preserved()/prepare intentionally refuse afterpromotion: no reset of historicalpins. For audit use frozenreceipts/read_run and savedoldDBsnapshot, not productionrollback. Preflight snapshots under test-output/install-1/before are private. Judge candidate answers separately fromtoolsuccess; reviewadvisory andplanconditions in bothseedpackets. No actual UI clientrestart verified yet; user can restartMCPs afterpromotion. No full model-backedqualification or browsercompatibility, no toggleNgModule/affirmativeconsentrecipe. The batch harness adds experimentduplication insidePOC; no newproductiondependency. Check publicfiles carefully forprivateassets and secrets. No authorreadinessverdict.
