const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {execFileSync}=require('node:child_process');
const {chromium}=require(process.argv[2]);
const root=path.resolve(__dirname,'..');
const base='http://ngis-audit.local';
const css=['design-tokens','app','shared-components','design-system','khmer-suite','mobile-header','navbar','ngis-components','smart-disclosure','ui-states','ui-cleanup'];
const selectors=['.smx-kpi-icon','.ks-kpi-icon','.ngis-notif-icon-wrap','.ngis-notif-item-icon','.smart-accordion-icon','.ngis-state-icon','.mob-bn-icon-wrap','.ngis-icon-slot'];
const representatives=['admin/admin','principal/principal','teacher/teacher','student/student','shared/departments'];
const affected=fs.readdirSync(path.join(root,'pages'),{withFileTypes:true}).filter(x=>x.isDirectory()).flatMap(({name})=>fs.readdirSync(path.join(root,'pages',name)).filter(f=>f.endsWith('.html')&&fs.readFileSync(path.join(root,'pages',name,f),'utf8').includes('ngis-icon-slot')).map(f=>name+'/'+f.slice(0,-5)));
const pages=[...new Set([...representatives,...affected])];
const baseline=new Map(css.map(name=>{const file='assets/css/'+name+'.css';return [file,execFileSync('git',['show','HEAD:'+file],{cwd:root})];}));
const mime={'.html':'text/html','.js':'application/javascript','.css':'text/css','.svg':'image/svg+xml','.json':'application/json'};
(async()=>{
 const browser=await chromium.launch({executablePath:process.argv[3],timeout:10000});
 try {
 const page=await browser.newPage({viewport:{width:768,height:860}});
 const fixture='<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width">'+css.map(x=>'<link rel="stylesheet" href="/assets/css/'+x+'.css">').join('')+
 '<main style="padding:32px 20px 32px 325px"><h1>Shared NGIS icon surfaces</h1>'+selectors.map((s,i)=>'<p><span class="'+(s==='.ks-kpi-icon'?'ks-kpi':'')+'"><span class="'+s.slice(1)+'">◆</span></span> '+s.slice(1)+'</p>').join('')+
 '<aside id="sidebar" class="sidebar" style="position:static"><a href="#current" class="nav-link nav-sub-link active" aria-current="page"><span class="nav-link-icon">◆</span><span class="nav-link-label">Current page</span></a></aside></main>';
 await page.route('**/*',async route=>{
  const u=new URL(route.request().url());
  if(u.hostname==='ngis-before.local'){
   if(u.pathname==='/fixture')return route.fulfill({contentType:'text/html',body:fixture});
   const original=baseline.get(u.pathname.slice(1));
   if(original)return route.fulfill({contentType:'text/css',body:original});
  }
  if(u.origin!==base) return route.abort();
  if(u.pathname==='/fixture') return route.fulfill({contentType:'text/html',body:fixture});
  if(u.pathname.startsWith('/api/')) return route.fulfill({json:{data:[],success:true}});
  const file=path.join(root,u.pathname);
  if(!file.startsWith(root+path.sep)||!fs.existsSync(file)||!fs.statSync(file).isFile())return route.fulfill({status:404,body:''});
  return route.fulfill({path:file,contentType:mime[path.extname(file)]});
 });
 const read=async selector=>page.locator(selector).first().evaluate(e=>{const c=getComputedStyle(e);return {background:c.backgroundColor,image:c.backgroundImage,color:c.color,outline:c.outlineStyle,width:c.outlineWidth}});
 await page.goto('http://ngis-before.local/fixture',{waitUntil:'load'});
 await page.screenshot({path:path.join(__dirname,'icon-components-git-baseline.png')});
 await page.goto(base+'/fixture',{waitUntil:'load'});
 await page.screenshot({path:path.join(__dirname,'icon-components-refined-light.png')});
 const styles={};
 for(const theme of ['light','dark']){
   await page.evaluate(theme=>document.documentElement.dataset.theme=theme,theme);
   styles[theme]={};
   for(const selector of selectors) {
     const style=await read(selector);
     styles[theme][selector]=style;
     assert.equal(style.background,'rgba(0, 0, 0, 0)',selector);
     assert.equal(style.image,'none',selector);
   }
 }
 await page.keyboard.press('Tab');
 styles.focus=await read('#sidebar .nav-link');
 assert.equal(styles.focus.outline,'solid');
 await page.locator('#sidebar .nav-link').hover();
 styles.hover=await read('#sidebar .nav-link');
 assert.equal(styles.hover.outline,'solid');
 assert.equal(styles.hover.background,'rgba(0, 0, 0, 0)');
 await page.screenshot({path:path.join(__dirname,'icon-components-verified.png')});
 const results=[];
 for(const width of [1440,768,375]){
   await page.setViewportSize({width,height:860});
   for(const route of pages){
      const response=await page.goto(base+'/pages/'+route+'.html',{waitUntil:'domcontentloaded',timeout:10000});
      const sample=await page.locator('.ngis-icon-slot,.ql-icon-wrap,.ngis-dept-row-icon').evaluateAll(els=>els.map(e=>({class:e.className,background:getComputedStyle(e).backgroundColor, rules:[...document.styleSheets].flatMap(sheet=>{try{return [...sheet.cssRules].filter(r=>r.selectorText&&r.style.backgroundColor&&e.matches(r.selectorText)).map(r=>[sheet.href,r.selectorText,r.style.backgroundColor])}catch{return []}})})));
      const screenshot=representatives.includes(route)?'icon-'+route.split('/')[0]+'-'+width+'-verified.png':null;
      if(screenshot) await page.screenshot({path:path.join(__dirname,screenshot),timeout:10000});
      results.push({route,width,status:response.status(),title:await page.title(),sample,screenshot});
      assert.equal(response.status(),200);

   }
 }
 fs.writeFileSync(path.join(__dirname,'icon-browser-verification.json'),JSON.stringify({styles,results},null,2));
 const failures=results.flatMap(r=>r.sample.filter(x=>x.background!=='rgba(0, 0, 0, 0)').map(x=>[r.route,r.width,x]));
 assert.equal(failures.length,0,JSON.stringify(failures.slice(0,20)));
 console.log(results.length+' portal viewport checks and shared fixture assertions passed');
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});



