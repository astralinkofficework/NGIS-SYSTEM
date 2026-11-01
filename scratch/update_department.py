import re

with open('pages/shared/department.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add phosphor icons script to head if not present
if '@phosphor-icons/web' not in content:
    content = content.replace(
        '<link rel="stylesheet" href="../../assets/css/design-system.css">',
        '<link rel="stylesheet" href="../../assets/css/design-system.css">\n<script src="https://unpkg.com/@phosphor-icons/web"></script>'
    )

# 2. Update body attributes
content = re.sub(r'<body data-page="department"[^>]*>', '<body data-page="department" data-role="student">', content)

# 3. Replace the inner headers & tabs block:
# Look for the block from `<nav class="hub-top-nav-bar"` down to `<div class="hub-grid"`
old_block_pattern = re.compile(
    r'<nav class="hub-top-nav-bar".*?<div class="hub-grid"',
    re.DOTALL
)

new_block = '''<div class="hub-top-nav-bar" aria-label="Department status">
        <div class="hub-term-badge">
          <span class="material-symbols-outlined">calendar_today</span>
          <span>Academic Year 2025–2026 · Term 2</span>
        </div>
      </div>

      <!-- ════════════════════════════════════════════════════════
           3-COLUMN CARDS GRID (1:1 with Reference Design)
           ════════════════════════════════════════════════════════ -->
      <div class="hub-grid"'''

content = old_block_pattern.sub(new_block, content)

# 4. Replace the style block
style_pattern = re.compile(r'<style>.*?</style>', re.DOTALL)
new_style = '''<style>
/* ═══════════════════════════════════════════════════════════════
   NGIS DEPARTMENT HUB — Clean Architecture & Brand System
   Charcoal Blue (#2F4550) · Blue Slate (#586F7C) · Light Blue (#B8DBD9)
   Font: Inter · Kantumruy Pro fallback
   ═══════════════════════════════════════════════════════════════ */

*, *::before, *::after {
  box-sizing: border-box !important;
  margin: 0;
  padding: 0;
}

:root {
  --hub-font: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --hub-card-bg: #ffffff;
  --hub-card-border: rgba(47, 69, 80, 0.12);
  --hub-card-border-hover: rgba(47, 69, 80, 0.28);
  --hub-icon-bg: rgba(184, 219, 217, 0.35);
  --hub-icon-border: rgba(184, 219, 217, 0.60);
  --hub-divider: rgba(47, 69, 80, 0.08);
}

html[data-theme="dark"], [data-theme="dark"] {
  --hub-card-bg: #182329;
  --hub-card-border: rgba(184, 219, 217, 0.18);
  --hub-card-border-hover: rgba(184, 219, 217, 0.38);
  --hub-icon-bg: rgba(184, 219, 217, 0.14);
  --hub-icon-border: rgba(184, 219, 217, 0.28);
  --hub-divider: rgba(184, 219, 217, 0.12);
}

html, body {
  margin: 0 !important;
  padding: 0 !important;
  width: 100% !important;
  max-width: 100vw !important;
  overflow-x: hidden !important;
  font-family: var(--hub-font) !important;
  background-color: var(--ghost-white, #f4f7fa);
}

html[data-theme="dark"] body, [data-theme="dark"] body,
html[data-theme="dark"] .main, [data-theme="dark"] .main,
html[data-theme="dark"] .page, [data-theme="dark"] .page {
  background-color: #0c121e !important;
  color: #e2e8f0 !important;
}

/* Strict Typography Constraint: NO BOLD FONTS */
* {
  font-weight: 400;
}
b, strong, th, h1, h2, h3, h4, h5, h6,
.font-bold, .font-extrabold, .font-semibold, .font-medium,
[class*="font-medium"] {
  font-weight: 500 !important;
}

/* Page Scaffolding */
.main {
  width: 100% !important;
  max-width: 100% !important;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  overflow-x: hidden !important;
}

.page {
  width: 100% !important;
  max-width: 100% !important;
  margin: 0 !important;
  padding: 20px 24px 80px !important;
  box-sizing: border-box !important;
  flex: 1;
}

/* Content Container */
.hub-content-container {
  width: 100% !important;
  max-width: 1200px !important;
  margin: 0 auto !important;
  padding: 0 !important;
  box-sizing: border-box !important;
}

/* Top Nav / Status Bar */
.hub-top-nav-bar {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  margin-bottom: 20px;
  gap: 12px;
}

.hub-term-badge {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  font-size: 12px;
  font-weight: 500;
  color: var(--charcoal-blue, #2f4550);
  background: #ffffff;
  border: 1px solid rgba(47, 69, 80, 0.12);
  padding: 6px 14px;
  border-radius: 999px;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
  letter-spacing: -0.01em;
  user-select: none;
}

[data-theme="dark"] .hub-term-badge {
  background: #182329;
  border-color: rgba(184, 219, 217, 0.22);
  color: var(--light-blue, #b8dbd9);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.35);
}

.hub-term-badge .material-symbols-outlined {
  font-size: 15px;
  color: var(--blue-slate, #586f7c);
}

[data-theme="dark"] .hub-term-badge .material-symbols-outlined {
  color: var(--light-blue, #b8dbd9);
}

/* ═══════════════════════════════════════════════════════════════
   HUB GRID — 3 Columns Responsive
   ═══════════════════════════════════════════════════════════════ */
.hub-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
  width: 100%;
}

/* ── Individual Hub Card ── */
.hub-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 200px;
  background: var(--hub-card-bg, #ffffff) !important;
  border: 1px solid var(--hub-card-border, rgba(47, 69, 80, 0.12)) !important;
  border-radius: 16px !important;
  padding: 18px 18px 15px;
  text-decoration: none !important;
  color: inherit !important;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04), 0 1px 2px rgba(15, 23, 42, 0.02) !important;
  transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  box-sizing: border-box !important;
}

.hub-card:hover {
  transform: translateY(-2px);
  border-color: var(--hub-card-border-hover, rgba(47, 69, 80, 0.28)) !important;
  box-shadow: 0 8px 20px -4px rgba(15, 23, 42, 0.08) !important;
}

/* Top Row: Icon Container + Metric Badge */
.hub-card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
  border: none !important;
  background: transparent !important;
}

.hub-card-icon {
  width: 40px;
  height: 40px;
  border-radius: 11px;
  background: var(--hub-icon-bg) !important;
  border: 1px solid var(--hub-icon-border) !important;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--charcoal-blue, #2f4550);
  flex-shrink: 0;
  box-shadow: none !important;
}

[data-theme="dark"] .hub-card-icon {
  color: var(--light-blue, #b8dbd9);
}

.hub-card-icon .material-symbols-outlined {
  font-size: 20px;
  line-height: 1;
}

/* Metric Pill Badges */
.hub-card-badge {
  display: inline-flex;
  align-items: center;
  font-size: 11.5px;
  font-weight: 500;
  color: var(--charcoal-blue, #2f4550);
  background: rgba(47, 69, 80, 0.06) !important;
  border: 1px solid rgba(47, 69, 80, 0.12) !important;
  padding: 3px 10px;
  border-radius: 999px !important;
  letter-spacing: -0.01em;
  user-select: none;
  box-shadow: none !important;
}

[data-theme="dark"] .hub-card-badge {
  color: var(--light-blue, #b8dbd9);
  background: rgba(184, 219, 217, 0.1) !important;
  border-color: rgba(184, 219, 217, 0.22) !important;
}

.hub-card-badge.badge-present {
  background: rgba(46, 111, 94, 0.08) !important;
  color: #2e6f5e !important;
  border-color: rgba(46, 111, 94, 0.22) !important;
}
[data-theme="dark"] .hub-card-badge.badge-present {
  background: rgba(107, 179, 159, 0.15) !important;
  color: #6bb39f !important;
  border-color: rgba(107, 179, 159, 0.3) !important;
}

.hub-card-badge.badge-due {
  background: rgba(140, 98, 43, 0.08) !important;
  color: #8c622b !important;
  border-color: rgba(140, 98, 43, 0.22) !important;
}
[data-theme="dark"] .hub-card-badge.badge-due {
  background: rgba(212, 167, 106, 0.15) !important;
  color: #d4a76a !important;
  border-color: rgba(212, 167, 106, 0.3) !important;
}

/* Middle: Title + Description */
.hub-card-body {
  flex: 1;
  margin-bottom: 16px;
  border: none !important;
  background: transparent !important;
}

.hub-card-title {
  font-size: 16px !important;
  font-weight: 500 !important;
  color: var(--charcoal-blue, #2f4550) !important;
  letter-spacing: -0.015em;
  line-height: 1.3;
  margin: 0 0 6px 0 !important;
  border: none !important;
  background: transparent !important;
}

[data-theme="dark"] .hub-card-title {
  color: #ffffff !important;
}

.hub-card-desc {
  font-size: 13px !important;
  font-weight: 400 !important;
  color: var(--blue-slate, #586f7c) !important;
  line-height: 1.5;
  margin: 0 !important;
  border: none !important;
  background: transparent !important;
}

[data-theme="dark"] .hub-card-desc {
  color: #9eb8b7 !important;
}

/* Bottom: Action Row & Chevron */
.hub-card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 13px;
  border-top: 1px solid var(--hub-divider) !important;
  border-left: none !important;
  border-right: none !important;
  border-bottom: none !important;
  background: transparent !important;
  border-radius: 0 !important;
  box-shadow: none !important;
  margin-top: auto;
}

.hub-card-action {
  font-size: 12.5px;
  font-weight: 500;
  color: var(--charcoal-blue, #2f4550);
  transition: color 0.18s ease;
}

[data-theme="dark"] .hub-card-action {
  color: var(--light-blue, #b8dbd9);
}

.hub-card-chevron {
  font-size: 18px !important;
  color: var(--blue-slate, #586f7c);
  transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), color 0.18s ease;
}

.hub-card:hover .hub-card-chevron {
  transform: translateX(3px);
  color: var(--charcoal-blue, #2f4550);
}

[data-theme="dark"] .hub-card-chevron {
  color: #9eb8b7;
}

[data-theme="dark"] .hub-card:hover .hub-card-chevron {
  color: #ffffff;
}

/* ── Advisor & Syllabus Strip ── */
.hub-advisor-strip {
  margin-top: 24px;
  background: #ffffff;
  border: 1px solid rgba(47, 69, 80, 0.12);
  border-radius: 16px;
  padding: 16px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  box-sizing: border-box !important;
}

[data-theme="dark"] .hub-advisor-strip {
  background: #182329;
  border-color: rgba(184, 219, 217, 0.18);
}

.hub-advisor-info {
  display: flex;
  align-items: center;
  gap: 14px;
}

.hub-advisor-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(184, 219, 217, 0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--charcoal-blue, #2f4550);
  font-size: 18px;
  flex-shrink: 0;
  border: 1px solid rgba(184, 219, 217, 0.6);
}

[data-theme="dark"] .hub-advisor-avatar {
  color: var(--light-blue, #b8dbd9);
  background: rgba(184, 219, 217, 0.14);
}

.hub-advisor-meta h4 {
  font-size: 13.5px;
  font-weight: 500;
  color: var(--charcoal-blue, #2f4550);
  margin: 0 0 3px 0;
}

[data-theme="dark"] .hub-advisor-meta h4 {
  color: #ffffff;
}

.hub-advisor-meta p {
  font-size: 12px;
  font-weight: 400;
  color: var(--blue-slate, #586f7c);
  margin: 0;
}

[data-theme="dark"] .hub-advisor-meta p {
  color: #9eb8b7;
}

.hub-advisor-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.hub-advisor-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px;
  font-size: 12px;
  font-weight: 500;
  border-radius: 8px;
  border: 1px solid rgba(47, 69, 80, 0.18);
  background: #ffffff;
  color: var(--charcoal-blue, #2f4550);
  cursor: pointer;
  transition: all 0.18s ease;
  text-decoration: none;
}

.hub-advisor-btn:hover {
  background: #f8fafc;
  border-color: rgba(47, 69, 80, 0.3);
}

.hub-advisor-btn-primary {
  background: var(--charcoal-blue, #2f4550);
  color: #ffffff;
  border-color: var(--charcoal-blue, #2f4550);
}

.hub-advisor-btn-primary:hover {
  background: #23343d;
  color: #ffffff;
}

[data-theme="dark"] .hub-advisor-btn {
  background: #22323a;
  border-color: rgba(184, 219, 217, 0.22);
  color: #e2e8f0;
}
[data-theme="dark"] .hub-advisor-btn:hover {
  background: #283a44;
}
[data-theme="dark"] .hub-advisor-btn-primary {
  background: var(--light-blue, #b8dbd9);
  color: var(--charcoal-blue, #2f4550);
  border-color: var(--light-blue, #b8dbd9);
}
[data-theme="dark"] .hub-advisor-btn-primary:hover {
  background: #a6c9c7;
}

/* ═══════════════════════════════════════════════════════════════
   RESPONSIVE BREAKPOINTS (Fluid mobile adaptation)
   ═══════════════════════════════════════════════════════════════ */
@media (max-width: 1024px) {
  .page {
    padding: 16px 20px 88px !important;
  }
  .hub-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 16px;
  }
}

@media (max-width: 768px) {
  .page {
    padding: 12px 14px 96px !important;
  }
  .hub-top-nav-bar {
    justify-content: flex-start;
    margin-bottom: 14px;
  }
  .hub-term-badge {
    width: 100%;
    justify-content: center;
    font-size: 11.5px;
    padding: 7px 12px;
  }
  .hub-advisor-strip {
    flex-direction: column;
    align-items: stretch;
    gap: 14px;
    padding: 16px;
  }
  .hub-advisor-actions {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    width: 100%;
  }
  .hub-advisor-btn {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 600px) {
  .hub-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  .hub-card {
    min-height: auto;
    padding: 16px 16px 14px;
  }
}

@media (max-width: 400px) {
  .page {
    padding: 10px 10px 96px !important;
  }
  .hub-advisor-actions {
    grid-template-columns: 1fr;
  }
}
</style>'''

content = style_pattern.sub(new_style, content)

# 5. In script, update applyDepartment and HERO_CONFIG
script_update = '''    // Update Hero Banner title & subtitle dynamically if present
    var heroTitleEl = document.querySelector('.hero-title');
    if (heroTitleEl) heroTitleEl.textContent = d.title;
    var heroGreetingEl = document.querySelector('.hero-greeting');
    if (heroGreetingEl) heroGreetingEl.textContent = d.desc;
    var heroBcEl = document.querySelector('.htb-bc-item:last-child');
    if (heroBcEl) heroBcEl.textContent = d.title.replace(' Hub', '');
'''

content = content.replace(
    '// Update Badges & Descriptions',
    script_update + '\n    // Update Badges & Descriptions'
)

# 6. Update HERO_CONFIG object definition
old_hero_config = '''window.HERO_CONFIG = {
  name: 'Nrinphouneta Hok',
  id: 'Student ID: 2026-STD-0142',
  grade: 'Grade 10',
  avatar: 'https://images.pexels.com/photos/3785079/pexels-photo-3785079.jpeg?auto=compress&cs=tinysrgb&w=160',
  avatarSm: 'https://images.pexels.com/photos/3785079/pexels-photo-3785079.jpeg?auto=compress&cs=tinysrgb&w=80',
  homeLink: '../../index.html',
  signOutLink: '../../index.html',
  profileLink: '../student/student-profile.html',
  notifLink: '../student/student-notifications.html',
  notifCount: 3,
  ddRows: [
    { icon: 'school', text: 'Grade 10 — Science Stream' },
    { icon: 'class', text: 'Class 10A' },
    { icon: 'email', text: 'nrinphouneta@ngis.edu.kh' },
    { icon: 'calendar_today', text: 'Enrolled: Sep 2024' },
    { icon: 'emoji_events', text: 'GPA: 3.87 / 4.00' }
  ],
  title: 'Academic Departments',
  greeting: 'Access all department coursework, evaluations, syllabus materials, and exam schedules.',
  breadcrumbs: [{ label: 'Departments', href: 'departments.html' }, { label: 'Department Hub' }]
};'''

new_hero_config = '''(function() {
  var p = new URLSearchParams(window.location.search);
  var currentId = (p.get('id') || 'english').toLowerCase();
  var dNames = {
    english: { title: 'English Department Hub', desc: 'English literature syllabi, essay coursework submissions, IGCSE past papers, and evaluations.' },
    khmer: { title: 'Khmer Department Hub', desc: 'Khmer literature, grammar textbooks, national examination roadmaps, and term performance reports.' },
    chinese: { title: 'Chinese Department Hub', desc: 'HSK 4 & 5 preparation materials, listening laboratory drills, stroke order guides, and grades.' },
    science: { title: 'Science & STEM Department Hub', desc: 'Central access for physics, chemistry, biology laboratories, coursework materials, and evaluations.' },
    math: { title: 'Mathematics Department Hub', desc: 'Calculus, advanced trigonometry problems, mathematical formula archives, and competition resources.' },
    social: { title: 'Social Studies & Humanities Hub', desc: 'World history, geography archives, civic engagement modules, and research evaluations.' },
    all: { title: 'Student Portal Hub', desc: 'Central access for all academic streams, coursework materials, examinations, and official evaluations.' }
  };
  var curD = dNames[currentId] || dNames.english;

  window.HERO_CONFIG = {
    name: 'Nrinphouneta Hok',
    id: 'Student ID: 2026-STD-0142',
    grade: 'Grade 10',
    avatar: 'https://images.pexels.com/photos/3785079/pexels-photo-3785079.jpeg?auto=compress&cs=tinysrgb&w=160',
    avatarSm: 'https://images.pexels.com/photos/3785079/pexels-photo-3785079.jpeg?auto=compress&cs=tinysrgb&w=80',
    homeLink: '../../index.html',
    signOutLink: '../../index.html',
    profileLink: '../student/student-profile.html',
    notifLink: '../student/student-notifications.html',
    notifCount: 3,
    ddRows: [
      { icon: 'school', text: 'Grade 10 — Science Stream' },
      { icon: 'class', text: 'Class 10A' },
      { icon: 'email', text: 'nrinphouneta@ngis.edu.kh' },
      { icon: 'calendar_today', text: 'Enrolled: Sep 2024' },
      { icon: 'emoji_events', text: 'GPA: 3.87 / 4.00' }
    ],
    title: curD.title,
    greeting: curD.desc,
    breadcrumbs: [
      { label: 'Departments', href: 'departments.html' },
      { label: curD.title.replace(' Hub', '') }
    ]
  };
})();'''

content = content.replace(old_hero_config, new_hero_config)

with open('pages/shared/department.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated pages/shared/department.html')

