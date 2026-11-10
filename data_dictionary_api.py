"""
Data Dictionary API module for NGIS School Management System.
Powers the 5 Data Dictionary sub-modules for Admin and Principal portals:
1. School Data (Campuses, Buildings, Departments, Grades, Terms, Grading Scales)
2. Student's Data (Statuses, Admissions, Identity Types, Exemptions, Infractions, Awards)
3. Teacher's Data (Employment Types, Positions, Qualifications, Efforts, Disciplinary Codes)
4. Additional Data (Document Categories, Languages, Transit Routes, Relationships, Audit Events)
5. Timetable's Data (Bell Schedules, Instructional Days, Room Types, Subject Classifications, Constraints)
"""

import os
import json
from flask import request, jsonify

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
DICT_FILE = os.path.join(DATA_DIR, 'data_dictionary.json')

def _load_dictionary():
    if not os.path.exists(DICT_FILE):
        return {}
    try:
        with open(DICT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def _save_dictionary(data):
    try:
        with open(DICT_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception:
        return False

def register_dictionary_routes(app, DB):
    """Register all REST endpoints for Data Dictionary."""

    # 1. Overview Telemetry
    @app.route('/api/dictionary/overview', methods=['GET'])
    def dictionary_overview():
        d = _load_dictionary()
        school_cnt = sum(len(v) for v in d.get('school', {}).values() if isinstance(v, list))
        student_cnt = sum(len(v) for v in d.get('students', {}).values() if isinstance(v, list))
        teacher_cnt = sum(len(v) for v in d.get('teachers', {}).values() if isinstance(v, list))
        additional_cnt = sum(len(v) for v in d.get('additional', {}).values() if isinstance(v, list))
        timetable_cnt = sum(len(v) for v in d.get('timetable', {}).values() if isinstance(v, list))
        total_entries = school_cnt + student_cnt + teacher_cnt + additional_cnt + timetable_cnt

        return jsonify({
            'totalEntries': total_entries,
            'sections': {
                'school': { 'label': 'School Data', 'tablesCount': len(d.get('school', {})), 'entriesCount': school_cnt },
                'students': { 'label': "Student's Data", 'tablesCount': len(d.get('students', {})), 'entriesCount': student_cnt },
                'teachers': { 'label': "Teacher's Data", 'tablesCount': len(d.get('teachers', {})), 'entriesCount': teacher_cnt },
                'additional': { 'label': 'Additional Data', 'tablesCount': len(d.get('additional', {})), 'entriesCount': additional_cnt },
                'timetable': { 'label': "Timetable's Data", 'tablesCount': len(d.get('timetable', {})), 'entriesCount': timetable_cnt }
            },
            'lastSync': 'Live System Sync',
            'version': 'EMIS v4.2 / MoEYS 2026'
        })

    # 2. Section Tables
    @app.route('/api/dictionary/section/<section_name>', methods=['GET'])
    def dictionary_section(section_name):
        d = _load_dictionary()
        sec = d.get(section_name.lower())
        if sec is None:
            return jsonify({'success': False, 'message': f'Section {section_name} not found'}), 404
        return jsonify({'success': True, 'section': section_name, 'tables': sec})

    # 3. Table Items
    @app.route('/api/dictionary/table/<section_name>/<table_name>', methods=['GET', 'POST'])
    def dictionary_table(section_name, table_name):
        d = _load_dictionary()
        sec = d.get(section_name.lower())
        if not sec or table_name not in sec:
            return jsonify({'success': False, 'message': 'Table not found'}), 404

        if request.method == 'GET':
            items = sec[table_name]
            search = (request.args.get('search') or '').strip().lower()
            if search:
                filtered = []
                for item in items:
                    val_str = ' '.join(str(v).lower() for v in item.values())
                    if search in val_str:
                        filtered.append(item)
                return jsonify({'data': filtered, 'total': len(filtered), 'tableName': table_name})
            return jsonify({'data': items, 'total': len(items), 'tableName': table_name})

        # POST: Add new entry
        data = request.get_json() or {}
        new_id = data.get('id') or f"{table_name.upper()[:3]}-{len(sec[table_name]) + 1:02d}"
        data['id'] = new_id
        sec[table_name].append(data)
        _save_dictionary(d)
        return jsonify({'success': True, 'item': data}), 201

    # 4. Update & Delete Table Item
    @app.route('/api/dictionary/table/<section_name>/<table_name>/<item_id>', methods=['PUT', 'DELETE'])
    def dictionary_item_action(section_name, table_name, item_id):
        d = _load_dictionary()
        sec = d.get(section_name.lower())
        if not sec or table_name not in sec:
            return jsonify({'success': False, 'message': 'Table not found'}), 404

        items = sec[table_name]
        idx = next((i for i, it in enumerate(items) if str(it.get('id')) == str(item_id)), None)
        if idx is None:
            return jsonify({'success': False, 'message': 'Item not found'}), 404

        if request.method == 'PUT':
            body = request.get_json() or {}
            items[idx].update(body)
            items[idx]['id'] = item_id  # maintain id
            _save_dictionary(d)
            return jsonify({'success': True, 'item': items[idx]})

        elif request.method == 'DELETE':
            removed = items.pop(idx)
            _save_dictionary(d)
            return jsonify({'success': True, 'removed': removed})

    print("Data Dictionary routes registered successfully.")
