import sys
sys.path.insert(0, '.')
import timetable_models as M

state = M.STORE.state()
# Auto assign 7B
M.auto_assign(state, class_id="class_7B")

# Place 3 cells for 7A
# Find 3 assignments for 7A
asgns_7a = [a for a in state['assignments'] if a['class_id'] == 'class_7A']
if asgns_7a:
    a0 = asgns_7a[0]
    # Place on Monday, Tuesday, Thursday morning P1
    state['grid']['ច័ន្ទ|ព្រឹក|1|class_7A'] = {'subject_id': a0['subject_id'], 'teacher_id': a0['teacher_id']}
    state['grid']['អង្គារ|ព្រឹក|1|class_7A'] = {'subject_id': a0['subject_id'], 'teacher_id': a0['teacher_id']}
    state['grid']['ព្រហស្បតិ៍|ព្រឹក|1|class_7A'] = {'subject_id': a0['subject_id'], 'teacher_id': a0['teacher_id']}

# Publish v7
M.publish_timetable(state, published_by="Dr. Ly Bunheng (Principal)", note="Grade 7B Semester 1 Schedule approved and published.")
state['published']['version'] = 7

saved = M.STORE.replace(state, "Initialized authoritative baseline (7B complete, 7A partial, v7 published)")
stats = M.statistics(saved)
print("Saved baseline state:")
print("Placed periods:", stats['placed'], "/ 408")
print("Published version:", saved.get('published', {}).get('version'))
print("Class 7B remaining:", next(c for c in stats['per_class'] if c['id'] == 'class_7B')['remaining'])
print("Class 7A remaining:", next(c for c in stats['per_class'] if c['id'] == 'class_7A')['remaining'])

