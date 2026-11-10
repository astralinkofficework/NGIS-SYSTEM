from playwright.sync_api import sync_playwright

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # Test 1: Desktop 1440px
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto('http://127.0.0.1:3000/pages/principal/principal-classes.html')
        page.wait_for_timeout(1000)
        
        # Capture full page view
        page.screenshot(path='scratch/classes_1440_full.png')
        
        # Capture telemetry cards & filter section
        page.locator('section[data-purpose="metrics-telemetry"]').screenshot(path='scratch/classes_cards_1440.png')
        page.locator('section[data-purpose="filtering-controls"]').screenshot(path='scratch/classes_filter_1440.png')
        
        # Check alignment of filters on desktop
        grade_box = page.locator('#gradeFilter').bounding_box()
        campus_box = page.locator('#campusFilter').bounding_box()
        status_box = page.locator('#statusFilter').bounding_box()
        print(f"Desktop 1440 - Grade Y: {grade_box['y']}, Campus Y: {campus_box['y']}, Status Y: {status_box['y']}")
        assert abs(grade_box['y'] - campus_box['y']) < 5, "Dropdowns must be aligned horizontally on desktop"
        assert abs(campus_box['y'] - status_box['y']) < 5, "Dropdowns must be aligned horizontally on desktop"
        
        # Open Edit Modal on Desktop
        page.locator("button:has-text('Edit')").first.click()
        page.wait_for_timeout(500)
        page.screenshot(path='scratch/edit_modal_desktop.png')
        page.locator('#editClassModal .w-full.max-w-2xl').screenshot(path='scratch/edit_modal_card_desktop.png')
        
        # Close Edit Modal
        page.locator('#editClassModal button:has-text("Cancel")').click()
        page.wait_for_timeout(300)
        
        # Open Students Modal on Desktop
        page.locator("button:has-text('View')").first.click()
        page.wait_for_timeout(500)
        page.screenshot(path='scratch/students_modal_desktop.png')
        page.locator('#classStudentsModal button:has-text("Done")').click()
        page.wait_for_timeout(300)
        page.close()
        
        # Test 2: Mobile 375px
        page_m = browser.new_page(viewport={'width': 375, 'height': 812})
        page_m.goto('http://127.0.0.1:3000/pages/principal/principal-classes.html')
        page_m.wait_for_timeout(1000)
        
        page_m.screenshot(path='scratch/classes_375_full.png')
        page_m.locator('section[data-purpose="filtering-controls"]').screenshot(path='scratch/classes_filter_375.png')
        
        # Open Edit Modal on Mobile
        page_m.evaluate("openEditModal('cls-10a')")
        page_m.wait_for_timeout(500)
        page_m.screenshot(path='scratch/edit_modal_mobile.png')
        
        page_m.close()
        browser.close()
        print("All tests and screenshots generated successfully!")

if __name__ == '__main__':
    test()

