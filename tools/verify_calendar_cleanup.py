import os
from playwright.sync_api import sync_playwright

def verify():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # 1. Student Calendar
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto('http://127.0.0.1:3000/pages/student/student-calendar.html')
        page.wait_for_timeout(1000)
        
        # Check removed elements
        tt_btn = page.locator('a[href*="student-timetable.html"]:has-text("View Class Timetable")')
        grade_term = page.locator('span:has-text("Grade 10 · Term 2")')
        academic_year_p = page.locator('p:has-text("Academic Year 2025–2026 · Official term dates")')
        filter_chips = page.locator('.cal-filter-chips')
        
        print(f"View Class Timetable button count: {tt_btn.count()}")
        print(f"Grade 10 · Term 2 pill count: {grade_term.count()}")
        print(f"Academic Year 2025–2026 p count: {academic_year_p.count()}")
        print(f"Filter chips count in DOM: {filter_chips.count()}")
        
        assert tt_btn.count() == 0, "Expected 0 timetable buttons, found some!"
        assert grade_term.count() == 0, "Expected 0 Grade 10 · Term 2 pills, found some!"
        assert academic_year_p.count() == 0, "Expected 0 academic year descriptions, found some!"
        assert filter_chips.count() == 0, "Expected 0 filter chips in student calendar, found some!"
        
        # Verify calendar grid is active and rendered
        cal_grid = page.locator('.cal-month-grid')
        print(f"Calendar month grid present: {cal_grid.count() == 1}")
        assert cal_grid.count() == 1, "Calendar grid is missing!"
        
        page.screenshot(path='student_calendar_cleaned_desktop.png', full_page=True)
        print("Captured student_calendar_cleaned_desktop.png")
        
        # Mobile view
        page.set_viewport_size({'width': 390, 'height': 844})
        page.wait_for_timeout(500)
        hamb = page.locator('[data-action="toggle-sidebar"]')
        print(f"Mobile hamburger menu button: {hamb.count() > 0}")
        assert hamb.count() > 0, "Mobile hamburger button missing!"
        page.screenshot(path='student_calendar_cleaned_mobile.png')
        print("Captured student_calendar_cleaned_mobile.png")
        
        # 2. Check Admin Calendar (make sure filter chips are NOT broken on Admin/Principal)
        page.set_viewport_size({'width': 1440, 'height': 900})
        page.goto('http://127.0.0.1:3000/pages/admin/admin-calendar.html')
        page.wait_for_timeout(1000)
        admin_chips = page.locator('.cal-filter-chips')
        print(f"Admin calendar filter chips preserved: {admin_chips.count() == 1}")
        assert admin_chips.count() == 1, "Admin calendar filter chips broken!"
        
        browser.close()

if __name__ == '__main__':
    verify()
