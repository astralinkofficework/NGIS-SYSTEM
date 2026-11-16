/* ══════════════════════════════════════
   SUBJECTS — Data + DOM Rendering with
   Strict Department Isolation
   ══════════════════════════════════════ */

(function () {
  'use strict';

  var ALL_SUBJECTS = [
    // English Department Subjects
    { dept: 'English Department', icon: 'calculate', name: 'Mathematics', teacher: 'Mr. John Smith', pct: 88, color: '#2563eb', bg: '#eff6ff', code: 'MATH' },
    { dept: 'English Department', icon: 'science', name: 'Science', teacher: 'Ms. Emily Johnson', pct: 82, color: '#16a34a', bg: '#f0fdf4', code: 'SCI' },
    { dept: 'English Department', icon: 'menu_book', name: 'English Language Arts', teacher: 'Mr. David Brown', pct: 90, color: '#2563eb', bg: '#eff6ff', code: 'ENG' },
    { dept: 'English Department', icon: 'computer', name: 'Computer Science', teacher: 'Mr. Michael Lee', pct: 85, color: '#7c3aed', bg: '#faf5ff', code: 'CS' },
    { dept: 'English Department', icon: 'public', name: 'Social Studies', teacher: 'Ms. Sarah Wilson', pct: 78, color: '#ea580c', bg: '#fff7ed', code: 'SOC' },

    // Khmer Department Subjects
    { dept: 'Khmer Studies Department', icon: 'translate', name: 'Khmer Literature', teacher: 'Mr. Chhem Sokha', pct: 86, color: '#db2777', bg: '#fdf2f8', code: 'KHM' },
    { dept: 'Khmer Studies Department', icon: 'history_edu', name: 'Cambodian History & Civics', teacher: 'Ms. Chanthou Sok', pct: 84, color: '#059669', bg: '#ecfdf5', code: 'KHM-HIST' },

    // Chinese Department Subjects
    { dept: 'Chinese Language Department', icon: 'translate', name: 'Mandarin Chinese I', teacher: 'Ms. Li Wei', pct: 91, color: '#b91c1c', bg: '#fef2f2', code: 'CHN' },
    { dept: 'Chinese Language Department', icon: 'school', name: 'HSK Chinese Preparation', teacher: 'Ms. Li Wei', pct: 88, color: '#d97706', bg: '#fffbeb', code: 'HSK' }
  ];

  var activeDeptFilter = 'all';

  function renderGrid(subjectsList) {
    var grid = document.getElementById('subjGrid');
    if (!grid) return;

    if (!subjectsList.length) {
      grid.innerHTML = '<div style="grid-column:1/-1;padding:24px;text-align:center;color:#64748b;font-size:12px;background:#f8fafc;border-radius:12px;border:1px dashed #cbd5e1;">No subjects registered for this department.</div>';
      return;
    }

    grid.innerHTML = subjectsList.map(function (s) {
      return '<div class="subj-item">' +
        '<div class="subj-ico" style="background:' + s.bg + '">' +
          '<span class="mi" style="color:' + s.color + '">' + s.icon + '</span>' +
        '</div>' +
        '<div class="subj-body">' +
          '<div class="subj-name">' + s.name + '</div>' +
          '<div class="subj-teacher">' + s.teacher + ' &middot; <span style="font-size:11px;color:#64748b;">' + s.dept.replace(' Department', '').replace(' Studies', '').replace(' Language', '') + '</span></div>' +
          '<div class="subj-bar-row">' +
            '<div class="subj-bar">' +
              '<div class="subj-fill" data-w="' + s.pct + '" style="background:' + s.color + '"></div>' +
            '</div>' +
            '<span class="subj-pct">' + s.pct + '%</span>' +
          '</div>' +
        '</div>' +
      '</div>';
    }).join('');

    setTimeout(function () {
      document.querySelectorAll('.subj-fill').forEach(function (el) {
        el.style.width = el.dataset.w + '%';
      });
    }, 150);
  }

  function renderDepartmentTabs(enrollments) {
    var headL = document.querySelector('.subj-card .sec-head-l');
    if (!headL) return;

    var existingTabs = document.getElementById('studentDeptTabs');
    if (existingTabs) existingTabs.remove();

    var tabsWrap = document.createElement('div');
    tabsWrap.id = 'studentDeptTabs';
    tabsWrap.style.cssText = 'display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin:10px 0 14px;padding:0 2px;';

    var tabs = [{ id: 'all', label: 'All Enrolled (' + enrollments.length + ' depts)' }];
    enrollments.forEach(function (e) {
      var shortDept = (e.department || '').replace(' Department', '').replace(' Studies', '').replace(' Language', '').trim();
      tabs.push({
        id: e.department,
        label: shortDept + ' (' + (e.class || e.grade || '') + ')'
      });
    });

    tabsWrap.innerHTML = tabs.map(function (t) {
      var isAct = activeDeptFilter === t.id;
      return '<button type="button" class="dept-tab-btn" data-dept-id="' + t.id + '" style="font-size:11px;font-weight:500;padding:4px 10px;border-radius:20px;border:1px solid ' +
        (isAct ? '#176B45' : '#E2E8F0') + ';background:' + (isAct ? '#E8F3ED' : '#FFFFFF') +
        ';color:' + (isAct ? '#176B45' : '#475569') + ';cursor:pointer;transition:all 120ms ease;">' + t.label + '</button>';
    }).join('');

    var card = document.querySelector('.subj-card');
    var list = document.querySelector('.subj-card .subj-list');
    if (card && list) card.insertBefore(tabsWrap, list);

    // Wire tab clicks
    tabsWrap.querySelectorAll('.dept-tab-btn').forEach(function (btn) {
      btn.onclick = function () {
        activeDeptFilter = btn.getAttribute('data-dept-id');
        tabsWrap.querySelectorAll('.dept-tab-btn').forEach(function (b) {
          var sel = b.getAttribute('data-dept-id') === activeDeptFilter;
          b.style.borderColor = sel ? '#176B45' : '#E2E8F0';
          b.style.backgroundColor = sel ? '#E8F3ED' : '#FFFFFF';
          b.style.color = sel ? '#176B45' : '#475569';
        });
        filterAndRender(enrollments);
      };
    });
  }

  function filterAndRender(enrollments) {
    var enrolledDeptNames = enrollments.map(function (e) { return e.department; });
    var visible = ALL_SUBJECTS.filter(function (s) {
      // Must belong to an actively enrolled department
      var inEnrolled = enrolledDeptNames.some(function (d) {
        return d && (s.dept.toLowerCase().indexOf(d.toLowerCase()) >= 0 || d.toLowerCase().indexOf(s.dept.toLowerCase()) >= 0);
      });
      if (!inEnrolled) return false;
      if (activeDeptFilter === 'all') return true;
      return s.dept.toLowerCase().indexOf(activeDeptFilter.toLowerCase()) >= 0 || activeDeptFilter.toLowerCase().indexOf(s.dept.toLowerCase()) >= 0;
    });

    var cnt = document.querySelector('.subj-card .cnt');
    if (cnt) cnt.textContent = '(' + visible.length + ')';

    renderGrid(visible);
  }

  function init() {
    fetch('/api/student/dashboard')
      .then(function (r) { return r.json(); })
      .then(function (j) {
        var student = (j && j.data && j.data.student) || {};
        var enrollments = student.enrollments || [
          { department: 'English Department', grade: student.grade || 'Grade 10', class: student.class || '10A' },
          { department: 'Khmer Studies Department', grade: student.grade || 'Grade 10', class: student.class || '10A' }
        ];

        renderDepartmentTabs(enrollments);
        filterAndRender(enrollments);
      })
      .catch(function () {
        // Fallback default
        var defEnrollments = [
          { department: 'English Department', grade: 'Grade 10', class: '10A' },
          { department: 'Khmer Studies Department', grade: 'Grade 10', class: '10A' }
        ];
        renderDepartmentTabs(defEnrollments);
        filterAndRender(defEnrollments);
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
