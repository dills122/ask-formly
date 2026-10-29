// Execute from an isolated scratch copy containing fixtures/, examples/, node_modules/.
import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { build } from 'esbuild';
import { chromium } from 'playwright';
const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.dirname(here);
const versions = Object.fromEntries(['@angular/core','@angular/material','@ngx-formly/core','@ngx-formly/material','rxjs','zone.js','playwright','esbuild'].map(name => [name, JSON.parse(fs.readFileSync(path.join(root, 'node_modules', name, 'package.json'), 'utf8')).version]));
if (versions['@ngx-formly/core'] !== '6.3.12' || versions['@ngx-formly/material'] !== '6.3.12') throw new Error('Formly version mismatch');
await build({entryPoints: [path.join(here, 'browser.ts')], outfile: path.join(root, 'bundle.js'), bundle: true, format: 'iife', platform: 'browser', target: 'es2022'});
const browser = await chromium.launch(process.env.CHROME_PATH ? {executablePath: process.env.CHROME_PATH} : {});
try {
  const page = await browser.newPage();
  await page.setContent('<!doctype html><html><head></head><body></body></html>');
  await page.addScriptTag({path: path.join(root, 'bundle.js')});
  const result = await page.evaluate(() => window.__linkedExamples);
  const digest = file => createHash('sha256').update(fs.readFileSync(file)).digest('hex');
  const content_sha256 = Object.fromEntries(fs.readdirSync(path.join(root, 'examples')).sort().map(id => [id + '/example.ts', digest(path.join(root, 'examples', id, 'example.ts'))]));
  const fixture_sha256 = Object.fromEntries(['browser.ts', 'run.mjs', 'package.json', 'package-lock.json'].map(name => [name, digest(path.join(here, name))]));
  const report = {...result, content_sha256, fixture_sha256, environment: {...versions, node: process.version, platform: process.platform, arch: process.arch, browser: browser.version()}};
  fs.writeFileSync(path.join(root, 'results.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report, null, 2));
  if (report.status !== 'passed') process.exitCode = 1;
} finally { await browser.close(); }
