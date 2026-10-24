# Eight-slot combination experiment

This is a separate integration harness authorized to test result combination. It does not edit the existing retrieval engine, question candidates, models or DB. Sealed evaluation stays closed.

Three policies share original and supplemental query rankings acquired once: foundation-only, current fusion, and a new policy reserving the first six foundation slots. The remaining two slots follow current-fusion order. This protects a prefix, not a guaranteed set of relevant facts.

See PROTOCOL.md for prospective criteria. First outputs and raw traces are retained under test-output. The runner refuses to overwrite an existing run. New tuning requires separate artifacts and fresh prospective cases.
