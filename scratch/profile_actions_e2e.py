import io, json, os, time
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:3000"
PDF_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "e2e_upload_doc.pdf")
with open(PDF_PATH, "wb") as f:
    f.write(b"%PDF-1.4\n1 0 obj<</Type/Catalog>>endobj\ntrailer<</Root 1 0 R>>\n%%EOF")

results = []
errors = []
def ck(name, cond, extra=""):
    results.append((bool(cond), name, str(extra)[:200]))
    print(("PASS " if cond else "FAIL ") + name + ("  " + str(extra)[:160] if extra else ""))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 950})
    pg.on("pageerror", lambda e: errors.append("pageerror: " + str(e)[:180]))
    pg.on("console", lambda m: errors.append("console: " + m.text[:180]) if m.type == "error" else None)

    # ─── TEACHER PAGE ───
    pg.goto(BASE + "/pages/principal/principal-teacher-profiles.html", wait_until="networkidle")
    pg.wait_for_timeout(1500)

    # 1) Edit teacher T-001 phone via modal
    row = pg.evaluate("(() => { const rows=[...document.querySelectorAll('#dirBody tr')]; const r=rows.find(x=>x.textContent.includes('T-001')); return r ? r.querySelector('[data-act=edit]').getAttribute('data-id') : null; })()")
    ck("found T-001 edit", row == "T-001", row)
    pg.click("#dirBody tr:has-text('T-001') [data-act='edit']")
    pg.wait_for_timeout(300)
    ck("edit modal open", pg.evaluate("!document.getElementById('formModal').classList.contains('hidden')"))
    PHONE = "+855 99 888 %03d" % (int(time.time()) % 1000)  # unique per run: server rejects no-change PUTs
    pg.fill("#fxPhone", PHONE)
    pg.click("#formSaveBtn")
    pg.wait_for_timeout(800)
    toast = pg.evaluate("(document.getElementById('ngisToast')||{}).textContent")
    ck("teacher edit toast", "updated" in (toast or "").lower(), toast)
    prof = pg.request  # not used
    import urllib.request
    def get_json(path):
        r = urllib.request.Request(BASE + path, headers={"Authorization": "Bearer mock-jwt-token-principal"})
        return json.loads(urllib.request.urlopen(r).read())
    d = get_json("/api/principal/roster/teachers/T-001")["data"]
    ck("phone persisted via API", d.get("phone") == PHONE, d.get("phone"))

    # 2) Add teacher via UI (skip if a previous run already added the record)
    pre_existing = [t for t in get_json("/api/principal/roster/teachers")["data"] if t["name"] == "E2E Test Educator"]
    if pre_existing:
        ck("add teacher persisted", len(pre_existing) == 1 and pre_existing[0]["id"].startswith("T-"), pre_existing)
        new_id = pre_existing[0]["id"]
    else:
        pg.click("#btnAddTeacher")
        pg.wait_for_timeout(300)
        pg.fill("#fxName", "E2E Test Educator")
        pg.fill("#fxEmail", "e2e.test.%d@ngis.edu.kh" % int(time.time()))
        pg.fill("#fxSubject", "Environmental Science")
        pg.select_option("#fxDept", "STEM")
        pg.click("#formSaveBtn")
        pg.wait_for_timeout(900)
        n = pg.evaluate("document.getElementById('kpiGrid').textContent")
        added = [t for t in get_json("/api/principal/roster/teachers")["data"] if t["name"] == "E2E Test Educator"]
        ck("add teacher persisted", len(added) == 1 and added[0]["id"].startswith("T-"), added)
        new_id = added[0]["id"] if added else None

    # 3) Deactivate then reactivate the new teacher via toggle + confirm
    if new_id:
        pg.click(f"#dirBody tr:has-text('{new_id}') [data-act='toggle']")
        pg.wait_for_timeout(300)
        ck("confirm dialog opened", pg.evaluate("!document.getElementById('confirmModal').classList.contains('hidden')"))
        pg.click("#cfOk")
        pg.wait_for_timeout(800)
        st = [t for t in get_json("/api/principal/roster/teachers")["data"] if t["id"] == new_id][0]["status"]
        ck("deactivated", str(st).lower() == "inactive", st)
        pg.click(f"#dirBody tr:has-text('{new_id}') [data-act='toggle']")
        pg.wait_for_timeout(300)
        pg.click("#cfOk")
        pg.wait_for_timeout(800)
        st = [t for t in get_json("/api/principal/roster/teachers")["data"] if t["id"] == new_id][0]["status"]
        ck("reactivated", str(st).lower() == "active", st)

    # 4) Documents: open profile -> Documents tab -> upload -> verify -> delete
    pg.click("#dirBody tr:has-text('T-001') [data-act='view']")
    pg.wait_for_timeout(1000)
    pg.evaluate("[...document.querySelectorAll('#pfTabBar .pf-tab')][4].click()")
    pg.wait_for_timeout(500)
    ck("docs tab has upload form", pg.evaluate("!!document.getElementById('docUploadBtn')"))
    pg.set_input_files("#docFile", PDF_PATH)
    pg.select_option("#docCat", "Certification")
    pg.fill("#docNote", "E2E verification upload")
    pg.click("#docUploadBtn")
    pg.wait_for_timeout(1500)
    docsh = pg.evaluate("(() => { const t=document.getElementById('pfTabBody'); return t ? t.textContent : ''; })()")
    ck("uploaded doc listed", "e2e_upload_doc.pdf" in docsh, docsh[:120])
    doc_id = pg.evaluate("(() => { const b=document.querySelector('[data-doc-del]'); return b ? b.getAttribute('data-doc-del') : null; })()")
    ck("doc delete button present", bool(doc_id), doc_id)
    if doc_id:
        pg.click(f"[data-doc-del='{doc_id}']")
        pg.wait_for_timeout(300)
        pg.click("#cfOk")
        pg.wait_for_timeout(1200)
        docsh2 = pg.evaluate("(() => { const t=document.getElementById('pfTabBody'); return t ? t.textContent : ''; })()")
        ck("doc removed after delete", "e2e_upload_doc.pdf" not in docsh2, docsh2[:120])
    # close modal (Escape)
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(300)

    # 5) CSV export triggers a download
    with pg.expect_download(timeout=8000) as dl:
        pg.click("#btnExport")
    ck("CSV export downloads", dl.value.suggested_filename.endswith(".csv"), dl.value.suggested_filename)

    # ─── STUDENT PAGE ───
    pg.goto(BASE + "/pages/principal/principal-student-profiles.html", wait_until="networkidle")
    pg.wait_for_timeout(1500)
    # open edit on ST-2026-004
    pg.click("#dirBody tr:has-text('ST-2026-004') [data-act='edit']")
    pg.wait_for_timeout(300)
    # try save without reason -> blocked
    pg.click("#formSaveBtn")
    pg.wait_for_timeout(400)
    ck("reason required shown", pg.evaluate("!document.getElementById('fxReasonErr').classList.contains('hidden')"))
    pg.fill("#fxClass", "11-C")
    pg.fill("#fxReason", "E2E class reassignment test")
    pg.click("#formSaveBtn")
    pg.wait_for_timeout(900)
    srow = [s for s in get_json("/api/principal/roster/students")["data"] if s["id"] == "ST-2026-004"][0]
    ck("student edit persisted", srow.get("class") == "11-C", srow.get("class"))

    # student toggle requires reason too
    pg.click("#dirBody tr:has-text('ST-2026-004') [data-act='toggle']")
    pg.wait_for_timeout(300)
    pg.click("#cfOk")  # no reason yet -> stays open
    pg.wait_for_timeout(300)
    ck("student toggle blocks empty reason", pg.evaluate("!document.getElementById('cfReasonError').classList.contains('hidden')"))
    pg.fill("#cfReason", "E2E status test")
    pg.click("#cfOk")
    pg.wait_for_timeout(900)
    srow = [s for s in get_json("/api/principal/roster/students")["data"] if s["id"] == "ST-2026-004"][0]
    ck("student status changed", str(srow["status"]).lower() == "inactive", srow["status"])
    # restore
    pg.fill("#cfReason", "") if False else None
    pg.click("#dirBody tr:has-text('ST-2026-004') [data-act='toggle']")
    pg.wait_for_timeout(300)
    pg.fill("#cfReason", "E2E restore to active")
    pg.click("#cfOk")
    pg.wait_for_timeout(900)
    srow = [s for s in get_json("/api/principal/roster/students")["data"] if s["id"] == "ST-2026-004"][0]
    ck("student status restored", str(srow["status"]).lower() == "active", srow["status"])

    # student profile tabs render data
    pg.fill("#dirSearch", "Sok Dara")
    pg.wait_for_timeout(400)
    pg.click("#dirBody tr:has-text('ST-2026-002') [data-act='view']")
    pg.wait_for_timeout(1000)
    lens = []
    nt = pg.evaluate("document.querySelectorAll('#pfTabBar .pf-tab').length")
    for i in range(nt):
        pg.evaluate(f"document.querySelectorAll('#pfTabBar .pf-tab')[{i}].click()")
        pg.wait_for_timeout(350)
        lens.append(pg.evaluate("(() => { const t = document.getElementById('pfTabBody'); return t ? t.textContent.trim().length : 0; })()"))
    ck("all 8 student tabs have content", len(lens) == 8 and min(lens) > 20, lens)

    # deep link ?student=ST-2026-007
    pg.goto(BASE + "/pages/principal/principal-student-profiles.html?student=ST-2026-007", wait_until="networkidle")
    pg.wait_for_timeout(1800)
    ck("deep link opens profile", pg.evaluate("!document.getElementById('profileModal').classList.contains('hidden') && (document.getElementById('profileModalInner').textContent||'').includes('Srey Neang')"))

    # ─── ADMIN PAGES load ───
    for name, path in [("admin-teacher", "/pages/admin/admin-teacher-profiles.html"), ("admin-student", "/pages/admin/admin-student-profiles.html")]:
        pg.goto(BASE + path, wait_until="networkidle")
        pg.wait_for_timeout(1500)
        rows = pg.evaluate("document.querySelectorAll('#dirBody tr').length")
        kpi = pg.evaluate("(document.getElementById('kpiGrid')||{}).textContent || ''")
        ck(name + " renders rows", rows >= 6, rows)
        ck(name + " KPIs populated", "0" != kpi.strip() and len(kpi) > 20, kpi[:60])

    b.close()

fails = [r for r in results if not r[0]]
print("\nERRORS:", errors[:8] if errors else "none")
print("SUMMARY:", f"{len(results)-len(fails)}/{len(results)} PASS")
if fails:
    print("FAILED:", [f[1] for f in fails])
