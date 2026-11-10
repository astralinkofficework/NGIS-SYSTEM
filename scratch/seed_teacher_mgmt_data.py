import os
import json

DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

# 1. Teacher Update Requests
teacher_update_requests = [
    {
        "id": "TUR-2026-001",
        "teacherId": "TCH-2024-015",
        "teacherName": "Dr. Pov Sophea",
        "department": "Science",
        "fieldChanged": "Phone Number & Emergency Contact",
        "previousValue": "+855 12 777 666",
        "proposedValue": "+855 12 999 111",
        "supportingDocument": "Telecom_Carrier_Verification.pdf",
        "submittedDate": "2026-07-05",
        "status": "pending",
        "comments": "Updated primary contact line for campus emergency notifications.",
        "reviewedBy": None,
        "reviewedDate": None
    },
    {
        "id": "TUR-2026-002",
        "teacherId": "TCH-2024-023",
        "teacherName": "Ms. Rin Lina",
        "department": "English",
        "fieldChanged": "Qualifications & Degree",
        "previousValue": "B.Ed English Education (RUPP)",
        "proposedValue": "M.Ed Curriculum & Instruction (Monash University) + CELTA Pass A",
        "supportingDocument": "Monash_Degree_Verification_Official.pdf",
        "submittedDate": "2026-07-04",
        "status": "pending",
        "comments": "Completed graduate degree conferral in June 2026. Requesting profile update and salary step review.",
        "reviewedBy": None,
        "reviewedDate": None
    },
    {
        "id": "TUR-2026-003",
        "teacherId": "TCH-2024-074",
        "teacherName": "Coach Samreth Bora",
        "department": "Arts & Physical Education",
        "fieldChanged": "First Aid & AED Safety Certification",
        "previousValue": "Red Cross Cert #8812 (Expired June 2026)",
        "proposedValue": "Red Cross First Aid / CPR / AED Recertification #9921 (Valid to June 2028)",
        "supportingDocument": "RedCross_Recertification_2026.pdf",
        "submittedDate": "2026-07-03",
        "status": "approved",
        "comments": "Mandatory bi-annual coaching safety certification.",
        "reviewedBy": "Dr. Sophal Meas",
        "reviewedDate": "2026-07-04 10:15"
    },
    {
        "id": "TUR-2026-004",
        "teacherId": "TCH-2024-031",
        "teacherName": "Mr. Chhem Sokha",
        "department": "Khmer Studies",
        "fieldChanged": "Residential Address & Khan Tax Record",
        "previousValue": "#45 St 214, Sangkat Boeung Raing, Daun Penh",
        "proposedValue": "#18 St 337, Sangkat Boeung Kak 1, Tuol Kork",
        "supportingDocument": "Family_Book_Khan_Tuol_Kork.pdf",
        "submittedDate": "2026-07-01",
        "status": "approved",
        "comments": "Relocated closer to primary campus.",
        "reviewedBy": "Mr. Heng Samnang",
        "reviewedDate": "2026-07-02 14:20"
    },
    {
        "id": "TUR-2026-005",
        "teacherId": "TCH-2024-089",
        "teacherName": "Muthukumaran Pakkirisamy",
        "department": "ICT & Computer Science",
        "fieldChanged": "Technical Certification",
        "previousValue": "CompTIA Security+",
        "proposedValue": "AWS Certified Solutions Architect & Cisco Certified Network Associate (CCNA)",
        "supportingDocument": "AWS_CCNA_Digital_Badge_Verification.pdf",
        "submittedDate": "2026-07-06",
        "status": "pending",
        "comments": "Accreditation for teaching senior advanced networking modules.",
        "reviewedBy": None,
        "reviewedDate": None
    }
]

# 2. Teacher Attendance
teacher_attendance = [
    {
        "id": "TAT-2026-001",
        "date": "2026-07-08",
        "teacherId": "TCH-2024-042",
        "teacherName": "Dr. Sarah Jenkins",
        "department": "Mathematics",
        "status": "present",
        "checkIn": "07:35 AM",
        "checkOut": "04:30 PM",
        "biometricTerminal": "Terminal Gate 1 (Faculty)",
        "notes": "On-time arrival; 4 class sessions delivered."
    },
    {
        "id": "TAT-2026-002",
        "date": "2026-07-08",
        "teacherId": "TCH-2024-015",
        "teacherName": "Dr. Pov Sophea",
        "department": "Science",
        "status": "present",
        "checkIn": "07:42 AM",
        "checkOut": "04:45 PM",
        "biometricTerminal": "Terminal Gate 2 (Science Wing)",
        "notes": "Physics lab supervision completed."
    },
    {
        "id": "TAT-2026-003",
        "date": "2026-07-08",
        "teacherId": "TCH-2024-023",
        "teacherName": "Ms. Rin Lina",
        "department": "English",
        "status": "late",
        "checkIn": "08:12 AM",
        "checkOut": "04:30 PM",
        "biometricTerminal": "Terminal Gate 1 (Faculty)",
        "notes": "12 minutes late due to Monivong Blvd traffic congestion. Notice provided."
    },
    {
        "id": "TAT-2026-004",
        "date": "2026-07-08",
        "teacherId": "TCH-2024-031",
        "teacherName": "Mr. Chhem Sokha",
        "department": "Khmer Studies",
        "status": "present",
        "checkIn": "07:28 AM",
        "checkOut": "04:15 PM",
        "biometricTerminal": "Terminal Gate 1 (Faculty)",
        "notes": "Homeroom 11B attendance verified."
    },
    {
        "id": "TAT-2026-005",
        "date": "2026-07-08",
        "teacherId": "TCH-2024-055",
        "teacherName": "Ms. Li Wei",
        "department": "Chinese Language",
        "status": "excused",
        "checkIn": "--",
        "checkOut": "--",
        "biometricTerminal": "N/A",
        "notes": "Official medical leave approved by HR. Class covered by Ms. Rin Lina."
    },
    {
        "id": "TAT-2026-006",
        "date": "2026-07-08",
        "teacherId": "TCH-2024-068",
        "teacherName": "Mr. John Vance",
        "department": "Humanities & Social Sciences",
        "status": "present",
        "checkIn": "07:40 AM",
        "checkOut": "04:20 PM",
        "biometricTerminal": "Terminal Gate 3",
        "notes": "World History exam papers moderated."
    },
    {
        "id": "TAT-2026-007",
        "date": "2026-07-08",
        "teacherId": "TCH-2024-074",
        "teacherName": "Coach Samreth Bora",
        "department": "Arts & Physical Education",
        "status": "duty",
        "checkIn": "07:15 AM",
        "checkOut": "05:30 PM",
        "biometricTerminal": "Sports Complex South",
        "notes": "Field duty — Interschool Athletic Meet official liaison."
    },
    {
        "id": "TAT-2026-008",
        "date": "2026-07-08",
        "teacherId": "TCH-2024-089",
        "teacherName": "Muthukumaran Pakkirisamy",
        "department": "ICT & Computer Science",
        "status": "present",
        "checkIn": "07:30 AM",
        "checkOut": "05:00 PM",
        "biometricTerminal": "Terminal Gate 1 (Faculty)",
        "notes": "Server maintenance and computer lab period."
    }
]

# 3. Teacher Commendations
teacher_commendations = [
    {
        "id": "TCM-2026-001",
        "teacherId": "TCH-2024-015",
        "teacherName": "Dr. Pov Sophea",
        "department": "Science",
        "category": "Curriculum Excellence & STEM Innovation",
        "title": "National STEM Educator Distinction 2026",
        "description": "Awarded for exceptional design of hands-on inquiry physics laboratories and leading student delegation to ASEAN Science Olympiad.",
        "issuingAuthority": "Executive Principal",
        "dateAwarded": "2026-06-25",
        "citation": "Demonstrating exemplary pedagogy, student engagement, and pioneering experimental methodology in secondary science.",
        "certificateRef": "CERT-STEM-2026-015.pdf"
    },
    {
        "id": "TCM-2026-002",
        "teacherId": "TCH-2024-042",
        "teacherName": "Dr. Sarah Jenkins",
        "department": "Mathematics",
        "category": "Academic Mentorship",
        "title": "Mathematics Department Faculty Leadership Citation",
        "description": "Recognized for elevating senior calculus pass rates to 98% and mentoring 4 junior teachers through curriculum accreditation.",
        "issuingAuthority": "Board of Trustees",
        "dateAwarded": "2026-05-30",
        "citation": "Invaluable commitment to faculty development, rigorous mathematical scholarship, and academic distinction.",
        "certificateRef": "CERT-MATH-2026-042.pdf"
    },
    {
        "id": "TCM-2026-003",
        "teacherId": "TCH-2024-031",
        "teacherName": "Mr. Chhem Sokha",
        "department": "Khmer Studies",
        "category": "Cultural Heritage & Civic Leadership",
        "title": "National Khmer Heritage & Literature Preserver Honor",
        "description": "Conferred by MoEYS for organizing inter-school Khmer literature recited recitation contests and classical manuscript digitization.",
        "issuingAuthority": "Ministry of Education MoEYS",
        "dateAwarded": "2026-04-12",
        "citation": "Distinguished service in advancing national linguistic heritage and cultural literacy among Cambodia's youth.",
        "certificateRef": "CERT-MOEYS-2026-031.pdf"
    },
    {
        "id": "TCM-2026-004",
        "teacherId": "TCH-2024-023",
        "teacherName": "Ms. Rin Lina",
        "department": "English",
        "category": "Extracurricular Distinction",
        "title": "Senior Debate Society Championship Coaching Honor",
        "description": "Coached the NGIS Senior Debate Team to first place in the National Model United Nations Invitational.",
        "issuingAuthority": "Executive Principal",
        "dateAwarded": "2026-03-20",
        "citation": "Inspiring student rhetoric, international diplomacy awareness, and ethical argumentation.",
        "certificateRef": "CERT-ENG-2026-023.pdf"
    }
]

# 4. Teacher Discipline
teacher_discipline = [
    {
        "id": "TDS-2026-001",
        "caseNumber": "CAS-2026-0104",
        "teacherId": "TCH-2024-068",
        "teacherName": "Mr. John Vance",
        "department": "Humanities & Social Sciences",
        "category": "Grading Compliance & Record Timeliness",
        "severity": "Level 1 - Formal Reminder",
        "incidentDate": "2026-06-18",
        "description": "Mid-term examination grades for Grade 10 World History submitted 4 business days past the institutional gradebook lockdown deadline.",
        "evidenceDocs": ["Gradebook_Lockdown_Audit_Log.pdf", "Department_Reminder_Notice.pdf"],
        "hearingDate": "2026-06-22",
        "status": "resolved",
        "decisionSummary": "Formal administrative reminder issued. Teacher completed grade reconciliation workshop. Full compliance acknowledged.",
        "confidentialLevel": "Restricted - Admin / Principal Oversight"
    },
    {
        "id": "TDS-2026-002",
        "caseNumber": "CAS-2026-0122",
        "teacherId": "TCH-2024-074",
        "teacherName": "Coach Samreth Bora",
        "department": "Arts & Physical Education",
        "category": "Unannounced Absence & Coverage Delay",
        "severity": "Level 2 - Written Admonition",
        "incidentDate": "2026-06-28",
        "description": "Failure to lodge advance absence notice for morning PE period (08:00 AM) resulting in 20-minute delayed classroom coverage.",
        "evidenceDocs": ["Duty_Roster_Discrepancy.pdf", "Security_Gate_Log.pdf"],
        "hearingDate": "2026-07-02",
        "status": "under_review",
        "decisionSummary": "Hearing conducted with Department Head. Teacher submitted medical documentation; written policy adherence warning logged in personnel file.",
        "confidentialLevel": "Restricted - Admin / Principal Oversight"
    },
    {
        "id": "TDS-2026-003",
        "caseNumber": "CAS-2026-0130",
        "teacherId": "TCH-2024-089",
        "teacherName": "Muthukumaran Pakkirisamy",
        "department": "ICT & Computer Science",
        "category": "Communication Protocol & Parent Inquiry",
        "severity": "Level 1 - Inquiry Review",
        "incidentDate": "2026-07-01",
        "description": "Parent raised inquiry regarding lab assignment grading rubrics and response turnaround time on the parent portal.",
        "evidenceDocs": ["Parent_Inquiry_Ticket_SR881.pdf"],
        "hearingDate": "2026-07-05",
        "status": "resolved",
        "decisionSummary": "Clarification provided. Department rubric shared with parent. Matter amicably reconciled with no disciplinary sanction.",
        "confidentialLevel": "Restricted - Admin / Principal Oversight"
    }
]

# 5. Teacher Efforts
teacher_efforts = [
    {
        "id": "TEF-2026-001",
        "teacherId": "TCH-2024-042",
        "teacherName": "Dr. Sarah Jenkins",
        "department": "Mathematics",
        "category": "Student Support",
        "title": "After-School Mathematics Clinic & Olympiad Coaching",
        "description": "Conducted 12 bi-weekly afternoon remedial sessions for struggling Grade 10 students and coached 4 senior candidates for AMC 10.",
        "hoursSpent": 24,
        "dateLogged": "2026-07-01",
        "supportingDocument": "Math_Clinic_Attendance_Roster.pdf",
        "status": "verified",
        "endorsedBy": "Dr. Sophal Meas"
    },
    {
        "id": "TEF-2026-002",
        "teacherId": "TCH-2024-015",
        "teacherName": "Dr. Pov Sophea",
        "department": "Science",
        "category": "School Activities",
        "title": "Annual Science Fair Committee Chair & Lab Safety Lead",
        "description": "Coordinated logistics, hazardous chemical auditing, 45 student project displays, and liaison with university guest judges.",
        "hoursSpent": 32,
        "dateLogged": "2026-06-28",
        "supportingDocument": "Science_Fair_Program_2026.pdf",
        "status": "endorsed",
        "endorsedBy": "Dr. Sophal Meas"
    },
    {
        "id": "TEF-2026-003",
        "teacherId": "TCH-2024-023",
        "teacherName": "Ms. Rin Lina",
        "department": "English",
        "category": "Academic Contributions",
        "title": "Bilingual Literacy Curriculum Alignment Taskforce",
        "description": "Authored supplementary reading guides aligned with Cambridge Lower Secondary English standards across Grades 7-9.",
        "hoursSpent": 20,
        "dateLogged": "2026-06-20",
        "supportingDocument": "Cambridge_Literacy_Guide_Draft.pdf",
        "status": "verified",
        "endorsedBy": "Mr. Heng Samnang"
    },
    {
        "id": "TEF-2026-004",
        "teacherId": "TCH-2024-031",
        "teacherName": "Mr. Chhem Sokha",
        "department": "Khmer Studies",
        "category": "Department Contributions",
        "title": "Khmer Traditional Arts & Cultural Assembly Director",
        "description": "Supervised student folk dance performances, traditional music rehearsals, and stage design for national cultural day.",
        "hoursSpent": 28,
        "dateLogged": "2026-06-15",
        "supportingDocument": "Cultural_Assembly_Event_Book.pdf",
        "status": "endorsed",
        "endorsedBy": "Dr. Sophal Meas"
    },
    {
        "id": "TEF-2026-005",
        "teacherId": "TCH-2024-089",
        "teacherName": "Muthukumaran Pakkirisamy",
        "department": "ICT & Computer Science",
        "category": "Training & Professional Development",
        "title": "Faculty AI & Digital Classroom Security Workshop",
        "description": "Conducted 3 interactive professional development seminars instructing 42 faculty members on digital gradebook safety and LMS tools.",
        "hoursSpent": 16,
        "dateLogged": "2026-07-03",
        "supportingDocument": "LMS_Workshop_SlideDeck_Feedback.pdf",
        "status": "verified",
        "endorsedBy": "Mr. Heng Samnang"
    }
]

# 6. Teaching Assignments
teaching_assignments = [
    {
        "id": "TAS-2026-001",
        "teacherId": "TCH-2024-042",
        "teacherName": "Dr. Sarah Jenkins",
        "department": "Mathematics",
        "subjectId": "subj-math",
        "subjectName": "Advanced Mathematics",
        "classId": "cls-10a",
        "className": "Grade 10A",
        "periodsPerWeek": 6,
        "room": "Room 302",
        "academicYear": "2025-2026",
        "semester": "Semester 2",
        "status": "active"
    },
    {
        "id": "TAS-2026-002",
        "teacherId": "TCH-2024-042",
        "teacherName": "Dr. Sarah Jenkins",
        "department": "Mathematics",
        "subjectId": "subj-calc",
        "subjectName": "Calculus I",
        "classId": "cls-11b",
        "className": "Grade 11B",
        "periodsPerWeek": 6,
        "room": "Room 304",
        "academicYear": "2025-2026",
        "semester": "Semester 2",
        "status": "active"
    },
    {
        "id": "TAS-2026-003",
        "teacherId": "TCH-2024-015",
        "teacherName": "Dr. Pov Sophea",
        "department": "Science",
        "subjectId": "subj-phys",
        "subjectName": "Physics & Lab",
        "classId": "cls-10a",
        "className": "Grade 10A",
        "periodsPerWeek": 6,
        "room": "Science Lab 1",
        "academicYear": "2025-2026",
        "semester": "Semester 2",
        "status": "active"
    },
    {
        "id": "TAS-2026-004",
        "teacherId": "TCH-2024-015",
        "teacherName": "Dr. Pov Sophea",
        "department": "Science",
        "subjectId": "subj-phys",
        "subjectName": "Physics & Lab",
        "classId": "cls-10b",
        "className": "Grade 10B",
        "periodsPerWeek": 6,
        "room": "Science Lab 1",
        "academicYear": "2025-2026",
        "semester": "Semester 2",
        "status": "active"
    },
    {
        "id": "TAS-2026-005",
        "teacherId": "TCH-2024-023",
        "teacherName": "Ms. Rin Lina",
        "department": "English",
        "subjectId": "subj-eng",
        "subjectName": "English Literature",
        "classId": "cls-10a",
        "className": "Grade 10A",
        "periodsPerWeek": 5,
        "room": "Room 201",
        "academicYear": "2025-2026",
        "semester": "Semester 2",
        "status": "active"
    },
    {
        "id": "TAS-2026-006",
        "teacherId": "TCH-2024-031",
        "teacherName": "Mr. Chhem Sokha",
        "department": "Khmer Studies",
        "subjectId": "subj-khm",
        "subjectName": "Khmer Studies",
        "classId": "cls-10a",
        "className": "Grade 10A",
        "periodsPerWeek": 5,
        "room": "Room 105",
        "academicYear": "2025-2026",
        "semester": "Semester 2",
        "status": "active"
    },
    {
        "id": "TAS-2026-007",
        "teacherId": "TCH-2024-089",
        "teacherName": "Muthukumaran Pakkirisamy",
        "department": "ICT & Computer Science",
        "subjectId": "subj-ict",
        "subjectName": "Computer Science & Coding",
        "classId": "cls-11c",
        "className": "Grade 11C",
        "periodsPerWeek": 5,
        "room": "Computer Lab A",
        "academicYear": "2025-2026",
        "semester": "Semester 2",
        "status": "active"
    },
    {
        "id": "TAS-2026-008",
        "teacherId": "TCH-2024-068",
        "teacherName": "Mr. John Vance",
        "department": "Humanities & Social Sciences",
        "subjectId": "subj-hist",
        "subjectName": "World History & Social Studies",
        "classId": "cls-10b",
        "className": "Grade 10B",
        "periodsPerWeek": 5,
        "room": "Room 208",
        "academicYear": "2025-2026",
        "semester": "Semester 2",
        "status": "active"
    }
]

# Write all JSON files
files_to_write = {
    'data/teacher_update_requests.json': teacher_update_requests,
    'data/teacher_attendance.json': teacher_attendance,
    'data/teacher_commendations.json': teacher_commendations,
    'data/teacher_discipline.json': teacher_discipline,
    'data/teacher_efforts.json': teacher_efforts,
    'data/teacher_assignments.json': teaching_assignments
}

for path, data in files_to_write.items():
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"Written: {path} ({len(data)} records)")

print("Teacher Management seed data generated successfully!")

