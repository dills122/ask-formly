# Packaging and releases

`npm run build` creates `dist/ask-formly-<version>.zip`, `.zip.sha256` and `.manifest.json`. The ZIP contains one ask-formly folder with only the portable skill. Preserve its layout and third-party notices when installing. `npm run test:bundle` checks hashes and exercises the extracted scanner/graph/notes against a synthetic project.

The root package is private and is not an npm distribution. Version starts at 0.1.0-dev for this standalone development snapshot. Update package.json and package-lock.json together for a release.

Prepared GitHub CI runs the root gate on pushes and pull requests. The release workflow is manually dispatched, repeats the gate, requires an existing version-matched tag at the tested commit, and creates a draft release. No remote, tag or hosted run exists from this extraction. Decide the original-work license, remote owner/visibility and publication intent before distributing publicly; the upstream MIT notice does not license the owner's original project automatically.
