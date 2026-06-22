/* Student portal pages (§12.1). Each export renders into the content slot. */
import { icon } from '../../modules/icons.js';
import {
  USERS, TIMETABLE, DAYS, PERIODS, GRADES, EXAMS, ASSIGNMENTS,
  ANNOUNCEMENTS, ATTENDANCE_MONTH, ATTENDANCE_SUMMARY, SCHOOL,
} from '../../data/mock.js';
import {
  esc, pageHead, statCard, badge, attBadge, progress, toast,
  lineChart, ringChart, emptyState,
} from '../../components/ui.js';

const u = USERS.student;
const today = 'Mon';

/* --------------------------------- Dashboard ------------------------------ */
export function dashboard(m) {
  const classes = TIMETABLE[today].map((c, i) => ({ ...c, time: PERIODS[i].time })).filter((c) => c.code);
  const upcoming = EXAMS.filter((e) => e.status === 'upcoming').slice(0, 3);
  const pinned = ANNOUNCEMENTS.filter((a) => a.pinned);

  m.innerHTML = pageHead({
    title: `Good morning, ${u.name.split(' ')[0]}`,
    subtitle: `${SCHOOL.year} · ${SCHOOL.term} · Class ${u.class}`,
    actions: `<button class="btn btn-secondary btn-sm">${icon('download')} Report card</button>
              <button class="btn btn-primary btn-sm">${icon('clipboard')} Open assignments</button>`,
  }) + `
  <div class="grid grid-stats" style="margin-bottom:var(--space-5)">
    ${statCard({ label: 'Attendance', value: ATTENDANCE_SUMMARY.rate + '%', icon: 'check', delta: '1.2% vs last term', deltaDir: 'up' })}
    ${statCard({ label: 'GPA', value: u.gpa.toFixed(2), icon: 'award', delta: '0.06', deltaDir: 'up' })}
    ${statCard({ label: 'Pending assignments', value: '3', icon: 'clipboard' })}
    ${statCard({ label: 'Upcoming exams', value: String(upcoming.length), icon: 'calendar' })}
  </div>

  <div class="grid grid-3">
    <div class="card span-2">
      <div class="card-header"><h3>Today’s classes · ${today}</h3><span class="badge badge-accent">${classes.length} periods</span></div>
      <div class="card-body col gap-2" style="padding-top:var(--space-3)">
        ${classes.map((c) => `
          <div class="list-row">
            <span class="tt-time" style="width:96px">${esc(c.time)}</span>
            <span style="width:4px;height:36px;border-radius:4px;background:${c.color}"></span>
            <div class="grow"><div style="font-weight:600">${esc(c.name)}</div>
            <div class="text-muted" style="font-size:var(--text-sm)">${esc(c.teacher)} · ${esc(c.room)}</div></div>
            ${badge(c.code, 'accent')}
          </div>`).join('')}
      </div>
    </div>

    <div class="card">
      <div class="card-header"><h3>Upcoming exams</h3></div>
      <div class="card-body col gap-3" style="padding-top:var(--space-3)">
        ${upcoming.map((e) => `
          <div class="list-row">
            <div class="state-icon" style="width:38px;height:38px;background:var(--accent-soft);color:var(--accent-soft-fg)">${icon('calendar')}</div>
            <div class="grow"><div style="font-weight:600">${esc(e.subject)}</div>
            <div class="text-muted" style="font-size:var(--text-sm)">${esc(e.name)}</div></div>
            <span class="badge">${esc(fmtDate(e.date))}</span>
          </div>`).join('')}
      </div>
    </div>
  </div>

  <div class="grid grid-2" style="margin-top:var(--space-5)">
    <div class="card">
      <div class="card-header"><h3>Attendance trend</h3><span class="text-muted" style="font-size:var(--text-sm)">Last 5 weeks</span></div>
      <div class="card-body">${lineChart([94, 96, 91, 88, 93], { labels: ['W1', 'W2', 'W3', 'W4', 'W5'], color: 'var(--chart-1)' })}</div>
    </div>
    <div class="card">
      <div class="card-header"><h3>Pinned announcements</h3></div>
      <div class="card-body col gap-3" style="padding-top:var(--space-3)">
        ${pinned.map((a) => `<div class="muted-card">
          <div class="row spread"><strong style="font-size:var(--text-sm)">${esc(a.title)}</strong>${badge(a.category, catVariant(a.category))}</div>
          <p class="text-muted" style="font-size:var(--text-sm);margin-top:4px">${esc(a.body)}</p></div>`).join('')}
      </div>
    </div>
  </div>`;
}

/* --------------------------------- Timetable ------------------------------ */
export function timetable(m) {
  m.innerHTML = pageHead({ title: 'Timetable', subtitle: 'Your weekly class schedule',
    actions: `<div class="segmented"><button class="active">Week</button><button>Day</button></div>` }) + `
  <div class="card card-pad" style="overflow-x:auto">
    <table class="timetable">
      <thead><tr><th style="width:90px"></th>${DAYS.map((d) => `<th${d === today ? ' style="color:var(--accent)"' : ''}>${d}</th>`).join('')}</tr></thead>
      <tbody>
        ${PERIODS.map((p, pi) => `<tr>
          <td class="tt-time">P${p.p}<br><span style="opacity:.7">${esc(p.time)}</span></td>
          ${DAYS.map((d) => {
            const c = TIMETABLE[d][pi];
            return `<td>${c && c.code ? `<div class="tt-cell filled" style="border-left:3px solid ${c.color}">
              <div class="subj">${esc(c.code)}</div><div class="meta">${esc(c.room)}</div></div>`
              : `<div class="tt-cell"></div>`}</td>`;
          }).join('')}
        </tr>`).join('')}
      </tbody>
    </table>
  </div>`;
}

/* -------------------------------- Attendance ------------------------------ */
export function attendance(m) {
  const s = ATTENDANCE_SUMMARY;
  const dows = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'];
  m.innerHTML = pageHead({ title: 'Attendance', subtitle: 'June 2026' }) + `
  <div class="grid grid-4" style="margin-bottom:var(--space-5)">
    ${statCard({ label: 'Present', value: s.present, icon: 'checkCircle' })}
    ${statCard({ label: 'Late', value: s.late, icon: 'clock' })}
    ${statCard({ label: 'Absent', value: s.absent, icon: 'xCircle' })}
    ${statCard({ label: 'Excused', value: s.excused, icon: 'info' })}
  </div>
  <div class="grid grid-3">
    <div class="card span-2">
      <div class="card-header"><h3>Monthly calendar</h3>
        <div class="legend">
          <span class="legend-item"><span class="sw" style="background:var(--att-present)"></span>Present</span>
          <span class="legend-item"><span class="sw" style="background:var(--att-late)"></span>Late</span>
          <span class="legend-item"><span class="sw" style="background:var(--att-absent)"></span>Absent</span>
          <span class="legend-item"><span class="sw" style="background:var(--att-excused)"></span>Excused</span>
        </div>
      </div>
      <div class="card-body">
        <div class="cal">
          ${dows.map((d) => `<div class="cal-dow">${d}</div>`).join('')}
          ${Array.from({ length: 7 }).map(() => '<div class="cal-day empty"></div>').join('')}
          ${Object.entries(ATTENDANCE_MONTH).map(([d, st]) => `
            <div class="cal-day ${st || ''}">${d}${st ? '<span class="d-mark"></span>' : ''}</div>`).join('')}
        </div>
      </div>
    </div>
    <div class="card center" style="padding:var(--space-6)">
      <div class="col center gap-4">
        ${ringChart(Math.round(s.rate), { label: 'Overall', color: 'var(--success)' })}
        <p class="text-muted" style="text-align:center;font-size:var(--text-sm)">Above the 90% attendance target. Keep it up!</p>
      </div>
    </div>
  </div>`;
}

/* ---------------------------------- Grades -------------------------------- */
export function grades(m) {
  m.innerHTML = pageHead({ title: 'Grades & Exams', subtitle: `GPA ${u.gpa.toFixed(2)} · ${SCHOOL.term}`,
    actions: `<button class="btn btn-primary btn-sm">${icon('download')} Download report card</button>` }) + `
  <div class="grid grid-3" style="margin-bottom:var(--space-5)">
    ${statCard({ label: 'Semester GPA', value: u.gpa.toFixed(2), icon: 'award' })}
    ${statCard({ label: 'Class rank', value: '4 / 29', icon: 'trend' })}
    ${statCard({ label: 'Best subject', value: 'CS · A+', icon: 'star' })}
  </div>
  <div class="card" style="margin-bottom:var(--space-5)">
    <div class="card-header"><h3>Subject grades</h3></div>
    <div class="table-wrap"><table class="table">
      <thead><tr><th>Subject</th><th>Score</th><th>Grade</th><th>Semester avg</th><th>Progress</th><th>Teacher comment</th></tr></thead>
      <tbody>
        ${GRADES.map((g) => `<tr>
          <td style="font-weight:600">${esc(g.subject)}</td>
          <td class="nums">${g.score}/${g.max}</td>
          <td>${badge(g.grade, gradeVariant(g.grade))}</td>
          <td class="nums">${g.semesterAvg}%</td>
          <td style="min-width:120px">${progress(g.score, g.score >= 85 ? 'success' : g.score >= 70 ? '' : 'warning')}</td>
          <td class="text-muted" style="font-size:var(--text-sm)">${esc(g.comment)}</td>
        </tr>`).join('')}
      </tbody>
    </table></div>
  </div>
  <div class="card">
    <div class="card-header"><h3>Exam schedule</h3></div>
    <div class="table-wrap"><table class="table">
      <thead><tr><th>Exam</th><th>Subject</th><th>Date</th><th>Max</th><th>Result</th></tr></thead>
      <tbody>
        ${EXAMS.map((e) => `<tr>
          <td style="font-weight:600">${esc(e.name)}</td><td>${esc(e.subject)}</td>
          <td>${esc(fmtDate(e.date))}</td><td class="nums">${e.max}</td>
          <td>${e.status === 'completed' ? `<span class="nums">${e.score}/${e.max}</span>` : badge('Upcoming', 'info')}</td>
        </tr>`).join('')}
      </tbody>
    </table></div>
  </div>`;
}

/* ------------------------------- Assignments ------------------------------ */
export function assignments(m) {
  const counts = { all: ASSIGNMENTS.length, pending: 0, submitted: 0, overdue: 0 };
  ASSIGNMENTS.forEach((a) => counts[a.status]++);
  const filters = ['all', 'pending', 'submitted', 'overdue'];

  m.innerHTML = pageHead({ title: 'Assignments', subtitle: `${counts.pending} pending · ${counts.overdue} overdue` }) + `
  <div class="row spread wrap gap-3" style="margin-bottom:var(--space-4)">
    <div class="tabs" id="asg-tabs">
      ${filters.map((f, i) => `<button class="tab ${i === 0 ? 'active' : ''}" data-filter="${f}">${cap(f)} <span class="text-muted">(${counts[f]})</span></button>`).join('')}
    </div>
    <div class="input-group" style="max-width:260px">${icon('search')}<input class="input" placeholder="Search assignments…" data-asg-search></div>
  </div>
  <div class="grid grid-2" id="asg-list"></div>`;

  const list = m.querySelector('#asg-list');
  let filter = 'all', q = '';
  const draw = () => {
    const rows = ASSIGNMENTS.filter((a) => (filter === 'all' || a.status === filter) && a.title.toLowerCase().includes(q));
    if (!rows.length) { list.innerHTML = `<div class="span-2">${emptyState({ icon: 'clipboard', title: 'No assignments', text: 'Nothing matches this filter.' })}</div>`; return; }
    list.innerHTML = rows.map((a) => {
      const v = a.status === 'overdue' ? 'danger' : a.status === 'submitted' ? 'success' : 'warning';
      const days = daysUntil(a.due);
      return `<div class="card card-hover card-pad col gap-3">
        <div class="row spread"><span class="badge badge-accent">${esc(a.subject)}</span>${badge(cap(a.status), v)}</div>
        <div><div style="font-weight:600">${esc(a.title)}</div><div class="text-muted" style="font-size:var(--text-sm)">${esc(a.teacher)}</div></div>
        <div class="row spread">
          <span class="text-muted" style="font-size:var(--text-sm)">${icon('clock')} ${a.status === 'submitted'
            ? `Submitted · ${esc(a.grade || '—')}`
            : days < 0 ? `${Math.abs(days)}d overdue` : `Due in ${days}d · ${esc(fmtDate(a.due))}`}</span>
          <button class="btn btn-sm ${a.status === 'submitted' ? 'btn-secondary' : 'btn-primary'}" data-open="${a.id}">
            ${a.status === 'submitted' ? 'View' : icon('upload') + ' Submit'}</button>
        </div>
      </div>`;
    }).join('');
    list.querySelectorAll('[data-open]').forEach((b) => b.addEventListener('click', () => toast('Submission flow is a Phase 1 deliverable', { type: 'info', title: 'Assignment' })));
  };
  draw();
  m.querySelectorAll('[data-filter]').forEach((t) => t.addEventListener('click', () => {
    m.querySelectorAll('[data-filter]').forEach((x) => x.classList.remove('active'));
    t.classList.add('active'); filter = t.dataset.filter; draw();
  }));
  m.querySelector('[data-asg-search]').addEventListener('input', (e) => { q = e.target.value.toLowerCase(); draw(); });
}

/* --------------------------- Lighter screens ------------------------------ */
export function documents(m) {
  const docs = [
    { name: 'Report Card — Term 1', type: 'report_card', date: '2026-01-15', icon: 'fileText' },
    { name: 'Enrollment Certificate', type: 'certificate', date: '2024-09-01', icon: 'award' },
    { name: 'Exam Slip — Term 2', type: 'exam_slip', date: '2026-06-20', icon: 'file' },
    { name: 'Conduct Letter', type: 'letter', date: '2026-03-10', icon: 'mail' },
  ];
  m.innerHTML = pageHead({ title: 'My Documents', subtitle: 'Downloads use secure, signed links' }) + `
  <div class="grid grid-4">
    ${docs.map((d) => `<div class="card card-hover card-pad col gap-3">
      <div class="state-icon" style="background:var(--accent-soft);color:var(--accent-soft-fg)">${icon(d.icon)}</div>
      <div><div style="font-weight:600">${esc(d.name)}</div><div class="text-muted" style="font-size:var(--text-sm)">${esc(fmtDate(d.date))}</div></div>
      <button class="btn btn-secondary btn-sm btn-block" data-dl>${icon('download')} Download</button>
    </div>`).join('')}
  </div>`;
  m.querySelectorAll('[data-dl]').forEach((b) => b.addEventListener('click', () => toast('Generating signed URL…', { type: 'success', title: 'Download' })));
}

export function announcements(m) {
  const cats = ['all', 'school', 'class', 'exams', 'events', 'emergency'];
  m.innerHTML = pageHead({ title: 'Announcements' }) + `
    <div class="tabs" style="margin-bottom:var(--space-4)">${cats.map((c, i) => `<button class="tab ${i ? '' : 'active'}">${cap(c)}</button>`).join('')}</div>
    <div class="col gap-3">
    ${[...ANNOUNCEMENTS].sort((a, b) => b.pinned - a.pinned).map((a) => `
      <div class="card card-pad">
        <div class="row spread wrap gap-2">
          <div class="row gap-2">${a.pinned ? icon('pin', 'icon') : ''}<strong>${esc(a.title)}</strong>${badge(a.category, catVariant(a.category))}</div>
          <span class="text-muted" style="font-size:var(--text-sm)">${esc(fmtDate(a.date))}</span>
        </div>
        <p style="margin-top:var(--space-2);color:var(--text-secondary)">${esc(a.body)}</p>
        <div class="text-muted" style="font-size:var(--text-sm);margin-top:var(--space-2)">${esc(a.author)} · ${esc(a.scope)}-wide</div>
      </div>`).join('')}
    </div>`;
}

export function calendar(m) {
  const events = [
    { d: '25', mo: 'JUN', title: 'Mathematics Mid-Term', type: 'exam' },
    { d: '28', mo: 'JUN', title: 'Science Fair', type: 'event' },
    { d: '04', mo: 'JUL', title: 'Independence Day — Holiday', type: 'holiday' },
    { d: '10', mo: 'JUL', title: 'Parent–Teacher Meeting', type: 'meeting' },
  ];
  const vmap = { exam: 'danger', event: 'accent', holiday: 'success', meeting: 'info' };
  m.innerHTML = pageHead({ title: 'Calendar', subtitle: 'Holidays, exams & events' }) + `
  <div class="card"><div class="card-header"><h3>Upcoming</h3></div><div class="card-body col gap-3" style="padding-top:var(--space-3)">
    ${events.map((e) => `<div class="list-row">
      <div class="muted-card" style="text-align:center;padding:var(--space-2) var(--space-3);min-width:56px">
        <div style="font-weight:700;font-size:var(--text-lg)">${e.d}</div><div class="text-muted" style="font-size:11px">${e.mo}</div></div>
      <div class="grow" style="font-weight:600">${esc(e.title)}</div>${badge(cap(e.type), vmap[e.type])}
    </div>`).join('')}
  </div></div>`;
}

export function help(m) {
  const faqs = [
    ['How do I download my report card?', 'Go to Grades & Exams and tap “Download report card”. The file is generated as a secure PDF.'],
    ['I can’t submit an assignment.', 'Check the deadline and file type. Supported: PDF, images and docs up to 20MB.'],
    ['How is my GPA calculated?', 'GPA uses a 4.0 scale weighted by subject credits across the current semester.'],
  ];
  m.innerHTML = pageHead({ title: 'Help Center' }) + `
  <div class="grid grid-3" style="margin-bottom:var(--space-5)">
    ${[['help', 'Browse FAQ', 'Common questions answered'], ['flag', 'Report an issue', 'Tell us what went wrong'], ['message', 'Contact administration', 'We reply within 1 school day']]
      .map(([ic, t, s]) => `<div class="card card-hover card-pad col gap-2"><div class="state-icon" style="background:var(--accent-soft);color:var(--accent-soft-fg)">${icon(ic)}</div><strong>${t}</strong><span class="text-muted" style="font-size:var(--text-sm)">${s}</span></div>`).join('')}
  </div>
  <div class="card"><div class="card-header"><h3>Frequently asked questions</h3></div><div class="card-body col gap-4">
    ${faqs.map(([q, a]) => `<div><div style="font-weight:600">${esc(q)}</div><p class="text-muted" style="font-size:var(--text-sm);margin-top:4px">${esc(a)}</p></div>`).join('')}
  </div></div>`;
}

/* --------------------------------- helpers -------------------------------- */
function fmtDate(iso) { return new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }); }
function daysUntil(iso) { return Math.round((new Date(iso) - new Date('2026-06-22')) / 86400000); }
function cap(s) { return s[0].toUpperCase() + s.slice(1); }
function gradeVariant(g) { return g.startsWith('A') ? 'success' : g.startsWith('B') ? 'accent' : g.startsWith('C') ? 'warning' : 'danger'; }
function catVariant(c) { return ({ exams: 'info', emergency: 'danger', events: 'accent', class: 'warning', school: '' })[c] || ''; }
