from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto("http://127.0.0.1:3000/pages/principal/principal-teacher-profiles.html", wait_until="networkidle")
    pg.wait_for_timeout(1500)
    print("initial:", pg.evaluate("document.querySelectorAll('#dirBody tr').length"))
    print("roster size from state:", pg.evaluate("window.__dbg ? 1 : document.querySelectorAll('#dirBody tr[data-dbg]').length"))
    print("pager:", pg.evaluate("document.getElementById('pagerInfo').textContent"))
    pg.fill("#dirSearch", "a")
    pg.wait_for_timeout(600)
    print("after 'a':", pg.evaluate("document.querySelectorAll('#dirBody tr').length"))
    print("names:", pg.evaluate("[...document.querySelectorAll('#dirBody tr')].map(r => r.textContent.trim().slice(0,28))"))
    b.close()
