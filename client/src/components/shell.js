/* App shell — sidebar (role nav) + topbar + content slot. Renders once per
   role; content is swapped on navigation. Handles collapse, mobile drawer,
   theme toggle, search, notifications, and user menu. */
import { icon } from '../modules/icons.js';
import { NAV } from '../modules/nav.js';
import { ROLE_LABEL, SCHOOL, NOTIFICATIONS } from '../data/mock.js';
import { ui, setSidebarCollapsed } from '../modules/store.js';
import { toggleTheme, getTheme } from '../modules/theme.js';
import { logout } from '../modules/auth.js';
import { navigate, currentPath } from '../modules/router.js';
import { esc, avatar } from './ui.js';

export function renderShell(user) {
  const groups = NAV[user.role] || [];
  const collapsed = ui.get('sidebarCollapsed');
  const unread = NOTIFICATIONS.filter((n) => !n.read).length;

  const navHtml = groups.map((g) => `
    <div class="nav-group-label">${esc(g.group)}</div>
    ${g.items.map((it) => `
      <a class="nav-item" data-nav href="#${it.to}" title="${esc(it.label)}">
        ${icon(it.icon)}<span class="label">${esc(it.label)}</span>
        ${it.badge ? `<span class="badge badge-accent nav-badge">${esc(it.badge)}</span>` : ''}
      </a>`).join('')}
  `).join('');

  document.getElementById('app').innerHTML = `
    <div class="app-shell ${collapsed ? 'collapsed' : ''}" id="shell">
      <div class="scrim" data-scrim></div>
      <aside class="sidebar" aria-label="Primary navigation">
        <div class="sidebar-brand">
          <div class="brand-mark">N</div>
          <div class="col" style="line-height:1.2">
            <span class="brand-name">${esc(SCHOOL.short)}</span>
            <span class="brand-sub">School OS</span>
          </div>
        </div>
        <nav class="sidebar-nav">${navHtml}</nav>
        <div class="sidebar-foot">
          <div class="user-chip" data-usermenu>
            ${avatar(user.initials)}
            <div class="meta grow">
              <div class="name">${esc(user.name)}</div>
              <div class="role">${esc(ROLE_LABEL[user.role])}</div>
            </div>
            ${icon('chevronDown', 'icon chev')}
          </div>
        </div>
      </aside>

      <div class="main">
        <header class="topbar">
          <button class="icon-btn" data-collapse aria-label="Toggle sidebar">${icon('menu')}</button>
          <div class="input-group search">
            ${icon('search')}
            <input class="input" type="search" placeholder="Search students, classes, pages…  ( / )" aria-label="Search" data-search>
          </div>
          <div class="topbar-spacer"></div>
          <button class="icon-btn" data-theme aria-label="Toggle theme">${icon(getTheme() === 'dark' ? 'sun' : 'moon')}</button>
          <button class="icon-btn" data-notif aria-label="Notifications">${icon('bell')}${unread ? '<span class="ind"></span>' : ''}</button>
          <button class="icon-btn" data-help aria-label="Help">${icon('help')}</button>
        </header>

        <main class="content" id="view" tabindex="-1"></main>
      </div>
    </div>`;

  wireShell(user);
  return document.getElementById('view');
}

function wireShell(user) {
  const shell = document.getElementById('shell');

  shell.querySelector('[data-collapse]').addEventListener('click', () => {
    if (window.innerWidth <= 768) { shell.classList.toggle('mobile-open'); return; }
    setSidebarCollapsed(!ui.get('sidebarCollapsed'));
    shell.classList.toggle('collapsed', ui.get('sidebarCollapsed'));
  });

  shell.querySelector('[data-scrim]').addEventListener('click', () => shell.classList.remove('mobile-open'));

  shell.querySelector('[data-theme]').addEventListener('click', (e) => {
    const t = toggleTheme();
    e.currentTarget.innerHTML = icon(t === 'dark' ? 'sun' : 'moon');
  });

  shell.querySelectorAll('[data-nav]').forEach((a) => {
    a.addEventListener('click', () => { if (window.innerWidth <= 768) shell.classList.remove('mobile-open'); });
  });

  shell.querySelector('[data-notif]').addEventListener('click', (e) => openNotif(e.currentTarget));
  shell.querySelector('[data-usermenu]').addEventListener('click', (e) => openUserMenu(e.currentTarget, user));
  shell.querySelector('[data-help]').addEventListener('click', () => navigate(`/${user.role === 'super_admin' ? 'superadmin' : user.role}`));

  const search = shell.querySelector('[data-search]');
  document.addEventListener('keydown', (e) => {
    if (e.key === '/' && document.activeElement !== search && !/input|textarea/i.test(document.activeElement.tagName)) {
      e.preventDefault(); search.focus();
    }
  });

  setActiveNav();
}

export function setActiveNav() {
  const path = currentPath();
  document.querySelectorAll('[data-nav]').forEach((a) => {
    const to = a.getAttribute('href').replace('#', '');
    a.classList.toggle('active', to === path);
  });
}

function popover(anchor, html) {
  document.querySelectorAll('.menu[data-pop]').forEach((m) => m.remove());
  const menu = document.createElement('div');
  menu.className = 'menu'; menu.setAttribute('data-pop', '');
  menu.innerHTML = html;
  document.body.appendChild(menu);
  const r = anchor.getBoundingClientRect();
  menu.style.top = `${r.bottom + 8}px`;
  menu.style.right = `${window.innerWidth - r.right}px`;
  const close = (e) => { if (!menu.contains(e.target) && e.target !== anchor) { menu.remove(); document.removeEventListener('click', close); } };
  setTimeout(() => document.addEventListener('click', close), 0);
  return menu;
}

function openNotif(anchor) {
  const items = NOTIFICATIONS.map((n) => `
    <button class="menu-item" style="align-items:flex-start">
      <span style="margin-top:2px;color:${n.read ? 'var(--text-muted)' : 'var(--accent)'}">${icon(n.icon)}</span>
      <span class="col" style="gap:2px"><span style="font-size:var(--text-sm);${n.read ? '' : 'font-weight:600'}">${esc(n.text)}</span>
      <span style="font-size:var(--text-xs);color:var(--text-muted)">${esc(n.time)}</span></span>
    </button>`).join('');
  popover(anchor, `<div style="padding:4px 8px 8px;font-weight:600;font-size:var(--text-sm)">Notifications</div>${items}
    <div class="menu-divider"></div><button class="menu-item" style="justify-content:center;color:var(--accent)">Mark all as read</button>`);
}

function openUserMenu(anchor, user) {
  popover(anchor, `
    <div style="padding:8px 10px"><div style="font-weight:600">${esc(user.name)}</div>
    <div style="font-size:var(--text-xs);color:var(--text-muted)">${esc(user.email)}</div></div>
    <div class="menu-divider"></div>
    <button class="menu-item">${icon('user')} Profile</button>
    <button class="menu-item">${icon('settings')} Settings</button>
    <div class="menu-divider"></div>
    <button class="menu-item danger" data-logout>${icon('logout')} Sign out</button>`)
    .querySelector('[data-logout]').addEventListener('click', () => { logout(); location.hash = '/login'; location.reload(); });
}
