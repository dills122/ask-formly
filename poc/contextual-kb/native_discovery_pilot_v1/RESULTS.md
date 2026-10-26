# Native discovery connection and pilot

The app-native connection is now verified after the user's restart. All three
ask_formly_discovery tools were visible and executed in this conversation:
lookup_formly, discover_formly_candidates and get_formly_facts. No SDK bridge,
separate caller CLI, old-model reference run or server-side inference was used.
This closes the native-registration limitation recorded by discovery_qualification_v1.

Eight fixed representative requests were exercised once. These are synthetic
realistic questions, not production traffic. Self-assessment:6/6covered answers
supported,2/2controls handled safely. Ten native calls completed without tool errors:
8lookups,1discovery page,1full-fact fetch. No repairs, retries or scope downgrade.

|Case|Outcome|Evidence handling|
|---|---|---|
|N01 invalid/untouched error visibility and message configuration|Supported|Preserved default-predicate conditions and renderer limits|
|N02 omitted wrappers versus wrappers: []|Supported|Limited conclusion to the type-wrapper fallback stage|
|N03 returned onInit Observable versus manual subscription|Supported|Distinguished managed lifecycle from caller-owned cleanup|
|N04 extension phases and numeric priority|Supported|No equal-priority or once-only guarantee invented|
|N05 inherited input type/defaults versus supplied field props|Supported after discovery/fetch|Recovered registration/default-merge evidence missing from initial packet|
|N06 public registration type|Supported|Public ConfigOption-derived type; no internal TypeOption import|
|N07 exact message precedence/reactive refresh|Safe knowledge gap|Explicitly declined unsupported details|
|N08 exact6.3.11 wrapper recipe|Safe scope stop|No substitution of6.3.12or further lookup|

N05 demonstrates the actual native round trip: initial facts established the
inheritance example but lacked the relevant default-merge claim. One16-record
discovery page exposed registration options and reverse-merged defaults. The caller
selected those two records and fetched their complete citations before answering.
The initial array/repeater facts were not treated as support for ordinary type
defaults. No other pilot request needed a discovery/fetch call. Unrelated retrieved
facts remain in raw output; they were not cited as support or used to inflate scores.

All answers and bare fact-ID citations are saved in test-output/answers.json.
Raw tool arguments/results/timings are in test-output/native-calls.json. Mechanical
checks verified unchanged original requests, identical lookup/discovery plans,
scope on every call, discovery bounds, full delivery of every citation and the
unsupported-scope stop. Preservation rehashed815pins with zero changes. Existing
candidates, original server config, model assets, installed DB and sealed evaluation
were not altered. No promotion, commit or publication was performed.
The required python3 tools/project.py check also passed; its log is retained in
test-output/project-check.txt.

This pilot is self-assessed, not a fourth independent review. The frozen implementation
and preceding qualification already completed their3of3review flow. This run verifies
native usability and a small set of request outcomes; it does not add a broad accuracy,
cross-harness compatibility, Angular runtime or end-to-end latency claim.

The experimental connection can now be used for a bounded real-task pilot. Making
it the default installed foundation and updating public setup docs would be a separate
promotion change; the accepted old foundation remains available and unchanged.
