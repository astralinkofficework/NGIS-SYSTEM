import json
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:3000/pages/principal/principal-reports.html"

Measure = """() => {
  const wrap = document.querySelector('.overflow-x-auto');
  const table = wrap ? wrap.querySelector('table') : null;
  const hamburger = !!document.querySelector('.hamburger-btn, .mobile-hamburger-btn');
  const h = document.getElementById('heroBanner');
  return {
    tableW: table ? table.scrollWidth : -1,
    wrapW: wrap ? wrap.clientWidth : -1,
    docOverflow: document.documentElement.scrollWidth > window.innerWidth + 1,
    hamburger,
    hero: h ? getComputedStyle(h).display : 'removed',
    rows: document.querySelectorAll('#clearanceBody tr').length,
    gpa: (document.getElementById('repAvgGpa')||{}).textContent,
    att: (document.getElementById('repAttRate')||{}).textContent,
    pass: (document.getElementById('repHonorRoll')||{}).textContent,
    kpiCards: document.querySelectorAll('.telemetry-card').length,
    h1Size: getComputedStyle(document.querySelector('h1')).fontSize,
  };
}"""

results = {}
errors_all = []
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    errs = []
    page.on("pageerror", lambda e: errs.append(str(e)))
    page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(1500)

    d = page.evaluate(Measure)
    results["desktop"] = d

    # search filter
    page.fill("#tableSearch", "jenkins")
    page.wait_for_timeout(200)
    vis = page.evaluate("() => [...document.querySelectorAll('#clearanceBody tr')].filter(r => r.style.display !== 'none').length")
    results["search_jenkins"] = vis
    page.fill("#tableSearch", "")

    # status filter
    page.select_option("#statusFilter", "ready")
    page.wait_for_timeout(200)
    results["filter_ready"] = page.evaluate("() => [...document.querySelectorAll('#clearanceBody tr')].filter(r => r.style.display !== 'none').length")
    page.select_option("#statusFilter", "")

    # select all -> bulk toolbar
    page.click("#selectAllCheckbox")
    page.wait_for_timeout(200)
    results["selectAll_count"] = page.evaluate("() => document.querySelectorAll('.row-checkbox:checked').length")
    results["bulkVisible"] = page.evaluate("() => !document.getElementById('bulk-toolbar').classList.contains('hidden')")
    page.click("#batchApproveSelectedBtn")
    page.wait_for_timeout(200)
    results["toast"] = page.evaluate("() => document.getElementById('toast').textContent")
    results["bulkAfterBatch"] = page.evaluate("() => !document.getElementById('bulk-toolbar').classList.contains('hidden')")

    errors_all += errs

    # tablet
    page.set_viewport_size({"width": 900, "height": 1000})
    page.wait_for_timeout(600)
    results["tablet"] = page.evaluate(Measure)

    # mobile
    page.set_viewport_size({"width": 390, "height": 844})
    page.wait_for_timeout(600)
    results["mobile"] = page.evaluate(Measure)
    page.screenshot(path=r"c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\scratch\reports_redesign_mobile.png")
    page.set_viewport_size({"width": 1440, "height": 900})
    page.wait_for_timeout(600)
    page.screenshot(path=r"c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\scratch\reports_redesign_desktop.png")
    browser.close()

print(json.dumps(results, indent=2))
print("ERRORS:", errors_all if errors_all else "none")
