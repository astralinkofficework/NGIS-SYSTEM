import sys, os, time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()

        print("[1] Opening teacher class assignment page...", flush=True)
        page.goto("http://localhost:3000/pages/principal/principal-teacher-class-assignment.html")
        page.wait_for_selector("#ks-root", timeout=10000)
        time.sleep(1)

        print("[2] Updating assignment via engine commit...", flush=True)
        # Update assignment for class_7A Mathematics (sub_M) to teacher t_M4 (Mao Thavy)
        res = page.evaluate("""() => {
            var s = window.KSEngine.get();
            var target = s.assignments.find(a => a.class_id === 'class_7A' && a.subject_id === 'sub_M');
            if (target) {
                target.teacher_id = 't_M4';
                window.KSEngine.commit('Assign Mao Thavy to 7A Math', (state) => {
                    var a = state.assignments.find(x => x.class_id === 'class_7A' && x.subject_id === 'sub_M');
                    if (a) a.teacher_id = 't_M4';
                });
                return { success: true, updated: target };
            }
            return { success: false };
        }""")
        print("Assignment update result:", res, flush=True)
        time.sleep(0.5)

        print("[3] Navigating to Master Timetables page (principal-timetables.html) without hard refresh...", flush=True)
        page.goto("http://localhost:3000/pages/principal/principal-timetables.html")
        page.wait_for_selector("#ks-root", timeout=10000)
        time.sleep(1.5)

        print("[4] Verifying state and rendered DOM in Master Timetable...", flush=True)
        check = page.evaluate("""() => {
            var s = window.KSEngine.get();
            var a = s.assignments.find(x => x.class_id === 'class_7A' && x.subject_id === 'sub_M');
            
            // Look for 7A cohort card in DOM
            var cards = Array.from(document.querySelectorAll('.font-display')).map(el => el.textContent.trim());
            var has7A = cards.some(c => c === '7A' || c.includes('7A'));
            
            // Check if M4 / Mao Thavy appears in the DOM
            var bodyText = document.body.innerText;
            var hasM4 = bodyText.includes('M4') || bodyText.includes('Mao Thavy');
            
            return {
                assignedTeacher: a ? a.teacher_id : null,
                has7A: has7A,
                hasM4: hasM4,
                revision: s.revision
            };
        }""")
        print("Verification result:", check, flush=True)
        assert check['assignedTeacher'] == 't_M4', f"Expected t_M4, got {check['assignedTeacher']}"
        assert check['hasM4'] == True, "Expected M4/Mao Thavy to appear in the rendered timetable!"
        print("PASS: Dynamic assignment propagated and rendered accurately without hard refresh!", flush=True)

        # Screenshot desktop
        shot_path = os.path.join(os.environ.get('USERPROFILE', ''), '.gemini', 'antigravity', 'brain', 'c3bf1c11-3155-48a6-b3ee-4e74d6713af7', 'viewer_dynamic_sync_verified.png')
        page.screenshot(path=shot_path, full_page=False)
        print("Screenshot saved to:", shot_path, flush=True)

        # Mobile check
        print("[5] Testing mobile view (375x667)...", flush=True)
        page.set_viewport_size({'width': 375, 'height': 667})
        time.sleep(0.5)
        btn = page.query_selector('[data-action="toggle-sidebar"]')
        assert btn is not None, "Mobile hamburger button must exist!"
        assert btn.is_visible(), "Mobile hamburger button must be visible!"
        print("PASS: Mobile hamburger button verified!", flush=True)

        mobile_shot = os.path.join(os.environ.get('USERPROFILE', ''), '.gemini', 'antigravity', 'brain', 'c3bf1c11-3155-48a6-b3ee-4e74d6713af7', 'viewer_mobile_sync_verified.png')
        page.screenshot(path=mobile_shot, full_page=False)
        print("Mobile screenshot saved to:", mobile_shot, flush=True)

        browser.close()
        print("ALL TESTS PASSED SUCCESSFULLY!", flush=True)

if __name__ == "__main__":
    run()
