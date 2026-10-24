# Packaging and recovery boundaries

The source checkpoint and draft PR preserve the accepted local MCP implementation, tests, setup, pins and compact history. They do not silently publish model weights, raw request/model logs, sealed evaluation, environments or downloaded caches into the public GitHub repository.

A separate allowlisted **local runtime bundle** includes exact pinned runtime/model/DB bytes plus active source/docs. It excludes environments and sealed evaluation. `bundle.py` verifies every member against its internal SHA-256 manifest and writes a whole-archive checksum. It refuses overwrite, outside paths and sealed/evaluation paths. This is local recovery packaging, not a public redistribution license or a tested fresh-machine installer.

```sh
python3 -B poc/contextual-kb/packaging/bundle.py --output /absolute/path/to/new-formly-foundation.tar.gz
```

`runtime-files.json` is the exact allowlist. Restore the archive's contextual-kb directory into a POC location, retain/create the two Python environments using the locked package lists, and run the stable launcher's doctor. Existing absolute paths in client examples need adjustment when relocating. Do not overwrite an existing checkout to test recovery. A model-enabled fresh-machine restoration is not qualified by this packaging checkpoint.

Recovery artifacts for the cleanup are under the ignored `local/poc-safety/2026-10-24/` directory in this checkout. The pre-cleanup full-POC archive is private local evidence; it includes historical raw artifacts and sealed bytes and must not be uploaded as a public PR artifact. The separate repository-source archive preserves the non-POC working source before cleanup, excluding environments/caches/credentials/AI shared links. Archive verification and checksums are recorded locally.

**GitHub backs up source and compact documentation, not the large runtime weights.** The local verified archives protect against cleanup mistakes on this machine, not disk loss. An off-machine private artifact backup is a separate operation; none is claimed here. Do not delete the recovery archives merely because the source PR exists.

The model and DB contents are unchanged. The accepted runtime still uses several historically named directories: these are retained dependencies, not invitations to revive abandoned experiments. Historical byte-level freeze chains belong to the recovery archive after cleanup; current startup uses the compact accepted foundation manifest. Original reports remain reconstructable from the recovery archive; the high-level history is versioned.

The final legacy retirement is archived separately under `local/poc-safety/2026-10-24/retirement/`. The active repository now centers this POC. Its compiler inputs and frozen original reference documents remain in Git; see [knowledge pipeline](../../../docs/knowledge-pipeline.md). The runtime bundle alone is not a complete compiler-source distribution: retain the source checkout as well. `source-files.json` pins repository-relative compiler/provenance inputs for source checks and is separate from the runtime bundle allowlist.
