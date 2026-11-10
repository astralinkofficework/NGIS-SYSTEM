with open('assets/css/design-system.css', 'r', encoding='utf-8') as f:
    text = f.read()

old_str = """html, body {
  background-color: var(--ngis-canvas) !important;
  color: var(--ngis-text-primary) !important;
  font-family: var(--font-primary) !important;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}"""

new_str = """html, body {
  background-color: var(--ngis-canvas) !important;
  color: var(--ngis-text-primary) !important;
  font-family: var(--font-primary) !important;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  overflow-x: hidden !important;
  max-width: 100vw;
}"""

if old_str in text:
    text = text.replace(old_str, new_str)
    with open('assets/css/design-system.css', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Updated design-system.css with overflow-x: hidden')
else:
    print('Target not found')

