import sys, os
sys.path.insert(0, os.path.abspath('.'))
import server
students = server.DB['students']
print(f"Total students in DB: {len(students)}")
for s in students[:8]:
    print(f"{s['id']} | {s['name']} | Class: {s['class']} | Grade: {s['grade']} | GPA: {s.get('gpa', 'N/A')}")

classes = server.DB.get('classes', [])
print(f"\nTotal classes in DB: {len(classes)}")
for c in classes:
    print(f"{c['id']} | {c['name']} | Room: {c.get('room')} | Cap: {c.get('studentCount', 32)}/{c.get('capacity', 35)}")
