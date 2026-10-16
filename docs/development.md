# Development

Run commands from this repository root. `npm ci --ignore-scripts --no-audit --no-fund` installs the locked TypeScript development compiler. `npm run check` runs metadata/link-target/Python/Node validation, 25 index tests, three packaging tests and the installed-bundle smoke exercise. `npm test`, `npm run validate`, and `npm run test:bundle` are narrower gates. Python and Node are required; graph tests cannot be skipped in the root gate.

`FORMLY_TEST_TYPESCRIPT=/absolute/path/to/typescript/lib/typescript.js` can select another existing trusted compiler for tests. Only 5.9.3 is qualified. The consuming application's compiler is selected independently by the index CLI. Build uses Python's standard library and needs no dependency installation.

## Angular probes and browser fixture

These remain separate, locked development fixtures. Avoid changing retained result files when reproducing them; copy sources into an ignored work area first. The following are relocated reproduction commands; see [extraction](extraction.md) for what was actually run during the move.

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

Original source/evidence was copied without rewriting embedded Research Depot paths, timestamps or checksums. Frozen audit scripts depend on their original snapshots and scratch fixtures; they are not current CI gates. The only modified extracted original file is the current index graph test's compiler fallback, now pointing at this repository's node_modules. See [source manifest](extraction-source-manifest.json). New test commands must not assume Research Depot is present.

The pinned upstream cache was copied to ignored local/ask-formly/upstream for local source inspection. It is not part of the skill ZIP or a fresh clone. Exact upstream URLs/hashes remain in the skill's evidence references.
