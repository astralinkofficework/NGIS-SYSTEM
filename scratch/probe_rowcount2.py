from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto("http://127.0.0.1:3000/pages/principal/principal-teacher-profiles.html", wait_until="networkidle")
    pg.wait_for_timeout(1200)
    print("dirBody count:", pg.evaluate("document.querySelectorAll('[id=dirBody]').length"))
    print("dirSearch count:", pg.evaluate("document.querySelectorAll('[id=dirSearch]').length"))
    print("profilesRoot count:", pg.evaluate("document.querySelectorAll('[id=profilesRoot]').length"))
    print("scripts ngis-profiles:", pg.evaluate("document.querySelectorAll('script[src*=ngis-profiles]').length"))
    # trace renderTable calls
    pg.evaluate("""() => { window.__calls = []; const mo = new MutationObserver(() => window.__calls.push(document.querySelectorAll('#dirBody tr').length)); mo.observe(document.querySelector('[id=dirBody]'), {childList: true, subtree: true}); window.__mo = mo; }""")
    pg.fill("#dirSearch", "a")
    pg.wait_for_timeout(800)
    print("mutation snapshots:", pg.evaluate("window.__calls"))
    print("rows:", pg.evaluate("document.querySelectorAll('#dirBody tr').length"))
    b.close()
