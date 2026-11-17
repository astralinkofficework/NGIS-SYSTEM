import asyncio
from playwright.async_api import async_playwright

pages_to_test = [
    ("Admin Teacher Profiles", "http://127.0.0.1:3000/pages/admin/admin-teacher-profiles.html"),
    ("Admin Student Profiles", "http://127.0.0.1:3000/pages/admin/admin-student-profiles.html"),
    ("Principal Teacher Profiles", "http://127.0.0.1:3000/pages/principal/principal-teacher-profiles.html"),
    ("Principal Student Profiles", "http://127.0.0.1:3000/pages/principal/principal-student-profiles.html"),
    ("Admin Departments", "http://127.0.0.1:3000/pages/admin/admin-departments.html"),
    ("Admin Services", "http://127.0.0.1:3000/pages/admin/admin-services.html"),
    ("Admin Timetables", "http://127.0.0.1:3000/pages/admin/admin-timetables.html"),
    ("Teacher Roster", "http://127.0.0.1:3000/pages/teacher/teacher-roster.html"),
    ("Teacher Submissions", "http://127.0.0.1:3000/pages/teacher/teacher-submissions.html"),
    ("Admin Student Assign", "http://127.0.0.1:3000/pages/admin/admin-student-assign.html")
]

viewports = [
    ("iPhone 14 (390x844)", {"width": 390, "height": 844}),
    ("Desktop (1280x800)", {"width": 1280, "height": 800})
]

async def run_suite():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        for vp_name, vp in viewports:
            print(f"\n==========================================")
            print(f"TESTING VIEWPORT: {vp_name}")
            print(f"==========================================")
            context = await browser.new_context(viewport=vp)

            for name, url in pages_to_test:
                page = await context.new_page()
                page_errors = []
                page.on("pageerror", lambda err: page_errors.append(str(err)))

                try:
                    await page.goto(url, wait_until="networkidle", timeout=15000)
                    await page.wait_for_timeout(600)

                    # Check overflow
                    scroll_w = await page.evaluate("() => document.documentElement.scrollWidth")
                    client_w = await page.evaluate("() => document.documentElement.clientWidth")
                    overflow = max(0, scroll_w - client_w)

                    # Check visible h1 count
                    h1_vis_count = await page.evaluate("""() => {
                        return Array.from(document.querySelectorAll('h1')).filter(h => {
                            const rect = h.getBoundingClientRect();
                            const style = window.getComputedStyle(h);
                            return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
                        }).length;
                    }""")

                    # Check duplicate plus icons on buttons
                    dup_plus = await page.evaluate("""() => {
                        const btns = Array.from(document.querySelectorAll('button'));
                        let count = 0;
                        btns.forEach(b => {
                            const hasIcon = b.querySelector('svg, .ph-plus, .bi-plus, .material-symbols-outlined') !== null;
                            const text = b.innerText.trim();
                            if (hasIcon && text.startsWith('+')) count++;
                        });
                        return count;
                    }""")

                    # Check search input double borders
                    search_inputs = await page.query_selector_all(".ngis-search input, #dirSearch")

                    status = "PASS" if (len(page_errors) == 0 and overflow == 0 and dup_plus == 0) else "WARN"
                    print(f"[{status}] {name:28} | Overflow: {overflow}px | Visible H1s: {h1_vis_count} | Dup '+': {dup_plus} | Errors: {len(page_errors)}")
                    if page_errors:
                        for err in page_errors[:2]:
                            print(f"       Error: {err[:100]}")

                except Exception as ex:
                    print(f"[FAIL] {name:28} | Exception: {ex}")
                finally:
                    await page.close()

            await context.close()

        await browser.close()

asyncio.run(run_suite())
