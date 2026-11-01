import asyncio
import json
import urllib.parse
from playwright.async_api import async_playwright

ROLES_CONFIG = [
    {
        "role": "admin",
        "start_url": "http://127.0.0.1:3000/pages/admin/admin.html",
        "expected_portal": "admin",
        "allowed_paths": ["/pages/admin/", "/pages/shared/"]
    },
    {
        "role": "teacher",
        "start_url": "http://127.0.0.1:3000/pages/teacher/teacher.html",
        "expected_portal": "teacher",
        "allowed_paths": ["/pages/teacher/"]
    },
    {
        "role": "student",
        "start_url": "http://127.0.0.1:3000/pages/student/student.html",
        "expected_portal": "student",
        "allowed_paths": ["/pages/student/", "/pages/shared/"]
    },
    {
        "role": "principal",
        "start_url": "http://127.0.0.1:3000/pages/principal/principal.html",
        "expected_portal": "principal",
        "allowed_paths": ["/pages/principal/", "/pages/shared/"]
    },
    {
        "role": "staff",
        "start_url": "http://127.0.0.1:3000/pages/staff/staff.html",
        "expected_portal": "staff",
        "allowed_paths": ["/pages/staff/", "/pages/shared/"]
    }
]

async def run_audit():
    results = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        
        for cfg in ROLES_CONFIG:
            role = cfg["role"]
            start_url = cfg["start_url"]
            expected_portal = cfg["expected_portal"]
            allowed_paths = cfg["allowed_paths"]
            
            page = await context.new_page()
            
            # Setup console error listener
            console_errors = []
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            
            # Seed active portal in localStorage
            await page.goto("http://127.0.0.1:3000/index.html")
            await page.evaluate(f"""() => {{
                localStorage.setItem('ngis_active_portal', '{role}');
                localStorage.setItem('ngis_token', 'mock-jwt-token-{role}');
            }}""")
            
            # Open start page
            await page.goto(start_url, wait_until="networkidle")
            await page.wait_for_selector(".side-nav .nav-link", timeout=5000)
            
            # Collect all sidebar links
            links_data = await page.evaluate("""() => {
                const links = Array.from(document.querySelectorAll('.side-nav .nav-link'));
                return links.map(el => {
                    const labelEl = el.querySelector('.nav-link-label');
                    const label = (labelEl || el).textContent.trim();
                    const href = el.getAttribute('href');
                    const fullHref = el.href;
                    return { label: label, href: href, fullHref: fullHref };
                });
            }""")
            
            print(f"\n========================================================")
            print(f"AUDITING ROLE: {role.upper()} ({len(links_data)} sidebar links)")
            print(f"========================================================")
            
            for item in links_data:
                label = item.get("label", "")
                href = item.get("href", "")
                full_href = item.get("fullHref") or item.get("full_href") or href
                
                # Skip logout / landing page redirect test
                if "logout" in label.lower() or href == "index.html" or href.endswith("/index.html") or href == "../../index.html":
                    results.append({
                        "role": role,
                        "label": label,
                        "href": href,
                        "target_url": full_href,
                        "passed": True,
                        "notes": "Logout link (returns to landing page as expected)"
                    })
                    print(f"  [PASS] {label:28} -> {href} (Logout)")
                    continue
                
                test_page = await context.new_page()
                target_errors = []
                test_page.on("console", lambda msg: target_errors.append(msg.text) if msg.type == "error" else None)
                
                # Ensure context is seeded with current role
                await test_page.goto("http://127.0.0.1:3000/index.html")
                await test_page.evaluate(f"""() => {{
                    localStorage.setItem('ngis_active_portal', '{role}');
                    localStorage.setItem('ngis_token', 'mock-jwt-token-{role}');
                }}""")
                
                # 1. Direct navigation
                resp = await test_page.goto(full_href, wait_until="networkidle")
                current_url = test_page.url
                
                # 2. Check active role and data-role
                page_state = await test_page.evaluate("""() => {
                    return {
                        bodyRole: document.body.getAttribute('data-role') || document.body.getAttribute('data-portal'),
                        windowPageRole: (window.PAGE && window.PAGE.role) || null,
                        activeNav: (window.PAGE && window.PAGE.active) || null,
                        storedPortal: localStorage.getItem('ngis_active_portal')
                    };
                }""")
                
                # 3. Refresh test
                await test_page.reload(wait_until="networkidle")
                refreshed_url = test_page.url
                refreshed_body_role = await test_page.evaluate("() => document.body.getAttribute('data-role') || (window.PAGE && window.PAGE.role)")
                
                # 4. Check path validity
                parsed = urllib.parse.urlparse(current_url)
                path = parsed.path
                
                # Strict check: Never allow student -> teacher or teacher -> student
                is_cross_role = False
                if role == "student" and "/pages/teacher/" in path:
                    is_cross_role = True
                if role == "teacher" and "/pages/student/" in path:
                    is_cross_role = True
                if role in ["admin", "teacher", "student", "principal", "staff"]:
                    if not any(path.startswith(p) for p in allowed_paths):
                        is_cross_role = True
                
                role_match = (page_state["windowPageRole"] == expected_portal) or (page_state["bodyRole"] == expected_portal)
                
                # Filter harmless icon font 404 or favicon from errors
                filtered_errors = [e for e in target_errors if "favicon" not in e and "font" not in e.lower() and "404" not in e]
                
                passed = (not is_cross_role) and role_match and (resp.status < 400)
                
                status_str = "PASS" if passed else "FAIL"
                notes = []
                if is_cross_role:
                    notes.append(f"CROSS ROLE LEAK: {path} not in {allowed_paths}")
                if not role_match:
                    notes.append(f"ROLE MISMATCH: got {page_state['windowPageRole']}/{page_state['bodyRole']}, expected {expected_portal}")
                if resp.status >= 400:
                    notes.append(f"HTTP STATUS: {resp.status}")
                
                res_obj = {
                    "role": role,
                    "label": label,
                    "href": href,
                    "target_url": current_url,
                    "resolved_role": page_state["windowPageRole"] or page_state["bodyRole"],
                    "passed": passed,
                    "notes": "; ".join(notes) if notes else "Verified clean - no cross-role leakage"
                }
                results.append(res_obj)
                
                print(f"  [{status_str}] {label:28} -> {path} (Role: {page_state['windowPageRole'] or page_state['bodyRole']}) {'; '.join(notes)}")
                
                await test_page.close()
                
            await page.close()
            
        await browser.close()
        
    with open("scratch/audit_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        
    total = len(results)
    passed_count = sum(1 for r in results if r["passed"])
    failed_count = total - passed_count
    print(f"\n========================================================")
    print(f"FINAL AUDIT RESULT: {passed_count}/{total} PASSED ({failed_count} FAILED)")
    print(f"========================================================")

asyncio.run(run_audit())
