# Separate repaired candidate qualification

The first broader run was stopped because the extensions-v1 candidate classified new facts as mixed, outside the frozen retrieval profile. This version targets extensions-v2 with correctly separated core/Material documents and an admission eligibility guard. Questions, answer checks, threshold and three repeats are unchanged; only the moved Material fact ID changes. These are visible repair/regression cases, not fresh or sealed evaluation. Retain all previous failed/missing outcomes separately.

After independent prebuild review, targeted and broader runs may execute concurrently in separate runtime directories. Final acceptance waits for both complete outcome reviews; timings are affected by contention and are descriptive only. No tuning or retries during either run.
