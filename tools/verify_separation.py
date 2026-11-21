import os
from playwright.sync_api import sync_playwright

def full_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # 1. student-calendar.html (Desktop)
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto('http://127.0.0.1:3000/pages/student/student-calendar.html')
        page.wait_for_timeout(1000)
        
        cal_sidebar = page.locator(".nav-group a[href*='student-calendar.html']")
        tt_sidebar = page.locator(".nav-group a[href*='student-timetable.html']")
        cal_app = page.locator('#academicCalendarApp')
        wktt_card = page.locator('#wkttCard')
        
        print(f"[Calendar Desktop] In sidebar -> Calendar: {cal_sidebar.count()}, Timetable: {tt_sidebar.count()}")
        print(f"[Calendar Desktop] Active class on calendar link: {'active' in (cal_sidebar.first.get_attribute('class') or '')}")
        print(f"[Calendar Desktop] Academic Calendar widget present: {cal_app.count() == 1}")
        print(f"[Calendar Desktop] Timetable card absent: {wktt_card.count() == 0}")
        
        page.screenshot(path='student_calendar_separate_desktop.png', full_page=True)
        
        # 2. student-calendar.html (Mobile 390px)
        page.set_viewport_size({'width': 390, 'height': 844})
        page.wait_for_timeout(500)
        hamb = page.locator('[data-action="toggle-sidebar"]')
        print(f"[Calendar Mobile] Hamburger menu button present: {hamb.count() > 0}")
        page.screenshot(path='student_calendar_separate_mobile.png')
        
        # 3. student-timetable.html (Desktop)
        page.set_viewport_size({'width': 1440, 'height': 900})
        page.goto('http://127.0.0.1:3000/pages/student/student-timetable.html')
        page.wait_for_timeout(1000)
        
        cal_sidebar_tt = page.locator(".nav-group a[href*='student-calendar.html']")
        tt_sidebar_tt = page.locator(".nav-group a[href*='student-timetable.html']")
        wktt_card_tt = page.locator('#wkttCard')
        cal_app_tt = page.locator('#academicCalendarApp')
        
        print(f"[Timetable Desktop] In sidebar -> Calendar: {cal_sidebar_tt.count()}, Timetable: {tt_sidebar_tt.count()}")
        print(f"[Timetable Desktop] Active class on timetable link: {'active' in (tt_sidebar_tt.first.get_attribute('class') or '')}")
        print(f"[Timetable Desktop] Timetable card present: {wktt_card_tt.count() == 1}")
        print(f"[Timetable Desktop] Academic Calendar widget absent: {cal_app_tt.count() == 0}")
        
        page.screenshot(path='student_timetable_separate_desktop.png', full_page=True)
        
        # 4. Reverted department.html (Desktop)
        page.goto('http://127.0.0.1:3000/pages/shared/department.html?id=english&portal=student')
        page.wait_for_timeout(1000)
        
        grid = page.locator('#hubCardsGrid')
        cards = page.locator('#hubCardsGrid .hub-card')
        print(f"[Department Hub English] #hubCardsGrid present: {grid.count() == 1}")
        print(f"[Department Hub English] 6 hub cards present: {cards.count() == 6}")
        
        page.screenshot(path='department_english_reverted.png', full_page=True)
        
        browser.close()

if __name__ == '__main__':
    full_verification()
