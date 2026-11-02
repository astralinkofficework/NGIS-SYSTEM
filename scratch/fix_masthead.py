with open('pages/teacher/teacher-classes.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = '<section class="bg-white dark:bg-slate-900 border-t border-slate-100 dark:border-slate-800/80 shadow-xs" data-purpose="workspace-masthead">'
replacement = '<section class="bg-transparent border-0 shadow-none" style="background: transparent !important; border: none !important; box-shadow: none !important;" data-purpose="workspace-masthead">'

if target in text:
    text = text.replace(target, replacement, 1)
    with open('pages/teacher/teacher-classes.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("SUCCESS: Updated workspace-masthead in teacher-classes.html!")
else:
    print("Target not found, checking with normalize...")
    target_norm = target.replace('\r\n', '\n')
    text_norm = text.replace('\r\n', '\n')
    if target_norm in text_norm:
        text_norm = text_norm.replace(target_norm, replacement, 1)
        with open('pages/teacher/teacher-classes.html', 'w', encoding='utf-8') as f:
            f.write(text_norm)
        print("SUCCESS with normalized newlines!")
    else:
        print("ERROR: Target not found")

