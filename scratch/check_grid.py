import json
d = json.load(open('data/timetable_state.json', encoding='utf-8'))
grid = d.get('grid', {})
print('grid len:', len(grid))
if grid:
    print('Sample 3 keys:', list(grid.keys())[:3])
    print('Sample value:', list(grid.values())[0])

