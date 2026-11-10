"""
NGIS School Information & Academic Configuration API
Authoritative backend service for institutional configuration, academic years,
campuses, operating hours, bell schedules, calendar, departments, timetable rules,
staff policies, permission management, and audit logging.
"""

import os
import json
import sqlite3
import datetime
from flask import Blueprint, request, jsonify

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
CONFIG_FILE = os.path.join(DATA_DIR, 'system_configuration.json')
TIMETABLE_STATE_FILE = os.path.join(DATA_DIR, 'timetable_state.json')
SQLITE_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.data', 'academic.sqlite3')

school_config_bp = Blueprint('school_config_bp', __name__)

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

def _get_caller(req):
    role = req.headers.get('X-User-Role')
    if not role:
        auth_hdr = req.headers.get('Authorization', '')
        if 'mock-jwt-token-' in auth_hdr:
            role = auth_hdr.split('mock-jwt-token-')[-1].strip().lower()
    if not role:
        role = req.args.get('role', 'admin').lower()
    if role not in ['admin', 'principal', 'editor', 'teacher', 'student']:
        role = 'admin'

    user_id = req.headers.get('X-User-Id') or req.args.get('userId')
    if not user_id:
        if role == 'admin':
            user_id = 'ADM-2024-001'
        elif role == 'principal':
            user_id = 'PRN-2024-001'
        elif role == 'editor':
            user_id = 'USR-006'
        else:
            user_id = 'USR-GUEST'

    user_name = req.headers.get('X-User-Name')
    if not user_name:
        if role == 'admin':
            user_name = 'Mr. Heng Samnang'
        elif role == 'principal':
            user_name = 'Dr. Ly Bunheng'
        elif role == 'editor':
            user_name = 'Ms. Keo Sreymom'
        else:
            user_name = 'Guest User'

    user_campus = req.headers.get('X-User-Campus', 'ALL')
    if role == 'editor' and user_campus == 'ALL':
        user_campus = 'TK-MAIN'

    return {
        'role': role,
        'userId': user_id,
        'userName': user_name,
        'campus': user_campus
    }

def _check_permission(caller, section, action='view'):
    cfg = _load_config()
    matrix = cfg.get('permissions_matrix', {}).get('roles', {})
    role = caller['role']
    if role == 'admin':
        return True, ""

    role_rules = matrix.get(role, {})
    sec_rule = role_rules.get('sections', {}).get(section, {})
    
    if action == 'view':
        allowed = sec_rule.get('view', False)
    elif action == 'edit':
        allowed = sec_rule.get('edit', False)
    elif action == 'activate':
        allowed = sec_rule.get('activate', False)
    elif action == 'rollback':
        allowed = sec_rule.get('rollback', False)
    else:
        allowed = False

    # Check editor explicit permissions list
    if role == 'editor':
        assigned = cfg.get('permissions_matrix', {}).get('assignedEditors', [])
        my_editor = next((e for e in assigned if e.get('id') == caller['userId']), None)
        if my_editor:
            permitted = my_editor.get('permittedSections', [])
            if action == 'view':
                allowed = True
            elif action == 'edit':
                allowed = (section in permitted)
            else:
                allowed = False

    if not allowed:
        return False, f"Access denied: Role '{role}' does not have '{action}' permission on '{section}'."
    return True, ""

def _log_audit(cfg, caller, section, action, prev_val, new_val, scope="School-wide", notes="", status="applied"):
    now_iso = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logs = cfg.setdefault('audit_log', [])
    entry_id = f"AUD-{len(logs) + 1:04d}"
    entry = {
        "id": entry_id,
        "timestamp": now_iso,
        "userId": caller['userId'],
        "userName": caller['userName'],
        "userRole": caller['role'],
        "section": section,
        "action": action,
        "previousValue": str(prev_val) if prev_val is not None else "—",
        "newValue": str(new_val) if new_val is not None else "—",
        "scope": scope,
        "status": status,
        "notes": notes
    }
    logs.insert(0, entry)
    # Keep up to 500 audit logs
    if len(logs) > 500:
        cfg['audit_log'] = logs[:500]
    return entry

def _sync_active_academic_year(year_id, year_str):
    # 1. Sync to SQLite academic.sqlite3 if available
    if os.path.exists(SQLITE_DB_PATH):
        try:
            conn = sqlite3.connect(SQLITE_DB_PATH)
            c = conn.cursor()
            c.execute("UPDATE academic_years SET is_current = 0")
            c.execute("UPDATE academic_years SET is_current = 1 WHERE name = ? OR id = ?", (year_str, year_id))
            conn.commit()
            conn.close()
        except Exception as e:
            print("SQLite sync error:", e)

    # 2. Sync to timetable_state.json
    if os.path.exists(TIMETABLE_STATE_FILE):
        try:
            with open(TIMETABLE_STATE_FILE, 'r', encoding='utf-8') as f:
                tt = json.load(f)
            tt.setdefault('institution', {})['academic_year'] = year_str
            with open(TIMETABLE_STATE_FILE, 'w', encoding='utf-8') as f:
                json.dump(tt, f, indent=2)
        except Exception as e:
            print("Timetable state sync error:", e)

def _sync_timetable_days(saturday_enabled):
    if os.path.exists(TIMETABLE_STATE_FILE):
        try:
            with open(TIMETABLE_STATE_FILE, 'r', encoding='utf-8') as f:
                tt = json.load(f)
            base_days = ["ច័ន្ទ", "អង្គារ", "ពុធ", "ព្រហស្បតិ៍", "សុក្រ"]
            if saturday_enabled:
                base_days.append("សៅរ៍")
            tt.setdefault('settings', {})['days'] = base_days
            with open(TIMETABLE_STATE_FILE, 'w', encoding='utf-8') as f:
                json.dump(tt, f, indent=2)
        except Exception as e:
            print("Timetable days sync error:", e)

# ══════════════════════════════════════════════════════════════
# REST API Endpoints
# ══════════════════════════════════════════════════════════════

@school_config_bp.route('/api/school-config/overview', methods=['GET'])
def get_overview():
    cfg = _load_config()
    caller = _get_caller(request)
    info = cfg.get('school_info', {})
    years = cfg.get('school_years', [])
    active_year = next((y for y in years if y.get('isCurrent') or y.get('status') == 'active'), None) or (years[0] if years else {})
    campuses = cfg.get('campuses', [])
    active_campuses = [c for c in campuses if c.get('status') == 'active']
    op = cfg.get('operating_schedule', {})
    open_days = [d for d in op.get('weeklyDays', []) if d.get('open')]
    departments = cfg.get('curricula', [])
    cur_term = "Semester 1"
    if active_year and active_year.get('terms'):
        act_term = next((t for t in active_year['terms'] if t.get('status') == 'active'), active_year['terms'][0])
        cur_term = act_term.get('name', 'Semester 1')

    # Get last updated info from audit log
    audit = cfg.get('audit_log', [])
    last_update = audit[0] if audit else {"timestamp": "2026-07-08 14:20:00", "userName": "Dr. Ly Bunheng"}

    return jsonify({
        'success': True,
        'schoolName': info.get('nameEnglish', 'New Gateway International School'),
        'khmerName': info.get('nameKhmer', 'សាលាអន្តរជាតិ ញូ ហ្គេតវ៉េ'),
        'moeysCode': info.get('moeysCode', 'MOEYS-PP-SEC-2016-048'),
        'logoUrl': info.get('logoUrl', '../../assets/images/logo.png'),
        'activeYear': active_year.get('year', '2026–2027'),
        'activeYearId': active_year.get('id', 'SY-2026'),
        'academicYearDates': f"{active_year.get('startDate', '2026-09-01')} to {active_year.get('endDate', '2027-06-30')}",
        'campusesCount': len(active_campuses),
        'totalCampuses': len(campuses),
        'operatingDaysCount': len(open_days),
        'saturdayEnabled': op.get('saturdayEnabled', True),
        'openingTime': open_days[0].get('openTime', '07:00') if open_days else '07:00',
        'closingTime': open_days[0].get('closeTime', '17:00') if open_days else '17:00',
        'departmentsCount': 8,
        'gradeLevelsCount': 6,
        'currentTerm': cur_term,
        'academicConfigStatus': 'Operational & Synchronized',
        'pendingReviewsCount': len(cfg.get('pending_reviews', [])),
        'lastUpdatedDate': last_update.get('timestamp', '2026-07-08 14:20:00'),
        'lastUpdatedUser': f"{last_update.get('userName', 'Administrator')} ({last_update.get('userRole', 'Admin').title()})"
    })

@school_config_bp.route('/api/school-config/full', methods=['GET'])
def get_full_configuration():
    cfg = _load_config()
    caller = _get_caller(request)
    
    # Calculate user capabilities for UI controls
    matrix = cfg.get('permissions_matrix', {}).get('roles', {}).get(caller['role'], {})
    assigned = cfg.get('permissions_matrix', {}).get('assignedEditors', [])
    editor_info = next((e for e in assigned if e.get('id') == caller['userId']), None)
    
    permitted_sections = []
    if caller['role'] == 'admin':
        permitted_sections = ["school_overview", "school_profile", "academic_years", "campuses", 
                              "school_days", "bell_schedule", "academic_calendar", "departments", 
                              "timetable_rules", "staff_policies", "permissions_access", "change_history"]
    elif caller['role'] == 'principal':
        permitted_sections = ["school_overview", "school_profile", "academic_years", "campuses", 
                              "school_days", "bell_schedule", "academic_calendar", "departments", 
                              "timetable_rules", "staff_policies", "change_history"]
    elif caller['role'] == 'editor':
        permitted_sections = editor_info.get('permittedSections', ["school_profile", "school_days", "bell_schedule", "academic_calendar"]) if editor_info else ["school_profile"]

    # Filter campuses if caller is scoped
    campuses = cfg.get('campuses', [])
    if caller['role'] == 'editor' and caller['campus'] != 'ALL':
        campuses = [c for c in campuses if c.get('id') == caller['campus'] or c.get('code') == caller['campus']]

    return jsonify({
        'success': True,
        'caller': caller,
        'userPermissions': {
            'role': caller['role'],
            'userId': caller['userId'],
            'userName': caller['userName'],
            'campusScope': caller['campus'],
            'permittedSections': permitted_sections,
            'canActivateYear': caller['role'] in ['admin', 'principal'],
            'canEditPermissions': caller['role'] == 'admin',
            'canRollback': caller['role'] == 'admin'
        },
        'school_info': cfg.get('school_info', {}),
        'academic_years': cfg.get('school_years', []),
        'campuses': campuses,
        'operating_schedule': cfg.get('operating_schedule', {}),
        'bell_schedule': cfg.get('bell_schedule', {}),
        'academic_calendar': cfg.get('academic_calendar', []),
        'timetable_rules': cfg.get('timetable_rules', {}),
        'staff_policies': cfg.get('staff_policies', {}),
        'permissions_matrix': cfg.get('permissions_matrix', {}),
        'audit_log': cfg.get('audit_log', []),
        'pending_reviews': cfg.get('pending_reviews', [])
    })

# 1. School Profile
@school_config_bp.route('/api/school-config/profile', methods=['GET', 'PUT'])
def handle_school_profile():
    cfg = _load_config()
    caller = _get_caller(request)
    if request.method == 'GET':
        return jsonify({'success': True, 'data': cfg.get('school_info', {})})

    allowed, err = _check_permission(caller, 'school_profile', 'edit')
    if not allowed:
        return jsonify({'success': False, 'message': err}), 403

    data = request.get_json() or {}
    prev = cfg.get('school_info', {}).get('nameEnglish', '')
    cfg.setdefault('school_info', {}).update(data)
    cfg['school_info']['updatedAt'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cfg['school_info']['updatedBy'] = f"{caller['userId']} ({caller['userName']})"

    _log_audit(cfg, caller, "School Profile", "update_profile", prev, cfg['school_info'].get('nameEnglish', ''), notes="Updated institutional profile and contact details")
    _save_config(cfg)
    return jsonify({'success': True, 'data': cfg['school_info'], 'message': 'School Profile updated successfully.'})

# 2. Academic Years
@school_config_bp.route('/api/school-config/academic-years', methods=['GET', 'POST'])
def handle_academic_years():
    cfg = _load_config()
    caller = _get_caller(request)
    if request.method == 'GET':
        return jsonify({'success': True, 'data': cfg.get('school_years', [])})

    allowed, err = _check_permission(caller, 'academic_years', 'edit')
    if not allowed:
        return jsonify({'success': False, 'message': err}), 403

    data = request.get_json() or {}
    year_name = data.get('year', '').strip()
    if not year_name:
        return jsonify({'success': False, 'message': 'Academic year name (e.g. 2026–2027) is required.'}), 400

    years = cfg.setdefault('school_years', [])
    if any(y.get('year') == year_name for y in years):
        return jsonify({'success': False, 'message': f"Academic year '{year_name}' already exists."}), 400

    new_id = f"SY-{datetime.datetime.now().year + len(years)}"
    new_year = {
        "id": new_id,
        "year": year_name,
        "displayName": data.get('displayName') or f"Academic Year {year_name}",
        "status": data.get('status', 'draft'),
        "isCurrent": False,
        "startDate": data.get('startDate', '2027-09-01'),
        "endDate": data.get('endDate', '2028-06-30'),
        "enrollmentStart": data.get('enrollmentStart', '2027-07-01'),
        "enrollmentEnd": data.get('enrollmentEnd', '2027-08-25'),
        "termsCount": len(data.get('terms', [])) or 2,
        "terms": data.get('terms') or [
            { "id": f"TRM-{new_id}-S1", "name": "Semester 1", "code": "S1", "sequence": 1, "startDate": "2027-09-01", "endDate": "2028-01-21", "status": "draft" },
            { "id": f"TRM-{new_id}-S2", "name": "Semester 2", "code": "S2", "sequence": 2, "startDate": "2028-02-07", "endDate": "2028-06-30", "status": "draft" }
        ]
    }
    years.append(new_year)
    _log_audit(cfg, caller, "Academic Years", "create_year", None, year_name, notes=f"Created new academic year {year_name} ({new_year['status']})")
    _save_config(cfg)
    return jsonify({'success': True, 'item': new_year, 'message': f"Academic year '{year_name}' created successfully."}), 201

@school_config_bp.route('/api/school-config/academic-years/<year_id>', methods=['PUT', 'DELETE'])
def handle_academic_year_item(year_id):
    cfg = _load_config()
    caller = _get_caller(request)
    allowed, err = _check_permission(caller, 'academic_years', 'edit')
    if not allowed:
        return jsonify({'success': False, 'message': err}), 403

    years = cfg.get('school_years', [])
    target = next((y for y in years if y.get('id') == year_id), None)
    if not target:
        return jsonify({'success': False, 'message': 'Academic year not found.'}), 404

    if request.method == 'DELETE':
        if target.get('isCurrent'):
            return jsonify({'success': False, 'message': 'Cannot delete the currently active academic year.'}), 400
        years.remove(target)
        _log_audit(cfg, caller, "Academic Years", "delete_year", target.get('year'), None, notes=f"Deleted academic year {target.get('year')}")
        _save_config(cfg)
        return jsonify({'success': True, 'message': f"Academic year '{target.get('year')}' deleted."})

    # PUT update
    data = request.get_json() or {}
    prev_val = json.dumps(target)
    target.update({k: v for k, v in data.items() if k not in ['id', 'isCurrent']})
    _log_audit(cfg, caller, "Academic Years", "update_year", prev_val, json.dumps(target), notes=f"Updated details for academic year {target.get('year')}")
    _save_config(cfg)
    return jsonify({'success': True, 'item': target, 'message': 'Academic year updated successfully.'})

@school_config_bp.route('/api/school-config/academic-years/<year_id>/activate', methods=['POST'])
def activate_academic_year(year_id):
    cfg = _load_config()
    caller = _get_caller(request)
    
    # Check if Editor: Editors cannot activate critical settings directly
    if caller['role'] == 'editor':
        # Submit for review
        pending = cfg.setdefault('pending_reviews', [])
        rev_id = f"REV-{len(pending) + 1:03d}"
        req_item = {
            "id": rev_id,
            "section": "Academic Years",
            "action": "activate_year",
            "targetId": year_id,
            "submittedBy": f"{caller['userId']} ({caller['userName']})",
            "submittedRole": caller['role'],
            "submittedAt": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "pending",
            "details": f"Request to activate Academic Year {year_id}"
        }
        pending.append(req_item)
        _log_audit(cfg, caller, "Academic Years", "submit_activation_review", None, year_id, status="pending_approval", notes="Submitted academic year activation for administrative approval")
        _save_config(cfg)
        return jsonify({
            'success': True,
            'requiresApproval': True,
            'reviewId': rev_id,
            'message': 'Activation request submitted for Administrator review and approval.'
        }), 202

    allowed, err = _check_permission(caller, 'academic_years', 'activate')
    if not allowed:
        return jsonify({'success': False, 'message': err}), 403

    years = cfg.get('school_years', [])
    target = next((y for y in years if y.get('id') == year_id), None)
    if not target:
        return jsonify({'success': False, 'message': 'Academic year not found.'}), 404

    prev_active = next((y for y in years if y.get('isCurrent')), None)
    prev_name = prev_active.get('year') if prev_active else "None"

    # Set all to non-current, target to active & current
    for y in years:
        if y.get('id') == year_id:
            y['isCurrent'] = True
            y['status'] = 'active'
        else:
            y['isCurrent'] = False
            if y.get('status') == 'active':
                y['status'] = 'completed'

    cfg.setdefault('general_settings', {})['academicYear'] = target.get('year')
    cfg.setdefault('timetable_rules', {})['activeAcademicYear'] = target.get('year')

    # Synchronize to SQLite and Timetable state
    _sync_active_academic_year(target.get('id'), target.get('year'))

    _log_audit(cfg, caller, "Academic Years", "activate_year", prev_name, target.get('year'), notes=f"Officially activated Academic Year {target.get('year')}")
    _save_config(cfg)
    return jsonify({
        'success': True,
        'item': target,
        'message': f"Academic Year '{target.get('year')}' is now the authoritative active school year."
    })

# 3. Campuses
@school_config_bp.route('/api/school-config/campuses', methods=['GET', 'POST'])
def handle_campuses():
    cfg = _load_config()
    caller = _get_caller(request)
    if request.method == 'GET':
        campuses = cfg.get('campuses', [])
        if caller['role'] == 'editor' and caller['campus'] != 'ALL':
            campuses = [c for c in campuses if c.get('id') == caller['campus'] or c.get('code') == caller['campus']]
        return jsonify({'success': True, 'data': campuses})

    allowed, err = _check_permission(caller, 'campuses', 'edit')
    if not allowed:
        return jsonify({'success': False, 'message': err}), 403

    data = request.get_json() or {}
    name = data.get('name', '').strip()
    code = data.get('code', '').strip().upper()
    if not name or not code:
        return jsonify({'success': False, 'message': 'Campus name and code are required.'}), 400

    campuses = cfg.setdefault('campuses', [])
    if any(c.get('code') == code for c in campuses):
        return jsonify({'success': False, 'message': f"Campus code '{code}' is already registered."}), 400

    new_id = f"CMP-{len(campuses) + 1:02d}"
    new_campus = {
        "id": new_id,
        "code": code,
        "name": name,
        "type": data.get('type', 'Secondary Campus'),
        "address": data.get('address', 'Phnom Penh, Cambodia'),
        "phone": data.get('phone', '+855 23 888 777'),
        "email": data.get('email', f"{code.lower()}@ngis.edu.kh"),
        "administrator": data.get('administrator', 'Mr. Heng Samnang'),
        "principal": data.get('principal', 'Dr. Ly Bunheng'),
        "status": data.get('status', 'active'),
        "established": str(data.get('established', datetime.datetime.now().year)),
        "academicLevels": data.get('academicLevels', ["Grades 7-12"]),
        "departments": data.get('departments', ["dept-mat", "dept-sci", "dept-eng", "dept-khm"]),
        "operatingDays": data.get('operatingDays', ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]),
        "operatingHours": data.get('operatingHours', {"open": "07:00", "close": "17:00"}),
        "saturdayEnabled": data.get('saturdayEnabled', False)
    }
    campuses.append(new_campus)
    _log_audit(cfg, caller, "Campuses", "add_campus", None, name, scope=code, notes=f"Added new campus facility {name} ({code})")
    _save_config(cfg)
    return jsonify({'success': True, 'item': new_campus, 'message': f"Campus '{name}' added successfully."}), 201

@school_config_bp.route('/api/school-config/campuses/<campus_id>', methods=['PUT', 'DELETE'])
def handle_campus_item(campus_id):
    cfg = _load_config()
    caller = _get_caller(request)
    allowed, err = _check_permission(caller, 'campuses', 'edit')
    if not allowed:
        return jsonify({'success': False, 'message': err}), 403

    campuses = cfg.get('campuses', [])
    target = next((c for c in campuses if c.get('id') == campus_id or c.get('code') == campus_id), None)
    if not target:
        return jsonify({'success': False, 'message': 'Campus record not found.'}), 404

    # Scope check: if caller has specific campus scope, ensure matching
    if caller['campus'] != 'ALL' and caller['campus'] not in [target.get('id'), target.get('code')]:
        return jsonify({'success': False, 'message': f"Access denied: You are not authorized to modify campus '{target.get('name')}'."}), 403

    if request.method == 'DELETE':
        if target.get('code') == 'TK-MAIN':
            return jsonify({'success': False, 'message': 'Cannot delete the primary main campus.'}), 400
        campuses.remove(target)
        _log_audit(cfg, caller, "Campuses", "delete_campus", target.get('name'), None, scope=target.get('code'), notes=f"Removed campus {target.get('name')}")
        _save_config(cfg)
        return jsonify({'success': True, 'message': f"Campus '{target.get('name')}' removed."})

    # PUT update
    data = request.get_json() or {}
    prev_val = json.dumps(target)
    target.update({k: v for k, v in data.items() if k not in ['id']})
    _log_audit(cfg, caller, "Campuses", "update_campus", prev_val, json.dumps(target), scope=target.get('code'), notes=f"Updated campus details for {target.get('name')}")
    _save_config(cfg)
    return jsonify({'success': True, 'item': target, 'message': 'Campus updated successfully.'})

# 4. Operating Days & Hours
@school_config_bp.route('/api/school-config/operating-schedule', methods=['GET', 'PUT'])
def handle_operating_schedule():
    cfg = _load_config()
    caller = _get_caller(request)
    if request.method == 'GET':
        return jsonify({'success': True, 'data': cfg.get('operating_schedule', {})})

    allowed, err = _check_permission(caller, 'school_days', 'edit')
    if not allowed:
        return jsonify({'success': False, 'message': err}), 403

    data = request.get_json() or {}
    prev = cfg.get('operating_schedule', {})
    cfg['operating_schedule'] = data
    
    # Check Saturday toggle and sync to timetable state
    sat_enabled = data.get('saturdayEnabled', True)
    _sync_timetable_days(sat_enabled)

    _log_audit(cfg, caller, "Operating Schedule", "update_schedule", json.dumps(prev), json.dumps(data), notes=f"Updated weekly school schedule. Saturday enabled: {sat_enabled}")
    _save_config(cfg)
    return jsonify({'success': True, 'data': cfg['operating_schedule'], 'message': 'Operating schedule updated and synchronized.'})

# 5. Bell Schedule & Class Periods
@school_config_bp.route('/api/school-config/bell-schedule', methods=['GET', 'PUT'])
def handle_bell_schedule():
    cfg = _load_config()
    caller = _get_caller(request)
    if request.method == 'GET':
        return jsonify({'success': True, 'data': cfg.get('bell_schedule', {})})

    allowed, err = _check_permission(caller, 'bell_schedule', 'edit')
    if not allowed:
        return jsonify({'success': False, 'message': err}), 403

    data = request.get_json() or {}
    periods = data.get('periods', [])
    
    # Validate periods: start time < end time
    for p in periods:
        s = p.get('start', '')
        e = p.get('end', '')
        if s and e and s >= e:
            return jsonify({'success': False, 'message': f"Invalid period time range: {p.get('label')} ({s} - {e}). Closing time must occur after start time."}), 400

    prev = cfg.get('bell_schedule', {})
    cfg['bell_schedule'] = data
    
    _log_audit(cfg, caller, "Bell Schedule", "update_bell_schedule", json.dumps(prev), json.dumps(data), notes=f"Updated bell schedule with {len(periods)} instructional & break slots")
    _save_config(cfg)
    return jsonify({'success': True, 'data': cfg['bell_schedule'], 'message': 'Bell schedule updated successfully.'})

# 6. Academic Calendar Events
@school_config_bp.route('/api/school-config/calendar', methods=['GET', 'POST'])
def handle_calendar():
    cfg = _load_config()
    caller = _get_caller(request)
    if request.method == 'GET':
        return jsonify({'success': True, 'data': cfg.get('academic_calendar', [])})

    allowed, err = _check_permission(caller, 'academic_calendar', 'edit')
    if not allowed:
        return jsonify({'success': False, 'message': err}), 403

    data = request.get_json() or {}
    title = data.get('title', '').strip()
    if not title:
        return jsonify({'success': False, 'message': 'Event title is required.'}), 400

    events = cfg.setdefault('academic_calendar', [])
    new_id = f"EVT-{datetime.datetime.now().year}-{len(events) + 1:03d}"
    new_evt = {
        "id": new_id,
        "title": title,
        "category": data.get('category', 'event'),
        "startDate": data.get('startDate', datetime.datetime.now().strftime("%Y-%m-%d")),
        "endDate": data.get('endDate', data.get('startDate', datetime.datetime.now().strftime("%Y-%m-%d"))),
        "campuses": data.get('campuses', ["All Campuses"]),
        "grades": data.get('grades', ["All Grades"]),
        "description": data.get('description', ''),
        "status": data.get('status', 'scheduled')
    }
    events.append(new_evt)
    _log_audit(cfg, caller, "Academic Calendar", "add_event", None, title, notes=f"Added calendar event '{title}' ({new_evt['category']})")
    _save_config(cfg)
    return jsonify({'success': True, 'item': new_evt, 'message': f"Calendar event '{title}' scheduled."}), 201

@school_config_bp.route('/api/school-config/calendar/<evt_id>', methods=['PUT', 'DELETE'])
def handle_calendar_item(evt_id):
    cfg = _load_config()
    caller = _get_caller(request)
    allowed, err = _check_permission(caller, 'academic_calendar', 'edit')
    if not allowed:
        return jsonify({'success': False, 'message': err}), 403

    events = cfg.get('academic_calendar', [])
    target = next((e for e in events if e.get('id') == evt_id), None)
    if not target:
        return jsonify({'success': False, 'message': 'Calendar event not found.'}), 404

    if request.method == 'DELETE':
        events.remove(target)
        _log_audit(cfg, caller, "Academic Calendar", "delete_event", target.get('title'), None, notes=f"Removed calendar event '{target.get('title')}'")
        _save_config(cfg)
        return jsonify({'success': True, 'message': f"Event '{target.get('title')}' deleted."})

    # PUT update
    data = request.get_json() or {}
    prev_val = json.dumps(target)
    target.update({k: v for k, v in data.items() if k not in ['id']})
    _log_audit(cfg, caller, "Academic Calendar", "update_event", prev_val, json.dumps(target), notes=f"Updated calendar event '{target.get('title')}'")
    _save_config(cfg)
    return jsonify({'success': True, 'item': target, 'message': 'Calendar event updated.'})

# 7. Timetable Rules
@school_config_bp.route('/api/school-config/timetable-rules', methods=['GET', 'PUT'])
def handle_timetable_rules():
    cfg = _load_config()
    caller = _get_caller(request)
    if request.method == 'GET':
        return jsonify({'success': True, 'data': cfg.get('timetable_rules', {})})

    allowed, err = _check_permission(caller, 'timetable_rules', 'edit')
    if not allowed:
        return jsonify({'success': False, 'message': err}), 403

    data = request.get_json() or {}
    prev = cfg.get('timetable_rules', {})
    cfg['timetable_rules'] = data
    _log_audit(cfg, caller, "Timetable Rules", "update_rules", json.dumps(prev), json.dumps(data), notes="Updated scheduling constraints & maximum period allocations")
    _save_config(cfg)
    return jsonify({'success': True, 'data': cfg['timetable_rules'], 'message': 'Timetable scheduling rules updated.'})

# 8. Staff Policies
@school_config_bp.route('/api/school-config/staff-policies', methods=['GET', 'PUT'])
def handle_staff_policies():
    cfg = _load_config()
    caller = _get_caller(request)
    if request.method == 'GET':
        return jsonify({'success': True, 'data': cfg.get('staff_policies', {})})

    allowed, err = _check_permission(caller, 'staff_policies', 'edit')
    if not allowed:
        return jsonify({'success': False, 'message': err}), 403

    data = request.get_json() or {}
    prev = cfg.get('staff_policies', {})
    cfg['staff_policies'] = data
    _log_audit(cfg, caller, "Staff Policies", "update_policies", json.dumps(prev), json.dumps(data), notes="Updated staff teaching targets, attendance cutoff, and grade submission policies")
    _save_config(cfg)
    return jsonify({'success': True, 'data': cfg['staff_policies'], 'message': 'Staff & academic operational policies updated.'})

# 9. Permissions & Access
@school_config_bp.route('/api/school-config/permissions', methods=['GET', 'PUT'])
def handle_permissions():
    cfg = _load_config()
    caller = _get_caller(request)
    if request.method == 'GET':
        return jsonify({'success': True, 'data': cfg.get('permissions_matrix', {})})

    allowed, err = _check_permission(caller, 'permissions_access', 'edit')
    if not allowed:
        return jsonify({'success': False, 'message': err}), 403

    data = request.get_json() or {}
    prev = cfg.get('permissions_matrix', {})
    cfg['permissions_matrix'] = data
    _log_audit(cfg, caller, "Permissions & Access", "update_permissions", json.dumps(prev), json.dumps(data), notes="Modified role access permissions and assigned editor scopes")
    _save_config(cfg)
    return jsonify({'success': True, 'data': cfg['permissions_matrix'], 'message': 'Permissions matrix updated.'})

# 10. Audit Log
@school_config_bp.route('/api/school-config/audit-log', methods=['GET'])
def get_audit_log():
    cfg = _load_config()
    caller = _get_caller(request)
    allowed, err = _check_permission(caller, 'change_history', 'view')
    if not allowed:
        return jsonify({'success': False, 'message': err}), 403

    logs = cfg.get('audit_log', [])
    
    # Filter by section
    sec = request.args.get('section')
    if sec and sec != 'all':
        logs = [l for l in logs if l.get('section', '').lower() == sec.lower()]

    # Filter by query
    q = request.args.get('q', '').lower().strip()
    if q:
        logs = [l for l in logs if q in l.get('action', '').lower() or q in l.get('notes', '').lower() or q in l.get('userName', '').lower() or q in l.get('section', '').lower()]

    return jsonify({'success': True, 'data': logs, 'total': len(logs)})

# 11. Review & Approval Workflow
@school_config_bp.route('/api/school-config/approve-review', methods=['POST'])
def approve_review():
    cfg = _load_config()
    caller = _get_caller(request)
    if caller['role'] not in ['admin', 'principal']:
        return jsonify({'success': False, 'message': 'Only Administrators and Principals can approve configuration revisions.'}), 403

    data = request.get_json() or {}
    rev_id = data.get('reviewId')
    reviews = cfg.get('pending_reviews', [])
    rev = next((r for r in reviews if r.get('id') == rev_id), None)
    if not rev:
        return jsonify({'success': False, 'message': 'Pending review record not found.'}), 404

    # Execute action
    action = rev.get('action')
    if action == 'activate_year':
        year_id = rev.get('targetId')
        years = cfg.get('school_years', [])
        target = next((y for y in years if y.get('id') == year_id), None)
        if target:
            for y in years:
                y['isCurrent'] = (y.get('id') == year_id)
                if y['isCurrent']:
                    y['status'] = 'active'
                elif y.get('status') == 'active':
                    y['status'] = 'completed'
            cfg.setdefault('general_settings', {})['academicYear'] = target.get('year')
            cfg.setdefault('timetable_rules', {})['activeAcademicYear'] = target.get('year')
            _sync_active_academic_year(target.get('id'), target.get('year'))

    rev['status'] = 'approved'
    rev['approvedBy'] = f"{caller['userId']} ({caller['userName']})"
    rev['approvedAt'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reviews.remove(rev)

    _log_audit(cfg, caller, rev.get('section', 'General'), "approve_revision", None, rev.get('details'), notes=f"Approved change request {rev_id}")
    _save_config(cfg)
    return jsonify({'success': True, 'message': f"Review request '{rev_id}' approved and applied to live school configuration."})

print("School Configuration API module initialized successfully.")

