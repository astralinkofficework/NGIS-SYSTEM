import os, tempfile
from playwright.sync_api import sync_playwright

BASE = 'http://localhost:3000'
URL = BASE + '/pages/principal/principal-approvals.html'
OUT = os.path.join(tempfile.gettempdir(), 'ngis_lockcheck')
os.makedirs(OUT, exist_ok=True)

def probe(page):
    return page.evaluate("""() => {
        const sb = document.getElementById('sidebar') || document.querySelector('.sidebar');
        const cb = document.getElementById('sidebarCollapseBtn');
        const eb = document.getElementById('sidebarExpandBtn');
        const vis = el => el && getComputedStyle(el).display !== 'none' && el.offsetParent !== null;
        return {
            collapsed: sb ? sb.classList.contains('collapsed') : null,
            open: sb ? sb.classList.contains('open') : null,
            width: sb ? Math.round(sb.getBoundingClientRect().width) : null,
            collapseBtnVisible: vis(cb),
            expandBtnVisible: vis(eb),
        };
    }""")

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={'width': 1440, 'height': 900})
    page.goto(URL, wait_until='networkidle')
    page.wait_for_timeout(600)
    print('DESKTOP initial   :', probe(page))
    # Try to force-close via the exposed API / click the toggles
    page.evaluate("() => { const e=document.getElementById('sidebarExpandBtn'); if(e) e.click(); }")
    page.wait_for_timeout(300)
    print('DESKTOP after exp :', probe(page))
    page.evaluate("() => { if(window.toggleSidebar) window.toggleSidebar(); }")
    page.wait_for_timeout(300)
    print('DESKTOP after tog :', probe(page))
    # Shrink to mobile, then back to desktop
    page.set_viewport_size({'width': 500, 'height': 900})
    page.wait_for_timeout(400)
    print('MOBILE            :', probe(page))
    page.set_viewport_size({'width': 1440, 'height': 900})
    page.wait_for_timeout(400)
    print('BACK TO DESKTOP   :', probe(page))
    page.screenshot(path=os.path.join(OUT, 'desktop_locked.png'))
    b.close()
print('shot:', os.path.join(OUT, 'desktop_locked.png'))
