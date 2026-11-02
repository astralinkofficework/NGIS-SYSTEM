import os, re

# 1. Update assets/css/app.css
app_path = r'assets/css/app.css'
with open(app_path, 'r', encoding='utf-8') as f:
    app_text = f.read()

# Replace .sidebar dark background
app_text = re.sub(
    r'\.sidebar\s*\{[^}]*background:\s*#0b1a30\s*!important;[^}]*\}',
    '''.sidebar {
  width: var(--sidebar-w); flex-shrink: 0;
  background: var(--token-surface, #ffffff) !important;
  border-right: 1px solid var(--token-border, #E5EAF2) !important;
  display: flex; flex-direction: column;
  position: fixed; inset: 0 auto 0 0; z-index: 60;
  transition: transform .28s cubic-bezier(.4,0,.2,1), width .28s cubic-bezier(.4,0,.2,1);
  color: var(--token-text-primary, #243247) !important;
  box-shadow: none !important;
  user-select: none;
}''',
    app_text
)

# Replace .side-brand block in app.css
side_brand_pattern = re.compile(
    r'/\* Brand header \*/\s*\.side-brand\s*\{.*?\.\.\.\s*\}|\.side-brand\s*\{[^}]*background:\s*#0b1a30;[^}]*\}',
    re.DOTALL
)

app_text = re.sub(
    r'\.side-brand\s*\{[^}]*background:\s*#0b1a30;[^}]*\}',
    '''.side-brand {
  height: 72px; min-height: 72px; padding: 0 16px; flex-shrink: 0;
  display: flex; align-items: center; justify-content: space-between; gap: 12px;
  border-bottom: 1px solid var(--token-border, #E5EAF2) !important;
  background: var(--token-surface, #ffffff) !important;
}''',
    app_text
)

# Replace side-brand-name and side-brand-school colors in app.css
app_text = re.sub(
    r'\.side-brand-name\s*\{[^}]*color:\s*#ffffff;[^}]*\}',
    '''.side-brand-name {
  font-size: 18px; font-weight: 500; color: var(--token-text-primary, #243247) !important; letter-spacing: -0.01em;
  font-family: 'Inter', -apple-system, sans-serif;
}''',
    app_text
)

app_text = re.sub(
    r'\.side-brand-school\s*\{[^}]*color:\s*#94a3b8;[^}]*\}',
    '''.side-brand-school {
  font-size: 10px; font-weight: 400; color: var(--token-text-muted, #64748B) !important;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  letter-spacing: -0.015em; margin-top: 1px;
}''',
    app_text
)

# Replace .sidebar-collapse-btn in app.css
app_text = re.sub(
    r'\.sidebar-collapse-btn\s*\{[^}]*border:\s*1px solid rgba\(255, 255, 255, 0\.1\)[^}]*\}',
    '''.sidebar-collapse-btn {
  width: 32px; height: 32px; flex-shrink: 0;
  display: none; align-items: center; justify-content: center;
  border: 1px solid var(--token-border, #E5EAF2) !important; border-radius: 8px;
  background: var(--token-surface, #ffffff) !important; color: var(--token-text-muted, #64748B) !important;
  cursor: pointer;
  transition: all 150ms ease;
  margin-left: auto;
  box-shadow: 0 1px 2px rgba(36, 50, 71, 0.04);
}''',
    app_text
)

app_text = re.sub(
    r'\.sidebar-collapse-btn:hover\s*\{[^}]*background:\s*rgba\(255, 255, 255, 0\.14\)[^}]*\}',
    '''.sidebar-collapse-btn:hover {
  background: var(--token-accent-soft, #EAF2FF) !important;
  color: var(--color-royal-blue, #2455D6) !important;
  border-color: var(--token-accent-border, #C9DEFF) !important;
  box-shadow: 0 2px 4px rgba(36, 85, 214, 0.12);
}''',
    app_text
)

# Replace .side-user-card in app.css
app_text = re.sub(
    r'\.side-user-card\s*\{[^}]*background:\s*rgba\(255, 255, 255, 0\.04\);[^}]*\}',
    '''.side-user-card {
  display: flex; align-items: center; gap: 12px;
  padding: 10px 14px; margin: 12px 14px 4px 14px;
  background: var(--token-surface-subtle, #F2F6FC) !important;
  border: 1px solid var(--token-border, #E5EAF2) !important;
  border-radius: 12px;
  cursor: pointer;
  transition: background 0.2s ease, border-color 0.2s ease;
  user-select: none;
  flex-shrink: 0;
}''',
    app_text
)

app_text = re.sub(
    r'\.side-user-card:hover\s*\{[^}]*background:\s*rgba\(255, 255, 255, 0\.08\);[^}]*\}',
    '''.side-user-card:hover {
  background: var(--token-accent-soft, #EAF2FF) !important;
  border-color: var(--token-accent-border, #C9DEFF) !important;
}''',
    app_text
)

app_text = re.sub(
    r'\.side-user-name\s*\{[^}]*color:\s*#ffffff;[^}]*\}',
    '''.side-user-name {
  font-size: 13.5px; font-weight: 500; color: var(--token-text-primary, #243247) !important;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  letter-spacing: -0.01em; line-height: 1.25;
}''',
    app_text
)

app_text = re.sub(
    r'\.side-user-role\s*\{[^}]*color:\s*#94a3b8;[^}]*\}',
    '''.side-user-role {
  font-size: 11px; font-weight: 400; color: var(--token-text-muted, #64748B) !important;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  line-height: 1.2; margin-top: 1px;
}''',
    app_text
)

with open(app_path, 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(app_text)
print("Updated app.css")


# 2. Update assets/css/interactions.css
inter_path = r'assets/css/interactions.css'
with open(inter_path, 'r', encoding='utf-8') as f:
    inter_text = f.read()

# Replace the explicit restoration for sidebar collapse button
old_collapse_rule = '''html body .sidebar-collapse-btn,
html body #sidebarCollapseBtn {
border: 1px solid rgba(255, 255, 255, 0.1) !important;
background: rgba(255, 255, 255, 0.06) !important;
color: #94a3b8 !important;
border-radius: 8px !important;
}'''

new_collapse_rule = '''html body .sidebar-collapse-btn,
html body #sidebarCollapseBtn {
border: 1px solid var(--token-border, #E5EAF2) !important;
background: var(--token-surface, #ffffff) !important;
color: var(--token-text-muted, #64748B) !important;
border-radius: 8px !important;
box-shadow: 0 1px 2px rgba(36, 50, 71, 0.04) !important;
}'''

if old_collapse_rule in inter_text:
    inter_text = inter_text.replace(old_collapse_rule, new_collapse_rule)
    print("Updated collapse rule in interactions.css")
else:
    # Try regex
    inter_text = re.sub(
        r'html body \.sidebar-collapse-btn,\s*html body #sidebarCollapseBtn\s*\{[^}]*\}',
        new_collapse_rule,
        inter_text
    )
    print("Updated collapse rule in interactions.css via regex")

old_hover_rule = '''html body .sidebar-collapse-btn:hover,
html body #sidebarCollapseBtn:hover {
border-color: rgba(255, 255, 255, 0.22) !important;
background: rgba(255, 255, 255, 0.14) !important;
color: #ffffff !important;
box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3) !important;
}'''

new_hover_rule = '''html body .sidebar-collapse-btn:hover,
html body #sidebarCollapseBtn:hover {
border-color: var(--token-accent-border, #C9DEFF) !important;
background: var(--token-accent-soft, #EAF2FF) !important;
color: var(--color-royal-blue, #2455D6) !important;
box-shadow: 0 2px 4px rgba(36, 85, 214, 0.12) !important;
}'''

if old_hover_rule in inter_text:
    inter_text = inter_text.replace(old_hover_rule, new_hover_rule)
    print("Updated collapse hover rule in interactions.css")
else:
    inter_text = re.sub(
        r'html body \.sidebar-collapse-btn:hover,\s*html body #sidebarCollapseBtn:hover\s*\{[^}]*\}',
        new_hover_rule,
        inter_text
    )
    print("Updated collapse hover rule in interactions.css via regex")

with open(inter_path, 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(inter_text)
print("Updated interactions.css")


# 3. Add explicit rules in assets/css/shared-components.css
sc_path = r'assets/css/shared-components.css'
with open(sc_path, 'r', encoding='utf-8') as f:
    sc_text = f.read()

side_brand_tokens_rule = '''
/* ── Sidebar Brand Header & Collapse Control (Invo Reference UI) ─ */
.side-brand,
#sidebar .side-brand,
.sidebar .side-brand {
  height: 72px !important;
  min-height: 72px !important;
  padding: 0 16px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 12px !important;
  background: var(--token-surface, #ffffff) !important;
  border-bottom: 1px solid var(--token-border, #E5EAF2) !important;
}

.side-brand-info,
#sidebar .side-brand-info,
.sidebar .side-brand-info {
  display: flex !important;
  align-items: center !important;
  gap: 12px !important;
  min-width: 0 !important;
  text-decoration: none !important;
  flex: 1 !important;
}

.side-brand-crest,
#sidebar .side-brand-crest,
.sidebar .side-brand-crest {
  width: 40px !important;
  height: 40px !important;
  border-radius: 50% !important;
  flex-shrink: 0 !important;
  object-fit: cover !important;
  display: block !important;
  border: 1px solid var(--token-border, #E5EAF2) !important;
  box-shadow: 0 1px 3px rgba(36, 50, 71, 0.08) !important;
}

.side-brand-titles,
#sidebar .side-brand-titles,
.sidebar .side-brand-titles {
  display: flex !important;
  flex-direction: column !important;
  min-width: 0 !important;
  line-height: 1.25 !important;
}

.side-brand-name,
#sidebar .side-brand-name,
.sidebar .side-brand-name {
  font-size: 17px !important;
  font-weight: 500 !important;
  color: var(--token-text-primary, #243247) !important;
  letter-spacing: -0.01em !important;
  font-family: var(--token-font-family, 'Inter', -apple-system, sans-serif) !important;
}

.side-brand-school,
#sidebar .side-brand-school,
.sidebar .side-brand-school {
  font-size: 10.5px !important;
  font-weight: 400 !important;
  color: var(--token-text-muted, #64748B) !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  letter-spacing: -0.015em !important;
  margin-top: 1px !important;
}

.sidebar-collapse-btn,
#sidebarCollapseBtn,
#sidebar .sidebar-collapse-btn,
.sidebar .sidebar-collapse-btn {
  width: 32px !important;
  height: 32px !important;
  flex-shrink: 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  border: 1px solid var(--token-border, #E5EAF2) !important;
  border-radius: 8px !important;
  background: var(--token-surface, #ffffff) !important;
  color: var(--token-text-muted, #64748B) !important;
  cursor: pointer !important;
  transition: all 150ms ease !important;
  box-shadow: 0 1px 2px rgba(36, 50, 71, 0.04) !important;
}

.sidebar-collapse-btn:hover,
#sidebarCollapseBtn:hover,
#sidebar .sidebar-collapse-btn:hover,
.sidebar .sidebar-collapse-btn:hover {
  background: var(--token-accent-soft, #EAF2FF) !important;
  border-color: var(--token-accent-border, #C9DEFF) !important;
  color: var(--color-royal-blue, #2455D6) !important;
  box-shadow: 0 2px 4px rgba(36, 85, 214, 0.12) !important;
  transform: none !important;
}

.side-collapse-svg,
#sidebar .side-collapse-svg,
.sidebar .side-collapse-svg {
  width: 15px !important;
  height: 15px !important;
  stroke: currentColor !important;
  stroke-width: 2 !important;
  stroke-linecap: round !important;
  stroke-linejoin: round !important;
  fill: none !important;
  display: block !important;
  pointer-events: none !important;
  flex-shrink: 0 !important;
}

/* User Profile Card in Sidebar */
.side-user-card,
#sidebar .side-user-card,
.sidebar .side-user-card {
  display: flex !important;
  align-items: center !important;
  gap: 12px !important;
  padding: 10px 14px !important;
  margin: 12px 14px 4px 14px !important;
  background: var(--token-surface-subtle, #F2F6FC) !important;
  border: 1px solid var(--token-border, #E5EAF2) !important;
  border-radius: 12px !important;
  cursor: pointer !important;
  transition: background 0.2s ease, border-color 0.2s ease !important;
}

.side-user-card:hover,
#sidebar .side-user-card:hover,
.sidebar .side-user-card:hover {
  background: var(--token-accent-soft, #EAF2FF) !important;
  border-color: var(--token-accent-border, #C9DEFF) !important;
}

.side-user-name,
#sidebar .side-user-name,
.sidebar .side-user-name {
  font-size: 13.5px !important;
  font-weight: 500 !important;
  color: var(--token-text-primary, #243247) !important;
}

.side-user-role,
#sidebar .side-user-role,
.sidebar .side-user-role {
  font-size: 11px !important;
  font-weight: 400 !important;
  color: var(--token-text-muted, #64748B) !important;
}

.side-user-avatar,
#sidebar .side-user-avatar,
.sidebar .side-user-avatar {
  background: var(--token-accent-soft, #EAF2FF) !important;
  color: var(--color-royal-blue, #2455D6) !important;
  border: 1px solid var(--token-accent-border, #C9DEFF) !important;
}

/* Dark Theme Overrides for Sidebar Brand */
[data-theme="dark"] .side-brand,
[data-theme="dark"] #sidebar .side-brand {
  background: #0f172a !important;
  border-bottom: 1px solid #1e293b !important;
}
[data-theme="dark"] .side-brand-name,
[data-theme="dark"] #sidebar .side-brand-name {
  color: #F8FAFC !important;
}
[data-theme="dark"] .side-brand-school,
[data-theme="dark"] #sidebar .side-brand-school {
  color: #94A3B8 !important;
}
[data-theme="dark"] .sidebar-collapse-btn,
[data-theme="dark"] #sidebarCollapseBtn {
  background: #1e293b !important;
  border-color: #334155 !important;
  color: #94A3B8 !important;
}
[data-theme="dark"] .sidebar-collapse-btn:hover,
[data-theme="dark"] #sidebarCollapseBtn:hover {
  background: #2455D6 !important;
  color: #FFFFFF !important;
  border-color: #2455D6 !important;
}
[data-theme="dark"] .side-user-card,
[data-theme="dark"] #sidebar .side-user-card {
  background: #1e293b !important;
  border-color: #334155 !important;
}
[data-theme="dark"] .side-user-name,
[data-theme="dark"] #sidebar .side-user-name {
  color: #F8FAFC !important;
}
[data-theme="dark"] .side-user-role,
[data-theme="dark"] #sidebar .side-user-role {
  color: #94A3B8 !important;
}
'''

if '.side-brand,' not in sc_text:
    sc_text += side_brand_tokens_rule
    with open(sc_path, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(sc_text)
    print("Added side-brand tokens rule to shared-components.css")
else:
    print("shared-components.css already has side-brand rules")

print("All side-brand color fixes successfully applied!")

