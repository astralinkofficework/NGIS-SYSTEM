import asyncio, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1440, 'height': 900})
        await pg.goto('http://127.0.0.1:3000/pages/admin/admin.html', wait_until='networkidle')
        await pg.wait_for_timeout(800)
        info = await pg.evaluate("""() => {
          const a = [...document.querySelectorAll('a')].find(x => (x.getAttribute('href')||'').includes('admin-users.html'));
          if (!a) return 'no link';
          const r = a.getBoundingClientRect();
          const cs = getComputedStyle(a);
          const grp = a.closest('[id*="users-grp"], .nav-group, [data-group]');
          return {visible: !!(r.width && r.height) && cs.display !== 'none' && cs.visibility !== 'hidden',
                  rect: [r.x, r.y, r.width, r.height], display: cs.display,
                  groupCollapsed: grp ? (grp.className + ' | ' + (grp.dataset.open ?? grp.getAttribute('aria-expanded'))) : 'no grp el'};
        }""")
        print('User Directory link state:', info)
        await pg.screenshot(path='scratch/admin_sidebar_full.png')
        await b.close()
asyncio.run(main())
