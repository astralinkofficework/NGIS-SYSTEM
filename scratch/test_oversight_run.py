import sys
sys.path.insert(0, '.')
import timetable_oversight as O

data = O.compute_oversight_data()
print("Oversight computed successfully!")
print("Stages:")
for s in data['stages']:
    print(f"  Step {s['step']}: {s['name']} -> {s['status']} ({s['summary']})")
print("Outstanding tasks count:", len(data['outstanding_tasks']))
print("Reminders count:", len(data['reminders']))
print("Activity history count:", len(data['activity_history']))

