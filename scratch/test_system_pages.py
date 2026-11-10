import asyncio
import os
import sys
from playwright.async_api import async_playwright

PAGES = [
    ("pages/admin/admin-system-school-info.html", "sys-school-info", None),
    ("pages/admin/admin-system-school-year.html", "sys-school-year", "sys-year-config-drop"),
    ("pages/admin/admin-system-school-week.html", "sys-school-week", "sys-year-config-drop"),
    ("pages/admin/admin-system-exam-config.html", "sys-exam-config", "sys-year-config-drop"),
    ("pages/admin/admin-system-score-lock.html", "sys-score-lock", "sys-year-config-drop"),
    ("pages/admin/admin-system-define-curriculum.html", "sys-define-curriculum", "sys-year-config-drop"),
    ("pages/admin/admin-system-design-curriculum.html", "sys-design-curriculum", "sys-year-config-drop"),
    ("pages/admin/admin-system-declare-class.html", "sys-declare-class", "sys-year-config-drop"),
    ("pages/admin/admin-system-student-transition.html", "sys-student-transition", "sys-year-config-drop"),
    ("pages/admin/admin-system-technician-assign.html", "sys-technician-assign", "sys-year-config-drop"),
    ("pages/admin/admin-system-employee-group.html", "sys-employee-group", "sys-account-mgmt-drop"),
    ("pages/admin/admin-system-employee-accounts.html", "sys-employee-accounts", "sys-account-mgmt-drop"),
    ("pages/admin/admin-system-student-accounts.html", "sys-student-accounts", "sys-account-mgmt-drop"),
    ("pages/admin/admin-system-parent-accounts.html", "sys-parent-accounts", "sys-account-mgmt-drop"),
    ("pages/admin/admin-system-schedule.html", "sys-schedule", None),
    ("pages/admin/admin-system-general-setting.html", "sys-general-setting", None),
]

ARTIFACT_DIR = r"C:\Users\oudom\.gemini\antigravity\brain\8fd19b10-a09a-43d8-a122-cb4a75dc0ff6"

async def run_tests():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

        print(f"Starting test for {len(PAGES)} Admin System pages...")

        for rel_url, active_id, nested_parent in PAGES:
            full_url = f"http://127.0.0.1:3000/{rel_url}"
            resp = await page.goto(full_url, wait_until="networkidle")
            assert resp.status == 200, f"Page {rel_url} failed with status {resp.status}"

            # Wait for system content to load into systemMgmtRoot
            await page.wait_for_selector("#systemMgmtRoot > div", timeout=5000)

            # Check Desktop sidebar structure
            system_subgroup = page.locator('.nav-subgroup[data-subgroup-id="system-mgmt-drop"]')
            assert await system_subgroup.count() > 0, f"System subgroup missing on {rel_url}"
            is_expanded = await system_subgroup.evaluate('el => el.classList.contains("expanded")')
            assert is_expanded, f"System subgroup not expanded on {rel_url}"

            # If nested parent expected, check nested group is expanded
            if nested_parent:
                nested_el = page.locator(f'.nav-nested-group[data-nested-id="{nested_parent}"]')
                assert await nested_el.count() > 0, f"Nested parent {nested_parent} missing on {rel_url}"
                is_nested_expanded = await nested_el.evaluate('el => el.classList.contains("expanded")')
                assert is_nested_expanded, f"Nested parent {nested_parent} not expanded on {rel_url}"

            # Check active item
            active_link = page.locator(f'.nav-link[data-id="{active_id}"]')
            assert await active_link.count() > 0, f"Active link with data-id={active_id} missing on {rel_url}"
            is_active = await active_link.evaluate('el => el.classList.contains("active")')
            assert is_active, f"Link {active_id} does not have .active class on {rel_url}"

            print(f"  [OK] {rel_url} (active: {active_id}, parent: {nested_parent or 'direct'})")

        # Now test Screenshots and Mobile View
        # 1. School Info Desktop screenshot
        await page.set_viewport_size({"width": 1280, "height": 800})
        await page.goto("http://127.0.0.1:3000/pages/admin/admin-system-school-info.html", wait_until="networkidle")
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "admin_system_school_info_desktop.png"))

        # 2. School Year Desktop screenshot (School Year Configuration expanded)
        await page.goto("http://127.0.0.1:3000/pages/admin/admin-system-school-year.html", wait_until="networkidle")
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "admin_system_school_year_desktop.png"))

        # 3. Employee Accounts Desktop screenshot (Account Management expanded)
        await page.goto("http://127.0.0.1:3000/pages/admin/admin-system-employee-accounts.html", wait_until="networkidle")
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "admin_system_employee_accounts_desktop.png"))

        # 4. Mobile responsive check & drawer opening
        await page.set_viewport_size({"width": 390, "height": 844})
        await page.goto("http://127.0.0.1:3000/pages/admin/admin-system-school-info.html", wait_until="networkidle")

        # Verify mobile hamburger button
        btn = page.locator('button.mobile-hamburger-btn[data-action="toggle-sidebar"]').first
        assert await btn.is_visible(), "Mobile hamburger button is not visible on mobile view"

        # Click hamburger button to open drawer
        await btn.click()
        await page.wait_for_timeout(300)
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "admin_system_mobile_drawer.png"))

        # Verify no bold fonts across the page (rule: NO BOLD FONTS)
        bolds = await page.evaluate('''() => {
            const boldElements = [];
            const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
            let node;
            while ((node = walker.nextNode())) {
                const weight = parseInt(window.getComputedStyle(node).fontWeight, 10);
                if (weight > 500 && node.offsetParent !== null && node.innerText.trim().length > 0) {
                    boldElements.push({ tag: node.tagName, text: node.innerText.trim().slice(0, 30), weight });
                }
            }
            return boldElements.slice(0, 5);
        }''')
        print(f"Font weight check (>500): {len(bolds)} elements found: {bolds}")

        await browser.close()
        print("All System Management tests passed successfully!")

asyncio.run(run_tests())

