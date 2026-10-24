# Context-preserving supplemental query experiment

The first contextual-query candidate shows a small retrieval gain, but fails qualification. Keep foundation-only as the working baseline. Do not promote this candidate or describe the pooled89.94% as consistent90% performance.

## What ran

36freshly worded development requests in3disjoint batches,12each;49first foundation questions and49first supplemental queries. Each batch used a fresh native agent context with frozen qualification_v3contract, then the supplementcontract and unchanged plan. No catalog or retrieval results supplied to generators. This is a native-agent first-submission experiment, not a pinned hosted API or repeated generation qualification. Same foundation output in botharms. Four supplementalqueries exactlymatched theoriginal and were skipped, leaving45additionalqueries.

Independent prospective review covered everyplan/query and all46catalogfacts.26requests aredirectly supported,4partial,6unsupported-in-catalog. Partial gaps: C05fullMaterialcustomcontrolimplementation; C25whether/exactlywhen an expression can supply defaultValue; C27initialhiddenrenderer lifecycle; C34dotted-key parsing semantics. Gold requiredgroups cover only supportedaspects, not these gaps. Three groupjudgments clarified before retrieval (C08/C15/C18), with unchanged relevanceIDs and provenance in preflightreview.

Originalfullquestion searches alwaysrun. Candidateadds one operation-first rewrite preserving conditions, then unchanged hybrid/RRF/interleave at eightresults. No GLiNER inference/training, no newranker, no answerer. Read-only SQLite mode=ro/query_only;46transientfactvectors.123inputs/code/artifacts/dependencymetadata hashes frozen before execution;72pairedretrievalrecords savedonce. No repair, rerun or tuning afterresults.

## Paired retrieval result

All relevance metrics below are macroaverages over30nonempty-gold cases (10perbatch), including only catalog-backedparts of partialcases. Sixunsupportedcases are reported separately. Recall means fraction of all labeled relevantfacts found; completegroups means eachminimumrequirement has at least one predeclared substitute. Neither is finalansweraccuracy.

| Metric | Foundation | +contextual query |
|---|---:|---:|
| Recall@8 |89.39%|89.94%|
| Precision@8 |25.42%|25.42%|
| nDCG@8 |86.99%|86.85%|
| MRR@8 |91.11%|91.78%|
| Any-hit@8 |29/30|30/30|
| Mean required-group coverage@8 |90.83%|93.06%|
| Complete required groups@8 |26/30|26/30|
| Recall@4 |85.83%|85.83%|
| Precision@4 |46.67%|46.67%|
| Complete required groups@4 |24/30|24/30|
| Query calls |49|94|
| Query characters |5,504|10,564|

All six unsupportedcases receive eightcandidates in eacharm (48total);at4,24. No abstention or falseanswer measurement. Identicalfixedk precision does not mean candidatequality is interchangeable; one criticalfact waslost andanother gained.

| Fresh batch | Foundation recall@8 | Context recall@8 | Foundation/context completegroups@8 |
|---|---:|---:|---:|
|1|92.50%|90.83%|10/10 →9/10|
|2|91.67%|91.67%|9/10 →9/10|
|3|84.00%|87.33%|7/10 →8/10|

Both pooledscores fall within the requested90%engineering tolerance, but batch3fails the89.25%floor. Context is0.0556pointsbelow90pooled, yet1.9167pointsbelowthefloor inbatch3. Rounding or pooledaverages cannot establish consistency. Frozenutilitygate alsofails: gain+0.5556points<+2required;batch1regresses;C06losescompletegroups;semanticfailures remain. Failurewouldremain evenwithout the semanticgate.

Descriptive request-bootstrap95%intervals for pooledrecall: foundation81.11–96.06%,candidate83.00–95.83%. Requests are related syntheticcases, so these are descriptive, not populationconfidence or proof of±0.75precision. Onecase'srecall canmove abatchmean by up to10points; smallbatches remain coarse. No repeateddeterministicrun was counted as fresh evidence.

## Every recall change

Only two of36requests change recall@8; neither changes recall@4.

- C30: contextualquery recovers custom-types-and-wrappers/reverse-merged-defaults. Originalzero-of-three relevantfacts becomesone-of-three; the requiredgroup nowhasitsfact. The originalquestion placed the defaultOptionscondition before the requestedcombineoperation. The rewrite leads with “How does Formly combine the supplied property and missing defaults” and retains thecondition. Saved supplementalranking has themergingfactfirst; fusedpacket putsitfifth. This is an observedbenefit of thisrewrite, not proof of a general operation-firstrule.
- C06: registration/use lookup falls fromfive-of-six relevantfacts tofour-of-six. The key/modelversustype/rendererfact dropsout, replacedbydefault-eligibility. Bothoriginalqueries stillretrievedthemappingfact (positions7and4), but supplementalranking/fusion/interleave pushesitoutsideeight. Thecandidateintroducedno semanticfailure in thiscase: preservingmeaning didnotguarantee preservationofretrievedevidence.

Foundationmissingcompletegroups:C15,C27,C28,C30. Candidatemissing:C06,C15,C27,C28. No pairedcomplete-grouplossat4;C06isapairedlossat8. All percaseadded/lostIDs,rankings andmetrics retainedinscores.json/results.jsonl. Others maychangeorder ornonrelevantfacts without changingrecall; no suchchangesarehidden.

## Meaning and delivery

All36firstfoundations passedstructuralvalidation;all49supplementals passed schemaandverbatimledgercopy. No runtimefailures, missingoutputs, changedfoundationplans or repairedoutputs.

Independent semanticreview found:

- C09supplement Q1 puts “when the field is destroyed” immediatelyafter “if onInit returns an Observable”, creating an attachment ambiguity between teardown-time andreturn-time. The sourcewasclear. Exactsubstringssurvive but the temporalrelationshipweakens. Countedfailure;not repaired.
- C11foundation preserves “in IndexedDB” inquestionprose butomitsthesuppliedchannel fromthemandatoryconditionledger. This is afoundationcontractomission on anunsupportedcatalogrequest; the supplement preserves itsmeaning. ItdoesnotdemonstrateincorrectFormlyknowledge ormissing prose. Existingqualificationresultsremainunchanged.

35/36foundationplans pass thesemanticreview;35/36supplementalsets passtheirlocalrewritecontract;34/36combinedcasespassboth. Thesearecasecounts, notperquestionmodelaccuracy. Semanticfailures arecounted separatelyfromretrievalrecall and are not excludedfromdenominators.

## Cost and preservation

Across36requests, warmretrievaltime total0.329sfoundation versus0.620scontext. Requestp50/p95:0.0082/0.0141s versus0.0153/0.0270s. One-timesetup0.908s. Nativegenerationtime/token/servicecost notmeasured; the extraagentrewritehasadditionalcost beyondthisretrievaltiming. No serviceSLA claim. ONNXtelemetrypersistencewarning retained;72rowscompleted. No extraction/model-loadcost becauseGLiNERnotrun.

17tests passedincludingpairedloss,batchregression,semanticfailure,optional-failureisolationandconditioncopy. Preflightready permitsanexperiment,notcandidatepromotion. Completedindependentreview andfinalpreservationrecordedseparately. Existing45protectionmanifests include allpriorcandidates/models/DB andsealeddata(hashonly); nosemanticsealedreads. DBhashbefore/after unchanged.

## Decision and implications

Keepfoundation-only. Contextualsupplementscanrecoverusefulfacts, but nearlydoublingqueriesisnotjustifiedbythissmallgainwithapairedlossandunmetbatchfloor. These newcasesarenotdirectlycomparabletoearlier92.22%batchscores: frozenfoundationcodehasnotchanged;questionsandprospectivelabelsdiffer.

Do nottrainGLiNERorloosenthegatebasedonthisresult. The preservedfullquestions alreadyfoundthelostC06fact; thecombinationofqueryrankingsandfixedbudgetdiscardedit. This identifies a downstreamintegrationlimit worthseparatelyscoped investigation; itdoesnotauthorizechangingtheengine,mergingpolicyorDB here. The C30gain supports keepingcontextualqueriesasexperimental, notuniversaldefault.

No furtherprompttuning onthese36cases wasperformed. Theyarenowdiagnostics. A subsequentproposalshouldexplicitlyaddress evidence displacement and the remaininghide/defaultqualifications, with freshcasesandapredeclaredbudget, ratherthanrepeatbroadparaphrasinghopingforapooled90. No suchfollow-upimplementedinthisexperiment.
