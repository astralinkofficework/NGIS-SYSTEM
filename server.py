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

import academic_store as ACADEMIC

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

        # Grade 10A (Homeroom & Adv Math)

        {'id': '2026-STD-0142', 'name': 'Nrinphouneta Hok', 'gender': 'M', 'grade': 'Grade 10', 'class': '10A', 'gpa': 3.87, 'attendance': 96, 'status': 'active', 'parentEmail': 'parent@ngis.edu.kh', 'parentName': 'Chan Dara Vuth', 'advisor': 'Dr. Sarah Jenkins'},

        {'id': '2026-STD-0144', 'name': 'Sophea Chan',      'gender': 'F', 'grade': 'Grade 10', 'class': '10A', 'gpa': 3.55, 'attendance': 91, 'status': 'active', 'parentEmail': 's.chan.parent@ngis.edu.kh', 'parentName': 'Sophea Sok', 'advisor': 'Dr. Sarah Jenkins'},

        {'id': '2026-STD-0145', 'name': 'Virak Heng',        'gender': 'M', 'grade': 'Grade 10', 'class': '10A', 'gpa': 3.65, 'attendance': 95, 'status': 'active', 'parentEmail': 'v.heng@example.com', 'parentName': 'Heng Piseth', 'advisor': 'Dr. Sarah Jenkins'},

        {'id': '2026-STD-0148', 'name': 'Kosal Rith Mony',  'gender': 'M', 'grade': 'Grade 10', 'class': '10A', 'gpa': 3.72, 'attendance': 94, 'status': 'active', 'parentEmail': 'parent@ngis.edu.kh', 'parentName': 'Chan Dara Vuth', 'advisor': 'Dr. Sarah Jenkins'},

        {'id': '2026-STD-0151', 'name': 'Sreylin Vuth',     'gender': 'F', 'grade': 'Grade 10', 'class': '10A', 'gpa': 3.92, 'attendance': 99, 'status': 'active', 'parentEmail': 's.vuth@example.com', 'parentName': 'Vuth Samnang', 'advisor': 'Dr. Sarah Jenkins'},

        {'id': '2026-STD-0155', 'name': 'Heng Piseth',       'gender': 'M', 'grade': 'Grade 10', 'class': '10A', 'gpa': 3.45, 'attendance': 88, 'status': 'active', 'parentEmail': 'h.piseth@example.com', 'parentName': 'Piseth Chea', 'advisor': 'Dr. Sarah Jenkins'},

        {'id': '2026-STD-0160', 'name': 'Emily Jenkins',     'gender': 'F', 'grade': 'Grade 10', 'class': '10A', 'gpa': 3.98, 'attendance': 100, 'status': 'active', 'parentEmail': 'teacher@ngis.edu.kh', 'parentName': 'Dr. Sarah Jenkins', 'advisor': 'Dr. Sarah Jenkins'},

        {'id': '2026-STD-0162', 'name': 'Kevin Jenkins',     'gender': 'M', 'grade': 'Grade 10', 'class': '10A', 'gpa': 3.78, 'attendance': 97, 'status': 'active', 'parentEmail': 'teacher@ngis.edu.kh', 'parentName': 'Dr. Sarah Jenkins', 'advisor': 'Dr. Sarah Jenkins'},

        {'id': '2026-STD-0168', 'name': 'Linda Chea',        'gender': 'F', 'grade': 'Grade 10', 'class': '10A', 'gpa': 3.84, 'attendance': 96, 'status': 'active', 'parentEmail': 'l.chea@example.com', 'parentName': 'Chea Vatanak', 'advisor': 'Dr. Sarah Jenkins'},

        {'id': '2026-STD-0171', 'name': 'Vicheka Meas',      'gender': 'M', 'grade': 'Grade 10', 'class': '10A', 'gpa': 3.68, 'attendance': 93, 'status': 'active', 'parentEmail': 'v.meas@example.com', 'parentName': 'Meas Sarin', 'advisor': 'Dr. Sarah Jenkins'},

        {'id': '2026-STD-0174', 'name': 'Dara Panha',        'gender': 'M', 'grade': 'Grade 10', 'class': '10A', 'gpa': 3.35, 'attendance': 85, 'status': 'active', 'parentEmail': 'd.panha@example.com', 'parentName': 'Panha Sovann', 'advisor': 'Dr. Sarah Jenkins'},

        {'id': '2026-STD-0177', 'name': 'Bormey Sen',        'gender': 'F', 'grade': 'Grade 10', 'class': '10A', 'gpa': 3.89, 'attendance': 98, 'status': 'active', 'parentEmail': 'b.sen@example.com', 'parentName': 'Sen Rithy', 'advisor': 'Dr. Sarah Jenkins'},

        {'id': '2026-STD-0182', 'name': 'Kimleng Seng',      'gender': 'M', 'grade': 'Grade 10', 'class': '10A', 'gpa': 3.62, 'attendance': 94, 'status': 'active', 'parentEmail': 'k.seng@example.com', 'parentName': 'Seng Dara', 'advisor': 'Dr. Sarah Jenkins'},

        {'id': '2026-STD-0185', 'name': 'Nathalie Pich',     'gender': 'F', 'grade': 'Grade 10', 'class': '10A', 'gpa': 3.91, 'attendance': 99, 'status': 'active', 'parentEmail': 'n.pich@example.com', 'parentName': 'Pich Moly', 'advisor': 'Dr. Sarah Jenkins'},

        {'id': '2026-STD-0189', 'name': 'Rithy Kong',        'gender': 'M', 'grade': 'Grade 10', 'class': '10A', 'gpa': 3.52, 'attendance': 92, 'status': 'active', 'parentEmail': 'r.kong@example.com', 'parentName': 'Kong Bunthoeun', 'advisor': 'Dr. Sarah Jenkins'},

        {'id': '2026-STD-0193', 'name': 'Thida Bun',         'gender': 'F', 'grade': 'Grade 10', 'class': '10A', 'gpa': 3.86, 'attendance': 97, 'status': 'active', 'parentEmail': 't.bun@example.com', 'parentName': 'Bun Phearith', 'advisor': 'Dr. Sarah Jenkins'},

        {'id': '2026-STD-0199', 'name': 'Sarath Om',         'gender': 'M', 'grade': 'Grade 10', 'class': '10A', 'gpa': 3.70, 'attendance': 95, 'status': 'active', 'parentEmail': 's.om@example.com', 'parentName': 'Om Vanny', 'advisor': 'Dr. Sarah Jenkins'},



        # Grade 11B (Physics CP)

        {'id': '2026-STD-0143', 'name': 'Kosal Rith Mony',  'gender': 'M', 'grade': 'Grade 11', 'class': '11B', 'gpa': 3.72, 'attendance': 94, 'status': 'active', 'parentEmail': 'parent@ngis.edu.kh', 'parentName': 'Chan Dara Vuth', 'advisor': 'Dr. Sarah Jenkins'},

        {'id': '2026-STD-0146', 'name': 'Sreymom Vuth',     'gender': 'F', 'grade': 'Grade 11', 'class': '11B', 'gpa': 3.82, 'attendance': 98, 'status': 'active', 'parentEmail': 's.vuth@example.com', 'parentName': 'Vuth Samnang', 'advisor': 'Dr. Sarah Jenkins'},

        {'id': '2026-STD-0152', 'name': 'Chenda Sam',       'gender': 'F', 'grade': 'Grade 11', 'class': '11B', 'gpa': 3.65, 'attendance': 92, 'status': 'active', 'parentEmail': 'c.sam@example.com', 'parentName': 'Sam Bopha', 'advisor': 'Dr. Sarah Jenkins'},

        {'id': '2026-STD-0158', 'name': 'Sovannary Keo',    'gender': 'F', 'grade': 'Grade 11', 'class': '11B', 'gpa': 3.88, 'attendance': 96, 'status': 'active', 'parentEmail': 's.keo@example.com', 'parentName': 'Keo Pheakdey', 'advisor': 'Dr. Sarah Jenkins'},

        {'id': '2026-STD-0164', 'name': 'Bopha Devi',        'gender': 'F', 'grade': 'Grade 11', 'class': '11B', 'gpa': 3.95, 'attendance': 99, 'status': 'active', 'parentEmail': 'b.devi@example.com', 'parentName': 'Devi Rath', 'advisor': 'Dr. Sarah Jenkins'},

        {'id': '2026-STD-0170', 'name': 'Rathana Sok',      'gender': 'M', 'grade': 'Grade 11', 'class': '11B', 'gpa': 3.58, 'attendance': 90, 'status': 'active', 'parentEmail': 'r.sok@example.com', 'parentName': 'Sok Chanthou', 'advisor': 'Dr. Sarah Jenkins'},



        # Grade 11C (AP Calculus BC)

        {'id': '2026-STD-0147', 'name': 'Kimheak Chheng',   'gender': 'M', 'grade': 'Grade 11', 'class': '11C', 'gpa': 3.88, 'attendance': 97, 'status': 'active', 'parentEmail': 'k.chheng@example.com', 'parentName': 'Chheng Kim', 'advisor': 'Muthukumaran Pakkirisamy'},

        {'id': '2026-STD-0149', 'name': 'Prak Piseth',       'gender': 'M', 'grade': 'Grade 11', 'class': '11C', 'gpa': 3.42, 'attendance': 89, 'status': 'active', 'parentEmail': 'p.piseth@example.com', 'parentName': 'Piseth Chea', 'advisor': 'Muthukumaran Pakkirisamy'},

        {'id': '2026-STD-0153', 'name': 'Maly Ros',          'gender': 'F', 'grade': 'Grade 11', 'class': '11C', 'gpa': 3.79, 'attendance': 95, 'status': 'active', 'parentEmail': 'm.ros@example.com', 'parentName': 'Ros Saroeun', 'advisor': 'Dr. Sarah Jenkins'},

        {'id': '2026-STD-0159', 'name': 'Chantrea Seng',    'gender': 'F', 'grade': 'Grade 11', 'class': '11C', 'gpa': 3.91, 'attendance': 98, 'status': 'active', 'parentEmail': 'c.seng@example.com', 'parentName': 'Seng Visal', 'advisor': 'Dr. Sarah Jenkins'},

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

            'subjects': ['Advanced Mathematics', 'Calculus I', 'AP Biology', 'Pre-AP Chemistry'],

            'classes': ['10A', '11B', '11C'],

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

        {'id': 'cls-11c', 'name': 'Grade 11C', 'grade': '11', 'section': 'C', 'homeroomTeacher': 'Muthukumaran Pakkirisamy', 'room': 'Room 407 (11C)', 'studentCount': 28, 'campus': 'Sensok'},

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

        'contactMethod': data.get('contactMethod', 'email'),

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



@app.route('/api/lost-found/<int:item_id>', methods=['PUT', 'DELETE'])
def update_or_delete_lost_found_item(item_id):
    if request.method == 'DELETE':
        items = load_lost_found_items()
        idx = next((i for i, item in enumerate(items) if item.get('id') == item_id), None)
        if idx is None:
            return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Item not found'}}), 404
        deleted = items.pop(idx)
        save_lost_found_items(items)
        return jsonify({'data': deleted, 'message': 'Item deleted successfully'})


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

        'contactMethod': data.get('contactMethod', 'email'),

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

    student_id = request.args.get('studentId') or request.args.get('userId') or request.args.get('requesterId')

    role = request.args.get('role')

    

    items = DB['serviceRequests']

    if status and status != 'all':

        items = [r for r in items if r.get('status') == status]

    if category and category != 'all':

        items = [r for r in items if r.get('category') == category]

    if type_ and type_ != 'all':

        items = [r for r in items if r.get('type') == type_]

    if campus and campus != 'all':

        items = [r for r in items if r.get('campus') == campus]

    if student_id and student_id != 'all':

        items = [r for r in items if r.get('studentId') == student_id]

    if role and role != 'all':

        items = [r for r in items if r.get('role') == role or (role == 'teacher' and str(r.get('studentId', '')).startswith('TCH')) or (role == 'student' and str(r.get('studentId', '')).startswith('2026-STD'))]

    

    items.sort(key=lambda x: datetime.strptime(x.get('date', '2026-01-01'), '%Y-%m-%d'), reverse=True)

    return jsonify({'data': items, 'meta': {'total': len(items)}})



@app.route('/api/service-requests/<id>', methods=['GET'])

def get_service_request(id):

    item = next((r for r in DB['serviceRequests'] if r['id'] == id), None)

    if not item:

        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Service request not found'}}), 404

    return jsonify({'data': item})



@app.route('/api/service-requests', methods=['POST'])

def create_service_request():

    data = request.get_json() or {}

    student_id = data.get('studentId') or data.get('requesterId') or data.get('userId') or 'TCH-2024-042'

    student_name = data.get('studentName') or data.get('requesterName') or data.get('userName') or 'Dr. Sarah Jenkins'

    role = data.get('role') or data.get('requesterRole') or ('teacher' if str(student_id).startswith('TCH') else 'student')

    category = data.get('category')

    type_ = data.get('type')

    title = data.get('title')

    description = data.get('description')

    priority = data.get('priority') or 'normal'

    campus = data.get('campus') or 'Sensok'

    

    if not student_id or not category or not type_ or not title:

        return jsonify({'error': {'code': 'VALIDATION_ERROR', 'message': 'studentId, category, type, and title are required'}}), 400

    

    id = f"SR-{1000 + len(DB['serviceRequests']) + 1}"

    entry = {

        'id': id,

        'studentId': student_id,

        'studentName': student_name,

        'role': role,

        'category': category,

        'type': type_,

        'title': title,

        'description': description or '',

        'status': 'open',

        'priority': priority,

        'campus': campus,

        'assignee': 'Operations & Academic Facilities',

        'date': datetime.now().strftime('%Y-%m-%d'),

        'updatedAt': datetime.now().strftime('%Y-%m-%d'),

        'comments': [

            {'by': student_name, 'text': f'Submitted service request for {title}.', 'date': datetime.now().strftime('%Y-%m-%d')}

        ]

    }

    DB['serviceRequests'].append(entry)

    try:

        _persist_service_requests()

    except Exception as e:

        pass

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



# Persistent academic source of truth. The legacy DB remains available for

# unrelated demo modules while Grades & Attendance uses this transactional

# store and its explicit authorization rules.

ACADEMIC.init(DB)



def _academic_user():

    """Resolve an exact demo bearer token; never infer a role from a substring."""

    header = request.headers.get('Authorization', '')

    if not header.startswith('Bearer '):

        return None

    token = header[7:].strip()

    for role, email in {

        'admin': 'admin@ngis.edu.kh', 'principal': 'principal@ngis.edu.kh',

        'teacher': 'teacher@ngis.edu.kh', 'student': 'student@ngis.edu.kh',

        'parent': 'parent@ngis.edu.kh', 'staff': 'staff@ngis.edu.kh'

    }.items():

        if token == f'mock-jwt-token-{role}':

            user = dict(AUTH_USERS[email])

            # Canonical academic identifiers are the IDs used by enrollments.

            if role == 'student': user['id'] = '2026-STD-0142'

            return user

    return None



def _academic_require(roles=None):

    user = _academic_user()

    if not user:

        return None, (jsonify({'error': {'code': 'UNAUTHORIZED', 'message': 'A valid academic session is required'}}), 401)

    if roles and user['role'] not in roles:

        return None, (jsonify({'error': {'code': 'FORBIDDEN', 'message': 'This role is not allowed to perform this action'}}), 403)

    return user, None



def _student(student_id):

    return next((s for s in DB['students'] if str(s.get('id')) == str(student_id)), None)



def _parent_can_view(user, student_id):

    if user['role'] != 'parent': return True

    parent = next((p for p in DB['parents'] if p.get('id') == user['id']), None)

    # Demo parent ID is PAR-2024-118 and is the authenticated parent record.

    if parent is None and user['id'] == 'PAR-2024-118': parent = DB['parents'][0]

    return bool(parent and student_id in parent.get('children', []))



def _teacher_can_class(user, class_id):

    if user['role'] in ('admin', 'principal'): return True

    if user['role'] != 'teacher': return False

    teacher = next((t for t in DB['teachers'] if t.get('id') == user['id']), None)

    cls = next((c for c in DB['classes'] if c.get('id') == class_id), None)

    return bool(teacher and cls and (cls.get('name', '').replace('Grade ', '') in teacher.get('classes', [])))



def _academic_error(code, message, status=400):

    return jsonify({'error': {'code': code, 'message': message}}), status



@app.route('/api/academic/config', methods=['GET'])

def academic_config():

    user, error = _academic_require()

    if error: return error

    return jsonify({'data': {

        'academicYears': ACADEMIC.query('SELECT * FROM academic_years ORDER BY name DESC'),

        'gradingPeriods': ACADEMIC.query('SELECT * FROM grading_periods ORDER BY sequence_no'),

        'subjects': ACADEMIC.query('SELECT * FROM subjects WHERE status="active" ORDER BY name'),

        'gradingRules': ACADEMIC.query('SELECT id, name, version, max_gpa, rules_json FROM grading_rules WHERE is_active=1')

    }})



@app.route('/api/academic/overview', methods=['GET'])

def academic_overview():

    user, error = _academic_require()

    if error: return error

    requested = request.args.get('studentId')

    if user['role'] == 'student': requested = user['id']

    if user['role'] == 'parent' and requested and not _parent_can_view(user, requested):

        return _academic_error('FORBIDDEN', 'This student is not linked to your account', 403)

    students = DB['students']

    if requested: students = [s for s in students if s.get('id') == requested]

    elif user['role'] == 'parent':

        parent = next((p for p in DB['parents'] if p.get('id') == user['id']), DB['parents'][0])

        students = [s for s in students if s.get('id') in parent.get('children', [])]

    elif user['role'] == 'teacher':

        teacher = next((t for t in DB['teachers'] if t.get('id') == user['id']), None)

        names = (teacher or {}).get('classes', [])

        students = [s for s in students if s.get('class') in names]

    rows = []

    for student in students:

        rows.append({**student, 'gpa': ACADEMIC.aggregate_gpa(student['id']), 'attendance': ACADEMIC.attendance_summary(student['id'])['percentage']})

    return jsonify({'data': {'students': rows, 'total': len(rows), 'generatedAt': ACADEMIC.now()}})



def _academic_grade_row(row):

    pct = (float(row['score']) / float(row['max_score']) * 100) if row.get('score') is not None and row.get('max_score') else None

    letter, points = ACADEMIC.grade_band(pct)

    return {**row, 'percentage': round(pct, 2) if pct is not None else None, 'letterGrade': letter, 'gpaPoints': points,

            'studentId': row.get('student_id'), 'subjectId': row.get('subject_id'), 'assessmentTitle': row.get('assessment_title'),

            'maxScore': row.get('max_score'), 'recordedAt': row.get('recorded_at'),

            'student_name': (_student(row.get('student_id')) or {}).get('name', row.get('student_id')),

            'subject_name': (ACADEMIC.one('SELECT name FROM subjects WHERE id=?', (row.get('subject_id'),)) or {}).get('name', row.get('subject_id')),

            'assessment_title': row.get('assessment_title'), 'max_score': row.get('max_score'),

            'letter_grade': letter, 'recorded_at': row.get('recorded_at')}



@app.route('/api/academic/grades', methods=['GET', 'POST'])

def academic_grades():

    user, error = _academic_require()

    if error: return error

    if request.method == 'GET':

        student_id = request.args.get('studentId')

        if user['role'] == 'student': student_id = user['id']

        if user['role'] == 'parent' and student_id and not _parent_can_view(user, student_id):

            return _academic_error('FORBIDDEN', 'This student is not linked to your account', 403)

        clauses, args = ['1=1'], []

        if student_id: clauses.append('g.student_id=?'); args.append(student_id)

        if request.args.get('periodId'): clauses.append('a.grading_period_id=?'); args.append(request.args['periodId'])

        if user['role'] == 'teacher':

            teacher_classes = [c['id'] for c in DB['classes'] if c.get('name','').replace('Grade ','') in (next((t.get('classes',[]) for t in DB['teachers'] if t.get('id') == user['id']), []))]

            if not teacher_classes: return jsonify({'data': [], 'meta': {'total': 0}})

            clauses.append('a.class_id IN (%s)' % ','.join('?' for _ in teacher_classes)); args.extend(teacher_classes)

        rows = ACADEMIC.query('''SELECT g.*, a.title AS assessment_title, a.max_score, a.class_id, a.subject_id,

          a.grading_period_id, a.category, a.status AS assessment_status FROM grades g JOIN assessments a ON a.id=g.assessment_id

          WHERE ''' + ' AND '.join(clauses) + ' ORDER BY g.updated_at DESC', args)

        return jsonify({'data': [_academic_grade_row(r) for r in rows], 'meta': {'total': len(rows)}})

    if user['role'] not in ('teacher', 'admin'):

        return _academic_error('FORBIDDEN', 'Only teachers and administrators can record grades', 403)

    data = request.get_json(silent=True) or {}

    required = ['studentId', 'classId', 'subjectId', 'assessmentTitle', 'score', 'maxScore']

    missing = [k for k in required if data.get(k) in (None, '')]

    if missing: return _academic_error('VALIDATION_ERROR', 'Missing: ' + ', '.join(missing))

    if not _teacher_can_class(user, data['classId']): return _academic_error('FORBIDDEN', 'You are not assigned to this class', 403)

    student = _student(data['studentId'])

    if not student: return _academic_error('NOT_FOUND', 'Student not found', 404)

    cls = next((c for c in DB['classes'] if c.get('id') == data['classId']), None)

    if not cls or student.get('class') != cls.get('name','').replace('Grade ',''): return _academic_error('VALIDATION_ERROR', 'Student is not enrolled in this class')

    try: score, max_score = float(data['score']), float(data['maxScore'])

    except (TypeError, ValueError): return _academic_error('VALIDATION_ERROR', 'Score and maxScore must be numbers')

    if max_score <= 0 or score < 0 or score > max_score: return _academic_error('VALIDATION_ERROR', 'Score must be between 0 and maxScore')

    period_id = data.get('gradingPeriodId', 'gp-term-2')

    if not ACADEMIC.one('SELECT id FROM grading_periods WHERE id=?', (period_id,)): return _academic_error('VALIDATION_ERROR', 'Unknown grading period')

    subject = ACADEMIC.one('SELECT * FROM subjects WHERE id=?', (data['subjectId'],))

    if not subject: return _academic_error('NOT_FOUND', 'Subject not found', 404)

    assessment_id = data.get('assessmentId') or ACADEMIC.new_id('asm')

    grade_id = ACADEMIC.new_id('grd'); now = ACADEMIC.now(); workflow = data.get('workflow', 'submitted' if user['role'] == 'teacher' else 'published')

    if workflow not in ('draft', 'submitted', 'published', 'returned'): return _academic_error('VALIDATION_ERROR', 'Invalid workflow state')

    statements = []

    if not data.get('assessmentId'):

        statements.append(('INSERT INTO assessments(id,class_id,subject_id,grading_period_id,title,category,max_score,weight,teacher_id,status,created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)',

          (assessment_id, data['classId'], data['subjectId'], period_id, str(data['assessmentTitle']).strip(), data.get('category','assessment'), max_score, float(data.get('weight', 1)), user['id'], 'published', now)))

    statements.append(('INSERT INTO grades(id,assessment_id,student_id,score,state,comments,workflow,recorded_by,recorded_at,updated_at) VALUES (?,?,?,?,?,?,?,?,?,?) ON CONFLICT(assessment_id,student_id) DO UPDATE SET score=excluded.score, comments=excluded.comments, workflow=excluded.workflow, updated_at=excluded.updated_at',

      (grade_id, assessment_id, data['studentId'], score, 'graded', data.get('comments',''), workflow, user['id'], now, now)))

    try: ACADEMIC.transaction(statements)

    except Exception as exc: return _academic_error('CONFLICT', f'Could not save grade: {exc}', 409)

    ACADEMIC.audit(user['id'], user['role'], 'GRADE_UPSERT', 'grade', grade_id, data.get('reason',''), {'studentId': data['studentId'], 'assessmentId': assessment_id})

    row = ACADEMIC.one('''SELECT g.*, a.title AS assessment_title, a.max_score, a.class_id, a.subject_id, a.grading_period_id, a.category, a.status AS assessment_status FROM grades g JOIN assessments a ON a.id=g.assessment_id WHERE g.assessment_id=? AND g.student_id=?''', (assessment_id, data['studentId']))

    return jsonify({'data': _academic_grade_row(row), 'message': 'Grade saved'}), 201



@app.route('/api/academic/grades/<grade_id>/workflow', methods=['PATCH'])

def academic_grade_workflow(grade_id):

    user, error = _academic_require(('teacher', 'admin', 'principal'))

    if error: return error

    data = request.get_json(silent=True) or {}; state = data.get('workflow')

    if state not in ('draft', 'submitted', 'published', 'returned'): return _academic_error('VALIDATION_ERROR', 'Invalid workflow state')

    row = ACADEMIC.one('SELECT * FROM grades WHERE id=?', (grade_id,))

    if not row: return _academic_error('NOT_FOUND', 'Grade not found', 404)

    if state == 'published' and user['role'] not in ('admin', 'principal'): return _academic_error('FORBIDDEN', 'Only administrators or principals can publish grades', 403)

    ACADEMIC.execute('UPDATE grades SET workflow=?, updated_at=? WHERE id=?', (state, ACADEMIC.now(), grade_id))

    ACADEMIC.audit(user['id'], user['role'], 'GRADE_WORKFLOW', 'grade', grade_id, data.get('reason',''), {'workflow': state})

    return jsonify({'data': ACADEMIC.one('SELECT * FROM grades WHERE id=?', (grade_id,))})



@app.route('/api/academic/attendance', methods=['GET', 'POST'])

def academic_attendance():

    user, error = _academic_require()

    if error: return error

    if request.method == 'GET':

        student_id = request.args.get('studentId')

        if user['role'] == 'student': student_id = user['id']

        if user['role'] == 'parent' and student_id and not _parent_can_view(user, student_id): return _academic_error('FORBIDDEN', 'This student is not linked to your account', 403)

        clauses, args = ['1=1'], []

        if student_id: clauses.append('student_id=?'); args.append(student_id)

        if request.args.get('classId'): clauses.append('class_id=?'); args.append(request.args['classId'])

        if request.args.get('from'): clauses.append('attendance_date>=?'); args.append(request.args['from'])

        if request.args.get('to'): clauses.append('attendance_date<=?'); args.append(request.args['to'])

        rows = ACADEMIC.query('SELECT * FROM attendance WHERE ' + ' AND '.join(clauses) + ' ORDER BY attendance_date DESC', args)

        enriched_rows = []

        for r in rows:

            st = _student(r.get('student_id')) or {}

            cls = next((c for c in DB['classes'] if c.get('id') == r.get('class_id')), None)

            item = {

                **r,

                'student_name': st.get('name', r.get('student_id')),

                'student_grade': st.get('grade', 'Grade 11'),

                'class_name': cls.get('name') if cls else r.get('class_id'),

                'date': r.get('attendance_date'),

                'notes': r.get('note', ''),

                'status': 'late' if r.get('status') == 'tardy' else r.get('status')

            }

            enriched_rows.append(item)

        rows = enriched_rows



        if request.args.get('status'):

            target_status = request.args['status'].lower()

            if target_status == 'tardy': target_status = 'late'

            rows = [r for r in rows if r['status'] == target_status or (target_status == 'late' and r['status'] == 'tardy')]



        if request.args.get('search'):

            query = request.args['search'].lower().strip()

            rows = [r for r in rows if query in r['student_id'].lower() or query in r['student_name'].lower()]



        summary = ACADEMIC.attendance_summary(student_id) if student_id else None

        # Teacher roster mode: return every enrolled student for the selected class,

        # overlaying today's saved record so the UI can mark missing students.

        if request.args.get('classId') and not student_id and (user['role'] == 'teacher' or request.args.get('view') == 'roster'):

            class_id = request.args['classId']; date = request.args.get('date')

            cls_obj = next((c for c in DB['classes'] if c.get('id') == class_id), None)

            cls_code = cls_obj.get('name', '').replace('Grade ', '') if cls_obj else ''

            

            # Fetch from enrollments first

            roster = ACADEMIC.query('SELECT student_id FROM enrollments WHERE class_id=? AND academic_year_id=? ORDER BY student_id', (class_id, 'ay-2025-26'))

            s_ids = [r['student_id'] for r in roster]

            if cls_code:

                # Merge students assigned to this class in DB['students']

                matching_sids = [s['id'] for s in DB['students'] if s.get('class') == cls_code]

                for sid in matching_sids:

                    if sid not in s_ids:

                        s_ids.append(sid)

            if not s_ids:

                s_ids = [s['id'] for s in DB['students'] if s.get('class') == '10A']

                

            existing = {r['student_id']: r for r in rows if not date or r['attendance_date'] == date}

            data = []

            for sid in s_ids:

                student = _student(sid) or {}

                rec = existing.get(sid, {})

                s_name = student.get('name', sid)

                name_parts = s_name.split(' ')

                data.append({

                    'student_id': sid,

                    'student_number': sid,

                    'name': s_name,

                    'first_name': name_parts[0],

                    'last_name': ' '.join(name_parts[1:]) if len(name_parts) > 1 else '',

                    'gender': student.get('gender', 'M' if int(sid.split('-')[-1]) % 2 == 0 else 'F'),

                    'status': rec.get('status', 'present'),

                    'note': rec.get('note', ''),

                    'notes': rec.get('note', ''),

                    'date': date,

                    'class_id': class_id

                })

            return jsonify({'data': data, 'meta': {'total': len(data)}})

        meta = {'total': len(rows), 'summary': summary}

        if summary:

            meta.update({'present': summary['present'], 'late': summary['tardy'], 'absent': summary['absent'], 'rate': summary['percentage']})

        else:

            p_cnt = sum(1 for r in rows if r['status'] == 'present')

            l_cnt = sum(1 for r in rows if r['status'] in ('late', 'tardy'))

            a_cnt = sum(1 for r in rows if r['status'] == 'absent')

            e_cnt = sum(1 for r in rows if r['status'] == 'excused')

            tot = len(rows)

            rate = round((p_cnt / tot * 100), 1) if tot > 0 else 100.0

            meta.update({'present': p_cnt, 'late': l_cnt, 'absent': a_cnt, 'excused': e_cnt, 'rate': rate})

        return jsonify({'data': rows, 'meta': meta})

    if user['role'] not in ('teacher', 'admin'): return _academic_error('FORBIDDEN', 'Only teachers and administrators can record attendance', 403)

    payload = request.get_json(silent=True) or {}; records = payload.get('records') if isinstance(payload, dict) else payload

    if not isinstance(records, list): records = [payload]

    allowed = {'present', 'absent', 'tardy', 'late', 'excused'}; saved = []

    for item in records:

        item = {**payload, **item} if isinstance(payload, dict) else item

        for field in ('studentId', 'classId', 'date', 'status'):

            if item.get(field) in (None, ''): return _academic_error('VALIDATION_ERROR', f'{field} is required')

        if item['status'] not in allowed: return _academic_error('VALIDATION_ERROR', 'Status must be present, absent, tardy, or excused')

        if not _teacher_can_class(user, item['classId']): return _academic_error('FORBIDDEN', 'You are not assigned to this class', 403)

        student = _student(item['studentId']); cls = next((c for c in DB['classes'] if c.get('id') == item['classId']), None)

        if not student or not cls: return _academic_error('NOT_FOUND', 'Student or class not found', 404)

        if student.get('class') != cls.get('name','').replace('Grade ',''): return _academic_error('VALIDATION_ERROR', 'Student is not enrolled in this class')

        stored_status = 'tardy' if item['status'] == 'late' else item['status']

        now = ACADEMIC.now(); record_id = ACADEMIC.new_id('att')

        ACADEMIC.execute('''INSERT INTO attendance(id,student_id,class_id,subject_id,attendance_date,session,status,note,workflow,recorded_by,recorded_at,updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)

          ON CONFLICT(student_id,class_id,subject_id,attendance_date,session) DO UPDATE SET status=excluded.status,note=excluded.note,updated_at=excluded.updated_at,recorded_by=excluded.recorded_by''',

          (record_id, item['studentId'], item['classId'], item.get('subjectId') or '', item['date'], item.get('session','daily'), stored_status, item.get('note',''), item.get('workflow','submitted'), user['id'], now, now))

        saved.append(item['studentId'])

    ACADEMIC.audit(user['id'], user['role'], 'ATTENDANCE_BULK_UPSERT', 'attendance', ','.join(saved), payload.get('reason','') if isinstance(payload, dict) else '', {'count': len(saved)})

    return jsonify({'data': ACADEMIC.query('SELECT * FROM attendance ORDER BY updated_at DESC LIMIT ?', (len(saved),)), 'message': f'{len(saved)} attendance record(s) saved'}), 201



@app.route('/api/academic/report-cards', methods=['GET'])

def academic_report_cards():

    user, error = _academic_require()

    if error: return error

    class_id = request.args.get('classId')

    period_id = request.args.get('periodId', 'gp-term-2')



    if class_id:

        if user['role'] == 'teacher' and not _teacher_can_class(user, class_id):

            return _academic_error('FORBIDDEN', 'You are not assigned to this class', 403)

        cls_obj = next((c for c in DB['classes'] if c.get('id') == class_id), None)

        cls_code = cls_obj.get('name', '').replace('Grade ', '') if cls_obj else ''

        students = [s for s in DB['students'] if s.get('class') == cls_code]

        if not students:

            enr = ACADEMIC.query("SELECT student_id FROM enrollments WHERE class_id=?", (class_id,))

            students = [_student(r['student_id']) for r in enr if _student(r['student_id'])]



        cards = []

        for s in students:

            sid = s['id']

            cards.append({

                'studentId': sid,

                'name': s.get('name', sid),

                'classId': class_id,

                'className': cls_obj.get('name', class_id) if cls_obj else class_id,

                'term': period_id,

                'status': 'Issued' if (s.get('attendance', 95) or 95) > 94 else 'Ready',

                'lastGenerated': '2026-10-23',

                'gpa': s.get('gpa', 3.8),

                'attendance': s.get('attendance', 96)

            })

        return jsonify({'data': {'items': cards, 'total': len(cards)}})



    student_id = request.args.get('studentId')

    if user['role'] == 'student': student_id = user['id']

    if user['role'] == 'parent' and student_id and not _parent_can_view(user, student_id): return _academic_error('FORBIDDEN', 'This student is not linked to your account', 403)

    if not student_id: return _academic_error('VALIDATION_ERROR', 'studentId is required')

    student = _student(student_id)

    if not student: return _academic_error('NOT_FOUND', 'Student not found', 404)

    period_id = request.args.get('periodId', 'gp-term-2'); grades = academic_grades_for_report(student_id, period_id)

    return jsonify({'data': {'student': student, 'gradingPeriod': ACADEMIC.one('SELECT * FROM grading_periods WHERE id=?', (period_id,)), 'grades': grades, 'gpa': ACADEMIC.aggregate_gpa(student_id, period_id), 'attendance': ACADEMIC.attendance_summary(student_id)}})



def academic_grades_for_report(student_id, period_id):

    rows = ACADEMIC.query('''SELECT g.*, a.title AS assessment_title, a.max_score, a.class_id, a.subject_id, a.grading_period_id, a.category FROM grades g JOIN assessments a ON a.id=g.assessment_id WHERE g.student_id=? AND a.grading_period_id=? ORDER BY a.subject_id, a.title''', (student_id, period_id))

    return [_academic_grade_row(r) for r in rows]



# ── ACADEMIC TRANSCRIPTS (PERSISTENT FILE & RECORD STORE) ─────────

TRANSCRIPTS_FILE = os.path.join(ROOT, 'data', 'transcripts.json')

TRANSCRIPTS_UPLOAD_DIR = os.path.join(ROOT, 'assets', 'uploads', 'transcripts')

os.makedirs(TRANSCRIPTS_UPLOAD_DIR, exist_ok=True)



def load_transcripts():

    if not os.path.exists(TRANSCRIPTS_FILE):

        return []

    try:

        with open(TRANSCRIPTS_FILE, 'r', encoding='utf-8') as f:

            return json.load(f)

    except Exception as e:

        print(f"Error loading transcripts.json: {e}")

        return []



def save_transcripts(items):

    try:

        os.makedirs(os.path.dirname(TRANSCRIPTS_FILE), exist_ok=True)

        with open(TRANSCRIPTS_FILE, 'w', encoding='utf-8') as f:

            json.dump(items, f, indent=2, ensure_ascii=False)

        return True

    except Exception as e:

        print(f"Error saving transcripts.json: {e}")

        return False



def _format_bytes(num_bytes):

    if num_bytes < 1024:

        return f"{num_bytes} B"

    elif num_bytes < 1024 * 1024:

        return f"{num_bytes / 1024:.1f} KB"

    else:

        return f"{num_bytes / (1024 * 1024):.2f} MB"



def _resolve_transcript_user():

    user = _academic_user()

    if user:

        return user

    token = request.headers.get('X-Auth-Token') or request.form.get('authToken') or request.args.get('token')

    if token:

        for role, email in {

            'admin': 'admin@ngis.edu.kh', 'principal': 'principal@ngis.edu.kh',

            'teacher': 'teacher@ngis.edu.kh', 'student': 'student@ngis.edu.kh',

            'parent': 'parent@ngis.edu.kh', 'staff': 'staff@ngis.edu.kh'

        }.items():

            if token == f'mock-jwt-token-{role}':

                u = dict(AUTH_USERS[email])

                if role == 'student': u['id'] = '2026-STD-0142'

                return u

    referer = request.headers.get('Referer', '').lower()

    if '/teacher/' in referer:

        return dict(AUTH_USERS['teacher@ngis.edu.kh'])

    if '/student/' in referer:

        u = dict(AUTH_USERS['student@ngis.edu.kh'])

        u['id'] = '2026-STD-0142'

        return u

    return None



@app.route('/api/academic/transcripts/upload', methods=['POST'])

def upload_academic_transcript():

    user = _resolve_transcript_user()

    if not user:

        return jsonify({'error': {'code': 'UNAUTHORIZED', 'message': 'Authentication required to upload transcripts'}}), 401

    if user.get('role') not in ('teacher', 'admin', 'principal'):

        return jsonify({'error': {'code': 'FORBIDDEN', 'message': 'Only teachers and administrators are permitted to upload and assign transcripts'}}), 403



    if 'file' not in request.files:

        return jsonify({'error': {'code': 'MISSING_FILE', 'message': 'No file was provided in the upload request'}}), 400



    file = request.files['file']

    if not file or file.filename == '':

        return jsonify({'error': {'code': 'EMPTY_FILE', 'message': 'Please select a valid file to upload'}}), 400



    orig_name = os.path.basename(file.filename)

    ext = orig_name.rsplit('.', 1)[-1].lower() if '.' in orig_name else ''

    allowed_exts = {'pdf', 'png', 'jpg', 'jpeg', 'webp'}

    if ext not in allowed_exts:

        return jsonify({'error': {'code': 'INVALID_FILE_TYPE', 'message': f'File format .{ext} is not allowed. Only PDF and image formats (.png, .jpg, .webp) are accepted.'}}), 400



    file_bytes = file.read()

    size_bytes = len(file_bytes)

    max_size = 15 * 1024 * 1024

    if size_bytes > max_size:

        return jsonify({'error': {'code': 'FILE_TOO_LARGE', 'message': f'File size ({_format_bytes(size_bytes)}) exceeds the maximum allowed limit of 15 MB'}}), 400

    if size_bytes == 0:

        return jsonify({'error': {'code': 'EMPTY_FILE', 'message': 'The uploaded file is empty (0 bytes)'}}), 400



    student_id = request.form.get('studentId', '').strip()

    if not student_id:

        return jsonify({'error': {'code': 'MISSING_STUDENT', 'message': 'Student ID is required to assign this transcript'}}), 400



    student_name = request.form.get('studentName', '').strip()

    if not student_name:

        st_obj = _student(student_id)

        student_name = st_obj.get('name') if st_obj else student_id



    term = request.form.get('term', 'Semester 1 (2025–26)').strip()

    class_grade = request.form.get('classGrade', 'Grade 10A').strip()

    notes = request.form.get('notes', '').strip()



    mime = 'application/pdf' if ext == 'pdf' else f'image/{ext if ext != "jpg" else "jpeg"}'



    timestamp = int(datetime.now().timestamp())

    clean_student_id = re.sub(r'[^a-zA-Z0-9_\-]', '', student_id)

    clean_base = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', orig_name)

    stored_filename = f"tr_{timestamp}_{clean_student_id}_{clean_base}"

    stored_path = os.path.join(TRANSCRIPTS_UPLOAD_DIR, stored_filename)



    with open(stored_path, 'wb') as f:

        f.write(file_bytes)



    transcripts = load_transcripts()

    new_id = f"tr_{timestamp}_{uuid.uuid4().hex[:6]}"

    uploader_name = user.get('name') or f"{user.get('firstName', '')} {user.get('lastName', '')}".strip() or "Dr. Sarah Jenkins"



    record = {

        'id': new_id,

        'studentId': student_id,

        'studentName': student_name,

        'classGrade': class_grade,

        'term': term,

        'fileName': orig_name,

        'storedFileName': stored_filename,

        'fileUrl': f"/assets/uploads/transcripts/{stored_filename}",

        'fileType': mime,

        'fileSize': _format_bytes(size_bytes),

        'fileSizeBytes': size_bytes,

        'uploadedBy': uploader_name,

        'uploadedByRole': user.get('role', 'teacher'),

        'uploadedAt': datetime.now().isoformat(),

        'status': 'Official Released',

        'verified': True,

        'notes': notes

    }



    updated = [t for t in transcripts if not (t.get('studentId') == student_id and t.get('term') == term)]

    updated.insert(0, record)

    save_transcripts(updated)



    return jsonify({

        'success': True,

        'data': record,

        'message': f"Official transcript uploaded and assigned to {student_name} ({student_id}) successfully."

    }), 201



@app.route('/api/academic/transcripts', methods=['GET'])

def get_academic_transcripts():

    user = _resolve_transcript_user()

    transcripts = load_transcripts()

    student_id = request.args.get('studentId')

    term = request.args.get('term')



    if user and user.get('role') == 'student':

        student_id = user.get('id', '2026-STD-0142')



    if student_id:

        transcripts = [t for t in transcripts if t.get('studentId') == student_id]

    if term:

        transcripts = [t for t in transcripts if t.get('term') == term]



    return jsonify({'success': True, 'data': transcripts, 'total': len(transcripts)})



@app.route('/api/academic/transcripts/<student_id>', methods=['GET'])

def get_student_transcript(student_id):

    user = _resolve_transcript_user()

    if student_id == 'STU-2024-089' or student_id == 'me':

        student_id = '2026-STD-0142'

    if user and user.get('role') == 'student':

        student_id = user.get('id', '2026-STD-0142')



    transcripts = load_transcripts()

    matching = [t for t in transcripts if t.get('studentId') == student_id]

    if not matching:

        return jsonify({'success': False, 'data': None, 'message': f'No official transcript found for student {student_id}'}), 404



    return jsonify({'success': True, 'data': matching[0]})



@app.route('/api/academic/transcripts/<transcript_id>', methods=['DELETE'])

def delete_academic_transcript(transcript_id):

    user = _resolve_transcript_user()

    if not user:

        return jsonify({'error': {'code': 'UNAUTHORIZED', 'message': 'Authentication required'}}), 401

    if user.get('role') not in ('teacher', 'admin', 'principal'):

        return jsonify({'error': {'code': 'FORBIDDEN', 'message': 'Only teachers and administrators can delete transcripts'}}), 403



    transcripts = load_transcripts()

    target = next((t for t in transcripts if t.get('id') == transcript_id), None)

    if not target:

        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Transcript record not found'}}), 404



    stored_file = target.get('storedFileName')

    if stored_file:

        file_path = os.path.join(TRANSCRIPTS_UPLOAD_DIR, stored_file)

        if os.path.exists(file_path):

            try:

                os.remove(file_path)

            except Exception as e:

                print(f"Error removing file {file_path}: {e}")



    remaining = [t for t in transcripts if t.get('id') != transcript_id]

    save_transcripts(remaining)

    return jsonify({'success': True, 'message': 'Transcript removed successfully'})



@app.route('/api/academic/transcripts/download/<transcript_id>', methods=['GET'])

def download_academic_transcript(transcript_id):

    transcripts = load_transcripts()

    target = next((t for t in transcripts if t.get('id') == transcript_id), None)

    if not target:

        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Transcript not found'}}), 404



    user = _resolve_transcript_user()

    if user and user.get('role') == 'student' and user.get('id') != target.get('studentId'):

        return jsonify({'error': {'code': 'FORBIDDEN', 'message': 'Unauthorized to download this transcript'}}), 403



    stored_file = target.get('storedFileName')

    file_path = os.path.join(TRANSCRIPTS_UPLOAD_DIR, stored_file)

    if not os.path.exists(file_path):

        return jsonify({'error': {'code': 'FILE_NOT_FOUND', 'message': 'Transcript file is missing from storage'}}), 404



    return send_from_directory(TRANSCRIPTS_UPLOAD_DIR, stored_file, as_attachment=True, download_name=target.get('fileName', stored_file))





@app.route('/api/academic/audit', methods=['GET'])

def academic_audit():

    user, error = _academic_require(('admin', 'principal'))

    if error: return error

    limit = min(max(int(request.args.get('limit', 50)), 1), 200)

    return jsonify({'data': ACADEMIC.query('SELECT * FROM audit_events ORDER BY id DESC LIMIT ?', (limit,)), 'meta': {'total': limit}})



@app.route('/api/academic/attendance-by-class', methods=['GET'])

def academic_attendance_by_class():

    user, error = _academic_require()

    if error: return error

    student_id = request.args.get('studentId')

    if user['role'] == 'student':

        student_id = user['id']

    elif user['role'] == 'parent':

        if not student_id:

            parent = next((p for p in DB['parents'] if p.get('id') == user['id']), DB['parents'][0])

            student_id = (parent.get('children', ['2026-STD-0142'])[0]) if parent else '2026-STD-0142'

        if not _parent_can_view(user, student_id):

            return _academic_error('FORBIDDEN', 'This student is not linked to your account', 403)

    elif not student_id:

        student_id = '2026-STD-0142'



    student = _student(student_id)

    if not student:

        return _academic_error('NOT_FOUND', 'Student not found', 404)



    data = ACADEMIC.get_attendance_by_class(student_id)

    data['student'] = {

        'id': student['id'],

        'name': student['name'],

        'grade': student.get('grade', 'Grade 11'),

        'class': student.get('class', '11C'),

        'stream': 'Science & Social Studies Stream',

        'advisor': 'Ms. Rathana Chea'

    }

    return jsonify({'data': data})



@app.route('/api/academic/course-details', methods=['GET'])

def academic_course_details():

    user, error = _academic_require()

    if error: return error

    student_id = request.args.get('studentId')

    if user['role'] == 'student':

        student_id = user['id']

    elif user['role'] == 'parent':

        if not student_id:

            parent = next((p for p in DB['parents'] if p.get('id') == user['id']), DB['parents'][0])

            student_id = (parent.get('children', ['2026-STD-0142'])[0]) if parent else '2026-STD-0142'

        if not _parent_can_view(user, student_id):

            return _academic_error('FORBIDDEN', 'This student is not linked to your account', 403)

    elif not student_id:

        student_id = '2026-STD-0142'



    subject_id = request.args.get('subjectId')

    if not subject_id:

        return _academic_error('VALIDATION_ERROR', 'subjectId is required')



    period_id = request.args.get('periodId') or request.args.get('periodCode')

    assessments = ACADEMIC.get_course_assessments(student_id, subject_id, period_id)

    subject = ACADEMIC.one('SELECT * FROM subjects WHERE id=?', (subject_id,)) or {'name': subject_id}

    return jsonify({'data': {'subject': dict(subject), 'assessments': assessments, 'total': len(assessments)}})



@app.route('/api/academic/attendance-by-day', methods=['GET'])

def academic_attendance_by_day():

    user, error = _academic_require()

    if error: return error

    student_id = request.args.get('studentId')

    if user['role'] == 'student':

        student_id = user['id']

    elif user['role'] == 'parent':

        if not student_id:

            parent = next((p for p in DB['parents'] if p.get('id') == user['id']), DB['parents'][0])

            student_id = (parent.get('children', ['2026-STD-0142'])[0]) if parent else '2026-STD-0142'

        if not _parent_can_view(user, student_id):

            return _academic_error('FORBIDDEN', 'This student is not linked to your account', 403)

    elif not student_id:

        student_id = '2026-STD-0142'



    limit = min(max(int(request.args.get('limit', 50)), 1), 200)

    records = ACADEMIC.get_daily_attendance(student_id, limit)

    summary = ACADEMIC.attendance_summary(student_id)

    return jsonify({'data': {'studentId': student_id, 'records': records, 'summary': summary, 'total': len(records)}})



@app.route('/api/academic/gradebook', methods=['GET'])

def academic_gradebook():

    user, error = _academic_require(('teacher', 'admin', 'principal'))

    if error: return error

    class_id = request.args.get('classId', 'cls-10a')

    subject_id = request.args.get('subjectId', 'subj-math')

    period_id = request.args.get('periodId', 'gp-q1')



    if user['role'] == 'teacher' and not _teacher_can_class(user, class_id):

        return _academic_error('FORBIDDEN', 'You are not assigned to this class', 403)



    # Assessments for this class, subject, period

    assessments = ACADEMIC.query(

        """SELECT * FROM assessments WHERE class_id=? AND subject_id=? AND (grading_period_id=? OR grading_period_id IN (SELECT id FROM grading_periods WHERE code=?)) ORDER BY created_at""",

        (class_id, subject_id, period_id, period_id)

    )



    # Roster

    enrollment_rows = ACADEMIC.query(

        """SELECT student_id FROM enrollments WHERE class_id=? AND academic_year_id='ay-2025-26'""",

        (class_id,)

    )

    student_ids = [r['student_id'] for r in enrollment_rows]

    if not student_ids:

        cls_name = next((c.get('name','').replace('Grade ','') for c in DB['classes'] if c.get('id') == class_id), '')

        student_ids = [s['id'] for s in DB['students'] if s.get('class') == cls_name]

        if not student_ids:

            student_ids = ['2026-STD-0142', '2026-STD-0144']



    students_out = []

    for sid in student_ids:

        st = _student(sid) or {'id': sid, 'name': sid}

        student_grades = {}

        total_score = 0.0

        total_max = 0.0

        has_any = False

        workflow_state = 'draft'



        for a in assessments:

            gr = ACADEMIC.one("SELECT score, state, comments, workflow FROM grades WHERE assessment_id=? AND student_id=?", (a['id'], sid))

            if gr and gr['score'] is not None:

                student_grades[a['id']] = {

                    'score': gr['score'],

                    'comments': gr['comments'] or '',

                    'workflow': gr['workflow'] or 'draft'

                }

                total_score += float(gr['score']) * float(a.get('weight', 1.0))

                total_max += float(a['max_score']) * float(a.get('weight', 1.0))

                has_any = True

                workflow_state = gr['workflow']

            else:

                student_grades[a['id']] = {

                    'score': '',

                    'comments': '',

                    'workflow': 'draft'

                }



        calc_pct = (total_score / total_max * 100) if total_max > 0 else None

        letter, pts = ACADEMIC.grade_band(calc_pct)



        students_out.append({

            'id': sid,

            'name': st.get('name', sid),

            'number': sid,

            'grades': student_grades,

            'totalPercentage': round(calc_pct, 1) if calc_pct is not None else 0,

            'letterGrade': letter if calc_pct is not None else '—',

            'workflow': workflow_state if has_any else 'draft'

        })



    cls_obj = next((c for c in DB['classes'] if c.get('id') == class_id), {'id': class_id, 'name': class_id})

    subj_obj = ACADEMIC.one("SELECT * FROM subjects WHERE id=?", (subject_id,)) or {'id': subject_id, 'name': subject_id}

    period_obj = ACADEMIC.one("SELECT * FROM grading_periods WHERE id=? OR code=?", (period_id, period_id)) or {'id': period_id, 'name': period_id}



    return jsonify({

        'data': {

            'class': cls_obj,

            'subject': dict(subj_obj),

            'period': dict(period_obj),

            'assessments': assessments,

            'students': students_out

        }

    })



@app.route('/api/academic/gradebook/batch', methods=['POST'])

def academic_gradebook_batch():

    user, error = _academic_require(('teacher', 'admin', 'principal'))

    if error: return error

    data = request.get_json(silent=True) or {}

    class_id = data.get('classId')

    subject_id = data.get('subjectId')

    period_id = data.get('periodId', 'gp-q1')

    workflow = data.get('workflow', 'draft')



    if not class_id or not subject_id:

        return _academic_error('VALIDATION_ERROR', 'classId and subjectId are required')

    if user['role'] == 'teacher' and not _teacher_can_class(user, class_id):

        return _academic_error('FORBIDDEN', 'You are not assigned to this class', 403)



    grades_list = data.get('grades', [])

    now = ACADEMIC.now()

    statements = []



    for item in grades_list:

        student_id = item.get('studentId')

        assessment_id = item.get('assessmentId')

        score = item.get('score')

        comments = item.get('comments', '')

        if not student_id or not assessment_id:

            continue



        numeric_score = float(score) if score not in (None, '', '—') else None

        state = 'graded' if numeric_score is not None else 'missing'

        grd_id = ACADEMIC.new_id('grd')



        statements.append((

            """INSERT INTO grades(id, assessment_id, student_id, score, state, comments, workflow, recorded_by, recorded_at, updated_at)

               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

               ON CONFLICT(assessment_id, student_id) DO UPDATE SET

                 score=excluded.score, state=excluded.state, comments=excluded.comments,

                 workflow=excluded.workflow, updated_at=excluded.updated_at, recorded_by=excluded.recorded_by""",

            (grd_id, assessment_id, student_id, numeric_score, state, comments, workflow, user['id'], now, now)

        ))



    if statements:

        try:

            ACADEMIC.transaction(statements)

        except Exception as exc:

            return _academic_error('DATABASE_ERROR', f'Could not save batch grades: {exc}', 500)



    ACADEMIC.audit(user['id'], user['role'], 'GRADEBOOK_BATCH_SAVE', 'class', class_id, data.get('reason', ''), {'count': len(statements), 'workflow': workflow})

    return jsonify({'message': f'Successfully saved {len(statements)} grade record(s)', 'workflow': workflow}), 200



@app.route('/api/academic/assessments', methods=['POST'])

def academic_create_assessment():

    user, error = _academic_require(('teacher', 'admin', 'principal'))

    if error: return error

    data = request.get_json(silent=True) or {}

    required = ['classId', 'subjectId', 'title', 'maxScore']

    for req in required:

        if not data.get(req):

            return _academic_error('VALIDATION_ERROR', f'{req} is required')



    class_id = data['classId']

    if user['role'] == 'teacher' and not _teacher_can_class(user, class_id):

        return _academic_error('FORBIDDEN', 'You are not assigned to this class', 403)



    asm_id = ACADEMIC.new_id('asm')

    period_id = data.get('gradingPeriodId', 'gp-q1')

    now = ACADEMIC.now()

    weight = float(data.get('weight', 1.0))

    max_score = float(data.get('maxScore', 100))

    category = data.get('category', 'Quiz')

    due_date = data.get('dueDate', now[:10])



    ACADEMIC.execute(

        """INSERT INTO assessments(id, class_id, subject_id, grading_period_id, title, category, max_score, weight, teacher_id, status, created_at, due_date)

           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'published', ?, ?)""",

        (asm_id, class_id, data['subjectId'], period_id, data['title'].strip(), category, max_score, weight, user['id'], now, due_date)

    )



    ACADEMIC.audit(user['id'], user['role'], 'ASSESSMENT_CREATE', 'assessment', asm_id, '', {'title': data['title']})

    created = ACADEMIC.one("SELECT * FROM assessments WHERE id=?", (asm_id,))

    return jsonify({'data': created, 'message': 'Assessment created successfully'}), 201



@app.route('/api/academic/admin/publish-grades', methods=['POST'])

def academic_admin_publish_grades():

    user, error = _academic_require(('admin', 'principal'))

    if error: return error

    data = request.get_json(silent=True) or {}

    class_id = data.get('classId')

    subject_id = data.get('subjectId')

    period_id = data.get('periodId')



    clauses = ["g.workflow IN ('submitted', 'draft')"]

    args = []

    if class_id:

        clauses.append("a.class_id=?"); args.append(class_id)

    if subject_id:

        clauses.append("a.subject_id=?"); args.append(subject_id)

    if period_id:

        clauses.append("(a.grading_period_id=? OR a.grading_period_id IN (SELECT id FROM grading_periods WHERE code=?))")

        args.extend([period_id, period_id])



    now = ACADEMIC.now()

    sql = f"""UPDATE grades SET workflow='published', updated_at='{now}'

              WHERE id IN (

                SELECT g.id FROM grades g JOIN assessments a ON a.id=g.assessment_id

                WHERE {' AND '.join(clauses)}

              )"""

    ACADEMIC.execute(sql, args)

    ACADEMIC.audit(user['id'], user['role'], 'GRADES_BULK_PUBLISH', 'grades', class_id or 'all', data.get('reason', ''), {'periodId': period_id})

    return jsonify({'message': 'Grades published successfully'}), 200



@app.route('/api/academic/admin/override-grade', methods=['POST'])

def academic_admin_override_grade():

    user, error = _academic_require(('admin', 'principal'))

    if error: return error

    data = request.get_json(silent=True) or {}

    grade_id = data.get('gradeId')

    score = data.get('score')

    reason = data.get('reason', '').strip()



    if not grade_id or score is None:

        return _academic_error('VALIDATION_ERROR', 'gradeId and score are required')

    if not reason:

        return _academic_error('VALIDATION_ERROR', 'Reason is mandatory for administrative grade overrides')



    row = ACADEMIC.one("SELECT * FROM grades WHERE id=?", (grade_id,))

    if not row:

        return _academic_error('NOT_FOUND', 'Grade record not found', 404)



    now = ACADEMIC.now()

    prev_score = row['score']

    ACADEMIC.execute("UPDATE grades SET score=?, state='graded', updated_at=? WHERE id=?", (float(score), now, grade_id))

    ACADEMIC.audit(user['id'], user['role'], 'GRADE_OVERRIDE', 'grade', grade_id, reason, {'previousScore': prev_score, 'newScore': float(score)})

    updated = ACADEMIC.one("SELECT * FROM grades WHERE id=?", (grade_id,))

    return jsonify({'data': updated, 'message': 'Grade override recorded in academic audit log'}), 200



@app.route('/api/academic/admin/override-attendance', methods=['POST'])

def academic_admin_override_attendance():

    user, error = _academic_require(('admin', 'principal'))

    if error: return error

    data = request.get_json(silent=True) or {}

    att_id = data.get('attendanceId') or data.get('attendance_id')

    status = (data.get('status') or '').strip().lower()

    reason = (data.get('reason') or '').strip()



    if status == 'late': status = 'tardy'

    if status not in ('present', 'absent', 'tardy', 'excused'):

        return _academic_error('VALIDATION_ERROR', 'Status must be present, absent, tardy, or excused')

    if not reason:

        return _academic_error('VALIDATION_ERROR', 'Reason is mandatory for administrative attendance corrections')



    row = ACADEMIC.one("SELECT * FROM attendance WHERE id=?", (att_id,))

    if not row:

        return _academic_error('NOT_FOUND', 'Attendance record not found', 404)



    now = ACADEMIC.now()

    prev_status = row['status']

    note_update = f"{row['note'] or ''} [Corrected: {reason}]".strip()

    ACADEMIC.execute("UPDATE attendance SET status=?, note=?, updated_at=?, recorded_by=? WHERE id=?", (status, note_update, now, user['id'], att_id))

    ACADEMIC.audit(user['id'], user['role'], 'ATTENDANCE_CORRECTION', 'attendance', att_id, reason, {

        'previousStatus': prev_status,

        'newStatus': status,

        'studentId': row['student_id'],

        'date': row['attendance_date']

    })

    updated = ACADEMIC.one("SELECT * FROM attendance WHERE id=?", (att_id,))

    return jsonify({'data': updated, 'message': 'Attendance record corrected and audited'}), 200



@app.route('/api/academic/admin/oversight', methods=['GET'])

def academic_admin_oversight():

    user, error = _academic_require(('admin', 'principal'))

    if error: return error



    # Overall stats

    total_students = len(DB['students'])

    total_classes = len(DB['classes'])

    pending_grades = ACADEMIC.one("SELECT COUNT(*) AS n FROM grades WHERE workflow='submitted'")['n']

    published_grades = ACADEMIC.one("SELECT COUNT(*) AS n FROM grades WHERE workflow='published'")['n']

    total_assessments = ACADEMIC.one("SELECT COUNT(*) AS n FROM assessments")['n']



    # Grade distribution

    grades_rows = ACADEMIC.query("SELECT g.score, a.max_score FROM grades g JOIN assessments a ON a.id=g.assessment_id WHERE g.workflow='published' AND g.score IS NOT NULL")

    distribution = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}

    for g in grades_rows:

        pct = (float(g["score"]) / float(g["max_score"]) * 100) if g["max_score"] else 0

        letter, _ = ACADEMIC.grade_band(pct)

        base_letter = letter[0] if letter != '—' else 'F'

        if base_letter in distribution:

            distribution[base_letter] += 1



    return jsonify({

        'data': {

            'totalStudents': total_students,

            'totalClasses': total_classes,

            'pendingGrades': pending_grades,

            'publishedGrades': published_grades,

            'totalAssessments': total_assessments,

            'averageGpa': 3.72,

            'distribution': distribution

        }

    })



@app.route('/api/academic/report-cards/details', methods=['GET'])

def academic_report_card_details():

    user, error = _academic_require()

    if error: return error

    student_id = request.args.get('studentId')

    if user['role'] == 'student':

        student_id = user['id']

    elif user['role'] == 'parent':

        if not student_id:

            parent = next((p for p in DB['parents'] if p.get('id') == user['id']), DB['parents'][0])

            student_id = (parent.get('children', ['2026-STD-0142'])[0]) if parent else '2026-STD-0142'

        if not _parent_can_view(user, student_id):

            return _academic_error('FORBIDDEN', 'This student is not linked to your account', 403)

    elif not student_id:

        student_id = '2026-STD-0142'



    student = _student(student_id)

    if not student:

        return _academic_error('NOT_FOUND', 'Student not found', 404)



    matrix = ACADEMIC.get_attendance_by_class(student_id)

    att_summary = ACADEMIC.attendance_summary(student_id)

    gpa_info = ACADEMIC.calculate_gpa(student_id)



    return jsonify({

        'data': {

            'student': {

                'id': student['id'],

                'name': student['name'],

                'grade': student.get('grade', 'Grade 11'),

                'class': student.get('class', '11C'),

                'dob': '2008-04-18',

                'stream': 'Science & Social Studies Stream',

                'advisor': 'Ms. Rathana Chea',

                'principal': 'Dr. Ly Bunheng'

            },

            'academicYear': '2025–2026',

            'semester': 'Semester 1 & Continuous Assessment',

            'weightedGpa': gpa_info['weighted'] if gpa_info['weighted'] > 0 else 3.88,

            'unweightedGpa': gpa_info['unweighted'] if gpa_info['unweighted'] > 0 else 3.75,

            'attendanceSummary': att_summary,

            'courses': matrix['courses'],

            'issueDate': 'October 23, 2026',

            'verifiedBy': 'Office of the Academic Registry · New Gateway International School'

        }

    })



@app.route('/api/auth/login', methods=['POST'])

def auth_login():

    data = request.get_json(silent=True) or {}

    email = data.get('email', '').strip().lower()

    password = data.get('password', '')

    user = AUTH_USERS.get(email)

    if not user or password != 'password123':

        return _academic_error('INVALID_CREDENTIALS', 'Invalid email or password', 401)

    token = f"mock-jwt-token-{user['role']}"

    return jsonify({

        'data': {

            'token': token,

            'user': user

        }

    })



@app.route('/api/auth/me', methods=['GET'])

def auth_me():

    user = _academic_user()

    if not user:

        return _academic_error('UNAUTHORIZED', 'A valid session is required', 401)

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

    user = _academic_user()

    if not user:

        return _academic_error('UNAUTHORIZED', 'Authentication required', 401)



    classes_list = DB['classes']

    teacher_name = 'Dr. Sarah Jenkins'

    if user['role'] == 'teacher':

        teacher = next((t for t in DB['teachers'] if t.get('id') == user['id'] or t.get('email') == user.get('email')), DB['teachers'][0])

        teacher_name = teacher.get('name', 'Dr. Sarah Jenkins')

        assigned_names = [c.replace('Grade ', '') for c in teacher.get('classes', [])]

        classes_list = [c for c in DB['classes'] if c.get('name', '').replace('Grade ', '') in assigned_names or c.get('id') in assigned_names]

        if not classes_list:

            classes_list = DB['classes'][:3]



    enriched = []

    for c in classes_list:

        cid = c['id']

        c_code = c.get('name','').replace('Grade ','')

        c_students = [s for s in DB['students'] if s.get('class') == c_code]

        asgns = [a for a in DB['assignments'] if a.get('classId') == cid]

        pending_subs = sum(len([s for s in a.get('submissions', []) if s.get('status') == 'submitted']) for a in asgns)



        att_rows = ACADEMIC.query("SELECT status FROM attendance WHERE class_id=? AND attendance_date=?", (cid, ACADEMIC.now()[:10]))

        att_rate = 96.4

        if att_rows:

            p_cnt = sum(1 for r in att_rows if r['status'] == 'present')

            att_rate = round(p_cnt / len(att_rows) * 100, 1)



        enriched.append({

            **c,

            'studentCount': len(c_students) if c_students else c.get('studentCount', 28),

            'pendingSubmissions': pending_subs,

            'activeAssignments': len(asgns),

            'attendanceRate': att_rate,

            'department': 'Mathematics & Sciences',

            'isHomeroom': c.get('homeroomTeacher') == teacher_name

        })



    return jsonify({'data': enriched, 'meta': {'total': len(enriched)}})



@app.route('/api/teacher/classes/<class_id>/workspace', methods=['GET'])

def get_teacher_class_workspace(class_id):

    user, error = _academic_require(('teacher', 'admin', 'principal'))

    if error: return error

    if user['role'] == 'teacher' and not _teacher_can_class(user, class_id):

        return _academic_error('FORBIDDEN', 'You are not assigned to this class', 403)



    cls_obj = next((c for c in DB['classes'] if c.get('id') == class_id), None)

    if not cls_obj:

        return _academic_error('NOT_FOUND', 'Class not found', 404)



    cls_code = cls_obj.get('name', '').replace('Grade ', '')

    students = [s for s in DB['students'] if s.get('class') == cls_code]

    if not students:

        enr = ACADEMIC.query("SELECT student_id FROM enrollments WHERE class_id=?", (class_id,))

        s_ids = [r['student_id'] for r in enr]

        students = [_student(sid) for sid in s_ids if _student(sid)]

    if not students:

        students = [DB['students'][0]]



    # Assignments for this class

    asgns = [a for a in DB['assignments'] if a.get('classId') == class_id]



    # Submissions

    all_subs = []

    for a in asgns:

        for s in a.get('submissions', []):

            st_obj = _student(s.get('studentId'))

            all_subs.append({

                **s,

                'assignmentId': a['id'],

                'assignmentTitle': a['title'],

                'maxScore': a.get('maxScore', 100),

                'studentName': st_obj.get('name', s.get('studentId')) if st_obj else s.get('studentId')

            })



    # Attendance today

    today_str = ACADEMIC.now()[:10]

    att_today_rows = ACADEMIC.query("SELECT * FROM attendance WHERE class_id=? AND attendance_date=?", (class_id, today_str))

    marked_count = len(att_today_rows)

    present_count = sum(1 for r in att_today_rows if r['status'] == 'present')

    late_count = sum(1 for r in att_today_rows if r['status'] in ('late', 'tardy'))

    absent_count = sum(1 for r in att_today_rows if r['status'] == 'absent')

    excused_count = sum(1 for r in att_today_rows if r['status'] == 'excused')

    att_pct = round((present_count / marked_count * 100), 1) if marked_count > 0 else 96.4



    # Lessons

    lessons = [l for l in DB.get('lessons', []) if l.get('classId') == class_id or l.get('class') == cls_obj.get('name')]

    if not lessons and DB.get('lessons'):

        lessons = [DB['lessons'][0]]



    # Gradebook completion

    grades_count = ACADEMIC.one(

        "SELECT COUNT(*) as n FROM grades g JOIN assessments a ON a.id=g.assessment_id WHERE a.class_id=?",

        (class_id,)

    )['n']



    pending_subs_count = sum(1 for s in all_subs if s.get('status') == 'submitted')



    teacher = next((t for t in DB['teachers'] if t.get('id') == user['id']), DB['teachers'][0])

    is_homeroom = cls_obj.get('homeroomTeacher') == teacher.get('name')



    workspace_data = {

        'class': {

            'id': cls_obj['id'],

            'name': cls_obj['name'],

            'grade': cls_obj.get('grade', '10'),

            'section': cls_obj.get('section', 'A'),

            'room': cls_obj.get('room', 'Room 302'),

            'campus': cls_obj.get('campus', 'Sensok'),

            'department': 'Mathematics & Sciences',

            'academicYear': '2025–2026',

            'semester': 'Semester 1 (Active)',

            'homeroomTeacher': cls_obj.get('homeroomTeacher', 'Dr. Sarah Jenkins'),

            'isHomeroom': is_homeroom,

            'enrolledCount': len(students),

        },

        'overview': {

            'enrolledStudents': len(students),

            'attendanceToday': {

                'isMarked': marked_count > 0,

                'rate': att_pct,

                'present': present_count,

                'tardy': late_count,

                'absent': absent_count,

                'excused': excused_count,

                'totalMarked': marked_count,

                'rosterTotal': len(students)

            },

            'pendingSubmissions': pending_subs_count,

            'activeAssignments': len(asgns),

            'gradebookCompletion': 98 if grades_count > 0 else 85,

            'publishedLessons': len(lessons),

            'pendingActions': pending_subs_count + (0 if marked_count > 0 else 1)

        },

        'students': students,

        'assignments': asgns,

        'submissions': all_subs,

        'lessons': lessons,

        'attendanceSummary': {

            'averageRate': att_pct,

            'presentDays': 42,

            'totalSessions': 44

        }

    }

    return jsonify({'data': workspace_data})



@app.route('/api/teacher/classes/<class_id>/students', methods=['GET'])

def get_teacher_class_students(class_id):

    user, error = _academic_require(('teacher', 'admin', 'principal'))

    if error: return error

    if user['role'] == 'teacher' and not _teacher_can_class(user, class_id):

        return _academic_error('FORBIDDEN', 'You are not assigned to this class', 403)



    cls_obj = next((c for c in DB['classes'] if c.get('id') == class_id), None)

    if not cls_obj:

        return _academic_error('NOT_FOUND', 'Class not found', 404)



    cls_code = cls_obj.get('name', '').replace('Grade ', '')

    students = [s for s in DB['students'] if s.get('class') == cls_code]

    return jsonify({'data': students, 'meta': {'total': len(students)}})



@app.route('/api/teacher/classes/<class_id>/submissions', methods=['GET'])

def get_teacher_class_submissions(class_id):

    user, error = _academic_require(('teacher', 'admin', 'principal'))

    if error: return error

    if user['role'] == 'teacher' and not _teacher_can_class(user, class_id):

        return _academic_error('FORBIDDEN', 'You are not assigned to this class', 403)



    asgns = [a for a in DB['assignments'] if a.get('classId') == class_id]

    all_subs = []

    for a in asgns:

        for s in a.get('submissions', []):

            st_obj = _student(s.get('studentId'))

            all_subs.append({

                **s,

                'assignmentId': a['id'],

                'assignmentTitle': a['title'],

                'maxScore': a.get('maxScore', 100),

                'studentName': st_obj.get('name', s.get('studentId')) if st_obj else s.get('studentId'),

                'dueDate': a.get('dueDate', a.get('due_date', '—'))

            })

    return jsonify({'data': all_subs, 'meta': {'total': len(all_subs)}})



@app.route('/api/teacher/exams', methods=['GET'])

def get_teacher_exams():

    user, error = _academic_require(('teacher', 'admin', 'principal'))

    if error: return error



    teacher_classes = ['cls-10a', 'cls-11b', 'cls-11c']



    my_exams = [

        {

            'id': 'exam-10a-math-midterm',

            'title': 'Mid-Term Exam: Advanced Mathematics',

            'subjectId': 'subj-math',

            'subjectName': 'Advanced Mathematics',

            'classId': 'cls-10a',

            'className': 'Grade 10A',

            'date': '2026-11-04',

            'time': '08:30 – 10:30',

            'room': 'Room 302',

            'role': 'Lead Examiner & Invigilator',

            'status': 'Scheduled',

            'enrolledCount': 17,

            'maxScore': 50,

            'isToday': False,

            'instructions': 'Distribute Formula Sheets (Form C) and scientific calculators. Scratch paper collected at end.'

        },

        {

            'id': 'exam-11b-phys-midterm',

            'title': 'Mid-Term Exam: Physics CP & Kinematics',

            'subjectId': 'subj-phys',

            'subjectName': 'Physics CP',

            'classId': 'cls-11b',

            'className': 'Grade 11B',

            'date': '2026-11-06',

            'time': '10:45 – 12:15',

            'room': 'Room 203',

            'role': 'Course Teacher',

            'status': 'Scheduled',

            'enrolledCount': 6,

            'maxScore': 50,

            'isToday': False,

            'instructions': 'Formula packet attached to exam booklet. Graphing calculators permitted.'

        },

        {

            'id': 'exam-10a-math-final',

            'title': 'Semester 1 Final Examination: Mathematics',

            'subjectId': 'subj-math',

            'subjectName': 'Advanced Mathematics',

            'classId': 'cls-10a',

            'className': 'Grade 10A',

            'date': '2026-12-14',

            'time': '08:30 – 11:00',

            'room': 'Room 302',

            'role': 'Chief Invigilator',

            'status': 'Upcoming',

            'enrolledCount': 17,

            'maxScore': 100,

            'isToday': False,

            'instructions': 'Formal institutional examination. Student ID check at door mandatory.'

        }

    ]



    invigilation_duties = [

        {

            'id': 'duty-inv-01',

            'examTitle': 'Mid-Term Exam: Advanced Mathematics',

            'classId': 'cls-10a',

            'className': 'Grade 10A',

            'room': 'Room 302',

            'date': '2026-11-04',

            'time': '08:30 – 10:30',

            'reportingTime': '08:10 (20 mins prior)',

            'dutyRole': 'Chief Invigilator',

            'partnerInvigilator': 'Muthukumaran Pakkirisamy',

            'studentCount': 17,

            'status': 'Confirmed',

            'conflict': None,

            'checklist': [

                'Collect test packets from Examination Office (Room 101) at 08:05',

                'Verify student photo IDs upon seating',

                'Ensure mobile phones and smart devices are powered off in bags at front',

                'Announce 15-minute remaining warning at 10:15',

                'Seal answer booklets in presence of student witness'

            ]

        },

        {

            'id': 'duty-inv-02',

            'examTitle': 'Final Written Test: Khmer Literature',

            'classId': 'cls-12a',

            'className': 'Grade 12A',

            'room': 'Room 407 (11C)',

            'date': '2026-11-05',

            'time': '13:30 – 15:30',

            'reportingTime': '13:15 (15 mins prior)',

            'dutyRole': 'Assistant Invigilator',

            'partnerInvigilator': 'Sokha Meng',

            'studentCount': 14,

            'status': 'Confirmed',

            'conflict': None,

            'checklist': [

                'Support Chief Invigilator with attendance roll verification',

                'Monitor room perimeter and corridor restroom transitions',

                'Collect test papers in alphabetical sequence'

            ]

        }

    ]



    room_arrangements = []

    for c_id in teacher_classes:

        c_obj = next((c for c in DB['classes'] if c.get('id') == c_id), None)

        if not c_obj: continue

        c_code = c_obj.get('name','').replace('Grade ','')

        students = [s for s in DB['students'] if s.get('class') == c_code]

        room_name = c_obj.get('room', 'Room 302')

        capacity = 24 if '302' in room_name else (20 if '203' in room_name else 16)

        is_over = len(students) > capacity



        room_arrangements.append({

            'roomId': c_obj.get('room', 'Room 302').lower().replace(' ', '-').replace('(', '').replace(')', ''),

            'roomName': room_name,

            'classId': c_id,

            'className': c_obj.get('name', c_id),

            'capacity': capacity,

            'assignedCount': len(students),

            'availableDesks': max(0, capacity - len(students)),

            'isOverCapacity': is_over,

            'students': [

                {

                    'id': s['id'],

                    'name': s['name'],

                    'desk': f"Desk {idx + 1:02d}",

                    'specialAccommodations': 'Standard' if idx % 4 != 0 else 'Extra 15 mins (IEP)'

                }

                for idx, s in enumerate(students)

            ],

            'supervisor': 'Dr. Sarah Jenkins',

            'emergencyExit': 'Stairwell B (North Wing)'

        })



    return jsonify({

        'data': {

            'exams': my_exams,

            'invigilations': invigilation_duties,

            'rooms': room_arrangements,

            'conflicts': []

        }

    })



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

@app.route('/api/classes/<class_id>', methods=['GET', 'PUT'])
def handle_single_class(class_id):
    c = next((item for item in DB['classes'] if item['id'] == class_id), None)
    if not c:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Class not found'}}), 404
    if request.method == 'GET':
        return jsonify({'data': c})
    # PUT
    data = request.get_json(silent=True) or {}
    for field in ['name', 'grade', 'section', 'room', 'homeroomTeacher', 'campus', 'studentCount']:
        if field in data:
            c[field] = data[field]
    return jsonify({'data': c, 'message': 'Class updated successfully'})




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



# ════════════════════════════════════════════════════════════════════

# PRINCIPAL CENTRAL MANAGEMENT & OVERSIGHT API LAYER

# ════════════════════════════════════════════════════════════════════

# Every item in this layer is derived from live records: the SQLite

# academic store (grade workflow + audit_events), the persisted

# transcript and service-request files, and the school rosters. The

# rosters are persisted through overlay JSON files so Principal edits

# survive server restarts. Decisions update the original records,

# notify the submitter, and write a durable audit trail.



# ── DESIGN / DEMO MODE FLAG ────────────────────────────────────

# When True, every /api/principal/* route reads and writes ONLY the

# in-memory PRINCIPAL_DEMO_STATE fixtures below. No SQLite queries,

# no overlay file writes, no notifications to real student/teacher

# accounts. Flip to False to reconnect the layer to the live store.

PRINCIPAL_DEMO_MODE = False



SERVICE_REQUESTS_FILE = os.path.join(ROOT, 'data', 'service_requests.json')

STUDENTS_OVERLAY_FILE = os.path.join(ROOT, 'data', 'students_overlay.json')



def _load_json_file(path, default=None):

    if not os.path.exists(path):

        return default

    try:

        with open(path, 'r', encoding='utf-8') as f:

            return json.load(f)

    except Exception as exc:

        print(f"Error loading {path}: {exc}")

        return default



def _write_json_file(path, payload):

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'w', encoding='utf-8') as f:

        json.dump(payload, f, indent=2, ensure_ascii=False)



def _persist_service_requests():

    if PRINCIPAL_DEMO_MODE:

        return  # design mode: never touch disk

    _write_json_file(SERVICE_REQUESTS_FILE, DB['serviceRequests'])



def _persist_students():

    if PRINCIPAL_DEMO_MODE:

        return  # design mode: never touch disk

    _write_json_file(STUDENTS_OVERLAY_FILE, DB['students'])



# Restore persisted state at startup (overlays win when present).

# In demo mode we skip the restore entirely so the fixtures stay pure.

_saved_sr = _load_json_file(SERVICE_REQUESTS_FILE)
if isinstance(_saved_sr, list) and _saved_sr:
    DB['serviceRequests'] = _saved_sr

if not PRINCIPAL_DEMO_MODE:
    _saved_students = _load_json_file(STUDENTS_OVERLAY_FILE)
    if isinstance(_saved_students, list) and _saved_students:
        DB['students'] = _saved_students



def _notify_user(user_id, title, message, ntype='general'):

    """Deliver an in-portal notification to a student or teacher account."""

    if not user_id:

        return

    try:

        nid = max([n.get('id', 0) for n in DB['notifications']] or [0]) + 1

    except Exception:

        nid = len(DB['notifications']) + 1

    DB['notifications'].append({

        'id': nid, 'userId': user_id, 'type': ntype, 'title': title,

        'message': message, 'read': False,

        'date': datetime.now().strftime('%Y-%m-%d')

    })



def _actor_label(user):

    return user.get('name') or (f"{user.get('firstName', '')} {user.get('lastName', '')}").strip() or 'Principal'



def _teacher_name(tid):

    t = next((x for x in DB['teachers'] if x.get('id') == tid), None)

    if t:

        return t.get('name', tid)

    u = next((x for x in AUTH_USERS.values() if x.get('id') == tid), None)

    if u:

        return f"{u.get('firstName', '')} {u.get('lastName', '')}".strip()

    return tid



def _class_name(cid):

    c = next((x for x in DB['classes'] if x.get('id') == cid), None)

    return c.get('name', cid) if c else cid



def _period_name(pid):

    row = ACADEMIC.one('SELECT name FROM grading_periods WHERE id=? OR code=?', (pid, pid))

    return row.get('name', pid) if row else pid



def _last_decision(entity_id):

    row = ACADEMIC.one(

        "SELECT reason, actor_id, details_json, created_at FROM audit_events "

        "WHERE entity_type='approval' AND entity_id=? ORDER BY id DESC LIMIT 1", (entity_id,))

    if not row:

        return {'decidedBy': None, 'decisionNote': '', 'decidedAt': None}

    name = ''

    try:

        name = json.loads(row['details_json'] or '{}').get('actorName', '')

    except Exception:

        pass

    return {'decidedBy': name or row['actor_id'], 'decisionNote': row['reason'], 'decidedAt': row['created_at']}



def _grade_submission_groups(pending_only=True):

    """Live gradebook-release queue straight from the grades workflow table."""

    states = ("'draft','submitted','returned'" if pending_only else "'published'")

    return ACADEMIC.query(f"""

        SELECT a.class_id AS class_id, a.grading_period_id AS period_id,

               COUNT(DISTINCT g.assessment_id) AS assessments,

               COUNT(DISTINCT g.student_id) AS student_count,

               COUNT(*) AS records,

               ROUND(AVG(CASE WHEN a.max_score > 0 THEN 100.0 * g.score / a.max_score END), 1) AS avg_pct,

               SUM(CASE WHEN g.workflow='returned' THEN 1 ELSE 0 END) AS returned_ct,

               MAX(g.updated_at) AS last_update,

               GROUP_CONCAT(DISTINCT a.teacher_id) AS teacher_ids

        FROM grades g JOIN assessments a ON a.id = g.assessment_id

        WHERE g.workflow IN ({states}) AND g.score IS NOT NULL

        GROUP BY a.class_id, a.grading_period_id

        ORDER BY last_update DESC""")



def _transcript_approval_status(t):

    if t.get('verified'):

        return 'approved'

    status = (t.get('status') or '').lower()

    if 'reject' in status:

        return 'rejected'

    if 'return' in status or 'revision' in status:

        return 'needs_correction'

    return 'pending'



def build_principal_queue():

    items = []



    # 1 · Teacher gradebook releases (draft / submitted / returned workflow)

    for grp in _grade_submission_groups():

        key = f"grade:{grp['class_id']}:{grp['period_id']}"

        status = 'needs_correction' if grp['returned_ct'] else 'pending'

        teachers = ', '.join(_teacher_name(t) for t in (grp['teacher_ids'] or '').split(',') if t)

        item = {

            'id': key,

            'type': 'grade_submission',

            'category': 'Gradebook Release',

            'title': f"{_class_name(grp['class_id'])} · {_period_name(grp['period_id'])} gradebook release",

            'submittedBy': teachers or 'Faculty',

            'submittedRole': 'Teacher grade submission',

            'submittedAt': grp['last_update'],

            'scope': f"{grp['student_count']} students · {grp['records']} grade records · {grp['assessments']} assessments",

            'classId': grp['class_id'],

            'periodId': grp['period_id'],

            'details': 'Faculty-recorded grades awaiting executive clearance. Authorizing publishes them to the student and parent portals with recomputed GPA.',

            'diffOld': 'Unpublished (draft / submitted)',

            'diffNew': 'Official published gradebook & certified GPA',

            'status': status,

            'studentCount': grp['student_count'],

            'avgScore': f"{grp['avg_pct']}%" if grp['avg_pct'] is not None else '—',

        }

        item.update(_last_decision(key))

        items.append(item)



    # 2 · Student service requests that need an executive decision

    for r in DB['serviceRequests']:

        if r.get('category') not in ('document', 'academic', 'administration'):

            continue

        st = r.get('status')

        status_map = {'open': 'pending', 'pending': 'pending', 'in_progress': 'needs_correction',

                      'completed': 'approved', 'rejected': 'rejected'}

        if st not in status_map:

            continue

        item = {

            'id': f"request:{r['id']}",

            'type': 'service_request',

            'category': 'Student Request',

            'title': f"{r.get('title', 'Request')} · {r.get('studentName', 'Student')}",

            'submittedBy': r.get('studentName', 'Student'),

            'submittedRole': f"Student · {r.get('studentId', '')}",

            'submittedAt': r.get('date'),

            'scope': f"{r.get('category')} / {r.get('type', 'request')} · priority {r.get('priority', 'normal')}",

            'requestId': r['id'],

            'studentId': r.get('studentId'),

            'details': r.get('description', ''),

            'diffOld': f"Request status: {st}",

            'diffNew': 'Approved & fulfilled by the school office',

            'status': status_map[st],

        }

        # Most recent principal/office comment on the request doubles as the decision trail

        comments = r.get('comments') or []

        executive = next((c for c in reversed(comments) if str(c.get('by', '')).lower().startswith(('principal', 'executive'))), None)

        item['decidedBy'] = executive['by'] if executive else None

        item['decisionNote'] = executive['text'] if executive else ''

        item['decidedAt'] = executive['date'] if executive else None

        items.append(item)



    # 3 · Official transcript certifications (persisted upload records)

    for t in load_transcripts():

        item = {

            'id': f"transcript:{t.get('id')}",

            'type': 'transcript_certification',

            'category': 'Official Document',

            'title': f"Official transcript · {t.get('studentName', t.get('studentId', ''))} ({t.get('term', '')})",

            'submittedBy': t.get('uploadedBy', 'Registrar'),

            'submittedRole': f"Uploaded by {t.get('uploadedByRole', 'faculty')}",

            'submittedAt': t.get('uploadedAt'),

            'scope': f"{t.get('studentId', '')} · {t.get('classGrade', '')} · {t.get('fileName', '')}",

            'studentId': t.get('studentId'),

            'transcriptId': t.get('id'),

            'details': t.get('notes') or 'Uploaded academic transcript awaiting executive certification before release to the student portal.',

            'diffOld': 'Pending executive certification',

            'diffNew': 'Certified & digitally sealed by the Principal',

            'status': _transcript_approval_status(t),

        }

        item.update(_last_decision(item['id']))

        items.append(item)



    items.sort(key=lambda x: (0 if x['status'] == 'pending' else 1 if x['status'] == 'needs_correction' else 2, x.get('submittedAt') or ''), )

    return items



def _approval_counts(items):

    return {

        'total': len(items),

        'pending': sum(1 for i in items if i['status'] == 'pending'),

        'approved': sum(1 for i in items if i['status'] == 'approved'),

        'needs_correction': sum(1 for i in items if i['status'] == 'needs_correction'),

        'rejected': sum(1 for i in items if i['status'] == 'rejected'),

    }



_QUEUE_TYPE_BY_CATEGORY = {'grades': 'grade_submission', 'requests': 'service_request',

                           'transcripts': 'transcript_certification', 'clearance': 'service_request'}



# ════════════════════════════════════════════════════════════════════

# DEMO / DESIGN LAYER — self-contained fixtures for UX review.

# Everything below is pure in-memory sample data. It never touches

# SQLite, disk, or real notification channels. Flip

# PRINCIPAL_DEMO_MODE back to False to hand control to the real layer.

# ════════════════════════════════════════════════════════════════════

def _demo_now():

    return datetime.now().strftime('%Y-%m-%dT%H:%M:%S')



def _demo_label(user):

    return f"Principal · {user.get('name') or 'Design Review'}"



PRINCIPAL_DEMO_STATE = {

    'students': [

        {'id': 'ST-2026-001', 'name': 'Chan Sovann',     'gender': 'Male',   'grade': 'Grade 10', 'class': '10-A', 'status': 'active',   'parentName': 'Chan Dara',    'parentEmail': 'dara.chan@example.kh',  'advisor': 'T-001', 'gpaLive': 3.62, 'attendancePct': 96.4, 'openRequests': 1},

        {'id': 'ST-2026-002', 'name': 'Sok Dara',        'gender': 'Female', 'grade': 'Grade 10', 'class': '10-A', 'status': 'active',   'parentName': 'Sok Vichea',   'parentEmail': 'vichea.sok@example.kh', 'advisor': 'T-001', 'gpaLive': 3.91, 'attendancePct': 98.8, 'openRequests': 0},

        {'id': 'ST-2026-003', 'name': 'Ly Malis',        'gender': 'Female', 'grade': 'Grade 10', 'class': '10-B', 'status': 'active',   'parentName': 'Ly Sopheap',   'parentEmail': 'sopheap.ly@example.kh', 'advisor': 'T-002', 'gpaLive': 3.48, 'attendancePct': 92.1, 'openRequests': 1},

        {'id': 'ST-2026-004', 'name': 'Kim Rith',        'gender': 'Male',   'grade': 'Grade 11', 'class': '11-A', 'status': 'active',   'parentName': 'Kim Bopha',    'parentEmail': 'bopha.kim@example.kh',  'advisor': 'T-003', 'gpaLive': 3.05, 'attendancePct': 87.5, 'openRequests': 0},

        {'id': 'ST-2026-005', 'name': 'Nita Prasidh',    'gender': 'Female', 'grade': 'Grade 11', 'class': '11-A', 'status': 'active',   'parentName': 'Nita Sothy',   'parentEmail': 'sothy.nita@example.kh', 'advisor': 'T-003', 'gpaLive': 3.88, 'attendancePct': 99.2, 'openRequests': 0},

        {'id': 'ST-2026-006', 'name': 'Vichea Hem',      'gender': 'Male',   'grade': 'Grade 11', 'class': '11-B', 'status': 'suspended','parentName': 'Vichea Lida',  'parentEmail': 'lida.hem@example.kh',   'advisor': 'T-004', 'gpaLive': 2.15, 'attendancePct': 68.3, 'openRequests': 1},

        {'id': 'ST-2026-007', 'name': 'Srey Neang',      'gender': 'Female', 'grade': 'Grade 12', 'class': '12-A', 'status': 'active',   'parentName': 'Srey Kanha',   'parentEmail': 'kanha.srey@example.kh', 'advisor': 'T-005', 'gpaLive': 3.76, 'attendancePct': 94.8, 'openRequests': 0},

        {'id': 'ST-2026-008', 'name': 'Thyra Keo',       'gender': 'Female', 'grade': 'Grade 12', 'class': '12-A', 'status': 'active',   'parentName': 'Thyra Sokhon', 'parentEmail': 'sokhon.thyra@example.kh','advisor': 'T-005', 'gpaLive': 3.34, 'attendancePct': 90.2, 'openRequests': 0},

        {'id': 'ST-2026-009', 'name': 'Piseth Nuon',     'gender': 'Male',   'grade': 'Grade 12', 'class': '12-B', 'status': 'active',   'parentName': 'Piseth Chanrath','parentEmail': 'chanrath.nuon@example.kh','advisor': 'T-006', 'gpaLive': 2.92, 'attendancePct': 82.6, 'openRequests': 1},

        {'id': 'ST-2026-010', 'name': 'Bopha Rin',       'gender': 'Female', 'grade': 'Grade 9',  'class': '9-A',  'status': 'active',   'parentName': 'Bopha Vann',   'parentEmail': 'vann.bopha@example.kh', 'advisor': 'T-002', 'gpaLive': 3.55, 'attendancePct': 95.0, 'openRequests': 0},

        {'id': 'ST-2026-011', 'name': 'Rathanak Sam',    'gender': 'Male',   'grade': 'Grade 9',  'class': '9-A',  'status': 'active',   'parentName': 'Rathanak Srey','parentEmail': 'srey.rathanak@example.kh','advisor': 'T-002', 'gpaLive': 2.68, 'attendancePct': 78.4, 'openRequests': 0},

        {'id': 'ST-2026-012', 'name': 'Chandavy Truong', 'gender': 'Female', 'grade': 'Grade 9',  'class': '9-B',  'status': 'graduated','parentName': 'Chandavy Piseth','parentEmail': 'piseth.chandavy@example.kh','advisor': 'T-004', 'gpaLive': 3.94, 'attendancePct': 97.9, 'openRequests': 0},

        {'id': 'ST-2026-013', 'name': 'Sokuntheary Meas','gender': 'Female', 'grade': 'Grade 12', 'class': '12-B', 'status': 'active',   'parentName': 'Sokun Meas',   'parentEmail': 'meas.sokun@example.kh', 'advisor': 'T-006', 'gpaLive': 3.21, 'attendancePct': 88.9, 'openRequests': 1},

        {'id': 'ST-2026-014', 'name': 'Dara Phon',       'gender': 'Male',   'grade': 'Grade 10', 'class': '10-B', 'status': 'active',   'parentName': 'Dara Raksmey', 'parentEmail': 'raksmey.phon@example.kh','advisor': 'T-001', 'gpaLive': 3.12, 'attendancePct': 91.3, 'openRequests': 0},

        {'id': 'ST-2026-015', 'name': 'Kanitha Yim',     'gender': 'Female', 'grade': 'Grade 11', 'class': '11-B', 'status': 'active',   'parentName': 'Kanitha Sova', 'parentEmail': 'sova.kanitha@example.kh','advisor': 'T-003', 'gpaLive': 3.69, 'attendancePct': 93.7, 'openRequests': 0},

    ],

    'teachers': [

        {'id': 'T-001', 'name': 'Sophea Kuon',   'subject': 'Mathematics',       'department': 'STEM',       'email': 'sophea.k@ngis.edu.kh',  'status': 'active',   'classesAssigned': 3, 'yearsAtSchool': 6},

        {'id': 'T-002', 'name': 'Bopha Chey',    'subject': 'Physics',           'department': 'STEM',       'email': 'bopha.c@ngis.edu.kh',   'status': 'active',   'classesAssigned': 2, 'yearsAtSchool': 4},

        {'id': 'T-003', 'name': 'Rithy Sem',     'subject': 'English Literature','department': 'Humanities', 'email': 'rithy.s@ngis.edu.kh',   'status': 'active',   'classesAssigned': 4, 'yearsAtSchool': 9},

        {'id': 'T-004', 'name': 'Kanha Prum',    'subject': 'History',           'department': 'Humanities', 'email': 'kanha.p@ngis.edu.kh',   'status': 'on-leave', 'classesAssigned': 2, 'yearsAtSchool': 3},

        {'id': 'T-005', 'name': 'Srey Leak Huon','subject': 'Biology',           'department': 'STEM',       'email': 'sreyleak.h@ngis.edu.kh','status': 'active',   'classesAssigned': 3, 'yearsAtSchool': 7},

        {'id': 'T-006', 'name': 'Vichea Tong',   'subject': 'Computer Science',  'department': 'STEM',       'email': 'vichea.t@ngis.edu.kh',  'status': 'active',   'classesAssigned': 2, 'yearsAtSchool': 2},

    ],

    'transcripts': [

        {'id': 'TR-9001', 'studentId': 'ST-2026-002', 'studentName': 'Sok Dara',        'term': 'Semester 1 · AY 2025-26', 'gpa': 3.91, 'uploadedBy': 'Registrar Desk',  'uploadedByRole': 'faculty',  'date': '2026-06-28', 'status': 'Awaiting Principal Certification', 'verified': False, 'fileUrl': '/files/transcripts/TR-9001.pdf'},

        {'id': 'TR-9002', 'studentId': 'ST-2026-005', 'studentName': 'Nita Prasidh',    'term': 'Semester 1 · AY 2025-26', 'gpa': 3.88, 'uploadedBy': 'Registrar Desk',  'uploadedByRole': 'faculty',  'date': '2026-06-27', 'status': 'Awaiting Principal Certification', 'verified': False, 'fileUrl': '/files/transcripts/TR-9002.pdf'},

        {'id': 'TR-9003', 'studentId': 'ST-2026-007', 'studentName': 'Srey Neang',      'term': 'Semester 1 · AY 2025-26', 'gpa': 3.76, 'uploadedBy': 'Vice Principal','uploadedByRole': 'admin',    'date': '2026-06-25', 'status': 'Awaiting Principal Certification', 'verified': False, 'fileUrl': '/files/transcripts/TR-9003.pdf'},

        {'id': 'TR-9004', 'studentId': 'ST-2026-012', 'studentName': 'Chandavy Truong', 'term': 'Full Programme · AY 2023-26', 'gpa': 3.94, 'uploadedBy': 'Registrar Desk','uploadedByRole': 'faculty', 'date': '2026-06-20', 'status': 'Certified & Released',             'verified': True,  'certifiedBy': 'Principal · Dr. Ly Bunheng', 'certifiedAt': '2026-06-22T09:14:00', 'fileUrl': '/files/transcripts/TR-9004.pdf'},

        {'id': 'TR-9005', 'studentId': 'ST-2026-013', 'studentName': 'Sokuntheary Meas','term': 'Semester 1 · AY 2025-26', 'gpa': 3.21, 'uploadedBy': 'Registrar Desk',  'uploadedByRole': 'faculty',  'date': '2026-06-18', 'status': 'Returned for Revision',              'verified': False, 'decisionNote': 'Missing grade for Physical Education module.', 'fileUrl': '/files/transcripts/TR-9005.pdf'},

        {'id': 'TR-9006', 'studentId': 'ST-2026-009', 'studentName': 'Piseth Nuon',     'term': 'Semester 1 · AY 2025-26', 'gpa': 2.92, 'uploadedBy': 'Homeroom 12-B',   'uploadedByRole': 'faculty',  'date': '2026-06-15', 'status': 'Rejected',                         'verified': False, 'decisionNote': 'Signed consent form not attached to the request.', 'fileUrl': '/files/transcripts/TR-9006.pdf'},

    ],

    'serviceRequests': [

        {'id': 'SR-501', 'studentId': 'ST-2026-001', 'studentName': 'Chan Sovann',     'category': 'document',    'type': 'Official Transcript Copy',   'title': 'Request official transcript for university application', 'description': 'Need 3 certified hardcopies before 15 July for scholarship submission.', 'priority': 'high',   'status': 'pending',     'date': '2026-06-30', 'updatedAt': '2026-06-30', 'comments': []},

        {'id': 'SR-502', 'studentId': 'ST-2026-003', 'studentName': 'Ly Malis',        'category': 'clearance',   'type': 'Activity Clearance',         'title': 'Sports club clearance – end of year',                   'description': 'Robotics club coach sign-off pending.',                                'priority': 'normal', 'status': 'pending',     'date': '2026-06-29', 'updatedAt': '2026-06-29', 'comments': []},

        {'id': 'SR-503', 'studentId': 'ST-2026-006', 'studentName': 'Vichea Hem',      'category': 'discipline',  'type': 'Appeal',                     'title': 'Appeal suspension decision',                            'description': 'Parent requests meeting to review attendance incident.',              'priority': 'high',   'status': 'in_progress', 'date': '2026-06-27', 'updatedAt': '2026-06-30', 'comments': [{'by': 'Principal · Dean of Discipline', 'text': 'Meeting scheduled with parent for 04 July.', 'date': '2026-06-30'}]},

        {'id': 'SR-504', 'studentId': 'ST-2026-009', 'studentName': 'Piseth Nuon',     'category': 'document',    'type': 'Character Certificate',      'title': 'Request character certificate for internship',            'description': 'Needed for hotel management internship on 20 July.',                  'priority': 'normal', 'status': 'pending',     'date': '2026-06-26', 'updatedAt': '2026-06-26', 'comments': []},

        {'id': 'SR-505', 'studentId': 'ST-2026-011', 'studentName': 'Rathanak Sam',    'category': 'counseling',  'type': 'Counseling Session',         'title': 'Request counseling for exam anxiety',                     'description': 'Student self-referral through homeroom teacher.',                     'priority': 'high',   'status': 'in_progress', 'date': '2026-06-25', 'updatedAt': '2026-06-28', 'comments': [{'by': 'Counselor', 'text': 'Initial intake completed, follow-up booked.', 'date': '2026-06-28'}]},

        {'id': 'SR-506', 'studentId': 'ST-2026-013', 'studentName': 'Sokuntheary Meas','category': 'records',     'type': 'Record Correction',          'title': 'Correct date of birth on enrolment form',                 'description': 'Family book shows 12 Feb 2008, portal shows 12 Jan 2008.',           'priority': 'normal', 'status': 'pending',     'date': '2026-06-24', 'updatedAt': '2026-06-24', 'comments': []},

        {'id': 'SR-507', 'studentId': 'ST-2026-015', 'studentName': 'Kanitha Yim',     'category': 'document',    'type': 'Transfer Letter',            'title': 'Transfer letter to Provincial School',                    'description': 'Family relocation before Term 3 start.',                                'priority': 'urgent', 'status': 'pending',     'date': '2026-06-22', 'updatedAt': '2026-06-22', 'comments': []},

        {'id': 'SR-508', 'studentId': 'ST-2026-002', 'studentName': 'Sok Dara',        'category': 'lost_found',  'type': 'Lost Item Report',           'title': 'Lost water bottle in Science Block',                      'description': 'Blue Hydro flask left in Lab 2 during lunch.',                          'priority': 'low',    'status': 'open',        'date': '2026-06-20', 'updatedAt': '2026-06-20', 'comments': []},

    ],

    'gradebookGroups': [

        {'id': 'grade:cls-10a:gp-q1', 'type': 'grade_submission', 'category': 'Grade Submission',

         'title': 'Grade 10-A · Term 1 Gradebook',                 'submittedBy': 'Sophea Kuon (T-001)', 'submittedRole': 'teacher',

         'submittedAt': '2026-06-28T10:12:00', 'scope': '32 records · Math, Physics, Chemistry',

         'classId': 'cls-10a', 'periodId': 'gp-q1', 'teacherIds': 'T-001',

         'details': 'All summative assessments entered. Awaiting executive authorization.',

         'diffOld': 'Gradebook status: submitted (locked)', 'diffNew': 'Gradebook status: published to student portals',

         'status': 'pending', 'decidedBy': None, 'decisionNote': '', 'decidedAt': None},

        {'id': 'grade:cls-11a:gp-q1', 'type': 'grade_submission', 'category': 'Grade Submission',

         'title': 'Grade 11-A · Term 1 Gradebook',                 'submittedBy': 'Rithy Sem (T-003)', 'submittedRole': 'teacher',

         'submittedAt': '2026-06-27T14:05:00', 'scope': '28 records · English Literature, History',

         'classId': 'cls-11a', 'periodId': 'gp-q1', 'teacherIds': 'T-003',

         'details': 'Two students have provisional marks pending retest results.',

         'diffOld': 'Gradebook status: submitted (locked)', 'diffNew': 'Gradebook status: published to student portals',

         'status': 'pending', 'decidedBy': None, 'decisionNote': '', 'decidedAt': None},

        {'id': 'grade:cls-12b:gp-q1', 'type': 'grade_submission', 'category': 'Grade Submission',

         'title': 'Grade 12-B · Term 1 Gradebook',                 'submittedBy': 'Vichea Tong (T-006)', 'submittedRole': 'teacher',

         'submittedAt': '2026-06-20T09:30:00', 'scope': '24 records · Computer Science',

         'classId': 'cls-12b', 'periodId': 'gp-q1', 'teacherIds': 'T-006',

         'details': 'Grading rubric updated mid-term, three outliers require Principal review.',

         'diffOld': 'Gradebook status: submitted (locked)', 'diffNew': 'Gradebook status: returned for revision',

         'status': 'needs_correction', 'decidedBy': 'Principal · Dr. Ly Bunheng', 'decisionNote': 'Please re-check outliers for Piseth Nuon and Sokuntheary Meas before publishing.', 'decidedAt': '2026-06-22T16:20:00'},

        {'id': 'grade:cls-9a:gp-q1',  'type': 'grade_submission', 'category': 'Grade Submission',

         'title': 'Grade 9-A · Term 1 Gradebook',                  'submittedBy': 'Bopha Chey (T-002)', 'submittedRole': 'teacher',

         'submittedAt': '2026-06-18T11:00:00', 'scope': '30 records · Physics foundations',

         'classId': 'cls-9a',  'periodId': 'gp-q1', 'teacherIds': 'T-002',

         'details': 'Standard first-term submission.',

         'diffOld': 'Gradebook status: submitted (locked)', 'diffNew': 'Gradebook status: published to student portals',

         'status': 'approved', 'decidedBy': 'Principal · Dr. Ly Bunheng', 'decisionNote': 'Authorized.', 'decidedAt': '2026-06-19T09:00:00'},

    ],

    'auditEvents': [

        {'id': 9007, 'created_at': '2026-06-30T15:40:00', 'actor_id': 'U-PRN-01', 'actor_role': 'principal', 'action': 'PRINCIPAL_STUDENT_RECORD_EDIT',    'entity_type': 'student',   'entity_id': 'ST-2026-003', 'reason': 'Legal name spelling corrected on registrar hardcopy.', 'metadata_json': '{"actorName":"Principal · Dr. Ly Bunheng","changes":{"name":"Ly Malis"},"previous":{"name":"Ly Mallis"}}'},

        {'id': 9006, 'created_at': '2026-06-29T11:10:00', 'actor_id': 'U-PRN-01', 'actor_role': 'principal', 'action': 'PRINCIPAL_TRANSCRIPT_DECISION',    'entity_type': 'approval',  'entity_id': 'transcript:TR-9005', 'reason': 'Missing PE module — returned to registrar.',    'metadata_json': '{"actorName":"Principal · Dr. Ly Bunheng","resultStatus":"Returned for Revision"}'},

        {'id': 9005, 'created_at': '2026-06-28T08:52:00', 'actor_id': 'U-PRN-01', 'actor_role': 'principal', 'action': 'PRINCIPAL_BATCH_APPROVE',          'entity_type': 'approval',  'entity_id': 'all-pending',        'reason': 'Weekly executive sign-off session.',              'metadata_json': '{"actorName":"Principal · Dr. Ly Bunheng","count":2}'},

        {'id': 9004, 'created_at': '2026-06-27T13:20:00', 'actor_id': 'T-001',    'actor_role': 'teacher',   'action': 'GRADEBOOK_SUBMITTED',              'entity_type': 'gradebook', 'entity_id': 'grade:cls-10a:gp-q1','reason': 'Term 1 gradebook finalized for review.',    'metadata_json': '{"actorName":"Sophea Kuon","records":32}'},

        {'id': 9003, 'created_at': '2026-06-25T10:05:00', 'actor_id': 'U-ADM-02', 'actor_role': 'admin',     'action': 'STUDENT_ENROLMENT_UPDATED',        'entity_type': 'student',   'entity_id': 'ST-2026-011', 'reason': 'Emergency contact refreshed after parent call.',  'metadata_json': '{"actorName":"Registrar Admin"}'},

        {'id': 9002, 'created_at': '2026-06-22T16:20:00', 'actor_id': 'U-PRN-01', 'actor_role': 'principal', 'action': 'PRINCIPAL_PUBLISH_GRADES',         'entity_type': 'approval',  'entity_id': 'grade:cls-9a:gp-q1', 'reason': 'Authorized 9-A gradebook.',                   'metadata_json': '{"actorName":"Principal · Dr. Ly Bunheng"}'},

        {'id': 9001, 'created_at': '2026-06-20T09:15:00', 'actor_id': 'U-PRN-01', 'actor_role': 'principal', 'action': 'PRINCIPAL_REQUEST_DECISION',       'entity_type': 'approval',  'entity_id': 'request:SR-503',   'reason': 'Escalated to dean of discipline for investigation.','metadata_json': '{"actorName":"Principal · Dr. Ly Bunheng","resultStatus":"in_progress"}'},

    ],

    '_nextAuditId':  9008,

    'gradeOverrides': {},

}



def _demo_audit(user, action, entity_type, entity_id, reason, extra=None):

    md = {'actorName': _demo_label(user)}

    if extra:

        md.update(extra)

    event = {

        'id': PRINCIPAL_DEMO_STATE['_nextAuditId'],

        'created_at': _demo_now(),

        'actor_id': user.get('id') or 'U-PRN-01',

        'actor_role': user.get('role') or 'principal',

        'action': action,

        'entity_type': entity_type,

        'entity_id': entity_id,

        'reason': reason,

        'metadata_json': json.dumps(md),

    }

    PRINCIPAL_DEMO_STATE['_nextAuditId'] += 1

    PRINCIPAL_DEMO_STATE['auditEvents'].insert(0, event)

    return event



def _demo_filter_queue(status=None, category=None):

    items = list(PRINCIPAL_DEMO_STATE['gradebookGroups'])

    for r in PRINCIPAL_DEMO_STATE['serviceRequests']:

        items.append({

            'id': f"request:{r['id']}",

            'type': 'service_request',

            'category': 'Service Request',

            'title': r.get('title', 'Service request'),

            'submittedBy': r.get('studentName', r.get('studentId', '')),

            'submittedRole': 'student',

            'submittedAt': r.get('date'),

            'scope': f"{r.get('category')} / {r.get('type', 'request')} · priority {r.get('priority', 'normal')}",

            'requestId': r['id'],

            'studentId': r.get('studentId'),

            'details': r.get('description', ''),

            'diffOld': f"Request status: {r.get('status')}",

            'diffNew': 'Approved & fulfilled by the school office',

            'status': {'pending': 'pending', 'open': 'pending', 'in_progress': 'needs_correction',

                       'completed': 'approved', 'approved': 'approved', 'rejected': 'rejected'}.get(r.get('status'), 'pending'),

            'decidedBy': None, 'decisionNote': '', 'decidedAt': None,

        })

    for t in PRINCIPAL_DEMO_STATE['transcripts']:

        items.append({

            'id': f"transcript:{t['id']}",

            'type': 'transcript_certification',

            'category': 'Official Document',

            'title': f"Official transcript · {t.get('studentName', t.get('studentId', ''))} ({t.get('term', '')})",

            'submittedBy': t.get('uploadedBy', 'Registrar'),

            'submittedRole': f"Uploaded by {t.get('uploadedByRole', 'faculty')}",

            'submittedAt': t.get('date'),

            'scope': f"GPA {t.get('gpa', '—')} · {t.get('term', '')}",

            'transcriptId': t['id'],

            'studentId': t.get('studentId'),

            'details': 'Registrar-prepared transcript awaiting executive certification.',

            'diffOld': f"Document status: {t.get('status')}",

            'diffNew': 'Certified & Released · signed by Principal',

            'status': 'approved' if t.get('verified') else ({

                'Returned for Revision': 'needs_correction',

                'Rejected': 'rejected',

            }.get(t.get('status'), 'pending')),

            'decidedBy': t.get('certifiedBy') if t.get('verified') else None,

            'decisionNote': t.get('decisionNote', ''),

            'decidedAt': t.get('certifiedAt'),

        })

    order = {'pending': 0, 'needs_correction': 1, 'approved': 2, 'rejected': 3}

    items.sort(key=lambda x: (order.get(x.get('status'), 4), x.get('submittedAt') or ''))

    if status and status != 'all':

        items = [i for i in items if i.get('status') == status]

    if category and category != 'all':

        wanted = _QUEUE_TYPE_BY_CATEGORY.get(category)

        if wanted:

            items = [i for i in items if i.get('type') == wanted]

    return items



def _demo_counts():

    everything = _demo_filter_queue()

    return _approval_counts(everything)



def _demo_grade_band(score):

    if score >= 90: return 'A'

    if score >= 85: return 'B+'

    if score >= 80: return 'B'

    if score >= 75: return 'C+'

    if score >= 70: return 'C'

    if score >= 60: return 'D'

    return 'F'



def _demo_grades_for(student_id):

    student = next((s for s in PRINCIPAL_DEMO_STATE['students'] if s['id'] == student_id), None)

    if not student:

        return []

    gpa = student.get('gpaLive') or 3.0

    base = int(66 + (gpa / 4.0) * 28)

    subjects = ['Mathematics', 'Physics', 'English Literature', 'History', 'Biology', 'Computer Science']

    overrides = PRINCIPAL_DEMO_STATE.get('gradeOverrides', {})

    rows = []

    for idx, subj in enumerate(subjects):

        gid = f"{student_id}-g{idx+1}"

        pct = max(52, min(99, base + (idx * 2 - 5)))

        pct = overrides.get(gid, pct)

        rows.append({

            'id': gid,

            'studentId': student_id,

            'assessmentTitle': f"{subj} · Semester 1 Exam",

            'subject_name': subj,

            'score': round(pct * 1.0),

            'maxScore': 100,

            'percentage': pct,

            'letterGrade': _demo_grade_band(pct),

            'workflow': 'published' if idx % 3 else 'submitted',

            'teacher': PRINCIPAL_DEMO_STATE['teachers'][idx % len(PRINCIPAL_DEMO_STATE['teachers'])]['name'],

        })

    return rows



def _demo_attendance_for(student_id, limit=8):

    student = next((s for s in PRINCIPAL_DEMO_STATE['students'] if s['id'] == student_id), None)

    pct = (student or {}).get('attendancePct', 90)

    courses = ['Mathematics', 'Physics', 'English Literature', 'Chemistry', 'History']

    dates = ['2026-07-06', '2026-07-05', '2026-07-04', '2026-07-03', '2026-07-02',

             '2026-07-01', '2026-06-30', '2026-06-29', '2026-06-26', '2026-06-25']

    records = []

    for idx, d in enumerate(dates[:max(1, min(limit, len(dates)))]):

        if pct >= 95:

            status = 'present'

        elif pct >= 85:

            status = 'present' if idx % 4 else 'tardy'

        elif pct >= 75:

            status = 'present' if idx % 3 else ('tardy' if idx % 2 else 'absent')

        else:

            status = 'absent' if idx % 2 else 'present'

        records.append({'attendance_date': d, 'status': status, 'course': courses[idx % len(courses)]})

    return {'studentId': student_id, 'records': records, 'summary': {'percentage': pct}}



def _demo_avatar(name):

    from urllib.parse import quote as _q

    return 'https://api.dicebear.com/9.x/initials/svg?seed=' + _q(name or 'NG') + '&backgroundColor=202F63,92243D&fontSize=42&textColor=ffffff'



_DEMO_DISTRICTS = ['Chamkar Mon', 'Toul Kork', 'Bkk. Kandal', 'Dun Penh', 'Mean Chey', 'Chbar Ampov']

_DEMO_OCCUPATIONS = ['Engineer', 'Healthcare Worker', 'Small Business Owner', 'Civil Servant',

                     'Banker', 'Teacher', 'Logistics Manager', 'Software Developer']

_DEMO_RELATIONS = ['Mother', 'Father', 'Guardian']



def _demo_teacher_profile(t):

    tid = t.get('id')

    advised = sorted({s.get('class') for s in PRINCIPAL_DEMO_STATE['students']

                      if s.get('advisor') == tid and s.get('class')})

    homerooms = advised[:1]

    return {

        **t,

        'subjects': [t.get('subject')],

        'classesTaught': advised or ['—'],

        'homeroom': homerooms[0] if homerooms else '—',

        'adviseeCount': len([s for s in PRINCIPAL_DEMO_STATE['students'] if s.get('advisor') == tid]),

        'phone': '+855 9%d %d %d' % (int(tid[-1]) or 1, 200 + int(tid[-1] or 0) * 7, 3000 + int(tid[-1] or 0) * 111),

        'employmentType': 'Full-time',

        'contractEnd': '2027-08-31',

        'certifications': ['Ministry Teaching Licence', 'Safeguarding Level 2'],

        'languages': ['Khmer', 'English'],

        'avatarUrl': _demo_avatar(t.get('name')),

    }



def _demo_guardian_profiles():

    """Derive one parent/guardian profile per enrolled student from the

    roster's parentName / parentEmail fields, enriched with demo contact

    details so the Roster & Profiles design has real-looking records."""

    out = []

    for idx, s in enumerate(PRINCIPAL_DEMO_STATE['students']):

        pid = 'PG-' + str(s['id'])[-3:]

        tail = int(str(s['id'])[-3:])

        name = s.get('parentName') or ('Guardian ' + str(s['id'])[-3:])

        out.append({

            'id': pid,

            'name': name,

            'relation': _DEMO_RELATIONS[idx % len(_DEMO_RELATIONS)],

            'email': s.get('parentEmail') or '',

            'phone': '+855 12 %d %d' % (230 + tail, 4000 + tail * 13),

            'occupation': _DEMO_OCCUPATIONS[idx % len(_DEMO_OCCUPATIONS)],

            'district': _DEMO_DISTRICTS[idx % len(_DEMO_DISTRICTS)],

            'preferredLanguage': 'Khmer' if idx % 3 else 'English',

            'avatarUrl': _demo_avatar(name),

            'consentOnFile': tail % 5 != 0,

            'meetingsAttended': (tail % 4) + 1,

            'lastContact': '2026-%02d-%02d' % (6 - (idx % 4), 5 + (tail % 20)),

            'linkedStudents': [{'id': s['id'], 'name': s.get('name'),

                                'class': s.get('class'), 'grade': s.get('grade'),

                                'status': s.get('status'), 'gpa': s.get('gpaLive'),

                                'attendancePct': s.get('attendancePct')}],

        })

    return out



def _demo_event_out(ev):

    """Audit rows expose both metadata_json (real schema) and details_json

    (what the Management Action Log renders) so the design is stable when

    the layer is later reconnected to SQLite."""

    out = dict(ev)

    if 'details_json' not in out:

        out['details_json'] = out.get('metadata_json', '{}')

    if 'metadata_json' not in out:

        out['metadata_json'] = out.get('details_json', '{}')

    return out



def _demo_sync_student_rollups():

    for s in PRINCIPAL_DEMO_STATE['students']:

        s['openRequests'] = len([r for r in PRINCIPAL_DEMO_STATE['serviceRequests']

                                 if r.get('studentId') == s['id']

                                 and r.get('status') in ('open', 'pending', 'in_progress')])



def _demo_approve_item(user, item_id, action, note, now_iso):

    prefix, _, rest = item_id.partition(':')

    if prefix == 'grade':

        parts = rest.split(':')

        grp = next((g for g in PRINCIPAL_DEMO_STATE['gradebookGroups']

                    if len(parts) == 2 and g['classId'] == parts[0] and g['periodId'] == parts[1]), None)

        if not grp:

            return None

        grp['status'] = 'approved' if action == 'approve' else 'needs_correction'

        grp['decidedBy'] = _demo_label(user)

        grp['decisionNote'] = note or ('Authorized by Principal.' if action == 'approve' else 'Return for revision.')

        grp['decidedAt'] = now_iso

        _demo_audit(user, 'PRINCIPAL_PUBLISH_GRADES' if action == 'approve' else 'PRINCIPAL_RETURN_CORRECTION',

                    'approval', item_id, note or f'{action.title()} by {_demo_label(user)}',

                    {'classId': grp['classId'], 'periodId': grp['periodId']})

        return grp

    if prefix == 'request':

        req = next((r for r in PRINCIPAL_DEMO_STATE['serviceRequests'] if r['id'] == rest), None)

        if not req:

            return None

        req['status'] = {'approve': 'completed', 'reject': 'rejected'}.get(action, 'in_progress')

        req['updatedAt'] = now_iso[:10]

        req.setdefault('comments', []).append({'by': _demo_label(user), 'text': note or f'Executive decision: {action}', 'date': req['updatedAt']})

        _demo_audit(user, 'PRINCIPAL_REQUEST_DECISION', 'approval', item_id,

                    note or action, {'requestId': rest, 'resultStatus': req['status']})

        return req

    if prefix == 'transcript':

        tr = next((t for t in PRINCIPAL_DEMO_STATE['transcripts'] if t['id'] == rest), None)

        if not tr:

            return None

        if action == 'approve':

            tr['verified'] = True

            tr['status'] = 'Certified & Released'

            tr['certifiedBy'] = _demo_label(user)

            tr['certifiedAt'] = now_iso

        elif action == 'reject':

            tr['verified'] = False

            tr['status'] = 'Rejected'

        else:

            tr['verified'] = False

            tr['status'] = 'Returned for Revision'

        tr['decisionNote'] = note

        _demo_audit(user, 'PRINCIPAL_TRANSCRIPT_DECISION', 'approval', item_id,

                    note or action, {'transcriptId': rest, 'studentId': tr.get('studentId'),

                                     'resultStatus': tr['status']})

        return tr

    return None



def _demo_stats_payload(user):

    _demo_sync_student_rollups()

    counts = _demo_counts()

    students = PRINCIPAL_DEMO_STATE['students']

    att_vals = [s['attendancePct'] for s in students if isinstance(s.get('attendancePct'), (int, float))]

    gpa_vals = [s['gpaLive'] for s in students if isinstance(s.get('gpaLive'), (int, float)) and s['gpaLive'] > 0]

    attendance_rate = round(sum(att_vals) / len(att_vals), 1) if att_vals else None

    avg_gpa = round(sum(gpa_vals) / len(gpa_vals), 2) if gpa_vals else None

    published = sum(len(g.get('details', '').split('·')[0].split()) for g in PRINCIPAL_DEMO_STATE['gradebookGroups'] if g['status'] == 'approved')

    draft = sum(1 for g in PRINCIPAL_DEMO_STATE['gradebookGroups'] if g['status'] in ('pending', 'needs_correction'))

    return {

        'mode': 'demo',

        'totalStudents': len(students),

        'totalTeachers': len(PRINCIPAL_DEMO_STATE['teachers']),

        'totalClasses': len({s.get('class') for s in students if s.get('class')}),

        'activeServiceRequests': len([r for r in PRINCIPAL_DEMO_STATE['serviceRequests']

                                      if r.get('status') in ('open', 'pending', 'in_progress')]),

        'pendingApprovals': counts['pending'],

        'needsCorrection': counts['needs_correction'],

        'publishedGradeRecords': draft * 8 + published,

        'draftGradeRecords': draft,

        'attendanceRate': attendance_rate,

        'averageGpa': avg_gpa,

        'honorsRate': round(sum(1 for v in gpa_vals if v >= 3.5) / len(gpa_vals) * 100, 1) if gpa_vals else None,

        'publishedGrades': draft * 8 + published,

        'recentActions': [_demo_event_out(e) for e in PRINCIPAL_DEMO_STATE['auditEvents'][:6]],

        'approvalBreakdown': counts,

    }



# ════════════════════════════════════════════════════════════════════

# PRINCIPAL APPROVAL QUEUE ROUTES

# ════════════════════════════════════════════════════════════════════



@app.route('/api/principal/approvals', methods=['GET'])

def get_principal_approvals():

    user, error = _academic_require(('principal', 'admin'))

    if error: return error

    if PRINCIPAL_DEMO_MODE:

        items = _demo_filter_queue(

            status=(request.args.get('status') or 'all').lower(),

            category=(request.args.get('category') or 'all').lower(),

        )

        return jsonify({'status': 'success', 'mode': 'demo', 'counts': _demo_counts(), 'data': items})



    items = build_principal_queue()

    all_counts = _approval_counts(items)



    status_filter = (request.args.get('status') or 'all').lower()

    category_filter = (request.args.get('category') or 'all').lower()

    if category_filter not in ('all', 'grades', 'requests', 'transcripts', 'clearance'):

        category_filter = 'all'

    if category_filter != 'all':

        items = [i for i in items if i['type'] == _QUEUE_TYPE_BY_CATEGORY[category_filter]]

    if status_filter != 'all':

        items = [i for i in items if i['status'] == status_filter]



    return jsonify({'status': 'success', 'counts': all_counts, 'data': items})



@app.route('/api/principal/approvals/<item_id>/action', methods=['POST'])

def handle_principal_approval_action(item_id):

    user, error = _academic_require(('principal', 'admin'))

    if error: return error

    if PRINCIPAL_DEMO_MODE:

        data = request.get_json(silent=True) or {}

        action = (data.get('action') or '').lower()

        note = (data.get('note') or '').strip()

        if action not in ('approve', 'reject', 'return', 'needs_correction'):

            return _academic_error('INVALID_ACTION', 'Action must be approve, reject, or needs_correction')

        if action in ('reject', 'needs_correction', 'return') and not note:

            return _academic_error('REASON_REQUIRED', 'A written reason is required when rejecting or returning a submission')

        updated = _demo_approve_item(user, item_id, action, note, _demo_now())

        if updated is None:

            return _academic_error('NOT_FOUND', 'Demo approval item not found', 404)

        _demo_sync_student_rollups()

        return jsonify({'status': 'success', 'mode': 'demo',

                        'message': f'Demo approval {item_id} processed ({action})',

                        'counts': _demo_counts(), 'item': updated})



    data = request.get_json(silent=True) or {}

    action = (data.get('action') or '').lower()

    note = (data.get('note') or '').strip()

    if action not in ('approve', 'reject', 'return', 'needs_correction'):

        return _academic_error('INVALID_ACTION', 'Action must be approve, reject, or needs_correction')

    if action in ('reject', 'needs_correction', 'return') and not note:

        return _academic_error('REASON_REQUIRED', 'A written reason is required when rejecting or returning a submission')



    actor_name = _actor_label(user)

    now_iso = ACADEMIC.now()

    prefix, _, rest = item_id.partition(':')



    if prefix == 'grade':

        parts = rest.split(':')

        if len(parts) != 2:

            return _academic_error('NOT_FOUND', 'Malformed gradebook approval id', 404)

        class_id, period_id = parts

        existing = next((g for g in _grade_submission_groups() if g['class_id'] == class_id and g['period_id'] == period_id), None)

        if not existing:

            return _academic_error('NOT_FOUND', 'No pending gradebook group matches this approval', 404)

        teachers = [t for t in (existing['teacher_ids'] or '').split(',') if t]

        new_state = 'published' if action == 'approve' else 'returned'

        ACADEMIC.execute(

            """UPDATE grades SET workflow=?, updated_at=? WHERE score IS NOT NULL AND workflow IN ('draft','submitted','returned')

               AND assessment_id IN (SELECT id FROM assessments WHERE class_id=? AND grading_period_id=?)""",

            (new_state, now_iso, class_id, period_id))

        ACADEMIC.audit(user['id'], user['role'],

                       'PRINCIPAL_PUBLISH_GRADES' if action == 'approve' else 'PRINCIPAL_RETURN_CORRECTION',

                       'approval', item_id, note or f'{action.title()} by {actor_name}',

                       {'actorName': actor_name, 'classId': class_id, 'periodId': period_id})

        for tid in teachers:

            _notify_user(tid, 'Gradebook decision',

                         f"{_class_name(class_id)} ({_period_name(period_id)}): " +

                         ('grades were authorized and published to student portals.' if action == 'approve'

                          else f'grades were returned for revision. Note: {note}'), 'grade')

        for st in ACADEMIC.query("SELECT DISTINCT student_id FROM grades WHERE workflow=? AND assessment_id IN (SELECT id FROM assessments WHERE class_id=? AND grading_period_id=?)",

                                 (new_state, class_id, period_id)):

            _notify_user(st['student_id'], 'Grades updated',

                         f"Your {_class_name(class_id)} results for {_period_name(period_id)} were " +

                         ('published by the Principal.' if action == 'approve' else 'returned by faculty for review.'), 'grade')



    elif prefix == 'request':

        sr_id = rest

        req = next((r for r in DB['serviceRequests'] if r['id'] == sr_id), None)

        if not req:

            return _academic_error('NOT_FOUND', 'Service request not found', 404)

        req['status'] = {'approve': 'completed', 'reject': 'rejected'}.get(action, 'in_progress')

        req['updatedAt'] = datetime.now().strftime('%Y-%m-%d')

        req.setdefault('comments', []).append({'by': f'Principal · {actor_name}', 'text': note or f'Executive decision: {action}', 'date': req['updatedAt']})

        _persist_service_requests()

        ACADEMIC.audit(user['id'], user['role'], 'PRINCIPAL_REQUEST_DECISION', 'approval', item_id,

                       note or action, {'actorName': actor_name, 'requestId': sr_id, 'resultStatus': req['status']})

        _notify_user(req.get('studentId'), 'Service request update',

                     f"“{req.get('title', 'Request')}” is now: {req['status']}. " + (note or ''), 'general')



    elif prefix == 'transcript':

        tr_id = rest

        transcripts = load_transcripts()

        target = next((t for t in transcripts if t.get('id') == tr_id), None)

        if not target:

            return _academic_error('NOT_FOUND', 'Transcript record not found', 404)

        if action == 'approve':

            target['verified'] = True

            target['status'] = 'Certified & Released'

            target['certifiedBy'] = actor_name

            target['certifiedAt'] = now_iso

        elif action == 'reject':

            target['verified'] = False

            target['status'] = 'Rejected'

        else:

            target['verified'] = False

            target['status'] = 'Returned for Revision'

        target['decisionNote'] = note

        save_transcripts(transcripts)

        ACADEMIC.audit(user['id'], user['role'], 'PRINCIPAL_TRANSCRIPT_DECISION', 'approval', item_id,

                       note or action, {'actorName': actor_name, 'transcriptId': tr_id,

                                        'studentId': target.get('studentId')})

        _notify_user(target.get('studentId'), 'Official transcript update',

                     f"Your transcript ({target.get('term', 'term')}) was {target['status'].lower()}. " + (note or ''), 'general')



    else:

        return _academic_error('NOT_FOUND', 'Unknown approval item', 404)



    items = build_principal_queue()

    return jsonify({'status': 'success', 'message': f'Approval {item_id} processed ({action})',

                    'counts': _approval_counts(items)})



@app.route('/api/principal/approvals/batch-action', methods=['POST'])

def handle_principal_batch_approvals():

    user, error = _academic_require(('principal', 'admin'))

    if error: return error

    if PRINCIPAL_DEMO_MODE:

        data = request.get_json(silent=True) or {}

        action = (data.get('action') or 'approve').lower()

        if action != 'approve':

            return _academic_error('INVALID_ACTION', 'Batch action supports approve only')

        note = (data.get('note') or 'Batch authorized by Principal (demo)').strip()

        pend = [i for i in _demo_filter_queue(status='pending') if i['type'] == 'grade_submission']

        now_iso = _demo_now()

        for it in pend:

            _demo_approve_item(user, it['id'], 'approve', note, now_iso)

        return jsonify({'status': 'success', 'mode': 'demo',

                        'message': f'Demo: authorized {len(pend)} gradebook group(s)',

                        'affected': len(pend), 'counts': _demo_counts()})



    data = request.get_json(silent=True) or {}

    action = (data.get('action') or 'approve').lower()

    if action != 'approve':

        return _academic_error('INVALID_ACTION', 'Batch action supports approve only')



    note = (data.get('note') or 'Batch authorized by Principal').strip()

    now_iso = ACADEMIC.now()

    groups = _grade_submission_groups()

    affected = len(groups)

    if affected:

        ACADEMIC.execute("UPDATE grades SET workflow='published', updated_at=? WHERE workflow IN ('draft','submitted','returned') AND score IS NOT NULL", (now_iso,))

        ACADEMIC.audit(user['id'], user['role'], 'PRINCIPAL_BATCH_APPROVE', 'approval', 'all-pending', note,

                       {'actorName': _actor_label(user), 'count': affected})

    items = build_principal_queue()

    return jsonify({'status': 'success', 'message': f'Authorized {affected} gradebook group(s)',

                    'affected': affected, 'counts': _approval_counts(items)})



@app.route('/api/principal/audit', methods=['GET'])

def get_principal_audit_log():

    user, error = _academic_require(('principal', 'admin'))

    if error: return error

    if PRINCIPAL_DEMO_MODE:

        try:

            limit = min(max(int(request.args.get('limit', 25)), 1), 200)

        except ValueError:

            limit = 25

        role_f = (request.args.get('role') or '').lower()

        actor_f = (request.args.get('actor') or '').strip().lower()

        search = (request.args.get('search') or '').lower()

        rows = []

        for ev in PRINCIPAL_DEMO_STATE['auditEvents']:

            if role_f and role_f != 'all' and (ev.get('actor_role') or '').lower() != role_f:

                continue

            if actor_f:

                md_raw = ev.get('metadata_json') or '{}'

                try:

                    md_val = json.loads(md_raw)

                except Exception:

                    md_val = {}

                actor_label = (md_val.get('actorName') or '').lower()

                if actor_f not in (ev.get('actor_id') or '').lower() and actor_f not in actor_label:

                    continue

            if search:

                hay = f"{ev.get('action','')} {ev.get('reason','')} {ev.get('entity_id','')}".lower()

                if search not in hay:

                    continue

            rows.append(_demo_event_out(ev))

            if len(rows) >= limit:

                break

        return jsonify({'status': 'success', 'mode': 'demo', 'data': rows, 'meta': {'total': len(rows)}})

    limit = min(max(int(request.args.get('limit', 25)), 1), 200)

    role_filter = (request.args.get('role') or '').lower()

    search = (request.args.get('search') or '').lower()

    clauses, args = ['1=1'], []

    if role_filter and role_filter != 'all':

        clauses.append('actor_role=?'); args.append(role_filter)

    if search:

        clauses.append('(LOWER(action) LIKE ? OR LOWER(reason) LIKE ? OR LOWER(entity_id) LIKE ?)')

        like = f'%{search}%'

        args.extend([like, like, like])

    events = ACADEMIC.query(

        f"SELECT * FROM audit_events WHERE {' AND '.join(clauses)} ORDER BY id DESC LIMIT ?", (*args, limit))

    return jsonify({'status': 'success', 'data': [dict(e) for e in events]})



@app.route('/api/principal/stats', methods=['GET'])

def principal_stats():

    user, error = _academic_require(('principal', 'admin'))

    if error: return error

    if PRINCIPAL_DEMO_MODE:

        return jsonify({'status': 'success', 'mode': 'demo', 'data': _demo_stats_payload(user)})



    queue = build_principal_queue()

    counts = _approval_counts(queue)

    att = ACADEMIC.one("SELECT COUNT(*) AS total, SUM(CASE WHEN status IN ('present','tardy','excused') THEN 1 ELSE 0 END) AS present FROM attendance")

    attendance_rate = round((att['present'] / att['total'] * 100), 1) if att and att['total'] else None

    gpas = [ACADEMIC.aggregate_gpa(s['id']) for s in DB['students'][:20]]

    gpas = [g for g in gpas if isinstance(g, (int, float)) and g > 0]

    avg_gpa = round(sum(gpas) / len(gpas), 2) if gpas else None

    recent = ACADEMIC.query("SELECT * FROM audit_events WHERE actor_role IN ('principal','admin') ORDER BY id DESC LIMIT 6")

    return jsonify({

        'status': 'success',

        'data': {

            'totalStudents': len(DB['students']),

            'totalTeachers': len(DB['teachers']),

            'totalClasses': len(DB['classes']),

            'activeServiceRequests': len([r for r in DB['serviceRequests'] if r.get('status') in ('open', 'pending', 'in_progress')]),

            'pendingApprovals': counts['pending'],

            'needsCorrection': counts['needs_correction'],

            'publishedGradeRecords': ACADEMIC.one("SELECT COUNT(*) AS n FROM grades WHERE workflow='published'")['n'],

            'draftGradeRecords': ACADEMIC.one("SELECT COUNT(*) AS n FROM grades WHERE workflow IN ('draft','submitted','returned')")['n'],

            'attendanceRate': attendance_rate,

            'averageGpa': avg_gpa,

            'recentActions': [dict(e) for e in recent],

        }

    })



# ── PRINCIPAL STUDENT RECORDS & AUTHORIZED EDITS ──

@app.route('/api/principal/roster/students', methods=['GET'])

def principal_roster_students():

    user, error = _academic_require(('principal', 'admin'))

    if error: return error

    if PRINCIPAL_DEMO_MODE:

        _demo_sync_student_rollups()

        search = (request.args.get('search') or '').lower()

        class_filter = (request.args.get('class') or '').strip()

        rows = []

        for s in PRINCIPAL_DEMO_STATE['students']:

            if class_filter and s.get('class') != class_filter:

                continue

            if search and search not in str(s.get('name', '')).lower() and search not in str(s.get('id', '')).lower():

                continue

            rows.append(dict(s))

        classes = sorted({s.get('class') for s in PRINCIPAL_DEMO_STATE['students'] if s.get('class')})

        return jsonify({'status': 'success', 'mode': 'demo', 'data': rows, 'classes': classes, 'meta': {'total': len(rows)}})

    search = (request.args.get('search') or '').lower()

    class_filter = (request.args.get('class') or '').strip()

    rows = []

    for s in DB['students']:

        if class_filter and s.get('class') != class_filter:

            continue

        if search and search not in str(s.get('name', '')).lower() and search not in str(s.get('id', '')).lower():

            continue

        rows.append({**s,

                     'gpaLive': ACADEMIC.aggregate_gpa(s['id']),

                     'attendancePct': ACADEMIC.attendance_summary(s['id']).get('percentage'),

                     'openRequests': len([r for r in DB['serviceRequests'] if r.get('studentId') == s['id'] and r.get('status') in ('open', 'pending', 'in_progress')])})

    classes = sorted({s.get('class') for s in DB['students'] if s.get('class')})

    return jsonify({'status': 'success', 'data': rows, 'classes': classes, 'meta': {'total': len(rows)}})



STUDENT_EDITABLE_FIELDS = ('name', 'gender', 'grade', 'class', 'status', 'parentEmail', 'parentName', 'advisor')



@app.route('/api/principal/roster/students/<student_id>', methods=['PUT'])

def principal_edit_student(student_id):

    user, error = _academic_require(('principal', 'admin'))

    if error: return error

    if PRINCIPAL_DEMO_MODE:

        data = request.get_json(silent=True) or {}

        reason = (data.get('reason') or '').strip()

        if not reason:

            return _academic_error('REASON_REQUIRED', 'A written reason is mandatory for official record corrections')

        student = next((s for s in PRINCIPAL_DEMO_STATE['students'] if s['id'] == student_id), None)

        if not student:

            return _academic_error('NOT_FOUND', 'Demo student not found', 404)

        changes = {k: data[k] for k in STUDENT_EDITABLE_FIELDS if k in data and str(data[k]) != str(student.get(k))}

        if not changes:

            return _academic_error('NO_CHANGES', 'No field values actually changed')

        previous = {k: student.get(k) for k in changes}

        student.update(changes)

        _demo_audit(user, 'PRINCIPAL_STUDENT_RECORD_EDIT', 'student', student_id, reason,

                    {'changes': changes, 'previous': previous})

        return jsonify({'status': 'success', 'mode': 'demo', 'data': dict(student),

                        'message': 'Demo student record updated and audited'})

    data = request.get_json(silent=True) or {}

    reason = (data.get('reason') or '').strip()

    if not reason:

        return _academic_error('REASON_REQUIRED', 'A written reason is mandatory for official record corrections')

    student = _student(student_id)

    if not student:

        return _academic_error('NOT_FOUND', 'Student not found', 404)

    changes = {k: data[k] for k in STUDENT_EDITABLE_FIELDS if k in data and str(data[k]) != str(student.get(k))}

    if not changes:

        return _academic_error('NO_CHANGES', 'No field values actually changed')

    previous = {k: student.get(k) for k in changes}

    student.update(changes)

    _persist_students()

    ACADEMIC.audit(user['id'], user['role'], 'PRINCIPAL_STUDENT_RECORD_EDIT', 'student', student_id, reason,

                   {'actorName': _actor_label(user), 'changes': changes, 'previous': previous})

    return jsonify({'status': 'success', 'data': student, 'message': 'Student record updated and audited'})



# ── PRINCIPAL FACULTY OVERSIGHT ──

@app.route('/api/principal/roster/teachers', methods=['GET'])

def principal_roster_teachers():

    user, error = _academic_require(('principal', 'admin'))

    if error: return error

    if PRINCIPAL_DEMO_MODE:

        search = (request.args.get('search') or '').lower()

        dept = (request.args.get('department') or '').strip()

        pend, pub = {}, {}

        for grp in PRINCIPAL_DEMO_STATE['gradebookGroups']:

            for tid in (grp.get('teacherIds') or '').split(','):

                if not tid:

                    continue

                if grp['status'] == 'pending':

                    pend[tid] = pend.get(tid, 0) + 1

                elif grp['status'] == 'approved':

                    pub[tid] = pub.get(tid, 0) + 1

        rows = []

        for t in PRINCIPAL_DEMO_STATE['teachers']:

            if dept and t.get('department') != dept:

                continue

            if search and search not in str(t.get('name', '')).lower() and search not in str(t.get('id', '')).lower() and search not in str(t.get('subject', '')).lower():

                continue

            prof = _demo_teacher_profile(t)

            rows.append({**prof, 'pendingGradeRecords': pend.get(t['id'], 0),

                         'publishedGradeRecords': pub.get(t['id'], 0)})

        return jsonify({'status': 'success', 'mode': 'demo', 'data': rows, 'meta': {'total': len(rows)}})

    pending_by_teacher = {}

    for grp in _grade_submission_groups():

        for tid in (grp['teacher_ids'] or '').split(','):

            if tid:

                pending_by_teacher[tid] = pending_by_teacher.get(tid, 0) + grp['records']

    published_by_teacher = {r['recorded_by']: r['n'] for r in ACADEMIC.query(

        "SELECT recorded_by, COUNT(*) AS n FROM grades WHERE workflow='published' GROUP BY recorded_by")}

    rows = []

    for t in DB['teachers']:

        rows.append({**t,

                     'pendingGradeRecords': pending_by_teacher.get(t.get('id'), 0),

                     'publishedGradeRecords': published_by_teacher.get(t.get('id'), 0)})

    return jsonify({'status': 'success', 'data': rows, 'meta': {'total': len(rows)}})



# ── PRINCIPAL PARENT / GUARDIAN ROSTER (demo) ──

@app.route('/api/principal/roster/parents', methods=['GET'])

def principal_roster_parents():

    user, error = _academic_require(('principal', 'admin'))

    if error: return error

    rows = _demo_guardian_profiles()

    if PRINCIPAL_DEMO_MODE:

        search = (request.args.get('search') or '').lower()

        relation = (request.args.get('relation') or '').strip()

        grade = (request.args.get('grade') or '').strip()

        if relation and relation != 'all':

            rows = [r for r in rows if r.get('relation') == relation]

        if grade and grade != 'all':

            rows = [r for r in rows if any(ls.get('grade') == grade for ls in r['linkedStudents'])]

        if search:

            def _hit(r):

                hay = ' '.join([str(r.get('name', '')), str(r.get('id', '')), str(r.get('email', '')),

                                str(r.get('occupation', '')), str(r.get('district', ''))]

                               + [str(ls.get('name', '')) + ' ' + str(ls.get('class', '')) for ls in r['linkedStudents']]).lower()

                return search in hay

            rows = [r for r in rows if _hit(r)]

        grades = sorted({ls.get('grade') for r in _demo_guardian_profiles() for ls in r['linkedStudents'] if ls.get('grade')})

        return jsonify({'status': 'success', 'mode': 'demo', 'data': rows, 'grades': grades, 'meta': {'total': len(rows)}})

    # Real mode: derive guardians from the live student roster.

    seen, rows = set(), []

    for s in DB['students']:

        pid = 'PG-' + str(s['id'])[-3:]

        if pid in seen:

            continue

        seen.add(pid)

        rows.append({'id': pid, 'name': s.get('parentName'), 'email': s.get('parentEmail'),

                     'linkedStudents': [{'id': s['id'], 'name': s.get('name'), 'class': s.get('class')}],

                     'avatarUrl': _demo_avatar(s.get('parentName') or s.get('name'))})

    return jsonify({'status': 'success', 'data': rows, 'meta': {'total': len(rows)}})





# ════════════════════════════════════════════════════════════════════

# DEMO-ONLY PRINCIPAL SUPPORT ENDPOINTS (used while PRINCIPAL_DEMO_MODE)

# These power the documents and student-detail views from the in-memory

# fixtures so the whole portal can be reviewed before real wiring.

# ════════════════════════════════════════════════════════════════════

@app.route('/api/principal/transcripts', methods=['GET'])

def principal_demo_transcripts():

    user, error = _academic_require(('principal', 'admin'))

    if error: return error

    rows = []

    for t in PRINCIPAL_DEMO_STATE['transcripts']:

        rec = dict(t)

        rec.setdefault('fileName', f"transcript-{t.get('id','doc')}.pdf")

        rec.setdefault('uploadedAt', t.get('date'))

        rows.append(rec)

    return jsonify({'status': 'success', 'mode': 'demo', 'data': rows, 'meta': {'total': len(rows)}})



@app.route('/api/principal/service-requests', methods=['GET'])

def principal_demo_service_requests():

    user, error = _academic_require(('principal', 'admin'))

    if error: return error

    category = (request.args.get('category') or '').strip().lower()

    student_id = (request.args.get('studentId') or '').strip()

    rows = []

    for r in PRINCIPAL_DEMO_STATE['serviceRequests']:

        if category and str(r.get('category', '')).lower() != category:

            continue

        if student_id and r.get('studentId') != student_id:

            continue

        rows.append(dict(r))

    return jsonify({'status': 'success', 'mode': 'demo', 'data': rows, 'meta': {'total': len(rows)}})



@app.route('/api/principal/grades', methods=['GET'])

def principal_demo_grades():

    user, error = _academic_require(('principal', 'admin'))

    if error: return error

    student_id = (request.args.get('studentId') or '').strip()

    rows = _demo_grades_for(student_id) if student_id else []

    return jsonify({'status': 'success', 'mode': 'demo', 'data': rows, 'meta': {'total': len(rows)}})



@app.route('/api/principal/attendance-by-day', methods=['GET'])

def principal_demo_attendance_by_day():

    user, error = _academic_require(('principal', 'admin'))

    if error: return error

    student_id = (request.args.get('studentId') or '').strip()

    try:

        limit = int(request.args.get('limit', 8))

    except ValueError:

        limit = 8

    payload = _demo_attendance_for(student_id, limit) if student_id else {'studentId': None, 'records': []}

    return jsonify({'status': 'success', 'mode': 'demo', 'data': payload})



@app.route('/api/principal/override-grade', methods=['POST'])

def principal_demo_override_grade():

    user, error = _academic_require(('principal', 'admin'))

    if error: return error

    data = request.get_json(silent=True) or {}

    grade_id = data.get('gradeId')

    reason = (data.get('reason') or '').strip()

    if not grade_id:

        return _academic_error('NOT_FOUND', 'Missing grade reference', 404)

    if not reason:

        return _academic_error('REASON_REQUIRED', 'A written reason is mandatory for grade overrides')

    try:

        new_score = int(data.get('score'))

    except (TypeError, ValueError):

        return _academic_error('INVALID_SCORE', 'Score must be a number')

    previous = PRINCIPAL_DEMO_STATE['gradeOverrides'].get(grade_id)

    PRINCIPAL_DEMO_STATE['gradeOverrides'][grade_id] = new_score

    _demo_audit(user, 'PRINCIPAL_GRADE_OVERRIDE', 'grade', str(grade_id), reason,

                {'gradeId': grade_id, 'newScore': new_score, 'previous': previous})

    updated = {'id': grade_id, 'score': new_score, 'maxScore': 100, 'percentage': new_score,

               'letterGrade': _demo_grade_band(new_score), 'workflow': 'published',

               'overrideNote': reason}

    return jsonify({'status': 'success', 'mode': 'demo', 'data': updated,

                    'message': 'Demo grade override recorded in the management audit trail'})





# ── TEACHER / PRINCIPAL GRADEBOOK CLEARANCE SYNC ──

@app.route('/api/academic/gradebook/clearance-status', methods=['GET'])

def academic_gradebook_clearance_status():

    class_id = request.args.get('classId', 'cls-10a')

    period_id = request.args.get('periodId', 'gp-q1')



    queue = build_principal_queue()

    matching_item = next((it for it in queue if it.get('classId') == class_id or it.get('id') == f"grade:{class_id}:{period_id}"), None)



    row = ACADEMIC.one("""

        SELECT g.workflow, g.updated_at 

        FROM grades g 

        JOIN assessments a ON a.id = g.assessment_id 

        WHERE a.class_id = ? 

        ORDER BY g.updated_at DESC LIMIT 1

    """, (class_id,))



    workflow = (row and row.get('workflow')) or 'draft'

    status = 'draft'

    decision_note = ''

    decided_by = 'Dr. Ly Bunheng'

    decided_at = ''



    if matching_item:

        status = matching_item.get('status', 'pending')

        decision_note = matching_item.get('decisionNote', '')

        decided_by = matching_item.get('decidedBy', 'Dr. Ly Bunheng')

        decided_at = matching_item.get('decidedAt', '')

        if status == 'approved':

            workflow = 'published'

        elif status == 'needs_correction':

            workflow = 'returned'

        elif status == 'pending':

            workflow = 'submitted'

    else:

        if workflow == 'published':

            status = 'approved'

        elif workflow == 'returned':

            status = 'needs_correction'

        elif workflow == 'submitted':

            status = 'pending'



    labels = {

        'published': 'Verified & Published by Academic Principal',

        'submitted': 'Pending Principal Clearance',

        'returned': 'Revisions Requested by Principal',

        'draft': 'Draft · Not Yet Submitted for Clearance'

    }



    return jsonify({

        'status': status,

        'workflow': workflow,

        'label': labels.get(workflow, 'Draft'),

        'decisionNote': decision_note,

        'decidedBy': decided_by,

        'decidedAt': decided_at,

        'classId': class_id,

        'periodId': period_id

    }), 200



@app.route('/api/academic/gradebook/submit-clearance', methods=['POST'])

def academic_gradebook_submit_clearance():

    data = request.get_json(silent=True) or {}

    class_id = data.get('classId', 'cls-10a')

    period_id = data.get('periodId', 'gp-q1')



    ACADEMIC.execute("""

        UPDATE grades SET workflow='submitted', updated_at=? 

        WHERE assessment_id IN (SELECT id FROM assessments WHERE class_id=?)

    """, (ACADEMIC.now(), class_id))



    ACADEMIC.audit('tch-jenkins', 'teacher', 'TEACHER_SUBMIT_CLEARANCE', 'gradebook', class_id, 'Submitted gradebook for Principal clearance', {'classId': class_id, 'periodId': period_id})



    return jsonify({'status': 'pending', 'workflow': 'submitted', 'message': 'Gradebook submitted to Academic Principal for Executive Clearance.'}), 200



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

    print("=" * 60)

    print(f"  API:  http://localhost:{PORT}/api/health")

    print("=" * 60)

    

    app.run(host='0.0.0.0', port=PORT, debug=True)

