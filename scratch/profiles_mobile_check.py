import os
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:3000"
shots = os.path.join(os.path.dirname(os.path.abspath(__file__)), "profile_shots")
os.makedirs(shots, exist_ok=True)
results = []
def ck(name, cond, extra=""):
    results.append((bool(cond), name)); print(("PASS " if cond else "FAIL ") + name + ("  " + str(extra)[:140] if extra else ""))

with sync_playwright() as p:
    b = p.chromium.launch()

    # desktop screenshots
    pg = b.new_page(viewport={"width": 1440, "height": 950})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)[:160]))
    pg.on("console", lambda m: errs.append(m.text[:160]) if m.type == "error" else None)
    for tag, path in [("teacher", "/pages/principal/principal-teacher-profiles.html"),
                      ("student", "/pages/principal/principal-student-profiles.html")]:
        pg.goto(BASE + path, wait_until="networkidle")
        pg.wait_for_timeout(1600)
        pg.screenshot(path=os.path.join(shots, f"principal-{tag}-profiles.png"))
    for tag, path in [("teacher", "/pages/admin/admin-teacher-profiles.html"),
                      ("student", "/pages/admin/admin-student-profiles.html")]:
        pg.goto(BASE + path, wait_until="networkidle")
        pg.wait_for_timeout(1600)
        pg.screenshot(path=os.path.join(shots, f"admin-{tag}-profiles.png"))
    ck("desktop screenshots + no errors", len(errs) == 0, errs[:4])
    pg.close()

    # mobile 390px: hamburger opens drawer, no horizontal overflow
    mp = b.new_page(viewport={"width": 390, "height": 844})
    merrs = []
    mp.on("pageerror", lambda e: merrs.append(str(e)[:160]))
    for tag, path in [("principal", "/pages/principal/principal-teacher-profiles.html"),
                      ("principal-student", "/pages/principal/principal-student-profiles.html"),
                      ("admin", "/pages/admin/admin-teacher-profiles.html")]:
        mp.goto(BASE + path, wait_until="networkidle")
        mp.wait_for_timeout(1500)
        hb = mp.evaluate_handle("() => [...document.querySelectorAll('.mobile-hamburger-btn')].find(el => { const r = el.getBoundingClientRect(); return r.width > 10 && r.height > 10 && el.offsetParent !== null; })").as_element()
        ck(f"mobile {tag}: hamburger visible", hb is not None and hb.is_visible())
        over = mp.evaluate("document.documentElement.scrollWidth - window.innerWidth")
        ck(f"mobile {tag}: no h-overflow", over <= 1, over)
        hb.click()
        mp.wait_for_timeout(600)
        drawer = mp.evaluate("""(() => {
          const el = document.querySelector('.sidebar.open, #sidebar.open, aside.open, .sidebar.is-open, [id*=sidebar].open, .mobile-drawer-open .sidebar, body.nav-open .sidebar, .sidebar');
          if (!el) return 'none';
          const r = el.getBoundingClientRect();
          return (r.left > -r.width * 0.5 && r.left < window.innerWidth * 0.5 && r.width > 100) ? 'open' : ('rect:' + Math.round(r.left) + '/' + Math.round(r.width));
        })()""")
        ck(f"mobile {tag}: drawer slid into view", drawer == "open", drawer)
        mp.screenshot(path=os.path.join(shots, f"mobile-{tag}-drawer.png"))
        mp.keyboard.press("Escape")
        mp.evaluate("document.body.click()")
    ck("mobile no page errors", len(merrs) == 0, merrs[:4])
    b.close()

fails = [n for ok, n in results if not ok]
print("SUMMARY:", f"{len(results)-len(fails)}/{len(results)} PASS", fails if fails else "")
print("SHOTS:", sorted(os.listdir(shots)))
