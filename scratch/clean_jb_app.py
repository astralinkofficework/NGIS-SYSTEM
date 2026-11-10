with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace(
    '--mono: ui-monospace, "SF Mono", "JetBrains Mono", Menlo, Consolas, monospace;',
    '--mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;'
)

with open('assets/css/app.css', 'w', encoding='utf-8') as f:
    f.write(c)

print('Cleaned mono in app.css')

