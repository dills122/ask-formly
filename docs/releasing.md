# Packaging and recovery

The accepted library MCP source is versioned in Git. Large model weights, DB files, environments, sealed evaluation and private recovery archives are not public release artifacts.

Use the POC's [allowlisted runtime packaging](../poc/contextual-kb/packaging/README.md) for local recovery. That bundle is not a fresh-machine installer or a license to redistribute all included assets. Preserve the compiler inputs and frozen reference provenance described in [the knowledge pipeline](knowledge-pipeline.md) as well.

The former portable-skill ZIP builder and draft-release workflow are retired. No new public binary release, tag or installer is created by this cleanup. Private recovery archives remain local; GitHub source history alone is not an off-machine backup of model/DB assets.
