import os
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:3000"
shots = os.path.join(os.path.dirname(os.path.abspath(__file__)), "profile_shots")
os.makedirs(shots, exist_ok=True)
PAGES = ["principal-teacher-profiles", "principal-student-profiles"]
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 950})
    for name in PAGES:
        pg.goto(BASE + "/pages/principal/" + name + ".html", wait_until="networkidle")
        pg.wait_for_timeout(1800)
        pg.screenshot(path=os.path.join(shots, name + ".png"))
    b.close()
print("OK")
