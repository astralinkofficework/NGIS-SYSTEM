const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');

const ordinarySlots = {
  'admin-dashboard-cms.css': ['.cms-page-icon', '.cms-activity-icon'],
  'admin-operations-control.css': ['.ops-card-icon'],
  'announcements.css': ['.ann-widget-icon'],
  'app.css': ['.ngis-icon-slot'],
  'design-system.css': ['.smx-kpi-icon', '.smx-kpi-icon.warn', '.smx-kpi-icon.bad'],
  'khmer-suite.css': ['.ks-kpi-icon'],
  'mobile-header.css': ['.ngis-notif-icon-wrap'],
  'navbar.css': ['.ngis-notif-item-icon', '.ngis-search-item-icon'],
  'roles-access.css': ['.banner-icon'],
  'shared-components.css': ['.ngis-dept-row-icon', '.mob-bn-icon-wrap'],
  'smart-disclosure.css': ['.smart-accordion-icon'],
  'ngis-components.css': ['.ngis-state-icon'],
  'ui-states.css': ['.ngis-state-icon'],
};

for (const [file, slots] of Object.entries(ordinarySlots)) {
  const css = fs.readFileSync(path.join(root, 'assets/css', file), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '');
  for (const slot of slots) {
    const matchingRules = [...css.matchAll(/([^{}]+)\{([^{}]*)\}/g)]
      .filter(([, selectors]) => selectors.includes(slot));
    assert.ok(matchingRules.length, file + ' must style ' + slot);
    for (const [, selector, declarations] of matchingRules) {
      assert.doesNotMatch(declarations, /(?:^|;)\s*(?:background(?:-color|-image)?|box-shadow|border-radius)\s*:/i,
        file + ' paints the ordinary icon slot ' + selector.trim());
    }
  }
}

const pages = path.join(root, 'pages');
for (const portal of fs.readdirSync(pages, {withFileTypes: true}).filter(entry => entry.isDirectory())) {
  const folder = path.join(pages, portal.name);
  for (const name of fs.readdirSync(folder).filter(file => file.endsWith('.html'))) {
    const html = fs.readFileSync(path.join(folder, name), 'utf8');
    for (const [, classes] of html.matchAll(/class="([^"]*\bngis-icon-slot\b[^"]*)"/g)) {
      assert.doesNotMatch(classes, /(?:^|[\s:])(?:bg-|rounded(?:-|\b)|shadow(?:-|\b))/,
        name + ' adds decorative utilities to an ordinary icon slot');
    }
  }
}

for (const role of ['student', 'teacher']) {
  const html = fs.readFileSync(path.join(root, 'pages', role, role + '.html'), 'utf8');
  assert.doesNotMatch(html, /<[^>]*class="ql-icon-wrap"[^>]*style="[^"]*background/i,
    role + ' quick link paints its alignment wrapper');
}

// Verification of shared JS engines: icon containers carry color directly without decorative bg/pill containers
const adminTtJs = fs.readFileSync(path.join(root, 'assets/js/admin-timetable-monitoring.js'), 'utf8');
assert.doesNotMatch(adminTtJs, /class="[^"]*w-10 h-10[^"]*bg-(?:amber|rose|emerald)-100/i,
  'admin-timetable-monitoring.js paints review banner icon wrappers');

const layoutJs = fs.readFileSync(path.join(root, 'assets/js/layout.js'), 'utf8');
assert.doesNotMatch(layoutJs, /class="[^"]*w-14 h-14[^"]*bg-emerald-50/i,
  'layout.js paints dialog success icon container');

const profilesJs = fs.readFileSync(path.join(root, 'assets/js/ngis-profiles.js'), 'utf8');
assert.doesNotMatch(profilesJs, /class="[^"]*sm:w-10 sm:h-10[^"]*bg-emerald-50/i,
  'ngis-profiles.js paints telemetry icon container');

const teacherMgmtJs = fs.readFileSync(path.join(root, 'assets/js/teacher-management.js'), 'utf8');
assert.doesNotMatch(teacherMgmtJs, /class="[^"]*w-9 h-9[^"]*bg-\[(?:#E8F3ED|#FEF0E3)\]/i,
  'teacher-management.js paints telemetry icon containers');

console.log('Ordinary shared icon slots, quick links, and JS engines use unpainted wrappers.');
