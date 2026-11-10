import json
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:3000/pages/principal/principal-reports.html"
errs = []
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1440, "height": 900})
    page.on("pageerror", lambda e: errs.append(str(e)))
    page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(1500)
    out = page.evaluate("""() => ({
      liveSection: !!document.getElementById('academicLiveSummary'),
      rows: document.querySelectorAll('#clearanceBody tr').length,
      gpa: (document.getElementById('repAvgGpa')||{}).textContent,
      firstChild: document.querySelector('.page > div > div').firstElementChild.className.slice(0, 40),
    })""")
    b.close()
print(json.dumps(out, indent=2))
print("ERRORS:", errs if errs else "none")
