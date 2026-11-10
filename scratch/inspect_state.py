import json

with open('data/timetable_state.json', 'r', encoding='utf-8') as f:
    state = json.load(f)

print('timetable_state keys:', list(state.keys()))
print('Classes count:', len(state.get('classes', [])))
print('Subjects count:', len(state.get('subjects', [])))
print('Teachers count:', len(state.get('teachers', [])))
print('Assignments count:', len(state.get('assignments', [])))
print('Grid cells count:', len(state.get('cells', [])))
print('Published status:', state.get('published', {}).get('status') if isinstance(state.get('published'), dict) else state.get('published'))

with open('data/system_configuration.json', 'r', encoding='utf-8') as f:
    sys_cfg = json.load(f)
print('system_configuration keys:', list(sys_cfg.keys()))

