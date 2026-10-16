#!/usr/bin/env node
'use strict';
// Static compiler API only. Never load application modules or evaluate factories.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');

function analyze(input, ts) {
  if (!/^[56]\./.test(ts.version)) throw new Error('Supported compiler API majors: 5 and 6; tested with 5.9.3.');
  const root = path.resolve(input.root);
  const contents = new Map();
  for (const rel of input.files) {
    const absolute = path.resolve(root, rel);
    if (!absolute.startsWith(root + path.sep) || fs.realpathSync(absolute) !== absolute) throw new Error('Unsafe source path');
    const data = fs.readFileSync(absolute);
    if (input.hashes && crypto.createHash('sha256').update(data).digest('hex') !== input.hashes[rel]) throw new Error('Source changed during scan: ' + rel);
    contents.set(absolute, data.toString('utf8'));
  }
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
    const id = `${loc.file}:${typeof node === 'string' ? 0 : node.getStart()}:${kind}${kind === 'registration' ? ':' + extra.scope : ''}`;
    if (!byId.has(id)) { const value = { id, kind, name, ...loc, ...extra }; byId.set(id, value); nodes.push(value); }
    return id;
  }
  function edge(from, relation, to, evidence = 'static-source') {
    if (!from || !to || from === to) return;
    const key = JSON.stringify([from, relation, to, evidence]);
    if (!edgeKeys.has(key)) { edgeKeys.add(key); edges.push({ from, relation, to, evidence }); }
  }
  const options = { noLib: true, noEmit: true, allowJs: true, experimentalDecorators: true, target: ts.ScriptTarget.Latest, module: ts.ModuleKind.ESNext, moduleResolution: ts.ModuleResolutionKind.Node10 };
  // Only indexed configuration files can be read; external extends remain explicit gaps.
  function config(file, seen = new Set()) {
    if (seen.has(file)) { issue(relative(file), 'tsconfig-cycle'); return {}; }
    seen.add(file);
    const text = contents.get(file);
    if (text === undefined) { issue(relative(file), 'tsconfig-outside-index'); return {}; }
    const parsed = ts.parseConfigFileTextToJson(file, text);
    if (parsed.error) { issue(relative(file), 'tsconfig-parse-error'); return {}; }
    const doc = parsed.config; let inherited = {};
    for (const base of doc.extends ? (Array.isArray(doc.extends) ? doc.extends : [doc.extends]) : []) {
      if (typeof base !== 'string' || !base.startsWith('.')) { issue(relative(file), 'external-tsconfig-extends'); continue; }
      const target = path.resolve(path.dirname(file), base.endsWith('.json') ? base : base + '.json');
      inherited = { ...inherited, ...config(target, new Set(seen)) };
    }
    const converted = ts.convertCompilerOptionsFromJson(doc.compilerOptions || {}, path.dirname(file));
    if (converted.errors.length) issue(relative(file), 'tsconfig-option-errors');
    return { ...inherited, ...converted.options };
  }
  const rootConfig = ['tsconfig.json', 'tsconfig.base.json'].map(f => path.join(root, f)).find(f => contents.has(f));
  if (rootConfig) Object.assign(options, config(rootConfig));
  Object.assign(options, { noLib: true, noEmit: true, allowJs: true });
  for (const file of contents.keys()) if (/[/\\]tsconfig[^/\\]*\.json$/.test(file) && path.dirname(file) !== root) issue(relative(file), 'nested-tsconfig-not-selected', 'Root compiler options only; inspect project-specific aliases.');
  const host = ts.createCompilerHost(options);
  host.readFile = file => contents.get(path.resolve(file));
  host.fileExists = file => contents.has(path.resolve(file));
  host.directoryExists = dir => [...contents.keys()].some(f => f.startsWith(path.resolve(dir) + path.sep));
  host.getDirectories = () => [];
  host.getCurrentDirectory = () => root;
  host.realpath = file => path.resolve(file);
  host.getSourceFile = (file, languageVersion) => contents.has(path.resolve(file)) ? ts.createSourceFile(path.resolve(file), contents.get(path.resolve(file)), languageVersion, true) : undefined;
  host.writeFile = () => { throw new Error('No emit allowed'); };
  const sourceNames = [...contents.keys()].filter(f => /\.[cm]?[jt]sx?$/.test(f));
  const program = ts.createProgram(sourceNames, options, host), checker = program.getTypeChecker();
  const sources = program.getSourceFiles().filter(sf => contents.has(sf.fileName));
  const fileIds = new Map([...contents.keys()].map(f => [f, add('file', relative(f), relative(f))]));
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
  const classInfo = [], registry = [], fields = [];
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
      if (ts.isObjectLiteralExpression(node) && (value(node, 'type') || value(node, 'fieldGroup') || value(node, 'fieldArray') || value(node, 'key') && ['validators', 'asyncValidators'].some(k => value(node, k)))) {
        const id = add('field-config', literal(value(node, 'key')) || (value(node, 'key') ? '(computed key)' : value(node, 'type') ? '(keyless type)' : '(unkeyed group)'), node, { evidence: 'structural-candidate' });
        edge(owner(node.parent), 'contains-field', id); astIds.set(node, id); fields.push(node);
      }
    });
  }
  function moduleTarget(sf, specifier) {
    return ts.resolveModuleName(specifier, sf.fileName, options, host).resolvedModule?.resolvedFileName;
  }
  function importedName(sf, local, module) {
    for (const stmt of sf.statements) {
      if (!ts.isImportDeclaration(stmt) || literal(stmt.moduleSpecifier) !== module) continue;
      const bindings = stmt.importClause?.namedBindings;
      if (bindings && ts.isNamedImports(bindings)) for (const e of bindings.elements) if (e.name.text === local) return (e.propertyName || e.name).text;
    }
    return undefined;
  }
  function objects(expression, context, reason, seen = new Set()) {
    const resolved = resolve(expression);
    if (seen.has(resolved)) { issue(context, 'cyclic-static-array'); return []; }
    seen = new Set(seen); seen.add(resolved);
    if (resolved && ts.isArrayLiteralExpression(resolved)) return resolved.elements.flatMap(e => ts.isSpreadElement(e) ? objects(e.expression, context, reason, seen) : objects(e, context, reason, seen));
    if (resolved && ts.isObjectLiteralExpression(resolved)) return [resolved];
    issue(context, reason); return [];
  }
  function configProperties(expression, seen = new Set()) {
    const resolved = resolve(expression);
    if (!resolved || !ts.isObjectLiteralExpression(resolved)) { issue(expression, 'dynamic-registration-config'); return undefined; }
    if (seen.has(resolved)) { issue(expression, 'cyclic-registration-config'); return undefined; }
    seen = new Set(seen); seen.add(resolved);
    const properties = new Map();
    for (const p of resolved.properties) {
      if (ts.isSpreadAssignment(p)) {
        const spread = configProperties(p.expression, seen);
        if (!spread) return undefined; // Unknown spread can override any category.
        for (const [key, val] of spread) properties.set(key, val);
      } else {
        const key = nameOf(p.name);
        if (!key) { issue(p, 'computed-registration-property'); return undefined; }
        properties.set(key, p.initializer || (ts.isShorthandPropertyAssignment(p) ? p.name : undefined));
      }
    }
    return properties;
  }
  function registration(entry, expression) {
    const objs = objects(expression, expression, 'dynamic-registration-config');
    for (const obj of objs) {
      const properties = configProperties(obj); if (!properties) continue;
      for (const category of ['types', 'wrappers', 'validators', 'validationMessages', 'extensions', 'presets']) {
        const expr = properties.get(category); if (!expr) continue;
        for (const item of objects(expr, expr, 'dynamic-registration-list')) {
          const name = literal(value(item, 'name'));
          if (name === undefined) { issue(item, 'dynamic-registration-name'); continue; }
          const id = add('registration', name, item, { category, scope: entry }); registry.push({ id, name, category });
          edge(entry, 'registers', id);
          for (const key of ['component', 'validation', 'extension', 'message', 'fields']) {
            const impl = value(item, key); if (!impl) continue;
            const dest = target(impl);
            if (dest) edge(id, 'implementation', dest);
            else { const inline = add('inline-implementation', key, impl); edge(id, 'implementation', inline); edge(inline, 'defined-in', fileIds.get(impl.getSourceFile().fileName)); }
          }
          for (const key of ['extends', 'wrappers']) if (value(item, key)) issue(item, 'registration-inheritance-needs-review', key);
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
      if (node.expression.kind === ts.SyntaxKind.ImportKeyword) {
        const specifier = literal(node.arguments[0]), dest = specifier && moduleTarget(sf, specifier);
        if (dest) edge(owner(node), 'lazy-import', fileIds.get(dest)); else issue(node, 'dynamic-or-external-import');
      }
      if (ts.isPropertyAccessExpression(node.expression)) {
        const mode = node.expression.name.text, receiver = node.expression.expression;
        if (['forRoot', 'forChild'].includes(mode) && ts.isIdentifier(receiver) && importedName(sf, receiver.text, '@ngx-formly/core') === 'FormlyModule') {
          const id = add('entry-point', `FormlyModule.${mode}`, node, { registration_mode: mode }); edge(owner(node), 'configures', id);
          if (node.arguments[0]) registration(id, node.arguments[0]);
        }
      }
    }
    if (ts.isObjectLiteralExpression(node)) {
      const token = value(node, 'provide');
      if (token && ts.isIdentifier(token) && importedName(sf, token.text, '@ngx-formly/core') === 'FORMLY_CONFIG') {
        const id = add('entry-point', 'FORMLY_CONFIG', node, { registration_mode: 'provider' }); edge(owner(node), 'configures', id);
        const configValue = value(node, 'useValue'); if (configValue) registration(id, configValue); else issue(node, 'dynamic-provider-factory');
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
        if (!ts.isCallExpression(call) || !ts.isIdentifier(call.expression) || importedName(sf, call.expression.text, '@angular/core') !== 'Component') continue;
        const meta = resolve(call.arguments[0]); if (!meta || !ts.isObjectLiteralExpression(meta)) { issue(node, 'dynamic-component-metadata'); continue; }
        const url = literal(value(meta, 'templateUrl')), inline = value(meta, 'template');
        const templateFile = url && path.resolve(path.dirname(sf.fileName), url);
        const template = templateFile ? contents.get(templateFile) : literal(inline);
        classInfo.push({ node, id: astIds.get(node), selector: literal(value(meta, 'selector')), template, templateFile, inline });
        if (templateFile) { edge(astIds.get(node), 'template', fileIds.get(templateFile)); if (template === undefined) issue(node, 'template-outside-index'); }
      }
    }
  });
  function candidate(from, name, category, relation) {
    const matches = registry.filter(r => r.name === name && r.category === category);
    for (const r of matches) edge(from, relation, r.id, 'registration-scope-unresolved');
    if (!matches.length) issue(byId.get(from).file, 'registration-not-in-index', category + ':' + name);
  }
  for (const node of fields) {
    const id = astIds.get(node), type = value(node, 'type');
    if (type) { const name = literal(resolve(type)); if (name !== undefined) candidate(id, name, 'types', 'type-candidate'); else issue(type, 'dynamic-field-type'); }
    const wrappers = resolve(value(node, 'wrappers'));
    if (wrappers && ts.isArrayLiteralExpression(wrappers)) for (const item of wrappers.elements) { const name = literal(item); if (name) candidate(id, name, 'wrappers', 'wrapper-candidate'); else issue(item, 'dynamic-wrapper'); }
    for (const group of ['validators', 'asyncValidators']) {
      const validators = resolve(value(node, group)); if (!validators) continue;
      if (!ts.isObjectLiteralExpression(validators)) { issue(validators, 'dynamic-field-validators'); continue; }
      for (const p of validators.properties) {
        const name = nameOf(p.name), expr = p.initializer; if (!expr) continue;
        if (name === 'validation') {
          const list = resolve(expr);
          if (ts.isArrayLiteralExpression(list)) for (const item of list.elements) { const key = literal(item); if (key) candidate(id, key, 'validators', 'validator-candidate'); else edge(id, 'validator-function', target(item)); }
          else issue(expr, 'dynamic-validator-list');
        } else { const validator = add('inline-validator', name || '(computed)', p); edge(id, 'validates-with', validator); edge(validator, 'implementation', target(expr)); }
      }
    }
  }
  for (const info of classInfo) {
    if (info.template === undefined) continue;
    // Angular template parsing is deliberately conservative: simple member bindings only.
    const template = info.template.replace(/<!--[\s\S]*?-->/g, match => match.replace(/[^\n]/g, ' '));
    for (const match of template.matchAll(/<formly-(form|field)\b([^>]*?)>/g)) {
      const name = 'formly-' + match[1], id = `${info.id}:host:${match.index}`;
      const line = template.slice(0, match.index).split('\n').length + (info.templateFile ? 0 : location(info.inline).line - 1);
      const item = { id, kind: 'form-host', name, file: info.templateFile ? relative(info.templateFile) : location(info.node).file, line, evidence: 'template-candidate' };
      nodes.push(item); byId.set(id, item); edge(info.id, 'renders', id);
      const binding = /\[(fields|field)\]\s*=\s*(["'])(.*?)\2/.exec(match[2]);
      if (!binding) { issue(item.file, 'missing-or-unsupported-fields-binding'); continue; }
      const member = /^(?:this\.)?([\w$]+)$/.exec(binding[3].trim());
      const declared = member && info.node.members.find(m => nameOf(m.name) === member[1]);
      if (declared) edge(id, 'binds-fields', astIds.get(declared)); else issue(item.file, member ? 'template-member-unresolved' : 'complex-template-binding');
    }
    for (const other of classInfo) if (other.selector && /^[a-z][\w-]*$/.test(other.selector) && new RegExp('<' + other.selector + '(?=[\\s>])').test(template)) edge(info.id, 'component-selector-candidate', other.id, 'template-scope-unresolved');
  }
  return { mode: 'typescript-static', typescript_version: ts.version, nodes, edges, unresolved, limitations: [
    'Static declarations and reference graph; no application execution, Angular compilation or browser observation.',
    'Root tsconfig only. Angular template bindings use a limited recognizer; inherited members, inputs, pipes and complex expressions need review.',
    'Registration names are candidates across indexed scopes; injector precedence, module reachability and overrides are not resolved.',
    'Computed names, service/backend schemas, factory return values, template control flow and runtime mutation require source or runtime review.',
    'Files and declarations include non-Formly context; structural field/route matches require classification.'
  ] };
}

try {
  const input = JSON.parse(fs.readFileSync(0, 'utf8'));
  const ts = require(path.resolve(process.argv[2]));
  process.stdout.write(JSON.stringify(analyze(input, ts)));
} catch (error) { process.stderr.write(error.message + '\n'); process.exitCode = 1; }
