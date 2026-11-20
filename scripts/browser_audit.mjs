import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import {spawnSync} from 'node:child_process';
const root=path.resolve(import.meta.dirname,'../research');
const require=createRequire(path.join(root,'tools/package.json'));
const {chromium}=require('playwright-core');
const mime={'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.png':'image/png','.woff':'font/woff','.woff2':'font/woff2','.json':'application/json'};
const server=http.createServer((req,res)=>{
 let file=path.resolve(root,'output','.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));
 if(!file.startsWith(path.join(root,'output')+path.sep)){res.writeHead(403);res.end();return;}
 if(fs.existsSync(file)&&fs.statSync(file).isDirectory())file=path.join(file,'index.html');
 if(!fs.existsSync(file)){res.writeHead(404);res.end();return;}
 res.setHeader('Content-Type',mime[path.extname(file)]||'application/octet-stream');fs.createReadStream(file).pipe(res);
});
await new Promise(r=>server.listen(8765,'127.0.0.1',r));
const result={}; fs.mkdirSync(path.join(root,'screenshots'),{recursive:true});
const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
try{
for(const name of ['mkdocs','sphinx','pelican']){
 result[name]={};
 for(const [label,width,height]of [['desktop',1440,1000],['mobile',390,844]]){
  const context=await browser.newContext({viewport:{width,height},deviceScaleFactor:1});
  const page=await context.newPage(); const requests=[],errors=[],responses=[],pending=[];
  page.on('request',r=>requests.push(r.url()));page.on('pageerror',e=>errors.push(String(e)));
  page.on('response',r=>pending.push((async()=>{let bytes=0;try{bytes=(await r.body()).length}catch{}responses.push({url:r.url(),status:r.status(),bytes})})()));
  await page.goto(`http://127.0.0.1:8765/${name}/index.html`,{waitUntil:'networkidle'});
  await page.waitForFunction(()=>document.querySelector('mjx-container')&&document.querySelector('.js-plotly-plot'),{timeout:30000});
  await page.screenshot({path:path.join(root,'screenshots',`${name}-${label}.png`),fullPage:true});
  const checks=await page.evaluate(()=>({width:innerWidth,documentWidth:document.documentElement.scrollWidth,math:document.querySelectorAll('mjx-container').length,mathErrors:[...document.querySelectorAll('[data-mjx-error]')].map(x=>x.textContent),plot:!!document.querySelector('.js-plotly-plot'),rowspan:!!document.querySelector('[rowspan="2"]'),colspan:!!document.querySelector('[colspan="2"]'),columns:getComputedStyle(document.querySelector('.experiment-columns')).gridTemplateColumns,footnotes:!!document.querySelector('.footnote,.footnote-reference,[role="doc-noteref"]'),brokenImages:[...document.images].filter(x=>!x.complete||!x.naturalWidth).map(x=>x.src)}));
  await Promise.all(pending);
  result[name][label]={checks,requests:requests.length,external_requests:requests.filter(u=>new URL(u).hostname!=='127.0.0.1').length,resource_bytes:responses.reduce((s,r)=>s+r.bytes,0),responses,errors};
  await context.close();
 }
}
await browser.close();
// Async child process keeps the local HTTP server serving Lighthouse requests.
const {spawn}=await import('node:child_process');
for(const name of Object.keys(result)){
 const args=[path.join(root,'tools/node_modules/lighthouse/cli/index.js'),`http://127.0.0.1:8765/${name}/index.html`,'--chrome-path=C:/Program Files/Google/Chrome/Application/chrome.exe','--chrome-flags=--headless','--output=json',`--output-path=${root}/${name}/lighthouse.json`,'--quiet'];
 await new Promise(resolve=>{const child=spawn('node',args);let log='';child.stdout.on('data',b=>log+=b);child.stderr.on('data',b=>log+=b);child.on('close',code=>{fs.writeFileSync(path.join(root,name,'lighthouse.log'),log);if(code===0){const data=JSON.parse(fs.readFileSync(path.join(root,name,'lighthouse.json')));result[name].lighthouse=Object.fromEntries(Object.entries(data.categories).map(([k,v])=>[k,v.score]));}else result[name].lighthouse={error:log};resolve();});});
}
}finally{fs.writeFileSync(path.join(root,'browser-metrics.json'),JSON.stringify(result,null,2));await browser.close();server.close();}
console.log('Browser metrics and screenshots saved');
