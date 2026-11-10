with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace(
    '--sans: "Manrope", "Plus Jakarta Sans", "Inter", "Kantumruy Pro", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;',
    '--sans: "Manrope", "Plus Jakarta Sans", system-ui, -apple-system, sans-serif;'
)
c = c.replace(
    "font-family: 'Manrope', 'Inter', sans-serif;",
    "font-family: 'Manrope', 'Plus Jakarta Sans', sans-serif;"
)

with open('assets/css/app.css', 'w', encoding='utf-8') as f:
    f.write(c)

print('app.css clean!')

