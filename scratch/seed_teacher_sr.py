import json

with open('data/service_requests.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

existing_ids = {item['id'] for item in data}

new_items = [
  {
    "id": "SR-1006",
    "studentId": "TCH-2024-042",
    "studentName": "Dr. Sarah Jenkins",
    "role": "teacher",
    "category": "it_support",
    "type": "projector_av",
    "title": "Room 302 Ceiling Projector Calibration & HDMI Sync",
    "description": "Interactive laser projector in Academic Wing B Room 302 shows color fringing and loses HDMI audio during Calculus lectures.",
    "status": "in_progress",
    "priority": "high",
    "campus": "Sensok",
    "assignee": "Campus IT Support Team",
    "date": "2026-10-28",
    "updatedAt": "2026-10-29",
    "comments": [
      {
        "by": "Dr. Sarah Jenkins",
        "text": "Reported during 2nd period Calculus. HDMI cable replaced once, issue persists in projector optical unit.",
        "date": "2026-10-28"
      },
      {
        "by": "Campus IT Team",
        "text": "Technician scheduled for optical lens alignment and HDMI port firmware update today at 15:30.",
        "date": "2026-10-29"
      }
    ]
  },
  {
    "id": "SR-1007",
    "studentId": "TCH-2024-042",
    "studentName": "Dr. Sarah Jenkins",
    "role": "teacher",
    "category": "supplies",
    "type": "exam_stationery",
    "title": "Batch 250 Midterm Exam Booklets & Mathematical Formula Tables",
    "description": "Requisition for standard Grade 11 & 12 Advanced Mathematics midterm examination sheets and graphing paper pads.",
    "status": "open",
    "priority": "normal",
    "campus": "Sensok",
    "assignee": "Academic Registrar & Supplies",
    "date": "2026-11-01",
    "updatedAt": "2026-11-01",
    "comments": [
      {
        "by": "Dr. Sarah Jenkins",
        "text": "Needed for upcoming Grade 11-A & 12-B midterm assessments next Monday.",
        "date": "2026-11-01"
      }
    ]
  },
  {
    "id": "SR-1008",
    "studentId": "TCH-2024-042",
    "studentName": "Dr. Sarah Jenkins",
    "role": "teacher",
    "category": "facilities",
    "type": "space_booking",
    "title": "Science Lab B Booking — Inter-School Math & Science Exhibition",
    "description": "Room reservation for after-school preparation and student project setup for the November Olympiad.",
    "status": "completed",
    "priority": "normal",
    "campus": "Sensok",
    "assignee": "Facilities Management",
    "date": "2026-10-20",
    "updatedAt": "2026-10-22",
    "comments": [
      {
        "by": "Dr. Sarah Jenkins",
        "text": "Requested for Oct 22, 15:30 - 17:30.",
        "date": "2026-10-20"
      },
      {
        "by": "Facilities Management",
        "text": "Approved and scheduled on master room timetable. Key signed out to Faculty Department.",
        "date": "2026-10-22"
      }
    ]
  }
]

for item in new_items:
    if item['id'] not in existing_ids:
        data.append(item)

with open('data/service_requests.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Total service requests now: {len(data)}")

