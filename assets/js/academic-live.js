/* NGIS Academic Live — small shared read model for every portal. */
(function () {
  'use strict';
  function esc(value) { return String(value == null ? '' : value).replace(/[&<>"']/g, function (c) { return ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' })[c]; }); }
  function role() { return (window.PAGE && window.PAGE.role) || (window.NGISAuth && NGISAuth.getRole && NGISAuth.getRole()) || 'student'; }
  function render(data) {
    var page = document.querySelector('.page'); if (!page || document.getElementById('academicLiveSummary')) return;
    var r = role(), model = data || {}, students = model.students || [], student = students[0];
    if (r === 'student' && model.student) student = model.student;
    var gpa = student && student.gpa != null ? Number(student.gpa).toFixed(2) : (model.gpa != null ? Number(model.gpa).toFixed(2) : '—');
    var att = student && student.attendance != null ? Number(student.attendance).toFixed(1) : (model.attendance != null ? Number(model.attendance).toFixed(1) : '—');
    var label = r === 'student' ? 'Your authoritative academic record' : 'Authoritative academic overview';
    var el = document.createElement('section'); el.id = 'academicLiveSummary'; el.className = 'card anim-up';
    el.style.cssText = 'margin:0 0 16px;border-left:4px solid #13829b;';
    el.innerHTML = '<div class="card-head"><div><h3 style="margin:0">Live academic data</h3><div class="sub">' + esc(label) + ' · synced from NGIS Academic Records</div></div><span class="badge green">LIVE</span></div>' +
      '<div class="card-pad" style="display:flex;gap:24px;flex-wrap:wrap;align-items:center">' +
      '<div><div class="faint" style="font-size:11px;text-transform:uppercase">GPA</div><strong style="font-size:24px">' + esc(gpa) + '</strong><span class="faint"> / 4.00</span></div>' +
      '<div><div class="faint" style="font-size:11px;text-transform:uppercase">Attendance</div><strong style="font-size:24px">' + esc(att) + '%</strong></div>' +
      '<div><div class="faint" style="font-size:11px;text-transform:uppercase">Records in view</div><strong style="font-size:24px">' + esc(model.total != null ? model.total : students.length) + '</strong></div>' +
      '<div class="faint" style="font-size:12px">Grades use the active grading period and published workflow state.</div></div>';
    page.insertBefore(el, page.firstChild);
  }
  async function boot() {
    if (!window.NGISAuth || !NGISAuth.api) return;
    try {
      var r = role(), url = r === 'student' ? '/api/academic/report-cards' : '/api/academic/overview';
      var response = await NGISAuth.api(url), data = response.data || {};
      if (r === 'student' && data.student) { data.total = (data.grades || []).length; data.gpa = data.gpa; data.attendance = data.attendance && data.attendance.percentage; }
      render(data);
    } catch (e) {
      var page = document.querySelector('.page');
      if (page && !document.getElementById('academicLiveSummary')) {
        var el = document.createElement('div'); el.id = 'academicLiveSummary'; el.className = 'card'; el.style.cssText = 'margin:0 0 16px;border-left:4px solid #dc2626'; el.innerHTML = '<div class="card-pad" style="font-size:13px;color:#991b1b">Academic records are temporarily unavailable. No local fallback data was shown.</div>'; page.insertBefore(el, page.firstChild);
      }
    }
  }
  window.addEventListener('DOMContentLoaded', function () { setTimeout(boot, 80); });
})();
