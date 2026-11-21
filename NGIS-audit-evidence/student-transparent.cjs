const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const { chromium } = require(process.argv[2]);
const root = path.resolve(__dirname, '..');
const origin = 'http://ngis-audit.local';
const mime = {'.html':'text/html; charset=utf-8','.css':'text/css','.js':'application/javascript','.svg':'image/svg+xml','.json':'application/json','.png':'image/png','.jpg':'image/jpeg'};
(async () => {
  const browser = await chromium.launch({executablePath:process.argv[3]});
  try {
    const page = await browser.newPage({viewport:{width:1440,height:900}});
    await page.route('**/*', async route => {
      const u = new URL(route.request().url());
      if (u.hostname === 'cdn.tailwindcss.com') return route.fulfill({contentType:'application/javascript',body:'window.tailwind={};'});
      if (u.origin !== origin) return route.abort();
      if (u.pathname.startsWith('/api/')) return route.fulfill({json:{success:true,data:[]}});
      const file = path.join(root,decodeURIComponent(u.pathname));
      if (!file.startsWith(root+path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile()) return route.fulfill({status:404,body:''});
      return route.fulfill({path:file,contentType:mime[path.extname(file)]});
    });
    const results = [];
    for (const width of [320,375,768,991,1024,1440,1920]) {
      await page.setViewportSize({width,height:900});
      await page.goto(origin+'/pages/student/student.html',{waitUntil:'domcontentloaded'});
      const bar = page.locator('.student-dashboard-hero .hero-topbar');
      await bar.waitFor();
      await page.waitForTimeout(300);
      const row = await bar.evaluate(el => {
        const rect=el.getBoundingClientRect(), logo=el.querySelector('.htb-brand-wrap').getBoundingClientRect(), controls=el.querySelector('.htb-right-controls').getBoundingClientRect();
        return {width:innerWidth,background:getComputedStyle(el).backgroundColor,hero:getComputedStyle(el.parentElement).backgroundColor,overflow:Math.max(0,document.documentElement.scrollWidth-innerWidth),controlsFit:controls.right<=rect.right+1,brandFits:logo.right<=controls.left+1,navbarCount:document.querySelectorAll('#ngisGlobalNavbar').length};
      });
      assert.equal(row.background,'rgba(0, 0, 0, 0)');
      assert.equal(row.hero,'rgba(0, 0, 0, 0)');
      assert.equal(row.overflow,0);
      assert.ok(row.controlsFit && row.brandFits, JSON.stringify(row));
      assert.equal(row.navbarCount,0);
      await page.keyboard.press('Control+k');
      assert.equal(await page.locator('#htbSearchInput').evaluate(e=>document.activeElement===e),true);
      if(width<=1024) {
        const menu=page.locator('#htbHamburger');
        await menu.click();
        await page.waitForTimeout(120);
        row.menuOpened=await page.locator('body').evaluate(el=>el.classList.contains('sidebar-open'));
        assert.ok(row.menuOpened,JSON.stringify(row));
        await page.keyboard.press('Escape');
        await page.waitForFunction(()=>!document.body.classList.contains('sidebar-open'));
        await page.waitForTimeout(250);
      }
      assert.equal(await page.locator('.htb-chip-avatar').evaluate(img=>img.complete && img.naturalWidth>0),true);
      await page.locator('#htbProfile').click();
      assert.equal(await page.locator('#htbProfile').getAttribute('aria-expanded'),'true');
      await page.keyboard.press('Escape');
      assert.equal(await page.locator('#htbProfile').getAttribute('aria-expanded'),'false');
      await page.evaluate(()=>document.documentElement.dataset.theme='dark');
      assert.equal(await bar.evaluate(el=>getComputedStyle(el).backgroundColor),'rgba(0, 0, 0, 0)');
      await page.evaluate(()=>document.documentElement.dataset.theme='light');
      results.push(row);
      if([375,768,1440].includes(width)) await page.locator('.student-dashboard-hero').screenshot({path:path.join(__dirname,'student-transparent-'+width+'.png')});
    }
    fs.writeFileSync(path.join(__dirname,'student-transparent-results.json'),JSON.stringify(results,null,2));
    console.log(results.length+' Student header viewport checks passed');
  } finally { await browser.close(); }
})().catch(e=>{console.error(e);process.exitCode=1});

