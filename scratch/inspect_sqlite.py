import sys
sys.path.insert(0, '.')
import academic_store as ACADEMIC

for tbl in ['academic_years', 'grading_periods', 'subjects', 'teacher_assignments', 'enrollments', 'grading_rules', 'assessments', 'grades', 'attendance', 'report_cards', 'audit_events']:
    rows = ACADEMIC.query(f"SELECT * FROM {tbl}")
    print(f"Table {tbl}: {len(rows)} rows")
    if rows:
        print("  Sample:", rows[0])
