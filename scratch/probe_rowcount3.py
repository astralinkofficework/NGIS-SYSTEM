from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    logs = []
    pg.on("console", lambda m: logs.append(m.text))
    pg.goto("http://127.0.0.1:3000/pages/principal/principal-teacher-profiles.html", wait_until="networkidle")
    pg.wait_for_timeout(1200)
    print("dbg exists:", pg.evaluate("!!window.__NGIS_PROFILES_DEBUG"))
    print("state:", pg.evaluate("({all: __NGIS_PROFILES_DEBUG.state.all.length, filtered: __NGIS_PROFILES_DEBUG.state.filtered.length, search: __NGIS_PROFILES_DEBUG.state.search})"))
    pg.fill("#dirSearch", "a")
    pg.wait_for_timeout(500)
    print("after fill:", pg.evaluate("({all: __NGIS_PROFILES_DEBUG.state.all.length, filtered: __NGIS_PROFILES_DEBUG.state.filtered.length, search: __NGIS_PROFILES_DEBUG.state.search, page: __NGIS_PROFILES_DEBUG.state.page})"))
    print("trs:", pg.evaluate("document.querySelectorAll('#dirBody tr').length"))
    print("tbody html tail:", pg.evaluate("document.querySelector('#dirBody').innerHTML.slice(-320)"))
    b.close()
