import asyncio
import os
import json
from playwright.async_api import async_playwright

PAGES_TO_AUDIT = [
    ("Admin Departments", "pages/admin/admin-departments.html", "#deptSearch", "admin", None),
    ("Principal Departments", "pages/principal/principal-departments.html", "#deptSearchInput", "principal", None),
    ("Admin Classes", "pages/admin/admin-classes.html", "#classSearchInput", "admin", None),
    ("Admin Services", "pages/admin/admin-services.html", "#svSearch", "admin", None),
    ("Admin Campuses", "pages/admin/admin-campuses.html", "#campusSearch", "admin", None),
    ("Admin Attendance", "pages/admin/admin-attendance.html", "#searchFilter", "admin", None),
    ("Admin Absence Stats", "pages/admin/admin-absence-stats.html", "#tableSearchInput", "admin", None),
    ("Admin Lost & Found", "pages/admin/admin-lost-found.html", "#lfSearch", "admin", None),
    ("Admin News", "pages/admin/admin-news.html", "#tableSearchInput", "admin", None),
    ("Admin Timetables", "pages/admin/admin-timetables.html", "#monSearch", "admin", None),
    ("Admin Assignments", "pages/admin/admin-assignments.html", ".toolbar input", "admin", None),
    ("Admin Grades", "pages/admin/admin-grades.html", "#searchGrades", "admin", None),
    ("Admin Security", "pages/admin/admin-security.html", "#usSearch", "admin", "button[data-tab='users']"),
    ("Teacher Lessons", "pages/teacher/teacher-lessons.html", "#lessonSearch", "teacher", None),
    ("Teacher Roster", "pages/teacher/teacher-roster.html", "#rosterSearchInput", "teacher", None),
    ("Teacher Gradebook", "pages/teacher/teacher-gradebook.html", "#searchStudentInput", "teacher", None),
    ("Teacher Reports", "pages/teacher/teacher-reports.html", "#searchReportInput", "teacher", None),
    ("Teacher Submissions", "pages/teacher/teacher-submissions.html", "#searchStudent", "teacher", None),
    ("Student Assignments", "pages/student/student-assignments.html", "#asgnSearch", "student", None),
    ("Shared Departments", "pages/shared/departments.html", "#dept-search", "student", None),
    ("Shared Lessons", "pages/shared/lessons.html", "#oakFilterInput", "student", None),
    ("Shared Announcements", "pages/shared/announcements.html", "#annSearch", "student", None),
    ("Shared News", "pages/shared/news.html", "#newsSearchInput", "student", None),
    ("Master Directory", "pages-directory.html", "#dirSearchInput", "admin", None),
    ("Admin Topbar", "pages/admin/admin.html", ".htb-search-input, .search input", "admin", None),
    ("Teacher Topbar", "pages/teacher/teacher.html", ".htb-search-input, .search input", "teacher", None),
    ("Student Topbar", "pages/student/student.html", ".htb-search-input, .search input", "student", None),
    ("Principal Topbar", "pages/principal/principal.html", ".htb-search-input, .search input", "principal", None)
]

VIEWPORTS = [
    ("Desktop", 1440, 900),
    ("Tablet", 768, 1024),
    ("Mobile", 375, 667)
]

async def run_audit():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        results = []
        total_tests = 0
        passed_tests = 0

        for title, path, selector, role, tab_btn in PAGES_TO_AUDIT:
            for vp_name, w, h in VIEWPORTS:
                # Topbars are intentionally hidden on mobile (<=768px) per NGIS responsive spec
                if "Topbar" in title and w <= 768:
                    continue

                total_tests += 1
                context = await browser.new_context(viewport={"width": w, "height": h})
                profile = {"id": f"{role}-1", "name": f"Auditor {role}", "role": role, "email": f"{role}@ngis.edu"}
                user_json = json.dumps(profile)
                await context.add_init_script(f"""
                    localStorage.setItem('auth_user', JSON.stringify({user_json}));
                    localStorage.setItem('token', 'fake-jwt');
                    localStorage.setItem('ngis-theme', 'light');
                """)
                page = await context.new_page()
                url = f"http://127.0.0.1:3000/{path}"

                try:
                    await page.goto(url, wait_until="domcontentloaded", timeout=6000)
                    await page.wait_for_timeout(250)

                    if tab_btn:
                        t = page.locator(tab_btn).first
                        if await t.count() > 0:
                            await t.click(timeout=2000)
                            await page.wait_for_timeout(200)

                    input_el = page.locator(selector).first
                    if await input_el.count() == 0:
                        print(f"[-] {title} [{vp_name}]: selector not found", flush=True)
                        results.append({"title": title, "vp": vp_name, "status": "NOT_FOUND"})
                        await context.close()
                        continue

                    # Focus input
                    await input_el.scroll_into_view_if_needed()
                    await input_el.focus(timeout=3000)
                    await page.wait_for_timeout(250)

                    info_focus = await input_el.evaluate("""el => {
                        const p = el.closest('.ngis-search') || el.closest('.dir-search-wrap') || el.parentElement;
                        const csIn = window.getComputedStyle(el);
                        const csPa = window.getComputedStyle(p);
                        return {
                            inputBorderWidth: csIn.borderWidth,
                            inputOutlineWidth: csIn.outlineWidth,
                            inputOutlineStyle: csIn.outlineStyle,
                            inputShadow: csIn.boxShadow,
                            inputBg: csIn.backgroundColor,
                            parentBorderColor: csPa.borderColor,
                            parentBoxShadow: csPa.boxShadow,
                            parentWidth: csPa.width,
                            parentClass: p.className
                        };
                    }""")

                    # Test typing
                    await input_el.fill("math", timeout=3000)
                    await page.wait_for_timeout(50)

                    # Criteria:
                    # 1. Input border must be 0px
                    # 2. Input outline must be 0px or none
                    # 3. Input shadow must be none
                    # 4. Parent has focus border or shadow (Forest Green, or white glass on hero banner)
                    border_ok = info_focus['inputBorderWidth'] in ['0px', '0px 0px 0px 0px']
                    outline_ok = info_focus['inputOutlineWidth'] in ['0px', '0px 0px 0px 0px'] or info_focus['inputOutlineStyle'] == 'none'
                    shadow_ok = info_focus['inputShadow'] in ['none', 'none 0px 0px 0px']
                    parent_focus_ok = (
                        'rgb(23, 107, 69)' in info_focus['parentBorderColor'] or
                        'rgb(24, 108, 70)' in info_focus['parentBorderColor'] or
                        'rgb(26, 109, 72)' in info_focus['parentBorderColor'] or
                        'rgb(29, 111, 74)' in info_focus['parentBorderColor'] or
                        'rgba(23, 107, 69' in info_focus['parentBoxShadow'] or
                        'rgba(255, 255, 255' in info_focus['parentBorderColor'] or
                        'rgba(255, 255, 255' in info_focus['parentBoxShadow']
                    )

                    all_ok = border_ok and outline_ok and shadow_ok and parent_focus_ok

                    if all_ok:
                        passed_tests += 1
                        print(f"[PASS] {title} [{vp_name}]: single boundary ok (parent: {info_focus['parentBorderColor']})", flush=True)
                        results.append({"title": title, "vp": vp_name, "status": "PASS"})
                    else:
                        print(f"[FAIL] {title} [{vp_name}]: border={info_focus['inputBorderWidth']}, outline={info_focus['inputOutlineWidth']}, shadow={info_focus['inputShadow']}, parentBdr={info_focus['parentBorderColor']}", flush=True)
                        results.append({"title": title, "vp": vp_name, "status": "FAIL", "info": info_focus})

                except Exception as e:
                    print(f"[ERR] {title} [{vp_name}]: {e}", flush=True)
                    results.append({"title": title, "vp": vp_name, "status": "ERROR", "error": str(e)})

                await context.close()

        print(f"\n=======================================================", flush=True)
        print(f" AUDIT COMPLETE: {passed_tests} / {total_tests} PASSED", flush=True)
        print(f"=======================================================", flush=True)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run_audit())
