import asyncio
from playwright.async_api import async_playwright

PAGES_TO_AUDIT = [
    ("Admin Dashboard", "pages/admin/admin.html", "admin"),
    ("Admin Students", "pages/admin/admin-students.html", "admin"),
    ("Admin Lifecycle", "pages/admin/admin-lifecycle.html", "admin"),
    ("Teacher Dashboard", "pages/teacher/teacher.html", "teacher"),
    ("Teacher Attendance", "pages/teacher/teacher-attendance.html", "teacher"),
    ("Teacher Classes", "pages/teacher/teacher-classes.html", "teacher"),
    ("Teacher Lessons", "pages/teacher/teacher-lessons.html", "teacher"),
    ("Teacher Reports", "pages/teacher/teacher-reports.html", "teacher"),
    ("Teacher Roster", "pages/teacher/teacher-roster.html", "teacher"),
    ("Teacher Gradebook", "pages/teacher/teacher-gradebook.html", "teacher"),
    ("Student Dashboard", "pages/student/student.html", "student"),
    ("Student Services", "pages/student/student-services.html", "student"),
    ("Principal Dashboard", "pages/principal/principal.html", "principal"),
    ("Staff Dashboard", "pages/staff/staff.html", "staff"),
    ("Student Assignments", "pages/student/student-assignments.html", "student"),
    ("Teacher Submissions", "pages/teacher/teacher-submissions.html", "teacher")
]

VIEWPORTS = [
    ("Desktop", 1440, 900),
    ("Tablet", 768, 1024),
    ("Mobile", 390, 844)
]

USER_PROFILES = {
    "admin": {"id": "admin-1", "name": "Sok Panha Heng", "role": "admin", "email": "admin@ngis.edu"},
    "teacher": {"id": "teacher-jenkins", "name": "Dr. Sarah Jenkins", "role": "teacher", "email": "jenkins@ngis.edu"},
    "student": {"id": "student-1", "name": "Vannak Meas", "role": "student", "email": "vannak@student.ngis.edu"},
    "principal": {"id": "princ-1", "name": "H.E. Dr. Chhem Kieth", "role": "principal", "email": "principal@ngis.edu"},
    "staff": {"id": "staff-1", "name": "Chan Sothea", "role": "staff", "email": "sothea@ngis.edu"}
}

async def run_audit():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        total_checks = 0
        passed_checks = 0
        issues = []

        for title, path, role in PAGES_TO_AUDIT:
            print(f"\n=======================================================")
            print(f" AUDITING: {title} ({path}) [Role: {role}]")
            print(f"=======================================================")

            for vp_name, width, height in VIEWPORTS:
                context = await browser.new_context(viewport={"width": width, "height": height})
                profile = USER_PROFILES[role]
                import json
                user_json = json.dumps(profile)
                await context.add_init_script(f"""
                    localStorage.setItem('auth_user', JSON.stringify({user_json}));
                    localStorage.setItem('token', 'fake-jwt-token-{role}');
                    localStorage.setItem('ngis-theme', 'light');
                """)
                page = await context.new_page()
                url = f"http://127.0.0.1:3000/{path}"
                try:
                    await page.goto(url, wait_until="domcontentloaded")
                    await page.wait_for_timeout(300)

                    # 1. Check Visible Top Headers
                    headers_info = await page.evaluate("""
                        () => {
                            const hdrs = Array.from(document.querySelectorAll('header, #heroBanner .hero-topbar, #heroBanner .hero'));
                            return hdrs.filter(h => {
                                const rect = h.getBoundingClientRect();
                                const style = window.getComputedStyle(h);
                                return style.display !== 'none' && style.visibility !== 'hidden' && rect.height > 10 && rect.y < 120;
                            }).map(h => ({
                                tag: h.tagName,
                                id: h.id,
                                className: h.className,
                                height: h.getBoundingClientRect().height
                            }));
                        }
                    """)
                    total_checks += 1
                    # Exactly one top header or zero if chat pane
                    if len(headers_info) <= 1:
                        passed_checks += 1
                    else:
                        issues.append(f"{title} on {vp_name}: Multiple visible top headers ({len(headers_info)})")

                    # 2. Check Horizontal Scroll Overflow
                    overflow_info = await page.evaluate("""
                        () => {
                            const scrollW = document.documentElement.scrollWidth;
                            const innerW = window.innerWidth;
                            return { scrollW, innerW, overflow: scrollW > innerW + 2 };
                        }
                    """)
                    total_checks += 1
                    if not overflow_info['overflow']:
                        passed_checks += 1
                    else:
                        issues.append(f"{title} on {vp_name}: Horizontal overflow ({overflow_info['scrollW']} > {overflow_info['innerW']})")

                    # 3. Check Hamburger on Mobile / Tablet
                    if width <= 1024:
                        total_checks += 1
                        has_hamburger = await page.evaluate("""
                            () => {
                                const btns = Array.from(document.querySelectorAll('[data-action="toggle-sidebar"], .hamburger-btn, .mobile-hamburger-btn'));
                                return btns.some(b => {
                                    const rect = b.getBoundingClientRect();
                                    const style = window.getComputedStyle(b);
                                    return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 15;
                                });
                            }
                        """)
                        if has_hamburger:
                            passed_checks += 1
                        else:
                            issues.append(f"{title} on {vp_name}: Missing visible hamburger button")

                    # 4. Check Strict NO BOLD policy (max font weight <= 500)
                    total_checks += 1
                    bold_elements = await page.evaluate("""
                        () => {
                            const els = Array.from(document.querySelectorAll('h1, h2, h3, h4, th, td, b, strong, .card, .ws-card, [class*="card"]'));
                            let maxWeight = 400;
                            let offender = null;
                            for (const el of els) {
                                const fw = parseInt(window.getComputedStyle(el).fontWeight, 10);
                                if (!isNaN(fw) && fw > maxWeight) {
                                    maxWeight = fw;
                                    offender = el.tagName + '.' + el.className.slice(0, 30);
                                }
                            }
                            return { maxWeight, offender };
                        }
                    """)
                    if bold_elements['maxWeight'] <= 500:
                        passed_checks += 1
                    else:
                        issues.append(f"{title} on {vp_name}: Found font-weight > 500 ({bold_elements['maxWeight']} on {bold_elements['offender']})")

                    print(f"  [{vp_name} {width}x{height}]: Headers: {len(headers_info)}, Overflow: {overflow_info['overflow']}, Max Weight: {bold_elements['maxWeight']}")
                except Exception as e:
                    issues.append(f"{title} on {vp_name}: Load error {str(e)[:60]}")
                finally:
                    await context.close()

        await browser.close()
        print(f"\n=======================================================")
        print(f" AUDIT SUMMARY: {passed_checks} / {total_checks} CHECKS PASSED")
        print(f"=======================================================")
        if issues:
            print("Issues detected:")
            for iss in issues:
                print(f"  - {iss}")
        else:
            print("ALL PAGES AND VIEWPORTS PASSED WITH ZERO ISSUES!")

if __name__ == '__main__':
    asyncio.run(run_audit())

