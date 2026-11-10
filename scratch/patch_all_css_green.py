import glob
import re

css_files = [
    'assets/css/portal-dashboard.css',
    'assets/css/shared-components.css',
    'assets/css/hero.css',
    'assets/css/admin-view.css',
    'assets/css/bottom-nav.css',
    'assets/css/ui-states.css',
    'assets/css/ui-cleanup.css',
    'assets/css/interactions.css',
    'assets/css/announcements.css',
    'pages/admin/css/dashboard.css',
    'pages/shared/css/lessons.css',
] + glob.glob('pages/student/css/*.css')

replacements = [
    # Gradients
    ('linear-gradient(135deg, var(--color-midnight, #021024) 0%, var(--color-deep-blue, #052659) 100%)',
     'linear-gradient(135deg, #125638 0%, #176B45 100%)'),
    ('linear-gradient(135deg, #000000 0%, #021024 50%, #021024 100%)',
     'linear-gradient(135deg, #125638 0%, #176B45 100%)'),
    ('linear-gradient(135deg, #052659, #021024)', 'linear-gradient(135deg, #125638, #176B45)'),
    ('linear-gradient(135deg, #052659, #052659)', 'linear-gradient(135deg, #125638, #176B45)'),

    # Color variables
    ('var(--color-midnight, #021024)', '#176B45'),
    ('var(--color-deep-blue, #052659)', '#176B45'),
    ('var(--color-royal-blue, #052659)', '#176B45'),
    ('var(--color-light-blue, #C1E8FF)', '#E8F3ED'),
    ('var(--color-pale-blue, #EAF6FF)', '#F7F9F7'),
    ('var(--color-steel-blue, #5483B3)', '#64746A'),
    ('var(--color-muted-blue, #7DA0CA)', '#8FA095'),

    # Direct hexes
    ('#DCE8F3', '#E1E9E3'),
    ('#dce8f3', '#e1e9e3'),
    ('#C1E8FF', '#E8F3ED'),
    ('#c1e8ff', '#e8f3ed'),
    ('#052659', '#176B45'),
    ('#041d44', '#125638'),
    ('#5483B3', '#176B45'),
    ('#5483b3', '#176b45'),
    ('#7DA0CA', '#8FA095'),
    ('#7da0ca', '#8fa095'),
    ('#EAF6FF', '#F7F9F7'),
    ('#eaf6ff', '#f7f9f7'),
    ('#021024', '#29352E'),
]

for file_path in css_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        orig = content
        for src, dst in replacements:
            content = content.replace(src, dst)

        if content != orig:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Updated {file_path}')
        else:
            print(f'No changes for {file_path}')
    except Exception as e:
        print(f'Error reading {file_path}: {e}')

print('CSS patching finished.')

