# Readiness and limits

The accepted Formly MCP is ready for bounded local stdio use in the existing checkout. See its [setup](../poc/contextual-kb/mcp_foundation/README.md), [recorded usability checks](../poc/contextual-kb/mcp_foundation/RESULTS.md) and [independent review](../poc/contextual-kb/mcp_foundation/REVIEW.md).

It is a 46-fact Formly 6.3.12 core/Material knowledge sample. It does not know application components or guarantee complete recipes. Question understanding, advisory extraction, retrieval coverage and final answers have separate failure modes. Correctly reporting missing knowledge is required behavior.

The portable skill/indexing implementation is separate. Its static and runtime qualifications do not transfer automatically to the new MCP. Earlier workflow trials produced mixed speed/answer results; the [history summary](history/experiments.md) retains negative results. Two historical Angular browser failures (B06/B13) remain unresolved evidence, not cleanup failures or newly passing tests.

Fresh-machine provisioning, remote hosting, production scale, unseen overall accuracy and knowledge expansion are not established. Models and data/DB remain locked; sealed evaluation is not consumed by cleanup. Current cleanup validation is recorded separately, without rewriting prior trial outcomes.
