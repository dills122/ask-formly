# Linked example browser fixtures

These checks execute the three candidate examples with **Formly core/Material
6.3.12 and Angular/Material 18.2.14**. They do not promote candidate knowledge or
qualify other dependency versions. Historical browser failures B06/B13 remain
unchanged; these are new bounded scenarios.

From the repository root, use a new output directory. This command installs only
into that directory, checks TypeScript, bundles the exact example source files,
and runs Angular JIT TestBed in a headless browser:

```sh
CHROME_PATH='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' \
python3 poc/contextual-kb/linked_examples_v1/fixtures/run.py \
  --output test-output/linked-examples-v1/browser-check
```

`CHROME_PATH` may point to another installed Chrome/Chromium executable. If
omitted, Playwright expects its own previously installed Chromium. Node/npm and
network access for the first pinned dependency install are required. The lockfile
pins transitive dependencies; no forced peer resolution or shared dependency
environment is used. `npm ci --ignore-scripts` avoids dependency install scripts.
The browser uses an isolated temporary profile, without the user's browser data.

The runner writes `results.json` and bundle/dependencies only in the new output
directory. A failure exits nonzero. The report records actual package/browser
versions, example code hashes, fixture/lock hashes, and each assertion result.
`--skipLibCheck` skips dependency declaration checking; the delivered examples
and fixture are still typechecked. The 17 assertions cover:

- Hide/show with retained model value and removed/re-registered control.
- Supplementary reset-on-hide enabled and visible shared-key exception cases.
- Distinct nested section controls, enclosing model scopes, and independent edits.
- Existing model value versus undefined fallback, returned onInit subscription,
  and disposal after component destruction.

The examples are original illustrations linked to unchanged authored facts.
Application choices are not upstream examples or universal guarantees. Browser
execution verifies these assertions, not all conditions stated by linked facts.
