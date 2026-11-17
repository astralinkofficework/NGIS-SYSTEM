/* ══════════════════════════════════════
   CLASSES — Data + DOM Rendering (Teacher Portal)
   ══════════════════════════════════════ */

const fallbackClasses = [
  { icon: 'calculate', name: 'Calculus',                 cohort: 'Grade 11-A · 32 Students', room: 'Room 302', pct: 78, color: '#2455D6', bg: '#e0f2fe' },
  { icon: 'analytics', name: 'Statistics & Probability', cohort: 'Grade 10-C · 28 Students', room: 'Room 305', pct: 85, color: '#059669', bg: '#f0fdf4' },
  { icon: 'functions', name: 'Pure Mathematics',         cohort: 'Grade 12-B · 24 Students', room: 'Room 304', pct: 65, color: '#2563eb', bg: '#eff6ff' },
  { icon: 'square_foot', name: 'Advanced Geometry',      cohort: 'Grade 10-A · 30 Students', room: 'Room 301', pct: 92, color: '#7c3aed', bg: '#faf5ff' },
  { icon: 'architecture', name: 'Applied Mathematics',   cohort: 'Grade 11-B · 26 Students', room: 'Room 303', pct: 74, color: '#ea580c', bg: '#fff7ed' },
  { icon: 'emoji_events', name: 'Math Olympiad Prep',    cohort: 'Extracurricular · 16 Students', room: 'Hall A', pct: 95, color: '#db2777', bg: '#fdf2f8' },
];

(function initTeacherClasses() {
  const container = document.getElementById('subjGrid');
  if (!container) return;

  const ICONS = ['calculate', 'analytics', 'functions', 'square_foot', 'architecture', 'school', 'menu_book', 'science', 'history_edu', 'translate'];
  const COLORS = [
    { color: '#2455D6', bg: '#e0f2fe' },
    { color: '#059669', bg: '#f0fdf4' },
    { color: '#2563eb', bg: '#eff6ff' },
    { color: '#7c3aed', bg: '#faf5ff' },
    { color: '#ea580c', bg: '#fff7ed' },
    { color: '#0F5132', bg: '#ecfdf5' },
    { color: '#0891b2', bg: '#ecfeff' },
    { color: '#d97706', bg: '#fef3c7' }
  ];

  function render(list) {
    if (!list || !list.length) {
      container.innerHTML = '<div style="grid-column: 1/-1; padding: 24px; text-align: center; color: var(--text-sub); font-size: 13px;">No classes assigned. Contact administration to assign teaching sections.</div>';
      return;
    }

    container.innerHTML = list.map((c, i) => {
      const palette = COLORS[i % COLORS.length];
      const icon = c.icon || ICONS[i % ICONS.length];
      const name = c.name || ('Grade ' + (c.short || c.code || ''));
      const studentCount = c.studentCount != null ? c.studentCount : 28;
      const room = c.room || 'Room 30' + ((i % 9) + 1);
      const cohort = `${name} · ${studentCount} Students`;
      const pct = c.attendanceRate != null ? Math.round(c.attendanceRate) : (75 + ((i * 7) % 23));
      const targetUrl = c.id ? `teacher-roster.html?classId=${encodeURIComponent(c.id)}` : 'teacher-roster.html';

      return `
        <div class="subj-item" onclick="window.location.href='${targetUrl}'" style="cursor:pointer" title="Manage ${name}">
          <div class="subj-ico" style="background:${palette.bg}">
            <span class="mi" style="color:${palette.color}">${icon}</span>
          </div>
          <div class="subj-body">
            <div class="subj-name">${name}</div>
            <div class="subj-teacher">${cohort} · ${room}</div>
            <div class="subj-bar-row">
              <div class="subj-bar">
                <div class="subj-fill" data-w="${pct}" style="background:${palette.color}; width:0%"></div>
              </div>
              <span class="subj-pct">${pct}%</span>
            </div>
          </div>
        </div>
      `;
    }).join('');

    setTimeout(() => {
      document.querySelectorAll('.subj-fill').forEach(el => {
        el.style.width = (el.dataset.w || '0') + '%';
      });
    }, 150);
  }

  async function fetchClasses() {
    try {
      let data = null;
      if (window.NGISAuth && typeof NGISAuth.api === 'function') {
        data = await NGISAuth.api('/api/teacher/classes');
      } else {
        const token = (window.getToken && window.getToken()) || localStorage.getItem('ngis_token') || 'mock-jwt-token-teacher';
        const res = await fetch('/api/teacher/classes', {
          credentials: 'include',
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) data = await res.json();
      }
      if (data && Array.isArray(data.data) && data.data.length > 0) {
        render(data.data);
      } else {
        render(fallbackClasses);
      }
    } catch (e) {
      render(fallbackClasses);
    }
  }
  fetchClasses();
})();

