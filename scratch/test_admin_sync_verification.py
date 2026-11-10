import sys, os, time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()

        print("[1] Opening admin timetables page...", flush=True)
        page.goto("http://localhost:3000/pages/admin/admin-timetables.html")
        page.wait_for_selector("#ks-root", timeout=10000)
        time.sleep(1)

        print("[2] Verifying admin layout...", flush=True)
        res = page.evaluate("""() => {
            var s = window.KSEngine.get();
            var a = s.assignments.find(x => x.class_id === 'class_7A' && x.subject_id === 'sub_M');
            var bodyText = document.body.innerText;
            return {
                assignedTeacher: a ? a.teacher_id : null,
                hasM4: bodyText.includes('M4') || bodyText.includes('Mao Thavy'),
                hasHeader: bodyText.includes('Master Timetable') || bodyText.includes('Teacher Distribution Matrix')
            };
        }""")
        print("Admin verification result:", res, flush=True)
        assert res['assignedTeacher'] == 't_M4', "Admin state should also reflect the persisted assignment!"
        assert res['hasM4'] == True, "Admin timetable matrix should show M4/Mao Thavy!"

        admin_shot = os.path.join(os.environ.get('USERPROFILE', ''), '.gemini', 'antigravity', 'brain', 'c3bf1c11-3155-48a6-b3ee-4e74d6713af7', 'admin_viewer_dynamic_sync_verified.png')
        page.screenshot(path=admin_shot, full_page=False)
        print("Admin screenshot saved to:", admin_shot, flush=True)

        browser.close()
        print("ADMIN TEST PASSED SUCCESSFULLY!", flush=True)

if __name__ == "__main__":
    run()

