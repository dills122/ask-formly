#!/usr/bin/env node
'use strict';
// Static compiler API only. Never load application modules or evaluate factories.
const fs = require('node:fs');
const path = require('node:path');

const {discover, source, hash} = require('./workspace.cjs');

function analyze(input, ts, workspace, context) {
  const root = workspace.root, contents = workspace.contents;
  const nodes = [], edges = [], unresolved = [];
  const byId = new Map(), astIds = new WeakMap(), edgeKeys = new Set(), issues = new Set();
  const relative = file => path.relative(root, file).split(path.sep).join('/');
  function issue(node, reason, detail) {
    const item = { reason, ...(typeof node === 'string' ? { file: node } : node ? location(node) : {}), ...(detail ? { detail } : {}) };
    const key = JSON.stringify(item);
    if (!issues.has(key)) { issues.add(key); unresolved.push(item); }
  }
  function location(node) {
    const sf = node.getSourceFile();
    return { file: relative(sf.fileName), line: sf.getLineAndCharacterOfPosition(node.getStart(sf)).line + 1 };
  }
  function add(kind, name, node, extra = {}) {
    const loc = typeof node === 'string' ? { file: node, line: 1 } : location(node);
    const id = `${loc.file}:${typeof node === 'string' ? 0 : node.getStart()}:${kind}${kind === 'registration' ? ':' + extra.scope + ':' + extra.category : ''}`;
    if (!byId.has(id)) { const value = { id, kind, name, ...loc, ...extra }; byId.set(id, value); nodes.push(value); }
    return id;
  }
  function edge(from, relation, to, evidence = 'static-source') {
    if (!from || !to || from === to) return;
    const key = JSON.stringify([from, relation, to, evidence]);
    if (!edgeKeys.has(key)) { edgeKeys.add(key); edges.push({ from, relation, to, evidence }); }
  }
  const options = { experimentalDecorators: true, target: ts.ScriptTarget.Latest, module: ts.ModuleKind.ESNext,
    moduleResolution: ts.ModuleResolutionKind.Node10, ...context.options, noLib: true, noEmit: true, allowJs: true };
  const host = ts.createCompilerHost(options);
  host.readFile = workspace.host.readFile;
  host.fileExists = workspace.host.fileExists;
  host.directoryExists = workspace.host.directoryExists;
  host.getDirectories = () => [];
  host.getCurrentDirectory = () => root;
  host.realpath = workspace.canonical;
  host.getSourceFile = (file, languageVersion) => { const real = workspace.canonical(file); return contents.has(real) ? ts.createSourceFile(real, contents.get(real), languageVersion, true) : undefined; };
  host.writeFile = () => { throw new Error('No emit allowed'); };
  const program = ts.createProgram(context.rootNames, options, host), checker = program.getTypeChecker();
  const sources = program.getSourceFiles().filter(sf => contents.has(sf.fileName));
  const fileIds = new Map(sources.map(sf => [sf.fileName, add('file', relative(sf.fileName), relative(sf.fileName))]));
  const walk = (node, fn) => { fn(node); ts.forEachChild(node, child => walk(child, fn)); };
  const nameOf = node => node && (ts.isIdentifier(node) || ts.isStringLiteralLike(node) || ts.isNumericLiteral(node)) ? node.text : undefined;
  const prop = (obj, name) => ts.isObjectLiteralExpression(obj) ? [...obj.properties].reverse().find(p => nameOf(p.name) === name) : undefined;
  const value = (obj, name) => { const p = prop(obj, name); return p && (p.initializer || (ts.isShorthandPropertyAssignment(p) ? p.name : undefined)); };
  const literal = node => node && ts.isStringLiteralLike(node) ? node.text : undefined;
  function declarations(node) {
    let symbol = ts.isShorthandPropertyAssignment(node.parent) ? checker.getShorthandAssignmentValueSymbol(node.parent) : checker.getSymbolAtLocation(node);
    if (symbol && symbol.flags & ts.SymbolFlags.Alias) symbol = checker.getAliasedSymbol(symbol);
    return symbol ? symbol.declarations || [] : [];
  }
  function target(node) {
    if (!node) return undefined;
    if (ts.isPropertyAccessExpression(node)) node = node.name;
    return declarations(node).map(d => astIds.get(d)).find(Boolean);
  }
  function owner(node) {
    for (let p = node; p; p = p.parent) if (astIds.has(p)) return astIds.get(p);
    return fileIds.get(node.getSourceFile().fileName);
  }
  function resolve(node, seen = new Set()) {
    if (!node || seen.has(node)) return node;
    seen.add(node);
    if (ts.isAsExpression(node) || ts.isParenthesizedExpression(node) || ts.isSatisfiesExpression(node)) return resolve(node.expression, seen);
    if (ts.isIdentifier(node) || ts.isPropertyAccessExpression(node)) {
      const ds = declarations(ts.isPropertyAccessExpression(node) ? node.name : node);
      const init = ds.find(d => d.initializer);
      if (init) return resolve(init.initializer, seen);
    }
    return node;
  }
  const classInfo = [], registry = [], fields = [], fieldProperties = new WeakMap();
  for (const sf of sources) {
    if (sf.parseDiagnostics.length) issue(sf, 'typescript-parse-errors');
    walk(sf, node => {
      if (ts.isClassDeclaration(node) || ts.isFunctionDeclaration(node) || ts.isVariableDeclaration(node) || ts.isPropertyDeclaration(node) || ts.isMethodDeclaration(node) || ts.isGetAccessorDeclaration(node)) {
        const name = nameOf(node.name);
        if (!name) return;
        const kind = ts.isClassDeclaration(node) ? 'class' : ts.isFunctionDeclaration(node) || ts.isMethodDeclaration(node) ? 'function' : 'declaration';
        const parent = owner(node.parent), id = add(kind, name, node);
        astIds.set(node, id); edge(parent, 'contains', id);
      }
      if (ts.isObjectLiteralExpression(node) && (value(node, 'type') || value(node, 'fieldGroup') || value(node, 'fieldArray') || value(node, 'key') && (['validators', 'asyncValidators'].some(k => value(node, k)) || node.properties.some(ts.isSpreadAssignment)))) {
        const properties = objectProperties(node, 'field'), key = properties?.get('key');
        const name = !properties ? '(unresolved field)' : literal(resolve(key)) ?? (key ? '(computed key)' : properties.has('type') ? '(keyless type)' : '(unkeyed group)');
        const id = add('field-config', name, node, { evidence: 'structural-candidate' });
        edge(owner(node.parent), 'contains-field', id); astIds.set(node, id); fields.push(node); fieldProperties.set(node, properties);
      }
    });
  }
  function moduleTarget(sf, specifier) {
    const file = ts.resolveModuleName(specifier, sf.fileName, options, host).resolvedModule?.resolvedFileName;
    return file && workspace.canonical(file);
  }
  function importedName(expression, module) {
    // Check lexical binding identity, not spelling: a local parameter may shadow an import.
    const namespace = expression && ts.isPropertyAccessExpression(expression);
    const local = namespace ? expression.expression : expression;
    if (!local || !ts.isIdentifier(local)) return undefined;
    const symbol = checker.getSymbolAtLocation(local);
    for (const declaration of symbol?.declarations || []) {
      const imported = namespace ? ts.isNamespaceImport(declaration) : ts.isImportSpecifier(declaration);
      if (!imported) continue;
      let statement = declaration.parent;
      while (statement && !ts.isImportDeclaration(statement)) statement = statement.parent;
      if (statement && literal(statement.moduleSpecifier) === module) {
        return namespace ? expression.name.text : (declaration.propertyName || declaration.name).text;
      }
    }
    return undefined;
  }
  function hasFormlyProviderToken(expression, seen = new Set()) {
    const node = resolve(expression);
    if (!node || !ts.isObjectLiteralExpression(node) || seen.has(node)) return false;
    seen = new Set(seen); seen.add(node);
    if (importedName(value(node, 'provide'), '@ngx-formly/core') === 'FORMLY_CONFIG') return true;
    return node.properties.some(p => ts.isSpreadAssignment(p) && hasFormlyProviderToken(p.expression, seen));
  }
  function objects(expression, context, reason, seen = new Set()) {
    const resolved = resolve(expression);
    if (seen.has(resolved)) { issue(context, 'cyclic-static-array'); return []; }
    seen = new Set(seen); seen.add(resolved);
    if (resolved && ts.isArrayLiteralExpression(resolved)) return resolved.elements.flatMap(e => ts.isSpreadElement(e) ? objects(e.expression, context, reason, seen) : objects(e, context, reason, seen));
    if (resolved && ts.isObjectLiteralExpression(resolved)) return [resolved];
    issue(context, reason); return [];
  }
  function objectProperties(expression, purpose = 'registration', seen = new Set(), report = true) {
    const resolved = resolve(expression);
    if (!resolved || !ts.isObjectLiteralExpression(resolved)) { if (report) issue(expression, `dynamic-${purpose}-config`); return undefined; }
    if (seen.has(resolved)) { if (report) issue(expression, `cyclic-${purpose}-config`); return undefined; }
    seen = new Set(seen); seen.add(resolved);
    const properties = new Map();
    for (const p of resolved.properties) {
      if (ts.isSpreadAssignment(p)) {
        const spread = objectProperties(p.expression, purpose, seen, report);
        if (!spread) return undefined; // Unknown spread can override any category.
        for (const [key, val] of spread) properties.set(key, val);
      } else {
        const key = nameOf(p.name);
        if (!key) { if (report) issue(p, `computed-${purpose}-property`); return undefined; }
        properties.set(key, p.initializer || (ts.isShorthandPropertyAssignment(p) ? p.name : undefined));
      }
    }
    return properties;
  }
  function registration(entry, expression) {
    const objs = objects(expression, expression, 'dynamic-registration-config');
    for (const obj of objs) {
      const properties = objectProperties(obj); if (!properties) continue;
      for (const category of ['types', 'wrappers', 'validators', 'validationMessages', 'extensions', 'presets']) {
        const expr = properties.get(category); if (!expr) continue;
        for (const item of objects(expr, expr, 'dynamic-registration-list')) {
          const itemProperties = objectProperties(item); if (!itemProperties) continue;
          const name = literal(resolve(itemProperties.get('name')));
          if (name === undefined) { issue(item, 'dynamic-registration-name'); continue; }
          const id = add('registration', name, item, { category, scope: entry }); registry.push({ id, name, category, properties: itemProperties });
          edge(entry, 'registers', id);
          for (const key of ['component', 'validation', 'extension', 'message', 'fields']) {
            const impl = itemProperties.get(key); if (!impl) continue;
            const dest = target(impl);
            if (dest) edge(id, 'implementation', dest);
            else { const inline = add('inline-implementation', key, impl); edge(id, 'implementation', inline); edge(inline, 'defined-in', fileIds.get(impl.getSourceFile().fileName)); }
          }
          for (const key of ['extends', 'wrappers']) if (itemProperties.has(key)) issue(item, 'registration-inheritance-needs-review', key);
        }
      }
    }
  }
  for (const sf of sources) walk(sf, node => {
    if (ts.isIdentifier(node) && (node.parent?.name !== node || ts.isShorthandPropertyAssignment(node.parent))) edge(owner(node), 'references', target(node));
    // Property-access names need checker resolution too (e.g. this.fields).
    if (ts.isPropertyAccessExpression(node)) edge(owner(node), 'references', target(node));
    if (ts.isBinaryExpression(node) && node.operatorToken.kind === ts.SyntaxKind.EqualsToken) {
      const dest = target(node.left);
      walk(node.right, part => {
        if (ts.isIdentifier(part) || ts.isPropertyAccessExpression(part)) edge(dest, 'assigned-from', target(part));
        if (astIds.has(part)) edge(dest, 'assigned-from', astIds.get(part));
      });
    }
    if (ts.isImportDeclaration(node) || ts.isExportDeclaration(node)) {
      const specifier = literal(node.moduleSpecifier);
      if (specifier) { const dest = moduleTarget(sf, specifier); if (dest) edge(fileIds.get(sf.fileName), 'imports', fileIds.get(dest)); else if (specifier.startsWith('.') || !specifier.startsWith('@angular/') && !specifier.startsWith('@ngx-formly/')) issue(node, 'import-outside-index-or-unresolved', specifier); }
    }
    if (ts.isCallExpression(node)) {
      const api = importedName(node.expression, '@ngx-formly/core');
      if (['provideFormlyCore', 'provideFormlyConfig'].includes(api)) {
        const id = add('entry-point', api, node, { registration_mode: api });
        edge(owner(node), 'configures', id);
        if (node.arguments[0]) {
          registration(id, node.arguments[0]);
          const config = resolve(node.arguments[0]);
          // Locate a factory without evaluating its return value or injector scope.
          if (config && ts.isCallExpression(config)) edge(id, 'config-factory', target(config.expression));
        }
      }
      if (node.expression.kind === ts.SyntaxKind.ImportKeyword) {
        const specifier = literal(node.arguments[0]), dest = specifier && moduleTarget(sf, specifier);
        if (dest) edge(owner(node), 'lazy-import', fileIds.get(dest)); else issue(node, 'dynamic-or-external-import');
      }
      if (ts.isPropertyAccessExpression(node.expression)) {
        const mode = node.expression.name.text, receiver = node.expression.expression;
        if (['forRoot', 'forChild'].includes(mode) && importedName(receiver, '@ngx-formly/core') === 'FormlyModule') {
          const id = add('entry-point', `FormlyModule.${mode}`, node, { registration_mode: mode }); edge(owner(node), 'configures', id);
          if (node.arguments[0]) registration(id, node.arguments[0]);
        }
      }
    }
    if (ts.isObjectLiteralExpression(node)) {
      const knownProvider = hasFormlyProviderToken(node);
      // Probe other spreads quietly: most object literals are unrelated to Angular providers.
      const provider = knownProvider || node.properties.some(ts.isSpreadAssignment)
        ? objectProperties(node, 'provider', new Set(), knownProvider) : undefined;
      if (importedName(provider?.get('provide'), '@ngx-formly/core') === 'FORMLY_CONFIG') {
        const id = add('entry-point', 'FORMLY_CONFIG', node, { registration_mode: 'provider' }); edge(owner(node), 'configures', id);
        const configValue = provider.get('useValue');
        if (configValue) registration(id, configValue);
        else {
          // An implementation pointer is useful even when its output is unknowable.
          const factory = provider.get('useFactory'), resolved = resolve(factory);
          const implementation = target(factory);
          if (implementation) edge(id, 'provider-factory', implementation);
          else if (resolved && (ts.isArrowFunction(resolved) || ts.isFunctionExpression(resolved))) {
            const inline = add('inline-implementation', 'useFactory', resolved);
            edge(id, 'provider-factory', inline);
            edge(inline, 'defined-in', fileIds.get(resolved.getSourceFile().fileName));
          }
          issue(node, 'dynamic-provider-factory');
        }
      }
      const routePath = literal(value(node, 'path'));
      if (routePath !== undefined && ['component', 'loadComponent', 'loadChildren', 'children'].some(k => value(node, k))) {
        const id = add('route', routePath, node, { evidence: 'route-candidate' }); edge(owner(node), 'contains-route', id);
        edge(id, 'route-component', target(value(node, 'component')));
        walk(node, child => { if (ts.isCallExpression(child) && child.expression.kind === ts.SyntaxKind.ImportKeyword) { const dest = literal(child.arguments[0]) && moduleTarget(sf, literal(child.arguments[0])); if (dest) edge(id, 'lazy-import', fileIds.get(dest)); } });
      }
    }
    if (ts.isClassDeclaration(node)) {
      for (const decorator of ts.getDecorators(node) || []) {
        const call = decorator.expression;
        if (!ts.isCallExpression(call) || importedName(call.expression, '@angular/core') !== 'Component') continue;
        const meta = resolve(call.arguments[0]); if (!meta || !ts.isObjectLiteralExpression(meta)) { issue(node, 'dynamic-component-metadata'); continue; }
        const url = literal(value(meta, 'templateUrl')), inline = value(meta, 'template');
        const templateFile = url && path.resolve(path.dirname(sf.fileName), url);
        const template = templateFile ? contents.get(templateFile) : literal(inline);
        classInfo.push({ node, id: astIds.get(node), selector: literal(value(meta, 'selector')), template, templateFile, inline });
        if (templateFile) { if (template !== undefined && !fileIds.has(templateFile)) fileIds.set(templateFile, add('file', relative(templateFile), relative(templateFile))); edge(astIds.get(node), 'template', fileIds.get(templateFile)); if (template === undefined) issue(node, 'template-outside-index'); }
      }
    }
  });
  function candidate(from, name, category, relation) {
    const matches = registry.filter(r => r.name === name && r.category === category);
    for (const r of matches) edge(from, relation, r.id, 'registration-scope-unresolved');
    if (!matches.length) issue(byId.get(from).file, 'registration-not-in-index', category + ':' + name);
  }
  function arrayItems(expression, reason, seen = new Set()) {
    const resolved = resolve(expression);
    if (seen.has(resolved)) { issue(expression, 'cyclic-static-array'); return []; }
    if (!resolved || !ts.isArrayLiteralExpression(resolved)) { issue(expression, reason); return []; }
    seen = new Set(seen); seen.add(resolved);
    return resolved.elements.flatMap(item => ts.isSpreadElement(item) ? arrayItems(item.expression, reason, seen) : [item]);
  }
  function wrapperCandidates(from, expression) {
    if (!expression) return;
    for (const item of arrayItems(expression, 'dynamic-wrapper-list')) {
      const name = literal(resolve(item));
      if (name !== undefined) candidate(from, name, 'wrappers', 'wrapper-candidate');
      else issue(item, 'dynamic-wrapper');
    }
  }
  // Follow declared relationships without merging defaults or choosing injector scope.
  for (const registration of registry) {
    if (registration.category !== 'types') continue;
    const base = registration.properties.get('extends'), name = literal(resolve(base));
    if (name !== undefined) candidate(registration.id, name, 'types', 'extends-type-candidate');
    wrapperCandidates(registration.id, registration.properties.get('wrappers'));
  }
  for (const node of fields) {
    const properties = fieldProperties.get(node); if (!properties) continue;
    const id = astIds.get(node), type = properties.get('type');
    if (type) { const name = literal(resolve(type)); if (name !== undefined) candidate(id, name, 'types', 'type-candidate'); else issue(type, 'dynamic-field-type'); }
    wrapperCandidates(id, properties.get('wrappers'));
    for (const group of ['validators', 'asyncValidators']) {
      const validators = resolve(properties.get(group)); if (!validators) continue;
      if (!ts.isObjectLiteralExpression(validators)) { issue(validators, 'dynamic-field-validators'); continue; }
      const validatorProperties = objectProperties(validators, 'validator'); if (!validatorProperties) continue;
      for (const [name, expr] of validatorProperties) {
        if (!expr) continue;
        if (name === 'validation') {
          for (const item of arrayItems(expr, 'dynamic-validator-list')) {
            const key = literal(resolve(item));
            if (key !== undefined) candidate(id, key, 'validators', 'validator-candidate');
            else {
              const implementation = target(item);
              if (implementation) edge(id, 'validator-function', implementation);
              else issue(item, 'dynamic-validator-list');
            }
          }
        } else { const validator = add('inline-validator', name, expr); edge(id, 'validates-with', validator); edge(validator, 'implementation', target(expr)); }
      }
    }
  }
  for (const info of classInfo) {
    if (info.template === undefined) continue;
    // Recognize only direct members and simple runtime-value source pointers.
    const template = info.template.replace(/<!--[\s\S]*?-->/g, match => match.replace(/[^\n]/g, ' '));
    // Without an Angular scope parser, decline possible local shadows anywhere in this template.
    // Explicit this.member still identifies the component. This guard favors gaps over wrong links.
    const locals = new Set();
    for (const pattern of [/\blet-([\w$]+)/g, /#([\w$]+)/g, /\b(?:let|as)\s+([\w$]+)/g, /@for\s*\(\s*([\w$]+)/g]) {
      for (const local of template.matchAll(pattern)) locals.add(local[1]);
    }
    for (const match of template.matchAll(/<formly-(form|field)\b([^>]*?)>/g)) {
      const name = 'formly-' + match[1], id = `${info.id}:host:${match.index}`;
      const line = template.slice(0, match.index).split('\n').length + (info.templateFile ? 0 : location(info.inline).line - 1);
      const item = { id, kind: 'form-host', name, file: info.templateFile ? relative(info.templateFile) : location(info.node).file, line, evidence: 'template-candidate' };
      nodes.push(item); byId.set(id, item); edge(info.id, 'renders', id);
      const binding = /\[(fields|field)\]\s*=\s*(["'])(.*?)\2/.exec(match[2]);
      if (!binding) { issue(item.file, 'missing-or-unsupported-fields-binding'); continue; }
      const expression = binding[3].trim();
      const direct = /^(?:this\.)?([\w$]+)$/.exec(expression);
      const member = direct || /^(?:this\.)?([\w$]+)\s*(?:\(\s*\)|\|\s*async)$/.exec(expression);
      if (member && !binding[3].trim().startsWith('this.') && locals.has(member[1])) {
        issue(item.file, 'template-local-binding-needs-review', member[1]); continue;
      }
      const declared = member && info.node.members.find(m => nameOf(m.name) === member[1]);
      if (declared) {
        edge(id, direct ? 'binds-fields' : 'binds-fields-source', astIds.get(declared), direct ? 'static-source' : 'runtime-value-unresolved');
        if (!direct) issue(item.file, 'template-value-needs-review', expression);
      } else issue(item.file, member ? 'template-member-unresolved' : 'complex-template-binding');
    }
    for (const other of classInfo) if (other.selector && /^[a-z][\w-]*$/.test(other.selector) && new RegExp('<' + other.selector + '(?=[\\s>])').test(template)) edge(info.id, 'component-selector-candidate', other.id, 'template-scope-unresolved');
  }
  return { mode: 'typescript-static', typescript_version: ts.version, nodes, edges, unresolved, limitations: [
    'Static declarations and reference graph; no application execution, Angular compilation or browser observation.',
    'Separate TypeScript config contexts; build file replacements and injector reachability are not simulated. Angular template bindings use a limited recognizer; inherited members, inputs, pipes and complex expressions need review.',
    'Registration names are candidates across indexed scopes; injector precedence, module reachability and overrides are not resolved.',
    'Computed names, service/backend schemas, factory return values, template control flow and runtime mutation require source or runtime review.',
    'Files and declarations include non-Formly context; structural field/route matches require classification.'
  ] };
}

function run(input, ts) {
  if (!/^[56]\./.test(ts.version)) throw new Error('Supported compiler API majors: 5 and 6; tested with 5.9.3.');
  const root = path.resolve(input.root), contents = new Map();
  for (const rel of input.files) {
    const file = path.resolve(root, rel);
    if (!file.startsWith(root + path.sep) || fs.realpathSync(file) !== file) throw new Error('Unsafe source path');
    const data = fs.readFileSync(file);
    if (input.hashes && hash(data) !== input.hashes[rel]) throw new Error('Source changed during scan: ' + rel);
    contents.set(file, data.toString('utf8'));
  }
  const workspace = discover(input, ts, contents), covered = new Set(), results = [];
  function visit(context) {
    const result = analyze(input, ts, workspace, context), prefix = encodeURIComponent(context.id) + '::';
    for (const node of result.nodes) {
      covered.add(path.resolve(root, node.file)); node.id = prefix + node.id;
      if (node.scope) node.scope = prefix + node.scope;
      node.context = context.id; node.projects = workspace.owners(path.resolve(root, node.file));
    }
    for (const edge of result.edges) { edge.from = prefix + edge.from; edge.to = prefix + edge.to; edge.context = context.id; }
    for (const issue of result.unresolved) issue.context = context.id;
    results.push(result);
  }
  for (const context of workspace.contexts) visit(context);
  // Preserve inventory of source excluded from compilation, but label it and keep
  // it out of configured contexts. Never silently borrow another app's aliases.
  const orphans = new Map();
  for (const file of contents.keys()) {
    if (!source(file) || covered.has(file)) continue;
    const owners = workspace.owners(file);
    if (input.settings?.projects && !owners.some(p => input.settings.projects.includes(p))) continue;
    const key = owners.join(',') || '(unowned)';
    if (!orphans.has(key)) orphans.set(key, []);
    orphans.get(key).push(file);
  }
  for (const [owner, rootNames] of orphans) {
    const context = {id: 'unconfigured:' + owner, projects: owner === '(unowned)' ? [] : owner.split(','), rootNames,
      options: {}, references: [], evidence: 'unconfigured-source-candidate'};
    workspace.contexts.push(context); visit(context);
    workspace.unresolved.push({reason: 'source-outside-configured-program', context: context.id, count: rootNames.length});
  }
  return {mode: 'typescript-static', typescript_version: ts.version,
    nodes: results.flatMap(r => r.nodes), edges: results.flatMap(r => r.edges),
    unresolved: [...workspace.unresolved, ...results.flatMap(r => r.unresolved)],
    limitations: [...new Set(results.flatMap(r => r.limitations))],
    workspace: workspace.workspace,
    contexts: workspace.contexts.map(({options, rootNames, ...context}) => ({...context, rootFiles: rootNames.map(f => path.relative(root, f).split(path.sep).join('/'))})),
    resolution_inputs: workspace.resolutionInputs};
}
try {
  const input = JSON.parse(fs.readFileSync(0, 'utf8'));
  const ts = require(path.resolve(process.argv[2]));
  process.stdout.write(JSON.stringify(run(input, ts)));
} catch (error) { process.stderr.write(error.message + '\n'); process.exitCode = 1; }
