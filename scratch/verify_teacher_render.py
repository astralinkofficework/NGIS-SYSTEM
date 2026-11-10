import asyncio
import json
from playwright.async_api import async_playwright

PAGES = {
    'services': 'http://127.0.0.1:3000/pages/teacher/teacher-services.html',
    'lostfound': 'http://127.0.0.1:3000/pages/teacher/teacher-lost-found.html',
}

async def check(page, name, url, errors_by_page):
    await page.goto(url, wait_until='networkidle')
    await page.wait_for_timeout(800)
    info = await page.evaluate("""() => {
      const hero = document.getElementById('heroBanner');
      const sidebar = document.querySelector('aside, .sidebar, [data-sidebar]');
      const ham = document.querySelector('[data-action="toggle-sidebar"]');
      return {
        heroPopulated: !!hero && hero.children.length > 0,
        heroHiddenClass: hero ? hero.className : null,
        sidebarInjected: !!sidebar,
        statCards: document.querySelectorAll('.filter-stat-card').length,
        navPills: document.querySelectorAll('.nav-tab-btn').length,
        catPills: document.querySelectorAll('.cat-pill').length,
        cardsRendered: document.querySelectorAll('.req-card, .item-card').length,
        fab: !!document.getElementById('fabNewRequestBtn'),
        boldUsed: [...document.querySelectorAll('*')].some(el => {
          const w = getComputedStyle(el).fontWeight;
          return (w === '700' || w === '800' || w === '900') && el.innerText && el.innerText.trim().length > 0;
        }),
      };
    }""")
    print(name, 'desktop =>', json.dumps(info))
    await page.screenshot(path=f'scratch/tv_{name}_desktop.png', full_page=False)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        page_errors = []
        page.on('pageerror', lambda e: page_errors.append(str(e)))
        console_errors = []
        page.on('console', lambda m: console_errors.append(m.text) if m.type == 'error' else None)
        for name, url in PAGES.items():
            await check(page, name, url, None)
        # mobile: hamburger presence
        await page.set_viewport_size({'width': 390, 'height': 844})
        for name, url in PAGES.items():
            await page.goto(url, wait_until='networkidle')
            ham = await page.evaluate("""() => {
              const h = document.querySelector('[data-action="toggle-sidebar"]');
              if (!h) return null;
              const r = h.getBoundingClientRect();
              return {visible: r.width >= 38 && r.height >= 38 && getComputedStyle(h).display !== 'none', w: r.width, h: r.height};
            }""")
            print(name, 'mobile hamburger =>', json.dumps(ham))
            await page.screenshot(path=f'scratch/tv_{name}_mobile.png')
        print('page errors:', page_errors or 'NONE')
        print('console errors:', console_errors[:8] or 'NONE')
        await browser.close()

asyncio.run(main())
