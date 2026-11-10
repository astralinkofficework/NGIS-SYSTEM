import json
from playwright.sync_api import sync_playwright

PAGES = [
    ("principal-teacher", "http://127.0.0.1:3000/pages/principal/principal-teacher-profiles.html"),
    ("principal-student", "http://127.0.0.1:3000/pages/principal/principal-student-profiles.html"),
    ("admin-teacher", "http://127.0.0.1:3000/pages/admin/admin-teacher-profiles.html"),
    ("admin-student", "http://127.0.0.1:3000/pages/admin/admin-student-profiles.html"),
]

MEASURE = """() => {
  const rows = document.querySelectorAll('#dirBody tr').length;
  const kpis = [...document.querySelectorAll('#kpiGrid .pf-kpi')].map(c => c.textContent.replace(/\\s+/g,' ').trim().slice(0,60));
  return {
    rows,
    kpis,
    hamburger: !!document.querySelector('.hamburger-btn'),
    sidebar: !!document.querySelector('.sidebar, #ngisSidebar, aside'),
    chips: (document.getElementById('filterChips')||{}).textContent,
    pager: (document.getElementById('pagerInfo')||{}).textContent,
    tableW: (() => { const w=document.querySelector('.overflow-x-auto'); const t=w&&w.querySelector('table'); return t?t.scrollWidth:-1; })(),
    wrapW: (() => { const w=document.querySelector('.overflow-x-auto'); return w?w.clientWidth:-1; })(),
  };
}"""

PROFILE_CHECK = """() => {
  const modal = document.getElementById('profileModal');
  const tabs = [...document.querySelectorAll('#pfTabBar .pf-tab')].map(t => t.textContent.trim());
  const cells = [...document.querySelectorAll('#pfTabBody .pf-cell-value')].slice(0,6).map(c => c.textContent.trim());
  return { open: modal && !modal.classList.contains('hidden'), tabs, cells };
}"""

out = {}
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    errors = {}
    cur = None

    def hook(kind, msg):
        errors.setdefault(cur, []).append(kind + ": " + msg[:200])

    for name, url in PAGES:
        cur = name
        errors[name] = []
        page.on("pageerror", lambda e: hook("pageerror", str(e)))
        page.on("console", lambda m: hook("console", m.text) if m.type == "error" else None)
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(1800)
        d = page.evaluate(MEASURE)
        # wheel scroll sanity
        page.mouse.move(700, 500)
        page.mouse.wheel(0, 600)
        page.wait_for_timeout(400)
        d["scrollY"] = page.evaluate("window.scrollY")
        # search filter
        page.fill("#dirSearch", "a")
        page.wait_for_timeout(300)
        d["rowsAfterSearch"] = page.evaluate("document.querySelectorAll('#dirBody tr').length")
        page.fill("#dirSearch", "")
        page.wait_for_timeout(300)
        # open first profile
        first = page.query_selector("#dirBody [data-act='view']")
        if first:
            first.click()
            page.wait_for_timeout(1200)
            d["profile"] = page.evaluate(PROFILE_CHECK)
            # click every tab, record tab body length
            tabinfo = []
            ntabs = page.evaluate("document.querySelectorAll('#pfTabBar .pf-tab').length")
            for i in range(ntabs):
                page.evaluate(f"document.querySelectorAll('#pfTabBar .pf-tab')[{i}].click()")
                page.wait_for_timeout(500)
                tabinfo.append(page.evaluate("(() => { const b=document.getElementById('pfTabBody'); return b ? (b.textContent||'').trim().length : -1; })()"))
            d["tabLens"] = tabinfo
            page.evaluate("window.__ngisCloseProfile()")
        # pagination click page 2 if exists
        d["hasPagerBtns"] = page.evaluate("document.querySelectorAll('#pagerControls [data-page]').length")
        out[name] = d
    # screenshots of teacher principal
    pg = browser.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(PAGES[0][1], wait_until="networkidle")
    pg.wait_for_timeout(1500)
    pg.screenshot(path="scratch/profiles_teacher_principal.png", full_page=False)
    pg.goto(PAGES[3][1], wait_until="networkidle")
    pg.wait_for_timeout(1500)
    pg.screenshot(path="profiles_student_admin.png", full_page=False)
    browser.close()

print(json.dumps(out, indent=1)[:4000])
print("\nERRORS:")
for k, v in errors.items():
    print(k, "->", v[:6] if v else "none")
