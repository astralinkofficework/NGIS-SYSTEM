from playwright.sync_api import sync_playwright

PAGES = [
    "http://127.0.0.1:3000/pages/principal/principal-reports.html",
    "http://127.0.0.1:3000/pages/principal/principal-teachers.html",
    "http://127.0.0.1:3000/pages/principal/principal-attendance.html",
    "http://127.0.0.1:3000/pages/principal/principal-classes.html",
    "http://127.0.0.1:3000/pages/principal/principal-approvals.html",
]

with sync_playwright() as p:
    br = p.chromium.launch()
    page = br.new_page(viewport={"width": 1366, "height": 768})
    for u in PAGES:
        page.goto(u, wait_until="networkidle")
        page.wait_for_timeout(1000)
        info = page.evaluate("() => ({sh: document.documentElement.scrollHeight, ih: innerHeight})")
        page.evaluate("() => window.scrollTo(0, 0)")
        page.mouse.move(700, 400)
        for _ in range(5):
            page.mouse.wheel(0, 240)
            page.wait_for_timeout(70)
        sy = page.evaluate("() => window.scrollY")
        maxs = info["sh"] - info["ih"]
        status = "OK" if (maxs <= 0 or sy > 0) else "STUCK"
        print(f"{u.split('/')[-1]:32} scrollRange={maxs:5} wheelScrollY={sy:5} -> {status}")
    br.close()
