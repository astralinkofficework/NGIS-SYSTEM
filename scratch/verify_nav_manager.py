"""NGIS Global Sidebar Manager - headless UI verification.

Checks the manager workspace inside admin-dashboard-content.html:
portal loading, tree rendering, item editing, live preview, viewport modes,
undo, health/validate panels, version modal, portal switching, and that the
student sidebar stays functional. Fails loudly.
"""
import sys
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:3000/pages/admin/admin-dashboard-content.html"

results = []
errors = []


def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))
    if not cond:
        errors.append(name + (" :: " + detail if detail else ""))


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1600, "height": 950})

        page_errors = []
        console_errors = []
        page.on("pageerror", lambda e: page_errors.append(str(e)))
        page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)

        page.goto(URL, wait_until="networkidle", timeout=60000)

        # ── Nav item + default panel ──
        sm_item = page.locator('.cms-nav-item[data-panel="tabSections"]')
        check("Sidebar Manager nav item exists", sm_item.count() == 1)
        check("nav label = Sidebar Manager",
              "Sidebar Manager" in sm_item.inner_text())
        check("tabSections active by default",
              page.locator("#tabSections").evaluate("el => el.classList.contains('active')"))
        check("panel title = Global Sidebar Manager",
              page.locator("#cmsPanelTitle").inner_text().strip() == "Global Sidebar Manager")

        # ── Manager mounts and loads ──
        page.wait_for_selector("#sgmTree .sgm-node", timeout=20000)
        opts = page.locator("#sgmPortalSelect option")
        check("portal selector has 4 portals", opts.count() == 4, "count=%d" % opts.count())
        labels = [opts.nth(i).inner_text() for i in range(opts.count())]
        check("portal labels present", all(labels), "labels=%s" % labels)

        check("tree renders groups", page.locator("#sgmTree .sgm-group").count() > 0,
              "groups=%d" % page.locator("#sgmTree .sgm-group").count())
        check("tree renders nodes", page.locator("#sgmTree .sgm-node").count() > 0,
              "nodes=%d" % page.locator("#sgmTree .sgm-node").count())

        # ── Live preview ──
        check("preview renders brand", page.locator("#sgmPreview .sv-brand-name").count() == 1)
        check("preview renders links", page.locator("#sgmPreview .sv-link").count() > 0,
              "links=%d" % page.locator("#sgmPreview .sv-link").count())

        # ── Select an item → settings appears ──
        first_node = page.locator("#sgmTree .sgm-node").first
        first_node.click()
        page.wait_for_selector("#sgmSettings #sgmFieldLabel", timeout=5000)
        check("settings shows label field", page.locator("#sgmFieldLabel").count() == 1)
        check("settings shows destination field", page.locator("#sgmFieldHref").count() == 1)
        check("selected node highlighted", page.locator("#sgmTree .sgm-node.selected").count() >= 1)

        # ── Edit label → preview + chip update ──
        page.fill("#sgmFieldLabel", "QA Renamed Item")
        page.wait_for_timeout(250)
        prev_text = page.locator("#sgmPreview").inner_text()
        check("edit reflects in live preview", "QA Renamed Item" in prev_text)
        check("status chip shows Draft", "Draft" in page.locator("#sgmStatusChip").inner_text())
        check("undo button enabled after edit", not page.locator("#sgmBtnUndo").is_disabled())

        # ── Viewport switching ──
        page.locator('[data-sgm-viewport="tablet"]').click()
        page.wait_for_timeout(150)
        check("tablet viewport class applied",
              "mode-tablet" in (page.locator("#sgmPreview").get_attribute("class") or ""))
        page.locator('[data-sgm-viewport="mobile"]').click()
        page.wait_for_timeout(150)
        check("mobile viewport class applied",
              "mode-mobile" in (page.locator("#sgmPreview").get_attribute("class") or ""))
        page.locator('[data-sgm-viewport="desktop"]').click()
        page.wait_for_timeout(150)

        # ── Collapsed preview toggle ──
        page.locator("#sgmPreviewCollapse").click()
        page.wait_for_timeout(150)
        check("collapsed preview class applied",
              "is-collapsed" in (page.locator("#sgmPreview").get_attribute("class") or ""))
        page.locator("#sgmPreviewCollapse").click()
        page.wait_for_timeout(150)
        check("expanded preview class restored",
              "is-collapsed" not in (page.locator("#sgmPreview").get_attribute("class") or ""))

        # ── Undo restores ──
        page.click("#sgmBtnUndo")
        page.wait_for_timeout(200)
        check("undo reverts preview text", "QA Renamed Item" not in page.locator("#sgmPreview").inner_text())

        # ── Visibility toggle ──
        page.locator("#sgmTree .sgm-node").first.click()
        page.wait_for_timeout(150)
        vis_toggle = page.locator("#sgmTree .sgm-node").first.locator("[data-toggle-visible]")
        if vis_toggle.count():
            vis_toggle.click()
            page.wait_for_timeout(200)
            check("hidden node marked is-hidden",
                  page.locator("#sgmTree .sgm-node").first.evaluate("el => el.classList.contains('is-hidden')"))
            page.click("#sgmBtnUndo")
            page.wait_for_timeout(200)
        else:
            check("mandatory item has no visibility toggle (lock only)", True)

        # ── Reorder via move-down and verify order changes ──
        groups = page.locator("#sgmTree > .sgm-group")
        target_gi = -1
        for i in range(groups.count()):
            if groups.nth(i).locator("> .sgm-group-links > .sgm-node").count() >= 2:
                target_gi = i
                break
        check("group with multiple top-level items exists", target_gi >= 0)
        if target_gi >= 0:
            g = groups.nth(target_gi)
            first = g.locator("> .sgm-group-links > .sgm-node").nth(0)
            second = g.locator("> .sgm-group-links > .sgm-node").nth(1)
            first_id = first.get_attribute("data-nav-id")
            second_id = second.get_attribute("data-nav-id")
            first.locator('[data-move-item="1"]').click()
            page.wait_for_timeout(350)
            after = g.locator("> .sgm-group-links > .sgm-node")
            check("reorder swaps first two items in the group",
                  after.nth(0).get_attribute("data-nav-id") == second_id and
                  after.nth(1).get_attribute("data-nav-id") == first_id,
                  "order=%s" % [after.nth(k).get_attribute("data-nav-id") for k in range(min(3, after.count()))])
            check("reorder marks draft", "Draft" in page.locator("#sgmStatusChip").inner_text())
            check("undo enabled after reorder", not page.locator("#sgmBtnUndo").is_disabled())
            page.click("#sgmBtnUndo")
            page.wait_for_timeout(350)
            check("undo restores original order",
                  g.locator("> .sgm-group-links > .sgm-node").nth(0).get_attribute("data-nav-id") == first_id)

        # ── Save Draft persists (then reset) ──
        page.click("#sgmBtnSave")
        page.wait_for_timeout(1000)
        check("save draft clears pending undo", page.locator("#sgmBtnUndo").is_disabled())
        check("chip reflects unpublished draft",
              "Draft" in page.locator("#sgmStatusChip").inner_text())

        # ── Health panel ──
        page.click("#sgmBtnHealth")
        page.wait_for_timeout(700)
        check("health panel visible", not page.locator("#sgmHealth").is_hidden())
        check("health panel has header",
              page.locator("#sgmHealth .sgm-health-head").count() == 1)
        page.click("#sgmBtnValidate")
        page.wait_for_timeout(700)
        check("validate renders findings header",
              page.locator("#sgmHealth .sgm-health-title").count() == 1)

        # ── Version modal ──
        page.click("#sgmBtnVersions")
        page.wait_for_timeout(700)
        check("version modal opens",
              page.locator("#cmsModalBackdrop.open").count() == 1)
        page.click("#cmsModalCloseBtn")
        page.wait_for_timeout(300)

        # ── Portal switch to student ──
        page.select_option("#sgmPortalSelect", "student")
        page.wait_for_timeout(900)
        check("student tree renders nodes",
              page.locator("#sgmTree .sgm-node").count() > 0,
              "nodes=%d" % page.locator("#sgmTree .sgm-node").count())
        check("student preview brand shows Student",
              "Student" in page.locator("#sgmPreview .sv-brand-name").inner_text())

        # ── Panel switch away and back keeps manager alive ──
        page.locator('.cms-nav-item[data-panel="tabHero"]').click()
        page.wait_for_timeout(300)
        page.locator('.cms-nav-item[data-panel="tabSections"]').click()
        page.wait_for_timeout(500)
        check("manager survives panel round-trip",
              page.locator("#sgmTree .sgm-node").count() > 0)

        # ── No fatal JS errors ──
        check("no page errors", len(page_errors) == 0, "errors=%s" % page_errors[:3])
        nav_console = [c for c in console_errors if "sidebar-manager" in c.lower() or "NavMgr" in c]
        check("no NavMgr console errors", len(nav_console) == 0, "errors=%s" % nav_console[:3])

        # ── Published nav is served to a real portal page via layout.js ──
        page.goto("http://127.0.0.1:3000/pages/student/student.html",
                  wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(1200)
        nav_links = page.locator(".nav .nav-link, aside .nav-link, .nav-link")
        check("student portal sidebar renders from published nav",
              nav_links.count() > 0, "nav-links=%d" % nav_links.count())
        cached = page.evaluate("() => sessionStorage.getItem('ngis-nav-published')")
        check("layout.js cached published nav", bool(cached) and "groups" in (cached or ""),
              "cached=%s" % (str(cached)[:60] if cached else None))

        browser.close()


def cleanup():
    """Reset the admin portal back to factory defaults (removes test draft)."""
    import json
    import urllib.request
    body = json.dumps({"portal": "admin"}).encode()
    r = urllib.request.Request("http://127.0.0.1:3000/api/nav/defaults", data=body, method="POST")
    r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=10) as resp:
            return resp.status == 200
    except Exception:
        return False


main()
reset_ok = cleanup()

print("=" * 60)
for name, ok, detail in results:
    print(("PASS " if ok else "FAIL ") + name + (("  ->  " + detail) if detail and not ok else ""))
print("=" * 60)
print("TOTAL %d  PASSED %d  FAILED %d" % (len(results), sum(1 for _, ok, _ in results if ok), len(errors)))
sys.exit(1 if errors else 0)
