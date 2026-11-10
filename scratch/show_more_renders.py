with open('assets/js/school-information.js', 'r', encoding='utf-8') as f:
    text = f.read()

for name in ['renderAcademicYears', 'renderCampuses', 'renderBellSchedule', 'renderCalendar', 'renderDepartments']:
    pos = text.find(name + ' = function')
    print(f'=== {name} ===')
    print(text[pos:pos+500])

