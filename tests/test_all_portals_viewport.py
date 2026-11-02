import asyncio
from playwright.async_api import async_playwright

TEST_PAGES = [
    ("Student Dashboard", "student", "http://localhost:3000/pages/student/student.html"),
    ("Admin Dashboard", "admin", "http://localhost:3000/pages/admin/admin.html"),
    ("Admin Users", "admin", "http://localhost:3000/pages/admin/admin-users.html"),
    ("Admin Classes", "admin", "http://localhost:3000/pages/admin/admin-classes.html"),
    ("Teacher Dashboard", "teacher", "http://localhost:3000/pages/teacher/teacher.html"),
    ("Principal Dashboard", "principal", "http://localhost:3000/pages/principal/principal.html"),
    ("Shared News", "teacher", "http://localhost:3000/pages/shared/news.html"),
    ("Landing Index", "guest", "http://localhost:3000/index.html"),
]

VIEWPORTS = [
    ("Desktop", 1440, 900),
    ("Tablet", 768, 1024),
    ("Mobile", 390, 844),
]

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        all_passed = True

        for page_name, role, url in TEST_PAGES:
            print(f"\n--- AUDITING: {page_name} ---", flush=True)

            for vp_name, width, height in VIEWPORTS:
                context = await browser.new_context(
                    viewport={"width": width, "height": height},
                    device_scale_factor=1
                )

                if role != "guest":
                    await context.add_init_script(f"""
                        localStorage.setItem('auth_user', JSON.stringify({{
                            id: '{role}-test',
                            name: 'Test {role.title()}',
                            role: '{role}',
                            email: '{role}@ngis.edu'
                        }}));
                        localStorage.setItem('token', 'fake-jwt-token-{role}');
                        localStorage.setItem('ngis-theme', 'light');
                    """)

                page = await context.new_page()
                try:
                    await page.goto(url, wait_until="domcontentloaded", timeout=6000)
                except Exception as e:
                    print(f"[{vp_name}] Load warning: {e}", flush=True)

                await page.wait_for_timeout(350)

                # 1. Zero horizontal overflow
                scroll_w = await page.evaluate("document.documentElement.scrollWidth")
                inner_w = await page.evaluate("window.innerWidth")
                overflow_ok = scroll_w <= inner_w + 1
                if not overflow_ok:
                    print(f"  [FAIL] {vp_name}: Overflow! scrollWidth={scroll_w} > innerWidth={inner_w}", flush=True)
                    all_passed = False
                else:
                    print(f"  [PASS] {vp_name}: Zero overflow ({scroll_w} <= {inner_w})", flush=True)

                # 2. Hamburger button on screen <= 1024px
                if width <= 1024 and role != "guest":
                    hambs = page.locator('[data-action="toggle-sidebar"]')
                    count = await hambs.count()
                    visible_found = False
                    for i in range(count):
                        if await hambs.nth(i).is_visible():
                            visible_found = True
                            break
                    if not visible_found:
                        print(f"  [FAIL] {vp_name}: No visible hamburger button found!", flush=True)
                        all_passed = False
                    else:
                        print(f"  [PASS] {vp_name}: Visible hamburger verified", flush=True)

                # 3. Check font weights <= 500
                fw_result = await page.evaluate("""
                    () => {
                        const els = document.querySelectorAll('h1, h2, h3, h4, th, td, button, label');
                        let maxWeight = 0;
                        let heavy = null;
                        els.forEach(el => {
                            const cs = window.getComputedStyle(el);
                            const w = parseInt(cs.fontWeight, 10);
                            if (!isNaN(w) && w > maxWeight) {
                                maxWeight = w;
                                heavy = el.tagName + ': ' + el.textContent.trim().slice(0, 25);
                            }
                        });
                        return { maxWeight, heavy };
                    }
                """)
                if fw_result["maxWeight"] > 500:
                    print(f"  [FAIL] {vp_name}: Font weight > 500 found: {fw_result['maxWeight']} on {fw_result['heavy']}", flush=True)
                    all_passed = False
                else:
                    print(f"  [PASS] {vp_name}: Font weight <= 500 (max: {fw_result['maxWeight']})", flush=True)

                await context.close()

        await browser.close()
        print(f"\n========================================================", flush=True)
        if all_passed:
            print("ALL AUDITED PORTALS PASSED ALL RESPONSIVENESS & TYPOGRAPHY CHECKS!", flush=True)
        else:
            print("SOME CHECKS FAILED", flush=True)
        print(f"========================================================", flush=True)

if __name__ == "__main__":
    asyncio.run(run())
