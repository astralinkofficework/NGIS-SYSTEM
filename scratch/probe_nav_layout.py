"""Layout probe: 3 columns present, no horizontal overflow, responsive stacking."""
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:3000/pages/admin/admin-dashboard-content.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for label, w, h in [("desktop", 1600, 950), ("tablet", 1024, 900), ("mobile", 400, 900)]:
        page = browser.new_page(viewport={"width": w, "height": h})
        page.goto(URL, wait_until="networkidle", timeout=60000)
        page.wait_for_selector("#sgmTree .sgm-node", timeout=20000)

        overflow = page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
        cols = page.evaluate("""() => {
          const g = document.querySelector('.sgm-grid');
          if (!g) return null;
          const st = getComputedStyle(g);
          const kids = [...g.children].map(c => c.getBoundingClientRect().width);
          return { display: st.display, cols: st.gridTemplateColumns, kidWidths: kids.map(x => Math.round(x)) };
        }""")
        preview_visible = page.locator("#sgmPreview").is_visible()
        tree_visible = page.locator("#sgmTree").is_visible()
        settings_visible = page.locator("#sgmSettings").is_visible()
        print("[%s %dx%d] overflowX=%d grid=%s preview=%s tree=%s settings=%s"
              % (label, w, h, overflow, cols, preview_visible, tree_visible, settings_visible))
        page.close()
    browser.close()
