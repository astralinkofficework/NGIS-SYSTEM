import re

path = "assets/css/app.css"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update .sidebar
content = re.sub(
    r'\.sidebar\s*\{[^}]*background:[^;]*;[^}]*color:[^;]*;[^}]*\}',
    '''.sidebar {
  width: var(--sidebar-w); flex-shrink: 0;
  background: var(--color-midnight, #021024) !important;
  border-right: 1px solid rgba(220, 232, 243, 0.12) !important;
  display: flex; flex-direction: column;
  position: fixed; inset: 0 auto 0 0; z-index: 60;
  transition: transform .28s cubic-bezier(.4,0,.2,1), width .28s cubic-bezier(.4,0,.2,1);
  color: #FFFFFF !important;
  box-shadow: none !important;
  user-select: none;
}''',
    content,
    flags=re.DOTALL
)

# 2. Update .side-brand
content = re.sub(
    r'\.side-brand\s*\{[^}]*\}',
    '''.side-brand {
  height: 72px; min-height: 72px; padding: 0 16px; flex-shrink: 0;
  display: flex; align-items: center; justify-content: space-between; gap: 12px;
  border-bottom: 1px solid rgba(220, 232, 243, 0.12) !important;
  background: var(--color-midnight, #021024) !important;
}''',
    content,
    flags=re.DOTALL
)

# 3. Update .side-brand-name and .side-brand-school
content = re.sub(
    r'\.side-brand-name\s*\{[^}]*\}',
    '''.side-brand-name {
  font-size: 18px; font-weight: 500; color: #FFFFFF !important; letter-spacing: -0.01em;
  font-family: 'Manrope', 'Inter', sans-serif;
}''',
    content,
    flags=re.DOTALL
)

content = re.sub(
    r'\.side-brand-school\s*\{[^}]*\}',
    '''.side-brand-school {
  font-size: 10px; font-weight: 400; color: var(--color-light-blue, #C1E8FF) !important;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  letter-spacing: -0.015em; margin-top: 1px;
}''',
    content,
    flags=re.DOTALL
)

# 4. Update .sidebar-collapse-btn
content = re.sub(
    r'\.sidebar-collapse-btn\s*\{[^}]*\}',
    '''.sidebar-collapse-btn {
  width: 32px; height: 32px; flex-shrink: 0;
  display: none; align-items: center; justify-content: center;
  border: 1px solid rgba(220, 232, 243, 0.2) !important; border-radius: 8px;
  background: rgba(193, 232, 255, 0.1) !important; color: var(--color-light-blue, #C1E8FF) !important;
  cursor: pointer;
  transition: all 150ms ease;
  margin-left: auto;
  box-shadow: none;
}''',
    content,
    flags=re.DOTALL
)

# 5. Update .nav-group-label
content = re.sub(
    r'\.nav-group-label\s*\{[^}]*color:[^;]*;[^}]*\}',
    '''.nav-group-label {
  display: flex; align-items: center; gap: 8px;
  padding: 10px 12px 4px 12px;
  font-size: 11px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em;
  color: var(--color-muted-blue, #7DA0CA) !important;
  border: none; background: transparent; width: 100%; text-align: left;
  user-select: none;
}''',
    content,
    flags=re.DOTALL
)

# 6. Update .nav-link, .nav-link-icon, .nav-link:hover, .nav-link.active
old_active_pattern = r'/\* Active State:.*?\*/\s*\.nav-link\.active,\s*\.sidebar \.nav-link\.active\s*\{[^}]*\}'
new_active_block = '''/* Active State: Light Blue #C1E8FF Container with Midnight Navy #021024 Text & Icon */
.nav-link.active,
.sidebar .nav-link.active,
.nav-group-label-link.active {
  background: var(--color-light-blue, #C1E8FF) !important;
  background-color: var(--color-light-blue, #C1E8FF) !important;
  border: 1px solid var(--color-light-blue, #C1E8FF) !important;
  border-radius: 10px !important;
  color: var(--color-midnight, #021024) !important;
  font-weight: 500 !important;
  box-shadow: none !important;
}
.nav-link.active .nav-link-icon,
.nav-link.active .nav-link-label,
.nav-link.active .nav-link-chevron,
.nav-link.active i,
.nav-link.active span,
.nav-group-label-link.active span {
  color: var(--color-midnight, #021024) !important;
}
.nav-link.active .pill {
  background: var(--color-deep-blue, #052659) !important;
  color: #FFFFFF !important;
}'''

match = re.search(old_active_pattern, content, re.DOTALL)
if match:
    content = content[:match.start()] + new_active_block + content[match.end():]
    print("Replaced .nav-link.active block!")
else:
    print("Could not match active pattern directly, checking alternative...")

# Ensure .nav-link defaults
content = re.sub(
    r'\.nav-link-icon\s*\{[^}]*color:[^;]*;[^}]*\}',
    '.nav-link-icon { font-size: 20px !important; color: var(--color-light-blue, #C1E8FF) !important; line-height: 1; flex-shrink: 0; transition: color 150ms ease; }',
    content
)

content = re.sub(
    r'\.nav-link\s*\{([^}]*?)color:\s*[^;]+;',
    r'.nav-link {\1color: rgba(255, 255, 255, 0.88) !important;',
    content,
    count=1
)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated assets/css/app.css successfully!")

