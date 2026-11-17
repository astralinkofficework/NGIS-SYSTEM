import os
import glob
import re
import json
import asyncio
from playwright.async_api import async_playwright

def normalize_path(p):
    return p.replace(os.sep, '/')

async def run_comprehensive_page_audit():
    html_files = [normalize_path(f) for f in glob.glob('**/*.html', recursive=True) if 'node_modules' not in f and not f.startswith(('.', 'tests'))]
    print(f"Total HTML pages to crawl: {len(html_files)}")

    results = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # Test roles for testing context
        roles = {
            "admin": {"id": "adm-1", "name": "Admin Tester", "role": "admin", "email": "admin@ngis.edu"},
            "teacher": {"id": "tch-1", "name": "Teacher Tester", "role": "teacher", "email": "teacher@ngis.edu"},
            "student": {"id": "std-1", "name": "Student Tester", "role": "student", "email": "student@ngis.edu"},
            "principal": {"id": "pri-1", "name": "Principal Tester", "role": "principal", "email": "principal@ngis.edu"},
            "shared": {"id": "std-1", "name": "Shared Tester", "role": "student", "email": "student@ngis.edu"},
            "root": {"id": "adm-1", "name": "Root Tester", "role": "admin", "email": "admin@ngis.edu"}
        }

        for idx, page_path in enumerate(sorted(html_files), 1):
            portal = "root"
            parts = page_path.split('/')
            if len(parts) > 1 and parts[0] == 'pages':
                portal = parts[1]
            
            user_profile = roles.get(portal, roles["admin"])
            user_json = json.dumps(user_profile)

            page_result = {
                "file": page_path,
                "portal": portal,
                "title": "",
                "status": 0,
                "console_errors": [],
                "page_errors": [],
                "failed_requests": [],
                "horizontal_overflow_desktop": False,
                "horizontal_overflow_mobile": False,
                "hamburger_present_mobile": False,
                "missing_interactive_buttons": []
            }

            # 1. Desktop Test (1440x900)
            context = await browser.new_context(viewport={"width": 1440, "height": 900})
            await context.add_init_script(f"""
                localStorage.setItem('auth_user', JSON.stringify({user_json}));
                localStorage.setItem('token', 'fake-jwt');
                localStorage.setItem('ngis-theme', 'light');
            """)
            page = await context.new_page()

            page.on("console", lambda msg: page_result["console_errors"].append(f"[{msg.type}] {msg.text}") if msg.type in ["error"] else None)
            page.on("pageerror", lambda err: page_result["page_errors"].append(str(err)))
            page.on("requestfailed", lambda req: page_result["failed_requests"].append(f"{req.method} {req.url} - {req.failure}"))

            try:
                resp = await page.goto(f"http://127.0.0.1:3000/{page_path}", wait_until="domcontentloaded", timeout=5000)
                page_result["status"] = resp.status if resp else 0
                await page.wait_for_timeout(200)

                page_result["title"] = await page.title()

                # Check horizontal overflow desktop
                has_overflow_dt = await page.evaluate("() => document.documentElement.scrollWidth > window.innerWidth + 2")
                page_result["horizontal_overflow_desktop"] = has_overflow_dt

            except Exception as e:
                page_result["page_errors"].append(f"Goto error: {str(e)}")

            await context.close()

            # 2. Mobile Test (375x667)
            context_m = await browser.new_context(viewport={"width": 375, "height": 667})
            await context_m.add_init_script(f"""
                localStorage.setItem('auth_user', JSON.stringify({user_json}));
                localStorage.setItem('token', 'fake-jwt');
                localStorage.setItem('ngis-theme', 'light');
            """)
            page_m = await context_m.new_page()
            try:
                await page_m.goto(f"http://127.0.0.1:3000/{page_path}", wait_until="domcontentloaded", timeout=5000)
                await page_m.wait_for_timeout(200)

                # Check mobile overflow
                has_overflow_m = await page_m.evaluate("() => document.documentElement.scrollWidth > window.innerWidth + 2")
                page_result["horizontal_overflow_mobile"] = has_overflow_m

                # Check mobile hamburger menu presence (per AGENTS.md rule)
                has_hamburger = await page_m.evaluate("""() => {
                    const btn = document.querySelector('.hamburger-btn, .mobile-hamburger-btn, .htb-hamburger, [data-action="toggle-sidebar"]');
                    return !!btn;
                }""")
                page_result["hamburger_present_mobile"] = has_hamburger

            except Exception as e:
                pass

            await context_m.close()

            # Filter out expected or non-critical console errors (like favicon 404 or expected aborts)
            real_errors = [e for e in page_result["console_errors"] if 'favicon' not in e and 'ERR_ABORTED' not in e]
            page_result["console_errors"] = real_errors

            status_str = "OK" if not page_result["page_errors"] and not real_errors and not page_result["horizontal_overflow_desktop"] and not page_result["horizontal_overflow_mobile"] else "WARN"
            if page_result["page_errors"]:
                status_str = "ERR"

            print(f"[{status_str}] ({idx}/{len(html_files)}) {page_path} - Title: '{page_result['title'][:35]}' - Status: {page_result['status']} - Err: {len(page_result['page_errors'])}/{len(real_errors)} - Overflow: D={page_result['horizontal_overflow_desktop']}/M={page_result['horizontal_overflow_mobile']}")

            results.append(page_result)

        await browser.close()

    with open('tools/comprehensive_page_audit.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print("\n=== AUDIT SUMMARY ===")
    total_pages = len(results)
    err_pages = [r for r in results if r["page_errors"]]
    console_err_pages = [r for r in results if r["console_errors"]]
    overflow_dt_pages = [r for r in results if r["horizontal_overflow_desktop"]]
    overflow_m_pages = [r for r in results if r["horizontal_overflow_mobile"]]
    missing_hamburger_pages = [r for r in results if not r["hamburger_present_mobile"] and r["portal"] in ["admin", "teacher", "student", "principal", "shared"]]

    print(f"Total Pages Crawled: {total_pages}")
    print(f"Pages with Uncaught Exceptions: {len(err_pages)}")
    print(f"Pages with Console Errors:     {len(console_err_pages)}")
    print(f"Pages with Desktop Overflow:   {len(overflow_dt_pages)}")
    print(f"Pages with Mobile Overflow:    {len(overflow_m_pages)}")
    print(f"Portal Pages Missing Hamburger:{len(missing_hamburger_pages)}")

if __name__ == '__main__':
    asyncio.run(run_comprehensive_page_audit())
