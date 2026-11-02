import glob

for cf in glob.glob('assets/css/*.css') + glob.glob('pages/**/css/*.css', recursive=True):
    with open(cf, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    if 'ov-task' in text:
        print(f"Found in {cf}")

