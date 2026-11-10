import json

with open('data/timetable_state.json', 'r', encoding='utf-8') as f:
    state = json.load(f)

classes = state.get('classes', [])
subjects = state.get('subjects', [])
teachers = state.get('teachers', [])
assignments = state.get('assignments', [])
grid = state.get('grid', {})
published = state.get('published')

print('Classes:', len(classes))
print('Subjects:', len(subjects))
print('Teachers:', len(teachers))
print('Assignments:', len(assignments))
print('Grid cells:', len(grid))
print('Published:', published)

# Calculate total quota and placed periods
total_quota = sum(sum(s.get('lessons_per_week', 2) for s in subjects) for c in classes)
print('Total quota calculated:', total_quota)

# Per class placed
per_class_placed = {}
for k, cell in grid.items():
    cid = cell.get('class_id')
    per_class_placed[cid] = per_class_placed.get(cid, 0) + 1

print('Per class placed count:', per_class_placed)

# Check teacher workloads
teacher_load = {}
for a in assignments:
    tid = a.get('teacher_id')
    teacher_load[tid] = teacher_load.get(tid, 0) + a.get('lessons', 2)

overloaded_teachers = []
for t in teachers:
    t_id = t.get('id')
    load = teacher_load.get(t_id, 0)
    target = t.get('target', 17)
    if load > 23:
        overloaded_teachers.append({'id': t_id, 'code': t.get('code'), 'name': t.get('name_en'), 'load': load, 'target': target})

print('Overloaded teachers:', len(overloaded_teachers), overloaded_teachers)

