import json, os
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:3000"
shots = os.path.join(os.path.dirname(os.path.abspath(__file__)), "profile_shots")
os.makedirs(shots, exist_ok=True)
results = []
def ck(name, cond, extra=""):
    results.append((bool(cond), name))
    print(("PASS " if cond else "FAIL ") + name + ("  " + str(extra)[:140] if extra else ""))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 950})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
    pg.on("console", lambda m: errs.append("console: " + m.text[:150]) if m.type == "error" else None)

    # ── classes page ──
    pg.goto(BASE + "/pages/principal/principal-classes.html", wait_until="networkidle")
    pg.wait_for_timeout(1600)
    body = pg.evaluate("document.body.innerText")
    ck("classes: breadcrumb removed", "Principal Academic Oversight" not in body)
    ck("classes: subtitle removed", "Central school authority over all teacher classes" not in body)
    btns = pg.evaluate("[...document.querySelectorAll('#classesTable tbody button, tbody button')].map(x => x.textContent.trim()).filter(t => t)")
    ck("classes: View/Edit buttons render", "View" in btns and "Edit" in btns, btns[:6])
    ck("classes: fake more-options removed", pg.evaluate("!document.querySelector('[aria-label=\"More options\"]')"))
    pg.click("tbody button:has-text('View')")
    pg.wait_for_timeout(600)
    ck("classes: View opens students modal", pg.evaluate("!document.getElementById('classStudentsModal').classList.contains('hidden')"))
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(300)
    pg.evaluate("document.getElementById('classStudentsModal') && document.getElementById('classStudentsModal').classList.add('hidden')")
    pg.click("tbody button:has-text('Edit')")
    pg.wait_for_timeout(400)
    ck("classes: Edit opens edit modal", pg.evaluate("(() => { const m=document.getElementById('editClassModal'); return m && !m.classList.contains('hidden'); })()"))
    pg.evaluate("document.getElementById('editClassModal') && document.getElementById('editClassModal').classList.add('hidden')")

    # ── profile pages: header removals + toolbar responsive ──
    for page, label, other in [
        ("principal-teacher-profiles", "teacher", "enrolled student"),
        ("principal-student-profiles", "student", "educator on file"),
    ]:
        pg.goto(BASE + "/pages/principal/" + page + ".html", wait_until="networkidle")
        pg.wait_for_timeout(1500)
        t = pg.evaluate("document.body.innerText")
        ck(label + ": eyebrow gone", "Principal Central" not in t and "Faculty Registry" not in t and "Enrolled Cohort" not in t)
        ck(label + ": subtitle gone", "Central directory of every" not in t)
        ck(label + ": title present", (label.capitalize() + " Profiles") in t or "Profiles" in t)
        ck(label + ": table loads", pg.evaluate("document.querySelectorAll('#dirBody tr').length") > 0)
        # desktop toolbar: search + filters on one row
        geo = pg.evaluate("""(() => {
          const s = document.getElementById('dirSearch').getBoundingClientRect();
          const d = document.getElementById('deptFilter').getBoundingClientRect();
          return { sameRow: Math.abs((s.top + s.height/2) - (d.top + d.height/2)) < 40, sw: Math.round(s.width), dw: Math.round(d.width) };
        })()""")
        ck(label + ": desktop toolbar inline", geo["sameRow"], geo)
        pg.screenshot(path=os.path.join(shots, page + "-desktop-new.png"))

    # ── mobile toolbar ──
    mp = b.new_page(viewport={"width": 390, "height": 844})
    mp_errs = []
    mp.on("pageerror", lambda e: mp_errs.append(str(e)[:200]))
    mp.goto(BASE + "/pages/principal/principal-teacher-profiles.html", wait_until="networkidle")
    mp.wait_for_timeout(1500)
    mgeo = mp.evaluate("""(() => {
      const vw = window.innerWidth;
      const over = [...document.querySelectorAll('#deptFilter,#statusFilter,#sortSelect,#btnResetFilters,#dirSearch')]
        .map(el => { const r = el.getBoundingClientRect(); return { id: el.id, right: Math.round(r.right), w: Math.round(r.width) }; })
        .filter(x => x.right > vw - 4 || x.w < 60);
      const d = document.getElementById('deptFilter').getBoundingClientRect();
      const s = document.getElementById('statusFilter').getBoundingClientRect();
      return { overflow: over, deptStatusSideBySide: Math.abs(d.top - s.top) < 8 };
    })()""")
    ck("mobile: toolbar fits width", not mgeo["overflow"], mgeo["overflow"])
    ck("mobile: filters side-by-side grid", mgeo["deptStatusSideBySide"])
    ck("mobile: no page errors", not mp_errs, mp_errs)
    mp.screenshot(path=os.path.join(shots, "principal-teacher-profiles-mobile-new.png"))

    ck("no console errors (desktop pass)", not errs, errs[:3])
    b.close()

fails = [n for ok, n in results if not ok]
print("SUMMARY: %d/%d PASS" % (len(results) - len(fails), len(results)) + (" FAILED: " + str(fails) if fails else ""))
