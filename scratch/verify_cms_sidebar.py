"""Headless verification of the NGIS CMS internal sidebar redesign.

Checks: nav entries, panel switching, panel data rendering, collapse/expand,
hash navigation, mobile drawer, and horizontal overflow. Fails loudly.
"""
import sys
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:3000/pages/admin/admin-dashboard-content.html"
PANELS = [
    "panelOverview", "tabSections", "tabHero", "tabBanners",
    "tabMedia", "panelPublishing", "panelActivity",
]

results = []
errors = []


def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))
    if not cond:
        errors.append(name + (" :: " + detail if detail else ""))


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})

        console_errors = []
        page_errors = []
        page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: page_errors.append(str(e)))

        page.goto(URL, wait_until="networkidle", timeout=45000)

        # ── Nav structure ──
        items = page.locator(".cms-nav-item")
        check("nav has 7 entries", items.count() == 7, "count=%d" % items.count())
        check("internal sidebar present", page.locator("#cmsNav").count() == 1)
        check("NOT a global portal sidebar", page.locator("#cmsNav .portal-nav, #cmsNav .sidebar-nav").count() == 0)

        # ── Default panel ──
        check("default active = tabSections",
              page.locator("#tabSections").evaluate("el => el.classList.contains('active')"))
        check("default title = Page Sections",
              page.locator("#cmsPanelTitle").inner_text().strip() == "Page Sections")

        # ── Switch through every panel ──
        for pid in PANELS:
            page.locator('.cms-nav-item[data-panel="%s"]' % pid).click()
            page.wait_for_timeout(250)
            active = page.locator("#" + pid).evaluate("el => el.classList.contains('active')")
            visible = page.locator("#" + pid).is_visible()
            selected = page.locator('.cms-nav-item[data-panel="%s"]' % pid).get_attribute("aria-selected")
            check("panel %s activates" % pid, active and visible, "active=%s visible=%s" % (active, visible))
            check("panel %s aria-selected" % pid, selected == "true", "got=%s" % selected)

        # ── Panel content actually rendered (no fakes) ──
        page.locator('.cms-nav-item[data-panel="panelOverview"]').click()
        page.wait_for_timeout(800)
        check("overview rendered stats",
              page.locator("#cmsOverviewBody .cms-stat-card").count() >= 4,
              "cards=%d" % page.locator("#cmsOverviewBody .cms-stat-card").count())
        ov = page.locator("#cmsOverviewBody").inner_text()
        check("overview has no raw error", "Unable to load" not in ov)

        page.locator('.cms-nav-item[data-panel="panelPublishing"]').click()
        page.wait_for_timeout(400)
        check("publishing rendered",
              page.locator("#cmsPublishStatus .cms-kv-row").count() >= 3,
              "rows=%d" % page.locator("#cmsPublishStatus .cms-kv-row").count())
        check("visibility rendered",
              page.locator("#cmsVisibilityList .cms-visibility-row").count() >= 1)

        page.locator('.cms-nav-item[data-panel="panelActivity"]').click()
        page.wait_for_timeout(900)
        act = page.locator("#cmsActivityList").inner_text()
        check("activity loaded or empty state",
              page.locator("#cmsActivityList .cms-activity-item").count() > 0
              or "No recorded" in act,
              act[:80])

        # ── Page Sections panel preserves real list ──
        page.locator('.cms-nav-item[data-panel="tabSections"]').click()
        page.wait_for_timeout(300)
        secs = page.locator("#cmsSectionsList").inner_text().strip()
        check("sections list populated", len(secs) > 0, "len=%d" % len(secs))

        # ── Hash navigation ──
        page.goto(URL + "#tabHero", wait_until="networkidle", timeout=45000)
        page.wait_for_timeout(400)
        check("hash opens tabHero",
              page.locator("#tabHero").evaluate("el => el.classList.contains('active')"))
        page.go_back()
        page.wait_for_timeout(400)
        check("browser back returns to sections",
              page.locator("#tabSections").evaluate("el => el.classList.contains('active')"))

        # ── Collapse / expand ──
        page.locator("#cmsNavCollapse").click()
        page.wait_for_timeout(250)
        check("collapse applies nav-collapsed",
              page.locator(".cms-workspace").evaluate("el => el.classList.contains('nav-collapsed')"))
        page.locator("#cmsNavCollapse").click()
        page.wait_for_timeout(250)
        check("expand removes nav-collapsed",
              not page.locator(".cms-workspace").evaluate("el => el.classList.contains('nav-collapsed')"))

        # ── Desktop overflow ──
        ow = page.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
        check("no horizontal overflow (desktop)", ow <= 2, "overflow=%d" % ow)

        # ── Mobile drawer ──
        page.set_viewport_size({"width": 390, "height": 844})
        page.wait_for_timeout(400)
        check("mobile nav toggle visible", page.locator("#cmsNavToggle").is_visible())
        page.locator("#cmsNavToggle").click()
        page.wait_for_timeout(350)
        check("drawer opens", page.locator("#cmsNav").evaluate("el => el.classList.contains('open')"))
        check("backdrop visible", page.locator("#cmsNavBackdrop").is_visible())
        page.mouse.click(378, 500)
        page.wait_for_timeout(350)
        check("drawer closes on backdrop", not page.locator("#cmsNav").evaluate("el => el.classList.contains('open')"))
        # open, pick a panel, drawer auto-closes
        page.locator("#cmsNavToggle").click()
        page.wait_for_timeout(300)
        page.locator('.cms-nav-item[data-panel="tabBanners"]').click()
        page.wait_for_timeout(350)
        check("drawer closes after nav",
              not page.locator("#cmsNav").evaluate("el => el.classList.contains('open')"))
        check("mob nav switched panel",
              page.locator("#tabBanners").evaluate("el => el.classList.contains('active')"))
        ow2 = page.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
        check("no horizontal overflow (mobile)", ow2 <= 2, "overflow=%d" % ow2)

        browser.close()

    # ── JS errors (ignore failed external CDN font/icon loads) ──
    ignorable = ("fonts.googleapis", "fonts.gstatic", "unpkg.com", "cdn.tailwindcss", "ERR_INTERNET", "net::")
    console_errors = [e for e in console_errors if not any(k in e for k in ignorable)]
    check("no JS page errors", len(page_errors) == 0, "; ".join(page_errors[:3]))
    check("no JS console errors", len(console_errors) == 0, "; ".join(console_errors[:3]))

    print("\n=== CMS SIDEBAR VERIFICATION ===")
    for name, ok, detail in results:
        print(("PASS  " if ok else "FAIL  ") + name + (("  [" + detail + "]") if detail and not ok else ""))
    print("\n%d/%d checks passed" % (sum(1 for _, ok, _ in results if ok), len(results)))
    if errors:
        print("\nFAILURES:\n  - " + "\n  - ".join(errors))
        sys.exit(1)
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
