#!/usr/bin/env node
'use strict';
// Optional real-tool qualification. Supplied tools are trusted; all Nx plugin
// execution is confined to our generated temporary fixtures, never a user's app.
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {execFileSync} = require('node:child_process');
const assert = require('node:assert/strict');
const {parseArgs} = require('node:util');
const {values} = parseArgs({options: {'nx-package': {type:'string'}, 'angular-core': {type:'string'}}});
if (!values['nx-package'] || !values['angular-core']) throw new Error('Pass --nx-package /path/to/nx/package.json --angular-core /path/to/@angular-devkit/core');
const nxPackage = path.resolve(values['nx-package']), nx = require(nxPackage);
const angularPath = path.resolve(values['angular-core']), angular = require(angularPath);
const repo = path.resolve(__dirname, '..'), cli = path.join(repo, 'skill/ask-formly/scripts/project_index.py');
const compiler = process.env.FORMLY_TEST_TYPESCRIPT || path.join(repo, 'node_modules/typescript/lib/typescript.js');
const temporary = fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), 'ask-formly-workspaces-')));
const results = [];
function put(root, name, content) {
  const file = path.join(root,name);fs.mkdirSync(path.dirname(file),{recursive:true});fs.writeFileSync(file, typeof content === 'string' ? content : JSON.stringify(content,null,2));
}
function scan(root, args=[]) {
  const output=JSON.parse(execFileSync('python3',[cli,'scan','--root',root,'--typescript',compiler,...args],{encoding:'utf8',timeout:120000}));
  assert.equal(output.graph_mode,'typescript-static');
  return JSON.parse(fs.readFileSync(path.join(root,'.agents/ask-formly/graph.json'),'utf8'));
}
function fixture(root, app, lib) {
  put(root,'tsconfig.base.json',{compilerOptions:{baseUrl:'.',paths:{'@acme/forms':[lib+'/src/index.ts']}}});
  put(root,app+'/tsconfig.app.json',{extends:(app==='.'?'./':'')+path.posix.relative(app,'tsconfig.base.json'),include:['src/*.ts']});
  put(root,lib+'/tsconfig.lib.json',{extends:path.posix.relative(lib,'tsconfig.base.json'),include:['src/*.ts']});
  put(root,lib+'/src/index.ts',"export const fields=[{key:'customer',type:'input'}];");
  put(root,app+'/src/app.ts',"import { Component } from '@angular/core'; import { fields } from '@acme/forms'; @Component({selector:'app-root',template:'<formly-form [fields]=\"fields\" />'}) export class AdminComponent { fields = fields; }");
  return {
    admin:{root:app,sourceRoot:app+'/src',projectType:'application',architect:{build:{builder:'@angular/build:application',options:{tsConfig:app+'/tsconfig.app.json'}}}},
    forms:{root:lib,sourceRoot:lib+'/src',projectType:'library',architect:{build:{builder:'@angular/build:ng-packagr',options:{tsConfig:lib+'/tsconfig.lib.json'}}}}
  };
}
function verify(graph, app, lib) {
  const nodes=new Map(graph.nodes.map(n=>[n.id,n]));
  assert.ok(graph.edges.some(e=>e.relation==='imports' && nodes.get(e.from).file===(app?app+'/':'')+'src/app.ts' && nodes.get(e.to).file===lib+'/src/index.ts'));
  assert.ok(graph.edges.some(e=>e.relation==='binds-fields'));
  assert.ok(graph.nodes.some(n=>n.kind==='field-config' && n.name==='customer'));
  assert.ok(!graph.unresolved.some(i=>i.reason==='tsconfig-error'));
}
(async()=>{
  try {
    for (const multiple of [false,true]) {
      const name=multiple?'angular-multi':'angular-single', root=path.join(temporary,name);
      const app=multiple?'products/admin':'.',lib=multiple?'shared/forms':'forms';
      const projects=fixture(root,app,lib);
      if (!multiple) { projects.admin.root=''; delete projects.forms; }
      put(root,'angular.json',{version:1,projects});
      const host={readFile: async file=>fs.readFileSync(file,'utf8'),writeFile:async()=>{throw new Error('read-only');},isFile:async file=>{try{return fs.statSync(file).isFile();}catch{return false;}},isDirectory:async file=>{try{return fs.statSync(file).isDirectory();}catch{return false;}}};
      const official=(await angular.workspaces.readWorkspace(path.join(root,'angular.json'),host)).workspace;
      const graph=scan(root);
      assert.deepEqual(graph.workspace.projects.map(p=>p.name).sort(),[...official.projects.keys()].sort());
      verify(graph,app==='.'?'':app,lib); // normalized paths are checked below for the root app
      results.push({case:name,projects:graph.workspace.projects.length,contexts:graph.contexts.length,status:'pass'});
    }
    for (const packages of [false,true]) {
      const name=packages?'nx-packages':'nx-integrated',root=path.join(temporary,name);
      const app=packages?'packages/admin':'products/admin',lib=packages?'packages/forms':'shared/forms';
      const projects=fixture(root,app,lib);
      put(root,'package.json',{name:'qualification',private:true,...(packages?{workspaces:['packages/*','!packages/ignored']}:{}),devDependencies:{nx:nx.version}});
      put(root,'nx.json',{plugins:['./tools/inferred.cjs'],targetDefaults:{build:{cache:true}}});
      put(root,'tools/inferred.cjs',`const path=require('node:path'); exports.createNodesV2=['**/formly-project.json',async files=>files.map(file=>{const root=path.dirname(file);return [file,{projects:{[root]:{name:'inferred',root,targets:{build:{executor:'nx:run-commands',options:{command:'echo fixture',tsConfig:root+'/compile.json'}}}}}}];})];`);
      put(root,'extras/inferred/formly-project.json',{});put(root,'extras/inferred/compile.json',{include:['*.ts']});put(root,'extras/inferred/form.ts',"export const fields=[{key:'inferred',type:'input'}];");
      for (const [key,project] of Object.entries(projects)) {
        const {architect,...data}=project;data.targets=Object.fromEntries(Object.entries(architect).map(([target,{builder,...options}])=>[target,{executor:builder,...options}]));
        if (packages) put(root,project.root+'/package.json',{name:'@acme/'+key,version:'1.0.0',nx:data,...(key==='admin'?{dependencies:{'@acme/forms':'*'}}:{})});
        else put(root,project.root+'/project.json',{name:key,...data});
      }
      if (packages) { put(root,'packages/ignored/package.json',{name:'@acme/ignored',version:'1.0.0'});put(root,'pnpm-workspace.yaml',"packages:\n  - 'packages/*'\n  - '!packages/ignored'\n"); }
      fs.symlinkSync(path.dirname(path.dirname(nxPackage)),path.join(root,'node_modules'),'dir');
      const cache=path.join(temporary,name+'-cache');fs.mkdirSync(cache);
      const env={...process.env,NX_DAEMON:'false',NX_ISOLATE_PLUGINS:'false',NX_INTERACTIVE:'false',NX_CACHE_PROJECT_GRAPH:'false',NX_CACHE_DIRECTORY:cache,NX_WORKSPACE_DATA_DIRECTORY:path.join(cache,'data'),NX_NATIVE_FILE_CACHE_DIRECTORY:path.join(cache,'native'),NODE_COMPILE_CACHE:path.join(cache,'compile')};
      const exportPath='.agents/ask-formly/nx-project-graph.json';fs.mkdirSync(path.join(root,'.agents/ask-formly'),{recursive:true});
      execFileSync(process.execPath,[path.resolve(path.dirname(nxPackage),nx.bin.nx),'graph','--file='+exportPath],{cwd:root,env,encoding:'utf8',timeout:120000,stdio:['ignore','pipe','pipe']});
      const official=JSON.parse(fs.readFileSync(path.join(root,exportPath),'utf8')).graph;
      const all=scan(root,['--nx-graph',exportPath]);
      assert.ok(all.contexts.some(c=>c.config==='extras/inferred/compile.json'));
      assert.ok(all.nodes.some(n=>n.kind==='field-config' && n.name==='inferred'));
      const selected=packages?'@acme/admin':'admin',graph=scan(root,['--nx-graph',exportPath,'--project',selected]);
      assert.deepEqual(graph.workspace.projects.map(p=>p.name).sort(),Object.keys(official.nodes).sort());
      assert.ok(graph.workspace.projects.some(p=>p.name==='inferred'));
      assert.ok(!graph.workspace.projects.some(p=>p.name==='@acme/ignored'));
      verify(graph,app,lib);
      assert.ok(graph.workspace.projects.find(p=>p.name===selected).targets.build.cache);
      results.push({case:name,projects:graph.workspace.projects.length,contexts:graph.contexts.length,status:'pass'});
    }
    console.log(JSON.stringify({versions:{nx:nx.version,angular_devkit:require(path.join(angularPath,'package.json')).version,typescript:require(compiler).version,node:process.version},results},null,2));
  } finally {fs.rmSync(temporary,{recursive:true,force:true});}
})().catch(error=>{console.error(error.stack, error.stderr?.toString() || '');process.exitCode=1;});
