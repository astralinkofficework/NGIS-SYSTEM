import asyncio
from playwright.async_api import async_playwright

async def inspect():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        urls = [
            ("Principal Attendance", "http://127.0.0.1:3000/pages/principal/principal-attendance.html"),
            ("Principal Dashboard", "http://127.0.0.1:3000/pages/principal/principal.html"),
            ("Student Exams", "http://127.0.0.1:3000/pages/student/student-exams.html"),
            ("Admin Dashboard", "http://127.0.0.1:3000/pages/admin/admin.html"),
            ("Teacher Dashboard", "http://127.0.0.1:3000/pages/teacher/teacher.html"),
        ]

        for name, url in urls:
            print(f"\n================ {name} ({url}) ================")
            await page.goto(url, wait_until="networkidle")
            await page.wait_for_timeout(1000)

            data = await page.evaluate("""() => {
                const nav = document.getElementById('ngisGlobalNavbar');
                const sidebar = document.getElementById('sidebar');
                const main = document.querySelector('.main');
                const hero = document.querySelector('.hero') || document.querySelector('#heroBanner');
                const heroTopbar = document.querySelector('.hero-topbar');
                const stickySpacer = document.querySelector('.ngis-sticky-spacer');
                const searchInputs = Array.from(document.querySelectorAll('input[type="search"]')).map(i => ({
                    id: i.id,
                    className: i.className,
                    visible: i.offsetParent !== null,
                    rect: i.getBoundingClientRect()
                }));

                const navRect = nav ? nav.getBoundingClientRect() : null;
                const sidebarRect = sidebar ? sidebar.getBoundingClientRect() : null;
                const mainRect = main ? main.getBoundingClientRect() : null;
                const heroRect = hero ? hero.getBoundingClientRect() : null;

                return {
                    nav: navRect ? { y: navRect.y, height: navRect.height, left: navRect.left, width: navRect.width } : null,
                    sidebar: sidebarRect ? { y: sidebarRect.y, height: sidebarRect.height, width: sidebarRect.width, display: getComputedStyle(sidebar).display } : null,
                    main: mainRect ? { y: mainRect.y, left: mainRect.left, width: mainRect.width, paddingTop: getComputedStyle(main).paddingTop } : null,
                    hero: heroRect ? { y: heroRect.y, height: heroRect.height, display: getComputedStyle(hero).display } : null,
                    heroTopbar: heroTopbar ? { height: heroTopbar.offsetHeight, display: getComputedStyle(heroTopbar).display } : null,
                    stickySpacer: stickySpacer ? { height: stickySpacer.offsetHeight, display: getComputedStyle(stickySpacer).display } : null,
                    searchInputs: searchInputs
                };
            }""")
            print("Navbar:", data["nav"])
            print("Sidebar:", data["sidebar"])
            print("Main:", data["main"])
            print("Hero:", data["hero"])
            print("HeroTopbar:", data["heroTopbar"])
            print("StickySpacer:", data["stickySpacer"])
            print("Search Inputs:", data["searchInputs"])

        await browser.close()

asyncio.run(inspect())
