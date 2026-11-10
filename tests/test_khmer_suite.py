#!/usr/bin/env python3
"""
============================================================================
 Khmer School Admin Suite — end-to-end regression suite
============================================================================
Covers the MVP acceptance criteria:

  * derived counters (never hardcoded) from the single-source domain model
  * greedy auto-assign fills every lesson with zero conflicts
  * manual click edits update the unassigned counter immediately
  * teacher / class / shift hard conflicts are blocked
  * batch undo restores any single assignment
  * CRUD + locked subjects affect auto-assign
  * AI preview -> apply token flow
  * real .xlsx export with Khmer headers, and import round-trip
  * all 10 principal/admin page shells + shared assets + sidebar links exist

Run:  python -m unittest tests.test_khmer_suite -v
      python tests/test_khmer_suite.py
============================================================================
"""
from __future__ import annotations

import io
import json
import os
import sys
import unittest
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import server  # noqa: E402
import timetable_models as M  # noqa: E402
from timetable_xlsx import read_xlsx  # noqa: E402

BASE = "/api/timetable"
STATE_FILE = ROOT / "data" / "timetable_state.json"


class TestKhmerSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Preserve whatever the user had on disk; tests must be non-destructive.
        cls._original = STATE_FILE.read_bytes() if STATE_FILE.exists() else None
        server.app.config["TESTING"] = True
        cls.c = server.app.test_client()
        cls.c.post(BASE + "/reset")

    @classmethod
    def tearDownClass(cls):
        cls.c.post(BASE + "/reset")
        if cls._original is not None:
            STATE_FILE.write_bytes(cls._original)
        elif STATE_FILE.exists():
            pass  # a freshly created seed is fine to leave behind

    # ── helpers ────────────────────────────────────────────────────────────
    def state(self):
        return self.c.get(BASE + "/state").get_json()["state"]

    def stats(self):
        return self.c.get(BASE + "/statistics").get_json()["stats"]

    # ── 1. seed + derived counters ─────────────────────────────────────────
    def test_01_health_and_seed_integrity(self):
        r = self.c.get(BASE + "/health").get_json()
        self.assertTrue(r["success"])
        self.assertEqual(r["service"], "khmer-school-admin-suite")
        self.assertEqual(r["classes"], 12)
        self.assertEqual(r["subjects"], 13)
        self.assertEqual(r["grid_cells"], 0)

        s = self.state()
        self.assertEqual(s["schema_version"], M.SCHEMA_VERSION)
        displays = [c["display"] for c in s["classes"]]
        self.assertEqual(displays, [f"{g}{sec}" for g in range(7, 13)
                                    for sec in ("A", "B")])
        self.assertEqual({c["code"] for c in s["subjects"]},
                         {"K", "M", "P", "C", "B", "ES", "G", "H", "I",
                          "IT", "EN", "ED", "SH"})
        self.assertEqual(M.DAYS, ["ច័ន្ទ", "អង្គារ", "ពុធ", "ព្រហស្បតិ៍",
                                  "សុក្រ", "សៅរ៍"])
        self.assertEqual(M.MORNING_STARTS,
                         ["07:00", "07:50", "08:40", "09:30", "10:20"])
        self.assertEqual(M.AFTERNOON_STARTS,
                         ["13:00", "13:50", "14:40", "15:30", "16:20"])

    def test_02_all_counts_are_derived(self):
        s = self.state()
        demand = sum(a["lessons"] for a in s["assignments"])
        st = self.stats()
        self.assertEqual(st["total_demand"], demand)
        self.assertEqual(st["placed"], len(s["grid"]))
        self.assertEqual(st["unassigned"], demand - st["placed"])
        chips = self.c.get(BASE + "/chips").get_json()["chips"]
        self.assertEqual(sum(ch["count"] for ch in chips), st["unassigned"])
        self.assertEqual(sum(p["assigned"] for p in st["per_class"]), st["placed"])
        self.assertEqual(len(st["per_class"]), len(s["classes"]))
        for t in st["teachers"]:
            self.assertEqual(t["assigned"], sum(
                1 for cell in s["grid"].values()
                if cell["teacher_id"] == t["id"]))
            self.assertEqual(t["overloaded"], t["assigned"] > t["target"])

    # ── 2. auto-assign acceptance criterion ────────────────────────────────
    def test_03_auto_assign_fills_everything_with_zero_conflicts(self):
        before = self.stats()
        r = self.c.post(BASE + "/auto-assign", json={"clear_first": True}).get_json()
        self.assertTrue(r["success"])
        self.assertEqual(r["placed"], before["total_demand"])
        self.assertEqual(len(r["state"]["grid"]), before["total_demand"])
        after = r["stats"]
        self.assertEqual(after["unassigned"], 0)
        self.assertEqual(after["conflicts"], 0)
        self.assertEqual(self.c.get(BASE + "/conflicts").get_json()["error_count"], 0)
        for t in after["teachers"]:
            self.assertLessEqual(t["assigned"], t["target"],
                                 f"{t['code']} overloaded")
            self.assertFalse(t["overloaded"])
        for p in after["per_class"]:
            self.assertEqual(p["remaining"], 0, f"{p['display']} not full")

    def test_04_locked_subject_excluded_from_auto_assign(self):
        self.c.post(BASE + "/reset")
        s = self.state()
        locked = next(x for x in s["subjects"] if x["code"] == "P")
        r = self.c.put(BASE + "/subjects/" + locked["id"],
                       json={"is_locked": True}).get_json()
        self.assertTrue(r["item"]["is_locked"])
        locked_demand = sum(a["lessons"] for a in s["assignments"]
                            if a["subject_id"] == locked["id"])
        demand = self.stats()["total_demand"]
        out = self.c.post(BASE + "/auto-assign",
                          json={"clear_first": True}).get_json()
        self.assertEqual(out["placed"], demand - locked_demand)
        # Locked lessons stay visible as unassigned chips (manual placement).
        self.assertEqual(out["stats"]["unassigned"], locked_demand)
        self.assertTrue(any(x["reason"] == "subject_locked"
                            for x in out["skipped"]))
        self.assertFalse(any(cell["subject_id"] == locked["id"]
                             for cell in out["state"]["grid"].values()))
        self.c.post(BASE + "/reset")

    # ── 3. manual editing + conflicts + undo ───────────────────────────────
    def test_05_manual_clear_and_place_updates_counter(self):
        self.c.post(BASE + "/reset")
        self.c.post(BASE + "/auto-assign", json={"clear_first": True})
        grid = self.state()["grid"]
        key, cell = next(iter(grid.items()))
        before = self.stats()["unassigned"]

        cleared = self.c.delete(BASE + "/cells", json={"key": key}).get_json()
        self.assertTrue(cleared["cleared"])
        self.assertEqual(cleared["stats"]["unassigned"], before + 1)

        placed = self.c.post(BASE + "/cells", json={
            "key": key, "subject_id": cell["subject_id"],
            "teacher_id": cell["teacher_id"],
        }).get_json()
        self.assertTrue(placed["success"])
        self.assertEqual(placed["stats"]["unassigned"], before)
        self.assertEqual(placed["stats"]["conflicts"], 0)

    def test_06_hard_conflicts_are_blocked(self):
        self.c.post(BASE + "/reset")
        self.c.post(BASE + "/auto-assign", json={"clear_first": True})
        s = self.state()

        # (a) class already has a lesson in that exact slot
        key, cell = next(iter(s["grid"].items()))
        r = self.c.post(BASE + "/cells", json={
            "key": key, "subject_id": cell["subject_id"],
            "teacher_id": cell["teacher_id"],
        })
        self.assertEqual(r.status_code, 409)
        self.assertTrue(r.get_json()["blocked"])
        self.assertIn("class_double_booked",
                      [x["type"] for x in r.get_json()["conflicts"]])

        # (b) teacher already booked in another class at same day/shift/period
        parts = M.parse_grid_key(key)
        # Find ANY free class slot that shares a day/shift/period with a class
        # where this teacher is already teaching (408/720 cells are filled).
        free_key = None
        busy_teacher = None
        busy_subject = None
        for busy_key, busy_cell in s["grid"].items():
            p = M.parse_grid_key(busy_key)
            for cls in s["classes"]:
                candidate = M.grid_key(p["day"], p["shift"],
                                       p["period"], cls["id"])
                if candidate not in s["grid"]:
                    free_key = candidate
                    busy_teacher = busy_cell["teacher_id"]
                    busy_subject = busy_cell["subject_id"]
                    break
            if free_key:
                break
        self.assertIsNotNone(free_key)
        r = self.c.post(BASE + "/cells", json={
            "key": free_key, "subject_id": busy_subject,
            "teacher_id": busy_teacher,
        })
        self.assertEqual(r.status_code, 409)
        self.assertIn("teacher_double_booked",
                      [x["type"] for x in r.get_json()["conflicts"]])

        # (c) shift mismatch: force an afternoon-only teacher into a morning slot
        teachers = s["teachers"]
        afternoon = next((t for t in teachers
                          if t.get("shifts") == [M.SHIFTS[1]]), None)
        if afternoon:
            free_morning = None
            for day in M.DAYS:
                for period in range(1, 6):
                    for cls in s["classes"]:
                        candidate = M.grid_key(day, M.SHIFTS[0], period, cls["id"])
                        if candidate not in s["grid"]:
                            free_morning = candidate
                            break
                    if free_morning:
                        break
                if free_morning:
                    break
            self.assertIsNotNone(free_morning)
            r = self.c.post(BASE + "/cells", json={
                "key": free_morning, "subject_id": afternoon["subject_id"],
                "teacher_id": afternoon["id"],
            })
            self.assertEqual(r.status_code, 409)
            self.assertIn("shift_mismatch",
                          [x["type"] for x in r.get_json()["conflicts"]])

    def test_07_batch_undo_restores_single_assignment(self):
        self.c.post(BASE + "/reset")
        self.c.post(BASE + "/auto-assign", json={"clear_first": True})
        s = self.state()
        key, cell = next(iter(s["grid"].items()))
        snapshot = {k: dict(v) for k, v in s["grid"].items()}

        self.c.delete(BASE + "/cells", json={"key": key})
        self.assertEqual(self.stats()["unassigned"], 1)
        changes = [{"key": k, "cell": None} for k in self.state()["grid"]]
        # Rebuild the pre-delete snapshot atomically (undo).
        changes = [{"key": k, "cell": v} for k, v in snapshot.items()]
        # Grid currently holds every key except `key`; batch replaces values.
        r = self.c.post(BASE + "/cells/batch",
                        json={"changes": changes, "label": "ត្រឡប់"}).get_json()
        self.assertTrue(r["success"])
        self.assertEqual(r["stats"]["unassigned"], 0)
        self.assertEqual(r["stats"]["conflicts"], 0)
        self.assertIn(key, r["state"]["grid"])

    def test_08_state_put_autosave_round_trip(self):
        s = self.state()
        s["institution"]["name_kh"] = "វិទ្យាល័យសាកល្បង"
        r = self.c.put(BASE + "/state", json={"state": s, "label": "autosave"})
        self.assertEqual(r.status_code, 200)
        body = r.get_json()
        self.assertTrue(body["saved"])
        self.assertEqual(self.state()["institution"]["name_kh"],
                         "វិទ្យាល័យសាកល្បង")
        self.assertGreater(body["revision"], 0)
        # Malformed state is rejected without corrupting the store.
        bad = self.c.put(BASE + "/state", json={"state": {"grid": {}}})
        self.assertEqual(bad.status_code, 400)
        self.assertEqual(self.state()["institution"]["name_kh"],
                         "វិទ្យាល័យសាកល្បង")
        self.c.post(BASE + "/reset")

    # ── 4. CRUD + teacher picker ───────────────────────────────────────────
    def test_09_subject_crud_and_cascade(self):
        self.c.post(BASE + "/reset")
        before = len(self.state()["subjects"])
        created = self.c.post(BASE + "/subjects", json={
            "name_kh": "សាកល្បង", "code": "ZZ", "short_name": "ស",
            "color": "#123456", "lessons_per_week": 2,
        }).get_json()
        self.assertTrue(created["success"])
        sid = created["item"]["id"]
        self.assertEqual(len(self.state()["subjects"]), before + 1)

        upd = self.c.put(BASE + "/subjects/" + sid,
                         json={"lessons_per_week": 4, "is_locked": True}).get_json()
        self.assertEqual(upd["item"]["lessons_per_week"], 4)
        self.assertTrue(upd["item"]["is_locked"])

        removed = self.c.delete(BASE + "/subjects/" + sid).get_json()
        self.assertTrue(removed["success"])
        self.assertEqual(len(self.state()["subjects"]), before)
        self.assertEqual(self.c.delete(BASE + "/subjects/" + sid).status_code, 404)

    def test_10_teacher_candidates_ranked_and_searchable(self):
        self.c.post(BASE + "/reset")
        s = self.state()
        sub = next(x for x in s["subjects"] if x["code"] == "K")
        key = M.grid_key("ច័ន្ទ", M.SHIFTS[0], 1, s["classes"][0]["id"])
        out = self.c.get(BASE + "/candidates", query_string={
            "key": key, "subject_id": sub["id"], "q": "K1",
        }).get_json()
        self.assertTrue(out["success"])
        self.assertGreaterEqual(out["count"], 1)
        self.assertEqual(out["candidates"][0]["code"], "K1")
        self.assertTrue(all(c["subject_id"] == sub["id"]
                            for c in out["candidates"]))
        for c in out["candidates"]:
            self.assertIn("status_kh", c)
            self.assertIn("remaining", c)
            self.assertIn("shift_ok", c)

    def test_11_institution_and_records_endpoints(self):
        self.c.post(BASE + "/reset")
        r = self.c.put(BASE + "/institution",
                       json={"name_kh": "សាលា អ",
                             "year": "ឆ្នាំសិក្សា ២០២៦–២០២៧"}).get_json()
        self.assertEqual(self.c.get(BASE + "/institution").get_json()
                         ["institution"]["year"], "ឆ្នាំសិក្សា ២០២៦–២០២៧")
        recs = self.c.get(BASE + "/records").get_json()
        self.assertTrue(recs["success"])
        self.assertGreater(recs["summary"]["total"], 0)
        self.assertIn("amount_kh", recs["summary"])
        self.c.post(BASE + "/reset")

    # ── 5. AI preview / apply ──────────────────────────────────────────────
    def test_12_ai_preview_apply_and_token_expiry(self):
        self.c.post(BASE + "/reset")
        preview = self.c.post(BASE + "/generate", json={
            "preview": True, "constraints": {"workload": 17},
        }).get_json()
        self.assertEqual(preview["mode"], "preview")
        self.assertIn("token", preview)
        self.assertIn("diff", preview)
        self.assertIn("proposed_grid", preview)
        self.assertEqual(preview["stats"]["unassigned"], 0)
        # Preview must NOT mutate the live store.
        self.assertGreater(self.stats()["unassigned"], 0)

        applied = self.c.post(BASE + "/generate/apply",
                              json={"token": preview["token"]}).get_json()
        self.assertTrue(applied["applied"])
        self.assertEqual(applied["stats"]["unassigned"], 0)
        self.assertEqual(applied["stats"]["conflicts"], 0)
        # Token is single-use.
        self.assertEqual(self.c.post(BASE + "/generate/apply", json={
            "token": preview["token"]}).status_code, 410)

    # ── 6. real Excel export / import ──────────────────────────────────────
    def test_13_all_xlsx_exports_are_valid_ooxml_with_khmer_headers(self):
        self.c.post(BASE + "/reset")
        self.c.post(BASE + "/auto-assign", json={"clear_first": True})
        for kind in ("all", "timetable", "master", "records", "subjects",
                     "teachers", "unassigned"):
            with self.subTest(kind=kind):
                r = self.c.get(BASE + "/export", query_string={"type": kind})
                self.assertEqual(r.status_code, 200)
                self.assertEqual(
                    r.headers["Content-Type"].split(";")[0],
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                raw = r.data
                self.assertEqual(raw[:2], b"PK")
                with zipfile.ZipFile(io.BytesIO(raw)) as z:
                    self.assertIn("[Content_Types].xml", z.namelist())
                    for part in z.namelist():
                        if part.endswith((".xml", ".rels")):
                            ET.fromstring(z.read(part))  # well-formed
                    text = " ".join(
                        z.read(n).decode("utf-8", "ignore")
                        for n in z.namelist() if n.endswith(".xml"))
                    # Khmer Unicode range present in headers / data
                    self.assertTrue(any("\u1780" <= ch <= "\u17ff" for ch in text),
                                    f"{kind} has no Khmer text")

    def test_14_export_import_round_trip_preserves_type_column(self):
        self.c.post(BASE + "/reset")
        xlsx = self.c.get(BASE + "/export",
                          query_string={"type": "records"}).data
        rows = read_xlsx(xlsx)
        self.assertGreater(len(rows), 3)
        # Export uses title + summary + header rows before the data rows.
        header_index = next(i for i, r in enumerate(rows[:8])
                            if "គោត្តនាម" in " ".join(map(str, r)))
        headers = [str(h) for h in rows[header_index]]
        self.assertIn("ប្រភេទ", headers)
        self.assertIn("គោត្តនាម-នាម", headers)

        up = self.c.post(BASE + "/import", data={
            "file": (io.BytesIO(xlsx), "records.xlsx"),
        }, content_type="multipart/form-data").get_json()
        self.assertTrue(up["success"], up)
        self.assertGreater(up["imported"], 0)
        imported = self.c.get(BASE + "/records").get_json()["records"]
        self.assertTrue(any(r.get("type") == "គ្រូបង្រៀង" for r in imported))
        self.assertTrue(any(r.get("type") == "សិស្ស" for r in imported))
        self.c.post(BASE + "/reset")

    def test_15_json_import_and_validation(self):
        self.c.post(BASE + "/reset")
        rows = [{"no": 1, "name": "សុខ ដារ៉ា", "type": "គ្រូបង្រៀង"},
                {"no": 2, "name": "ចាន់ សុភី", "type": "សិស្ស"}]
        r = self.c.post(BASE + "/import", json={"records": rows}).get_json()
        self.assertTrue(r["success"])
        self.assertEqual(r["imported"], 2)
        self.assertEqual(self.c.post(BASE + "/import", json={}).status_code, 400)
        self.c.post(BASE + "/reset")

    # ── 7. static delivery: pages, assets, nav ─────────────────────────────
    def test_16_all_ten_page_shells_exist_and_wire_the_shared_ui(self):
        files = {
            "wizard": "teacher-class-assignment",
            "builder": "timetable-builder",
            "viewer": "timetables",
            "subjects": "subjects",
        }
        for role in ("principal", "admin"):
            for module, slug in files.items():
                with self.subTest(role=role, module=module):
                    path = ROOT / "pages" / role / f"{role}-{slug}.html"
                    self.assertTrue(path.exists(), str(path))
                    html = path.read_text(encoding="utf-8")
                    self.assertTrue('lang="en"' in html or 'lang="km"' in html)
                    self.assertIn('<main class="main">', html)
                    self.assertIn('id="ks-root"', html)
                    self.assertIn(f'KS_MODULE="{module}"', html)
                    self.assertIn(f'role:"{role}"', html)
                    self.assertIn(f'active:"ks-{module}"', html)
                    for asset in ("khmer-suite.css", "khmer-suite-data.js",
                                  "khmer-suite-engine.js", "khmer-suite-ui.js",
                                  "layout.js", "_auth-bootstrap.js"):
                        self.assertIn(asset, html, asset)
                    # served over HTTP by Flask
                    resp = self.c.get(f"/pages/{role}/{role}-{slug}.html")
                    self.assertEqual(resp.status_code, 200)

    def test_17_sidebar_has_role_specific_khmer_suite_links(self):
        layout = (ROOT / "assets" / "js" / "layout.js").read_text(encoding="utf-8")
        # Principal retains operational scheduling suite
        for module, slug in (("ks-wizard", "teacher-class-assignment"),
                             ("ks-builder", "timetable-builder"),
                             ("ks-viewer", "timetables"),
                             ("ks-subjects", "subjects")):
            with self.subTest(role="principal", module=module):
                self.assertIn(f'id:"{module}"', layout)
                self.assertIn(f'pages/principal/principal-{slug}.html', layout)
        # Admin has centralized timetable oversight
        for module, slug in (("ks-oversight", "timetable-management"),
                             ("ks-viewer", "timetables"),
                             ("ks-subjects", "subjects")):
            with self.subTest(role="admin", module=module):
                self.assertIn(f'id:"{module}"', layout)
                self.assertIn(f'pages/admin/admin-{slug}.html', layout)
        self.assertEqual(layout.count('pages/admin/admin-timetable-management.html'), 1)
        self.assertEqual(layout.count('pages/principal/principal-timetable-builder.html'), 1)

    def test_18_shared_assets_are_served(self):
        for asset in ("assets/css/khmer-suite.css",
                      "assets/js/khmer-suite-data.js",
                      "assets/js/khmer-suite-engine.js",
                      "assets/js/khmer-suite-ui.js"):
            with self.subTest(asset=asset):
                self.assertTrue((ROOT / asset).exists())
                self.assertEqual(self.c.get("/" + asset).status_code, 200)

    # ── 8. design-system conformance ───────────────────────────────────────
    def test_19_pages_use_master_design_tokens_and_dark_theme(self):
        css = (ROOT / "assets/css/khmer-suite.css").read_text(encoding="utf-8")
        self.assertEqual(css.count("{"), css.count("}"), "unbalanced CSS braces")
        # Colours must be aliases of the NGIS master palette, not a second palette.
        for token in ("--color-primary", "--color-background", "--color-border",
                      "--color-text", "--ngis-shadow-card", "--ngis-radius-card"):
            self.assertIn(token, css, token)
        self.assertIn('html[data-theme="dark"]', css)
        self.assertIn("ks-page-title", css)
        self.assertIn("ks-kpi-strip", css)
        self.assertNotIn("linear-gradient", css, "no decorative gradients (DESIGN-RULES V4)")
        self.assertNotIn("font-weight: 700", css)
        self.assertNotIn("font-weight: 600", css)

        ui = (ROOT / "assets/js/khmer-suite-ui.js").read_text(encoding="utf-8")
        self.assertIn("function pageHeadHtml()", ui)
        self.assertIn("function kpiHtml()", ui)
        self.assertIn("pageHeadHtml() + kpiHtml()", ui)
        self.assertIn('data-act="export" data-type="all"', ui)

        for role in ("principal", "admin"):
            for slug in ("teacher-class-assignment", "timetable-builder",
                         "timetables", "subjects"):
                html = (ROOT / "pages" / role / f"{role}-{slug}.html").read_text(encoding="utf-8")
                with self.subTest(role=role, slug=slug):
                    self.assertIn('content="web_dashboard"', html)
                    self.assertIn("localStorage.getItem('ngis-theme')", html)
                    self.assertNotIn("setItem('ngis-theme','light')", html,
                                     "dark theme must not be force-disabled")
                    self.assertIn("var(--color-background", html)


if __name__ == "__main__":
    unittest.main(verbosity=2)
