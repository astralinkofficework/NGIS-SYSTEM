import sys
sys.path.insert(0, '.')
import academic_store as ACADEMIC

rows = ACADEMIC.query("""
    SELECT a.class_id, a.grading_period_id, g.workflow, COUNT(*) as ct 
    FROM grades g JOIN assessments a ON a.id = g.assessment_id 
    GROUP BY a.class_id, a.grading_period_id, g.workflow
""")
for r in rows:
    print(dict(r))
