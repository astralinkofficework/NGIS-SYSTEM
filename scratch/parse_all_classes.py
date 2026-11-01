import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_sheets.json', 'r', encoding='utf-8') as f:
    raw_sheets = json.load(f)

# Helper to check if string contains Khmer
def has_khmer(s):
    return any('\u1780' <= c <= '\u17ff' for c in str(s))

def is_khmer_gender(s):
    s = str(s).strip()
    return s in ['ស្រី', 'ប្រុស', 'F', 'M']

# Let's inspect each of the 25 classes
class_sheet_names = [
    'ម.ត ក រសៀល',
    'ម.ត ខ រសៀល',
    '១ក វេនព្រឹក',
    '១ខ រសៀល',
    '២ខ រសៀល',
    '២ក រសៀល',
    '២គ រសៀល',
    '៣ក ព្រឹក',
    '៣ខ\u200b រសៀល',
    '៣គ រសៀល',
    '៤ក ព្រឹក',
    '៤ខ រសៀល',
    '4គ ព្រឹក',
    '៥ក ព្រឹក',
    '៥ខ រសៀល',
    '៦ក ព្រឹក',
    '៦ខ រសៀល',
    '៧ក ព្រឹក',
    '៧ខ រសៀល',
    '៨ក ព្រឹក',
    '៨ខ រសៀល',
    '៩ក ព្រឹក',
    '១០ក ព្រឹក',
    '១១ក ព្រឹក',
    '១២ក ព្រឹក',
]

def parse_class_sheet(sheet_name, rows):
    # Find teacher, room, time
    teacher = ""
    room = ""
    time_slot = ""
    class_title = ""
    month = "January"
    
    header_row_idx = -1
    date_row_idx = -1
    
    for r_idx, r in enumerate(rows[:10]):
        line_text = " ".join([str(c) for c in r['cells'] if str(c).strip()])
        if "បញ្ជីសម្រង់វត្តមានសិស្ស" in line_text:
            pass
        if "January" in line_text or "មករា" in line_text:
            month = "January"
        if "ថ្នាក់" in line_text and not ("គ្រូ" in line_text or "Nº" in line_text):
            for c in r['cells']:
                if "ថ្នាក់" in str(c):
                    class_title = str(c).strip()
                    break
        if "គ្រូ" in line_text:
            # parse teacher, room, time
            full_str = line_text
            m_teacher = re.search(r'គ្រូ\s*[:ៈ]\s*([^\|,\n]+)', full_str)
            if m_teacher:
                teacher = m_teacher.group(1).strip()
            m_room = re.search(r'បន្ទប់[់]*\s*[:ៈ]\s*([^\|,\n]+)', full_str)
            if m_room:
                room = m_room.group(1).strip()
            m_time = re.search(r'(?:Time:?\s*)?(\d{1,2}:\d{2}\s*-\s*\d{1,2}:\d{2}(?:\s*(?:am|pm|Am|Pm))?)', full_str)
            if m_time:
                time_slot = m_time.group(1).strip()

        # Check if this row is the header row
        for c_idx, c in enumerate(r['cells']):
            if str(c).strip() in ['Nº', 'No', 'No.', 'ល.រ']:
                header_row_idx = r_idx
                break
            if 'ឈ្មោះជាអក្សរឡាតាំង' in str(c) or 'គោត្តនាម' in str(c):
                header_row_idx = r_idx
                break

    # If class_title not found, use sheet_name
    if not class_title:
        class_title = sheet_name

    # Now look for date row
    # The date row usually comes right after or near header_row_idx
    # It has numbers like 2.0, 3.0, 6.0, ...
    if header_row_idx != -1:
        # Check header_row_idx + 1 or header_row_idx
        for offset in [1, 0, 2]:
            candidate_idx = header_row_idx + offset
            if candidate_idx < len(rows):
                candidate_row = rows[candidate_idx]['cells']
                # Check how many numeric date values it has
                nums = []
                for c_idx, val in enumerate(candidate_row):
                    try:
                        v = float(val)
                        if 1 <= v <= 31:
                            nums.append((c_idx, int(v)))
                    except:
                        pass
                if len(nums) >= 10:
                    date_row_idx = candidate_idx
                    break

    # Find date columns
    dates = []
    if date_row_idx != -1:
        date_cells = rows[date_row_idx]['cells']
        # Also check weekday names from previous row if applicable
        weekday_cells = rows[date_row_idx - 1]['cells'] if date_row_idx > 0 else []
        for c_idx, val in enumerate(date_cells):
            try:
                v = float(val)
                if 1 <= v <= 31:
                    day_num = int(v)
                    day_name = ""
                    if c_idx < len(weekday_cells):
                        day_name = str(weekday_cells[c_idx]).strip()
                    dates.append({'col': c_idx, 'dayNumber': day_num, 'dayName': day_name})
            except:
                pass

    # Find columns for student info
    col_no = 0
    col_name_latin = -1
    col_name_khmer = -1
    col_gender = -1
    col_parent = -1
    col_dob = -1
    col_id = -1
    col_class = -1

    if header_row_idx != -1:
        hcells = rows[header_row_idx]['cells']
        for c_idx, val in enumerate(hcells):
            sval = str(val).strip()
            if sval in ['Nº', 'No', 'No.', 'ល.រ']:
                col_no = c_idx
            elif 'ឡាតាំង' in sval or "Student's Name" in sval:
                col_name_latin = c_idx
            elif 'គោត្តនាម' in sval or 'Khmer Name' in sval:
                col_name_khmer = c_idx
            elif 'ភេទ' in sval or 'Sex' in sval:
                col_gender = c_idx
            elif 'Parent' in sval or 'Contact' in sval:
                col_parent = c_idx
            elif 'កំណើត' in sval or 'DOB' in sval:
                col_dob = c_idx
            elif 'អត្តលេខ' in sval or 'ID No' in sval:
                col_id = c_idx
            elif 'ថ្នាក់' in sval or 'Class' in sval:
                col_class = c_idx

    # If column indices were not found from header, use standard defaults
    # In most sheets: col0: No, col1: Name1, col2: Name2, col3: Gender, col4: Parent, col5: DOB, col6: ID
    if col_gender == -1:
        col_gender = 3
    if col_name_latin == -1 and col_name_khmer == -1:
        col_name_latin = 1
        col_name_khmer = 2

    # Now parse students
    students = []
    start_row = (date_row_idx if date_row_idx != -1 else header_row_idx) + 1
    # Check if there is another subheader row like "Contact, អង់គ្លេស, ចិន"
    if start_row < len(rows):
        sub_text = " ".join([str(c) for c in rows[start_row]['cells'] if str(c).strip()])
        if "Contact" in sub_text or "អង់គ្លេស" in sub_text or "Week" in sub_text:
            start_row += 1

    for r_idx in range(start_row, len(rows)):
        r = rows[r_idx]['cells']
        if not r or len(r) == 0:
            continue
        first_col = str(r[0]).strip() if len(r) > 0 else ''
        first_few = " ".join([str(c) for c in r[:5] if str(c).strip()])
        if "Total" in first_few or "សរុប" in first_few or "SUMMARY" in first_few or "Female" in first_few or "ស្រី" in first_few:
            break
        
        # Check if row has a student number or name
        try:
            student_no = int(float(first_col)) if first_col else len(students) + 1
        except:
            if not any(r):
                continue
            student_no = len(students) + 1

        val1 = r[col_name_latin] if col_name_latin < len(r) else ""
        val2 = r[col_name_khmer] if col_name_khmer < len(r) else ""

        # Determine which is latin and which is khmer
        if has_khmer(val1) and not has_khmer(val2):
            name_kh = val1
            name_en = val2
        elif has_khmer(val2) and not has_khmer(val1):
            name_kh = val2
            name_en = val1
        elif has_khmer(val1):
            name_kh = val1
            name_en = ""
        else:
            name_en = val1
            name_kh = val2

        if not name_en and not name_kh:
            continue

        gender = ""
        if col_gender < len(r):
            g_raw = str(r[col_gender]).strip()
            if g_raw in ['ស្រី', 'F', 'Female']:
                gender = 'F'
            elif g_raw in ['ប្រុស', 'M', 'Male']:
                gender = 'M'

        dob = str(r[col_dob]).strip() if col_dob != -1 and col_dob < len(r) else ""
        student_id = str(r[col_id]).strip() if col_id != -1 and col_id < len(r) else ""
        parent = str(r[col_parent]).strip() if col_parent != -1 and col_parent < len(r) else ""

        # Now extract daily attendance
        attendance_map = {}
        pres_count = 0
        late_count = 0
        abs_count = 0
        perm_count = 0

        for d in dates:
            c_idx = d['col']
            day_num = d['dayNumber']
            mark = str(r[c_idx]).strip() if c_idx < len(r) else ""
            if mark in ['√', 'P', '1', '✓']:
                standard_mark = '√'
                pres_count += 1
            elif mark in ['ច', 'E', 'p', 'P']:
                standard_mark = 'ច'
                perm_count += 1
            elif mark in ['យ', 'L', 'l']:
                standard_mark = 'យ'
                late_count += 1
            elif mark in ['អ', 'A', 'a']:
                standard_mark = 'អ'
                abs_count += 1
            elif mark:
                standard_mark = mark
            else:
                standard_mark = ""
            
            attendance_map[str(day_num)] = standard_mark

        total_sessions = len(dates)
        attended = pres_count + late_count + perm_count
        rate = round((attended / total_sessions * 100), 1) if total_sessions > 0 else 100.0

        students.append({
            'no': student_no,
            'id': student_id or f"NGIS-{len(students)+1:03d}",
            'name_en': name_en.strip(),
            'name_kh': name_kh.strip(),
            'gender': gender or 'M',
            'dob': dob,
            'parent': parent,
            'attendance': attendance_map,
            'stats': {
                'present': pres_count,
                'late': late_count,
                'absent': abs_count,
                'permission': perm_count,
                'rate': rate
            }
        })

    return {
        'sheet_name': sheet_name,
        'class_title': class_title,
        'teacher': teacher,
        'room': room,
        'time_slot': time_slot,
        'dates': dates,
        'students_count': len(students),
        'students': students
    }

parsed_classes = []
for sname in class_sheet_names:
    res = parse_class_sheet(sname, raw_sheets[sname])
    parsed_classes.append(res)
    print(f"Parsed {sname}: {res['class_title']} | Teacher: {res['teacher']} | Rm: {res['room']} | Time: {res['time_slot']} | Students: {res['students_count']} | Dates: {len(res['dates'])}")

with open('scratch/parsed_classes_test.json', 'w', encoding='utf-8') as out:
    json.dump(parsed_classes, out, ensure_ascii=False, indent=2)
