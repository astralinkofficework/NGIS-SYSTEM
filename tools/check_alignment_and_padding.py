from playwright.sync_api import sync_playwright

test_urls = [
    ('Student Dashboard', 'http://127.0.0.1:3000/pages/student/student.html'),
    ('Teacher Attendance', 'http://127.0.0.1:3000/pages/teacher/teacher-attendance.html'),
    ('Admin Campus', 'http://127.0.0.1:3000/pages/admin/admin-campus.html'),
    ('Shared Department', 'http://127.0.0.1:3000/pages/shared/department.html'),
    ('Student Exams', 'http://127.0.0.1:3000/pages/student/student-exams.html'),
]

viewports = [
    ('Mobile 375px', {'width': 375, 'height': 812}),
    ('Tablet 768px', {'width': 768, 'height': 1024}),
    ('Desktop 1280px', {'width': 1280, 'height': 900}),
    ('Wide 1920px', {'width': 1920, 'height': 1080})
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for vname, vp in viewports:
        print(f"\n==================== {vname} ====================")
        page = browser.new_page(viewport=vp)
        for name, url in test_urls:
            try:
                page.goto(url, wait_until='networkidle', timeout=15000)
                # Check page padding
                info = page.evaluate('''() => {
                    const main = document.querySelector('main.main, main');
                    const pageEl = document.querySelector('.page, #mainContent, .hub-container, #examsWorkspace, .workspace');
                    const hero = document.getElementById('heroBanner');
                    
                    const getP = (el) => el ? {
                        padLeft: window.getComputedStyle(el).paddingLeft,
                        padRight: window.getComputedStyle(el).paddingRight,
                        padTop: window.getComputedStyle(el).paddingTop,
                        padBottom: window.getComputedStyle(el).paddingBottom,
                        marginLeft: window.getComputedStyle(el).marginLeft,
                        marginRight: window.getComputedStyle(el).marginRight,
                        width: el.getBoundingClientRect().width,
                        x: el.getBoundingClientRect().x
                    } : null;
                    
                    return {
                        main: getP(main),
                        page: getP(pageEl),
                        hero: getP(hero),
                        hasHorizScroll: document.documentElement.scrollWidth > window.innerWidth
                    };
                }''')
                print(f"[{name}]")
                if info['hero']:
                    print(f"  Hero: x={info['hero']['x']:.1f}, padL={info['hero']['padLeft']}, padR={info['hero']['padRight']}")
                if info['page']:
                    print(f"  Page: x={info['page']['x']:.1f}, padL={info['page']['padLeft']}, padR={info['page']['padRight']}")
                print(f"  Horizontal scroll detected: {info['hasHorizScroll']}")
            except Exception as e:
                print(f"[{name}] Error: {e}")
        page.close()
    browser.close()
