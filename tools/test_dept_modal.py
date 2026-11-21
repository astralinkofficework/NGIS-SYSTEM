from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://127.0.0.1:3000/pages/student/student.html', wait_until='networkidle')
    
    test_cases = [
        ('timetable', 'Select Department Timetable', 'Weekly Class Schedule'),
        ('assignments', 'Select Department for Coursework', 'Assignments & Tasks'),
        ('results', 'Select Department Academic Results', 'Official Transcripts & Evaluations'),
        ('elearning', 'Select Subject for E-Learning', 'Course Materials & Library')
    ]
    
    for target, exp_title, exp_kicker in test_cases:
        page.evaluate(f"() => openDeptSelectionModal('{target}')")
        title_text = page.locator('#deptModalTitle').inner_text()
        kicker_text = page.locator('#deptModalKicker').inner_text()
        print(f"Target '{target}': title='{title_text}', kicker='{kicker_text}'")
        assert exp_title.lower() in title_text.lower(), f"Expected '{exp_title}' in '{title_text}'"
        assert exp_kicker.lower() in kicker_text.lower(), f"Expected '{exp_kicker}' in '{kicker_text}'"
        page.evaluate("() => closeDeptSelectionModal()")
        page.wait_for_timeout(100)
    
    # Test clicking a department row
    page.evaluate("() => openDeptSelectionModal('timetable')")
    rows = page.locator('.ngis-dept-row')
    row_count = rows.count()
    print(f"Total rows rendered: {row_count}")
    assert row_count == 8, f"Expected 8 rows (1 all + 7 departments), got {row_count}"
    
    # Check row styling
    row_0 = rows.nth(0)
    style = row_0.evaluate("""(el) => {
        const cs = window.getComputedStyle(el);
        return {
            height: cs.height,
            borderRadius: cs.borderRadius,
            border: cs.border,
            bg: cs.backgroundColor
        };
    }""")
    print("Row 0 computed style:", style)
    
    print("SUCCESS: All department modal tests passed!")
    browser.close()
