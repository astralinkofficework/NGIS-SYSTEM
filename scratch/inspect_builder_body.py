with open('pages/principal/principal-timetable-builder.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines[120:180]):
    print(f"{i+121}: {l.rstrip()}")

