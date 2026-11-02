import json

with open('all_pages_data.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Parse the JSON inside const ALL_PAGES = [ ... ];
start = text.find('[')
end = text.rfind(']')

if start != -1 and end != -1:
    raw_json = text[start:end+1]
    pages = json.loads(raw_json)
    
    new_entries = [
      {
        "path": "pages/teacher/teacher-lost-found.html",
        "name": "teacher-lost-found.html",
        "title": "Faculty Lost & Found Desk",
        "category": "Faculty & Operations",
        "roles": [
          "teacher"
        ],
        "description": "Classroom-discovered property registry and custody management. Log found student articles, process ownership verifications, and hand over custody to the campus front desk.",
        "tags": [
          "Classroom Found",
          "Faculty Custody",
          "Claim Verification",
          "Desk Handover"
        ]
      },
      {
        "path": "pages/teacher/teacher-services.html",
        "name": "teacher-services.html",
        "title": "Faculty Services & Support Hub",
        "category": "Faculty & Operations",
        "roles": [
          "teacher"
        ],
        "description": "Central requisition and maintenance ticketing for faculty. Submit classroom projector and AV repairs, air conditioning service, exam answer booklets, and campus space reservations.",
        "tags": [
          "IT & AV Support",
          "Facilities Maintenance",
          "Exam Stationery",
          "Space Booking"
        ]
      }
    ]
    
    # Add new entries if not already present
    existing_paths = {p['path'] for p in pages}
    for entry in new_entries:
        if entry['path'] not in existing_paths:
            pages.append(entry)
            
    updated_text = f"const ALL_PAGES = {json.dumps(pages, indent=2, ensure_ascii=False)};\n\nif (typeof window !== 'undefined') {{\n  window.NGIS_PAGES = ALL_PAGES;\n}}\n"
    
    with open('all_pages_data.js', 'w', encoding='utf-8') as f:
        f.write(updated_text)
        
    print(f"SUCCESS: Updated all_pages_data.js! Total pages: {len(pages)}")
else:
    print("Could not find array in all_pages_data.js")

