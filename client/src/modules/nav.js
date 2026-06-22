/* Role-based navigation. Mirrors the RBAC matrix (§10) and per-portal
   feature specs (§12). Each item: { to, label, icon, badge? } */

export const NAV = {
  student: [
    { group: 'Overview', items: [
      { to: '/student', label: 'Dashboard', icon: 'dashboard' },
      { to: '/student/timetable', label: 'Timetable', icon: 'calendar' },
    ]},
    { group: 'Academics', items: [
      { to: '/student/attendance', label: 'Attendance', icon: 'check' },
      { to: '/student/grades', label: 'Grades & Exams', icon: 'award' },
      { to: '/student/assignments', label: 'Assignments', icon: 'clipboard', badge: '3' },
      { to: '/student/documents', label: 'My Documents', icon: 'folder' },
    ]},
    { group: 'School', items: [
      { to: '/student/announcements', label: 'Announcements', icon: 'bell' },
      { to: '/student/calendar', label: 'Calendar', icon: 'calendar' },
      { to: '/student/help', label: 'Help Center', icon: 'help' },
    ]},
  ],
  teacher: [
    { group: 'Overview', items: [
      { to: '/teacher', label: 'Dashboard', icon: 'dashboard' },
      { to: '/teacher/classes', label: 'My Classes', icon: 'users' },
    ]},
    { group: 'Teaching', items: [
      { to: '/teacher/attendance', label: 'Attendance', icon: 'check' },
      { to: '/teacher/grades', label: 'Grades', icon: 'award' },
      { to: '/teacher/assignments', label: 'Assignments', icon: 'clipboard', badge: '7' },
      { to: '/teacher/documents', label: 'Documents', icon: 'folder' },
    ]},
    { group: 'Insights', items: [
      { to: '/teacher/analytics', label: 'Analytics', icon: 'chart' },
      { to: '/teacher/announcements', label: 'Announcements', icon: 'bell' },
    ]},
  ],
  parent: [
    { group: 'Overview', items: [
      { to: '/parent', label: 'Dashboard', icon: 'dashboard' },
      { to: '/parent/children', label: 'My Children', icon: 'users' },
    ]},
    { group: 'Academics', items: [
      { to: '/parent/attendance', label: 'Attendance', icon: 'check' },
      { to: '/parent/grades', label: 'Grades & Exams', icon: 'award' },
      { to: '/parent/assignments', label: 'Assignments', icon: 'clipboard' },
      { to: '/parent/fees', label: 'Fees & Payments', icon: 'wallet', badge: '$' },
    ]},
    { group: 'School', items: [
      { to: '/parent/messages', label: 'Messages', icon: 'message', badge: '2' },
      { to: '/parent/announcements', label: 'Announcements', icon: 'bell' },
      { to: '/parent/calendar', label: 'Calendar', icon: 'calendar' },
    ]},
  ],
  admin: [
    { group: 'Overview', items: [
      { to: '/admin', label: 'Dashboard', icon: 'dashboard' },
    ]},
    { group: 'Management', items: [
      { to: '/admin/users', label: 'Users', icon: 'users' },
      { to: '/admin/classes', label: 'Classes & Subjects', icon: 'book' },
      { to: '/admin/timetables', label: 'Timetables', icon: 'calendar' },
      { to: '/admin/fees', label: 'Fees & Payments', icon: 'wallet' },
    ]},
    { group: 'Records', items: [
      { to: '/admin/reports', label: 'Reports', icon: 'chart' },
      { to: '/admin/announcements', label: 'Announcements', icon: 'bell' },
      { to: '/admin/audit', label: 'Audit Logs', icon: 'list' },
    ]},
  ],
  super_admin: [
    { group: 'Overview', items: [
      { to: '/superadmin', label: 'Dashboard', icon: 'dashboard' },
    ]},
    { group: 'Administration', items: [
      { to: '/superadmin/users', label: 'Users & Admins', icon: 'users' },
      { to: '/superadmin/branding', label: 'School Branding', icon: 'building' },
    ]},
    { group: 'Infrastructure', items: [
      { to: '/superadmin/health', label: 'System Health', icon: 'activity' },
      { to: '/superadmin/backups', label: 'Backups', icon: 'database' },
      { to: '/superadmin/security', label: 'Security Logs', icon: 'shield' },
      { to: '/superadmin/maintenance', label: 'Maintenance', icon: 'settings' },
    ]},
  ],
};

export const HOME = {
  super_admin: '/superadmin', admin: '/admin', teacher: '/teacher', student: '/student', parent: '/parent',
};
