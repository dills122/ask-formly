'use strict';
// Workspace metadata is data, never a require() target. Configuration semantics
// come from the selected TypeScript compiler, not a hand-written extends merger.
const path = require('node:path');
const fs = require('node:fs');
const crypto = require('node:crypto');
const hash = data => crypto.createHash('sha256').update(data).digest('hex');
const source = file => /\.[cm]?[jt]sx?$/.test(file);

function discover(input, ts, contents) {
  const root = path.resolve(input.root), settings = input.settings || {};
  const relative = file => path.relative(root, file).split(path.sep).join('/');
  const absolute = file => path.resolve(root, file);
  const inside = file => file === root || file.startsWith(root + path.sep);
  const unresolved = [], projects = [], contexts = [], resolutionInputs = {};
  const issue = (file, reason, detail) => unresolved.push({file, reason, ...(detail ? {detail} : {})});
  function workspacePath(value, origin) {
    if (typeof value !== 'string' || path.isAbsolute(value) || value.split(/[\\/]/).includes('..')) {
      issue(origin, 'invalid-workspace-path', String(value)); return undefined;
    }
    return relative(absolute(value)) || '.';
  }
  function json(file) {
    const text = contents.get(absolute(file));
    if (text === undefined) { issue(file, 'metadata-outside-index'); return {}; }
    const parsed = ts.parseConfigFileTextToJson(file, text);
    if (parsed.error || !parsed.config || typeof parsed.config !== 'object' || Array.isArray(parsed.config)) {
      issue(file, 'metadata-parse-error'); return {};
    }
    return parsed.config;
  }
  function addProject(name, data, origin, evidence) {
    if (!data || typeof data !== 'object') { issue(origin, 'unsupported-project-entry', name); return; }
    const projectRoot = workspacePath(data.root, origin);
    if (projectRoot === undefined) return;
    const sourceRoot = data.sourceRoot === undefined ? undefined : workspacePath(data.sourceRoot, origin);
    if (JSON.stringify(data.targets || data.architect || {}).includes('fileReplacements')) issue(origin, 'build-file-replacements-not-applied', name);
    const row = {name, root: projectRoot, sourceRoot, projectType: data.projectType, file: origin,
      evidence, targets: data.targets || data.architect || {}};
    const existing = projects.find(p => p.name === name);
    if (existing) { issue(origin, 'overlapping-project-metadata', name); return; }
    if (projects.some(p => p.root === projectRoot)) issue(origin, 'overlapping-project-roots', name);
    projects.push(row);
  }
  const nx = contents.has(absolute('nx.json'));
  let kind = nx ? 'nx' : contents.has(absolute('angular.json')) ? 'angular' : 'typescript';
  let mode = nx ? 'static-candidates' : 'declared';
  let dependencies = {};
  if (settings.nx_graph) {
    const exported = json(settings.nx_graph), graph = exported.graph || exported;
    if (!graph.nodes || typeof graph.nodes !== 'object' || Array.isArray(graph.nodes)) throw new Error('Nx export must contain ProjectGraph.nodes or GraphJson.graph.nodes');
    for (const [name, node] of Object.entries(graph.nodes)) addProject(name, node.data, settings.nx_graph, 'nx-export');
    dependencies = graph.dependencies || {};
    kind = 'nx'; mode = 'exported-graph';
    issue(settings.nx_graph, 'nx-export-freshness-unverified', 'Regenerate with the installed Nx after workspace/plugin/config changes. Import does not execute or validate plugins.');
  } else {
    if (contents.has(absolute('angular.json'))) {
      const angular = json('angular.json');
      for (const [name, data] of Object.entries(angular.projects || {})) addProject(name, data, 'angular.json', nx ? 'static-candidate' : 'angular-declaration');
    }
    if (nx) {
      for (const file of contents.keys()) {
        const rel = relative(file);
        if (path.basename(file) === 'project.json') {
          const data = json(rel); addProject(data.name || relative(path.dirname(file)), {...data, root: relative(path.dirname(file)) || '.'}, rel, 'static-candidate');
        } else if (path.basename(file) === 'package.json') {
          const data = json(rel);
          if (data.nx) addProject(data.name || relative(path.dirname(file)), {...data.nx, root: relative(path.dirname(file)) || '.'}, rel, 'static-candidate');
        }
      }
      issue('nx.json', 'nx-resolved-project-graph-required', 'Static metadata cannot establish plugin-inferred projects, package workspace membership, targetDefaults or merged targets. Import nx graph --file output with --nx-graph.');
    }
  }
  projects.sort((a,b) => a.name.localeCompare(b.name));
  function owners(file) {
    const rel = relative(file);
    const matches = projects.filter(p => p.root === '.' || rel === p.root || rel.startsWith(p.root + '/'));
    const length = Math.max(-1, ...matches.map(p => p.root === '.' ? 0 : p.root.length));
    return matches.filter(p => (p.root === '.' ? 0 : p.root.length) === length).map(p => p.name);
  }
  const selected = settings.projects || projects.map(p => p.name);
  for (const name of selected) if (!projects.some(p => p.name === name)) throw new Error('Unknown workspace project: ' + name);
  const selectedProjects = projects.filter(p => selected.includes(p.name));
  // Only dependency JSON requested by TypeScript may escape the source inventory.
  // Record successes AND misses so installing/changing an extends package invalidates check.
  function canonical(file) {
    file = path.resolve(file);
    if (contents.has(file)) return file;
    if (inside(file) && relative(file).split('/').includes('node_modules')) {
      try { const real = fs.realpathSync(file); if (inside(real) && contents.has(real)) return real; } catch {}
    }
    return file;
  }
  const dependencyCache = new Map();
  function readFile(file) {
    file = path.resolve(file);
    if (contents.has(file)) return contents.get(file);
    if (!inside(file) || !relative(file).split('/').includes('node_modules')) return undefined;
    if (dependencyCache.has(file)) return dependencyCache.get(file);
    const rel = relative(file); let text;
    try {
      const real = fs.realpathSync(file);
      if (inside(real) && (file.endsWith('.json') || contents.has(real)) && fs.statSync(real).size <= 1024 * 1024) {
        const data = fs.readFileSync(real);
        if (contents.has(real) && data.toString('utf8') !== contents.get(real)) throw new Error('Workspace dependency changed during scan');
        resolutionInputs[rel] = {sha256: hash(data), realpath: relative(real)}; text = data.toString('utf8');
      } else if (file.endsWith('.json')) resolutionInputs[rel] = null;
    } catch (error) {
      if (error.message === 'Workspace dependency changed during scan') throw error;
      if (file.endsWith('.json')) resolutionInputs[rel] = null;
    }
    dependencyCache.set(file, text); return text;
  }
  const host = {
    useCaseSensitiveFileNames: true,
    readFile, fileExists: file => readFile(file) !== undefined,
    directoryExists: file => inside(path.resolve(file)) && (relative(path.resolve(file)).split('/').includes('node_modules') || ts.sys.directoryExists(file)),
    getCurrentDirectory: () => root,
    readDirectory: (dir, extensions, excludes, includes, depth) => {
      dir = path.resolve(dir);
      if (!inside(dir)) { issue(relative(dir), 'tsconfig-directory-outside-workspace'); return []; }
      const boundedIncludes = (includes || ['**/*']).filter(pattern => {
        if (inside(path.resolve(dir, pattern))) return true;
        issue(relative(dir), 'tsconfig-include-outside-workspace', pattern); return false;
      });
      if (!boundedIncludes.length) return [];
      const excluded = [...(excludes || []), '**/node_modules/**', '**/.git/**', '**/.agents/**', '**/.nx/**'];
      const matches = ts.sys.readDirectory(dir, extensions, excluded, boundedIncludes, depth);
      const omitted = matches.filter(file => !contents.has(path.resolve(file)));
      if (omitted.length) issue(relative(dir), 'tsconfig-inputs-outside-index', `${omitted.length} matching files excluded, ignored, unreadable or beyond scope`);
      return matches.filter(file => contents.has(path.resolve(file)));
    },
    onUnRecoverableConfigFileDiagnostic: diagnostic => issue(relative(diagnostic.file?.fileName || root), 'tsconfig-error', ts.flattenDiagnosticMessageText(diagnostic.messageText, '\n'))
  };
  const parsed = new Map();
  function parse(file, stack = new Set()) {
    file = path.resolve(file);
    if (stack.has(file)) { issue(relative(file), 'tsconfig-reference-cycle'); return undefined; }
    if (parsed.has(file)) return parsed.get(file);
    if (!inside(file) || !contents.has(file)) { issue(relative(file), 'tsconfig-outside-index'); return undefined; }
    const result = ts.getParsedCommandLineOfConfigFile(file, {}, host);
    parsed.set(file, result);
    if (!result) return undefined;
    for (const diagnostic of result.errors) issue(relative(file), 'tsconfig-error', ts.flattenDiagnosticMessageText(diagnostic.messageText, '\n'));
    for (const ref of result.projectReferences || []) parse(ts.resolveProjectReferencePath(ref), new Set([...stack, file]));
    return result;
  }
  function collectConfigs(value, origin, found) {
    if (!value || typeof value !== 'object') return;
    for (const [key, child] of Object.entries(value)) {
      if (key === 'tsConfig' && typeof child === 'string') {
        const rel = workspacePath(child.replaceAll('{workspaceRoot}/', ''), origin);
        if (rel) found.add(absolute(rel));
      } else collectConfigs(child, origin, found);
    }
  }
  const configFiles = new Set(), targetConfigs = new Set();
  if (settings.tsconfigs?.length) {
    for (const rel of settings.tsconfigs) configFiles.add(absolute(rel));
  } else {
    for (const project of selectedProjects) {
      const expanded = JSON.parse(JSON.stringify(project.targets).replaceAll('{projectRoot}', project.root));
      collectConfigs(expanded, project.file, targetConfigs);
    }
    for (const file of targetConfigs) configFiles.add(file);
    // Include conventional project/solution configs and arbitrary names from targets/references.
    for (const file of contents.keys()) if (/^tsconfig[^/]*\.json$/.test(path.basename(file))) {
      const owner = owners(file);
      if (!settings.projects || owner.some(p => selected.includes(p)) || path.dirname(file) === root) configFiles.add(file);
    }
  }
  for (const file of [...configFiles].sort()) parse(file);
  // Do not create a competing all-files context for configs used only as a base.
  const inherited = new Set();
  for (const result of parsed.values()) for (const file of result?.options.configFile?.extendedSourceFiles || []) inherited.add(path.resolve(file));
  for (const [file, result] of parsed) {
    if (!result || inherited.has(file) && !settings.tsconfigs?.some(f => absolute(f) === file) && !targetConfigs.has(file)) continue;
    if (result.fileNames.some(f => !contents.has(path.resolve(f)))) issue(relative(file), 'tsconfig-inputs-outside-index', 'Explicit file roots outside readable inventory');
    let names = result.fileNames.filter(f => contents.has(path.resolve(f)) && source(f));
    const owner = owners(file);
    if (settings.projects && owner.length && !owner.some(p => selected.includes(p))) continue;
    // A solution root with references is topology, not a synthetic whole-workspace app.
    if (result.projectReferences?.length && !names.length) continue;
    if (settings.projects && !owner.length) names = names.filter(f => owners(f).some(p => selected.includes(p)));
    if (!names.length) continue;
    contexts.push({id: relative(file), config: relative(file), projects: owner, rootNames: names, options: result.options,
      references: (result.projectReferences || []).map(r => relative(ts.resolveProjectReferencePath(r))), evidence: 'typescript-config'});
  }
  const configSummary = [...parsed].map(([file,result]) => ({file: relative(file), roots: result?.fileNames.map(relative) || [],
    references: (result?.projectReferences || []).map(r => relative(ts.resolveProjectReferencePath(r)))}));
  return {root, contents, host, canonical, owners, contexts, resolutionInputs, unresolved,
    workspace: {kind, mode, projects, selectedProjects: selected, dependencies, configs: configSummary}};
}
module.exports = {discover, source, hash};
