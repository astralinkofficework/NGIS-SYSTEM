for path in ['index.html', 'pages-directory.html']:
    print(f"=== {path} ===")
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    if '<aside' in content:
        start = content.find('<aside')
        end = content.find('</aside>', start) + 8
        print(content[start:end])

