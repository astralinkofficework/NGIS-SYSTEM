"""
System Management API module for NGIS School Management System.
Powers the complete System configuration section for Admin Portal:
- School Information
- School Year Configuration (School Year, School Week, Exam Config, Score Lock, Define/Design Curriculum, Declare Class, Student Transition, Technician Assign)
- Account Management (Employee Group, Employee Accounts, Student Accounts, Parent Accounts)
- Schedule
- General Setting
"""

import os
import json
from flask import request, jsonify

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
CONFIG_FILE = os.path.join(DATA_DIR, 'system_configuration.json')

def _load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def _save_config(data):
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception:
        return False

def register_system_routes(app, DB):
    """Register all REST endpoints for System Management."""

    @app.route('/api/system/overview', methods=['GET'])
    def system_overview():
        cfg = _load_config()
        return jsonify({
            'schoolName': cfg.get('school_info', {}).get('nameEnglish'),
            'academicYear': cfg.get('general_settings', {}).get('academicYear'),
            'totalAccounts': len(cfg.get('accounts', [])),
            'totalDeclaredClasses': len(cfg.get('declared_classes', [])),
            'curriculaCount': len(cfg.get('curricula', [])),
            'systemStatus': 'Operational' if not cfg.get('general_settings', {}).get('maintenanceMode') else 'Maintenance'
        })

    @app.route('/api/system/school-info', methods=['GET', 'PUT'])
    def system_school_info():
        cfg = _load_config()
        if request.method == 'GET':
            return jsonify({'success': True, 'data': cfg.get('school_info', {})})
        data = request.get_json() or {}
        cfg.setdefault('school_info', {}).update(data)
        _save_config(cfg)
        return jsonify({'success': True, 'data': cfg['school_info']})

    @app.route('/api/system/school-years', methods=['GET', 'POST'])
    def system_school_years():
        cfg = _load_config()
        if request.method == 'GET':
            return jsonify({'success': True, 'data': cfg.get('school_years', [])})
        data = request.get_json() or {}
        years = cfg.setdefault('school_years', [])
        new_id = f"SY-{len(years) + 2024}"
        data['id'] = new_id
        years.append(data)
        _save_config(cfg)
        return jsonify({'success': True, 'item': data}), 201

    @app.route('/api/system/school-weeks', methods=['GET'])
    def system_school_weeks():
        cfg = _load_config()
        return jsonify({'success': True, 'data': cfg.get('school_weeks', [])})

    @app.route('/api/system/exam-config', methods=['GET', 'PUT'])
    def system_exam_config():
        cfg = _load_config()
        if request.method == 'GET':
            return jsonify({'success': True, 'data': cfg.get('exam_config', {})})
        data = request.get_json() or {}
        cfg.setdefault('exam_config', {}).update(data)
        _save_config(cfg)
        return jsonify({'success': True, 'data': cfg['exam_config']})

    @app.route('/api/system/score-locks', methods=['GET'])
    def system_score_locks():
        cfg = _load_config()
        return jsonify({'success': True, 'data': cfg.get('score_locks', [])})

    @app.route('/api/system/score-locks/toggle', methods=['POST'])
    def system_score_locks_toggle():
        cfg = _load_config()
        data = request.get_json() or {}
        lock_id = data.get('id')
        locks = cfg.get('score_locks', [])
        target = next((l for l in locks if l['id'] == lock_id), None)
        if not target:
            return jsonify({'success': False, 'message': 'Lock record not found'}), 404
        target['status'] = 'unlocked' if target['status'] == 'locked' else 'locked'
        target['lockedBy'] = 'Administrator' if target['status'] == 'locked' else None
        _save_config(cfg)
        return jsonify({'success': True, 'item': target})

    @app.route('/api/system/curricula', methods=['GET'])
    def system_curricula():
        cfg = _load_config()
        return jsonify({'success': True, 'data': cfg.get('curricula', [])})

    @app.route('/api/system/curriculum-designs', methods=['GET'])
    def system_curriculum_designs():
        cfg = _load_config()
        return jsonify({'success': True, 'data': cfg.get('curriculum_designs', [])})

    @app.route('/api/system/declared-classes', methods=['GET', 'POST'])
    def system_declared_classes():
        cfg = _load_config()
        if request.method == 'GET':
            return jsonify({'success': True, 'data': cfg.get('declared_classes', [])})
        data = request.get_json() or {}
        classes = cfg.setdefault('declared_classes', [])
        new_id = f"DCLS-{len(classes) + 1:02d}"
        data['id'] = new_id
        classes.append(data)
        _save_config(cfg)
        return jsonify({'success': True, 'item': data}), 201

    @app.route('/api/system/student-transitions', methods=['GET'])
    def system_student_transitions():
        cfg = _load_config()
        return jsonify({'success': True, 'data': cfg.get('student_transitions', [])})

    @app.route('/api/system/technicians', methods=['GET', 'POST'])
    def system_technicians():
        cfg = _load_config()
        if request.method == 'GET':
            return jsonify({'success': True, 'data': cfg.get('technician_assignments', [])})
        data = request.get_json() or {}
        techs = cfg.setdefault('technician_assignments', [])
        new_id = f"TECH-{len(techs) + 1:02d}"
        data['id'] = new_id
        techs.append(data)
        _save_config(cfg)
        return jsonify({'success': True, 'item': data}), 201

    @app.route('/api/system/account-groups', methods=['GET'])
    def system_account_groups():
        cfg = _load_config()
        return jsonify({'success': True, 'data': cfg.get('account_groups', [])})

    @app.route('/api/system/accounts', methods=['GET'])
    def system_accounts():
        cfg = _load_config()
        role_filter = request.args.get('role', '').strip().upper()
        accounts = cfg.get('accounts', [])
        if role_filter and role_filter != 'ALL':
            accounts = [a for a in accounts if a.get('group') == role_filter or role_filter in a.get('role', '').upper()]
        return jsonify({'success': True, 'data': accounts, 'total': len(accounts)})

    @app.route('/api/system/schedule', methods=['GET', 'PUT'])
    def system_schedule():
        cfg = _load_config()
        if request.method == 'GET':
            return jsonify({'success': True, 'data': cfg.get('schedule', {})})
        data = request.get_json() or {}
        cfg.setdefault('schedule', {}).update(data)
        _save_config(cfg)
        return jsonify({'success': True, 'data': cfg['schedule']})

    @app.route('/api/system/general-settings', methods=['GET', 'PUT'])
    def system_general_settings():
        cfg = _load_config()
        if request.method == 'GET':
            return jsonify({'success': True, 'data': cfg.get('general_settings', {})})
        data = request.get_json() or {}
        cfg.setdefault('general_settings', {}).update(data)
        _save_config(cfg)
        return jsonify({'success': True, 'data': cfg['general_settings']})

    print("System Management routes registered successfully.")

