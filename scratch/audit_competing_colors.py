import glob
import re
from collections import defaultdict

html_files = glob.glob('pages/**/*.html', recursive=True) + glob.glob('*.html')
js_files = glob.glob('assets/js/*.js')

print(f"Scanning for competing accent colors in HTML and JS...")

# Looking for purple, indigo, pink, violet, fuchsia, cyan, teal in non-timetable contexts
competing_colors = defaultdict(list)
competing_re = re.compile(r'\b(?:bg|text|border)-(purple|indigo|pink|violet|fuchsia|cyan)-[0-9]{2,3}\b')

for fpath in html_files + js_files:
    # exclude timetable matrix builder files where subjects are coded
    is_timetable = 'timetable' in fpath.lower()
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    matches = competing_re.findall(content)
    if matches:
        for m in matches:
            competing_colors[m].append((fpath, is_timetable))

print(f"\n--- COMPETING ACCENT FAMILIES FOUND ---")
for color_fam, occurrences in sorted(competing_colors.items(), key=lambda x: len(x[1]), reverse=True):
    tt_count = sum(1 for _, is_tt in occurrences if is_tt)
    non_tt_count = len(occurrences) - tt_count
    sample_files = list(set(fp for fp, is_tt in occurrences if not is_tt))[:4]
    print(f"  {color_fam:10}: {len(occurrences):3d} total ({tt_count} in timetable, {non_tt_count} elsewhere)")
    if sample_files:
        print(f"      Non-timetable files: {sample_files}")
