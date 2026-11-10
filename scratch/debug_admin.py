from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.on("console", lambda msg: print("CONSOLE:", msg.text))
    pg.goto('http://localhost:3000/pages/admin/admin-timetables.html')
    time.sleep(2)
    res = pg.evaluate('''() => {
        var s = window.KSEngine.get();
        var rawLocal = localStorage.getItem("khmer_timetable_state_v2");
        var parsedLocal = rawLocal ? JSON.parse(rawLocal) : null;
        var a = s.assignments.find(x => x.class_id === "class_7A" && x.subject_id === "sub_M");
        return {
            stateRev: s.revision,
            localRev: parsedLocal ? parsedLocal.revision : null,
            localTeacher: parsedLocal ? (parsedLocal.assignments.find(x => x.class_id === "class_7A" && x.subject_id === "sub_M") || {}).teacher_id : null,
            assignedTeacher: a ? a.teacher_id : null,
            saveStatus: window.KSEngine.saveStatus()
        };
    }''')
    print("RESULT:", res)
    b.close()

