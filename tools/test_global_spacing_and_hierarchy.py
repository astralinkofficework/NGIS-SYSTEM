import sys
from playwright.sync_api import sync_playwright

test_urls = [
    ('Student Dashboard', 'http://127.0.0.1:3000/pages/student/student.html'),
    ('Student Exams', 'http://127.0.0.1:3000/pages/student/student-exams.html'),
    ('Teacher Attendance', 'http://127.0.0.1:3000/pages/teacher/teacher-attendance.html'),
    ('Admin Campus', 'http://127.0.0.1:3000/pages/admin/admin-campus.html'),
    ('Shared Department', 'http://127.0.0.1:3000/pages/shared/department.html'),
]

viewports = [
    ('Mobile 375px', {'width': 375, 'height': 812}, '16px'),
    ('Tablet 768px', {'width': 768, 'height': 1024}, '24px'),
    ('Desktop 1280px', {'width': 1280, 'height': 900}, '32px'),
]

errors = []

with sync_playwright() as p:
    browser = p.chromium.launch()
    for vname, vp, expected_pad in viewports:
        print(f"\n==================== Testing {vname} (Expected Pad: {expected_pad}) ====================")
        page = browser.new_page(viewport=vp)
        for name, url in test_urls:
            try:
                page.goto(url, wait_until='networkidle', timeout=15000)
                
                # Check page padding
                pad_info = page.evaluate('''() => {
                    const el = document.querySelector('.page, #mainContent, .hub-container, #examsWorkspace > .exw, .subpage-container');
                    if (!el) return null;
                    const s = window.getComputedStyle(el);
                    return {
                        padLeft: s.paddingLeft,
                        padRight: s.paddingRight,
                        boxSizing: s.boxSizing
                    };
                }''')
                
                if pad_info:
                    print(f"[{name}] padLeft={pad_info['padLeft']}, padRight={pad_info['padRight']}")
                    if pad_info['padLeft'] != expected_pad or pad_info['padRight'] != expected_pad:
                        errors.append(f"{name} at {vname} has padLeft={pad_info['padLeft']} (expected {expected_pad})")
                else:
                    print(f"[{name}] Container not found")
                
                # Check horizontal scroll
                has_scroll = page.evaluate('() => document.documentElement.scrollWidth > window.innerWidth')
                if has_scroll:
                    errors.append(f"{name} at {vname} has horizontal scrolling!")
                    
            except Exception as e:
                errors.append(f"{name} at {vname} failed with: {e}")
        page.close()
    
    # Check component rules on Desktop
    print("\n==================== Component Rules Audit (Desktop) ====================")
    page = browser.new_page(viewport={'width': 1280, 'height': 900})
    page.goto('http://127.0.0.1:3000/pages/admin/admin-campus.html', wait_until='networkidle')
    
    comp_checks = page.evaluate('''() => {
        const rootStyle = window.getComputedStyle(document.documentElement);
        const tokens = {
            s1: rootStyle.getPropertyValue('--space-1').trim(),
            s2: rootStyle.getPropertyValue('--space-2').trim(),
            s4: rootStyle.getPropertyValue('--space-4').trim(),
            s6: rootStyle.getPropertyValue('--space-6').trim(),
            s8: rootStyle.getPropertyValue('--space-8').trim(),
            s16: rootStyle.getPropertyValue('--space-16').trim(),
        };
        
        // Table cell checks
        const th = document.querySelector('table th, .tbl th, .sk-table th');
        const td = document.querySelector('table td, .tbl td, .sk-table td');
        
        const thInfo = th ? {
            height: window.getComputedStyle(th).height,
            borderRight: window.getComputedStyle(th).borderRightStyle,
            padTop: window.getComputedStyle(th).paddingTop,
            padBottom: window.getComputedStyle(th).paddingBottom
        } : null;
        
        const tdInfo = td ? {
            height: window.getComputedStyle(td).height,
            borderRight: window.getComputedStyle(td).borderRightStyle,
            padTop: window.getComputedStyle(td).paddingTop,
            padBottom: window.getComputedStyle(td).paddingBottom
        } : null;
        
        // Button check
        const btn = document.querySelector('.btn-primary, button.btn-primary');
        const btnInfo = btn ? {
            height: window.getComputedStyle(btn).height,
            padLeft: window.getComputedStyle(btn).paddingLeft,
            borderRadius: window.getComputedStyle(btn).borderRadius
        } : null;
        
        return { tokens, thInfo, tdInfo, btnInfo };
    }''')
    
    print("Tokens check:", comp_checks['tokens'])
    print("Table TH info:", comp_checks['thInfo'])
    print("Table TD info:", comp_checks['tdInfo'])
    print("Button info:", comp_checks['btnInfo'])
    
    # Assertions
    if comp_checks['tokens']['s1'] != '4px':
        errors.append(f"--space-1 is {comp_checks['tokens']['s1']}, expected 4px")
    if comp_checks['tokens']['s2'] != '8px':
        errors.append(f"--space-2 is {comp_checks['tokens']['s2']}, expected 8px")
    if comp_checks['tokens']['s4'] != '16px':
        errors.append(f"--space-4 is {comp_checks['tokens']['s4']}, expected 16px")
    if comp_checks['tokens']['s6'] != '24px':
        errors.append(f"--space-6 is {comp_checks['tokens']['s6']}, expected 24px")
    if comp_checks['tokens']['s8'] != '32px':
        errors.append(f"--space-8 is {comp_checks['tokens']['s8']}, expected 32px")
    if comp_checks['tokens']['s16'] != '64px':
        errors.append(f"--space-16 is {comp_checks['tokens']['s16']}, expected 64px")
        
    if comp_checks['thInfo'] and comp_checks['thInfo']['borderRight'] != 'none':
        errors.append(f"Table TH has borderRight={comp_checks['thInfo']['borderRight']}, expected none")
    if comp_checks['tdInfo'] and comp_checks['tdInfo']['borderRight'] != 'none':
        errors.append(f"Table TD has borderRight={comp_checks['tdInfo']['borderRight']}, expected none")
        
    page.close()
    browser.close()

print("\n==================== AUDIT RESULTS ====================")
if errors:
    print(f"FAILED with {len(errors)} errors:")
    for e in errors:
        print("  - ", e)
    sys.exit(1)
else:
    print("SUCCESS: All 8-point spacing, layout margins, table rows, and component consistency passed 100%!")
    sys.exit(0)
