import os
from playwright.sync_api import sync_playwright

def verify():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # 1. Test student.html
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto('http://127.0.0.1:3000/pages/student/student.html')
        page.wait_for_timeout(1000)
        
        task_tags = page.locator('.workspace-task-tag')
        overdue_pill = page.locator('.workspace-task-overdue-pill')
        print(f"[student.html] .workspace-task-tag count: {task_tags.count()}")
        print(f"[student.html] .workspace-task-overdue-pill count: {overdue_pill.count()}")
        
        assert task_tags.count() == 0, f"Expected 0 .workspace-task-tag, found {task_tags.count()}"
        assert overdue_pill.count() == 0, f"Expected 0 .workspace-task-overdue-pill, found {overdue_pill.count()}"
        
        # Verify status background is transparent
        status_bgs = page.evaluate("""() => {
            const statuses = document.querySelectorAll('.workspace-task-status');
            return Array.from(statuses).map(s => window.getComputedStyle(s).backgroundColor);
        }""")
        print(f"[student.html] Status backgrounds: {set(status_bgs)}")
        for bg in status_bgs:
            assert bg in ['rgba(0, 0, 0, 0)', 'transparent'], f"Non-transparent status bg: {bg}"
            
        tasks_card = page.locator('.workspace-tasks-card')
        tasks_card.screenshot(path='tasks_deadlines_no_badges.png')
        print("Captured tasks_deadlines_no_badges.png")
        page.screenshot(path='student_dashboard_no_badges_desktop.png')
        print("Captured student_dashboard_no_badges_desktop.png")
        
        # 2. Test student-calendar.html
        page.goto('http://127.0.0.1:3000/pages/student/student-calendar.html')
        page.wait_for_timeout(1000)
        
        chip_bgs = page.evaluate("""() => {
            const chips = document.querySelectorAll('.cal-event-chip');
            return Array.from(chips).map(c => ({
                text: c.innerText.trim(),
                bg: window.getComputedStyle(c).backgroundColor,
                border: window.getComputedStyle(c).border
            }));
        }""")
        print(f"[student-calendar.html] Calendar event chips count: {len(chip_bgs)}")
        for c in chip_bgs:
            print(f"  Event: '{c['text'][:30]}...' -> bg: {c['bg']}")
            assert c['bg'] in ['rgba(0, 0, 0, 0)', 'transparent'], f"Event chip has non-transparent bg: {c['bg']}"
            
        page.screenshot(path='student_calendar_no_badges_desktop.png')
        print("Captured student_calendar_no_badges_desktop.png")
        
        browser.close()

if __name__ == '__main__':
    verify()
