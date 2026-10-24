# Post-run candidate availability diagnostic

This exploratory diagnostic uses only the saved original and supplemental query-result lists. No retrieval was rerun; no policy, labels, or qualification criteria changed. The union may exceed eight facts and is not a deployable packet or measured system score.

The supported-case mean recall available anywhere in the candidate pools is 95.71%. By batch it is 100%, 87.14%, and 100%. Thus, under these fixed labels and retrieved lists, even perfect selection cannot bring batch 2 above the 89.25% qualification floor.

- M13: two relevant facts are absent from the entire pool: `props-and-registration/registration-adds-configuration` and `props-and-registration/type-name-registration`.
- M14: the required `custom-types-and-wrappers/reverse-merged-defaults` fact is absent.
- M19: the required `custom-types-and-wrappers/wrapper-decorates-not-control` fact is absent.

This separates two problems. Rank reservation loses available useful facts (M01/M13), while some required facts never reach the merger (M14/M19). A future experiment should diagnose candidate acquisition alongside selection; changing only the eight-slot merger cannot resolve all observed failures. This finding does not authorize changes to the locked DB or frozen candidates and does not demonstrate answer accuracy.

Evidence: `test-output/pool-diagnostic.json`, saved retrieval query lists, and prospectively reviewed gold cases. These are post-run observations, not a new qualified arm.
