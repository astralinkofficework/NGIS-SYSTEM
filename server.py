"""
============================================================
NGIS School Management System — Flask Server
New Gateway International School · 2026
============================================================
Serves the entire static frontend and exposes a lightweight
REST-style API layer for news, notifications, and data.
Run:  python server.py  (or: python -m flask run)
URL:  http://localhost:3000
============================================================
"""

import os
import json
import re
import uuid
import base64
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory, abort
from flask_cors import CORS

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

PORT = int(os.environ.get('PORT', 3000))
ROOT = os.path.dirname(os.path.abspath(__file__))

# ── Security headers ─────────────────────────────────────────────
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    return response

# ── In-memory data store (replaces DB until backend is wired) ──
DB = {
    # ── News ──
    'news': [
        {
            'id': 1, 'title': 'School Sports Day 2026 — All Teams Ready',
            'message': 'Annual sports day is confirmed for July 20. All students must register by July 15.',
            'image': None, 'audience': 'all', 'priority': 'normal',
            'date': '2026-07-04', 'category': 'events', 'pinned': False, 'views': 142, 'published': True
        },
        {
            'id': 2, 'title': 'Mid-Term Exam Schedule Released',
            'message': 'The official mid-term examination timetable for Semester 2, AY 2025-26 has been published.',
            'image': None, 'audience': 'all', 'priority': 'urgent',
            'date': '2026-07-03', 'category': 'exams', 'pinned': True, 'views': 389, 'published': True
        },
        {
            'id': 3, 'title': 'New Library Resources Available',
            'message': 'The digital library has been updated with 200+ new reference materials across all subjects.',
            'image': None, 'audience': 'students', 'priority': 'normal',
            'date': '2026-07-02', 'category': 'academic', 'pinned': False, 'views': 97, 'published': True
        },
        {
            'id': 4, 'title': 'Parent-Teacher Meeting — July 12',
            'message': 'All parents are invited to attend the progress review meeting. Booking required.',
            'image': None, 'audience': 'parents', 'priority': 'normal',
            'date': '2026-07-01', 'category': 'events', 'pinned': False, 'views': 201, 'published': True
        },
        {
            'id': 5, 'title': 'School Closed — National Holiday July 25',
            'message': 'The school will be closed on July 25, 2026 in observance of the national holiday.',
            'image': None, 'audience': 'all', 'priority': 'urgent',
            'date': '2026-06-30', 'category': 'urgent', 'pinned': True, 'views': 512, 'published': True
        },
    ],

    # ── Notifications ──
    'notifications': [
        {'id': 1, 'userId': '2026-STD-0142', 'type': 'assignment', 'title': 'New Assignment: Mathematics Ch.8', 'message': 'Mr. Sophea posted a new assignment due July 10.', 'read': False, 'date': '2026-07-06'},
        {'id': 2, 'userId': '2026-STD-0142', 'type': 'exam',       'title': 'Exam Tomorrow: Physics Mid-Term', 'message': 'Your Physics mid-term exam is scheduled for tomorrow at 8:00 AM.', 'read': False, 'date': '2026-07-05'},
        {'id': 3, 'userId': '2026-STD-0142', 'type': 'grade',      'title': 'Grade Released: Chemistry Practical', 'message': 'Your Chemistry practical assessment result is now available. Score: 88%.', 'read': False, 'date': '2026-07-04'},
        {'id': 4, 'userId': '2026-STD-0142', 'type': 'general',    'title': 'Academic Achievement: Top 5% GPA', 'message': 'Congratulations! You have achieved top 5% GPA in Grade 10 for Semester 1.', 'read': True,  'date': '2026-07-03'},
        {'id': 5, 'userId': '2026-STD-0142', 'type': 'club',       'title': 'Robotics Club: Meeting Tomorrow 3PM', 'message': 'Reminder: Robotics Club weekly session is tomorrow after school.', 'read': True,  'date': '2026-07-02'},
    ],

    # ── Students ──
    'students': [
        {'id': '2026-STD-0142', 'name': 'Nrinphouneta Hok', 'grade': 'Grade 10', 'class': '10A', 'gpa': 3.87, 'attendance': 96, 'status': 'active'},
        {'id': '2026-STD-0143', 'name': 'Kosal Rith Mony',  'grade': 'Grade 11', 'class': '11B', 'gpa': 3.72, 'attendance': 94, 'status': 'active'},
        {'id': '2026-STD-0144', 'name': 'Sophea Chan',      'grade': 'Grade 10', 'class': '10A', 'gpa': 3.55, 'attendance': 91, 'status': 'active'},
    ],

    # ── Clubs ──
    'clubs': [
        {'id': 1, 'name': 'Robotics Club',      'description': 'Build and program robots for competitions.', 'supervisor': 'Mr. Ratanak Som',  'members': 24, 'schedule': 'Every Thursday 3-5 PM', 'capacity': 30, 'icon': 'precision_manufacturing'},
        {'id': 2, 'name': 'Debate Society',     'description': 'Develop critical thinking and public speaking.', 'supervisor': 'Ms. Nary Chan',   'members': 18, 'schedule': 'Every Tuesday 3-4:30 PM', 'capacity': 25, 'icon': 'record_voice_over'},
        {'id': 3, 'name': 'Photography Club',   'description': 'Learn photography and visual storytelling.', 'supervisor': 'Mr. Dara Vin',    'members': 15, 'schedule': 'Every Friday 3-5 PM', 'capacity': 20, 'icon': 'camera_alt'},
        {'id': 4, 'name': 'Math Olympiad',      'description': 'Prepare for national mathematics competitions.', 'supervisor': 'Mr. Chea Sophea', 'members': 12, 'schedule': 'Every Wednesday 3-4 PM', 'capacity': 15, 'icon': 'calculate'},
        {'id': 5, 'name': 'Green Earth Club',   'description': 'Environmental awareness and sustainability.', 'supervisor': 'Ms. Bopha Keo',   'members': 30, 'schedule': 'Every Monday 3-4 PM',  'capacity': 35, 'icon': 'eco'},
        {'id': 6, 'name': 'Drama & Arts Club',  'description': 'Perform, create, and express through art.', 'supervisor': 'Ms. Sreymom Lim',  'members': 22, 'schedule': 'Every Friday 2-4 PM',  'capacity': 30, 'icon': 'theater_comedy'},
    ],

    # ── Lost & Found ──
    'lostFound': [
        {'id': 1, 'type': 'lost',  'item': 'Blue Water Bottle', 'description': '500ml blue Thermos brand, initials \'NK\' scratched on the bottom.', 'location': 'Cafeteria', 'date': '2026-07-04', 'status': 'open',   'photo': None, 'reporter': 'Nrinphouneta Hok'},
        {'id': 2, 'type': 'found', 'item': 'Glasses Case',      'description': 'Black hard-shell glasses case, no glasses inside.',              'location': 'Library',   'date': '2026-07-05', 'status': 'open',   'photo': None, 'reporter': 'Admin Office'},
        {'id': 3, 'type': 'found', 'item': 'USB Flash Drive',   'description': '16GB SanDisk USB, pink color.',                                  'location': 'Room 204',  'date': '2026-07-03', 'status': 'open',   'photo': None, 'reporter': 'Mr. Ratanak Som'},
        {'id': 4, 'type': 'lost',  'item': 'Scientific Calculator', 'description': 'Casio FX-991ES Plus, has a sticker of a cat on the back.', 'location': 'Physics Lab', 'date': '2026-07-02', 'status': 'claimed', 'photo': None, 'reporter': 'Sophea Chan'},
    ],

    # ── Competitions ──
    'competitions': [
        {'id': 1, 'name': 'National Math Olympiad 2026',       'type': 'academic', 'deadline': '2026-07-20', 'date': '2026-08-10', 'eligibility': 'Grade 10-12', 'teamSize': 1, 'status': 'open',   'registered': False},
        {'id': 2, 'name': 'ASEAN Robotics Championship',       'type': 'stem',     'deadline': '2026-07-15', 'date': '2026-08-25', 'eligibility': 'Grade 9-12',  'teamSize': 3, 'status': 'open',   'registered': True},
        {'id': 3, 'name': 'Inter-School Debate Tournament',    'type': 'academic', 'deadline': '2026-07-10', 'date': '2026-07-28', 'eligibility': 'Grade 10-12', 'teamSize': 2, 'status': 'closed', 'registered': False},
        {'id': 4, 'name': 'Photography Exhibition 2026',       'type': 'arts',     'deadline': '2026-07-25', 'date': '2026-08-15', 'eligibility': 'All Grades',  'teamSize': 1, 'status': 'open',   'registered': False},
        {'id': 5, 'name': 'National Science Fair',             'type': 'stem',     'deadline': '2026-08-01', 'date': '2026-08-30', 'eligibility': 'Grade 9-12',  'teamSize': 4, 'status': 'open',   'registered': False},
    ],


    # ── Feedback ──
    'feedback': [],

    # ── Service Requests ──
    'serviceRequests': [
        {'id': 'SR-1001', 'studentId': '2026-STD-0142', 'studentName': 'Nrinphouneta Hok', 'category': 'document', 'type': 'certificate', 'title': 'Perfect Attendance Certificate', 'description': 'Requesting certificate for Semester 1.', 'status': 'completed', 'priority': 'normal', 'campus': 'Sensok', 'assignee': 'Admin Office', 'date': '2026-06-28', 'updatedAt': '2026-06-30', 'comments': [{'by': 'Admin', 'text': 'Approved and generated.', 'date': '2026-06-30'}]},
        {'id': 'SR-1002', 'studentId': '2026-STD-0142', 'studentName': 'Nrinphouneta Hok', 'category': 'academic', 'type': 'class_change', 'title': 'Math Advanced Placement', 'description': 'Request to move to Math AP class for S2.', 'status': 'in_progress', 'priority': 'high', 'campus': 'Sensok', 'assignee': 'Mr. Chea Sophea', 'date': '2026-07-05', 'updatedAt': '2026-07-05', 'comments': []},
        {'id': 'SR-1003', 'studentId': '2026-STD-0143', 'studentName': 'Kosal Rith Mony', 'category': 'administration', 'type': 'status_change', 'title': 'Address Update', 'description': 'Change of residential address.', 'status': 'pending', 'priority': 'normal', 'campus': 'Sensok', 'assignee': '', 'date': '2026-07-06', 'updatedAt': '2026-07-06', 'comments': []},
        {'id': 'SR-1004', 'studentId': '2026-STD-0144', 'studentName': 'Sophea Chan', 'category': 'support', 'type': 'counselor', 'title': 'Counselor Appointment', 'description': 'Need guidance on subject selection.', 'status': 'open', 'priority': 'normal', 'campus': 'TK', 'assignee': '', 'date': '2026-07-06', 'updatedAt': '2026-07-06', 'comments': []},
        {'id': 'SR-1005', 'studentId': '2026-STD-0142', 'studentName': 'Nrinphouneta Hok', 'category': 'document', 'type': 'transcript', 'title': 'Official Transcript', 'description': 'Need transcript for university application.', 'status': 'open', 'priority': 'urgent', 'campus': 'Sensok', 'assignee': '', 'date': '2026-07-07', 'updatedAt': '2026-07-07', 'comments': []},
    ],

    # ── Team Projects ──
    'projects': [
        {
            'id': 1, 'title': 'Physics Group Lab Report — Wave Interference',
            'subject': 'Physics', 'teacher': 'Mr. Dara Vin', 'deadline': '2026-07-14',
            'members': ['Nrinphouneta Hok', 'Kosal Mony', 'Sophea Chan', 'Virak Heng'],
            'tasks': [
                {'id': 't1', 'title': 'Set up experiment apparatus', 'status': 'done',        'assignee': 'Kosal Mony'},
                {'id': 't2', 'title': 'Record wave frequency data',  'status': 'in-progress', 'assignee': 'Nrinphouneta Hok'},
                {'id': 't3', 'title': 'Analyze results',             'status': 'todo',        'assignee': 'Sophea Chan'},
                {'id': 't4', 'title': 'Write final report',          'status': 'todo',        'assignee': 'Virak Heng'},
            ]
        }
    ],

    # ── Teachers ──
    'teachers': [
        {
            'id': 'TCH-2024-042',
            'name': 'Dr. Sarah Jenkins',
            'email': 'teacher@ngis.edu.kh',
            'phone': '+855 12 888 999',
            'department': 'Mathematics',
            'subjects': ['Advanced Mathematics', 'Calculus I'],
            'classes': ['10A', '11B'],
            'homeroom': '10A',
            'status': 'active',
            'avatar': 'https://images.pexels.com/photos/1181686/pexels-photo-1181686.jpeg?auto=compress&cs=tinysrgb&w=80'
        },
        {
            'id': 'TCH-2024-015',
            'name': 'Dr. Pov Sophea',
            'email': 'p.sophea@ngis.edu.kh',
            'phone': '+855 12 777 666',
            'department': 'Science',
            'subjects': ['Physics & Lab'],
            'classes': ['10A', '10B'],
            'homeroom': '10B',
            'status': 'active',
            'avatar': 'https://images.pexels.com/photos/3769021/pexels-photo-3769021.jpeg?auto=compress&cs=tinysrgb&w=80'
        },
        {
            'id': 'TCH-2024-023',
            'name': 'Ms. Rin Lina',
            'email': 'r.lina@ngis.edu.kh',
            'phone': '+855 11 555 444',
            'department': 'English',
            'subjects': ['English Literature'],
            'classes': ['9A', '10A'],
            'homeroom': '9A',
            'status': 'active',
            'avatar': 'https://images.pexels.com/photos/1181685/pexels-photo-1181685.jpeg?auto=compress&cs=tinysrgb&w=80'
        }
    ],

    # ── Parents ──
    'parents': [
        {
            'id': 'PAR-2024-118',
            'name': 'Chan Dara Vuth',
            'email': 'parent@ngis.edu.kh',
            'phone': '+855 12 345 678',
            'address': 'Sensok, Phnom Penh',
            'children': ['2026-STD-0142', '2026-STD-0143'],
            'status': 'active'
        }
    ],

    # ── Staff ──
    'staff': [
        {
            'id': 'STF-2024-019',
            'name': 'Ms. Sreymom Lim',
            'email': 'staff@ngis.edu.kh',
            'phone': '+855 12 444 333',
            'department': 'Campus Operations',
            'role': 'Operations Coordinator',
            'campus': 'Sensok',
            'status': 'active',
            'avatar': 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=80&fit=crop&crop=face'
        }
    ],

    # ── Principals ──
    'principals': [
        {
            'id': 'PRN-2024-002',
            'name': 'Dr. Ly Bunheng',
            'email': 'principal@ngis.edu.kh',
            'phone': '+855 12 999 111',
            'role': 'Campus Principal',
            'campus': 'Sensok & TK',
            'status': 'active',
            'avatar': 'https://images.unsplash.com/photo-1560250097-0b93528c311a?w=80&fit=crop&crop=face'
        }
    ],

    # ── Classes ──
    'classes': [
        {'id': 'cls-10a', 'name': 'Grade 10A', 'grade': '10', 'section': 'A', 'homeroomTeacher': 'Dr. Sarah Jenkins', 'room': 'Room 302', 'studentCount': 32, 'campus': 'Sensok'},
        {'id': 'cls-10b', 'name': 'Grade 10B', 'grade': '10', 'section': 'B', 'homeroomTeacher': 'Dr. Pov Sophea', 'room': 'Room 304', 'studentCount': 30, 'campus': 'Sensok'},
        {'id': 'cls-11a', 'name': 'Grade 11A', 'grade': '11', 'section': 'A', 'homeroomTeacher': 'Ms. Rin Lina', 'room': 'Room 201', 'studentCount': 28, 'campus': 'TK'},
        {'id': 'cls-11b', 'name': 'Grade 11B', 'grade': '11', 'section': 'B', 'homeroomTeacher': 'Dr. Sarah Jenkins', 'room': 'Room 203', 'studentCount': 31, 'campus': 'Sensok'},
    ],

    # ── Assignments ──
    'assignments': [
        {
            'id': 'asgn-001',
            'title': 'Mathematics Ch.8: Differential Equations Problem Set',
            'description': 'Solve problems 1 through 15 on pages 142–145. Show all working clearly.',
            'subjectId': 'subj-math',
            'subject_name': 'Advanced Mathematics',
            'classId': 'cls-10a',
            'class_name': 'Grade 10A',
            'teacher_id': 'TCH-2024-042',
            'teacher_name': 'Dr. Sarah Jenkins',
            'dueDate': '2026-07-20',
            'due_date': '2026-07-20',
            'maxScore': 100,
            'max_score': 100,
            'status': 'published',
            'submissions': [
                {
                    'studentId': '2026-STD-0142',
                    'studentName': 'Nrinphouneta Hok',
                    'submittedAt': '2026-07-06T14:30:00Z',
                    'fileName': 'Math_Ch8_Nrinphouneta.pdf',
                    'score': 95,
                    'feedback': 'Excellent method and step-by-step clarity. Full marks on question 12.',
                    'status': 'graded'
                },
                {
                    'studentId': '2026-STD-0143',
                    'studentName': 'Kosal Rith Mony',
                    'submittedAt': '2026-07-06T16:00:00Z',
                    'fileName': 'Kosal_Math_Set.pdf',
                    'score': 88,
                    'feedback': 'Good overall work. Recheck boundary conditions in problem 7.',
                    'status': 'graded'
                }
            ]
        },
        {
            'id': 'asgn-002',
            'title': 'Physics Lab Report: Wave Interference & Optics',
            'description': 'Write up the full lab report following the IGCSE standard practical writeup structure.',
            'subjectId': 'subj-phys',
            'subject_name': 'Physics & Lab',
            'classId': 'cls-10a',
            'class_name': 'Grade 10A',
            'teacher_id': 'TCH-2024-015',
            'teacher_name': 'Dr. Pov Sophea',
            'dueDate': '2026-07-22',
            'due_date': '2026-07-22',
            'maxScore': 100,
            'max_score': 100,
            'status': 'published',
            'submissions': [
                {
                    'studentId': '2026-STD-0142',
                    'studentName': 'Nrinphouneta Hok',
                    'submittedAt': '2026-07-07T10:15:00Z',
                    'fileName': 'Physics_Optics_Lab_NH.docx',
                    'score': 92,
                    'feedback': 'Thorough error analysis in the conclusion section.',
                    'status': 'graded'
                }
            ]
        },
        {
            'id': 'asgn-003',
            'title': 'English Essay: Comparative Modern Literature',
            'description': 'Write a 1,200-word essay comparing the cultural themes of two contemporary short stories.',
            'subjectId': 'subj-eng',
            'subject_name': 'English Literature',
            'classId': 'cls-10a',
            'class_name': 'Grade 10A',
            'teacher_id': 'TCH-2024-023',
            'teacher_name': 'Ms. Rin Lina',
            'dueDate': '2026-07-25',
            'due_date': '2026-07-25',
            'maxScore': 100,
            'max_score': 100,
            'status': 'published',
            'submissions': []
        }
    ],

    # ── Grades ──
    'grades': [
        {'studentId': '2026-STD-0142', 'studentName': 'Nrinphouneta Hok', 'class': '10A', 'subject': 'Advanced Mathematics', 'grade': 'A', 'score': 95, 'term': 'Term 2', 'teacher': 'Dr. Sarah Jenkins', 'credits': 4.0},
        {'studentId': '2026-STD-0142', 'studentName': 'Nrinphouneta Hok', 'class': '10A', 'subject': 'Physics & Lab', 'grade': 'A', 'score': 92, 'term': 'Term 2', 'teacher': 'Dr. Pov Sophea', 'credits': 4.0},
        {'studentId': '2026-STD-0142', 'studentName': 'Nrinphouneta Hok', 'class': '10A', 'subject': 'English Literature', 'grade': 'A-', 'score': 88, 'term': 'Term 2', 'teacher': 'Ms. Rin Lina', 'credits': 3.0},
        {'studentId': '2026-STD-0142', 'studentName': 'Nrinphouneta Hok', 'class': '10A', 'subject': 'Chemistry Practicum', 'grade': 'A', 'score': 94, 'term': 'Term 2', 'teacher': 'Ms. Sopheap Keo', 'credits': 3.5},
        {'studentId': '2026-STD-0143', 'studentName': 'Kosal Rith Mony', 'class': '11B', 'subject': 'Advanced Mathematics', 'grade': 'B+', 'score': 88, 'term': 'Term 2', 'teacher': 'Dr. Sarah Jenkins', 'credits': 4.0},
        {'studentId': '2026-STD-0143', 'studentName': 'Kosal Rith Mony', 'class': '11B', 'subject': 'Physics & Lab', 'grade': 'A-', 'score': 89, 'term': 'Term 2', 'teacher': 'Dr. Pov Sophea', 'credits': 4.0},
        {'studentId': '2026-STD-0143', 'studentName': 'Kosal Rith Mony', 'class': '11B', 'subject': 'English Literature', 'grade': 'B', 'score': 83, 'term': 'Term 2', 'teacher': 'Ms. Rin Lina', 'credits': 3.0},
        {'studentId': '2026-STD-0144', 'studentName': 'Sophea Chan', 'class': '10A', 'subject': 'Advanced Mathematics', 'grade': 'B+', 'score': 86, 'term': 'Term 2', 'teacher': 'Dr. Sarah Jenkins', 'credits': 4.0},
    ],

    # ── Attendance Records ──
    'attendanceRecords': [
        {'studentId': '2026-STD-0142', 'studentName': 'Nrinphouneta Hok', 'classId': 'cls-10a', 'date': '2026-07-06', 'status': 'present', 'course': 'Advanced Mathematics'},
        {'studentId': '2026-STD-0143', 'studentName': 'Kosal Rith Mony', 'classId': 'cls-11b', 'date': '2026-07-06', 'status': 'present', 'course': 'Advanced Mathematics'},
        {'studentId': '2026-STD-0144', 'studentName': 'Sophea Chan', 'classId': 'cls-10a', 'date': '2026-07-06', 'status': 'late', 'course': 'Advanced Mathematics'},
    ],

    # ── Operational Tasks ──
    'operationalTasks': [
        {'id': 'TSK-001', 'title': 'Inspect cafeteria water filtration system', 'area': 'Sensok Facilities', 'priority': 'high', 'status': 'in_progress', 'assignedTo': 'Ms. Sreymom Lim', 'date': '2026-07-07'},
        {'id': 'TSK-002', 'title': 'Distribute new student ID badges to reception', 'area': 'Administration', 'priority': 'normal', 'status': 'pending', 'assignedTo': 'Front Desk Staff', 'date': '2026-07-07'},
        {'id': 'TSK-003', 'title': 'Science Lab 2 chemical inventory check', 'area': 'Sensok Science Dept', 'priority': 'normal', 'status': 'completed', 'assignedTo': 'Lab Technician', 'date': '2026-07-05'},
    ],

    # ── Lessons & Course Materials ──
    'lessons': [
        {
            'id': 1,
            'title': 'Differential Calculus: Limits & Derivatives',
            'description': 'Foundational rules of differential calculus, continuity criteria, rate of change, and limit theorems.',
            'subjectId': 'subj-math',
            'subject_name': 'Advanced Mathematics',
            'classId': 'cls-10a',
            'class_name': 'Grade 10A',
            'department': 'Mathematics',
            'teacher_id': 'TCH-2024-042',
            'teacher_name': 'Dr. Sarah Jenkins',
            'fileUrl': 'https://www.africau.edu/images/default/sample.pdf',
            'fileName': 'calculus_limits_derivatives.pdf',
            'fileType': 'pdf',
            'date': '2026-07-01',
            'views': 45,
            'status': 'published'
        },
        {
            'id': 2,
            'title': 'Quadratic Functions & Parabolic Curves',
            'description': 'Discriminant analysis, optimization problems, and graph transformations.',
            'subjectId': 'subj-math',
            'subject_name': 'Advanced Mathematics',
            'classId': 'cls-10a',
            'class_name': 'Grade 10A',
            'department': 'Mathematics',
            'teacher_id': 'TCH-2024-042',
            'teacher_name': 'Dr. Sarah Jenkins',
            'fileUrl': 'https://www.africau.edu/images/default/sample.pdf',
            'fileName': 'quadratic_curves.pdf',
            'fileType': 'pdf',
            'date': '2026-07-03',
            'views': 68,
            'status': 'published'
        },
        {
            'id': 3,
            'title': 'Wave Optics & Interference Phenomena',
            'description': 'Wave superposition, diffraction gratings, Young double slit experiment, and photon mechanics.',
            'subjectId': 'subj-phys',
            'subject_name': 'Physics & Lab',
            'classId': 'cls-10a',
            'class_name': 'Grade 10A',
            'department': 'Science',
            'teacher_id': 'TCH-2024-015',
            'teacher_name': 'Dr. Pov Sophea',
            'fileUrl': 'https://www.africau.edu/images/default/sample.pdf',
            'fileName': 'wave_optics_lab.pdf',
            'fileType': 'pdf',
            'date': '2026-07-04',
            'views': 52,
            'status': 'published'
        },
        {
            'id': 4,
            'title': 'Comparative Modern Literature & Rhetoric',
            'description': 'In-depth analysis of prose style, themes of identity, and essay construction.',
            'subjectId': 'subj-eng',
            'subject_name': 'English Literature',
            'classId': 'cls-10a',
            'class_name': 'Grade 10A',
            'department': 'English',
            'teacher_id': 'TCH-2024-023',
            'teacher_name': 'Ms. Rin Lina',
            'fileUrl': 'https://www.africau.edu/images/default/sample.pdf',
            'fileName': 'comparative_lit_guide.pdf',
            'fileType': 'pdf',
            'date': '2026-07-05',
            'views': 37,
            'status': 'published'
        }
    ]
}

_next_id = 100
def new_id():
    global _next_id
    _next_id += 1
    return _next_id

# ── API Routes ───────────────────────────────────────────────

# Health check
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'time': datetime.now().isoformat(),
        'version': '1.0.0',
        'name': 'NGIS School Management System'
    })

# ── NEWS ──
@app.route('/api/news', methods=['GET'])
def get_news():
    audience = request.args.get('audience')
    priority = request.args.get('priority')
    category = request.args.get('category')
    q = request.args.get('q')
    
    items = [n for n in DB['news'] if n['published']]
    
    if audience and audience != 'all':
        items = [n for n in items if n['audience'] == audience or n['audience'] == 'all']
    if priority:
        items = [n for n in items if n['priority'] == priority]
    if category:
        items = [n for n in items if n['category'] == category]
    if q:
        lq = q.lower()
        items = [n for n in items if lq in n['title'].lower() or lq in n['message'].lower()]
    
    items.sort(key=lambda x: (
        not x['pinned'],
        x['priority'] != 'urgent',
        datetime.strptime(x['date'], '%Y-%m-%d'),
    ), reverse=True)
    
    return jsonify({'data': items, 'meta': {'total': len(items)}})

@app.route('/api/news/<int:id>', methods=['GET'])
def get_news_item(id):
    item = next((n for n in DB['news'] if n['id'] == id), None)
    if not item:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'News post not found'}}), 404
    item['views'] = (item.get('views') or 0) + 1
    return jsonify({'data': item})

@app.route('/api/news', methods=['POST'])
def create_news():
    data = request.get_json()
    title = data.get('title')
    message = data.get('message')
    
    if not title or not message:
        return jsonify({'error': {'code': 'VALIDATION_ERROR', 'message': 'title and message are required'}}), 400
    
    item = {
        'id': new_id(),
        'title': title,
        'message': message,
        'audience': data.get('audience', 'all'),
        'priority': data.get('priority', 'normal'),
        'category': data.get('category', 'general'),
        'pinned': data.get('pinned', False),
        'image': data.get('image'),
        'date': datetime.now().strftime('%Y-%m-%d'),
        'views': 0,
        'published': True
    }
    DB['news'].insert(0, item)
    return jsonify({'data': item}), 201

@app.route('/api/news/<int:id>', methods=['PUT'])
def update_news(id):
    idx = next((i for i, n in enumerate(DB['news']) if n['id'] == id), None)
    if idx is None:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'News post not found'}}), 404
    DB['news'][idx].update(request.get_json())
    return jsonify({'data': DB['news'][idx]})

@app.route('/api/news/<int:id>', methods=['DELETE'])
def delete_news(id):
    idx = next((i for i, n in enumerate(DB['news']) if n['id'] == id), None)
    if idx is None:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'News post not found'}}), 404
    deleted = DB['news'].pop(idx)
    return jsonify({'data': deleted, 'message': 'Deleted successfully'})

# ── NOTIFICATIONS ──
@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    user_id = request.args.get('userId')
    items = [n for n in DB['notifications'] if n['userId'] == user_id] if user_id else DB['notifications']
    return jsonify({
        'data': items,
        'meta': {'total': len(items), 'unread': len([n for n in items if not n['read']])}
    })

@app.route('/api/notifications/<int:id>/read', methods=['POST', 'PUT'])
def mark_notification_read(id):
    n = next((n for n in DB['notifications'] if n['id'] == id), None)
    if not n:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Notification not found'}}), 404
    n['read'] = True
    return jsonify({'data': n})

@app.route('/api/notifications/read-all', methods=['POST', 'PUT'])
def mark_all_notifications_read():
    data = request.get_json(silent=True) or {}
    user_id = data.get('userId')
    for n in DB['notifications']:
        if not user_id or n['userId'] == user_id:
            n['read'] = True
    return jsonify({'message': 'All notifications marked as read'})

# ── STUDENTS ──
@app.route('/api/students', methods=['GET'])
def get_students():
    return jsonify({'data': DB['students'], 'meta': {'total': len(DB['students'])}})

@app.route('/api/students/<id>', methods=['GET'])
def get_student(id):
    s = next((s for s in DB['students'] if s['id'] == id), None)
    if not s:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Student not found'}}), 404
    return jsonify({'data': s})

# ── CLUBS ──
@app.route('/api/clubs', methods=['GET'])
def get_clubs():
    return jsonify({'data': DB['clubs'], 'meta': {'total': len(DB['clubs'])}})

@app.route('/api/clubs/<int:id>/join', methods=['POST'])
def join_club(id):
    club = next((c for c in DB['clubs'] if c['id'] == id), None)
    if not club:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Club not found'}}), 404
    if club['members'] >= club['capacity']:
        return jsonify({'error': {'code': 'FULL', 'message': 'Club is at full capacity'}}), 409
    club['members'] += 1
    return jsonify({'data': club, 'message': 'Join request submitted'})

# ── LOST & FOUND (FILE-PERSISTED & SECURE MARKETPLACE) ──
LOST_FOUND_FILE = os.path.join(ROOT, 'data', 'lost_found.json')
UPLOAD_DIR = os.path.join(ROOT, 'assets', 'uploads', 'lostfound')
os.makedirs(UPLOAD_DIR, exist_ok=True)

def load_lost_found_items():
    if not os.path.exists(LOST_FOUND_FILE):
        return []
    try:
        with open(LOST_FOUND_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading lost_found.json: {e}")
        return []

def save_lost_found_items(items):
    try:
        os.makedirs(os.path.dirname(LOST_FOUND_FILE), exist_ok=True)
        with open(LOST_FOUND_FILE, 'w', encoding='utf-8') as f:
            json.dump(items, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving lost_found.json: {e}")
        return False

def sanitize_item_for_user(item, user_role, current_user_id):
    """
    Enforces Section 11 Role-Based Access & Data Security:
    - Staff/Admin/Teacher can view private details, full claims, and audit history.
    - The reporter themselves can view their own item's full details and claims.
    - Other students/public cannot see private identifying evidence or other claimants' private submissions.
    """
    is_staff = user_role in ['admin', 'staff', 'teacher', 'principal']
    is_reporter = current_user_id and str(item.get('reporterId')) == str(current_user_id)
    
    clean = dict(item)
    if not (is_staff or is_reporter):
        if clean.get('privateDetails'):
            clean['privateDetails'] = "[Protected identifying details stored for staff verification]"
        filtered_claims = []
        for c in clean.get('claims', []):
            if current_user_id and str(c.get('claimantId')) == str(current_user_id):
                filtered_claims.append(c)
        clean['claims'] = filtered_claims
    return clean

@app.route('/api/lost-found', methods=['GET'])
def get_lost_found():
    type_ = request.args.get('type')
    category = request.args.get('category')
    status = request.args.get('status')
    campus = request.args.get('campus')
    search = request.args.get('search', '').strip().lower()
    reporter_id = request.args.get('reporterId')
    user_role = request.args.get('role', 'student').lower()
    current_user_id = request.args.get('userId', '')

    items = load_lost_found_items()

    if type_ and type_ != 'all':
        items = [i for i in items if i.get('type') == type_]
    if category and category != 'all':
        items = [i for i in items if i.get('category', '').lower() == category.lower()]
    if status and status != 'all':
        items = [i for i in items if i.get('status', '').lower() == status.lower()]
    if campus and campus != 'all':
        items = [i for i in items if i.get('campus', '').lower() == campus.lower()]
    if reporter_id:
        items = [i for i in items if str(i.get('reporterId')) == str(reporter_id)]
    if search:
        items = [i for i in items if (
            search in i.get('title', '').lower() or
            search in i.get('description', '').lower() or
            search in i.get('location', '').lower() or
            search in i.get('category', '').lower() or
            search in i.get('refId', '').lower()
        )]

    sanitized = [sanitize_item_for_user(i, user_role, current_user_id) for i in items]
    return jsonify({
        'data': sanitized,
        'meta': {
            'total': len(sanitized),
            'filters': {'type': type_, 'category': category, 'status': status, 'campus': campus}
        }
    })

@app.route('/api/lost-found/<int:item_id>', methods=['GET'])
def get_lost_found_item(item_id):
    user_role = request.args.get('role', 'student').lower()
    current_user_id = request.args.get('userId', '')
    items = load_lost_found_items()
    item = next((i for i in items if i.get('id') == item_id), None)
    if not item:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Item not found'}}), 404
    
    clean = sanitize_item_for_user(item, user_role, current_user_id)
    return jsonify({'data': clean})

@app.route('/api/lost-found', methods=['POST'])
def create_lost_found_item():
    data = request.get_json() or {}
    type_ = data.get('type')
    title = data.get('title') or data.get('item')
    category = data.get('category', 'other')
    description = data.get('description', '')
    location = data.get('location', '')
    campus = data.get('campus', 'Sensok')
    date_val = data.get('date', datetime.now().strftime('%Y-%m-%d'))
    time_val = data.get('time', datetime.now().strftime('%I:%M %p'))

    if not type_ or type_ not in ['lost', 'found']:
        return jsonify({'error': {'code': 'VALIDATION_ERROR', 'message': 'Type must be "lost" or "found"'}}), 400
    if not title or not description or not location:
        return jsonify({'error': {'code': 'VALIDATION_ERROR', 'message': 'Title, description, and location are required'}}), 400

    items = load_lost_found_items()
    new_num = max([i.get('id', 100) for i in items], default=100) + 1
    ref_id = f"LF-{datetime.now().year}-{new_num:04d}"

    now_iso = datetime.now().isoformat()
    reporter_id = data.get('reporterId', '2026-STD-0144')
    reporter_name = data.get('reporterName', 'Student User')
    reporter_role = data.get('reporterRole', 'student')

    entry = {
        'id': new_num,
        'refId': ref_id,
        'type': type_,
        'title': title.strip(),
        'category': category.lower(),
        'campus': campus,
        'location': location.strip(),
        'date': date_val,
        'time': time_val,
        'status': 'active',
        'description': description.strip(),
        'privateDetails': data.get('privateDetails', '').strip(),
        'custodyLocation': data.get('custodyLocation', 'With Reporter' if type_ == 'lost' else 'School Reception'),
        'handedToStaff': bool(data.get('handedToStaff', False)),
        'contactMethod': data.get('contactMethod', 'chat'),
        'reporterId': reporter_id,
        'reporterName': reporter_name,
        'reporterRole': reporter_role,
        'reporterGrade': data.get('reporterGrade', 'Student'),
        'image': data.get('image') or data.get('photo') or '',
        'claims': [],
        'auditLog': [
            {
                'action': 'reported',
                'by': reporter_name,
                'role': reporter_role,
                'date': now_iso,
                'notes': f'Initial {type_} report submitted.'
            }
        ],
        'createdAt': now_iso,
        'updatedAt': now_iso
    }

    items.insert(0, entry)
    save_lost_found_items(items)
    return jsonify({'data': entry, 'message': 'Report submitted successfully'}), 201

@app.route('/api/lost-found/<int:item_id>', methods=['PUT'])
def update_lost_found_item(item_id):
    data = request.get_json() or {}
    items = load_lost_found_items()
    item = next((i for i in items if i.get('id') == item_id), None)
    if not item:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Item not found'}}), 404

    updater_name = data.get('updatedBy', 'Staff Member')
    updater_role = data.get('updaterRole', 'staff')
    action_note = data.get('notes', 'Listing updated')

    allowed_fields = ['title', 'category', 'campus', 'location', 'description', 'status', 'custodyLocation', 'handedToStaff', 'privateDetails', 'image']
    for field in allowed_fields:
        if field in data:
            item[field] = data[field]

    now_iso = datetime.now().isoformat()
    item['updatedAt'] = now_iso
    item.setdefault('auditLog', []).append({
        'action': data.get('action', 'updated'),
        'by': updater_name,
        'role': updater_role,
        'date': now_iso,
        'notes': action_note
    })

    save_lost_found_items(items)
    return jsonify({'data': item, 'message': 'Item updated successfully'})

@app.route('/api/lost-found/<int:item_id>/claim', methods=['POST'])
def claim_lost_found_item(item_id):
    data = request.get_json() or {}
    items = load_lost_found_items()
    item = next((i for i in items if i.get('id') == item_id), None)
    if not item:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Item not found'}}), 404

    proof_desc = data.get('proofDescription', '').strip()
    if not proof_desc:
        return jsonify({'error': {'code': 'VALIDATION_ERROR', 'message': 'Ownership proof or distinguishing details required'}}), 400

    now_iso = datetime.now().isoformat()
    claim_id = f"CLM-{int(datetime.now().timestamp()) % 100000}"
    claim = {
        'id': claim_id,
        'claimantId': data.get('claimantId', '2026-STD-0144'),
        'claimantName': data.get('claimantName', 'Student Claimant'),
        'claimantRole': data.get('claimantRole', 'student'),
        'claimantGrade': data.get('claimantGrade', 'Student'),
        'proofDescription': proof_desc,
        'status': 'under_review',
        'contactMethod': data.get('contactMethod', 'chat'),
        'submittedAt': now_iso,
        'staffNotes': ''
    }

    item.setdefault('claims', []).append(claim)
    if item['status'] == 'active':
        item['status'] = 'matching'
    item['updatedAt'] = now_iso
    item.setdefault('auditLog', []).append({
        'action': 'claim_submitted',
        'by': claim['claimantName'],
        'role': claim['claimantRole'],
        'date': now_iso,
        'notes': f'Claim #{claim_id} submitted with private proof.'
    })

    save_lost_found_items(items)
    return jsonify({'data': claim, 'message': 'Ownership claim submitted successfully. Staff will review your evidence.'}), 201

@app.route('/api/lost-found/<int:item_id>/claims/<claim_id>', methods=['PUT'])
def review_claim(item_id, claim_id):
    data = request.get_json() or {}
    items = load_lost_found_items()
    item = next((i for i in items if i.get('id') == item_id), None)
    if not item:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Item not found'}}), 404

    claim = next((c for c in item.get('claims', []) if str(c.get('id')) == str(claim_id)), None)
    if not claim:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Claim not found'}}), 404

    new_status = data.get('status')
    staff_notes = data.get('staffNotes', '').strip()
    reviewer_name = data.get('reviewerName', 'Lost & Found Staff')
    reviewer_role = data.get('reviewerRole', 'staff')

    if new_status in ['approved', 'rejected', 'verified', 'ready_for_collection']:
        claim['status'] = new_status
        claim['staffNotes'] = staff_notes
        now_iso = datetime.now().isoformat()
        claim['reviewedAt'] = now_iso
        claim['reviewedBy'] = reviewer_name

        if new_status in ['approved', 'ready_for_collection']:
            item['status'] = 'ready_for_collection'
        elif new_status == 'rejected' and all(c.get('status') == 'rejected' for c in item.get('claims', [])):
            item['status'] = 'active'

        item['updatedAt'] = now_iso
        item.setdefault('auditLog', []).append({
            'action': f'claim_{new_status}',
            'by': reviewer_name,
            'role': reviewer_role,
            'date': now_iso,
            'notes': f'Claim #{claim_id} set to {new_status}. {staff_notes}'
        })

        save_lost_found_items(items)
        return jsonify({'data': claim, 'message': f'Claim status updated to {new_status}'})

    return jsonify({'error': {'code': 'INVALID_STATUS', 'message': 'Invalid claim status'}}), 400

@app.route('/api/lost-found/<int:item_id>/return', methods=['POST'])
def return_lost_found_item(item_id):
    data = request.get_json() or {}
    items = load_lost_found_items()
    item = next((i for i in items if i.get('id') == item_id), None)
    if not item:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Item not found'}}), 404

    handed_to = data.get('handedOverTo', 'Verified Owner')
    staff_name = data.get('handedOverBy', 'Authorized Staff')
    staff_role = data.get('staffRole', 'staff')
    handover_loc = data.get('handoverLocation', 'Main Reception Desk')
    notes = data.get('notes', 'Physical item successfully handed over and signed.')

    now_iso = datetime.now().isoformat()
    item['status'] = 'returned'
    item['custodyLocation'] = f'Returned to {handed_to}'
    item['updatedAt'] = now_iso
    item.setdefault('auditLog', []).append({
        'action': 'returned',
        'by': staff_name,
        'role': staff_role,
        'date': now_iso,
        'notes': f'Item returned to {handed_to} at {handover_loc}. {notes}'
    })

    save_lost_found_items(items)
    return jsonify({'data': item, 'message': 'Item successfully marked as returned and case closed.'})

@app.route('/api/lost-found/<int:item_id>/matches', methods=['GET'])
def get_lost_found_matches(item_id):
    items = load_lost_found_items()
    target = next((i for i in items if i.get('id') == item_id), None)
    if not target:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Item not found'}}), 404

    opposite_type = 'found' if target.get('type') == 'lost' else 'lost'
    candidates = [i for i in items if i.get('type') == opposite_type and i.get('status') != 'archived']

    def tokenize(text):
        return set(w for w in re.findall(r'[a-zA-Z0-9]{3,}', (text or '').lower()) if w not in {'with', 'from', 'room', 'floor', 'hall', 'near', 'the', 'and', 'for'})

    target_tokens = tokenize(target.get('title', '') + ' ' + target.get('description', ''))
    scored_matches = []

    for cand in candidates:
        score = 0
        reasons = []

        if cand.get('category', '').lower() == target.get('category', '').lower():
            score += 40
            reasons.append(f"Matching category: {cand.get('category').capitalize()}")

        if cand.get('campus', '').lower() == target.get('campus', '').lower():
            score += 20
            reasons.append(f"Same campus: {cand.get('campus')}")

        cand_tokens = tokenize(cand.get('title', '') + ' ' + cand.get('description', ''))
        common = target_tokens.intersection(cand_tokens)
        if common:
            kw_points = min(30, len(common) * 10)
            score += kw_points
            reasons.append(f"Keyword matches: {', '.join(list(common)[:4])}")

        try:
            d1 = datetime.strptime(target.get('date'), '%Y-%m-%d')
            d2 = datetime.strptime(cand.get('date'), '%Y-%m-%d')
            diff_days = abs((d1 - d2).days)
            if diff_days <= 3:
                score += 10
                reasons.append(f"Reported within {diff_days} days of each other")
        except:
            pass

        if score >= 40:
            scored_matches.append({
                'item': cand,
                'score': min(100, score),
                'reasons': reasons
            })

    scored_matches.sort(key=lambda x: x['score'], reverse=True)
    return jsonify({'data': scored_matches[:6]})

@app.route('/api/lost-found/upload', methods=['POST'])
def upload_lost_found_photo():
    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': {'code': 'EMPTY_FILE', 'message': 'No file selected'}}), 400
        ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else 'jpg'
        if ext not in ['jpg', 'jpeg', 'png', 'webp']:
            return jsonify({'error': {'code': 'INVALID_TYPE', 'message': 'Only JPG, PNG, and WebP images allowed'}}), 400
        
        filename = f"lf_{int(datetime.now().timestamp())}_{uuid.uuid4().hex[:6]}.{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        file.save(filepath)
        url = f"assets/uploads/lostfound/{filename}"
        return jsonify({'url': url, 'message': 'Photo uploaded successfully'})

    data = request.get_json() or {}
    base64_data = data.get('image')
    if base64_data and 'base64,' in base64_data:
        try:
            header, encoded = base64_data.split('base64,', 1)
            ext = 'png' if 'png' in header else 'jpg'
            decoded = base64.b64decode(encoded)
            filename = f"lf_{int(datetime.now().timestamp())}_{uuid.uuid4().hex[:6]}.{ext}"
            filepath = os.path.join(UPLOAD_DIR, filename)
            with open(filepath, 'wb') as f:
                f.write(decoded)
            url = f"assets/uploads/lostfound/{filename}"
            return jsonify({'url': url, 'message': 'Photo uploaded successfully'})
        except Exception as e:
            return jsonify({'error': {'code': 'UPLOAD_FAILED', 'message': str(e)}}), 500

    return jsonify({'error': {'code': 'NO_IMAGE', 'message': 'No image data provided'}}), 400

@app.route('/api/lost-found/stats', methods=['GET'])
def get_lost_found_stats():
    items = load_lost_found_items()
    user_id = request.args.get('userId', '2026-STD-0144')
    stats = {
        'total': len(items),
        'lost': len([i for i in items if i.get('type') == 'lost']),
        'found': len([i for i in items if i.get('type') == 'found']),
        'active': len([i for i in items if i.get('status') == 'active']),
        'matching': len([i for i in items if i.get('status') == 'matching']),
        'ready': len([i for i in items if i.get('status') == 'ready_for_collection']),
        'returned': len([i for i in items if i.get('status') == 'returned']),
        'myReports': len([i for i in items if str(i.get('reporterId')) == str(user_id)]),
    }
    return jsonify({'data': stats})

# ── COMPETITIONS ──
@app.route('/api/competitions', methods=['GET'])
def get_competitions():
    return jsonify({'data': DB['competitions'], 'meta': {'total': len(DB['competitions'])}})

@app.route('/api/competitions/<int:id>/register', methods=['POST'])
def register_competition(id):
    comp = next((c for c in DB['competitions'] if c['id'] == id), None)
    if not comp:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Competition not found'}}), 404
    if comp['status'] == 'closed':
        return jsonify({'error': {'code': 'CLOSED', 'message': 'Registration is closed'}}), 409
    comp['registered'] = True
    return jsonify({'data': comp, 'message': 'Registered successfully'})


# ── FEEDBACK ──
@app.route('/api/feedback', methods=['POST'])
def create_feedback():
    data = request.get_json()
    message = data.get('message')
    anonymous = data.get('anonymous')
    category = data.get('category')
    
    if not message:
        return jsonify({'error': {'code': 'VALIDATION_ERROR', 'message': 'message is required'}}), 400
    
    entry = {
        'id': new_id(),
        'message': message,
        'category': category or 'general',
        'anonymous': bool(anonymous),
        'status': 'submitted',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'reporter': 'Anonymous' if anonymous else (data.get('reporter', 'Student'))
    }
    DB['feedback'].append(entry)
    return jsonify({'data': entry, 'message': 'Feedback submitted successfully'}), 201

# ── SERVICE REQUESTS ──
@app.route('/api/service-requests', methods=['GET'])
def get_service_requests():
    status = request.args.get('status')
    category = request.args.get('category')
    type_ = request.args.get('type')
    campus = request.args.get('campus')
    student_id = request.args.get('studentId')
    
    items = DB['serviceRequests']
    if status and status != 'all':
        items = [r for r in items if r['status'] == status]
    if category:
        items = [r for r in items if r['category'] == category]
    if type_:
        items = [r for r in items if r['type'] == type_]
    if campus:
        items = [r for r in items if r['campus'] == campus]
    if student_id:
        items = [r for r in items if r['studentId'] == student_id]
    
    items.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)
    return jsonify({'data': items, 'meta': {'total': len(items)}})

@app.route('/api/service-requests/<id>', methods=['GET'])
def get_service_request(id):
    item = next((r for r in DB['serviceRequests'] if r['id'] == id), None)
    if not item:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Service request not found'}}), 404
    return jsonify({'data': item})

@app.route('/api/service-requests', methods=['POST'])
def create_service_request():
    data = request.get_json()
    student_id = data.get('studentId')
    student_name = data.get('studentName')
    category = data.get('category')
    type_ = data.get('type')
    title = data.get('title')
    description = data.get('description')
    priority = data.get('priority')
    campus = data.get('campus')
    
    if not student_id or not category or not type_ or not title:
        return jsonify({'error': {'code': 'VALIDATION_ERROR', 'message': 'studentId, category, type, and title are required'}}), 400
    
    id = f"SR-{1000 + len(DB['serviceRequests']) + 1}"
    entry = {
        'id': id,
        'studentId': student_id,
        'studentName': student_name or 'Student',
        'category': category,
        'type': type_,
        'title': title,
        'description': description or '',
        'status': 'open',
        'priority': priority or 'normal',
        'campus': campus or 'Sensok',
        'assignee': '',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'updatedAt': datetime.now().strftime('%Y-%m-%d'),
        'comments': []
    }
    DB['serviceRequests'].append(entry)
    return jsonify({'data': entry, 'message': 'Service request submitted'}), 201

@app.route('/api/service-requests/<id>', methods=['PUT'])
def update_service_request(id):
    idx = next((i for i, r in enumerate(DB['serviceRequests']) if r['id'] == id), None)
    if idx is None:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Service request not found'}}), 404
    
    data = request.get_json()
    allowed = ['status', 'priority', 'assignee', 'campus']
    for field in allowed:
        if field in data:
            DB['serviceRequests'][idx][field] = data[field]
    
    if 'comment' in data:
        DB['serviceRequests'][idx]['comments'].append({
            'by': data.get('commentBy', 'Admin'),
            'text': data['comment'],
            'date': datetime.now().strftime('%Y-%m-%d')
        })
    
    DB['serviceRequests'][idx]['updatedAt'] = datetime.now().strftime('%Y-%m-%d')
    return jsonify({'data': DB['serviceRequests'][idx]})

@app.route('/api/service-requests/<id>', methods=['DELETE'])
def delete_service_request(id):
    idx = next((i for i, r in enumerate(DB['serviceRequests']) if r['id'] == id), None)
    if idx is None:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Service request not found'}}), 404
    DB['serviceRequests'].pop(idx)
    return jsonify({'data': None, 'message': 'Deleted successfully'})

# ── DASHBOARD SUMMARY ──
@app.route('/api/projects', methods=['GET'])
def get_projects():
    return jsonify({'data': DB['projects'], 'meta': {'total': len(DB['projects'])}})

@app.route('/api/projects/<int:pid>/tasks/<tid>', methods=['PUT'])
def update_project_task(pid, tid):
    project = next((p for p in DB['projects'] if p['id'] == pid), None)
    if not project:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Project not found'}}), 404
    task = next((t for t in project['tasks'] if t['id'] == tid), None)
    if not task:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Task not found'}}), 404
    
    data = request.get_json()
    if 'status' in data:
        task['status'] = data['status']
    if 'title' in data:
        task['title'] = data['title']
    
    return jsonify({'data': project})

@app.route('/api/dashboard/<role>', methods=['GET'])
def get_dashboard(role):
    base = {
        'role': role,
        'date': datetime.now().isoformat(),
        'unreadNotifications': len([n for n in DB['notifications'] if not n['read']]),
        'news': [n for n in DB['news'] if n['published'] and n['pinned']][:3],
    }
    
    if role == 'student':
        base.update({
            'student': DB['students'][0],
            'upcomingExams': 6,
            'pendingAssignments': len([a for a in DB['assignments'] if a.get('classId') == 'cls-10a' and not any(s.get('studentId') == '2026-STD-0142' for s in a.get('submissions', []))]),
            'attendanceRate': 96.2,
            'gpa': 3.87,
            'clubs': DB['clubs'][:2],
            'serviceRequests': len([r for r in DB['serviceRequests'] if r['studentId'] == '2026-STD-0142']),
        })
    elif role == 'teacher':
        base.update({
            'teacher': DB['teachers'][0],
            'assignedClasses': ['10A', '11B'],
            'totalStudents': 63,
            'pendingGrading': len([a for a in DB['assignments'] if any(s.get('status') == 'submitted' for s in a.get('submissions', []))]),
            'averageClassScore': 87.4,
            'attendanceRate': 93.8,
            'classes': DB['classes'][:2]
        })
    elif role == 'parent':
        base.update({
            'parent': DB['parents'][0],
            'children': [s for s in DB['students'] if s['id'] in DB['parents'][0]['children']],
            'activeChild': DB['students'][0],
            'attendanceRate': 96.2,
            'pendingHomework': 1,
            'totalFeesDue': 0,
            'reportCards': 2
        })
    elif role == 'staff':
        base.update({
            'staff': DB['staff'][0],
            'openServiceRequests': len([r for r in DB['serviceRequests'] if r['status'] in ['open', 'pending']]),
            'lostFoundPending': len([i for i in DB['lostFound'] if i.get('status') in ['active', 'matching']]),
            'operationalTasks': len([t for t in DB['operationalTasks'] if t['status'] != 'completed']),
            'campusFacilitiesReady': '100%'
        })
    elif role == 'principal':
        base.update({
            'principal': DB['principals'][0],
            'totalStudents': 1250,
            'totalTeachers': len(DB['teachers']),
            'campusAttendance': 95.4,
            'overallGpa': 3.62,
            'pendingApprovals': 4,
            'academicHonorsRate': '24.2%'
        })
    elif role == 'admin':
        base.update({
            'totalStudents': len(DB['students']),
            'totalClubs': len(DB['clubs']),
            'openLostFound': len([i for i in DB['lostFound'] if i['status'] == 'open']),
            'openServiceRequests': len([r for r in DB['serviceRequests'] if r['status'] in ['open', 'pending']]),
            'totalServiceRequests': len(DB['serviceRequests']),
        })
    
    return jsonify({'data': base})

# ── AUTH & USER SESSION ENDPOINTS ──
AUTH_USERS = {
    'admin@ngis.edu.kh': {
        'id': 'ADM-2024-001',
        'firstName': 'Sok Panha',
        'lastName': 'Heng',
        'email': 'admin@ngis.edu.kh',
        'role': 'admin',
        'portal': 'admin',
        'avatar': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=80&fit=crop&crop=face'
    },
    'teacher@ngis.edu.kh': {
        'id': 'TCH-2024-042',
        'firstName': 'Dr. Sarah',
        'lastName': 'Jenkins',
        'email': 'teacher@ngis.edu.kh',
        'role': 'teacher',
        'portal': 'teacher',
        'avatar': 'https://images.pexels.com/photos/1181686/pexels-photo-1181686.jpeg?auto=compress&cs=tinysrgb&w=80'
    },
    'student@ngis.edu.kh': {
        'id': 'STU-2024-089',
        'firstName': 'Nrinphouneta',
        'lastName': 'Hok',
        'email': 'student@ngis.edu.kh',
        'role': 'student',
        'portal': 'student',
        'avatar': 'https://images.pexels.com/photos/3785079/pexels-photo-3785079.jpeg?auto=compress&cs=tinysrgb&w=80'
    },
    'parent@ngis.edu.kh': {
        'id': 'PAR-2024-118',
        'firstName': 'Chan Dara',
        'lastName': 'Vuth',
        'email': 'parent@ngis.edu.kh',
        'role': 'parent',
        'portal': 'parent',
        'avatar': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=80&fit=crop&crop=face'
    },
    'staff@ngis.edu.kh': {
        'id': 'STF-2024-019',
        'firstName': 'Sreymom',
        'lastName': 'Lim',
        'email': 'staff@ngis.edu.kh',
        'role': 'staff',
        'portal': 'staff',
        'avatar': 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=80&fit=crop&crop=face'
    },
    'principal@ngis.edu.kh': {
        'id': 'PRN-2024-002',
        'firstName': 'Dr. Ly',
        'lastName': 'Bunheng',
        'email': 'principal@ngis.edu.kh',
        'role': 'principal',
        'portal': 'principal',
        'avatar': 'https://images.unsplash.com/photo-1560250097-0b93528c311a?w=80&fit=crop&crop=face'
    }
}

@app.route('/api/auth/login', methods=['POST'])
def auth_login():
    data = request.get_json(silent=True) or {}
    email = data.get('email', '').strip().lower()
    user = AUTH_USERS.get(email)
    if not user:
        if 'teacher' in email:
            user = AUTH_USERS['teacher@ngis.edu.kh']
        elif 'student' in email:
            user = AUTH_USERS['student@ngis.edu.kh']
        elif 'parent' in email:
            user = AUTH_USERS['parent@ngis.edu.kh']
        elif 'staff' in email:
            user = AUTH_USERS['staff@ngis.edu.kh']
        elif 'principal' in email:
            user = AUTH_USERS['principal@ngis.edu.kh']
        else:
            user = AUTH_USERS['admin@ngis.edu.kh']
            
    token = f"mock-jwt-token-{user['role']}"
    return jsonify({
        'data': {
            'token': token,
            'user': user
        }
    })

@app.route('/api/auth/me', methods=['GET'])
def auth_me():
    auth_header = request.headers.get('Authorization', '')
    role = 'admin'
    for r in ['admin', 'teacher', 'student', 'parent', 'staff', 'principal']:
        if f'mock-jwt-token-{r}' in auth_header or f'role-{r}' in auth_header:
            role = r
            break
            
    email_map = {
        'admin': 'admin@ngis.edu.kh',
        'teacher': 'teacher@ngis.edu.kh',
        'student': 'student@ngis.edu.kh',
        'parent': 'parent@ngis.edu.kh',
        'staff': 'staff@ngis.edu.kh',
        'principal': 'principal@ngis.edu.kh'
    }
    user = AUTH_USERS.get(email_map.get(role, 'admin@ngis.edu.kh'))
    return jsonify({'data': user})

# ── CONNECTED ROLE-SPECIFIC APIS ──
@app.route('/api/teacher/me', methods=['GET'])
def get_teacher_me():
    return jsonify({
        'data': {
            'teacher': DB['teachers'][0],
            'user': AUTH_USERS['teacher@ngis.edu.kh'],
            'classes': DB['classes'][:2],
            'subjects': DB['teachers'][0]['subjects']
        }
    })

@app.route('/api/teacher/classes', methods=['GET'])
def get_teacher_classes():
    return jsonify({'data': DB['classes'][:2], 'meta': {'total': 2}})

@app.route('/api/student/dashboard', methods=['GET'])
def get_student_dashboard():
    return jsonify({
        'data': {
            'student': {
                'id': '2026-STD-0142',
                'name': 'Nrinphouneta Hok',
                'grade': 'Grade 10',
                'class': '10A',
                'class_id': 'cls-10a',
                'student_number': '2026-STD-0142',
                'attendance_rate': 96.2,
                'gpa': 3.87,
                'status': 'active'
            },
            'user': AUTH_USERS['student@ngis.edu.kh'],
            'unreadNotifications': 2,
            'gpa': 3.87,
            'attendanceRate': 96.2
        }
    })

@app.route('/api/parent/children', methods=['GET'])
def get_parent_children():
    linked_ids = DB['parents'][0].get('children', [])
    children = []
    for s in DB['students']:
        if s['id'] in linked_ids:
            parts = s['name'].split()
            children.append({
                'id': s['id'],
                'student_id': s['id'],
                'student_number': s['id'],
                'first_name': parts[0],
                'last_name': ' '.join(parts[1:]),
                'name': s['name'],
                'grade': s['grade'],
                'class': s['class'],
                'class_name': f"Grade {s['class']}",
                'gpa': s['gpa'],
                'attendance_rate': s['attendance'],
                'status': s['status']
            })
    return jsonify({'data': children, 'meta': {'total': len(children)}})

@app.route('/api/parent/children/<student_id>', methods=['GET'])
def get_parent_child(student_id):
    s = next((s for s in DB['students'] if s['id'] == student_id), None)
    if not s:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Child not found'}}), 404
    parts = s['name'].split()
    child = {
        'id': s['id'],
        'student_id': s['id'],
        'student_number': s['id'],
        'first_name': parts[0],
        'last_name': ' '.join(parts[1:]),
        'name': s['name'],
        'grade': s['grade'],
        'class': s['class'],
        'class_name': f"Grade {s['class']}",
        'gpa': s['gpa'],
        'attendance_rate': s['attendance'],
        'status': s['status']
    }
    return jsonify({'data': child})

@app.route('/api/parent/children/<student_id>/grades', methods=['GET'])
def get_parent_child_grades(student_id):
    grades = [g for g in DB['grades'] if g.get('studentId') == student_id]
    return jsonify({'data': grades, 'meta': {'total': len(grades)}})

@app.route('/api/parent/children/<student_id>/attendance', methods=['GET'])
def get_parent_child_attendance(student_id):
    records = [a for a in DB['attendanceRecords'] if a.get('studentId') == student_id]
    return jsonify({
        'data': {
            'rate': 96.2,
            'history': records or [
                {'date': '2026-07-06', 'status': 'present', 'course': 'Advanced Mathematics'},
                {'date': '2026-07-05', 'status': 'present', 'course': 'Physics & Lab'},
                {'date': '2026-07-04', 'status': 'present', 'course': 'English Literature'},
                {'date': '2026-07-03', 'status': 'late', 'course': 'Chemistry Practicum'},
            ]
        }
    })

@app.route('/api/parent/children/<student_id>/assignments', methods=['GET'])
def get_parent_child_assignments(student_id):
    s = next((s for s in DB['students'] if s['id'] == student_id), None)
    class_name = s.get('class', '') if s else ''
    matched = []
    for a in DB['assignments']:
        sub = next((sb for sb in a.get('submissions', []) if sb.get('studentId') == student_id), None)
        is_match = (
            sub is not None or
            (a.get('classId') == 'cls-11b' and '11' in class_name) or
            (a.get('classId') == 'cls-10a' and '10' in class_name) or
            (bool(class_name) and class_name.lower() in (a.get('class_name') or '').lower())
        )
        if is_match:
            matched.append({
                'id': a['id'],
                'title': a['title'],
                'subject_name': a.get('subject_name', ''),
                'dueDate': a.get('dueDate', ''),
                'due_date': a.get('due_date', ''),
                'status': 'graded' if (sub and sub.get('status') == 'graded') else ('submitted' if sub else 'pending'),
                'score': sub.get('score') if sub else None,
                'maxScore': a.get('maxScore', 100),
                'feedback': sub.get('feedback') if sub else None
            })
    return jsonify({'data': matched, 'meta': {'total': len(matched)}})

# ── LESSONS MANAGEMENT API ──
@app.route('/api/lessons', methods=['GET', 'POST'])
def handle_lessons():
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        title = data.get('title')
        if not title:
            return jsonify({'error': {'code': 'VALIDATION_ERROR', 'message': 'Lesson title is required'}}), 400

        class_id = data.get('classId', 'cls-10a')
        class_obj = next((c for c in DB['classes'] if c['id'] == class_id), None)
        class_name = class_obj['name'] if class_obj else data.get('class_name', 'Grade 10A')

        new_lesson = {
            'id': new_id(),
            'title': title.strip(),
            'description': data.get('description', ''),
            'subjectId': data.get('subjectId', 'subj-math'),
            'subject_name': data.get('subject_name') or 'Advanced Mathematics',
            'classId': class_id,
            'class_name': class_name,
            'department': data.get('department', 'Mathematics'),
            'teacher_id': data.get('teacher_id', 'TCH-2024-042'),
            'teacher_name': data.get('teacher_name', 'Dr. Sarah Jenkins'),
            'fileUrl': data.get('fileUrl', 'https://www.africau.edu/images/default/sample.pdf'),
            'fileName': data.get('fileName', 'lesson_material.pdf'),
            'fileType': data.get('fileType', 'pdf'),
            'date': data.get('date', datetime.now().strftime('%Y-%m-%d')),
            'views': 0,
            'status': data.get('status', 'published')
        }
        DB['lessons'].insert(0, new_lesson)
        return jsonify({'data': new_lesson, 'message': 'Lesson created successfully'}), 201

    class_id = request.args.get('classId')
    teacher_id = request.args.get('teacherId')
    dept = request.args.get('department')
    q = request.args.get('q')

    items = list(DB['lessons'])
    if class_id:
        items = [l for l in items if l.get('classId') == class_id]
    if teacher_id:
        items = [l for l in items if l.get('teacher_id') == teacher_id]
    if dept and dept != 'all':
        items = [l for l in items if l.get('department', '').lower() == dept.lower()]
    if q:
        lq = q.lower()
        items = [l for l in items if lq in l.get('title', '').lower() or lq in l.get('description', '').lower()]

    return jsonify({'data': items, 'meta': {'total': len(items)}})

@app.route('/api/lessons/<int:lesson_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_lesson_item(lesson_id):
    idx = next((i for i, l in enumerate(DB['lessons']) if l['id'] == lesson_id), None)
    if idx is None:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Lesson not found'}}), 404

    if request.method == 'GET':
        item = DB['lessons'][idx]
        item['views'] = item.get('views', 0) + 1
        return jsonify({'data': item})

    if request.method == 'PUT':
        data = request.get_json(silent=True) or {}
        DB['lessons'][idx].update(data)
        return jsonify({'data': DB['lessons'][idx], 'message': 'Lesson updated successfully'})

    if request.method == 'DELETE':
        deleted = DB['lessons'].pop(idx)
        return jsonify({'data': deleted, 'message': 'Lesson deleted successfully'})

# ── ASSIGNMENTS MANAGEMENT API ──
@app.route('/api/assignments', methods=['GET', 'POST'])
def handle_assignments():
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        title = data.get('title')
        if not title:
            return jsonify({'error': {'code': 'VALIDATION_ERROR', 'message': 'Title is required'}}), 400

        class_id = data.get('classId', 'cls-10a')
        class_obj = next((c for c in DB['classes'] if c['id'] == class_id), None)
        class_name = class_obj['name'] if class_obj else 'Grade 10A'

        new_item = {
            'id': f"asgn-{len(DB['assignments']) + 1:03d}",
            'title': title.strip(),
            'description': data.get('description', ''),
            'subjectId': data.get('subjectId', 'subj-math'),
            'subject_name': data.get('subject_name') or 'Advanced Mathematics',
            'classId': class_id,
            'class_name': class_name,
            'teacher_id': data.get('teacher_id', 'TCH-2024-042'),
            'teacher_name': data.get('teacher_name', 'Dr. Sarah Jenkins'),
            'dueDate': data.get('dueDate', '2026-07-28'),
            'due_date': data.get('dueDate', '2026-07-28'),
            'maxScore': int(data.get('maxScore', 100)),
            'max_score': int(data.get('maxScore', 100)),
            'status': data.get('status', 'published'),
            'submissions': []
        }
        DB['assignments'].insert(0, new_item)
        return jsonify({'data': new_item, 'message': 'Assignment created successfully'}), 201

    class_id = request.args.get('classId')
    teacher_id = request.args.get('teacherId')
    
    items = list(DB['assignments'])
    if class_id:
        items = [a for a in items if a.get('classId') == class_id]
    if teacher_id:
        items = [a for a in items if a.get('teacher_id') == teacher_id]
        
    return jsonify({'data': items, 'meta': {'total': len(items)}})

@app.route('/api/assignments/<asgn_id>/grade', methods=['POST'])
def grade_assignment(asgn_id):
    data = request.get_json(silent=True) or {}
    student_id = data.get('studentId', '')
    score = data.get('score', 0)
    feedback = data.get('feedback', '')
    
    asgn = next((a for a in DB['assignments'] if str(a['id']) == str(asgn_id)), None)
    if not asgn:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Assignment not found'}}), 404
    
    sub = next((s for s in asgn.setdefault('submissions', []) if s.get('studentId') == student_id), None)
    if not sub:
        st_obj = next((s for s in DB['students'] if s['id'] == student_id), None)
        sub = {
            'studentId': student_id,
            'studentName': st_obj['name'] if st_obj else 'Student',
            'submittedAt': datetime.now().isoformat(),
            'fileName': 'submission.pdf'
        }
        asgn['submissions'].append(sub)
        
    sub['score'] = score
    sub['feedback'] = feedback
    sub['status'] = 'graded'
    sub['gradedAt'] = datetime.now().isoformat()
    
    return jsonify({'data': sub, 'message': 'Grade and feedback saved successfully'})

@app.route('/api/assignments/<asgn_id>/submit', methods=['POST'])
def submit_assignment(asgn_id):
    data = request.get_json(silent=True) or {}
    student_id = data.get('studentId', '2026-STD-0142')
    student_name = data.get('studentName', 'Nrinphouneta Hok')
    file_name = data.get('fileName', 'coursework.pdf')
    
    asgn = next((a for a in DB['assignments'] if str(a['id']) == str(asgn_id)), None)
    if not asgn:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Assignment not found'}}), 404
        
    sub = next((s for s in asgn.setdefault('submissions', []) if s.get('studentId') == student_id), None)
    if not sub:
        sub = {
            'studentId': student_id,
            'studentName': student_name,
            'fileName': file_name,
            'submittedAt': datetime.now().isoformat(),
            'status': 'submitted'
        }
        asgn['submissions'].append(sub)
    else:
        sub['fileName'] = file_name
        sub['submittedAt'] = datetime.now().isoformat()
        sub['status'] = 'submitted'
        
    return jsonify({'data': sub, 'message': 'Assignment submitted successfully'}), 201

# ── CLASSES API ──
@app.route('/api/classes', methods=['GET'])
def get_classes():
    return jsonify({'data': DB['classes'], 'meta': {'total': len(DB['classes'])}})

# ── ATTENDANCE API ──
@app.route('/api/attendance', methods=['GET', 'POST'])
def handle_attendance():
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        class_id = data.get('classId')
        date_val = data.get('date', datetime.now().strftime('%Y-%m-%d'))
        records = data.get('records', [])
        for r in records:
            existing = next((a for a in DB['attendanceRecords'] if a.get('studentId') == r.get('studentId') and a.get('date') == date_val), None)
            if existing:
                existing['status'] = r.get('status', 'present')
            else:
                DB['attendanceRecords'].append({
                    'studentId': r.get('studentId'),
                    'studentName': r.get('studentName', 'Student'),
                    'classId': class_id,
                    'date': date_val,
                    'status': r.get('status', 'present')
                })
        return jsonify({'message': f'Attendance recorded for {len(records)} students', 'data': records})

    class_id = request.args.get('classId')
    date_val = request.args.get('date')

    if class_id:
        target_class = '10A' if '10a' in class_id.lower() else '11B'
        class_students = [s for s in DB['students'] if s.get('class') == target_class]
        if not class_students:
            class_students = DB['students']
        result = []
        for cs in class_students:
            rec = next((a for a in DB['attendanceRecords'] if a.get('studentId') == cs['id'] and a.get('date') == date_val), None)
            status = rec['status'] if rec else 'present'
            parts = cs['name'].split()
            result.append({
                'id': cs['id'],
                'first_name': parts[0],
                'last_name': ' '.join(parts[1:]),
                'student_number': cs['id'],
                'class': cs['class'],
                'status': status
            })
        return jsonify({'data': result, 'meta': {'total': len(result)}})

    return jsonify({
        'data': {
            'rate': 96.2,
            'presentDays': 142,
            'absentDays': 3,
            'lateDays': 2,
            'history': [
                {'date': '2026-07-06', 'status': 'present', 'course': 'Advanced Mathematics'},
                {'date': '2026-07-05', 'status': 'present', 'course': 'Physics'},
                {'date': '2026-07-04', 'status': 'present', 'course': 'English'},
                {'date': '2026-07-03', 'status': 'late', 'course': 'Chemistry'},
            ]
        }
    })

# ── GRADES API ──
@app.route('/api/grades', methods=['GET', 'POST'])
def handle_grades():
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        student_id = data.get('studentId')
        subject = data.get('subject', 'Advanced Mathematics')
        score = int(data.get('score', 85))
        grade = 'A' if score >= 90 else ('B+' if score >= 85 else ('B' if score >= 80 else ('C+' if score >= 75 else 'C')))
        
        entry = {
            'studentId': student_id,
            'studentName': data.get('studentName', 'Student'),
            'subject': subject,
            'score': score,
            'grade': grade,
            'term': data.get('term', 'Term 2'),
            'teacher': data.get('teacher', 'Dr. Sarah Jenkins')
        }
        DB['grades'].append(entry)
        return jsonify({'data': entry, 'message': 'Grade recorded successfully'}), 201

    student_id = request.args.get('studentId')
    if student_id:
        items = [g for g in DB['grades'] if g.get('studentId') == student_id]
        return jsonify({'data': items, 'meta': {'total': len(items)}})

    return jsonify({'data': DB['grades'], 'meta': {'total': len(DB['grades'])}})

# ── PRINCIPAL & STAFF OVERSIGHT APIS ──
@app.route('/api/principal/stats', methods=['GET'])
def principal_stats():
    return jsonify({
        'data': {
            'totalStudents': 1250,
            'totalTeachers': 86,
            'totalClasses': 48,
            'dailyAttendanceRate': 95.4,
            'overallSchoolGpa': 3.62,
            'honorsRate': '24.2%',
            'pendingApprovals': 4,
            'departments': [
                {'name': 'Mathematics', 'head': 'Dr. Sarah Jenkins', 'faculty': 14, 'avgScore': 87.2, 'status': 'Optimal'},
                {'name': 'Science', 'head': 'Dr. Pov Sophea', 'faculty': 18, 'avgScore': 85.8, 'status': 'Optimal'},
                {'name': 'English', 'head': 'Ms. Rin Lina', 'faculty': 16, 'avgScore': 88.4, 'status': 'Optimal'},
                {'name': 'Khmer Studies', 'head': 'Mr. Chea Sambath', 'faculty': 12, 'avgScore': 89.1, 'status': 'Optimal'},
                {'name': 'Computer Science', 'head': 'Mr. Heng Samnang', 'faculty': 10, 'avgScore': 84.6, 'status': 'Optimal'},
            ]
        }
    })

@app.route('/api/staff/stats', methods=['GET'])
def staff_stats():
    return jsonify({
        'data': {
            'openRequests': len([r for r in DB['serviceRequests'] if r['status'] in ['open', 'pending']]),
            'activeLostFound': len([i for i in DB['lostFound'] if i.get('status') in ['active', 'matching']]),
            'completedToday': 8,
            'pendingClaims': len([c for i in DB['lostFound'] for c in i.get('claims', []) if c.get('status') == 'under_review']),
            'facilityCheck': 'All Campuses Clear'
        }
    })

@app.route('/api/staff/tasks', methods=['GET', 'POST'])
def staff_tasks():
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        task = {
            'id': f"TSK-{len(DB['operationalTasks']) + 1:03d}",
            'title': data.get('title', 'Task'),
            'area': data.get('area', 'Operations'),
            'priority': data.get('priority', 'normal'),
            'status': 'pending',
            'assignedTo': data.get('assignedTo', 'Staff Team'),
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        DB['operationalTasks'].insert(0, task)
        return jsonify({'data': task, 'message': 'Operational task created'}), 201
    return jsonify({'data': DB['operationalTasks'], 'meta': {'total': len(DB['operationalTasks'])}})

# ── ADMIN MANAGEMENT API ENDPOINTS ──
@app.route('/api/admin/stats', methods=['GET'])
def admin_stats():
    return jsonify({
        'data': {
            'students': 1250,
            'teachers': 86,
            'parents': 980,
            'activeClasses': 48,
            'attendanceToday': 95.4,
            'pendingRequests': 14,
            'grades': len(DB['grades'])
        }
    })

@app.route('/api/admin/students', methods=['GET'])
def admin_students():
    return jsonify({'data': DB['students'], 'meta': {'total': len(DB['students'])}})

@app.route('/api/admin/teachers', methods=['GET'])
def admin_teachers():
    return jsonify({'data': DB['teachers'], 'meta': {'total': len(DB['teachers'])}})

@app.route('/api/admin/parents', methods=['GET'])
def admin_parents():
    return jsonify({'data': DB['parents'], 'meta': {'total': len(DB['parents'])}})

@app.route('/api/admin/audit', methods=['GET'])
def admin_audit():
    limit = int(request.args.get('limit', 50))
    logs = [
        {'id': 1, 'action': 'USER_LOGIN', 'actor': 'admin@ngis.edu.kh', 'target': 'Portal Auth', 'timestamp': datetime.now().isoformat(), 'status': 'SUCCESS'},
        {'id': 2, 'action': 'UPDATE_ROLE', 'actor': 'admin@ngis.edu.kh', 'target': 'TCH-001 Dr. Sarah Jenkins', 'timestamp': datetime.now().isoformat(), 'status': 'SUCCESS'},
        {'id': 3, 'action': 'PUBLISH_NEWS', 'actor': 'admin@ngis.edu.kh', 'target': 'School Sports Day 2026', 'timestamp': datetime.now().isoformat(), 'status': 'SUCCESS'},
    ]
    return jsonify({'data': logs[:limit], 'meta': {'total': len(logs)}})

@app.route('/api/announcements', methods=['GET', 'POST'])
def handle_announcements():
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        item = {
            'id': len(DB['news']) + 1,
            'title': data.get('title', 'Untitled'),
            'message': data.get('message', ''),
            'audience': data.get('audience', 'all'),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'category': data.get('category', 'general'),
            'pinned': bool(data.get('pinned', False)),
            'published': True
        }
        DB['news'].insert(0, item)
        return jsonify({'data': item}), 201
    return jsonify({'data': DB['news'], 'meta': {'total': len(DB['news'])}})

@app.route('/api/announcements/<int:id>', methods=['DELETE'])
def delete_announcement(id):
    idx = next((i for i, n in enumerate(DB['news']) if n['id'] == id), None)
    if idx is not None:
        DB['news'].pop(idx)
        return jsonify({'data': None, 'message': 'Deleted'})
    return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Announcement not found'}}), 404

# ── CLEAN ROUTE SHORTCUTS ──
@app.route('/admin')
@app.route('/admin/')
def route_admin():
    return send_from_directory(ROOT, 'pages/admin/admin.html')

@app.route('/teacher')
@app.route('/teacher/')
def route_teacher():
    return send_from_directory(ROOT, 'pages/teacher/teacher.html')

@app.route('/student')
@app.route('/student/')
def route_student():
    return send_from_directory(ROOT, 'pages/student/student.html')

@app.route('/parent')
@app.route('/parent/')
def route_parent():
    return send_from_directory(ROOT, 'pages/parent/parent.html')

@app.route('/staff')
@app.route('/staff/')
def route_staff():
    return send_from_directory(ROOT, 'pages/staff/staff.html')

@app.route('/principal')
@app.route('/principal/')
def route_principal():
    return send_from_directory(ROOT, 'pages/principal/principal.html')

@app.route('/access-denied')
def route_access_denied():
    return send_from_directory(ROOT, 'pages/shared/access-denied.html')

# ── CATCH-ALL & STATIC SERVING ──
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if not path:
        return send_from_directory(ROOT, 'index.html')
    
    # API endpoints that were not matched must return 404 JSON, NOT index.html!
    if path.startswith('api/') or path == 'api':
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': f'API route /{path} not found'}}), 404

    # Check if exact file exists on disk
    file_path = os.path.join(ROOT, path)
    if os.path.isfile(file_path):
        return send_from_directory(ROOT, path)

    # Static file extensions that do not exist -> 404
    if '.' in path:
        abort(404)

    return send_from_directory(ROOT, 'index.html')

@app.errorhandler(404)
def handle_404(e):
    if request.path.startswith('/api/') or request.path == '/api':
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': f'API route {request.path} not found'}}), 404
    return send_from_directory(ROOT, 'pages/shared/access-denied.html'), 404

# ── Start ─────────────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 60)
    print("  NGIS - New Gateway International School")
    print("  School Management System - Flask Server")
    print("=" * 60)
    print(f"  Running at:  http://localhost:{PORT}")
    print(f"  Environment: {os.environ.get('FLASK_ENV', 'development')}")
    print("=" * 60)
    print("  Portals:")
    print(f"  Admin   ->  http://localhost:{PORT}/pages/admin/admin.html")
    print(f"  Teacher ->  http://localhost:{PORT}/pages/teacher/teacher.html")
    print(f"  Student ->  http://localhost:{PORT}/pages/student/student.html")
    print(f"  Parent  ->  http://localhost:{PORT}/pages/parent/parent.html")
    print("=" * 60)
    print(f"  API:  http://localhost:{PORT}/api/health")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=PORT, debug=True)
