import asyncio
import os
from playwright.async_api import async_playwright

PAGES = [
    ("pages/admin/admin-campus.html", "admin_campus_color_refined", 1440, 900),
    ("pages/admin/admin-campus.html", "admin_campus_color_refined_mobile", 375, 812),
    ("pages/principal/principal-academic-workspace.html", "principal_workspace_color_refined", 1440, 900),
    ("pages/principal/principal-academic-workspace.html", "principal_workspace_color_refined_mobile", 375, 812),
    ("pages/student/student.html", "student_portal_color_refined", 1440, 900),
    ("pages/teacher/teacher.html", "teacher_portal_color_refined", 1440, 900),
    ("pages/admin/admin-lost-found.html", "admin_lost_found_color_refined", 1440, 900)
]

ARTIFACT_DIR = r"C:\Users\oudom\.gemini\antigravity\brain\f0e0db56-cd04-4f51-a7f8-40ba21b43536"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for page_rel, name, w, h in PAGES:
            context = await browser.new_context(viewport={"width": w, "height": h})
            page = await context.new_page()
            url = f"http://127.0.0.1:3000/{page_rel}"
            try:
                await page.goto(url, wait_until="networkidle", timeout=12000)
            except Exception:
                await page.goto(url, wait_until="domcontentloaded", timeout=12000)
            await asyncio.sleep(1)
            out_path = os.path.join(ARTIFACT_DIR, f"{name}.png")
            await page.screenshot(path=out_path, full_page=False)
            print(f"Captured: {out_path} ({w}x{h})")
            await context.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
