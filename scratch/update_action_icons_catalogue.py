import re

with open('assets/js/action-icons.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Add to PATHS:
# home, dashboard, attendance, grades, timetable, classes, documents, message
new_paths = '''    /* Core navigation & Flaticon mapping additions */
    home: '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>',
    dashboard: '<rect x="3" y="3" width="7" height="9" rx="1"/><rect x="14" y="3" width="7" height="5" rx="1"/><rect x="14" y="12" width="7" height="9" rx="1"/><rect x="3" y="16" width="7" height="5" rx="1"/>',
    attendance: '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
    grades: '<path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/><path d="M9 14l2 2 4-4"/>',
    timetable: '<rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="M8 14h.01"/><path d="M12 14h.01"/><path d="M16 14h.01"/>',
    classes: '<path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>',
    documents: '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>',
    message: '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',\n'''

if 'home:' not in content:
    content = content.replace("    /* Core action set */\n", "    /* Core action set */\n" + new_paths)
    print("Added new paths to assets/js/action-icons.js")
else:
    print("home already in assets/js/action-icons.js")

# Add additional aliases
new_aliases = '''    /* Master action mapping aliases */
    house: 'home', 'home-page': 'home', main: 'home',
    overview: 'dashboard', board: 'dashboard',
    gradebook: 'grades', scoring: 'grades',
    schedule: 'timetable', routine: 'timetable',
    roster: 'users', enrolled: 'users',
    student: 'user', teacher: 'user', principal: 'user', admin: 'shield',\n'''

if 'house:' not in content:
    content = content.replace("  var ALIASES = {\n", "  var ALIASES = {\n" + new_aliases)
    print("Added new aliases to assets/js/action-icons.js")

with open('assets/js/action-icons.js', 'w', encoding='utf-8') as f:
    f.write(content)

