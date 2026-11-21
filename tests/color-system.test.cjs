const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');

test('Color System: No rogue blue (rgba(36, 85, 214)) in CSS stylesheets', () => {
  const cssFiles = [
    'assets/css/app.css',
    'assets/css/hero.css',
    'assets/css/interactions.css',
    'assets/css/portal-dashboard.css',
    'assets/css/design-tokens.css',
    'assets/css/design-system.css',
    'assets/css/shared-components.css',
    'assets/css/announcements.css'
  ];

  const rogueBlueRegex = /rgba?\(\s*36\s*,\s*85\s*,\s*214/i;

  cssFiles.forEach(file => {
    const fullPath = path.resolve(__dirname, '..', file);
    if (!fs.existsSync(fullPath)) return;
    const content = fs.readFileSync(fullPath, 'utf8');
    const match = rogueBlueRegex.test(content);
    assert.strictEqual(
      match,
      false,
      `Found rogue blue rgba(36, 85, 214, ...) in ${file}`
    );
  });
});

test('Color System: Design Tokens single source of truth brand green', () => {
  const tokensPath = path.resolve(__dirname, '..', 'assets/css/design-tokens.css');
  const content = fs.readFileSync(tokensPath, 'utf8');

  // Verify --color-primary is #176B45
  assert.match(content, /--color-primary:\s*#176B45/i, 'Primary brand color must be #176B45');
  // Verify --color-surface is #FFFFFF
  assert.match(content, /--color-surface:\s*#FFFFFF/i, 'Neutral surface must be #FFFFFF');
  // Verify --color-background is #F7F9F7
  assert.match(content, /--color-background:\s*#F7F9F7/i, 'Neutral workspace canvas must be #F7F9F7');
});

test('Color System: No rainbow avatar colors in Admin Campus or Student Assignment', () => {
  const campusFile = path.resolve(__dirname, '..', 'pages/admin/admin-campus.html');
  const assignFile = path.resolve(__dirname, '..', 'pages/admin/admin-student-assign.html');

  const campusContent = fs.readFileSync(campusFile, 'utf8');
  assert.doesNotMatch(campusContent, /bg-purple-50 text-purple-800/, 'No purple avatar in admin-campus.html');
  assert.doesNotMatch(campusContent, /bg-cyan-50 text-cyan-800/, 'No cyan avatar in admin-campus.html');

  const assignContent = fs.readFileSync(assignFile, 'utf8');
  assert.doesNotMatch(assignContent, /bg-indigo-100 dark:bg-indigo-950/, 'No indigo avatar in admin-student-assign.html');
  assert.doesNotMatch(assignContent, /bg-violet-100 dark:bg-violet-950/, 'No violet avatar in admin-student-assign.html');
  assert.doesNotMatch(assignContent, /bg-pink-100 dark:bg-pink-950/, 'No pink avatar in admin-student-assign.html');
});

test('Color System: In Progress status badges use brand/neutral colors, not purple', () => {
  const reqPage = path.resolve(__dirname, '..', 'pages/principal/principal-requests.html');
  const reqJs = path.resolve(__dirname, '..', 'assets/js/academic-requests.js');

  const pageContent = fs.readFileSync(reqPage, 'utf8');
  assert.doesNotMatch(pageContent, /bg-purple-50 text-purple-700/, 'No purple status badge in principal-requests.html');

  const jsContent = fs.readFileSync(reqJs, 'utf8');
  assert.doesNotMatch(jsContent, /bg-purple-50 text-purple-700/, 'No purple status badge in academic-requests.js');
});

test('Color System: Lost & Found KPI 4 uses neutral/amber status, not indigo', () => {
  const lfPath = path.resolve(__dirname, '..', 'pages/admin/admin-lost-found.html');
  const content = fs.readFileSync(lfPath, 'utf8');

  assert.doesNotMatch(content, /text-indigo-700.*id="kpiClaims"/, 'kpiClaims must not use indigo');
  assert.doesNotMatch(content, /id="detailClaimsCountPill"[^>]*bg-indigo-50/, 'detailClaimsCountPill must not use indigo');
});
