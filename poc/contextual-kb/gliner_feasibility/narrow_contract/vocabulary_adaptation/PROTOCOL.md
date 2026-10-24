# Vocabulary coverage and role-discrimination adaptation

User authorizes autonomous improvement of missedAPI/roleconfusion and asks whether
question-layer vocabulary coverage should expand. Expand supervised contexts,
not regex/allow-list matching, schema, knowledgefacts orDB. No imported outside
project code. Read-only officialv6.3.12 declarations ground knownnames; hypothetical
API names still count when explicitly presented as libraryreferences. Recognition
never asserts existence or answerability. Allwrites newdirectoryonly. A,v2,data/DB,
prior artifacts and oldsealed evaluation remain untouched.

Author48new supervised questions:24broaderAPI/formatting,12rolecontrasts,
12mixed/negative preservation. Train original98+new48=146; never train on
fresh_flat48 or other exposeddiagnosticsets. New40 independently authored questions
(8families×5,>=6empty,>=6name/key/version/adaptermentions) authored without prior
questions/results or newtraining. Separate reviewer checks allgold beforefreeze.
Freeze both datasets and configuration before baselineinference. Reserved custom
names/keys differ; sharedAPIs/concepts expected. These are synthetic tests, not
productiontraffic. No deliberate ambiguity/statuslearning.

Evaluate BOTH current epoch8 flat candidates first on fresh40, and diagnostic
fresh_flat48 + challenge24 + olddev24. Baselines must exactly match earlier saved
flat outputs on diagnosticsets (includingconfidences, excludingtiming). No gold
enters inference. Review data/harness before optimization. No changesafterbaseline.

Continue each corresponding adapter for fixed6epochs on146examples with reset
AdamW lr1e-4 wd.01, clip1, serialaccum8 (lastchunk2 averagedby2), CPUfloat32,
fourthreads deterministic, seeds1701/1702.19updates/epoch114total. Same existing
LoRA architecture/frozenbase. Verify everytrain target native character->token
span before optimizing. Save/reload originalpanelparameter/output equivalence
at epoch1and6; hashtrainable/frozenweights before/after. No training-time eval or
checkpointselection, no threshold/label/decoder changes: flat,.5,sixdescribedroles.

After each finalcheckpoint evaluate same136fresh/diagnosticquestions and train146
separately. Report exact raw/acceptedtypedspanP/R/F1, role/family, exactenvelopes,
invalids/emptyFPs/criticalboundarymisses, everyregression and timing. Firstoutputs
preserved. The fresh set becomes exposedafterbaseline; this is pairedtesting,
not a second unseen test after adaptation.

Improvement gate (bothseeds): freshacceptedF1 gains>=2points, freshexactcount does
notfall, freshAPIrecall and adapterprecision do notfall, emptycaseFPcount doesnot
rise; eachdiagnosticsplit acceptedF1 maydrop<=2points with no invalidcountincrease.
Additionally targeteddiagnostic fresh_flat48 APIrecall mustgain>=5points perseed.
If gatesfail don't loosen them or selectone seed. Qualification remainsseparate:
>=90%overall/everynonemptyrole P/R,zeroinvalid/runtimeerrors,no criticalcompound/
quoted/opaque boundarymisses. No readiness/generalansweraccuracyclaim.

One bounded adaptation round, no parametersearch afterscores. Independent review
checks gold, source-grounding/coverage, hashes/native transport/save receipts,
training isolation/scoring/failures and verdict. Atmost3reviewinstances forround.
