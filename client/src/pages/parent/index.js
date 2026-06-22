/* Parent portal pages (§12.3) — multi-child with a child switcher. */
import { icon } from '../../modules/icons.js';
import { USERS, CHILDREN, FEES, SMART_ALERTS, GRADES, EXAMS, ASSIGNMENTS, ANNOUNCEMENTS } from '../../data/mock.js';
import { esc, pageHead, statCard, badge, progress, ringChart, toast, avatar, attBadge } from '../../components/ui.js';

const u = USERS.parent;
let active = CHILDREN[0];

function childSwitcher() {
  return `<div class="segmented" id="child-switch">
    ${CHILDREN.map((c, i) => `<button class="${c.id === active.id ? 'active' : ''}" data-child="${c.id}">${esc(c.name.split(' ')[0])}</button>`).join('')}
  </div>`;
}
function wireSwitch(m, rerender) {
  const sw = m.querySelector('#child-switch'); if (!sw) return;
  sw.querySelectorAll('[data-child]').forEach((b) => b.addEventListener('click', () => {
    active = CHILDREN.find((c) => c.id === b.dataset.child); rerender(m);
  }));
}

export function dashboard(m) {
  m.innerHTML = pageHead({ title: `Hello, ${u.name.split(' ')[0]}`, subtitle: `${CHILDREN.length} children · ${active.name}`, actions: childSwitcher() }) + `
  <div class="grid grid-stats" style="margin-bottom:var(--space-5)">
    ${statCard({ label: "Today's attendance", value: 'Present', icon: 'check' })}
    ${statCard({ label: 'GPA', value: active.gpa.toFixed(2), icon: 'award' })}
    ${statCard({ label: 'Pending assignments', value: String(active.pendingAssignments), icon: 'clipboard' })}
    ${statCard({ label: 'Outstanding fees', value: active.fees ? '$' + active.fees : '$0', icon: 'wallet', delta: active.fees ? 'Due Jul 1' : 'All paid', deltaDir: active.fees ? 'down' : 'up' })}
  </div>
  <div class="grid grid-3">
    <div class="card span-2"><div class="card-header"><h3>Smart alerts</h3><span class="badge badge-danger">${SMART_ALERTS.filter((a) => a.level === 'danger').length} urgent</span></div>
      <div class="card-body col gap-3" style="padding-top:var(--space-3)">
        ${SMART_ALERTS.map((a) => `<div class="list-row">
          <div class="state-icon" style="width:38px;height:38px;background:var(--${a.level}-soft);color:var(--${a.level}-fg)">${icon(a.icon)}</div>
          <div class="grow"><div style="font-weight:600">${esc(a.title)}</div><div class="text-muted" style="font-size:var(--text-sm)">${esc(a.text)}</div></div>
          ${badge(a.child.split(' ')[0], a.level === 'danger' ? 'danger' : a.level === 'warning' ? 'warning' : 'success')}</div>`).join('')}
      </div></div>
    <div class="card center" style="padding:var(--space-6)"><div class="col center gap-3">
      ${ringChart(active.attendance, { label: 'Attendance', color: active.attendance >= 90 ? 'var(--success)' : 'var(--warning)' })}
      <strong>${esc(active.name)}</strong><span class="text-muted" style="font-size:var(--text-sm)">Class ${esc(active.class)}</span>
    </div></div>
  </div>`;
  wireSwitch(m, dashboard);
}

export function children(m) {
  m.innerHTML = pageHead({ title: 'My Children' }) + `
  <div class="grid grid-2">${CHILDREN.map((c) => `<div class="card card-pad">
    <div class="row gap-4">${avatar(c.initials, 'avatar-xl')}
      <div class="grow"><h3 style="font-size:var(--text-lg)">${esc(c.name)}</h3>
      <div class="text-muted" style="font-size:var(--text-sm)">${esc(c.id)} · Class ${esc(c.class)} · Grade ${c.grade}</div>
      <div class="row gap-2" style="margin-top:var(--space-3)">${badge('GPA ' + c.gpa.toFixed(2), 'accent')}${badge(c.attendance + '% attendance', c.attendance >= 90 ? 'success' : 'warning')}${c.fees ? badge('$' + c.fees + ' due', 'danger') : badge('Fees clear', 'success')}</div></div>
    </div>
    <hr class="divider"><button class="btn btn-secondary btn-block btn-sm">${icon('chart')} View full progress</button>
  </div>`).join('')}</div>`;
}

export function attendance(m) {
  m.innerHTML = pageHead({ title: 'Attendance', subtitle: active.name, actions: childSwitcher() }) + `
  <div class="grid grid-4" style="margin-bottom:var(--space-5)">
    ${statCard({ label: 'Present', value: '88', icon: 'checkCircle' })}
    ${statCard({ label: 'Late', value: '4', icon: 'clock' })}
    ${statCard({ label: 'Absent', value: '3', icon: 'xCircle' })}
    ${statCard({ label: 'Rate', value: active.attendance + '%', icon: 'percent' })}
  </div>
  <div class="card"><div class="card-header"><h3>Recent records</h3></div><div class="table-wrap"><table class="table">
    <thead><tr><th>Date</th><th>Status</th><th>Class</th><th>Note</th></tr></thead><tbody>
    ${[['Jun 20', 'present'], ['Jun 19', 'excused'], ['Jun 18', 'absent'], ['Jun 17', 'present'], ['Jun 14', 'late']].map(([d, s]) => `<tr><td>${d}</td><td>${attBadge(s)}</td><td>10-B</td><td class="text-muted">${s === 'excused' ? 'Doctor appointment' : s === 'late' ? '12 min late' : '—'}</td></tr>`).join('')}
    </tbody></table></div></div>`;
  wireSwitch(m, attendance);
}

export function grades(m) {
  m.innerHTML = pageHead({ title: 'Grades & Exams', subtitle: `${active.name} · GPA ${active.gpa.toFixed(2)}`, actions: childSwitcher() }) + `
  <div class="card" style="margin-bottom:var(--space-5)"><div class="card-header"><h3>Subject performance</h3>
    <button class="btn btn-secondary btn-sm">${icon('download')} Report card</button></div>
  <div class="table-wrap"><table class="table"><thead><tr><th>Subject</th><th>Score</th><th>Grade</th><th>Progress</th><th>Comment</th></tr></thead>
  <tbody>${GRADES.map((g) => `<tr><td style="font-weight:600">${esc(g.subject)}</td><td class="nums">${g.score}/${g.max}</td>
    <td>${badge(g.grade, g.grade.startsWith('A') ? 'success' : g.grade.startsWith('B') ? 'accent' : 'warning')}</td>
    <td style="min-width:120px">${progress(g.score, g.score >= 85 ? 'success' : '')}</td>
    <td class="text-muted" style="font-size:var(--text-sm)">${esc(g.comment)}</td></tr>`).join('')}</tbody></table></div></div>
  <div class="card"><div class="card-header"><h3>Upcoming exams</h3></div><div class="card-body col gap-2" style="padding-top:var(--space-3)">
    ${EXAMS.filter((e) => e.status === 'upcoming').map((e) => `<div class="list-row"><div class="grow"><div style="font-weight:600">${esc(e.subject)}</div><div class="text-muted" style="font-size:var(--text-sm)">${esc(e.name)}</div></div>${badge(new Date(e.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }), 'info')}</div>`).join('')}
  </div></div>`;
  wireSwitch(m, grades);
}

export function assignmentsPage(m) {
  m.innerHTML = pageHead({ title: 'Assignments', subtitle: active.name, actions: childSwitcher() }) + `
  <div class="card"><div class="table-wrap"><table class="table"><thead><tr><th>Title</th><th>Subject</th><th>Due</th><th>Status</th></tr></thead>
  <tbody>${ASSIGNMENTS.map((a) => { const v = a.status === 'overdue' ? 'danger' : a.status === 'submitted' ? 'success' : 'warning';
    return `<tr><td style="font-weight:600">${esc(a.title)}</td><td>${esc(a.subject)}</td><td>${new Date(a.due).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}</td><td>${badge(cap(a.status), v)}</td></tr>`; }).join('')}
  </tbody></table></div></div>`;
  wireSwitch(m, assignmentsPage);
}

export function fees(m) {
  const pct = Math.round(FEES.paid / FEES.total * 100);
  m.innerHTML = pageHead({ title: 'Fees & Payments', subtitle: 'Recording & history (online gateway in Phase 3)',
    actions: `<button class="btn btn-primary btn-sm">${icon('creditCard')} Record payment</button>` }) + `
  <div class="grid grid-4" style="margin-bottom:var(--space-5)">
    ${statCard({ label: 'Total fees', value: '$' + FEES.total.toLocaleString(), icon: 'wallet' })}
    ${statCard({ label: 'Paid', value: '$' + FEES.paid.toLocaleString(), icon: 'checkCircle' })}
    ${statCard({ label: 'Remaining', value: '$' + FEES.remaining.toLocaleString(), icon: 'clock' })}
    ${statCard({ label: 'Collected', value: pct + '%', icon: 'percent' })}
  </div>
  <div class="card" style="margin-bottom:var(--space-5)"><div class="card-body">
    <div class="row spread" style="margin-bottom:var(--space-2)"><span class="section-title">Payment progress</span><span class="text-muted">${pct}%</span></div>
    ${progress(pct, 'success')}</div></div>
  <div class="card"><div class="card-header"><h3>Fee breakdown</h3></div><div class="table-wrap"><table class="table">
    <thead><tr><th>Item</th><th>Amount</th><th>Due</th><th>Status</th><th></th></tr></thead><tbody>
    ${FEES.items.map((f) => `<tr><td style="font-weight:600">${esc(f.label)}</td><td class="nums">$${f.amount.toLocaleString()}</td>
      <td>${new Date(f.due).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}</td>
      <td>${f.status === 'paid' ? badge('Paid', 'success') : badge('Pending', 'warning')}</td>
      <td>${f.status === 'paid' ? `<button class="btn btn-ghost btn-sm" data-rcpt>${icon('download')} Receipt</button>` : `<button class="btn btn-primary btn-sm">Pay</button>`}</td></tr>`).join('')}
    </tbody></table></div></div>`;
  m.querySelectorAll('[data-rcpt]').forEach((b) => b.addEventListener('click', () => toast('Receipt downloaded', { type: 'success' })));
}

export function messages(m) {
  const threads = [
    { who: 'Ms. Bello', role: 'Mathematics Teacher', last: 'Leo did very well on the last problem set.', time: '2h', unread: true, initials: 'AB' },
    { who: 'Admin Office', role: 'Administration', last: 'Your fee receipt for Term 2 is attached.', time: '1d', unread: true, initials: 'AO' },
    { who: 'Mr. Adeyemi', role: 'English Teacher', last: 'Please encourage more reading at home.', time: '3d', unread: false, initials: 'MA' },
  ];
  m.innerHTML = pageHead({ title: 'Messages', actions: `<button class="btn btn-primary btn-sm">${icon('plus')} New message</button>` }) + `
  <div class="card"><div class="col">${threads.map((t) => `<div class="list-row" style="padding:var(--space-4) var(--space-5);cursor:pointer">
    ${avatar(t.initials)}<div class="grow"><div class="row spread"><strong style="font-size:var(--text-sm)">${esc(t.who)}</strong><span class="text-muted" style="font-size:var(--text-xs)">${t.time}</span></div>
    <div class="text-muted" style="font-size:var(--text-xs)">${esc(t.role)}</div>
    <div style="font-size:var(--text-sm);margin-top:2px;${t.unread ? 'font-weight:600' : 'color:var(--text-muted)'}">${esc(t.last)}</div></div>
    ${t.unread ? '<span class="dot" style="width:8px;height:8px;border-radius:50%;background:var(--accent)"></span>' : ''}</div>`).join('')}</div></div>`;
}

export function announcements(m) {
  m.innerHTML = pageHead({ title: 'Announcements' }) + `<div class="col gap-3">
    ${[...ANNOUNCEMENTS].sort((a, b) => b.pinned - a.pinned).map((a) => `<div class="card card-pad">
      <div class="row spread"><div class="row gap-2">${a.pinned ? icon('pin') : ''}<strong>${esc(a.title)}</strong>${badge(a.category, a.category === 'emergency' ? 'danger' : 'accent')}</div>
      <button class="btn btn-ghost btn-sm">Mark read</button></div>
      <p class="text-muted" style="margin-top:var(--space-2);font-size:var(--text-sm)">${esc(a.body)}</p></div>`).join('')}</div>`;
}

export function calendar(m) {
  const events = [['25', 'JUN', 'Mathematics Mid-Term', 'exam'], ['28', 'JUN', 'Science Fair', 'event'], ['10', 'JUL', 'Parent–Teacher Meeting', 'meeting'], ['15', 'JUL', 'Sports Day', 'event']];
  m.innerHTML = pageHead({ title: 'Calendar' }) + `<div class="card"><div class="card-body col gap-3">
    ${events.map(([d, mo, t, ty]) => `<div class="list-row"><div class="muted-card" style="text-align:center;min-width:56px;padding:var(--space-2)">
      <div style="font-weight:700;font-size:var(--text-lg)">${d}</div><div class="text-muted" style="font-size:11px">${mo}</div></div>
      <div class="grow" style="font-weight:600">${t}</div>${badge(cap(ty), ty === 'exam' ? 'danger' : ty === 'meeting' ? 'info' : 'accent')}</div>`).join('')}
  </div></div>`;
}

function cap(s) { return s[0].toUpperCase() + s.slice(1); }
