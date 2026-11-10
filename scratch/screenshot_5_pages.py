from playwright.sync_api import sync_playwright
import os, time

urls = [
    ("teacher_assignment", "http://127.0.0.1:3000/pages/principal/principal-teacher-class-assignment.html"),
    ("timetable_builder", "http://127.0.0.1:3000/pages/principal/principal-timetable-builder.html"),
    ("timetables", "http://127.0.0.1:3000/pages/principal/principal-timetables.html"),
    ("subjects", "http://127.0.0.1:3000/pages/principal/principal-subjects.html"),
    ("records", "http://127.0.0.1:3000/pages/principal/principal-records.html")
]

art_dir = os.path.join(os.environ.get('USERPROFILE', ''), '.gemini', 'antigravity', 'brain', 'c3bf1c11-3155-48a6-b3ee-4e74d6713af7')

with sync_playwright() as p:
    browser = p.chromium.launch()
    for name, u in urls:
        page = browser.new_page(viewport={'width': 1280, 'height': 800})
        page.on("pageerror", lambda err: print(f"ERROR on {name}: {err}"))
        page.on("console", lambda msg: print(f"CONSOLE on {name}: [{msg.type}] {msg.text}"))
        resp = page.goto(u)
        time.sleep(2)
        shot = os.path.join(art_dir, f"page_check_{name}.png")
        page.screenshot(path=shot, full_page=True)
        print(f"Captured {name} -> {shot} (status: {resp.status}, final_url: {page.url})")
        page.close()
    browser.close()

