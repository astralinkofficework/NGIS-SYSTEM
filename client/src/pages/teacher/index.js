/* Teacher portal pages (§12.2). */
import { icon } from '../../modules/icons.js';
import {
  USERS, TIMETABLE, PERIODS, ROSTER, ATTENDANCE_TREND, CLASS_SCORE_DIST,
  ASSIGNMENTS, ANNOUNCEMENTS,
} from '../../data/mock.js';
import {
  esc, pageHead, statCard, badge, progress, toast, lineChart, barChart, avatar, emptyState,
} from '../../components/ui.js';

const u = USERS.teacher;
const today = 'Mon';

export function dashboard(m) {
  const classes = TIMETABLE[today].map((c, i) => ({ ...c, time: PERIODS[i].time })).filter((c) => c.code);
  const atRisk = ROSTER.filter((s) => s.flag === 'at-risk' || s.flag === 'low-attendance');
  m.innerHTML = pageHead({
    title: `Welcome, ${u.name.split(' ')[0]}`, subtitle: u.title,
    actions: `<button class="btn btn-secondary btn-sm">${icon('check')} Take attendance</button>
              <button class="btn btn-primary btn-sm">${icon('plus')} Create assignment</button>`,
  }) + `
  <div class="grid grid-stats" style="margin-bottom:var(--space-5)">
    ${statCard({ label: 'Total students', value: '142', icon: 'users' })}
    ${statCard({ label: 'Classes today', value: String(classes.length), icon: 'calendar' })}
    ${statCard({ label: 'Pending reviews', value: '7', icon: 'clipboard' })}
    ${statCard({ label: 'Avg class score', value: '83%', icon: 'award', delta: '2%', deltaDir: 'up' })}
  </div>
  <div class="grid grid-3">
    <div class="card span-2"><div class="card-header"><h3>Today’s schedule</h3></div>
      <div class="card-body col gap-2" style="padding-top:var(--space-3)">
        ${classes.map((c) => `<div class="list-row">
          <span class="tt-time" style="width:96px">${esc(c.time)}</span>
          <span style="width:4px;height:36px;border-radius:4px;background:${c.color}"></span>
          <div class="grow"><div style="font-weight:600">${esc(c.name)}</div><div class="text-muted" style="font-size:var(--text-sm)">${esc(c.room)} · Class 10-B</div></div>
          <button class="btn btn-secondary btn-sm">Open</button></div>`).join('')}
      </div></div>
    <div class="card"><div class="card-header"><h3>Student insights</h3></div>
      <div class="card-body col gap-3" style="padding-top:var(--space-3)">
        ${atRisk.map((s) => `<div class="list-row">${avatar(s.name.split(' ').map((n) => n[0]).join(''), 'avatar-sm')}
          <div class="grow"><div style="font-weight:600;font-size:var(--text-sm)">${esc(s.name)}</div>
          <div class="text-muted" style="font-size:var(--text-xs)">Attendance ${s.attendance}% · GPA ${s.gpa}</div></div>
          ${badge(s.flag === 'at-risk' ? 'At risk' : 'Low att.', 'danger')}</div>`).join('')}
        <div class="list-row">${avatar('FH', 'avatar-sm')}<div class="grow"><div style="font-weight:600;font-size:var(--text-sm)">Farid Hassan</div><div class="text-muted" style="font-size:var(--text-xs)">GPA 4.0</div></div>${badge('Excellent', 'success')}</div>
      </div></div>
  </div>`;
}

export function classes(m) {
  m.innerHTML = pageHead({ title: 'My Classes', subtitle: 'Class 10-B · Homeroom',
    actions: `<div class="input-group" style="max-width:240px">${icon('search')}<input class="input" placeholder="Search students…" data-rsearch></div>` }) + `
  <div class="card"><div class="card-header"><h3>Roster</h3><span class="badge">${ROSTER.length} students</span></div>
  <div class="table-wrap"><table class="table"><thead><tr><th>Student</th><th>ID</th><th>Attendance</th><th>GPA</th><th>Status</th><th></th></tr></thead>
  <tbody id="rbody">${rosterRows(ROSTER)}</tbody></table></div></div>`;
  m.querySelector('[data-rsearch]').addEventListener('input', (e) => {
    const q = e.target.value.toLowerCase();
    m.querySelector('#rbody').innerHTML = rosterRows(ROSTER.filter((s) => s.name.toLowerCase().includes(q)));
  });
}
function rosterRows(rows) {
  return rows.map((s) => `<tr>
    <td><div class="row gap-3">${avatar(s.name.split(' ').map((n) => n[0]).join(''), 'avatar-sm')}<span style="font-weight:600">${esc(s.name)}</span></div></td>
    <td class="mono text-muted">${esc(s.id)}</td>
    <td style="min-width:130px"><div class="row gap-2">${progress(s.attendance, s.attendance >= 85 ? 'success' : 'warning')}<span class="nums" style="font-size:var(--text-sm)">${s.attendance}%</span></div></td>
    <td class="nums">${s.gpa.toFixed(2)}</td>
    <td>${s.flag === 'excellent' ? badge('Excellent', 'success') : s.flag === 'at-risk' ? badge('At risk', 'danger') : s.flag === 'low-attendance' ? badge('Low att.', 'warning') : badge('On track')}</td>
    <td><button class="btn btn-ghost btn-icon btn-sm">${icon('chevronRight')}</button></td>
  </tr>`).join('');
}

/* ----------------------- Attendance entry (bulk) -------------------------- */
export function attendance(m) {
  m.innerHTML = pageHead({ title: 'Take Attendance', subtitle: 'Class 10-B · Mathematics · Today',
    actions: `<button class="btn btn-secondary btn-sm" data-allp>${icon('check')} Mark all present</button>
              <button class="btn btn-primary btn-sm" data-save>${icon('check')} Save attendance</button>` }) + `
  <div class="card"><div class="card-header"><h3>Roster</h3>
    <div class="legend"><span class="legend-item">P = Present</span><span class="legend-item">L = Late</span><span class="legend-item">A = Absent</span><span class="legend-item">E = Excused</span></div></div>
  <div class="table-wrap"><table class="table"><thead><tr><th>Student</th><th>ID</th><th style="text-align:center">Status</th><th>Note</th></tr></thead>
  <tbody>${ROSTER.map((s) => `<tr data-stu="${s.id}">
    <td><div class="row gap-3">${avatar(s.name.split(' ').map((n) => n[0]).join(''), 'avatar-sm')}<span style="font-weight:600">${esc(s.name)}</span></div></td>
    <td class="mono text-muted">${esc(s.id)}</td>
    <td><div class="att-pills" style="justify-content:center">
      ${['present', 'late', 'absent', 'excused'].map((st) => `<button class="att-pill ${st} ${st === 'present' ? 'on' : ''}" data-st="${st}" aria-label="${st}">${st[0].toUpperCase()}</button>`).join('')}
    </div></td>
    <td><input class="input" placeholder="Optional note" style="height:32px"></td>
  </tr>`).join('')}</tbody></table></div></div>`;

  m.querySelectorAll('tr[data-stu]').forEach((tr) => {
    const pills = tr.querySelectorAll('.att-pill');
    pills.forEach((p) => p.addEventListener('click', () => { pills.forEach((x) => x.classList.remove('on')); p.classList.add('on'); }));
  });
  m.querySelector('[data-allp]').addEventListener('click', () => {
    m.querySelectorAll('tr[data-stu]').forEach((tr) => { tr.querySelectorAll('.att-pill').forEach((p) => p.classList.toggle('on', p.dataset.st === 'present')); });
  });
  m.querySelector('[data-save]').addEventListener('click', () => toast(`Attendance saved for ${ROSTER.length} students`, { type: 'success', title: 'Class 10-B' }));
}

export function grades(m) {
  m.innerHTML = pageHead({ title: 'Grades', subtitle: 'Mathematics · Mid-Term',
    actions: `<button class="btn btn-secondary btn-sm">${icon('upload')} Bulk import</button>
              <button class="btn btn-primary btn-sm" data-save>${icon('check')} Save grades</button>` }) + `
  <div class="card"><div class="card-header"><h3>Enter scores (max 100)</h3></div>
  <div class="table-wrap"><table class="table"><thead><tr><th>Student</th><th style="width:140px">Score</th><th>Grade</th><th>Comment</th></tr></thead>
  <tbody>${ROSTER.map((s) => `<tr>
    <td><div class="row gap-3">${avatar(s.name.split(' ').map((n) => n[0]).join(''), 'avatar-sm')}<span style="font-weight:600">${esc(s.name)}</span></div></td>
    <td><input class="input score" type="number" min="0" max="100" value="${Math.round(s.gpa / 4 * 100)}" style="height:32px;width:90px"></td>
    <td class="gcell">${gradeFromScore(Math.round(s.gpa / 4 * 100))}</td>
    <td><input class="input" placeholder="Optional comment" style="height:32px"></td>
  </tr>`).join('')}</tbody></table></div></div>`;
  m.querySelectorAll('tr').forEach((tr) => {
    const inp = tr.querySelector('.score'); const cell = tr.querySelector('.gcell');
    if (inp) inp.addEventListener('input', () => { cell.innerHTML = gradeFromScore(+inp.value); });
  });
  m.querySelector('[data-save]').addEventListener('click', () => toast('Grades saved & audit-logged', { type: 'success', title: 'Mathematics' }));
}

export function assignmentsPage(m) {
  m.innerHTML = pageHead({ title: 'Assignments', subtitle: 'Created by you',
    actions: `<button class="btn btn-primary btn-sm">${icon('plus')} New assignment</button>` }) + `
  <div class="grid grid-2">${ASSIGNMENTS.map((a) => {
    const v = a.status === 'overdue' ? 'danger' : a.status === 'submitted' ? 'success' : 'warning';
    return `<div class="card card-pad col gap-3"><div class="row spread">${badge(a.subject, 'accent')}${badge(cap(a.status), v)}</div>
      <div style="font-weight:600">${esc(a.title)}</div>
      <div class="row spread"><span class="text-muted" style="font-size:var(--text-sm)">${icon('users')} 142 students</span>
      <button class="btn btn-secondary btn-sm">${icon('clipboard')} Grade submissions</button></div></div>`;
  }).join('')}</div>`;
}

export function documents(m) {
  m.innerHTML = pageHead({ title: 'Documents', subtitle: 'Lesson plans, worksheets & exam papers',
    actions: `<button class="btn btn-primary btn-sm">${icon('upload')} Upload</button>` }) +
    emptyStateCard('folder', 'No documents yet', 'Upload lesson plans, worksheets or exam papers. Version history is kept automatically.');
}

export function analytics(m) {
  m.innerHTML = pageHead({ title: 'Analytics', subtitle: 'Class 10-B · Mathematics' }) + `
  <div class="grid grid-3" style="margin-bottom:var(--space-5)">
    ${statCard({ label: 'Average score', value: '83%', icon: 'award', delta: '2%', deltaDir: 'up' })}
    ${statCard({ label: 'Completion rate', value: '91%', icon: 'check' })}
    ${statCard({ label: 'Attendance', value: '93%', icon: 'users', delta: '1%', deltaDir: 'down' })}
  </div>
  <div class="grid grid-2">
    <div class="card"><div class="card-header"><h3>Attendance trend</h3></div><div class="card-body">${lineChart(ATTENDANCE_TREND, { labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'] })}</div></div>
    <div class="card"><div class="card-header"><h3>Grade distribution</h3></div><div class="card-body">${barChart(CLASS_SCORE_DIST, { color: 'var(--chart-2)' })}</div></div>
  </div>`;
}

export function announcements(m) {
  m.innerHTML = pageHead({ title: 'Announcements', subtitle: 'Post to your classes',
    actions: `<button class="btn btn-primary btn-sm">${icon('plus')} New announcement</button>` }) + `
  <div class="col gap-3">${ANNOUNCEMENTS.filter((a) => a.scope !== 'school' || a.author.includes('Bello')).concat(ANNOUNCEMENTS.slice(0, 2)).slice(0, 3).map((a) => `
    <div class="card card-pad"><div class="row spread"><strong>${esc(a.title)}</strong><div class="row gap-2">${badge(a.category, 'accent')}<button class="btn btn-ghost btn-icon btn-sm">${icon('more')}</button></div></div>
    <p class="text-muted" style="margin-top:var(--space-2);font-size:var(--text-sm)">${esc(a.body)}</p></div>`).join('')}</div>`;
}

/* helpers */
function cap(s) { return s[0].toUpperCase() + s.slice(1); }
function gradeFromScore(n) {
  const g = n >= 95 ? 'A+' : n >= 90 ? 'A' : n >= 85 ? 'A-' : n >= 80 ? 'B+' : n >= 70 ? 'B' : n >= 60 ? 'C' : 'F';
  const v = g.startsWith('A') ? 'success' : g.startsWith('B') ? 'accent' : g === 'C' ? 'warning' : 'danger';
  return badge(g, v);
}
function emptyStateCard(ic, t, s) { return `<div class="card">${emptyState({ icon: ic, title: t, text: s, action: `<button class="btn btn-primary btn-sm" style="margin-top:8px">${icon('upload')} Upload now</button>` })}</div>`; }
