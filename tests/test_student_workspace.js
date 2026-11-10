#!/usr/bin/env node
/* ============================================================================
 * NGIS Student Management Executive Workspace — headless render/interaction test
 * ============================================================================
 * Verifies the token-scoped .ngis-sm/.smx-* renderers for:
 *   - Verify Student Profile Updates
 *   - Absence Statistics & Attendance Risk Register
 *
 * Run:  node tests/test_student_workspace.js
 * ==========================================================================*/
'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');
const JS = fs.readFileSync(path.join(ROOT, 'assets/js/ngis-student-workspace.js'), 'utf8');
const CSS = fs.readFileSync(path.join(ROOT, 'assets/css/design-system.css'), 'utf8');
const VERIFY_PAGE = fs.readFileSync(path.join(ROOT, 'pages/admin/admin-student-verify.html'), 'utf8');
const ABSENCE_PAGE = fs.readFileSync(path.join(ROOT, 'pages/admin/admin-absence-stats.html'), 'utf8');
let failures = 0;

function assert(cond, label) {
  if (!cond) { failures++; console.log('   FAIL: ' + label); }
  return cond;
}

const VERIFY_DATA = {
  data: [
    {
      id: 'SUR-2026-001', studentId: 'STD-001', studentName: 'Nrinphouneta Hok', initials: 'NH',
      class: '10A', field: 'Residential Address', fieldCategory: 'Student Primary Domicile',
      previousValue: 'No. 45, St. 2004', proposedValue: 'No. 128, St. 598',
      submittedBy: 'Parent', submittedAt: '2026-11-08 10:15', timeAgo: 'Nov 8',
      supportingDoc: 'lease.pdf', status: 'pending', comments: ''
    },
    {
      id: 'SUR-2026-002', studentId: 'STD-002', studentName: 'Sophea Chan', initials: 'SC',
      class: '10B', field: 'Emergency Contact & Phone', fieldCategory: 'Guardian Contact Channel',
      previousValue: '+855 12 345 678', proposedValue: '+855 98 765 432',
      submittedBy: 'Guardian', submittedAt: '2026-11-08 09:45', timeAgo: 'Nov 8',
      supportingDoc: 'id.pdf', status: 'pending', comments: ''
    },
    {
      id: 'SUR-2026-003', studentId: 'STD-003', studentName: 'Virak Heng', initials: 'VH',
      class: '10A', field: 'Legal Name Khmer Spelling', fieldCategory: 'MoEYS Formal Registry',
      previousValue: 'អេង វីរៈ', proposedValue: 'ហេង វីរៈ',
      submittedBy: 'Student', submittedAt: '2026-11-07 14:20', timeAgo: 'Nov 7',
      supportingDoc: 'birth.pdf', status: 'approved',
      reviewedBy: 'Admin · Records Office', reviewedAt: '2026-11-07 16:40',
      comments: 'Verified against civil registry.'
    }
  ],
  total: 3
};

const ABSENCE_DATA = {
  kpis: { overallRate: 95.1, totalAbsences: 115, unexcusedTotal: 25, chronicAbsentees: 4 },
  cohortDistribution: [
    { cohort: 'Grade 12A', enrolled: 178, absences: 1, attendancePct: 97.0, status: 'Excellent' },
    { cohort: 'Grade 11B', enrolled: 172, absences: 32, attendancePct: 93.2, status: 'At Risk' }
  ],
  absenceCategories: [
    { category: 'Medical & Authorized Leaves', days: 75, pct: 65.2, desc: 'Clinic note / guardian' },
    { category: 'Unexcused Truancy', days: 25, pct: 21.7, desc: 'No prior notification' }
  ],
  classComparison: [{ class: '10A', enrolled: 180, averageAttendance: 95.4, totalDaysMissed: 21 }],
  students: [
    {
      studentId: 'STD-001', studentName: 'Nrinphouneta Hok', initials: 'NH', class: '10A', grade: 'Grade 10',
      attendancePct: 88, attendedDays: 70, totalAbsentDays: 10, excusedAbsences: 6, unexcusedAbsences: 4,
      riskLevel: 'Critical (>5 Days)', isChronic: true, parentNotified: true,
      noticeStatus: 'Pending Dispatch', noticeDate: 'Today, 08:30 AM',
      guardian: { name: 'Guardian of Nrinphouneta Hok', phone: '+855 12 345 678' },
      absenceLog: [{ date: 'Nov 07, 2026', session: 'Full Day', category: 'Unexcused Truancy', verification: 'Unverified', action: 'Notice Sent' }]
    },
    {
      studentId: 'STD-002', studentName: 'Sophea Chan', initials: 'SC', class: '10B', grade: 'Grade 10',
      attendancePct: 96, attendedDays: 77, totalAbsentDays: 3, excusedAbsences: 3, unexcusedAbsences: 0,
      riskLevel: 'Normal', isChronic: false, parentNotified: false,
      noticeStatus: 'Not required', noticeDate: '',
      guardian: { name: 'Guardian of Sophea Chan', phone: '+855 98 765 432' },
      absenceLog: []
    }
  ]
};

function fakeEl(tag) {
  const attrs = {};
  const handlers = {};
  const el = {
    tagName: tag || 'DIV', id: '', className: '', innerHTML: '', textContent: '',
    style: {}, value: '', checked: false, disabled: false, parentNode: null, children: [],
    classList: { add() {}, remove() {} },
    setAttribute(k, v) { attrs[k] = String(v); },
    getAttribute(k) { return Object.prototype.hasOwnProperty.call(attrs, k) ? attrs[k] : null; },
    addEventListener(type, fn) { (handlers[type] || (handlers[type] = [])).push(fn); },
    appendChild(child) { child.parentNode = el; el.children.push(child); return child; },
    removeChild(child) {
      const i = el.children.indexOf(child);
      if (i >= 0) el.children.splice(i, 1);
      child.parentNode = null;
      return child;
    },
    remove() { if (el.parentNode) el.parentNode.removeChild(el); },
    focus() {}, setSelectionRange() {}, click() {},
    querySelector() { return null; }, querySelectorAll() { return []; },
    _handlers: handlers, _attrs: attrs
  };
  return el;
}

function makeContext() {
  const root = fakeEl('DIV');
  const body = fakeEl('BODY');
  const head = fakeEl('HEAD');
  const created = [];
  const posts = [];

  const doc = {
    body, head, readyState: 'complete', visibilityState: 'visible',
    getElementById(id) { return id === 'studentMgmtRoot' ? root : null; },
    createElement(tag) { const el = fakeEl(tag); created.push(el); return el; },
    addEventListener() {}, querySelector() { return null; }, querySelectorAll() { return []; }
  };

  function fetchStub(url, options) {
    let payload = {};
    if (url.indexOf('/action') !== -1 || url.indexOf('/notify') !== -1) {
      posts.push({ url, body: options && options.body ? JSON.parse(options.body) : {} });
      payload = { success: true, message: 'Guardian notice dispatched' };
    } else if (url.indexOf('/api/student-mgmt/verify') === 0) {
      payload = VERIFY_DATA;
    } else if (url.indexOf('/api/student-mgmt/absence-stats') === 0) {
      payload = ABSENCE_DATA;
    }
    return Promise.resolve({ ok: true, status: 200, json: () => Promise.resolve(payload) });
  }

  const sandbox = {
    console: { log() {}, warn() {}, error() {} },
    setTimeout, clearTimeout, fetch: fetchStub, Promise,
    document: doc,
    PAGE: { role: 'admin' },
    URL: undefined
  };
  sandbox.window = sandbox;
  sandbox.globalThis = sandbox;
  vm.createContext(sandbox);
  vm.runInContext(JS, sandbox, { filename: 'assets/js/ngis-student-workspace.js' });
  return { sandbox, root, doc, body, created, posts };
}

function fire(el, type, event) {
  (el._handlers[type] || []).forEach(fn => fn(event));
}

function targetNode(attrs) {
  const node = fakeEl('BUTTON');
  Object.keys(attrs || {}).forEach(k => node.setAttribute(k, attrs[k]));
  return node;
}

function flush() { return new Promise(resolve => setTimeout(resolve, 0)); }

async function main() {
  console.log('Static page + design-system wiring');
  {
    assert(VERIFY_PAGE.includes('ngis-student-workspace.js?v=1.1'), 'verify page loads the NGIS renderer');
    assert(ABSENCE_PAGE.includes('ngis-student-workspace.js?v=1.1'), 'absence page loads the NGIS renderer');
    assert(VERIFY_PAGE.indexOf('student-management.js') < VERIFY_PAGE.indexOf('ngis-student-workspace.js'),
           'verify renderer overrides the legacy controller');
    assert(ABSENCE_PAGE.indexOf('student-management.js') < ABSENCE_PAGE.indexOf('ngis-student-workspace.js'),
           'absence renderer overrides the legacy controller');
    assert(VERIFY_PAGE.includes('design-system.css?v=1.2') && ABSENCE_PAGE.includes('design-system.css?v=1.2'),
           'scoped stylesheet is cache-busted');
    assert(VERIFY_PAGE.includes('smx-appbar') && ABSENCE_PAGE.includes('smx-appbar'),
           'mobile appbar uses the NGIS surface rule');
    assert(VERIFY_PAGE.includes('flex smx-page') && ABSENCE_PAGE.includes('flex smx-page'),
           'both pages scope the responsive shell containment');
    assert(VERIFY_PAGE.includes('initVerify(') && ABSENCE_PAGE.includes('initAbsenceStats('),
           'page shells still call the expected controllers');
    assert(CSS.split('{').length === CSS.split('}').length, 'design-system.css braces are balanced');
    const scoped = CSS.slice(CSS.indexOf('STUDENT MANAGEMENT EXECUTIVE WORKSPACE'));
    assert(scoped.includes('.ngis-sm') && scoped.includes('.smx-kpi-grid') &&
           scoped.includes('.smx-bento') && scoped.includes('.smx-table'),
           'scoped NGIS workspace styles are present');
    assert(scoped.includes('@media (max-width: 720px)'), 'mobile breakpoint exists');
    // The injected .shell is a flex item; without a min-width floor the ledger's
    // min-content width used to push the whole app shell past the viewport.
    assert(/body\.smx-page \.shell\s*\{[^}]*min-width:\s*0[^}]*\}/.test(scoped),
           'layout shell is width-contained on the executive workspaces');
    assert(/body\.smx-page #studentMgmtRoot\.page\s*\{[^}]*min-width:\s*0[^}]*\}/.test(scoped),
           'page container cannot be sized by the wide ledger table');
    assert(JS.includes("suppressDuplicateHamburger") &&
           JS.includes("setProperty('display', 'none', 'important')"),
           'duplicate mobile hamburger is suppressed by the renderer');
    assert(/\.smx-table-scroll\s*\{[^}]*overflow-x:\s*auto[^}]*\}/.test(scoped),
           'dense ledger scrolls inside its card instead of widening the page');
    assert(!scoped.includes('linear-gradient'), 'scoped styles have no gradients');
    assert(!/font-weight:\s*(600|700|800)/.test(scoped), 'scoped styles use 400/500 weights only');
    assert(!/class="[^"]*\b(bg-|text-slate|shadow-|rounded-|font-bold|grid |flex )/.test(JS),
           'renderer markup avoids legacy Tailwind utility classes');
    assert(!JS.includes('linear-gradient') && !/font-weight:\s*(600|700|800)/.test(JS),
           'renderer introduces no gradients or 600/700 weights');
  }

  console.log('\nVerify Student Profile Updates render');
  {
    const ctx = makeContext();
    ctx.sandbox.STUDENT_MGMT.initVerify('studentMgmtRoot', 'admin');
    await flush();
    const h = ctx.root.innerHTML;
    assert(h.includes('data-renderer="ngis-sm"') && h.includes('class="ngis-sm"'),
           'token-scoped NGIS wrapper is rendered');
    assert(h.includes('Verify Student Profile Updates'), 'executive H1 is present');
    assert(h.includes('smx-kpi-grid'), 'KPI strip is present');
    assert((h.match(/class="smx-kpi"/g) || []).length === 4, 'exactly 4 KPI tiles');
    assert(h.includes('Clearance Ledger') && h.includes('class="smx-table"'),
           'dense clearance ledger is present');
    assert(h.includes('smx-tabs') && h.includes('smx-toolbar') && h.includes('smx-pager'),
           'tabs, filter toolbar and pagination are present');
    assert(h.includes('Nrinphouneta Hok') && h.includes('Sophea Chan'),
           'live API rows are rendered');
    assert(h.includes('Export CSV') && h.includes('AY 2026'), 'header actions are present');
    assert(!h.includes('undefined') && !h.includes('NaN'), 'no undefined / NaN output');
    assert(!/class="[^"]*\b(bg-|text-slate|shadow-)/.test(h), 'no legacy Tailwind surface classes');
  }

  console.log('\nVerify interactions');
  {
    const ctx = makeContext();
    ctx.sandbox.STUDENT_MGMT.initVerify('studentMgmtRoot', 'admin');
    await flush();

    fire(ctx.root, 'input', { target: { id: 'smxSearch', value: 'Sophea' } });
    assert(ctx.root.innerHTML.includes('Sophea Chan') && !ctx.root.innerHTML.includes('Nrinphouneta Hok'),
           'search filters the ledger');

    fire(ctx.root, 'click', { target: targetNode({ 'data-tab': 'pending' }) });
    assert(ctx.root.innerHTML.includes('smx-tab active'), 'tab filter re-renders active state');

    fire(ctx.root, 'click', { target: targetNode({ 'data-act': 'view', 'data-id': 'SUR-2026-001' }) });
    const modal = ctx.created.find(el => String(el.className).includes('smx-modal-backdrop'));
    assert(modal && modal.innerHTML.includes('Review Profile Amendment Diff'),
           'review modal uses the NGIS modal shell');
    assert(modal.innerHTML.includes('smx-diff') && modal.innerHTML.includes('smx-info-grid'),
           'review modal shows diff and student context');

    fire(modal, 'click', { target: targetNode({ 'data-act': 'modal-approve' }) });
    await flush();
    assert(ctx.posts.some(p => p.url.indexOf('/action') !== -1 && p.body.action === 'approve'),
           'modal approval posts to the live action endpoint');
    assert(ctx.root.innerHTML.includes('Approved &amp; Synced'), 'approval re-renders the derived KPI/ledger');

    fire(ctx.root, 'click', { target: targetNode({ 'data-act': 'approve', 'data-id': 'SUR-2026-002' }) });
    await flush();
    assert(ctx.posts.filter(p => p.body.action === 'approve').length >= 2,
           'direct row approval also posts to the action endpoint');
    assert(!ctx.root.innerHTML.includes('undefined') && !ctx.root.innerHTML.includes('NaN'),
           'interactions produce no undefined / NaN output');
  }

  console.log('\nAbsence Statistics & Attendance Risk Register render');
  {
    const ctx = makeContext();
    ctx.sandbox.STUDENT_MGMT.initAbsenceStats('studentMgmtRoot', 'admin');
    await flush();
    const h = ctx.root.innerHTML;
    assert(h.includes('data-renderer="ngis-sm"') && h.includes('class="ngis-sm"'),
           'token-scoped NGIS wrapper is rendered');
    assert(h.includes('Absence Statistics &amp; Attendance Risk Register'), 'executive H1 is present');
    assert(h.includes('smx-kpi-grid') && (h.match(/class="smx-kpi"/g) || []).length === 4,
           'four derived KPI tiles are present');
    assert(h.includes('Overall Attendance Rate') && h.includes('Chronic Absenteeism Flag'),
           'reference KPI labels are preserved');
    assert(h.includes('smx-bento') && h.includes('Attendance Distribution by Cohort') &&
           h.includes('Absence Classification'), 'bento analytics split is present');
    assert(h.includes('Attendance Risk Register') && h.includes('class="smx-table"'),
           'dense risk register is present');
    assert(h.includes('Nrinphouneta Hok') && h.includes('Critical (&gt;5 Days)'),
           'live risk rows and badges are rendered');
    assert(h.includes('smx-bar') && h.includes('smx-badge'), 'bars and status badges are present');
    assert(h.includes('smx-pager') && h.includes('Notify Selected'), 'pagination and notice workflow are present');
    assert(!h.includes('undefined') && !h.includes('NaN'), 'no undefined / NaN output');
    assert(!/class="[^"]*\b(bg-|text-slate|shadow-)/.test(h), 'no legacy Tailwind surface classes');
  }

  console.log('\nAbsence interactions');
  {
    const ctx = makeContext();
    ctx.sandbox.STUDENT_MGMT.initAbsenceStats('studentMgmtRoot', 'admin');
    await flush();

    fire(ctx.root, 'input', { target: { id: 'smxSearch', value: 'Sophea' } });
    assert(ctx.root.innerHTML.includes('Sophea Chan') && !ctx.root.innerHTML.includes('Nrinphouneta Hok'),
           'search filters the risk register');

    fire(ctx.root, 'click', { target: targetNode({ 'data-tab': 'critical' }) });
    assert(ctx.root.innerHTML.includes('smx-tab active'), 'risk tab re-renders active state');

    fire(ctx.root, 'click', { target: targetNode({ 'data-act': 'log', 'data-id': 'STD-001' }) });
    const modal = ctx.created.find(el => String(el.className).includes('smx-modal-backdrop'));
    assert(modal && modal.innerHTML.includes('Absence Log') && modal.innerHTML.includes('Recorded absence events'),
           'absence log modal is complete');

    fire(ctx.root, 'click', { target: targetNode({ 'data-act': 'notify', 'data-id': 'STD-001' }) });
    await flush();
    assert(ctx.posts.some(p => p.url.indexOf('/notify') !== -1 && p.body.studentIds.length === 1),
           'guardian notice posts to the live notify endpoint');
    assert(ctx.root.innerHTML.includes('Dispatched'), 'notice status updates after dispatch');
    assert(!ctx.root.innerHTML.includes('undefined') && !ctx.root.innerHTML.includes('NaN'),
           'interactions produce no undefined / NaN output');
  }

  console.log(failures ? `\n${failures} check(s) FAILED` : '\nAll workspace checks passed.');
  process.exit(failures ? 1 : 0);
}

main().catch(e => { console.error(e.stack || e); process.exit(1); });
