import re

def strip_emojis_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Exact emoji characters to remove
    emojis = [
        '👁', '⚙', '💾', '🕘', '📥', '⚠️', '⚠', '✅', '📋', '❓', 
        '🔍', '📚', '📖', '🏫', '🗓️', '🗓', '🔄', '🗑️', '🗑', 
        '🔒', '🔓', '⚡', '🚀', '❌', '⌁', '👨‍🏫', '📍', '💡', '🎉'
    ]
    for em in emojis:
        text = text.replace(em + ' ', '')
        text = text.replace(em, '')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f'Stripped emojis from {filepath}')

strip_emojis_from_file('assets/js/khmer-suite-ui.js')
strip_emojis_from_file('pages/student/student-timetable.html')
strip_emojis_from_file('pages/teacher/teacher-timetable.html')
strip_emojis_from_file('pages/teacher/teacher-calendar.html')

