import glob

terms = [
    'viewSwitcher',
    'Cambodian MoEYS Guidelines',
    'វិទ្យាល័យ ហ្គេតវេ',
    'Standard Cambodian National Curriculum'
]

for p in glob.glob('pages/**/*.html', recursive=True):
    with open(p, encoding='utf-8') as f:
        content = f.read()
    for t in terms:
        if t in content:
            print(f'HTML match "{t}" in {p}')
print("Done HTML check.")

