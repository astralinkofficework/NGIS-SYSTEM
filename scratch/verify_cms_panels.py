"""Regression: every CMS panel in admin-dashboard-content.html still renders."""
import sys
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:3000/pages/admin/admin-dashboard-content.html"
PANELS = ["panelOverview", "tabSections", "tabHero", "tabBanners",
          "tabMedia", "panelPublishing", "panelActivity"]

results = []
errors = []


def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))
    if not cond:
        errors.append(name + (" :: " + detail if detail else ""))


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1600, "height": 950})
    page_errors = []
    page.on("pageerror", lambda e: page_errors.append(str(e)))

    page.goto(URL, wait_until="networkidle", timeout=60000)

    check("cms nav has 7 entries", page.locator(".cms-nav-item").count() == 7,
          "count=%d" % page.locator(".cms-nav-item").count())

    for pid in PANELS:
        page.locator('.cms-nav-item[data-panel="%s"]' % pid).click()
        page.wait_for_timeout(300)
        panel = page.locator("#" + pid)
        active = panel.evaluate("el => el.classList.contains('active')")
        visible = panel.is_visible()
        text = panel.inner_text().strip()
        check("panel %s active+visible" % pid, active and visible,
              "active=%s visible=%s" % (active, visible))
        check("panel %s has content" % pid, len(text) > 20, "len=%d" % len(text))

    check("no page errors", len(page_errors) == 0, "errors=%s" % page_errors[:3])
    browser.close()

print("=" * 60)
for name, ok, detail in results:
    print(("PASS " if ok else "FAIL ") + name + (("  ->  " + detail) if detail and not ok else ""))
print("=" * 60)
print("TOTAL %d  PASSED %d  FAILED %d" % (len(results), sum(1 for _, ok, _ in results if ok), len(errors)))
sys.exit(1 if errors else 0)
