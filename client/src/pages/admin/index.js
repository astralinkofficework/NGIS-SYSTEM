/* Admin panel pages (§12.4). Cannot touch the Super Admin account. */
import { icon } from '../../modules/icons.js';
import { ADMIN_STATS, USER_DIRECTORY, ROLE_LABEL, SUBJECTS, ANNOUNCEMENTS, PERFORMANCE_TREND, SECURITY_LOG } from '../../data/mock.js';
import { esc, pageHead, statCard, badge, progress, avatar, toast, lineChart, emptyState, modal } from '../../components/ui.js';

export function dashboard(m) {
  const s = ADMIN_STATS;
  m.innerHTML = pageHead({ title: 'Admin Dashboard', subtitle: 'Northgate International School',
    actions: `<button class="btn btn-secondary btn-sm">${icon('download')} Export report</button><button class="btn btn-primary btn-sm">${icon('plus')} Add user</button>` }) + `
  <div class="grid grid-stats" style="margin-bottom:var(--space-5)">
    ${statCard({ label: 'Students', value: s.students.toLocaleString(), icon: 'graduation', delta: '24 this term', deltaDir: 'up' })}
    ${statCard({ label: 'Teachers', value: String(s.teachers), icon: 'user' })}
    ${statCard({ label: 'Parents', value: s.parents.toLocaleString(), icon: 'users' })}
    ${statCard({ label: 'Classes', value: String(s.classes), icon: 'book' })}
  </div>
  <div class="grid grid-3">
    <div class="card span-2"><div class="card-header"><h3>School performance trend</h3><span class="text-muted" style="font-size:var(--text-sm)">Avg score, 6 months</span></div>
      <div class="card-body">${lineChart(PERFORMANCE_TREND, { labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], color: 'var(--chart-1)' })}</div></div>
    <div class="card"><div class="card-header"><h3>Quick stats</h3></div><div class="card-body col gap-4" style="padding-top:var(--space-4)">
      <div><div class="row spread" style="margin-bottom:6px"><span class="text-muted" style="font-size:var(--text-sm)">Active today</span><strong>${s.activeToday.toLocaleString()}</strong></div>${progress(Math.round(s.activeToday / s.students * 100), 'success')}</div>
      <div><div class="row spread" style="margin-bottom:6px"><span class="text-muted" style="font-size:var(--text-sm)">Fees collected</span><strong>${s.feesCollected}%</strong></div>${progress(s.feesCollected)}</div>
      <div><div class="row spread" style="margin-bottom:6px"><span class="text-muted" style="font-size:var(--text-sm)">Attendance today</span><strong>94%</strong></div>${progress(94, 'success')}</div>
    </div></div>
  </div>`;
}

export function users(m) {
  const roles = ['all', 'student', 'teacher', 'parent', 'admin'];
  m.innerHTML = pageHead({ title: 'Users', subtitle: `${USER_DIRECTORY.length} accounts`,
    actions: `<button class="btn btn-primary btn-sm" data-add>${icon('plus')} Add user</button>` }) + `
  <div class="row spread wrap gap-3" style="margin-bottom:var(--space-4)">
    <div class="tabs">${roles.map((r, i) => `<button class="tab ${i ? '' : 'active'}" data-role="${r}">${r === 'all' ? 'All' : ROLE_LABEL[r] || cap(r)}</button>`).join('')}</div>
    <div class="input-group" style="max-width:260px">${icon('search')}<input class="input" placeholder="Search users…" data-usearch></div>
  </div>
  <div class="card"><div class="table-wrap"><table class="table"><thead><tr><th>Name</th><th>ID</th><th>Role</th><th>Email</th><th>Status</th><th>Joined</th><th></th></tr></thead>
  <tbody id="ubody">${userRows(USER_DIRECTORY)}</tbody></table></div></div>`;

  let role = 'all', q = '';
  const draw = () => { m.querySelector('#ubody').innerHTML = userRows(USER_DIRECTORY.filter((u) => (role === 'all' || u.role === role) && (u.name.toLowerCase().includes(q) || u.email.toLowerCase().includes(q)))); };
  m.querySelectorAll('[data-role]').forEach((t) => t.addEventListener('click', () => { m.querySelectorAll('[data-role]').forEach((x) => x.classList.remove('active')); t.classList.add('active'); role = t.dataset.role; draw(); }));
  m.querySelector('[data-usearch]').addEventListener('input', (e) => { q = e.target.value.toLowerCase(); draw(); });
  m.querySelector('[data-add]').addEventListener('click', openAddUser);
}
function userRows(rows) {
  if (!rows.length) return `<tr><td colspan="7">${emptyState({ icon: 'users', title: 'No users found' })}</td></tr>`;
  return rows.map((u) => `<tr>
    <td><div class="row gap-3">${avatar(u.name.split(' ').map((n) => n[0]).join(''), 'avatar-sm')}<span style="font-weight:600">${esc(u.name)}</span></div></td>
    <td class="mono text-muted">${esc(u.id)}</td><td>${badge(ROLE_LABEL[u.role], roleVariant(u.role))}</td>
    <td class="text-muted">${esc(u.email)}</td>
    <td>${u.status === 'active' ? badge('Active', 'success') : u.status === 'suspended' ? badge('Suspended', 'danger') : badge('Pending', 'warning')}</td>
    <td class="text-muted">${esc(u.joined)}</td>
    <td><button class="btn btn-ghost btn-icon btn-sm">${icon('more')}</button></td></tr>`).join('');
}
function openAddUser() {
  const { close } = modal({
    title: 'Add user',
    body: `<div class="col gap-4">
      <div class="field"><label>Full name</label><input class="input" placeholder="e.g. Jane Doe"></div>
      <div class="field"><label>Email</label><input class="input" type="email" placeholder="name@ngis.edu"></div>
      <div class="field"><label>Role</label><select class="select"><option>Student</option><option>Teacher</option><option>Parent</option><option>Admin</option></select></div>
    </div>`,
    footer: `<button class="btn btn-secondary" data-cancel>Cancel</button><button class="btn btn-primary" data-create>Create user</button>`,
  });
  document.querySelector('[data-cancel]').addEventListener('click', close);
  document.querySelector('[data-create]').addEventListener('click', () => { close(); toast('User created & invite sent', { type: 'success', title: 'New account' }); });
}

export function classesPage(m) {
  m.innerHTML = pageHead({ title: 'Classes & Subjects', actions: `<button class="btn btn-primary btn-sm">${icon('plus')} New class</button>` }) + `
  <div class="grid grid-2" style="margin-bottom:var(--space-5)">
    <div class="card"><div class="card-header"><h3>Classes</h3></div><div class="table-wrap"><table class="table"><thead><tr><th>Class</th><th>Grade</th><th>Homeroom</th><th>Students</th></tr></thead><tbody>
      ${[['10-A', 10, 'Ms. Bello', 28], ['10-B', 10, 'Mr. Adeyemi', 29], ['9-C', 9, 'Mrs. Cole', 31], ['7-A', 7, 'Dr. Okafor', 26]].map(([c, g, h, n]) => `<tr><td style="font-weight:600">${c}</td><td>${g}</td><td class="text-muted">${h}</td><td class="nums">${n}</td></tr>`).join('')}
    </tbody></table></div></div>
    <div class="card"><div class="card-header"><h3>Subjects</h3></div><div class="card-body col gap-2" style="padding-top:var(--space-3)">
      ${SUBJECTS.map((s) => `<div class="list-row"><span style="width:10px;height:10px;border-radius:3px;background:${s.color}"></span><span class="grow" style="font-weight:600">${esc(s.name)}</span>${badge(s.code)}</div>`).join('')}
    </div></div>
  </div>`;
}

export function timetables(m) {
  m.innerHTML = pageHead({ title: 'Timetables', subtitle: 'Manage class schedules' }) +
    `<div class="card">${emptyState({ icon: 'calendar', title: 'Select a class to edit its timetable', text: 'Drag-and-drop period assignment with conflict detection.', action: `<button class="btn btn-primary btn-sm" style="margin-top:8px">Choose class</button>` })}</div>`;
}

export function fees(m) {
  m.innerHTML = pageHead({ title: 'Fees & Payments', subtitle: 'School-wide overview',
    actions: `<button class="btn btn-secondary btn-sm">${icon('download')} Export</button>` }) + `
  <div class="grid grid-4" style="margin-bottom:var(--space-5)">
    ${statCard({ label: 'Billed (term)', value: '$1.42M', icon: 'wallet' })}
    ${statCard({ label: 'Collected', value: '$1.31M', icon: 'checkCircle' })}
    ${statCard({ label: 'Outstanding', value: '$112K', icon: 'clock' })}
    ${statCard({ label: 'Collection rate', value: '92%', icon: 'percent', delta: '3%', deltaDir: 'up' })}
  </div>
  <div class="card"><div class="card-header"><h3>Recent payments</h3></div><div class="table-wrap"><table class="table">
    <thead><tr><th>Student</th><th>Amount</th><th>Method</th><th>Date</th><th>Status</th></tr></thead><tbody>
    ${[['Leo Carter', 3200, 'Bank transfer', 'Jun 18'], ['Mia Carter', 600, 'Card', 'Jun 17'], ['Aisha Rahman', 4800, 'Card', 'Jun 15'], ['Daniel Park', 250, 'Cash', 'Jun 14']].map(([n, a, mth, d]) => `<tr><td style="font-weight:600">${n}</td><td class="nums">$${a.toLocaleString()}</td><td class="text-muted">${mth}</td><td>${d}</td><td>${badge('Recorded', 'success')}</td></tr>`).join('')}
  </tbody></table></div></div>`;
}

export function reports(m) {
  m.innerHTML = pageHead({ title: 'Reports' }) + `
  <div class="grid grid-3">${[['graduation', 'Enrollment report', 'Students by grade & class'], ['check', 'Attendance report', 'Daily & monthly trends'], ['award', 'Academic performance', 'Grades & GPA distribution'], ['wallet', 'Financial summary', 'Fees billed vs collected'], ['users', 'Staff report', 'Teachers & departments'], ['activity', 'Activity log', 'System usage analytics']]
    .map(([ic, t, s]) => `<div class="card card-hover card-pad col gap-2"><div class="state-icon" style="background:var(--accent-soft);color:var(--accent-soft-fg)">${icon(ic)}</div><strong>${t}</strong><span class="text-muted" style="font-size:var(--text-sm)">${s}</span><button class="btn btn-secondary btn-sm" style="margin-top:8px" data-gen>${icon('download')} Generate</button></div>`).join('')}</div>`;
  m.querySelectorAll('[data-gen]').forEach((b) => b.addEventListener('click', () => toast('Report queued for generation', { type: 'success' })));
}

export function announcements(m) {
  m.innerHTML = pageHead({ title: 'Announcements', subtitle: 'School-wide', actions: `<button class="btn btn-primary btn-sm">${icon('plus')} New announcement</button>` }) +
    `<div class="col gap-3">${ANNOUNCEMENTS.map((a) => `<div class="card card-pad"><div class="row spread"><div class="row gap-2">${a.pinned ? icon('pin') : ''}<strong>${esc(a.title)}</strong>${badge(a.category, a.category === 'emergency' ? 'danger' : 'accent')}</div><button class="btn btn-ghost btn-icon btn-sm">${icon('more')}</button></div><p class="text-muted" style="margin-top:var(--space-2);font-size:var(--text-sm)">${esc(a.body)}</p></div>`).join('')}</div>`;
}

export function audit(m) {
  m.innerHTML = pageHead({ title: 'Audit Logs', subtitle: 'Immutable record of sensitive actions' }) + `
  <div class="card"><div class="table-wrap"><table class="table"><thead><tr><th>Time</th><th>Actor</th><th>Action</th><th>Entity</th><th>IP</th><th>Device</th></tr></thead><tbody>
    ${SECURITY_LOG.map((l) => `<tr><td class="mono">${esc(l.when)}</td><td>${esc(l.actor)}</td><td>${badge(l.action, l.action.includes('failed') ? 'danger' : l.action.includes('change') || l.action.includes('edit') ? 'warning' : '')}</td><td class="text-muted">${esc(l.entity)}</td><td class="mono text-muted">${esc(l.ip)}</td><td class="text-muted">${esc(l.device)}</td></tr>`).join('')}
  </tbody></table></div></div>`;
}

function cap(s) { return s[0].toUpperCase() + s.slice(1); }
function roleVariant(r) { return ({ super_admin: 'danger', admin: 'accent', teacher: 'info', student: '', parent: 'warning' })[r] || ''; }
