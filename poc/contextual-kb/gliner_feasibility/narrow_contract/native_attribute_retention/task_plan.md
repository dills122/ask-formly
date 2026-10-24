# Retention experiment plan

Use TDD and planning-files-lite. Four isolated native GLiNER candidates: two seeds × control/treatment, same starting adapters, fixed budget. No old evaluation data becomes training. Original extractors, A, v2 and data/DB stay frozen.

- [ ] Implement and test deterministic matched schedules and weighted loss.
- [ ] Audit existing training-only inputs and freeze protocol after independent review.
- [ ] Reproduce baseline, train four candidates, evaluate fresh and all old diagnostic sets.
- [ ] Independently review results, record failures honestly, protect/freeze artifacts.

Proposed intervention: seven shared replay slots + one low-weight contrast slot per update vs eight replay slots in control. This estimates the whole sparse/low-weight replacement intervention, not a pure effect of weighting.
