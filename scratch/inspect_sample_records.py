import sys
sys.path.insert(0, '.')
from server import DB
import json

print("Sample Attendance Record:")
if DB.get('attendanceRecords'):
    print(DB['attendanceRecords'][0])

print("\nSample Grade Record:")
if DB.get('grades'):
    print(DB['grades'][0])

print("\nSample Lesson Record:")
if DB.get('lessons'):
    print(DB['lessons'][0])

print("\nSample Assignment Record:")
if DB.get('assignments'):
    print(DB['assignments'][0])

with open('data/system_configuration.json', 'r', encoding='utf-8') as f:
    cfg = json.load(f)
print("\nExam Config in system_configuration.json:")
print(cfg.get('exam_config'))

