import json
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:3000"

results = []
def ck(name, cond, extra=""):
    results.append((bool(cond), name))
    print(("PASS " if cond else "FAIL ") + name + ("  " + str(extra)[:140] if extra else ""))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 950})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)[:180]))
    pg.on("console", lambda m: errs.append(m.text[:180]) if m.type == "error" else None)

    # ── principal dashboard: sidebar links + quick buttons ──
    pg.goto(BASE + "/pages/principal/principal.html", wait_until="networkidle")
    pg.wait_for_timeout(1500)
    side = pg.evaluate("document.body.textContent")
    ck("sidebar has Teacher Profiles", "Teacher Profiles" in side)
    ck("sidebar has Student Profiles", "Student Profiles" in side)
    ck("sidebar has no Teachers & Staff", "Teachers & Staff" not in side)
    ck("quick link rewired (teacher)", pg.evaluate("!!document.querySelector('a[href=\"principal-teacher-profiles.html\"]')"))
    ck("quick link rewired (student)", pg.evaluate("!!document.querySelector('a[href=\"principal-student-profiles.html\"]')"))

    # click sidebar Teacher Profiles link -> navigates
    pg.evaluate("[...document.querySelectorAll('a')].find(a => a.getAttribute('href') && a.getAttribute('href').endsWith('principal-teacher-profiles.html') && a.closest('nav,aside,.sidebar,[id*=sidebar]')).click()")
    pg.wait_for_timeout(1500)
    ck("nav click lands on teacher profiles", "principal-teacher-profiles" in pg.url, pg.url)
    rows = pg.evaluate("document.querySelectorAll('#dirBody tr').length")
    ck("directory loaded (6 teachers)", 5 <= rows <= 7, rows)
    # active state highlight exists
    ck("sidebar active state", pg.evaluate("!!document.querySelector('.nav-link.active, .sidebar-link.active, [aria-current], .active[href*=teacher]')"))

    # ── deep link directly to student profile page ──
    pg.goto(BASE + "/pages/principal/principal-student-profiles.html?student=ST-2026-007", wait_until="networkidle")
    pg.wait_for_timeout(1600)
    ck("deep link opens Srey Neang profile", pg.evaluate("(document.getElementById('profileModalInner')||{}).textContent && document.getElementById('profileModalInner').textContent.includes('Srey Neang')"))

    # ── admin dashboard sidebar ──
    pg.goto(BASE + "/pages/admin/admin.html", wait_until="networkidle")
    pg.wait_for_timeout(1500)
    aside = pg.evaluate("document.body.textContent")
    ck("admin sidebar has Teacher Profiles", "Teacher Profiles" in aside)
    ck("admin sidebar has Student Profiles", "Student Profiles" in aside)
    pg.goto(BASE + "/pages/admin/admin-teacher-profiles.html", wait_until="networkidle")
    pg.wait_for_timeout(1500)
    ck("admin teacher page rows", pg.evaluate("document.querySelectorAll('#dirBody tr').length") >= 6)

    # ── old pages 404 ──
    import urllib.request
    for path in ["/pages/principal/principal-teachers.html", "/pages/principal/principal-students.html"]:
        try:
            code = urllib.request.urlopen(BASE + path).getcode()
        except urllib.error.HTTPError as e:
            code = e.code
        ck("old page 404 " + path.split("/")[-1], code == 404, code)

    # ── all principal + admin pages still 200 ──
    import os
    broken = []
    for role in ("principal", "admin"):
        d = os.path.join("pages", role)
        for f in sorted(os.listdir(d)):
            if f.endswith(".html"):
                try:
                    code = urllib.request.urlopen(BASE + "/pages/" + role + "/" + f).getcode()
                except urllib.error.HTTPError as e:
                    code = e.code
                if code != 200:
                    broken.append((f, code))
    ck("all portal pages 200", not broken, broken)

    b.close()
    print("\nERRORS:", errs if errs else "none")

fails = [n for ok, n in results if not ok]
print("SUMMARY:", f"{len(results)-len(fails)}/{len(results)} PASS", ("FAILED: " + str(fails)) if fails else "")
