with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'document.addEventListener("DOMContentLoaded"' in l or 'document.addEventListener(\'DOMContentLoaded\'' in l or 'window.addEventListener("DOMContentLoaded"' in l:
        print(f"Line {i+1}: {l.strip()}")
        for j in range(i, min(len(lines), i+40)):
            print(f"{j+1}: {lines[j].rstrip()}")
        break

