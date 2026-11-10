import glob
import re

html_files = glob.glob('**/*.html', recursive=True)

# Replacements list, ordered from specific to general
replacements = [
    # Tailwind arbitrary classes & inline styles
    ('focus:ring-[#052659]', 'focus:ring-[#176B45]'),
    ('focus:border-[#052659]', 'focus:border-[#176B45]'),
    ('focus:ring-[#021024]', 'focus:ring-[#176B45]'),
    ('focus:border-[#021024]', 'focus:border-[#176B45]'),
    ('accent-[#052659]', 'accent-[#176B45]'),
    ('accent-[#021024]', 'accent-[#176B45]'),
    
    ('text-[#021024]', 'text-[#29352E]'),
    ('hover:text-[#021024]', 'hover:text-[#176B45]'),
    ('text-[#052659]', 'text-[#176B45]'),
    ('hover:text-[#052659]', 'hover:text-[#125638]'),
    ('text-[#5483B3]', 'text-[#64746A]'),
    ('text-[#5483b3]', 'text-[#64746A]'),
    ('text-[#7DA0CA]', 'text-[#8FA095]'),
    ('text-[#7da0ca]', 'text-[#8fa095]'),
    ('text-[#C1E8FF]', 'text-[#176B45]'),
    ('text-[#c1e8ff]', 'text-[#176B45]'),

    ('border-[#DCE8F3]', 'border-[#E1E9E3]'),
    ('border-[#dce8f3]', 'border-[#e1e9e3]'),
    ('border-[#052659]', 'border-[#176B45]'),
    ('border-[#021024]', 'border-[#176B45]'),
    ('border-[#5483B3]', 'border-[#E1E9E3]'),
    ('border-[#C1E8FF]', 'border-[#E8F3ED]'),
    ('border-[#EAF6FF]', 'border-[#EEF4F0]'),
    
    ('hover:bg-[#021024]', 'hover:bg-[#125638]'),
    ('hover:bg-[#052659]', 'hover:bg-[#125638]'),
    ('bg-[#052659]', 'bg-[#176B45]'),
    ('bg-[#021024]', 'bg-[#176B45]'),
    ('bg-[#C1E8FF]', 'bg-[#E8F3ED]'),
    ('bg-[#c1e8ff]', 'bg-[#e8f3ed]'),
    ('bg-[#EAF6FF]', 'bg-[#F7F9F7]'),
    ('bg-[#eaf6ff]', 'bg-[#f7f9f7]'),

    # Direct hexes in styles or scripts
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

updated_count = 0
for path in html_files:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        orig = content
        for src, dst in replacements:
            content = content.replace(src, dst)

        if content != orig:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            updated_count += 1
            print(f'Updated {path}')
    except Exception as e:
        print(f'Error processing {path}: {e}')

print(f'Done. Total HTML files updated: {updated_count}')

