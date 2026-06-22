/* Super Admin panel (§12.5) — everything Admin can do, plus infrastructure.
   Super Admin account is permanent (§10): cannot be deleted/suspended. */
import { icon } from '../../modules/icons.js';
import { SYSTEM_HEALTH, BACKUPS, SECURITY_LOG, ADMIN_STATS, USER_DIRECTORY, ROLE_LABEL } from '../../data/mock.js';
import { esc, pageHead, statCard, badge, avatar, toast, progress } from '../../components/ui.js';

export function dashboard(m) {
  m.innerHTML = pageHead({ title: 'Super Admin', subtitle: 'System owner · full infrastructure control',
    actions: `<button class="btn btn-secondary btn-sm">${icon('refresh')} Run health check</button>` }) + `
  <div class="grid grid-stats" style="margin-bottom:var(--space-5)">
    ${statCard({ label: 'System uptime', value: '99.97%', icon: 'activity', delta: '30d', deltaDir: 'up' })}
    ${statCard({ label: 'API p95', value: '182ms', icon: 'zap' })}
    ${statCard({ label: 'Storage used', value: '128 GB', icon: 'database' })}
    ${statCard({ label: 'Active sessions', value: String(ADMIN_STATS.activeToday), icon: 'users' })}
  </div>
  <div class="grid grid-2">
    <div class="card"><div class="card-header"><h3>Service health</h3></div><div class="card-body col gap-3" style="padding-top:var(--space-3)">
      ${SYSTEM_HEALTH.map((s) => `<div class="list-row"><div class="state-icon" style="width:38px;height:38px;background:var(--${s.level}-soft);color:var(--${s.level}-fg)">${icon(s.icon)}</div>
        <div class="grow"><div style="font-weight:600">${esc(s.name)}</div><div class="text-muted" style="font-size:var(--text-sm)">${esc(s.metric)}</div></div>
        ${badge(cap(s.status), s.level)}</div>`).join('')}
    </div></div>
    <div class="card"><div class="card-header"><h3>Recent security events</h3><button class="btn btn-ghost btn-sm">View all</button></div><div class="card-body col gap-3" style="padding-top:var(--space-3)">
      ${SECURITY_LOG.slice(0, 4).map((l) => `<div class="list-row"><div class="state-icon" style="width:34px;height:34px;background:var(--bg-sunken)">${icon(l.action.includes('failed') ? 'alert' : 'shield')}</div>
        <div class="grow"><div style="font-weight:600;font-size:var(--text-sm)">${esc(l.action)}</div><div class="text-muted" style="font-size:var(--text-xs)">${esc(l.actor)} · ${esc(l.ip)}</div></div>
        <span class="text-muted mono" style="font-size:var(--text-xs)">${esc(l.when)}</span></div>`).join('')}
    </div></div>
  </div>`;
}

export function users(m) {
  m.innerHTML = pageHead({ title: 'Users & Admins', subtitle: 'Manage all accounts including administrators' }) + `
  <div class="card" style="margin-bottom:var(--space-5)"><div class="card-body row gap-3" style="background:var(--accent-soft)">
    ${icon('shield')}<div><strong>Super Admin is permanent</strong><div class="text-muted" style="font-size:var(--text-sm)">This account cannot be deleted, suspended, or downgraded — enforced at DB, service & UI layers.</div></div></div></div>
  <div class="card"><div class="table-wrap"><table class="table"><thead><tr><th>Name</th><th>Role</th><th>Email</th><th>Status</th><th></th></tr></thead><tbody>
    <tr><td><div class="row gap-3">${avatar('SO', 'avatar-sm')}<span style="font-weight:600">Sarah Okonkwo</span></div></td><td>${badge('Super Admin', 'danger')}</td><td class="text-muted">superadmin@ngis.edu</td><td>${badge('Active', 'success')}</td><td><span data-tip="Protected account" class="text-muted">${icon('lock')}</span></td></tr>
    ${USER_DIRECTORY.filter((u) => u.role === 'admin' || u.role === 'teacher').map((u) => `<tr><td><div class="row gap-3">${avatar(u.name.split(' ').map((n) => n[0]).join(''), 'avatar-sm')}<span style="font-weight:600">${esc(u.name)}</span></div></td><td>${badge(ROLE_LABEL[u.role], u.role === 'admin' ? 'accent' : 'info')}</td><td class="text-muted">${esc(u.email)}</td><td>${badge('Active', 'success')}</td><td><button class="btn btn-ghost btn-icon btn-sm">${icon('more')}</button></td></tr>`).join('')}
  </tbody></table></div></div>`;
}

export function health(m) {
  m.innerHTML = pageHead({ title: 'System Health', subtitle: 'Infrastructure monitoring',
    actions: `<button class="btn btn-secondary btn-sm">${icon('refresh')} Refresh</button>` }) + `
  <div class="grid grid-2" style="margin-bottom:var(--space-5)">
    ${SYSTEM_HEALTH.map((s) => `<div class="card card-pad"><div class="row spread">
      <div class="row gap-3"><div class="state-icon" style="background:var(--${s.level}-soft);color:var(--${s.level}-fg)">${icon(s.icon)}</div>
      <div><strong>${esc(s.name)}</strong><div class="text-muted" style="font-size:var(--text-sm)">${esc(s.metric)}</div></div></div>${badge(cap(s.status), s.level)}</div></div>`).join('')}
  </div>
  <div class="grid grid-3">
    <div class="card card-pad"><div class="row spread" style="margin-bottom:8px"><span class="text-muted" style="font-size:var(--text-sm)">CPU</span><strong>34%</strong></div>${progress(34, 'success')}</div>
    <div class="card card-pad"><div class="row spread" style="margin-bottom:8px"><span class="text-muted" style="font-size:var(--text-sm)">Memory</span><strong>61%</strong></div>${progress(61)}</div>
    <div class="card card-pad"><div class="row spread" style="margin-bottom:8px"><span class="text-muted" style="font-size:var(--text-sm)">DB connections</span><strong>78%</strong></div>${progress(78, 'warning')}</div>
  </div>`;
}

export function backups(m) {
  m.innerHTML = pageHead({ title: 'Backups', subtitle: 'RPO ≤ 24h · daily automatic backups',
    actions: `<button class="btn btn-primary btn-sm" data-bk>${icon('database')} Run backup now</button>` }) + `
  <div class="grid grid-3" style="margin-bottom:var(--space-5)">
    ${statCard({ label: 'Last backup', value: '02:00', icon: 'clock', delta: 'Success', deltaDir: 'up' })}
    ${statCard({ label: 'Total size', value: '4.2 GB', icon: 'database' })}
    ${statCard({ label: 'Retention', value: '30 days', icon: 'shield' })}
  </div>
  <div class="card"><div class="card-header"><h3>Backup history</h3></div><div class="table-wrap"><table class="table">
    <thead><tr><th>Type</th><th>Size</th><th>Location</th><th>Timestamp</th><th>Status</th><th></th></tr></thead><tbody>
    ${BACKUPS.map((b) => `<tr><td style="font-weight:600">${esc(b.type)}</td><td class="nums">${esc(b.size)}</td><td class="text-muted">${esc(b.location)}</td><td class="mono">${esc(b.when)}</td>
      <td>${b.status === 'success' ? badge('Success', 'success') : badge('Failed', 'danger')}</td>
      <td>${b.status === 'success' ? `<button class="btn btn-ghost btn-sm" data-restore>${icon('refresh')} Restore</button>` : `<button class="btn btn-ghost btn-sm">${icon('refresh')} Retry</button>`}</td></tr>`).join('')}
  </tbody></table></div></div>`;
  m.querySelector('[data-bk]').addEventListener('click', () => toast('Backup started — you’ll be notified on completion', { type: 'success' }));
  m.querySelectorAll('[data-restore]').forEach((b) => b.addEventListener('click', () => toast('Restore requires confirmation & runbook approval', { type: 'warning', title: 'Restore' })));
}

export function security(m) {
  m.innerHTML = pageHead({ title: 'Security Logs', subtitle: 'Device & session activity' }) + `
  <div class="card"><div class="table-wrap"><table class="table"><thead><tr><th>Time</th><th>Actor</th><th>Action</th><th>Detail</th><th>IP</th><th>Device</th></tr></thead><tbody>
    ${SECURITY_LOG.map((l) => `<tr><td class="mono">${esc(l.when)}</td><td>${esc(l.actor)}</td>
      <td>${badge(l.action, l.action.includes('failed') ? 'danger' : l.action.includes('change') || l.action.includes('edit') ? 'warning' : 'success')}</td>
      <td class="text-muted">${esc(l.entity)}</td><td class="mono text-muted">${esc(l.ip)}</td><td class="text-muted">${esc(l.device)}</td></tr>`).join('')}
  </tbody></table></div></div>`;
}

export function maintenance(m) {
  m.innerHTML = pageHead({ title: 'Maintenance', subtitle: 'System configuration & maintenance mode' }) + `
  <div class="grid grid-2">
    <div class="card card-pad"><div class="row spread"><div><strong>Maintenance mode</strong><div class="text-muted" style="font-size:var(--text-sm)">Show a maintenance page to all non-admin users.</div></div>
      <label class="checkbox"><input type="checkbox" data-maint></label></div></div>
    <div class="card card-pad"><div class="row spread"><div><strong>New registrations</strong><div class="text-muted" style="font-size:var(--text-sm)">Allow new parent/student sign-ups.</div></div>
      <label class="checkbox"><input type="checkbox" checked></label></div></div>
    <div class="card card-pad"><div><strong>Cloudflare WAF</strong><div class="text-muted" style="font-size:var(--text-sm);margin-bottom:var(--space-3)">Edge protection & rate limiting.</div>${badge('Active · 2 rules flagged', 'warning')}</div></div>
    <div class="card card-pad"><div><strong>API rate limits</strong><div class="text-muted" style="font-size:var(--text-sm);margin-bottom:var(--space-3)">Per-IP & per-user throttling.</div>${badge('100 req/min · auth 5/min', 'success')}</div></div>
  </div>`;
  m.querySelector('[data-maint]').addEventListener('change', (e) => toast(e.target.checked ? 'Maintenance mode ENABLED' : 'Maintenance mode disabled', { type: e.target.checked ? 'warning' : 'success' }));
}

export function branding(m) {
  m.innerHTML = pageHead({ title: 'School Branding', subtitle: 'Logo, colors & identity' }) + `
  <div class="grid grid-2"><div class="card card-pad col gap-4">
    <strong>Identity</strong>
    <div class="field"><label>School name</label><input class="input" value="Northgate International School"></div>
    <div class="field"><label>Short code</label><input class="input" value="NGIS"></div>
    <button class="btn btn-primary btn-sm" style="align-self:flex-start" data-save>${icon('check')} Save changes</button>
  </div>
  <div class="card card-pad col gap-4"><strong>Accent color</strong>
    <div class="row gap-2">${['#2563EB', '#16A34A', '#7C3AED', '#DC2626', '#0EA5E9'].map((c, i) => `<button class="att-pill ${i === 0 ? 'on' : ''}" style="background:${c};border-color:${c};width:40px;height:40px"></button>`).join('')}</div>
    <div class="text-muted" style="font-size:var(--text-sm)">Changes apply across all portals after save.</div>
  </div></div>`;
  m.querySelector('[data-save]').addEventListener('click', () => toast('Branding updated', { type: 'success' }));
}

function cap(s) { return s[0].toUpperCase() + s.slice(1); }
