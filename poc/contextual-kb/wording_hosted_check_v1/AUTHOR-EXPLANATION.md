# Author explanation

Intent: complete the hosted integration previously unavailable due approval rejection, now explicitly approved by user. No runtime source changes; only new execution harnesses/audit/evidence in a separate directory.

Plan: two deterministic saved F01 replays with actual hosted selector and two real calling-agent batches of four exposed requests. Both extractor seeds used. Saved replay injects original saved raw plan to guarantee exercise of normalization; all remaining stages real. Calling-agent batch uses unchanged caller instructions and new candidate stdio launcher, no planner/selector substitution, fresh generation and no retries. Native raw requests include F01/M03/M05/M07. Deliberately distinguish saved reproduction from fresh planner output.

Harness based on existing same-POC execution conventions, isolated output directories, ephemeral tool-disabled model sessions except the caller's approved MCP. Timeout captures failures without retry. Selector receipts/raw events/input/decision retain proof of hosted invocation. audit.py replays original baseline and exact selector decisions, validates canonical/raw provenance, full-query text, data/citation identity, packet delivery, model checks and preservation manifests. Independent answer review still needed; mechanical assertions are not semantic truth.

Existing source/method choices unchanged: gpt-6-astra medium planner/selector/caller, two frozen GLiNER adapters, depth20 supplemental retrieval, max2 replacements, eight facts. No training, default promotion or old score rewrite. No general paraphrase/90% qualification claim. New evidence reflects exposed diagnostic cases only. Any newly generated foundation failure or selector fallback must remain visible, not resampled.

Limits: small diagnostic sample, not repeated stability or unseen qualification. Saved replay is not new planner generation. Calling-agent final answer can remain partial/unsupported because DB lacks recipes. Runtime hashes protect existing model/data/candidates; sealed content never interpreted. Completion findings and exact outcomes will be in RESULTS.md.
