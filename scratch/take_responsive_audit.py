import os
from playwright.sync_api import sync_playwright

PAGES = [
    ("builder", "http://127.0.0.1:3000/pages/principal/principal-timetable-builder.html"),
    ("timetables", "http://127.0.0.1:3000/pages/principal/principal-timetables.html"),
    ("subjects", "http://127.0.0.1:3000/pages/principal/principal-subjects.html"),
    ("records", "http://127.0.0.1:3000/pages/principal/principal-records.html")
]

VIEWPORTS = [
    ("desktop", 1280, 800),
    ("tablet", 768, 1024),
    ("mobile", 390, 844)
]

os.makedirs("scratch/responsive_audit", exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    for name, url in PAGES:
        for vp_name, width, height in VIEWPORTS:
            page = browser.new_page(viewport={"width": width, "height": height})
            page.goto(url, wait_until="networkidle")
            page.wait_for_timeout(1000)
            shot_path = f"scratch/responsive_audit/{name}_{vp_name}.png"
            page.screenshot(path=shot_path, full_page=False)
            print(f"Captured {shot_path}")
            page.close()
    browser.close()
print("All screenshots captured!")

