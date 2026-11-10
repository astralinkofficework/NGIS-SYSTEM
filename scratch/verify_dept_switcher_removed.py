from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1400, 'height': 900})
    errors = []
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)

    page.goto("http://127.0.0.1:3000/pages/principal/principal-departments.html", wait_until="networkidle")
    print("Page Title:", page.title())

    # Check that switcher is gone
    btn_table = page.locator("#btnViewTable").count()
    btn_grid = page.locator("#btnViewGrid").count()
    print("btnViewTable count:", btn_table)
    print("btnViewGrid count:", btn_grid)
    assert btn_table == 0, "btnViewTable should be removed"
    assert btn_grid == 0, "btnViewGrid should be removed"

    # Verify table renders
    rows = page.locator("#departmentsTableBody tr").count()
    print("Department table rows:", rows)
    assert rows > 0, "Department table should render rows"

    # Screenshot
    page.screenshot(path="C:/Users/oudom/.gemini/antigravity/brain/8fd19b10-a09a-43d8-a122-cb4a75dc0ff6/departments_no_switcher.png")
    print("Screenshot saved!")

    assert len(errors) == 0, f"Console errors found: {errors}"
    browser.close()
    print("Verification passed!")

