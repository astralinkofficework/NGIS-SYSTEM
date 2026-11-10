import os, json
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:3000"
shots = os.path.join(os.path.dirname(os.path.abspath(__file__)), "profile_shots")
os.makedirs(shots, exist_ok=True)
results = []
def ck(name, cond, extra=""):
    results.append((bool(cond), name))
    print(("PASS " if cond else "FAIL ") + name + ("  " + str(extra)[:150] if extra else ""))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 950})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
    pg.on("console", lambda m: errs.append("console: " + m.text[:150]) if m.type == "error" else None)

    pg.goto(BASE + "/pages/principal/principal-departments.html", wait_until="networkidle")
    pg.wait_for_timeout(1800)

    rows = pg.evaluate("document.querySelectorAll('#departmentsTableBody tr').length")
    ck("table renders live departments", rows >= 5, rows)
    ck("subtitle removed", pg.evaluate("!document.body.innerText.includes('Principal management over school departments')"))
    ck("pager info shows", "departments" in (pg.evaluate("document.getElementById('deptPagerInfo').textContent") or ""))
    ck("grid hidden in table mode", pg.evaluate("document.getElementById('departmentsGrid').classList.contains('hidden')"))

    # compliance bars render
    bars = pg.evaluate("document.querySelectorAll('#departmentsTableBody .rounded-full > div[style*=width]').length")
    ck("compliance bars render", bars >= 5, bars)

    # toggle to grid
    pg.click("#btnViewGrid")
    pg.wait_for_timeout(500)
    ck("grid mode shows cards", pg.evaluate("!document.getElementById('departmentsGrid').classList.contains('hidden') && document.querySelectorAll('#departmentsGrid .dept-card').length >= 5"))
    ck("grid mode hides table", pg.evaluate("document.getElementById('departmentsTableWrap').classList.contains('hidden')"))

    # toggle back to table
    pg.click("#btnViewTable")
    pg.wait_for_timeout(500)
    ck("back to table mode", pg.evaluate("!document.getElementById('departmentsTableWrap').classList.contains('hidden')"))

    # search filter
    pg.fill("#deptSearchInput", "math")
    pg.wait_for_timeout(400)
    rows2 = pg.evaluate("document.querySelectorAll('#departmentsTableBody tr').length")
    ck("search filters rows", 1 <= rows2 < rows, f"{rows2}/{rows}")
    pg.fill("#deptSearchInput", "")
    pg.wait_for_timeout(400)

    # Manage opens edit modal
    pg.click("#departmentsTableBody button:has-text('Manage')")
    pg.wait_for_timeout(400)
    ck("Manage opens edit modal", pg.evaluate("!document.getElementById('editDeptModal').classList.contains('hidden')"))
    pg.evaluate("closeEditModal()")

    # View Syllabi opens faculty modal
    pg.click("#departmentsTableBody button:has-text('View Syllabi')")
    pg.wait_for_timeout(400)
    ck("View Syllabi opens faculty modal", pg.evaluate("!document.getElementById('deptFacultyModal').classList.contains('hidden')"))
    pg.evaluate("closeFacultyModal()")

    # CSV export
    try:
        with pg.expect_download(timeout=8000) as dl:
            pg.click("button:has-text('Export CSV')")
        ck("CSV export downloads", (dl.value.suggested_filename or "").endswith(".csv"), dl.value.suggested_filename)
    except Exception as e:
        ck("CSV export downloads", False, str(e)[:120])

    # no-bold audit: computed weights on key nodes
    weights = pg.evaluate("""(() => {
      const sel = ['h1','#departmentsTableBody td','#departmentsTableBody th, thead th','#deptPagerInfo','.telemetry-card span'];
      const bad = [];
      document.querySelectorAll('h1, thead th, #departmentsTableBody td, #departmentsTableBody button').forEach(el => {
        const w = parseInt(getComputedStyle(el).fontWeight, 10);
        if (w > 500) bad.push(el.tagName + '.' + (el.className || '').toString().slice(0,30) + '=' + w);
      });
      return bad.slice(0, 5);
    })()""")
    ck("no-bold rule: all weights <= 500", not weights, weights)

    pg.evaluate("document.querySelectorAll('#departmentsTableWrap .overflow-x-auto, #departmentsTableWrap').forEach(el => el.scrollLeft = 0); window.scrollTo(0, 0);")
    pg.wait_for_timeout(300)
    pg.screenshot(path=os.path.join(shots, "principal-departments-table.png"))
    ck("no console errors (desktop)", not errs, errs[:3])

    # mobile pass
    mp = b.new_page(viewport={"width": 390, "height": 844})
    merrs = []
    mp.on("pageerror", lambda e: merrs.append(str(e)[:200]))
    mp.goto(BASE + "/pages/principal/principal-departments.html", wait_until="networkidle")
    mp.wait_for_timeout(1600)
    ham = mp.evaluate("""(() => [...document.querySelectorAll('.mobile-hamburger-btn, .hamburger-btn')].find(el => { const r = el.getBoundingClientRect(); return r.width > 10 && r.height > 10 && el.offsetParent !== null; }) ? true : false)()""")
    ck("mobile: visible hamburger", ham)
    mgeo = mp.evaluate("""(() => {
      const vw = window.innerWidth;
      const s = document.getElementById('deptSearchInput').getBoundingClientRect();
      const overflow = [...document.querySelectorAll('#statusFilter,#complianceFilter,#btnViewGrid,#btnViewTable')].filter(el => el.getBoundingClientRect().right > vw - 2).length;
      return { searchFull: s.width > vw * 0.6, overflow };
    })()""")
    ck("mobile: toolbar wraps without overflow", mgeo["searchFull"] and mgeo["overflow"] == 0, mgeo)
    ck("mobile: table scrolls horizontally", mp.evaluate("(() => { const t=document.querySelector('#departmentsTableWrap .overflow-x-auto'); return t.scrollWidth > t.clientWidth; })()"))
    ck("mobile: no page errors", not merrs, merrs[:2])
    mp.screenshot(path=os.path.join(shots, "principal-departments-mobile.png"))
    b.close()

fails = [n for ok, n in results if not ok]
print("SUMMARY: %d/%d PASS" % (len(results) - len(fails), len(results)) + (" FAILED: " + str(fails) if fails else ""))
