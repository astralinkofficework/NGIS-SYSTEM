#!/usr/bin/env node
/* ============================================================================
 * Khmer School Admin Suite — headless DOM render + interaction test
 * ============================================================================
 * Runs the real data layer, engine and UI renderer inside a minimal DOM shim.
 * No browser, no npm dependencies. Verifies:
 *   1. all 5 modules render for principal and admin without runtime errors
 *   2. the Timetable Builder has its restored executive title, 4 derived KPI
 *      tiles, module navigation, bottom insights and a scrollable grid
 *   3. KPI numbers come from the live engine (never hardcoded)
 *   4. view-mode / cohort switching and auto-schedule keep the chrome in sync
 *   5. Ctrl+Z / Ctrl+Y still work
 *
 * Run:  node tests/test_khmer_suite_ui.js
 * ==========================================================================*/
'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');
const SOURCES = [
  'assets/js/khmer-suite-data.js',
  'assets/js/khmer-suite-engine.js',
  'assets/js/khmer-suite-ui.js'
].map(f => [f, fs.readFileSync(path.join(ROOT, f), 'utf8')]);

const CSS = fs.readFileSync(path.join(ROOT, 'assets/css/khmer-suite.css'), 'utf8');
const MODULES = ['wizard', 'builder', 'viewer', 'subjects', 'records'];
let failures = 0;

function assert(cond, label) {
  if (!cond) { failures++; console.log('   FAIL: ' + label); }
  return cond;
}

/** Build one isolated browser-ish context and return its handles. */
function makeContext(role, module) {
  const errors = [];
  const handlers = { root: {}, doc: {} };
  const store = {};
  let html = '';

  const fakeEl = () => ({
    className: '', textContent: '', innerHTML: '', id: '', style: {},
    classList: { add() {}, remove() {} },
    appendChild() {}, remove() {}, setAttribute() {}, addEventListener() {},
    querySelector() { return null; }, querySelectorAll() { return []; }
  });

  const root = {
    addEventListener(type, fn) { (handlers.root[type] ||= []).push(fn); },
    contains() { return true; },
    querySelector() { return null; },
    querySelectorAll() { return []; },
    set innerHTML(v) { html = v; },
    get innerHTML() { return html; }
  };

  const sandbox = {
    console: {
      log() {}, warn() {},
      error(e) { errors.push(String((e && e.stack) || e)); }
    },
    setTimeout, clearTimeout, TextEncoder, Uint8Array, ArrayBuffer, DataView,
    localStorage: {
      getItem(k) { return store[k] === undefined ? null : store[k]; },
      setItem(k, v) { store[k] = String(v); },
      removeItem(k) { delete store[k]; }
    },
    // Simulate offline: engine must fall back to its local seed state.
    fetch() { return Promise.resolve({ ok: false, status: 0, json: () => Promise.resolve({}) }); },
    requestAnimationFrame(fn) { fn(); return 1; },
    location: { href: '' },
    navigator: { onLine: false },
    confirm() { return true; },
    alert() {},
    document: {
      readyState: 'complete',
      visibilityState: 'visible',
      getElementById(id) { return id === 'ks-root' ? root : null; },
      querySelector() { return null; },
      querySelectorAll() { return []; },
      addEventListener(type, fn) { (handlers.doc[type] ||= []).push(fn); },
      createElement() { return fakeEl(); },
      head: { appendChild() {} },
      body: { appendChild() {} }
    },
    PAGE: { role, active: 'ks-' + module },
    KS_MODULE: module
  };
  sandbox.window = sandbox;
  sandbox.globalThis = sandbox;
  vm.createContext(sandbox);

  for (const [file, code] of SOURCES) {
    vm.runInContext(code, sandbox, { filename: file });
  }

  function fire(type, dataset, extra) {
    const mixin = extra || {};
    const node = Object.assign({ dataset, tagName: 'DIV' }, mixin);
    node.closest = () => node;
    const event = Object.assign({
      target: node,
      preventDefault() {}, stopPropagation() {},
      ctrlKey: false, metaKey: false, shiftKey: false, key: ''
    }, mixin);
    (handlers.root[type] || []).forEach(fn => fn(event));
    (handlers.doc[type] || []).forEach(fn => fn(event));
    return event;
  }

  return {
    sandbox, errors, fire,
    get html() { return html; },
    run(expression) { return vm.runInContext(expression, sandbox); }
  };
}

/* ── 1. Render matrix ───────────────────────────────────────────────────── */
console.log('Render matrix (5 modules x 2 roles)');
for (const role of ['principal', 'admin']) {
  for (const module of MODULES) {
    let ctx;
    try { ctx = makeContext(role, module); ctx.run('KSSuite.render();'); }
    catch (e) { failures++; console.log(`FAIL  ${role}/${module}: ${e.stack}`); continue; }
    const h = ctx.html;
    const checks = [
      ctx.errors.length === 0,
      h.length > 1000,
      !h.includes('undefined'),
      !h.includes('NaN')
    ];
    const ok = checks.every(Boolean);
    if (!ok) failures++;
    console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${role.padEnd(9)} ${module.padEnd(8)} html=${String(h.length).padStart(6)} errors=${ctx.errors.length}`);
    if (ctx.errors.length) console.log('        ' + ctx.errors[0].split('\n').slice(0, 2).join(' | '));
  }
}

/* ── 2. Builder page chrome (restored title / KPI / nav / insights) ─────── */
console.log('\nBuilder executive chrome');
{
  const ctx = makeContext('principal', 'builder');
  ctx.run('KSSuite.render();');
  const h = ctx.html;
  const stats = ctx.run('KSEngine.stats()');

  assert(h.includes('ks-exec-head'), 'executive header section exists');
  assert(h.includes('ks-page-title'), 'H1 page title exists');
  assert(h.includes('>Timetable Builder<'), 'title reads Timetable Builder');
  assert(h.includes('MODULE 02'), 'module eyebrow exists');
  assert(h.includes('AY 2026'), 'academic year tag uses the app label style');
  assert(h.includes('Zero conflicts'), 'live conflict badge exists');
  assert(h.includes('ks-kpi-strip'), 'KPI strip exists');
  assert((h.match(/class="ks-kpi"/g) || []).length === 4, 'exactly 4 KPI tiles');
  assert(h.includes(String(stats.placed)) && h.includes(String(stats.total_demand)),
         'KPI values come from the live engine');
  assert(h.includes('ks-modules') && h.includes('principal-timetables.html'),
         'module navigation links to role-specific pages');
  assert(h.includes('ks-insights') && h.includes('Weekly Load by Day') &&
         h.includes('Subject Legend') && h.includes('Recent Changes'),
         'bottom insights row is complete');
  assert(h.includes('ks-builder-toolbar'), 'toolbar has responsive hook');
  assert(h.includes('ks-timetable-container bg-white rounded-2xl border border-slate-200/80 shadow-xs overflow-x-auto'),
         'weekly grid scrolls inside its card instead of being clipped');
  assert(!/>\s*undefined\s*</.test(h), 'no undefined text nodes');
}

/* ── 3. Admin builder has the same chrome ───────────────────────────────── */
{
  const ctx = makeContext('admin', 'builder');
  ctx.run('KSSuite.render();');
  assert(ctx.html.includes('ks-exec-head'), 'admin builder has the executive header');
  assert(ctx.html.includes('admin-timetables.html'), 'admin module links use admin pages');
  assert((ctx.html.match(/class="ks-kpi"/g) || []).length === 4, 'admin builder has 4 KPI tiles');
}

/* ── 4. Interactions keep the derived chrome in sync ────────────────────── */
console.log('\nBuilder interactions');
{
  const ctx = makeContext('principal', 'builder');
  ctx.run('KSSuite.render();');
  const stats = () => ctx.run('KSEngine.stats()');

  ctx.fire('click', { act: 'set-view-mode', id: 'teacher' });
  assert(ctx.run('KSSuite.local.viewMode') === 'teacher', 'teacher view switches');
  assert(ctx.html.includes('ks-exec-head'), 'chrome survives view switch');
  ctx.fire('click', { act: 'set-view-mode', id: 'class' });
  assert(ctx.run('KSSuite.local.viewMode') === 'class', 'class view switches back');

  ctx.fire('click', { act: 'set-class-cohort', id: 'class_8A' });
  assert(ctx.run('KSSuite.local.selectedClass') === 'class_8A', 'cohort pill switches class');

  const before = stats().unassigned;
  ctx.fire('click', { act: 'auto-schedule-current' });
  const after = stats().unassigned;
  assert(after < before, 'auto-schedule places lessons (' + before + ' -> ' + after + ')');
  assert(ctx.html.includes(String(after)), 'KPI re-renders with the new derived value');
  assert(stats().conflicts === 0, 'auto-schedule creates no hard conflicts');

  ctx.fire('keydown', {}, { tagName: 'BODY', key: 'z', ctrlKey: true });
  assert(stats().unassigned === before, 'Ctrl+Z restores the unassigned count');
  ctx.fire('keydown', {}, { tagName: 'BODY', key: 'y', ctrlKey: true });
  assert(stats().unassigned === after, 'Ctrl+Y re-applies auto-schedule');
  assert(ctx.errors.length === 0, 'no runtime errors during interactions');
  if (ctx.errors.length) console.log('        ' + ctx.errors[0].split('\n').slice(0, 2).join(' | '));
}

/* ── 5. Design-system conformance of the shared stylesheet ──────────────── */
console.log('\nDesign-system conformance');
{
  assert(CSS.split('{').length === CSS.split('}').length, 'balanced CSS braces');
  assert(!CSS.includes('font-weight: 600') && !CSS.includes('font-weight: 700'),
         'no 600/700 font weights (AGENTS.md)');
  assert(!CSS.includes('linear-gradient'), 'no decorative gradients (DESIGN-RULES)');
  assert(CSS.includes('#ks-root .ks-exec-head'), 'executive header is token-scoped');
  assert(CSS.includes('@media (max-width: 760px)'), 'mobile breakpoint exists');
  assert(CSS.includes('overflow-x: auto'), 'scrollable grid rule exists');
}

console.log(failures ? `\n${failures} check(s) FAILED` : '\nAll UI checks passed.');
process.exit(failures ? 1 : 0);
