import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:3000/pages/principal/'
CHECKS = {
    'principal-teachers.html': ['Sync Registry', 'Add Teacher', 'Review All Submissions'],
    'principal-timetables.html': ['+ Add Timetable Slot', 'Timetable Management /'],
    'principal-attendance.html': ['Attendance Ledger & Daily Oversight', 'Highest school-level authority'],
}
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1440, 'height': 950})
    for page, gone in CHECKS.items():
        errs = []
        def on_err(e, sink=errs): sink.append(str(e))
        pg.on('pageerror', on_err)
        pg.goto(BASE + page, wait_until='networkidle')
        pg.wait_for_timeout(1100)
        text = pg.inner_text('body')
        left = [g for g in gone if g in text]
        print(f'{page:28} removed={not left} leftovers={left or "NONE"} errors={errs or "NONE"}')
        pg.remove_listener('pageerror', on_err)
    b.close()
