# Model-free alpha release checklist

## Current release candidate

`v0.1.0-rc.1` packages the [issue 21 demo repairs](issue-21-followup.md) with
model-free runtime `discovery8`. The knowledge DB remains byte-identical to the
192-fact baseline. Download `ask-formly-v0.1.0-rc.1-model-free.tar.gz` and its
matching checksum from [GitHub Releases](https://github.com/dills122/ask-formly/releases).
The archive retains the `ask-formly-alpha/` extraction directory. It adds
`help_formly` and uses the documented compact, single-JSON-text response contract.
The RC designation does not extend supported versions, adapters or platforms.

The exact 31-file RC archive passed a fresh virtual-environment install on
macOS arm64/Python 3.14.6, including pinned dependency installation, `pip check`,
doctor and real MCP self-test. The source suite passed 274 tests. These are
model-free release checks, not full model-backed or Angular/browser qualification.
The worktree's full local maintenance command remains unavailable without its
provisioned environments. The same Pydantic forward-reference warning appeared;
startup and lookup passed. Checksums remain unsigned.

RC archive SHA-256: `adce512cfe414c4982db0e3b0bc6fb53ae4120691419f49538594e20bbecb81e`.
The DB hash remains `f65802b58ec4f1c2719efd8dc1e391d7e250643a94c96b7a71d446ae67fe1b09`.

The original alpha milestone and its checksums below remain historical evidence.

The next release target is the **model-free alpha**: calling-agent reasoning, local read-only knowledge retrieval, and no server models or hosted provider calls. The installed knowledge remains exactly 192 facts / 36 documents for Formly 6.3.12 core/Material.

The first prerelease is `v0.1.0-alpha.1`; download its named model-free archive and checksum from [GitHub Releases](https://github.com/dills122/ask-formly/releases). The source and packaging tools are in Git; generated archives, environments and raw test evidence remain private. A fresh clone does not contain the DB needed to build the runtime artifact.

## Established

- [x] Separate model-free artifact builder, installer, dependency pins and generated stdio configuration.
- [x] Integrity checks, refusal to overwrite an existing installation, doctor and real MCP startup/lookup self-test.
- [x] Clean-environment install on the existing macOS arm64 host with Python 3.14.6.
- [x] Real calling-agent checks of lookup, discovery/fetch, scope repair and unsupported-version stopping.
- [x] Bounded JSON Schema recovery fix, regression replay and independent review.
- [x] [Installation guide](../poc/contextual-kb/alpha/README.md) covering connection, first request, troubleshooting and rollback.

See the [alpha checkpoint](../poc/contextual-kb/alpha/RESULTS.md) for exact results, retained failures and test limitations. These checks do not qualify other operating systems, every Python version, Claude/Kiro, or whole-library answer accuracy.

## First prerelease verification

`v0.1.0-alpha.1` includes 27 allowlisted payload files plus its integrity manifest. The final archive passed a fresh virtual-environment install, dependency checks, doctor and real stdio MCP initialization/catalog/read-only lookup on macOS arm64/Python 3.14.6. This repeated packaging/startup verification, not a new answer-quality qualification or a separate physical-machine test. The dependency emitted a Pydantic forward-reference warning; startup and lookup still passed.

Archive SHA-256: `cea989d620158ce82857a191f614f2c55f2502752b3e7235118b5354ee1af35e`. Bundled DB SHA-256: `f65802b58ec4f1c2719efd8dc1e391d7e250643a94c96b7a71d446ae67fe1b09`, identical to the installed baseline. Local maintenance and all 10 packaging tests passed. Licensing inclusion was tested red/green. Models, runtime implementations and sealed evaluation were unchanged. Checksums are unsigned.

## Checklist for subsequent alphas

1. **Confirm release contents and licensing.** Original project code uses [MIT](../LICENSE). The package includes that license and the full upstream Formly MIT notice, verified at the pinned source revision. Keep both notices in future artifacts.
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
