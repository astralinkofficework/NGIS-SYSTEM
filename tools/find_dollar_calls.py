with open('assets/js/ngis-profiles.js', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        if "$('" in line or '$("' in line or '$id(' in line:
            if 'querySelector' in line or "$('" in line or '$("' in line:
                print(f"{i}: {line.strip()}")
