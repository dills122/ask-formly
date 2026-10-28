# Model-free alpha release checklist

The next release target is the **model-free alpha**: calling-agent reasoning, local read-only knowledge retrieval, and no server models or hosted provider calls. The installed knowledge remains exactly 192 facts / 36 documents for Formly 6.3.12 core/Material.

No public release or downloadable alpha artifact is currently published. The source and packaging tools are in Git; generated archives, environments and raw test evidence remain private. A fresh clone does not contain the DB needed to build the runtime artifact.

## Established

- [x] Separate model-free artifact builder, installer, dependency pins and generated stdio configuration.
- [x] Integrity checks, refusal to overwrite an existing installation, doctor and real MCP startup/lookup self-test.
- [x] Clean-environment install on the existing macOS arm64 host with Python 3.14.6.
- [x] Real calling-agent checks of lookup, discovery/fetch, scope repair and unsupported-version stopping.
- [x] Bounded JSON Schema recovery fix, regression replay and independent review.
- [x] [Installation guide](../poc/contextual-kb/alpha/README.md) covering connection, first request, troubleshooting and rollback.

See the [alpha checkpoint](../poc/contextual-kb/alpha/RESULTS.md) for exact results, retained failures and test limitations. These checks do not qualify other operating systems, every Python version, Claude/Kiro, or whole-library answer accuracy.

## Before publishing an alpha

1. **Settle the release contents and licensing.** Choose the license for original project code, confirm which knowledge/source excerpts may be distributed, and include the applicable notices in the artifact. The repository has no project-wide license today. Existing [upstream attribution](../skill/ask-formly/THIRD_PARTY_NOTICES.md) is a starting point, not a project license.
2. **Choose the support statement.** The evidence currently supports a macOS arm64/Python 3.14.6 clean-environment alpha. Mark other combinations experimental unless they receive their own install and caller checks. The installer accepting Python 3.11+ is not evidence that all such versions work.
3. **Freeze a release candidate.** Select the release commit/version, build a new allowlisted archive from the pinned DB, and retain its checksum. Decide whether the release also carries a publisher signature; the current checksum is not one. Do not upload the private recovery bundle or raw test-output directory.
4. **Follow the published instructions on an independent setup.** Install in a new destination; verify doctor and self-test; configure a real agent; exercise a supported question, scope repair, discovery/fetch and unsupported-version stopping. Record the actual platform/client. Preserve existing installations for rollback.
5. **Publish only the approved artifact and release notes.** Notes should include supported scope/platforms, prerequisites, archive/checksum, setup link, test limits and known retrieval limitations. Link the README to the real download once it exists. Do not invent a download URL in advance.

Documentation changes inside `alpha/README.md` alter future package bytes: rebuild and checksum the final artifact after the release documentation is frozen. Historical artifact checksums in the results apply only to those original archives.

## Maintainer build and verification

Use the [artifact build instructions](../poc/contextual-kb/alpha/README.md#build-from-the-provisioned-repository), then install into a separate new path. Run the normal local checks from the provisioned repository:

```sh
python3 tools/project.py check
```

Source-only CI is deliberately narrower: it does not download private runtime assets or qualify a complete installation. Release checks use the exact archive intended for distribution. No release check needs to modify the installed DB/models or open sealed evaluation.

## Recovery is separate

The [allowlisted recovery bundle](../poc/contextual-kb/packaging/README.md) protects the existing model-backed setup locally. It contains a different asset set and is not the model-free alpha download. Retain compiler inputs and frozen provenance described in the [knowledge pipeline](knowledge-pipeline.md).

Private recovery archives, environments, raw requests, model weights and sealed evaluation must stay out of Git and public release uploads. Source history alone is not an off-machine backup of private runtime assets. The former portable-skill ZIP builder and draft-release workflow remain retired.
