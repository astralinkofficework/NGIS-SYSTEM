import os, tempfile
from playwright.sync_api import sync_playwright
URL = 'http://localhost:3000/pages/principal/principal-approvals.html'
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={'width': 1440, 'height': 900})
    page.goto(URL, wait_until='networkidle'); page.wait_for_timeout(700)
    print(page.evaluate("""() => {
        const cb=document.getElementById('sidebarCollapseBtn');
        const eb=document.getElementById('sidebarExpandBtn');
        const r=el=>el?{inline:el.style.display,computed:getComputedStyle(el).display,rect:Math.round(el.getBoundingClientRect().width)}:null;
        return {collapse:r(cb), expand:r(eb), innerW:window.innerWidth};
    }"""))
    b.close()
