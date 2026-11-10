def clean_remaining():
    with open('pages/student/student-timetable.html', 'r', encoding='utf-8') as f:
        text = f.read()
    text = text.replace('👨\u200d🏫', '').replace('👨', '')
    with open('pages/student/student-timetable.html', 'w', encoding='utf-8') as f:
        f.write(text)

    with open('assets/js/khmer-suite-ui.js', 'r', encoding='utf-8') as f:
        ui_text = f.read()
    # Replace ✓ with Step Done icon or text
    ui_text = ui_text.replace("'✓'", "'<span class=\"material-symbols-outlined text-[13px]\">check</span>'")
    ui_text = ui_text.replace("'✕'", "'<span class=\"material-symbols-outlined text-[14px]\">close</span>'")
    ui_text = ui_text.replace(">✕<", "><span class=\"material-symbols-outlined text-[14px]\">close</span><")
    with open('assets/js/khmer-suite-ui.js', 'w', encoding='utf-8') as f:
        f.write(ui_text)

clean_remaining()
print('Cleaned remaining.')
