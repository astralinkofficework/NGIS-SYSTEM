from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    for w in [360, 375, 414, 768, 820, 1024]:
        page = browser.new_page(viewport={'width': w, 'height': 800})
        page.goto('http://127.0.0.1:3000/pages/principal/principal-departments.html')
        page.wait_for_selector('[data-purpose="filtering-controls"]')
        
        search_box = page.locator('#deptSearchInput').bounding_box()
        status_box = page.locator('#statusFilter').bounding_box()
        comp_box = page.locator('#complianceFilter').bounding_box()
        reset_box = page.locator('button:has-text("Reset")').bounding_box()
        badge_box = page.locator('#deptFilterBadge').bounding_box()
        
        print(f"=== Width: {w}px ===")
        print(f"  Search: y={search_box['y']:.1f}, w={search_box['width']:.1f}")
        print(f"  Status: y={status_box['y']:.1f}, x={status_box['x']:.1f}, w={status_box['width']:.1f}")
        print(f"  Compliance: y={comp_box['y']:.1f}, x={comp_box['x']:.1f}, w={comp_box['width']:.1f}")
        print(f"  Reset: y={reset_box['y']:.1f}, x={reset_box['x']:.1f}, w={reset_box['width']:.1f}")
        print(f"  Badge: y={badge_box['y']:.1f}, x={badge_box['x']:.1f}, w={badge_box['width']:.1f}")
        page.close()
    browser.close()
