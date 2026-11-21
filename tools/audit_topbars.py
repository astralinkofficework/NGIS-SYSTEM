import os
from playwright.sync_api import sync_playwright

test_urls = [
    ("admin_dash", "http://127.0.0.1:3000/pages/admin/admin.html"),
    ("admin_sec", "http://127.0.0.1:3000/pages/admin/admin-security.html"),
    ("admin_assign", "http://127.0.0.1:3000/pages/admin/admin-student-assign.html"),
    ("teacher_dash", "http://127.0.0.1:3000/pages/teacher/teacher.html"),
    ("teacher_att", "http://127.0.0.1:3000/pages/teacher/teacher-attendance.html"),
    ("teacher_rep", "http://127.0.0.1:3000/pages/teacher/teacher-reports.html"),
    ("student_dash", "http://127.0.0.1:3000/pages/student/student.html"),
    ("student_att", "http://127.0.0.1:3000/pages/student/student-attendance.html"),
    ("principal_dash", "http://127.0.0.1:3000/pages/principal/principal.html"),
    ("shared_ann", "http://127.0.0.1:3000/pages/shared/announcements.html"),
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 900})

    for name, url in test_urls:
        try:
            page.goto(url, wait_until="networkidle")
            page.wait_for_timeout(400)

            hero_info = page.evaluate("""() => {
                const hero = document.querySelector('.hero, #heroBanner, header[role="banner"]');
                const topbar = document.querySelector('.hero-topbar, .topbar, .navbar, .mobile-appbar');
                const bodyBg = window.getComputedStyle(document.body).backgroundColor;
                const htmlBg = window.getComputedStyle(document.documentElement).backgroundColor;
                
                let heroBg = hero ? window.getComputedStyle(hero).backgroundColor : null;
                let topbarBg = topbar ? window.getComputedStyle(topbar).backgroundColor : null;
                let heroBoxShadow = hero ? window.getComputedStyle(hero).boxShadow : null;
                let topbarBorder = topbar ? window.getComputedStyle(topbar).borderBottom : null;
                let isSticky = topbar ? window.getComputedStyle(topbar).position : null;
                let heroSticky = hero ? window.getComputedStyle(hero).position : null;
                
                let icons = [];
                if (topbar) {
                    const iconEls = topbar.querySelectorAll('.mi, [data-ngis-icon], i, svg');
                    iconEls.forEach(el => {
                        const style = window.getComputedStyle(el);
                        const rect = el.getBoundingClientRect();
                        const tag = el.tagName;
                        const iconAttr = el.getAttribute('data-ngis-icon') || el.className;
                        const hasSvg = el.querySelector('svg') !== null || tag.toLowerCase() === 'svg';
                        const text = (el.innerText || el.textContent || '').trim();
                        icons.push({
                            tag, iconAttr, text: text.substring(0, 15),
                            width: Math.round(rect.width), height: Math.round(rect.height),
                            visible: style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0' && rect.width > 0,
                            color: style.color,
                            hasSvg
                        });
                    });
                }
                
                let badges = [];
                if (topbar) {
                    const badgeEls = topbar.querySelectorAll('.htb-ctrl-badge, [class*="badge"]');
                    badgeEls.forEach(b => {
                        const r = b.getBoundingClientRect();
                        badges.push({ text: (b.innerText || b.textContent || '').trim(), w: Math.round(r.width), h: Math.round(r.height), x: Math.round(r.x), y: Math.round(r.y) });
                    });
                }

                return {
                    bodyBg, htmlBg, heroBg, topbarBg, heroBoxShadow, topbarBorder, isSticky, heroSticky,
                    iconsCount: icons.length,
                    iconsSample: icons.slice(0, 8),
                    badges
                };
            }""")
            print(f"\n=== {name} ({url}) ===")
            print(f"  Body BG: {hero_info['bodyBg']} | Topbar BG: {hero_info['topbarBg']} | Hero BG: {hero_info['heroBg']}")
            print(f"  Sticky: topbar={hero_info['isSticky']} / hero={hero_info['heroSticky']}")
            print(f"  Topbar Border: {hero_info['topbarBorder']} | Shadow: {hero_info['heroBoxShadow']}")
            print(f"  Badges: {hero_info['badges']}")
            print(f"  Icons ({hero_info['iconsCount']}):")
            for ic in hero_info['iconsSample']:
                print(f"    - {ic['tag']} [{ic['iconAttr']}]: text='{ic['text']}', {ic['width']}x{ic['height']}, vis={ic['visible']}, hasSvg={ic['hasSvg']}, color={ic['color']}")

            os.makedirs("tools/screenshots", exist_ok=True)
            page.screenshot(path=f"tools/screenshots/{name}.png")
        except Exception as e:
            print(f"Error on {name}: {e}")

    browser.close()
