with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

target1 = "TEACHER_EDITABLE_FIELDS = ('name', 'subject', 'department', 'email', 'role', 'status', 'classesAssigned', 'yearsAtSchool', 'phone', 'employmentType', 'contractEnd')"
print("Found target1:", target1 in text)

target2 = """    for k in TEACHER_EDITABLE_FIELDS:
        if k not in data:
            continue
        val = data[k]
        if k in ('classesAssigned', 'yearsAtSchool'):
            try:
                val = int(val or 0)
            except (TypeError, ValueError):
                return _academic_error('BAD_NUMBER', 'classesAssigned and yearsAtSchool must be whole numbers')
        else:
            val = str(val or '').strip()
            if not val:
                return _academic_error('EMPTY_FIELD', 'Field "%s" cannot be blank' % k)
        if str(val) != str(teacher.get(k)):
            changes[k] = val"""

# Let's inspect exact indentation
idx = text.find("TEACHER_EDITABLE_FIELDS =")
print(text[idx:idx+300])

idx2 = text.find("for k in TEACHER_EDITABLE_FIELDS:")
print(text[idx2:idx2+600])

