/* App bootstrap — registers routes, guards auth, renders shell + pages. */
import { initTheme } from './modules/theme.js';
import { route, getHandler, setOnNavigate, startRouter, currentPath } from './modules/router.js';
import { getSession } from './modules/auth.js';
import { HOME } from './modules/nav.js';
import { renderShell, setActiveNav } from './components/shell.js';
import { renderLogin } from './pages/login.js';

import * as student from './pages/student/index.js';
import * as teacher from './pages/teacher/index.js';
import * as parent from './pages/parent/index.js';
import * as admin from './pages/admin/index.js';
import * as superadmin from './pages/superadmin/index.js';

initTheme();

/* ---- Route table: path -> { role, render } ---- */
const PAGES = {
  // Student
  '/student':              { role: 'student', render: student.dashboard },
  '/student/timetable':    { role: 'student', render: student.timetable },
  '/student/attendance':   { role: 'student', render: student.attendance },
  '/student/grades':       { role: 'student', render: student.grades },
  '/student/assignments':  { role: 'student', render: student.assignments },
  '/student/documents':    { role: 'student', render: student.documents },
  '/student/announcements':{ role: 'student', render: student.announcements },
  '/student/calendar':     { role: 'student', render: student.calendar },
  '/student/help':         { role: 'student', render: student.help },
  // Teacher
  '/teacher':              { role: 'teacher', render: teacher.dashboard },
  '/teacher/classes':      { role: 'teacher', render: teacher.classes },
  '/teacher/attendance':   { role: 'teacher', render: teacher.attendance },
  '/teacher/grades':       { role: 'teacher', render: teacher.grades },
  '/teacher/assignments':  { role: 'teacher', render: teacher.assignmentsPage },
  '/teacher/documents':    { role: 'teacher', render: teacher.documents },
  '/teacher/analytics':    { role: 'teacher', render: teacher.analytics },
  '/teacher/announcements':{ role: 'teacher', render: teacher.announcements },
  // Parent
  '/parent':               { role: 'parent', render: parent.dashboard },
  '/parent/children':      { role: 'parent', render: parent.children },
  '/parent/attendance':    { role: 'parent', render: parent.attendance },
  '/parent/grades':        { role: 'parent', render: parent.grades },
  '/parent/assignments':   { role: 'parent', render: parent.assignmentsPage },
  '/parent/fees':          { role: 'parent', render: parent.fees },
  '/parent/messages':      { role: 'parent', render: parent.messages },
  '/parent/announcements': { role: 'parent', render: parent.announcements },
  '/parent/calendar':      { role: 'parent', render: parent.calendar },
  // Admin
  '/admin':                { role: 'admin', render: admin.dashboard },
  '/admin/users':          { role: 'admin', render: admin.users },
  '/admin/classes':        { role: 'admin', render: admin.classesPage },
  '/admin/timetables':     { role: 'admin', render: admin.timetables },
  '/admin/fees':           { role: 'admin', render: admin.fees },
  '/admin/reports':        { role: 'admin', render: admin.reports },
  '/admin/announcements':  { role: 'admin', render: admin.announcements },
  '/admin/audit':          { role: 'admin', render: admin.audit },
  // Super Admin
  '/superadmin':             { role: 'super_admin', render: superadmin.dashboard },
  '/superadmin/users':       { role: 'super_admin', render: superadmin.users },
  '/superadmin/health':      { role: 'super_admin', render: superadmin.health },
  '/superadmin/backups':     { role: 'super_admin', render: superadmin.backups },
  '/superadmin/security':    { role: 'super_admin', render: superadmin.security },
  '/superadmin/maintenance': { role: 'super_admin', render: superadmin.maintenance },
  '/superadmin/branding':    { role: 'super_admin', render: superadmin.branding },
};

route('/login', () => {});
Object.keys(PAGES).forEach((p) => route(p, () => {}));

let currentRole = null; // shell is re-rendered only when role changes

setOnNavigate((path) => {
  const session = getSession();

  // Auth guard
  if (path === '/login') {
    if (session) { location.hash = HOME[session.user.role]; return; }
    currentRole = null;
    renderLogin(document.getElementById('app'));
    return;
  }
  if (!session) { location.hash = '/login'; return; }

  const page = PAGES[path];
  // Unknown route or role landing → send home
  if (!page) { location.hash = HOME[session.user.role]; return; }
  // RBAC: a user can only enter their own portal (§10)
  if (page.role !== session.user.role) { location.hash = HOME[session.user.role]; return; }

  // (Re)build shell if role changed; otherwise just swap content
  if (currentRole !== session.user.role || !document.getElementById('view')) {
    currentRole = session.user.role;
    const view = renderShell(session.user);
    page.render(view);
  } else {
    const view = document.getElementById('view');
    view.innerHTML = '';
    page.render(view);
    setActiveNav();
    view.focus();
  }
});

// Default route
if (!location.hash) location.hash = getSession() ? HOME[getSession().user.role] : '/login';

startRouter();
