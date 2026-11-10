from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    for w in [360, 375, 768, 820, 1024, 1280]:
        page = browser.new_page(viewport={'width': w, 'height': 800})
        page.goto('http://127.0.0.1:3000/pages/principal/principal-classes.html')
        page.wait_for_selector('[data-purpose="filtering-controls"]')
        
        search_box = page.locator('#classSearchInput').bounding_box()
        grade_box = page.locator('#gradeFilter').bounding_box()
        campus_box = page.locator('#campusFilter').bounding_box()
        status_box = page.locator('#statusFilter').bounding_box()
        badge_box = page.locator('#filterStatusCount').bounding_box()
        
        scroll_width = page.evaluate('document.documentElement.scrollWidth')
        client_width = page.evaluate('document.documentElement.clientWidth')
        has_overflow = scroll_width > client_width
        
        print(f"=== Classes @ {w}px ===")
        print(f"  Search: y={search_box['y']:.1f}, w={search_box['width']:.1f}")
        print(f"  Grade: y={grade_box['y']:.1f}, x={grade_box['x']:.1f}, w={grade_box['width']:.1f}")
        print(f"  Campus: y={campus_box['y']:.1f}, x={campus_box['x']:.1f}, w={campus_box['width']:.1f}")
        print(f"  Status: y={status_box['y']:.1f}, x={status_box['x']:.1f}, w={status_box['width']:.1f}")
        print(f"  Badge: y={badge_box['y']:.1f}, x={badge_box['x']:.1f}, w={badge_box['width']:.1f}")
        print(f"  Overflow: {has_overflow} (scrollW={scroll_width}, clientW={client_width})")
        page.close()
    browser.close()

