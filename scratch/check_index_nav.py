for path in ['index.html', 'pages-directory.html']:
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    print(f"=== {path} ===")
    start = text.find('<nav class="side-nav')
    end = text.find('</nav>', start)
    print(text[start:end+6])

