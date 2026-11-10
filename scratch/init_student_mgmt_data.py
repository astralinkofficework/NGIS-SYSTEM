import json
import os

DATA_DIR = os.path.abspath('data')

# 1. Update Requests
update_requests = [
    {
        "id": "SUR-2026-001",
        "studentId": "2026-STD-0142",
        "studentName": "Nrinphouneta Hok",
        "class": "10A",
        "field": "Residential Address",
        "previousValue": "No. 45, St. 2004, Sensok, Phnom Penh",
        "proposedValue": "No. 128, St. 598, Khan Russey Keo, Phnom Penh",
        "submittedBy": "Chan Dara Vuth (Parent)",
        "submittedAt": "2026-11-04 09:30",
        "supportingDoc": "proof_of_residence_lease.pdf",
        "status": "pending",
        "notes": "Relocated closer to North Campus. Utilities bill attached.",
        "reviewedBy": None,
        "reviewedAt": None,
        "comments": ""
    },
    {
        "id": "SUR-2026-002",
        "studentId": "2026-STD-0144",
        "studentName": "Sophea Chan",
        "class": "10A",
        "field": "Emergency Contact & Phone",
        "previousValue": "+855 12 345 678 (Mother)",
        "proposedValue": "+855 98 765 432 (Father - Primary) / +855 12 345 678 (Mother)",
        "submittedBy": "Chan Sophea (Guardian)",
        "submittedAt": "2026-11-05 14:15",
        "supportingDoc": "id_card_parent.pdf",
        "status": "pending",
        "notes": "Father returning from overseas assignment; please update primary contact.",
        "reviewedBy": None,
        "reviewedAt": None,
        "comments": ""
    },
    {
        "id": "SUR-2026-003",
        "studentId": "2026-STD-0145",
        "studentName": "Virak Heng",
        "class": "10A",
        "field": "Legal Name Khmer Spelling",
        "previousValue": "ហេង វីរៈ",
        "proposedValue": "ហេង វិរៈ",
        "submittedBy": "Virak Heng (Student)",
        "submittedAt": "2026-11-02 11:20",
        "supportingDoc": "birth_certificate_moeys.pdf",
        "status": "approved",
        "notes": "MoEYS Grade 9 National Examination Certificate alignment.",
        "reviewedBy": "Admin · Registrar Office",
        "reviewedAt": "2026-11-03 16:40",
        "comments": "Verified against official civil registry birth certificate."
    },
    {
        "id": "SUR-2026-004",
        "studentId": "2026-STD-0148",
        "studentName": "Kosal Rith Mony",
        "class": "10A",
        "field": "Medical Dietary & Allergy Note",
        "previousValue": "None on record",
        "proposedValue": "Severe Peanut & Shellfish Allergy (EpiPen Carrier)",
        "submittedBy": "Mony Chenda (Mother)",
        "submittedAt": "2026-11-06 08:45",
        "supportingDoc": "hospital_allergy_report.pdf",
        "status": "pending",
        "notes": "Physician report from Royal Phnom Penh Hospital attached.",
        "reviewedBy": None,
        "reviewedAt": None,
        "comments": ""
    },
    {
        "id": "SUR-2026-005",
        "studentId": "2026-STD-0155",
        "studentName": "Heng Piseth",
        "class": "10A",
        "field": "Guardian Legal Status",
        "previousValue": "Joint Guardianship",
        "proposedValue": "Sole Legal Custody - Pich Sreymom (Mother)",
        "submittedBy": "Pich Sreymom (Mother)",
        "submittedAt": "2026-10-28 10:10",
        "supportingDoc": "court_custody_decree.pdf",
        "status": "approved",
        "notes": "Municipal Court Decree #412/26 on file.",
        "reviewedBy": "Principal · Dr. Ly Bunheng",
        "reviewedAt": "2026-10-29 14:00",
        "comments": "Decree validated. Student emergency pickup list updated accordingly."
    }
]

# 2. Exemptions
exemptions = [
    {
        "id": "EXM-2026-001",
        "studentId": "2026-STD-0148",
        "studentName": "Kosal Rith Mony",
        "class": "10A",
        "subject": "Physical Education",
        "category": "Medical / Orthopedic Injury",
        "duration": "Semester 1 (AY 2025-26)",
        "reason": "Fractured clavicle recovery following sports accident.",
        "supportingDoc": "calmette_hospital_medical_certificate.pdf",
        "authorizedBy": "Principal · Dr. Ly Bunheng",
        "status": "active",
        "dateIssued": "2025-10-15",
        "academicCode": "EX",
        "notes": "Alternative theory wellness paper assigned in lieu of physical testing."
    },
    {
        "id": "EXM-2026-002",
        "studentId": "2026-STD-0160",
        "studentName": "Emily Jenkins",
        "class": "10A",
        "subject": "Khmer Literature & History",
        "category": "Foreign Passport / International Stream",
        "duration": "Academic Year 2025-26",
        "reason": "Diplomatic passport dependent; enrolled in ESL Southeast Asian Studies.",
        "supportingDoc": "embassy_diplomatic_credential.pdf",
        "authorizedBy": "Academic Dean · MoEYS Liaison",
        "status": "active",
        "dateIssued": "2025-09-01",
        "academicCode": "EX",
        "notes": "MoEYS International curriculum dispensation waiver granted."
    },
    {
        "id": "EXM-2026-003",
        "studentId": "2026-STD-0151",
        "studentName": "Sreylin Vuth",
        "class": "10A",
        "subject": "Introductory Computer Literacy",
        "category": "Advanced Credit Exemption",
        "duration": "Semester 1",
        "reason": "Scored 100% on Pre-assessment & holds Cambridge IGCSE Computer Science.",
        "supportingDoc": "cambridge_igcse_transcript.pdf",
        "authorizedBy": "ICT Department Head",
        "status": "active",
        "dateIssued": "2025-09-10",
        "academicCode": "EX",
        "notes": "Fast-tracked directly into AP Computer Science Principles."
    },
    {
        "id": "EXM-2026-004",
        "studentId": "2026-STD-0155",
        "studentName": "Heng Piseth",
        "class": "10A",
        "subject": "Swimming & Aquatics",
        "category": "Medical / Dermatology Condition",
        "duration": "Term 2",
        "reason": "Chronic contact dermatitis exacerbated by chlorinated water.",
        "supportingDoc": "dermatologist_note_kh.pdf",
        "authorizedBy": "School Health Clinic & Principal",
        "status": "under_review",
        "dateIssued": "2026-11-01",
        "academicCode": "PEN",
        "notes": "Awaiting final medical board confirmation."
    }
]

# 3. Registrations / Admissions
registrations = [
    {
        "id": "REG-2026-081",
        "applicantName": "Vannak Meas",
        "gender": "M",
        "dob": "2010-04-12",
        "appliedGrade": "Grade 10",
        "appliedCampus": "Sensok",
        "previousSchool": "Zaman International School",
        "gpaPrevious": 3.75,
        "guardianName": "Meas Vannak Sr.",
        "guardianPhone": "+855 12 888 999",
        "guardianEmail": "meas.sr@gmail.com",
        "submittedAt": "2026-11-03",
        "documents": ["Birth Certificate", "Grade 9 MoEYS Diploma", "Transcript", "Medical Record"],
        "status": "pending",
        "interviewScore": "88/100",
        "allocatedClass": None,
        "notes": "Strong background in Mathematics and Bilingual English."
    },
    {
        "id": "REG-2026-082",
        "applicantName": "Chanthou Kim",
        "gender": "F",
        "dob": "2010-09-25",
        "appliedGrade": "Grade 10",
        "appliedCampus": "Sensok",
        "previousSchool": "Hope International Academy",
        "gpaPrevious": 3.90,
        "guardianName": "Kim Sovann",
        "guardianPhone": "+855 17 444 333",
        "guardianEmail": "sovann.kim@outlook.com",
        "submittedAt": "2026-11-04",
        "documents": ["Birth Certificate", "Transcript", "Recommendation Letter"],
        "status": "pending",
        "interviewScore": "94/100",
        "allocatedClass": None,
        "notes": "Honor roll student. Applied for Science Stream."
    },
    {
        "id": "REG-2026-083",
        "applicantName": "Dara Roth",
        "gender": "M",
        "dob": "2009-11-18",
        "appliedGrade": "Grade 11",
        "appliedCampus": "Toul Kork",
        "previousSchool": "Western International School",
        "gpaPrevious": 3.20,
        "guardianName": "Roth Bunna",
        "guardianPhone": "+855 92 111 222",
        "guardianEmail": "bunna.roth@gmail.com",
        "submittedAt": "2026-10-25",
        "documents": ["Birth Certificate", "Grade 10 Transcript"],
        "status": "approved",
        "interviewScore": "82/100",
        "allocatedClass": "11B",
        "notes": "Placement test passed. Admitted to Grade 11B."
    },
    {
        "id": "REG-2026-084",
        "applicantName": "Monika Sen",
        "gender": "F",
        "dob": "2011-02-14",
        "appliedGrade": "Grade 10",
        "appliedCampus": "Sensok",
        "previousSchool": "Beltei International",
        "gpaPrevious": 2.85,
        "guardianName": "Sen Sokha",
        "guardianPhone": "+855 89 666 555",
        "guardianEmail": "sen.sokha@yahoo.com",
        "submittedAt": "2026-11-01",
        "documents": ["Birth Certificate"],
        "status": "missing_docs",
        "interviewScore": "Pending",
        "allocatedClass": None,
        "notes": "Official academic transcript and immunization record missing."
    }
]

# 4. Commendations
commendations = [
    {
        "id": "COM-2026-001",
        "studentId": "2026-STD-0142",
        "studentName": "Nrinphouneta Hok",
        "class": "10A",
        "category": "Academic Excellence",
        "title": "Top 5% GPA Honor Citation",
        "citation": "Demonstrated outstanding intellectual rigor and academic distinction in Advanced Mathematics and Chemistry.",
        "dateAwarded": "2026-07-03",
        "awardedBy": "Principal · Dr. Ly Bunheng",
        "status": "official",
        "certificateRef": "CERT-2026-HON-0142"
    },
    {
        "id": "COM-2026-002",
        "studentId": "2026-STD-0160",
        "studentName": "Emily Jenkins",
        "class": "10A",
        "category": "STEM & Innovation",
        "title": "National Science & Robotics First Place",
        "citation": "Led the school team to gold medal victory in the Inter-School Autonomous Robotics Olympiad.",
        "dateAwarded": "2026-08-15",
        "awardedBy": "Ministry of Education & NGIS Board",
        "status": "official",
        "certificateRef": "CERT-2026-ROB-0160"
    },
    {
        "id": "COM-2026-003",
        "studentId": "2026-STD-0151",
        "studentName": "Sreylin Vuth",
        "class": "10A",
        "category": "Leadership & Civic Service",
        "title": "Community Outreach Ambassador Award",
        "citation": "Spearheaded the provincial rural library book drive, gathering over 1,500 Khmer-English readers.",
        "dateAwarded": "2026-09-20",
        "awardedBy": "Dean of Student Affairs",
        "status": "official",
        "certificateRef": "CERT-2026-LDR-0151"
    },
    {
        "id": "COM-2026-004",
        "studentId": "2026-STD-0144",
        "studentName": "Sophea Chan",
        "class": "10A",
        "category": "Athletics & Sportsmanship",
        "title": "Varsity Badminton MVP",
        "citation": "Exemplary sportsmanship, team captaincy, and undefeated record during the National Interscholastic Games.",
        "dateAwarded": "2026-10-18",
        "awardedBy": "Athletics Director",
        "status": "official",
        "certificateRef": "CERT-2026-ATH-0144"
    }
]

# 5. Discipline
discipline_cases = [
    {
        "id": "DISC-2026-001",
        "studentId": "2026-STD-0155",
        "studentName": "Heng Piseth",
        "class": "10A",
        "incidentDate": "2026-10-22",
        "category": "Attendance & Unauthorized Departure",
        "severity": "Moderate",
        "reportedBy": "Campus Security & Advisor",
        "description": "Left campus premises during lunch break without authorized gate pass.",
        "actionTaken": "Written Warning & Mandatory Parent Conference",
        "status": "resolved",
        "decisionBy": "Dean of Discipline · Vice Principal",
        "decisionDate": "2026-10-24",
        "notes": "Parent attended meeting. Student placed on 30-day closed campus probation."
    },
    {
        "id": "DISC-2026-002",
        "studentId": "2026-STD-0145",
        "studentName": "Virak Heng",
        "class": "10A",
        "incidentDate": "2026-11-02",
        "category": "Device Policy Violation",
        "severity": "Minor",
        "reportedBy": "Mr. Keo Sambath (Teacher)",
        "description": "Unauthorized gaming on personal smartphone during instructional period.",
        "actionTaken": "Device Confiscation (24h) & Reflection Log",
        "status": "resolved",
        "decisionBy": "Grade 10 Coordinator",
        "decisionDate": "2026-11-03",
        "notes": "First offense. Device returned to student after completion of digital etiquette sheet."
    },
    {
        "id": "DISC-2026-003",
        "studentId": "2026-STD-0148",
        "studentName": "Kosal Rith Mony",
        "class": "10A",
        "incidentDate": "2026-11-07",
        "category": "Academic Integrity / Homework Sharing",
        "severity": "Minor",
        "reportedBy": "Ms. Chheang Voleak (Teacher)",
        "description": "Shared completed lab assignment with classmate prior to formal deadline submission.",
        "actionTaken": "Grade Reduction on Assignment & Counseling Session",
        "status": "under_review",
        "decisionBy": "Pending Department Head Review",
        "decisionDate": None,
        "notes": "Investigation in progress. Advisor speaking with both students."
    }
]

files = [
    ('student_update_requests.json', update_requests),
    ('student_exemptions.json', exemptions),
    ('student_registrations.json', registrations),
    ('student_commendations.json', commendations),
    ('student_discipline.json', discipline_cases)
]

for filename, data in files:
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Created {filename} with {len(data)} records.")

