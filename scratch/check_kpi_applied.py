with open('pages/teacher/teacher-departments.html', 'r', encoding='utf-8') as f:
    text = f.read()

print('Has "3 Cohorts":', '3 Cohorts' in text)
print('Has "3 Active Cohorts":', '3 Active Cohorts' in text)

