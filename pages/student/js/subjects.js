/* ══════════════════════════════════════
   SUBJECTS — Data + DOM Rendering
   ══════════════════════════════════════ */

const subjects = [
  { icon: 'calculate', name: 'Mathematics',          teacher: 'Mr. John Smith',    pct: 88, color: '#2563eb', bg: '#eff6ff' },
  { icon: 'science',   name: 'Science',               teacher: 'Ms. Emily Johnson', pct: 82, color: '#16a34a', bg: '#f0fdf4' },
  { icon: 'menu_book', name: 'English Language Arts', teacher: 'Mr. David Brown',   pct: 90, color: '#2563eb', bg: '#eff6ff' },
  { icon: 'computer',  name: 'Computer Science',      teacher: 'Mr. Michael Lee',   pct: 85, color: '#7c3aed', bg: '#faf5ff' },
  { icon: 'public',    name: 'Social Studies',        teacher: 'Ms. Sarah Wilson',  pct: 78, color: '#ea580c', bg: '#fff7ed' },
  { icon: 'translate', name: 'Khmer Language',        teacher: 'Ms. Chanthou Sok',  pct: 80, color: '#db2777', bg: '#fdf2f8' },
];

document.getElementById('subjGrid').innerHTML = subjects.map(s => `
  <div class="subj-item">
    <div class="subj-ico" style="background:${s.bg}">
      <span class="mi" style="color:${s.color}">${s.icon}</span>
    </div>
    <div class="subj-body">
      <div class="subj-name">${s.name}</div>
      <div class="subj-teacher">${s.teacher}</div>
      <div class="subj-bar-row">
        <div class="subj-bar">
          <div class="subj-fill" data-w="${s.pct}" style="background:${s.color}"></div>
        </div>
        <span class="subj-pct">${s.pct}%</span>
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
