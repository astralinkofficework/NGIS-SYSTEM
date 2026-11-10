import glob

for path in sorted(glob.glob('**/*', recursive=True)):
    if 'node_modules' in path or '.git' in path or 'scratch' in path:
        continue
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        if 'faculty records cleared' in content or 'academic departments covered' in content or 'Released to student transcripts' in content:
            print(f"MATCH: {path}")
    except:
        pass

