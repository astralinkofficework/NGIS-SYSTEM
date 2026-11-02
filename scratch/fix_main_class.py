for filepath in ['pages/teacher/teacher-lost-found.html', 'pages/teacher/teacher-services.html']:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<main class="app-main' in content:
        content = content.replace('<main class="app-main', '<main class="main')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath} to use <main class=\"main\">")
    else:
        print(f"No app-main found in {filepath}")

