/**
 * NGIS System Management Engine
 * Powers the 16 views under the System section in the Admin Portal:
 * - initSchoolInfo: School Information profile
 * - initSchoolYear: Academic Year management
 * - initSchoolWeek: 40-Week academic calendar
 * - initExamConfig: Exam scoring weights & passing thresholds
 * - initScoreLock: Gradebook lockdown controls
 * - initDefineCurriculum: Curriculum track definitions
 * - initDesignCurriculum: Syllabus and unit structures
 * - initDeclareClass: Section declarations & capacity
 * - initStudentTransition: Annual promotion pipeline
 * - initTechnicianAssign: IT and proctor duty allocations
 * - initEmployeeGroup: Role groups & permissions
 * - initEmployeeAccounts: Faculty & staff credentials
 * - initStudentAccounts: Student portal access accounts
 * - initParentAccounts: Parent portal access accounts
 * - initSchedule: Master bell schedule & shift times
 * - initGeneralSetting: Institutional system preferences
 */

(function (window, document) {
  'use strict';

  var SYS = window.SYS_MGMT = window.SYS = window.SYS_MGMT || {};

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function toast(msg, type) {
    var existing = document.getElementById('sysToast');
    if (existing) existing.remove();
    var t = document.createElement('div');
    t.id = 'sysToast';
    var bg = type === 'error' ? 'bg-rose-600' : (type === 'info' ? 'bg-slate-800' : 'bg-[#176B45]');
    t.className = 'fixed bottom-5 right-5 z-50 flex items-center gap-2.5 px-4 py-2.5 rounded-xl shadow-lg text-white text-xs font-medium transition-all transform translate-y-0 ' + bg;
    t.innerHTML = '<span class="material-symbols-outlined text-sm">' + (type === 'error' ? 'error' : 'check_circle') + '</span><span>' + esc(msg) + '</span>';
    document.body.appendChild(t);
    setTimeout(function () {
      t.classList.add('opacity-0', 'translate-y-2');
      setTimeout(function () { t.remove(); }, 300);
    }, 3200);
  }

  // 1. School Information
  SYS.initSchoolInfo = function (containerId) {
    var root = document.getElementById(containerId);
    if (!root) return;
    root.innerHTML = '<div class="flex items-center justify-center py-20 text-slate-400"><span class="w-2.5 h-2.5 rounded-full bg-[#176B45] animate-ping mr-2"></span><span class="text-xs font-medium">Loading School Information...</span></div>';

    fetch('/api/system/school-info')
      .then(function (r) { return r.json(); })
      .then(function (res) {
        var d = res.data || {};
        root.innerHTML = '' +
          '<div class="max-w-4xl space-y-5">' +
            '<div class="bg-white border border-slate-200 rounded-xl p-5 shadow-2xs">' +
              '<div class="flex items-start justify-between pb-4 border-b border-slate-100">' +
                '<div class="flex items-center gap-3.5">' +
                  '<div class="w-14 h-14 rounded-2xl bg-emerald-50 border border-emerald-200 flex items-center justify-center text-2xl font-serif text-[#176B45]">' +
                    'NG' +
                  '</div>' +
                  '<div>' +
                    '<h2 class="text-base font-medium text-slate-900">' + esc(d.nameEnglish) + '</h2>' +
                    '<p class="text-xs text-slate-500 font-khmer mt-0.5">' + esc(d.nameKhmer) + '</p>' +
                  '</div>' +
                '</div>' +
                '<span class="inline-flex items-center px-2.5 py-1 rounded-md text-[11px] font-medium bg-emerald-50 text-[#176B45] border border-emerald-200 font-mono">' +
                  esc(d.moeysCode) +
                '</span>' +
              '</div>' +

              '<div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">' +
                '<div>' +
                  '<label class="text-xs text-slate-500 font-medium">Official School Name (English):</label>' +
                  '<input type="text" id="inpNameEn" class="w-full mt-1 p-2 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-[#176B45] text-slate-800" value="' + esc(d.nameEnglish) + '">' +
                '</div>' +
                '<div>' +
                  '<label class="text-xs text-slate-500 font-medium">Official School Name (Khmer):</label>' +
                  '<input type="text" id="inpNameKm" class="w-full mt-1 p-2 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-[#176B45] text-slate-800 font-khmer" value="' + esc(d.nameKhmer) + '">' +
                '</div>' +
                '<div>' +
                  '<label class="text-xs text-slate-500 font-medium">MoEYS Registration Code:</label>' +
                  '<input type="text" id="inpMoeysCode" class="w-full mt-1 p-2 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-[#176B45] text-slate-800 font-mono" value="' + esc(d.moeysCode) + '">' +
                '</div>' +
                '<div>' +
                  '<label class="text-xs text-slate-500 font-medium">Accreditation Body:</label>' +
                  '<input type="text" id="inpAccreditation" class="w-full mt-1 p-2 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-[#176B45] text-slate-800" value="' + esc(d.accreditation) + '">' +
                '</div>' +
                '<div>' +
                  '<label class="text-xs text-slate-500 font-medium">Executive Principal:</label>' +
                  '<input type="text" id="inpPrincipal" class="w-full mt-1 p-2 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-[#176B45] text-slate-800" value="' + esc(d.principal) + '">' +
                '</div>' +
                '<div>' +
                  '<label class="text-xs text-slate-500 font-medium">Primary Contact Telephone:</label>' +
                  '<input type="text" id="inpPhone" class="w-full mt-1 p-2 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-[#176B45] text-slate-800" value="' + esc(d.phone) + '">' +
                '</div>' +
                '<div class="md:col-span-2">' +
                  '<label class="text-xs text-slate-500 font-medium">Campus Physical Address:</label>' +
                  '<input type="text" id="inpAddress" class="w-full mt-1 p-2 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-[#176B45] text-slate-800" value="' + esc(d.address) + '">' +
                '</div>' +
                '<div class="md:col-span-2">' +
                  '<label class="text-xs text-slate-500 font-medium">Institutional Motto & Vision:</label>' +
                  '<input type="text" id="inpMotto" class="w-full mt-1 p-2 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-[#176B45] text-slate-800 italic" value="' + esc(d.motto) + '">' +
                '</div>' +
              '</div>' +

              '<div class="mt-5 pt-4 border-t border-slate-100 flex items-center justify-end">' +
                '<button type="button" id="btnSaveSchoolInfo" class="px-4 py-2 rounded-lg bg-[#176B45] text-white hover:bg-[#125638] text-xs font-medium transition-all shadow-xs cursor-pointer flex items-center gap-1.5">' +
                  '<span class="material-symbols-outlined text-sm">save</span>' +
                  '<span>Save School Information</span>' +
                '</button>' +
              '</div>' +
            '</div>' +
          '</div>';

        document.getElementById('btnSaveSchoolInfo').onclick = function () {
          var payload = {
            nameEnglish: document.getElementById('inpNameEn').value,
            nameKhmer: document.getElementById('inpNameKm').value,
            moeysCode: document.getElementById('inpMoeysCode').value,
            accreditation: document.getElementById('inpAccreditation').value,
            principal: document.getElementById('inpPrincipal').value,
            phone: document.getElementById('inpPhone').value,
            address: document.getElementById('inpAddress').value,
            motto: document.getElementById('inpMotto').value
          };
          fetch('/api/system/school-info', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          })
            .then(function (r) { return r.json(); })
            .then(function (res) {
              if (res.success) toast('School information updated successfully.');
            });
        };
      });
  };

  // 2. School Year
  SYS.initSchoolYear = function (containerId) {
    var root = document.getElementById(containerId);
    if (!root) return;
    fetch('/api/system/school-years')
      .then(function (r) { return r.json(); })
      .then(function (res) {
        var items = res.data || [];
        var rows = items.map(function (y) {
          var badge = y.status === 'active' ? '<span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">Current Active</span>' :
                      (y.status === 'planning' ? '<span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-blue-50 text-blue-700 border border-blue-200">Planning / Enrollment</span>' :
                                                 '<span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-slate-100 text-slate-500">Archived</span>');
          return '<tr class="border-b border-slate-100 hover:bg-slate-50/60">' +
            '<td class="py-3 px-3 font-mono text-xs text-slate-700 font-medium">' + esc(y.id) + '</td>' +
            '<td class="py-3 px-3 text-xs font-medium text-slate-800">' + esc(y.year) + '</td>' +
            '<td class="py-3 px-3 text-xs text-slate-600">' + esc(y.startDate) + '</td>' +
            '<td class="py-3 px-3 text-xs text-slate-600">' + esc(y.endDate) + '</td>' +
            '<td class="py-3 px-3 text-xs text-slate-700">' + y.termsCount + ' Semesters</td>' +
            '<td class="py-3 px-3">' + badge + '</td>' +
          '</tr>';
        }).join('');

        root.innerHTML = '' +
          '<div class="space-y-4">' +
            '<div class="bg-white border border-slate-200 rounded-xl p-3 shadow-2xs flex items-center justify-between">' +
              '<div class="text-xs font-medium text-slate-700 uppercase tracking-wider">Institutional Academic Years</div>' +
              '<button type="button" class="px-3 py-1.5 rounded-lg bg-[#176B45] text-white text-xs font-medium hover:bg-[#125638] transition-all cursor-pointer shadow-xs">+ Add Academic Year</button>' +
            '</div>' +
            '<div class="bg-white border border-slate-200 rounded-xl shadow-2xs overflow-hidden">' +
              '<table class="w-full text-left border-collapse">' +
                '<thead class="bg-slate-50/70 border-b border-slate-200 text-[11px] font-medium text-slate-500 uppercase">' +
                  '<tr><th class="py-2.5 px-3">Year ID</th><th class="py-2.5 px-3">Academic Period</th><th class="py-2.5 px-3">Start Date</th><th class="py-2.5 px-3">End Date</th><th class="py-2.5 px-3">Terms</th><th class="py-2.5 px-3">Status</th></tr>' +
                '</thead>' +
                '<tbody>' + rows + '</tbody>' +
              '</table>' +
            '</div>' +
          '</div>';
      });
  };

  // 3. School Week
  SYS.initSchoolWeek = function (containerId) {
    var root = document.getElementById(containerId);
    if (!root) return;
    fetch('/api/system/school-weeks')
      .then(function (r) { return r.json(); })
      .then(function (res) {
        var items = res.data || [];
        var rows = items.map(function (w) {
          var typeBadge = w.type === 'exam' ? '<span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-medium bg-rose-50 text-rose-700 border border-rose-200">Exam Window</span>' :
                          (w.type === 'vacation' ? '<span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-medium bg-amber-50 text-amber-700 border border-amber-200">Recess / Holiday</span>' :
                                                   '<span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">Instructional Week</span>');
          return '<tr class="border-b border-slate-100 hover:bg-slate-50/60">' +
            '<td class="py-3 px-3 font-mono text-xs text-slate-700 font-medium">W' + w.weekNumber + '</td>' +
            '<td class="py-3 px-3 text-xs font-medium text-slate-800">' + esc(w.label) + '</td>' +
            '<td class="py-3 px-3 text-xs text-slate-600">' + esc(w.startDate) + '</td>' +
            '<td class="py-3 px-3 text-xs text-slate-600">' + esc(w.endDate) + '</td>' +
            '<td class="py-3 px-3">' + typeBadge + '</td>' +
          '</tr>';
        }).join('');

        root.innerHTML = '' +
          '<div class="space-y-4">' +
            '<div class="bg-white border border-slate-200 rounded-xl p-3 shadow-2xs flex items-center justify-between">' +
              '<div class="text-xs font-medium text-slate-700 uppercase tracking-wider">40-Week Academic Calendar Structure</div>' +
              '<span class="text-xs text-slate-500 font-mono">AY 2025–26</span>' +
            '</div>' +
            '<div class="bg-white border border-slate-200 rounded-xl shadow-2xs overflow-hidden">' +
              '<table class="w-full text-left border-collapse">' +
                '<thead class="bg-slate-50/70 border-b border-slate-200 text-[11px] font-medium text-slate-500 uppercase">' +
                  '<tr><th class="py-2.5 px-3">Week</th><th class="py-2.5 px-3">Milestone & Focus</th><th class="py-2.5 px-3">Start Date</th><th class="py-2.5 px-3">End Date</th><th class="py-2.5 px-3">Category</th></tr>' +
                '</thead>' +
                '<tbody>' + rows + '</tbody>' +
              '</table>' +
            '</div>' +
          '</div>';
      });
  };

  // 4. Exam Configuration
  SYS.initExamConfig = function (containerId) {
    var root = document.getElementById(containerId);
    if (!root) return;
    fetch('/api/system/exam-config')
      .then(function (r) { return r.json(); })
      .then(function (res) {
        var d = res.data || {};
        var w = d.gradeWeighting || {};
        root.innerHTML = '' +
          '<div class="max-w-3xl space-y-4">' +
            '<div class="bg-white border border-slate-200 rounded-xl p-5 shadow-2xs space-y-4">' +
              '<h3 class="text-xs font-medium text-slate-700 uppercase tracking-wider">Examination & Grade Weighting Parameters</h3>' +
              '<div class="grid grid-cols-2 sm:grid-cols-4 gap-3 p-3.5 bg-slate-50 rounded-xl border border-slate-100">' +
                '<div><label class="text-[11px] text-slate-500">Final Exam Weight:</label><div class="text-lg font-medium text-slate-800 mt-0.5">' + w.finalExam + '%</div></div>' +
                '<div><label class="text-[11px] text-slate-500">Mid-Term Weight:</label><div class="text-lg font-medium text-slate-800 mt-0.5">' + w.midTermExam + '%</div></div>' +
                '<div><label class="text-[11px] text-slate-500">Assignments & Lab:</label><div class="text-lg font-medium text-slate-800 mt-0.5">' + w.assignmentsAndProjects + '%</div></div>' +
                '<div><label class="text-[11px] text-slate-500">Attendance/Ethics:</label><div class="text-lg font-medium text-slate-800 mt-0.5">' + w.attendanceAndParticipation + '%</div></div>' +
              '</div>' +
              '<div class="grid grid-cols-1 sm:grid-cols-2 gap-4">' +
                '<div>' +
                  '<label class="text-xs text-slate-500 font-medium">Official Passing Score Threshold:</label>' +
                  '<input type="number" class="w-full mt-1 p-2 text-xs bg-slate-50 border border-slate-200 rounded-lg text-slate-800" value="' + d.passingGrade + '">' +
                '</div>' +
                '<div>' +
                  '<label class="text-xs text-slate-500 font-medium">Honors Roll Minimum GPA:</label>' +
                  '<input type="number" step="0.05" class="w-full mt-1 p-2 text-xs bg-slate-50 border border-slate-200 rounded-lg text-slate-800" value="' + d.honorsMinimumGpa + '">' +
                '</div>' +
              '</div>' +
              '<div class="pt-3 border-t border-slate-100 flex justify-end">' +
                '<button type="button" class="px-4 py-2 rounded-lg bg-[#176B45] text-white hover:bg-[#125638] text-xs font-medium cursor-pointer" onclick="window.SYS_MGMT.saveMock(\'Examination parameters saved.\')">Update Policy</button>' +
              '</div>' +
            '</div>' +
          '</div>';
      });
  };

  // 5. Score Lock Configuration
  SYS.initScoreLock = function (containerId) {
    var root = document.getElementById(containerId);
    if (!root) return;
    fetch('/api/system/score-locks')
      .then(function (r) { return r.json(); })
      .then(function (res) {
        var items = res.data || [];
        var rows = items.map(function (l) {
          var isLocked = l.status === 'locked';
          var badge = isLocked ? '<span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-rose-50 text-rose-700 border border-rose-200">Locked</span>' :
                                 '<span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">Open for Input</span>';
          return '<tr class="border-b border-slate-100 hover:bg-slate-50/60">' +
            '<td class="py-3 px-3 text-xs font-medium text-slate-800">' + esc(l.class) + '</td>' +
            '<td class="py-3 px-3 text-xs text-slate-700">' + esc(l.subject) + '</td>' +
            '<td class="py-3 px-3 text-xs text-slate-600">' + esc(l.teacher) + '</td>' +
            '<td class="py-3 px-3 text-xs text-slate-600">' + esc(l.term) + '</td>' +
            '<td class="py-3 px-3">' + badge + '</td>' +
            '<td class="py-3 px-3 text-right">' +
              '<button type="button" class="btn-toggle-lock px-2.5 py-1 rounded-lg border border-slate-200 text-xs font-medium text-slate-700 hover:bg-slate-100 cursor-pointer" data-id="' + esc(l.id) + '">' +
                (isLocked ? 'Unlock Section' : 'Lock Section') +
              '</button>' +
            '</td>' +
          '</tr>';
        }).join('');

        root.innerHTML = '' +
          '<div class="space-y-4">' +
            '<div class="bg-white border border-slate-200 rounded-xl p-3 shadow-2xs flex items-center justify-between">' +
              '<div class="text-xs font-medium text-slate-700 uppercase tracking-wider">Faculty Gradebook Lockdown Oversight</div>' +
              '<button type="button" class="px-3 py-1.5 rounded-lg bg-rose-600 text-white text-xs font-medium hover:bg-rose-700 cursor-pointer shadow-xs" onclick="window.SYS_MGMT.saveMock(\'All gradebooks locked.\')">Lock All Sections</button>' +
            '</div>' +
            '<div class="bg-white border border-slate-200 rounded-xl shadow-2xs overflow-hidden">' +
              '<table class="w-full text-left border-collapse">' +
                '<thead class="bg-slate-50/70 border-b border-slate-200 text-[11px] font-medium text-slate-500 uppercase">' +
                  '<tr><th class="py-2.5 px-3">Class</th><th class="py-2.5 px-3">Subject</th><th class="py-2.5 px-3">Teacher</th><th class="py-2.5 px-3">Examination Term</th><th class="py-2.5 px-3">Lock Status</th><th class="py-2.5 px-3 text-right">Action</th></tr>' +
                '</thead>' +
                '<tbody>' + rows + '</tbody>' +
              '</table>' +
            '</div>' +
          '</div>';

        root.querySelectorAll('.btn-toggle-lock').forEach(function (btn) {
          btn.addEventListener('click', function () {
            var id = btn.getAttribute('data-id');
            fetch('/api/system/score-locks/toggle', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ id: id })
            }).then(function () {
              toast('Lock status updated.');
              SYS.initScoreLock(containerId);
            });
          });
        });
      });
  };

  // 6. Define Curriculum
  SYS.initDefineCurriculum = function (containerId) {
    var root = document.getElementById(containerId);
    if (!root) return;
    fetch('/api/system/curricula')
      .then(function (r) { return r.json(); })
      .then(function (res) {
        var items = res.data || [];
        var cards = items.map(function (c) {
          return '<div class="bg-white border border-slate-200 rounded-xl p-4 shadow-2xs">' +
            '<div class="flex items-center justify-between mb-2">' +
              '<span class="text-xs font-mono font-medium text-slate-500">' + esc(c.code) + '</span>' +
              '<span class="px-2 py-0.5 rounded text-[11px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">Accredited</span>' +
            '</div>' +
            '<h4 class="text-sm font-medium text-slate-900 mb-1">' + esc(c.title) + '</h4>' +
            '<p class="text-xs text-slate-500 mb-3">' + esc(c.authority) + ' · ' + esc(c.grades) + '</p>' +
            '<div class="text-[11px] font-medium text-slate-600 mb-1.5">Core Disciplines:</div>' +
            '<div class="flex flex-wrap gap-1">' +
              c.coreSubjects.map(function (s) { return '<span class="px-2 py-0.5 rounded bg-slate-100 text-slate-700 text-[11px]">' + esc(s) + '</span>'; }).join('') +
            '</div>' +
          '</div>';
        }).join('');

        root.innerHTML = '' +
          '<div class="space-y-4">' +
            '<div class="bg-white border border-slate-200 rounded-xl p-3 shadow-2xs flex items-center justify-between">' +
              '<div class="text-xs font-medium text-slate-700 uppercase tracking-wider">Accredited Curriculum Frameworks</div>' +
              '<button type="button" class="px-3 py-1.5 rounded-lg bg-[#176B45] text-white text-xs font-medium hover:bg-[#125638] cursor-pointer shadow-xs">+ Define Framework</button>' +
            '</div>' +
            '<div class="grid grid-cols-1 md:grid-cols-3 gap-3">' + cards + '</div>' +
          '</div>';
      });
  };

  // 7. Design Curriculum
  SYS.initDesignCurriculum = function (containerId) {
    var root = document.getElementById(containerId);
    if (!root) return;
    fetch('/api/system/curriculum-designs')
      .then(function (r) { return r.json(); })
      .then(function (res) {
        var items = res.data || [];
        var rows = items.map(function (d) {
          return '<tr class="border-b border-slate-100 hover:bg-slate-50/60">' +
            '<td class="py-3 px-3 font-mono text-xs text-slate-700 font-medium">' + esc(d.id) + '</td>' +
            '<td class="py-3 px-3 text-xs font-medium text-slate-800">' + esc(d.curriculumId) + '</td>' +
            '<td class="py-3 px-3 text-xs text-slate-700">' + esc(d.grade) + '</td>' +
            '<td class="py-3 px-3 text-xs text-slate-700 font-medium">' + d.totalHours + ' hrs</td>' +
            '<td class="py-3 px-3 text-xs text-slate-600">' + esc(d.chair) + '</td>' +
            '<td class="py-3 px-3 text-xs font-mono text-slate-500">' + esc(d.approvedDate) + '</td>' +
          '</tr>';
        }).join('');

        root.innerHTML = '' +
          '<div class="space-y-4">' +
            '<div class="bg-white border border-slate-200 rounded-xl p-3 shadow-2xs flex items-center justify-between">' +
              '<div class="text-xs font-medium text-slate-700 uppercase tracking-wider">Curriculum Syllabus Design &amp; Hour Mapping</div>' +
              '<button type="button" class="px-3 py-1.5 rounded-lg bg-[#176B45] text-white text-xs font-medium hover:bg-[#125638] cursor-pointer shadow-xs">+ Design New Syllabus</button>' +
            '</div>' +
            '<div class="bg-white border border-slate-200 rounded-xl shadow-2xs overflow-hidden">' +
              '<table class="w-full text-left border-collapse">' +
                '<thead class="bg-slate-50/70 border-b border-slate-200 text-[11px] font-medium text-slate-500 uppercase">' +
                  '<tr><th class="py-2.5 px-3">Design ID</th><th class="py-2.5 px-3">Track</th><th class="py-2.5 px-3">Target Grade</th><th class="py-2.5 px-3">Annual Hours</th><th class="py-2.5 px-3">Chairperson</th><th class="py-2.5 px-3">Approval Date</th></tr>' +
                '</thead>' +
                '<tbody>' + rows + '</tbody>' +
              '</table>' +
            '</div>' +
          '</div>';
      });
  };

  // 8. Declare Class
  SYS.initDeclareClass = function (containerId) {
    var root = document.getElementById(containerId);
    if (!root) return;
    fetch('/api/system/declared-classes')
      .then(function (r) { return r.json(); })
      .then(function (res) {
        var items = res.data || [];
        var rows = items.map(function (c) {
          return '<tr class="border-b border-slate-100 hover:bg-slate-50/60">' +
            '<td class="py-3 px-3 font-mono text-xs text-slate-700 font-medium">' + esc(c.classCode) + '</td>' +
            '<td class="py-3 px-3 text-xs font-medium text-slate-800">' + esc(c.name) + '</td>' +
            '<td class="py-3 px-3 text-xs text-slate-700">' + esc(c.room) + '</td>' +
            '<td class="py-3 px-3 text-xs text-slate-600">' + esc(c.shift) + '</td>' +
            '<td class="py-3 px-3 text-xs text-slate-700 font-medium">' + c.enrolled + ' / ' + c.maxCapacity + '</td>' +
            '<td class="py-3 px-3"><span class="px-2 py-0.5 rounded text-[11px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">Active Section</span></td>' +
          '</tr>';
        }).join('');

        root.innerHTML = '' +
          '<div class="space-y-4">' +
            '<div class="bg-white border border-slate-200 rounded-xl p-3 shadow-2xs flex items-center justify-between">' +
              '<div class="text-xs font-medium text-slate-700 uppercase tracking-wider">Declared Class Cohorts (AY 2025–26)</div>' +
              '<button type="button" class="px-3 py-1.5 rounded-lg bg-[#176B45] text-white text-xs font-medium hover:bg-[#125638] cursor-pointer shadow-xs">+ Declare New Class</button>' +
            '</div>' +
            '<div class="bg-white border border-slate-200 rounded-xl shadow-2xs overflow-hidden">' +
              '<table class="w-full text-left border-collapse">' +
                '<thead class="bg-slate-50/70 border-b border-slate-200 text-[11px] font-medium text-slate-500 uppercase">' +
                  '<tr><th class="py-2.5 px-3">Class Code</th><th class="py-2.5 px-3">Full Title</th><th class="py-2.5 px-3">Assigned Room</th><th class="py-2.5 px-3">Shift</th><th class="py-2.5 px-3">Enrollment / Max</th><th class="py-2.5 px-3">Status</th></tr>' +
                '</thead>' +
                '<tbody>' + rows + '</tbody>' +
              '</table>' +
            '</div>' +
          '</div>';
      });
  };

  // 9. Student Transition
  SYS.initStudentTransition = function (containerId) {
    var root = document.getElementById(containerId);
    if (!root) return;
    fetch('/api/system/student-transitions')
      .then(function (r) { return r.json(); })
      .then(function (res) {
        var items = res.data || [];
        var rows = items.map(function (t) {
          var badge = t.transitionStatus === 'completed' ? '<span class="px-2 py-0.5 rounded text-[11px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">Finalized</span>' :
                                                           '<span class="px-2 py-0.5 rounded text-[11px] font-medium bg-amber-50 text-amber-700 border border-amber-200">Pending Finals</span>';
          return '<tr class="border-b border-slate-100 hover:bg-slate-50/60">' +
            '<td class="py-3 px-3 text-xs font-medium text-slate-800">' + esc(t.cohort) + '</td>' +
            '<td class="py-3 px-3 text-xs font-medium text-[#176B45]">' + esc(t.destination) + '</td>' +
            '<td class="py-3 px-3 text-xs text-slate-700">' + t.totalStudents + ' Students</td>' +
            '<td class="py-3 px-3 text-xs text-emerald-700 font-medium">' + t.promoted + ' Promoted</td>' +
            '<td class="py-3 px-3 text-xs text-slate-500">' + t.retained + ' Retained</td>' +
            '<td class="py-3 px-3">' + badge + '</td>' +
          '</tr>';
        }).join('');

        root.innerHTML = '' +
          '<div class="space-y-4">' +
            '<div class="bg-white border border-slate-200 rounded-xl p-3 shadow-2xs flex items-center justify-between">' +
              '<div class="text-xs font-medium text-slate-700 uppercase tracking-wider">Annual Student Transition &amp; Promotion Batches</div>' +
              '<button type="button" class="px-3 py-1.5 rounded-lg bg-[#176B45] text-white text-xs font-medium hover:bg-[#125638] cursor-pointer shadow-xs" onclick="window.SYS_MGMT.saveMock(\'Transition batch simulated.\')">Run Promotion Audit</button>' +
            '</div>' +
            '<div class="bg-white border border-slate-200 rounded-xl shadow-2xs overflow-hidden">' +
              '<table class="w-full text-left border-collapse">' +
                '<thead class="bg-slate-50/70 border-b border-slate-200 text-[11px] font-medium text-slate-500 uppercase">' +
                  '<tr><th class="py-2.5 px-3">Current Cohort</th><th class="py-2.5 px-3">Promoted Cohort</th><th class="py-2.5 px-3">Total Candidates</th><th class="py-2.5 px-3">Promoted</th><th class="py-2.5 px-3">Retained</th><th class="py-2.5 px-3">Status</th></tr>' +
                '</thead>' +
                '<tbody>' + rows + '</tbody>' +
              '</table>' +
            '</div>' +
          '</div>';
      });
  };

  // 10. Technician & Monitor Assign
  SYS.initTechnicianAssign = function (containerId) {
    var root = document.getElementById(containerId);
    if (!root) return;
    fetch('/api/system/technicians')
      .then(function (r) { return r.json(); })
      .then(function (res) {
        var items = res.data || [];
        var rows = items.map(function (t) {
          return '<tr class="border-b border-slate-100 hover:bg-slate-50/60">' +
            '<td class="py-3 px-3 font-mono text-xs text-slate-700 font-medium">' + esc(t.id) + '</td>' +
            '<td class="py-3 px-3 text-xs font-medium text-slate-800">' + esc(t.staffName) + '</td>' +
            '<td class="py-3 px-3 text-xs text-slate-700">' + esc(t.role) + '</td>' +
            '<td class="py-3 px-3 text-xs text-slate-600">' + esc(t.assignedZone) + '</td>' +
            '<td class="py-3 px-3 text-xs font-mono text-slate-500">' + esc(t.phone) + '</td>' +
            '<td class="py-3 px-3"><span class="px-2 py-0.5 rounded text-[11px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">On Duty</span></td>' +
          '</tr>';
        }).join('');

        root.innerHTML = '' +
          '<div class="space-y-4">' +
            '<div class="bg-white border border-slate-200 rounded-xl p-3 shadow-2xs flex items-center justify-between">' +
              '<div class="text-xs font-medium text-slate-700 uppercase tracking-wider">Campus Technicians &amp; Invigilator Duty Allocations</div>' +
              '<button type="button" class="px-3 py-1.5 rounded-lg bg-[#176B45] text-white text-xs font-medium hover:bg-[#125638] cursor-pointer shadow-xs">+ Assign Technician</button>' +
            '</div>' +
            '<div class="bg-white border border-slate-200 rounded-xl shadow-2xs overflow-hidden">' +
              '<table class="w-full text-left border-collapse">' +
                '<thead class="bg-slate-50/70 border-b border-slate-200 text-[11px] font-medium text-slate-500 uppercase">' +
                  '<tr><th class="py-2.5 px-3">Staff ID</th><th class="py-2.5 px-3">Name</th><th class="py-2.5 px-3">Role</th><th class="py-2.5 px-3">Zone / Building</th><th class="py-2.5 px-3">Phone</th><th class="py-2.5 px-3">Duty Status</th></tr>' +
                '</thead>' +
                '<tbody>' + rows + '</tbody>' +
              '</table>' +
            '</div>' +
          '</div>';
      });
  };

  // 11. Employee Group
  SYS.initEmployeeGroup = function (containerId) {
    var root = document.getElementById(containerId);
    if (!root) return;
    fetch('/api/system/account-groups')
      .then(function (r) { return r.json(); })
      .then(function (res) {
        var items = res.data || [];
        var cards = items.map(function (g) {
          return '<div class="bg-white border border-slate-200 rounded-xl p-4 shadow-2xs">' +
            '<div class="flex items-center justify-between mb-2">' +
              '<span class="text-xs font-mono font-medium text-slate-400">' + esc(g.code) + '</span>' +
              '<span class="px-2 py-0.5 rounded text-[11px] font-medium bg-slate-100 text-slate-700">' + g.membersCount + ' Accounts</span>' +
            '</div>' +
            '<h4 class="text-sm font-medium text-slate-900 mb-2">' + esc(g.name) + '</h4>' +
            '<div class="text-[11px] font-medium text-slate-500 mb-1.5">Authorized Permissions:</div>' +
            '<div class="flex flex-wrap gap-1">' +
              g.permissions.map(function (p) { return '<span class="px-2 py-0.5 rounded bg-emerald-50 text-[#176B45] text-[10px] font-medium border border-emerald-200">' + esc(p) + '</span>'; }).join('') +
            '</div>' +
          '</div>';
        }).join('');

        root.innerHTML = '' +
          '<div class="space-y-4">' +
            '<div class="bg-white border border-slate-200 rounded-xl p-3 shadow-2xs flex items-center justify-between">' +
              '<div class="text-xs font-medium text-slate-700 uppercase tracking-wider">Access Control Groups &amp; RBAC Matrix</div>' +
              '<button type="button" class="px-3 py-1.5 rounded-lg bg-[#176B45] text-white text-xs font-medium hover:bg-[#125638] cursor-pointer shadow-xs">+ Create Role Group</button>' +
            '</div>' +
            '<div class="grid grid-cols-1 md:grid-cols-3 gap-3">' + cards + '</div>' +
          '</div>';
      });
  };

  // 12. Employee Accounts / Student Accounts / Parent Accounts (General Accounts Renderer)
  SYS.initAccounts = function (containerId, roleFilter, titleLabel) {
    var root = document.getElementById(containerId);
    if (!root) return;
    var url = '/api/system/accounts' + (roleFilter ? '?role=' + encodeURIComponent(roleFilter) : '');
    fetch(url)
      .then(function (r) { return r.json(); })
      .then(function (res) {
        var items = res.data || [];
        var rows = items.map(function (a) {
          return '<tr class="border-b border-slate-100 hover:bg-slate-50/60">' +
            '<td class="py-3 px-3 font-mono text-xs text-slate-700 font-medium">' + esc(a.id) + '</td>' +
            '<td class="py-3 px-3 text-xs font-medium text-slate-800">' + esc(a.name) + '</td>' +
            '<td class="py-3 px-3 text-xs font-mono text-slate-600">' + esc(a.username) + '</td>' +
            '<td class="py-3 px-3 text-xs text-slate-700">' + esc(a.role) + '</td>' +
            '<td class="py-3 px-3"><span class="px-2 py-0.5 rounded text-[11px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">Active</span></td>' +
            '<td class="py-3 px-3 text-xs font-mono text-slate-400">' + esc(a.lastLogin) + '</td>' +
            '<td class="py-3 px-3 text-right">' +
              '<button type="button" class="text-xs text-[#176B45] hover:underline font-medium cursor-pointer" onclick="window.SYS_MGMT.saveMock(\'Password reset sent to ' + esc(a.username) + '\')">Reset Password</button>' +
            '</td>' +
          '</tr>';
        }).join('');

        root.innerHTML = '' +
          '<div class="space-y-4">' +
            '<div class="bg-white border border-slate-200 rounded-xl p-3 shadow-2xs flex items-center justify-between">' +
              '<div class="text-xs font-medium text-slate-700 uppercase tracking-wider">' + esc(titleLabel) + ' Directory</div>' +
              '<button type="button" class="px-3 py-1.5 rounded-lg bg-[#176B45] text-white text-xs font-medium hover:bg-[#125638] cursor-pointer shadow-xs">+ Add Account</button>' +
            '</div>' +
            '<div class="bg-white border border-slate-200 rounded-xl shadow-2xs overflow-hidden">' +
              '<table class="w-full text-left border-collapse">' +
                '<thead class="bg-slate-50/70 border-b border-slate-200 text-[11px] font-medium text-slate-500 uppercase">' +
                  '<tr><th class="py-2.5 px-3">User ID</th><th class="py-2.5 px-3">Full Name</th><th class="py-2.5 px-3">Login / Email</th><th class="py-2.5 px-3">Assigned Role</th><th class="py-2.5 px-3">Status</th><th class="py-2.5 px-3">Last Access</th><th class="py-2.5 px-3 text-right">Action</th></tr>' +
                '</thead>' +
                '<tbody>' + (rows || '<tr><td colspan="7" class="text-center py-10 text-xs text-slate-400">No accounts in this category.</td></tr>') + '</tbody>' +
              '</table>' +
            '</div>' +
          '</div>';
      });
  };

  // 13. Schedule
  SYS.initSchedule = function (containerId) {
    var root = document.getElementById(containerId);
    if (!root) return;
    fetch('/api/system/schedule')
      .then(function (r) { return r.json(); })
      .then(function (res) {
        var s = res.data || {};
        root.innerHTML = '' +
          '<div class="max-w-3xl space-y-4">' +
            '<div class="bg-white border border-slate-200 rounded-xl p-5 shadow-2xs space-y-4">' +
              '<h3 class="text-xs font-medium text-slate-700 uppercase tracking-wider">Institutional Bell Schedule &amp; Shift Timetable</h3>' +
              '<div class="grid grid-cols-1 sm:grid-cols-2 gap-4 p-4 bg-slate-50 rounded-xl border border-slate-100">' +
                '<div>' +
                  '<div class="text-xs font-medium text-slate-800 mb-1">Morning Shift (Junior Secondary):</div>' +
                  '<div class="text-sm font-mono text-emerald-800">' + s.morningShiftStart + ' – ' + s.morningShiftEnd + '</div>' +
                '</div>' +
                '<div>' +
                  '<div class="text-xs font-medium text-slate-800 mb-1">Afternoon Shift (Primary / Remedial):</div>' +
                  '<div class="text-sm font-mono text-blue-800">' + s.afternoonShiftStart + ' – ' + s.afternoonShiftEnd + '</div>' +
                '</div>' +
                '<div class="sm:col-span-2 pt-2 border-t border-slate-200">' +
                  '<div class="text-xs font-medium text-slate-800 mb-1">Full Day Modular Program (High School &amp; Cambridge):</div>' +
                  '<div class="text-sm font-mono text-purple-800">' + s.fullDayStart + ' – ' + s.fullDayEnd + ' (' + s.periodsPerDay + ' periods daily)</div>' +
                '</div>' +
              '</div>' +
              '<div class="pt-3 border-t border-slate-100 flex justify-end">' +
                '<button type="button" class="px-4 py-2 rounded-lg bg-[#176B45] text-white hover:bg-[#125638] text-xs font-medium cursor-pointer" onclick="window.SYS_MGMT.saveMock(\'Schedule updated successfully.\')">Save Schedule Config</button>' +
              '</div>' +
            '</div>' +
          '</div>';
      });
  };

  // 14. General Setting
  SYS.initGeneralSetting = function (containerId) {
    var root = document.getElementById(containerId);
    if (!root) return;
    fetch('/api/system/general-settings')
      .then(function (r) { return r.json(); })
      .then(function (res) {
        var g = res.data || {};
        root.innerHTML = '' +
          '<div class="max-w-3xl space-y-4">' +
            '<div class="bg-white border border-slate-200 rounded-xl p-5 shadow-2xs space-y-4">' +
              '<h3 class="text-xs font-medium text-slate-700 uppercase tracking-wider">System-Wide Operational Preferences</h3>' +
              '<div class="grid grid-cols-1 sm:grid-cols-2 gap-4">' +
                '<div>' +
                  '<label class="text-xs text-slate-500 font-medium">System Timezone:</label>' +
                  '<input type="text" class="w-full mt-1 p-2 text-xs bg-slate-50 border border-slate-200 rounded-lg text-slate-800" value="' + esc(g.timezone) + '">' +
                '</div>' +
                '<div>' +
                  '<label class="text-xs text-slate-500 font-medium">Default Locale / Language:</label>' +
                  '<input type="text" class="w-full mt-1 p-2 text-xs bg-slate-50 border border-slate-200 rounded-lg text-slate-800" value="' + esc(g.defaultLanguage) + '">' +
                '</div>' +
                '<div>' +
                  '<label class="text-xs text-slate-500 font-medium">Automatic Nightly Backup Hour:</label>' +
                  '<input type="text" class="w-full mt-1 p-2 text-xs bg-slate-50 border border-slate-200 rounded-lg text-slate-800 font-mono" value="' + esc(g.backupHour) + '">' +
                '</div>' +
                '<div>' +
                  '<label class="text-xs text-slate-500 font-medium">Active Academic Cycle:</label>' +
                  '<input type="text" class="w-full mt-1 p-2 text-xs bg-slate-50 border border-slate-200 rounded-lg text-slate-800" value="' + esc(g.academicYear) + '">' +
                '</div>' +
              '</div>' +
              '<div class="pt-3 border-t border-slate-100 flex justify-end gap-2">' +
                '<button type="button" class="px-3.5 py-2 rounded-lg border border-slate-200 text-slate-700 hover:bg-slate-100 text-xs font-medium cursor-pointer" onclick="window.SYS_MGMT.saveMock(\'Full database snapshot triggered.\')">Trigger Database Backup</button>' +
                '<button type="button" class="px-4 py-2 rounded-lg bg-[#176B45] text-white hover:bg-[#125638] text-xs font-medium cursor-pointer" onclick="window.SYS_MGMT.saveMock(\'General settings saved.\')">Save Preferences</button>' +
              '</div>' +
            '</div>' +
          '</div>';
      });
  };

  SYS.saveMock = function (msg) {
    toast(msg || 'Configuration saved.');
  };

})(window, document);
