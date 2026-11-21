import sys
from playwright.sync_api import sync_playwright

test_pages = [
    '/pages/admin/admin.html',
    '/pages/admin/admin-users-students.html',
    '/pages/admin/admin-users-teachers.html',
    '/pages/admin/admin-users-admins.html',
    '/pages/admin/admin-roles-permissions.html',
    '/pages/admin/admin-teacher-profiles.html',
    '/pages/admin/admin-teacher-class-assignment.html',
    '/pages/admin/admin-student-assign.html',
    '/pages/admin/admin-student-verify.html',
    '/pages/admin/admin-teacher-verify.html',
    '/pages/admin/admin-attendance.html',
    '/pages/admin/admin-absence-stats.html',
    '/pages/admin/admin-departments.html',
    '/pages/admin/admin-campuses.html',
    '/pages/admin/admin-classes.html',
    '/pages/admin/admin-timetables.html',
    '/pages/admin/admin-lost-found.html',
    '/pages/admin/admin-security.html'
]

def parse_rgb(s):
    try:
        if s.startswith('rgba'):
            parts = s[5:-1].split(',')
            return [float(p.strip()) for p in parts[:3]]
        elif s.startswith('rgb'):
            parts = s[4:-1].split(',')
            return [float(p.strip()) for p in parts[:3]]
    except:
        pass
    return [0, 0, 0]

def is_too_light(rgb):
    r, g, b = [x/255.0 for x in rgb]
    lum = 0.2126*r + 0.7152*g + 0.0722*b
    return lum > 0.85

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    for tp in test_pages:
        url = 'http://127.0.0.1:3000' + tp
        page.goto(url)
        page.wait_for_load_state('networkidle')
        elements = page.query_selector_all('button, a.btn, [role="button"], input[type="button"], input[type="submit"]')
        issues = []
        for el in elements:
            if not el.is_visible():
                continue
            text = (el.inner_text() or el.get_attribute('aria-label') or el.get_attribute('title') or el.get_attribute('class') or '').strip().replace('\n', ' ')[:25]
            
            cb = el.evaluate('el => window.getComputedStyle(el).color')
            bb = el.evaluate('el => window.getComputedStyle(el).backgroundColor')
            
            try:
                el.hover(timeout=300)
                page.wait_for_timeout(20)
            except:
                continue
            ca = el.evaluate('el => window.getComputedStyle(el).color')
            ba = el.evaluate('el => window.getComputedStyle(el).backgroundColor')
            oa = el.evaluate('el => window.getComputedStyle(el).opacity')
            
            rgb_c = parse_rgb(ca)
            rgb_b = parse_rgb(ba)
            
            if is_too_light(rgb_c) and (ba in ['rgba(0, 0, 0, 0)', 'transparent'] or is_too_light(rgb_b)):
                page_bg = page.evaluate('() => window.getComputedStyle(document.body).backgroundColor')
                if not is_too_light(parse_rgb(page_bg)):
                    pass
                else:
                    issues.append(f"Button '{text}': text={ca}, bg={ba}")
            elif ca == ba and ba not in ['rgba(0, 0, 0, 0)', 'transparent']:
                issues.append(f"Button '{text}' text matches bg: {ca}")
            elif oa == '0':
                issues.append(f"Button '{text}' opacity 0")
        
        if issues:
            print(f"[!] {tp}: {len(issues)} hover issues found!")
            for iss in issues[:5]:
                print(f"    - {iss}")
        else:
            print(f"[OK] {tp} (checked {len(elements)} clickable elements)")
        sys.stdout.flush()
    browser.close()
