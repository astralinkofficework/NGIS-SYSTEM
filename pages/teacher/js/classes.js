/* ══════════════════════════════════════
   CLASSES — Data + DOM Rendering (Teacher Portal)
   ══════════════════════════════════════ */

const classes = [
  { icon: 'calculate', name: 'Calculus',                 cohort: 'Grade 11-A · 32 Students', room: 'Room 302', pct: 78, color: '#13829b', bg: '#e0f2fe' },
  { icon: 'analytics', name: 'Statistics & Probability', cohort: 'Grade 10-C · 28 Students', room: 'Room 305', pct: 85, color: '#059669', bg: '#f0fdf4' },
  { icon: 'functions', name: 'Pure Mathematics',         cohort: 'Grade 12-B · 24 Students', room: 'Room 304', pct: 65, color: '#2563eb', bg: '#eff6ff' },
  { icon: 'square_foot', name: 'Advanced Geometry',      cohort: 'Grade 10-A · 30 Students', room: 'Room 301', pct: 92, color: '#7c3aed', bg: '#faf5ff' },
  { icon: 'architecture', name: 'Applied Mathematics',   cohort: 'Grade 11-B · 26 Students', room: 'Room 303', pct: 74, color: '#ea580c', bg: '#fff7ed' },
  { icon: 'emoji_events', name: 'Math Olympiad Prep',    cohort: 'Extracurricular · 16 Students', room: 'Hall A', pct: 95, color: '#db2777', bg: '#fdf2f8' },
];

(function renderClasses() {
  const container = document.getElementById('subjGrid');
  if (!container) return;

  container.innerHTML = classes.map(c => `
    <div class="subj-item" onclick="window.location.href='teacher-classes.html'" style="cursor:pointer" title="Manage ${c.name}">
      <div class="subj-ico" style="background:${c.bg}">
        <span class="mi" style="color:${c.color}">${c.icon}</span>
      </div>
      <div class="subj-body">
        <div class="subj-name">${c.name}</div>
        <div class="subj-teacher">${c.cohort} · ${c.room}</div>
        <div class="subj-bar-row">
          <div class="subj-bar">
            <div class="subj-fill" data-w="${c.pct}" style="background:${c.color}; width:0%"></div>
          </div>
          <span class="subj-pct">${c.pct}%</span>
        </div>
      </div>
    </div>
  `).join('');

  /* Animate progress bars after paint */
  setTimeout(() => {
    document.querySelectorAll('.subj-fill').forEach(el => {
      el.style.width = el.dataset.w + '%';
    });
  }, 200);
})();

