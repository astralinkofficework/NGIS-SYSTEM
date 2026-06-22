/* Login — split layout. Demo-account chips let you enter any role's portal
   (front-end only; the real flow uses §8 JWT + refresh). */
import { icon } from '../modules/icons.js';
import { USERS, SCHOOL, ROLE_LABEL } from '../data/mock.js';
import { login } from '../modules/auth.js';
import { HOME } from '../modules/nav.js';
import { navigate } from '../modules/router.js';
import { esc, toast } from '../components/ui.js';

export function renderLogin(mount) {
  const points = [
    'One platform for five roles',
    'Secure by default · RBAC on every action',
    'Calm, fast, fully responsive',
  ];
  mount.innerHTML = `
  <div class="auth-wrap">
    <div class="auth-aside">
      <div class="auth-brand">
        <div class="brand-mark" style="width:40px;height:40px;font-size:18px">N</div>
        <div class="col"><strong style="font-size:var(--text-md)">${esc(SCHOOL.short)}</strong>
        <span style="font-size:var(--text-xs);opacity:.8">School Operating System</span></div>
      </div>
      <div class="col gap-4">
        <h1>The calm way to run a school.</h1>
        <p>Enrollment, attendance, grades, fees and communication — unified for ${esc(SCHOOL.name)}.</p>
        <div class="auth-points">
          ${points.map((p) => `<div class="auth-point">${icon('checkCircle')}<span>${esc(p)}</span></div>`).join('')}
        </div>
      </div>
      <div style="font-size:var(--text-xs);opacity:.7;position:relative;z-index:1">${esc(SCHOOL.year)} · ${esc(SCHOOL.term)}</div>
    </div>

    <div class="auth-main">
      <div class="auth-card col gap-5">
        <div class="col gap-1">
          <h2>Sign in</h2>
          <p class="text-muted">Welcome back. Enter your credentials to continue.</p>
        </div>
        <form class="col gap-4" id="login-form">
          <div class="field">
            <label for="email">Email</label>
            <div class="input-group">${icon('mail')}<input class="input" id="email" type="email" value="student@ngis.edu" autocomplete="username"></div>
          </div>
          <div class="field">
            <label for="pwd">Password</label>
            <div class="input-group">${icon('lock')}<input class="input" id="pwd" type="password" value="demo-password" autocomplete="current-password"></div>
          </div>
          <div class="row spread">
            <label class="checkbox"><input type="checkbox" checked> Remember me</label>
            <a href="#" style="font-size:var(--text-sm)">Forgot password?</a>
          </div>
          <button class="btn btn-primary btn-lg btn-block" type="submit">Sign in${icon('arrowRight')}</button>
        </form>

        <div class="row gap-3" style="color:var(--text-muted);font-size:var(--text-xs)">
          <div class="grow" style="height:1px;background:var(--border)"></div>OR CONTINUE AS DEMO<div class="grow" style="height:1px;background:var(--border)"></div>
        </div>
        <div class="demo-accounts">
          ${Object.entries(USERS).map(([key, u]) => `
            <button class="demo-chip" data-role="${u.role}">
              <span class="avatar avatar-sm">${esc(u.initials)}</span>
              <span class="col" style="gap:0"><strong style="font-size:var(--text-sm)">${esc(ROLE_LABEL[u.role])}</strong>
              <span style="font-size:11px;color:var(--text-muted)">${esc(u.email)}</span></span>
            </button>`).join('')}
        </div>
      </div>
    </div>
  </div>`;

  const go = (roleKey) => {
    const session = login(roleKey);
    toast(`Signed in as ${session.user.name}`, { type: 'success', title: ROLE_LABEL[session.user.role] });
    navigate(HOME[session.user.role]);
  };

  mount.querySelector('#login-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const email = mount.querySelector('#email').value;
    const entry = Object.entries(USERS).find(([, u]) => u.email === email);
    go(entry ? entry[0] : 'student');
  });
  mount.querySelectorAll('.demo-chip').forEach((c) => c.addEventListener('click', () => {
    const roleKey = Object.keys(USERS).find((k) => USERS[k].role === c.dataset.role);
    go(roleKey);
  }));
}
