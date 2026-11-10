import json
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:3000/pages/principal/principal-reports.html"

with sync_playwright() as p:
    br = p.chromium.launch()
    page = br.new_page(viewport={"width": 1366, "height": 768})
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(1200)

    res = page.evaluate("() => ({sh: document.documentElement.scrollHeight, ih: innerHeight})")
    print("viewport 1366x768 ->", res)

    def wheel_test(name, x, y):
        page.mouse.move(x, y)
        page.evaluate("() => window.scrollTo(0, 0)")
        for _ in range(5):
            page.mouse.wheel(0, 240)
            page.wait_for_timeout(80)
        sy = page.evaluate("() => window.scrollY")
        print(f"wheel at {name}: scrollY after 5x240 = {sy}")
        return sy

    out = {}
    out["content_mid"] = wheel_test("content middle", 700, 400)
    out["over_table"] = wheel_test("over table body", 700, 600)
    out["hero_area"] = wheel_test("hero/top area", 700, 60)
    out["over_sidebar"] = wheel_test("over sidebar", 100, 400)
    out["bottom_right"] = wheel_test("bottom right", 1200, 700)

    # drag-scroll with mouse held? and keyboard
    page.evaluate("() => window.scrollTo(0, 0)")
    page.keyboard.press("End")
    page.wait_for_timeout(300)
    print("keyboard End ->", page.evaluate("() => window.scrollY"))

    # check what element is under hero area point
    print("elementFromPoint(700,60):", page.evaluate("""() => {
      const el = document.elementFromPoint(700, 60);
      const s = el ? getComputedStyle(el) : null;
      return el ? {tag: el.tagName, id: el.id, cls: String(el.className).slice(0,80), pos: s.position, oy: s.overflowY, h: Math.round(el.getBoundingClientRect().height), pe: s.pointerEvents} : null;
    }"""))
    # and full-size fixed elements regardless of opacity
    print("fixed layers:", page.evaluate("""() => [...document.querySelectorAll('body *')].filter(el => {
      const s = getComputedStyle(el); return s.position === 'fixed' && s.display !== 'none';
    }).map(el => { const r = el.getBoundingClientRect(); const s = getComputedStyle(el);
      return {id: el.id, cls: String(el.className).slice(0,50), w: Math.round(r.width), h: Math.round(r.height), z: s.zIndex, pe: s.pointerEvents, oy: s.overflowY};
    }).filter(o => o.h > 100)"""))
    br.close()
