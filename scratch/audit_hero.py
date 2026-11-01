import glob, os

for f in sorted(glob.glob('pages/student/*.html')):
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    uses_local_hero = 'js/hero.js' in c and 'assets/js/hero.js' not in c
    uses_assets_hero = 'assets/js/hero.js' in c
    is_student_dash = 'student-dashboard' in c
    print(f'{os.path.basename(f)}: local_hero={uses_local_hero}, assets_hero={uses_assets_hero}, student-dashboard={is_student_dash}')

