import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1440, 'height': 1000})
    pg.goto('http://127.0.0.1:3000/pages/principal/principal-reports.html', wait_until='networkidle')
    pg.wait_for_timeout(1200)
    r = pg.evaluate("""() => {
        let o = [];
        document.querySelectorAll('body *').forEach(el => {
            const w = getComputedStyle(el).fontWeight;
            if (parseInt(w) >= 600) o.push({
                tag: el.tagName,
                cls: (el.className || '').toString().slice(0, 70),
                txt: (el.textContent || '').trim().slice(0, 40),
                w: w,
                inPage: !!el.closest('.page')
            });
        });
        return o;
    }""")
    for item in r:
        print(item)
    b.close()
