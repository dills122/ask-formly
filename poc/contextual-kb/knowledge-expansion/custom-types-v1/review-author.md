# Author Explanation

## Intent and scope

Expand support for building/using custom types without another runtime redesign. This checkpoint produces a coverage inventory, ten compiler-shaped draft records, source evidence, 16 development cases and a bounded future comparison plan. No DB exists for this proposal. Runtime, active records, catalog and manifests are unchanged. Only this expansion directory is added.

## Approach and traceability

README maps capabilities against the existing claims and draft additions. existing-facts.json records all 46 accepted facts. Two draft JSON documents add nine core facts and one Material pattern. proposed-source.md supplies citation-bearing authored summaries in the existing provenance convention. sources.md and source-evidence.json preserve exact upstream extracts and immutable links. The archive hash matches prior provenance; each used local file matches the archive member byte-for-byte.

The compiler API can accept explicit paths; its CLI cannot. PLAN.md therefore requires a tested isolated runner after this checkpoint and prohibits default build/all. A future union retains all accepted facts, adds these ten, and uses separate catalog/input/output locations and candidate integrity checks. No production manifest repinning is proposed.

## Decisions

Keep existing alias, inheritance and wrapper concepts instead of duplicating them. Add concrete component wiring, attributes purpose, declarations, strict scalar/group typing, direct component versus alias, provider contracts, exact missing-name behavior, narrow wrappers fallback, concrete Material reference pattern, and public registration typing. The direct-component option avoids implying alias registration is universal. Avoid complete standalone/lazy-injector and arbitrary widget/CVA recipes because evidence and scope do not justify them.

## Verification

Existing source gate passed (31 tests). Temporary union lint passed: 11 documents, 56 facts, no schema/provenance/link errors. Every new fact has a development case. All case support IDs resolve. Installed DB, original nine records and active catalog hashes match the checkpoint. No inference, DB creation, application compilation, or runtime qualification occurred. Lint cannot establish semantic entailment; reviewer should challenge claims and limits.

## Costs and limitations

This adds a bounded knowledge proposal, not new dependencies or runtime behavior. Archive bytes remain outside POC as existing read-only research provenance; only attributed excerpts are saved in the proposal. Online raw fetching failed; verified archived sources were used. The original sealed evaluation is untouched. Development cases are visible and cannot substantiate unseen accuracy. Future thirty-case repeated qualification has coarse percentage resolution, and the 90% target remains a bounded engineering gate rather than a statistical guarantee.

## Challenge points

Check whether the ten claims genuinely add support, whether the wrapper fallback and forChild wording overstate behavior, whether the Material example is qualified enough, and whether candidate testing can honor accepted manifest guards without altering production setup. Independently assess plan criteria and exclusions beyond these suggested areas.
