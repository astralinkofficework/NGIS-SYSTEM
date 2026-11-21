import asyncio
from playwright.async_api import async_playwright

PAGES = [
    "admin.html",
    "admin-absence-stats.html",
    "admin-attendance.html",
    "admin-users-students.html",
    "admin-users-teachers.html",
    "admin-users-staff.html",
    "admin-users-admins.html",
    "admin-users-principals.html",
    "admin-teacher-profiles.html",
    "admin-student-profiles.html",
    "admin-teacher-class-assignment.html",
    "admin-student-assign.html",
    "admin-roles-permissions.html",
    "admin-student-verify.html",
    "admin-teacher-verify.html",
    "admin-departments.html",
    "admin-campuses.html",
    "admin-classes.html",
    "admin-timetables.html",
    "admin-lost-found.html",
    "admin-security.html"
]

async def verify_page(browser, page_name):
    url = f"http://127.0.0.1:3000/pages/admin/{page_name}"
    results = {"page": page_name, "errors": [], "mobile_hamburger": False, "heavy_fonts": 0}
    
    # 1. Mobile Check (375x667)
    mobile_page = await browser.new_page(viewport={"width": 375, "height": 667})
    try:
        mobile_page.on("pageerror", lambda err: results["errors"].append(f"Mobile JS Error: {err}"))
        await mobile_page.goto(url, wait_until="networkidle", timeout=15000)
        await mobile_page.wait_for_timeout(500)
        
        # Check hamburger button
        hamb = mobile_page.locator("button[data-action='toggle-sidebar'], .mobile-hamburger-btn, .hamburger-btn")
        results["mobile_hamburger"] = (await hamb.count()) > 0
    except Exception as e:
        results["errors"].append(f"Mobile load error: {e}")
    finally:
        await mobile_page.close()
        
    # 2. Desktop Check (1280x900)
    desktop_page = await browser.new_page(viewport={"width": 1280, "height": 900})
    try:
        desktop_page.on("pageerror", lambda err: results["errors"].append(f"Desktop JS Error: {err}"))
        await desktop_page.goto(url, wait_until="networkidle", timeout=15000)
        await desktop_page.wait_for_timeout(800)
        
        # Check font weights > 500
        heavy = await desktop_page.evaluate('''() => {
            let count = 0;
            document.querySelectorAll('body *:not(script):not(style)').forEach(el => {
                const fw = window.getComputedStyle(el).fontWeight;
                if (parseInt(fw, 10) > 500) count++;
            });
            return count;
        }''')
        results["heavy_fonts"] = heavy
        
    except Exception as e:
        results["errors"].append(f"Desktop load error: {e}")
    finally:
        await desktop_page.close()
        
    return results

async def main():
    print(f"Starting comprehensive audit of {len(PAGES)} Admin Portal pages...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        all_results = []
        for pg in PAGES:
            res = await verify_page(browser, pg)
            status = "PASS" if not res["errors"] and res["mobile_hamburger"] and res["heavy_fonts"] == 0 else "WARN/FAIL"
            print(f"[{status}] {pg:36} | Mobile Hamburger: {str(res['mobile_hamburger']):5} | Heavy Fonts (>500): {res['heavy_fonts']:3} | Errors: {len(res['errors'])}")
            if res["errors"]:
                for err in res["errors"]:
                    print(f"    -> {err}")
            all_results.append(res)
            
        await browser.close()
        
        # Summary
        passed = sum(1 for r in all_results if not r["errors"] and r["mobile_hamburger"] and r["heavy_fonts"] == 0)
        print(f"\n==========================================")
        print(f"TOTAL AUDITED: {len(all_results)} | PASSED: {passed} | FAILED: {len(all_results) - passed}")
        print(f"==========================================")

asyncio.run(main())
