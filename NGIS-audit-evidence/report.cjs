const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const dir = __dirname;
const read = name => fs.readFileSync(path.join(dir, name), 'utf8').replace(/^\uFEFF/, '');
const json = (name, fallback) => fs.existsSync(path.join(dir, name)) ? JSON.parse(read(name)) : fallback;
const data = json('page-results.json', []);
const workflows = json('workflow-results.json', {});
const targeted = json('targeted-results.json', {});
const suites = [...json('suite-results.json', []), ...json('extra-suite-results.json', [])];
const routes = json('server-routes.json', []);
const extra = json('states-results.json', {});
const findings = read('findings.md').trim();
const parts = findings.split(/(?=^### F\d\d\.)/m);
const findingPriority = ['F16','F01','F11','F02','F03','F04','F05','F06','F07','F08','F09','F13','F15','F10','F12','F14'];
const out = [parts[0].trim(), '', ...findingPriority.flatMap(id => [parts.find(part => part.startsWith('### '+id+'.')).trim(),''])];
const pageRows = new Map();
for (const record of data) {
  const key = record.role + '|' + record.path;
  if (!pageRows.has(key)) pageRows.set(key, {});
  pageRows.get(key)[record.width] = record;
}
function cell(record) {
  if (!record) return 'Unverified';
  if (!record.status) return 'Blocked · timeout or navigation error';
  if (record.status >= 400) return 'HTTP ' + record.status;
  if (record.final?.includes('access-denied.html') && !record.path.includes('access-denied')) return 'Restricted';
  const suffix = [];
  if (record.portal) suffix.push(record.portal);
  if (record.final && record.final !== record.path) suffix.push('redirected');
  if (record.width === 375 && record.sidebar) {
    if (!record.hamburgers.length) suffix.push('hamburger missing');
    else if (record.drawer === false) suffix.push('drawer check failed');
    else if (record.drawer === true) suffix.push('drawer opened');
  }
  if (record.overflow > 4) suffix.push('document overflow +' + record.overflow + ' px');
  if (record.errors?.length) suffix.push(record.errors.length + ' script error(s)');
  return String(record.status) + (suffix.length ? ' · ' + suffix.join(', ') : '');
}
const measuredPageCount = [...pageRows].filter(([, v]) => Object.values(v).some(x => x.status)).length;
const uniqueFiles = new Set(data.filter(r => r.status && r.path.endsWith('.html') && !r.path.includes('missing')).map(r => r.path));
out.push('## Coverage and evidence', '',
  '**' + measuredPageCount + ' page and route contexts received a browser document response** across ' + data.length + ' viewport attempts. This includes aliases, negative routes, shared portal variants and the two separately hosted timetable pages. The sweep considered **' + uniqueFiles.size + ' distinct Flask HTML page paths**. The Flask runtime inventory contains **' + routes.length + ' registered URL rules**, including static routing and APIs.',
  '', '[Page measurements and HTTP responses](NGIS-audit-evidence/page-results.json) · [Flask route inventory with methods and source lines](NGIS-audit-evidence/server-routes.json) · [Playwright workflow results](NGIS-audit-evidence/workflow-results.json) · [Targeted browser results](NGIS-audit-evidence/targeted-results.json) · [Regression suites](NGIS-audit-evidence/suite-results.json).', '',
  '### Every discovered application page and route context', '',
  '| Portal or host | Page or route | 1440 px | 375 px |', '|---|---|---|---|');
const roles = ['public','student','teacher','parent','principal','admin','superadmin','shared','timetable'];
for (const role of ['student','teacher','principal','admin','shared']) {
  const files = fs.readdirSync(path.join(root,'pages',role)).filter(x => x.endsWith('.html'));
  for (const file of files) {
    const key = role+'|/pages/'+role+'/'+file;
    if (!pageRows.has(key)) pageRows.set(key, {});
  }
}
const labels={public:'Public / routing',student:'Student',teacher:'Teacher',parent:'Parent',principal:'Principal',admin:'Admin',superadmin:'Super Admin preview',shared:'Shared',timetable:'Standalone timetable'};
for (const role of roles) {
  for (const [key, rec] of [...pageRows].sort(([a],[b])=>a.localeCompare(b))) {
    if (!key.startsWith(role+'|')) continue;
    out.push('| '+labels[role]+' | `'+key.split('|')[1]+'` | '+cell(rec[1440])+' | '+cell(rec[375])+' |');
  }
  if(role==='parent') out.push('| Parent | `/pages/parent/parent.html` | HTTP 404 · targeted check | No mobile portal to open |');
  if(role==='timetable') for(const route of ['/assign','/teachers','/classes','/subjects','/overtime','/now','/print']) {
    const observed=extra.timetableDeclared?.[route];
    out.push('| Standalone timetable | `'+route+'` | '+(observed?'HTTP '+observed.status:'Source only · sidebar link has no route file')+' | Schedule shell blocked |');
  }
}
out.push('', '### Major workflow coverage', '', '| ID | Portal | Workflow | Result and boundary |','|---|---|---|---|');
const checks = [];
const add=(role,flow,result,executed=false)=>checks.push({role,flow,result,executed});
const suite = (pattern) => suites.find(r => r.suite===pattern && r.summary?.some(x=>!x.includes('Ran 0')));
const summary = (pattern) => {
 const row=suite(pattern);
 if(!row) return 'No completed backend execution recorded.';
 return (row.exit===0?'Backend suite exited successfully. ':'Backend suite had failures or errors. ')+(row.summary.find(x=>x.startsWith('Ran ')&&!x.startsWith('Ran 0'))||'');
};
const addSuite=(role,flow,pattern,limit)=>add(role,flow,summary(pattern)+' '+limit,!!suite(pattern));
add('Public','Landing and portal entry','Four staff and learner cards reached on desktop. Mobile tap interception reproduced (F04).',true);
add('Shared','Own-portal shell and mobile drawer','Direct-load shell metrics for each page. Dashboard refresh sampled. Scope and drawer exceptions are in the page table.',true);
add('Shared','Cross-portal direct route isolation','Student was denied the canonical Admin page. Clean aliases returned foreign dashboard HTML with a Student shell (F11).',true);
add('Parent','Sign-in, landing and account navigation','Fixture sign-in succeeded. Parent landing and role page returned 404. Remaining Parent workflows blocked (F02).',true);
add('Super Admin','Dashboard and shared navigation','Query-based preview and refresh exercised. Fixture sign-in was rejected and privileged browser workflows were blocked.',true);
add('Student','Assignments, submission upload and resubmission','Assignment shell checked. Submission persistence and upload paths not exercised.');
add('Student','Report cards, grade visibility and attendance','Grade and attendance shells checked. '+summary('tests/academic-mvp.test.py'),!!suite('tests/academic-mvp.test.py'));
add('Student','Published timetable, day filters and export',extra.studentTimetable?'Network failure injected and misclassified as no enrollment (F13). The loading indicator was not conclusively observed.':'Timetable shell checked. Export and failure states unverified.',!!extra.studentTimetable);
add('Student','Calendar, announcements, notification read state and profile','Page shells checked. Calendar event action, read persistence and profile save unverified.');
add('Student / Teacher / Admin / Principal','Services and lost-and-found submission, fulfillment, claims and return','Page shells checked. Account-specific submission, upload and fulfillment unverified.');
add('Student / Teacher / Shared','Department context, lessons, exam materials and lesson detail','Shared portal variants and detail routes checked for direct-load shell. Materials upload and student assessment lifecycle unverified.');
add('Teacher','Roster and homeroom workflows','Shell checked. '+summary('tests/teacher-my-class.test.py'),!!suite('tests/teacher-my-class.test.py'));
add('Teacher','Gradebook and attendance editing, submissions and feedback','Page shells checked. '+summary('tests/academic-mvp.test.py')+' Browser saves, grading and feedback unverified.',!!suite('tests/academic-mvp.test.py'));
add('Teacher','Teaching materials, exams, documents and reports','Page shells checked. File CRUD, assessment publication and report generation unverified.');
add('Teacher','Timetable, calendar, news, notifications and profile','Page shells checked. Per-record actions unverified.');
for(const role of ['student','teacher','staff','principal','admin']) {
 const x=workflows['Add '+role]||{};
 add('Admin','Add '+role+' from scratch',x.createStatus===201&&x.loginStatus===200?'Wizard created a new person and account (201), login succeeded (200), and success screen returned to the directory.':(x.wizardOpened?'Wizard opened. ':'')+'Creation and login unverified'+(x.visibleError?' · '+x.visibleError:'.'),!!x.wizardOpened||!!x.error);
}
add('Admin','Registration photo and form feedback','PNG preview and removal exercised. Typed field loss and required-field feedback reproduced (F05).',true);
addSuite('Admin','Identity provisioning, status, audit trail and credential handling','test_user_management.py','Browser end-to-end status and reset flows unverified.');
add('Principal','Academic adjustment review, clarification, acceptance, decline, publication and history','All four actions executed on sample record. Actual cross-session history and publication failed (F01). New request creation and correction resubmission unverified.',true);
addSuite('Principal','Registration, approvals, roster, classes, service and activity oversight','test_principal_e2e.py','Registration decision UI and feed history not fully exercised.');
addSuite('Principal / Admin','School information and configuration','test_school_information_e2e.py','School year, calendar week and other system-setting mutations not individually exercised.');
addSuite('Principal / Admin','Timetable draft, validation, preview and publish','test_timetable_publication.py','Backend tests ran. Standalone Next.js schedule blocked. Direct browser timetable writes unverified.');
addSuite('Principal / Admin','Timetable replacement and import','test_timetable_replacement.py','Browser choose-file/import screens unverified.');
addSuite('Principal / Admin','Timetable monitoring and oversight','test_timetable_monitoring.py','Browser monitoring interactions unverified.');
add('Admin / Principal','Campus and department permission boundaries',targeted['Scoped Admin data reads']?.assignmentCampus?'Scoped Admin read requests returned out-of-campus entries (F16). Department grants, out-of-scope writes and other role combinations unverified.':'Browser attempt blocked before establishing scoped fixture. Static scope handlers reviewed.',true);
addSuite('Admin / Super Admin','Roles, access, delegated permissions, visibility overrides and audit','test_roles_access_v3.py','Backend tests ran. Full signed-in Super Admin browser session unverified.');
addSuite('Admin / Super Admin','Legacy route enforcement, hidden-only policy and scope resolver','test_roles_permissions.py','Code and backend suite, plus browser alias checks under Student.');
addSuite('Admin','Sidebar navigation management','test_sidebar_manager.py','Published nav consumed during sweep. Admin editing and rollback UI unverified.');
addSuite('Admin','Dashboard page content, banners and publishing','test_dashboard_cms.py','Browser content editing and rollback unverified.');
addSuite('Admin / Principal / Teacher / Student','Exam administration and published exam data','test_simplified_exams.py','Browser exam creation, publish and students taking exams unverified.');
add('Admin / Principal','Grade release, overrides, attendance correction, report-card and transcript upload/download','Shells inventoried. Transcript upload, grade release UI and override mutations not verified in a browser.');
add('Admin','Account security, logs, system configuration, campus pages and organization management','Shells inspected. Security controls, private audit exports, department and campus mutation and restoring settings not exercised.');
add('Admin / Principal','Data dictionary records, subjects, faculty assignments and school-year settings','Route coverage and code inspection. Full create/edit/delete/import/export combinations unverified.');
add('Shared','Error, access denied, empty-state demonstrations, onboarding and design previews','Direct shells and a missing route exercised. Individual examples and onboarding progression unverified.',true);
add('Shared','Keyboard focus and surface state','Inspect default, hover, press and keyboard focus measured. Sidebar label and active surface sampled (F06).',true);
add('Standalone timetable','Home, schedule, mobile drawer and linked destinations','Home returned 200 with starter content. Schedule returned 500. Upstream timetable actions and mobile drawer blocked (F03).',true);
for(const [idx,x] of checks.entries()) out.push('| W'+String(idx+1).padStart(2,'0')+' | '+x.role+' | '+x.flow+' | '+x.result+' |');
out.push('', '**'+checks.filter(x=>x.executed).length+' of '+checks.length+' workflow groups had a browser interaction or backend test execution.** Shell-only groups are shown separately in the table. A group can include a failed check or remaining scenario gaps.', '', '### Backend regression evidence', '',
'| Suite | Exit | Observed summary |','|---|---:|---|');
for (const s of suites) {
  const summary=(s.summary||[]).filter(l=>!l.startsWith('AssertionError')).slice(0,12).join(' / ').replaceAll('|','/');
  out.push('| `'+s.suite+'` | '+(s.exit??'—')+' | '+(summary||s.error||'No unittest summary printed. Consult the saved log.')+' |');
}
out.push('', '### Remaining coverage gaps', '',
'- Parent portal is missing. Super Admin preview was reachable but the local Super Admin sign-in fixture was rejected. No staging identity was used.',
'- The standalone Next.js timetable returned 500 before its schedule and drawer could render. Its downstream MCP data flows were unverified.',
'- Browser verification used Chromium at 375 and 1440 px. Tablet breakpoints, other engines, physical devices, full keyboard traversal, screen-reader behavior and systematic color-contrast coverage remain open.',
'- Only the selected interactions and regression suites described above ran. Full data-state, cross-campus and cross-department write permutations, production configuration, email delivery, generated documents and hands-on browser end-to-end checks for all workflows remain open.',
'- The current snapshot contains pre-existing uncommitted changes. No prior build was executed for a binary regression comparison. Regression signals refer to the current repository test contracts.',
'');
fs.writeFileSync(path.join(root,'NGIS-SYSTEM-AUDIT.md'),out.join('\n'));
console.log(JSON.stringify({pageContexts:measuredPageCount,viewportAttempts:data.length,htmlPaths:uniqueFiles.size,workflows:checks.filter(x=>x.executed).length,workflowInventory:checks.length,flaskRules:routes.length}));

