# Development

Run commands from this repository root. `npm ci --ignore-scripts --no-audit --no-fund` installs the locked TypeScript development compiler. `npm run check` runs metadata/link-target/Python/Node validation, 71 index tests from `tests/project-index/`, three packaging tests and the installed-bundle smoke exercise. `npm test`, `npm run validate`, and `npm run test:bundle` are narrower gates. Python and Node are required; graph tests cannot be skipped in the root gate.

`FORMLY_TEST_TYPESCRIPT=/absolute/path/to/typescript/lib/typescript.js` can select another existing trusted compiler for tests. Only 5.9.3 is qualified. The consuming application's compiler is selected independently by the index CLI. Build uses Python's standard library and needs no dependency installation.

## Angular probes and browser fixture

`qualification/` and `evaluation/` are intentionally ignored and absent from fresh checkouts. CI uses the committed `tests/project-index/` sources and does not need those archives. The commands below are optional local reproductions and require the historical `qualification/` folder to be present. These remain separate, locked development fixtures. Avoid changing retained result files when reproducing them; copy sources into an ignored work area first. The following are relocated reproduction commands; see [extraction](extraction.md) for what was actually run during the move.

```sh
mkdir -p local/qualification
cp qualification/package.json qualification/package-lock.json qualification/probe.mjs local/qualification/
npm ci --prefix local/qualification --ignore-scripts --no-audit --no-fund
(cd local/qualification && node probe.mjs > current-results.json 2> current-stderr.log)

mkdir -p local/browser
cp -R qualification/browser/. local/browser/
(cd local/browser && npm exec --yes --package=npm@11.6.2 -- npm ci --ignore-scripts --no-audit --no-fund)
(cd local/browser && node zoneless-probe.mjs > current-zoneless.json)
(cd local/browser && NG_BUILD_MAX_WORKERS=2 ./node_modules/.bin/ng build)
(cd local/browser && node check-aot-guard.mjs)
(cd local/browser && ./node_modules/.bin/playwright install chromium)
(cd local/browser && ./node_modules/.bin/playwright test)
```

The full browser suite previously passed 12/14; B06/B13 are retained ordinary failures and B14 verifies close/reopen recovery. Do not add a forced-success exit, skip them, or claim an all-green browser gate. These optional runtime commands install substantially more dependencies than the root index tests. Earlier npm 10 fixture resolution failed; the browser reproduction retains the npm 11.6.2 runner used previously.

## Historical evidence

Original source/evidence was copied without rewriting embedded Research Depot paths, timestamps or checksums. Frozen audit scripts depend on their original snapshots and scratch fixtures; they are not current CI gates. At extraction, only the current graph test's compiler fallback changed. After the owner excluded the archives, the two active regression files were copied into `tests/project-index/`; those are now canonical for CI. See [source manifest](extraction-source-manifest.json). New test commands must not assume Research Depot is present.

The pinned upstream cache was copied to ignored local/ask-formly/upstream for local source inspection. It is not part of the skill ZIP or a fresh clone. Exact upstream URLs/hashes remain in the skill's evidence references.

## Workspace discovery qualification

The regular gate includes 16 workspace-specific regression tests. The optional real-tool harness compares generated Angular project inventories with Angular's workspace API and imports actual Nx graphs for integrated and package-based fixtures (including a local inference plugin). It executes only the harness's generated temporary workspaces and removes them afterwards. It does not depend on the ignored historical archives.

Provide trusted existing installations, or install the pinned qualification tools into an ignored local directory:

```sh
npm install --prefix local/workspace-tools --ignore-scripts --no-audit --no-fund nx@23.3.0 @angular-devkit/core@21.2.27
node tools/qualify_workspaces.cjs \
  --nx-package "$PWD/local/workspace-tools/node_modules/nx/package.json" \
  --angular-core "$PWD/local/workspace-tools/node_modules/@angular-devkit/core"
```

Qualified with Node 22.23.3 / TypeScript 5.9.3. This is an optional additional tool integration check, not part of `npm run check` and not a browser or Angular compilation gate. See [workspace research and results](workspace-support-research.md).

## Exact pnpm Nx Formly fixture

Three additional offline regressions exercise the committed apps/libs fixture,
captured Nx export, full cross-library flow, a broken barrel and freshness. They
run in `npm run check`. For a real install/export/package-link check, copy the
fixture into a disposable ignored directory and use pnpm 10.23.0 with Node 22:

```sh
mkdir -p local/pnpm-nx-formly
cp -R tests/fixtures/pnpm-nx-formly/. local/pnpm-nx-formly/
pnpm --dir local/pnpm-nx-formly install --frozen-lockfile --ignore-scripts
python3 tools/qualify_pnpm_nx.py --workspace "$PWD/local/pnpm-nx-formly"
```

The harness regenerates the Nx graph, checks the full admin flow, then temporarily
removes the base config's path aliases to check real pnpm source package exports.
It restores the base config and index afterwards. Use only a disposable fixture
copy; this command writes its config/index and executes its installed Nx. It does
not build an Angular app or test runtime peer compatibility. See the
[executed qualification and public corpus](pnpm-nx-public-qualification.md).
