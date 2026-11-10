/**
 * NGIS SYSTEM — Admin Timetable Oversight & Workflow Monitoring
 * Production JavaScript Controller
 * Strictly font-medium and font-normal (NO BOLD FONTS)
 */

(function (window, document) {
  'use strict';

  var TIMETABLE_OVERSIGHT = {
    data: null,
    reminders: [],
    currentStage: null,
    currentClassId: 'class_7A',
    currentFilter: 'all',
    currentGradeFilter: 'all',
    currentSearch: '',
    previewMode: 'draft', // 'draft' or 'published'
    previewTeacherId: 'all',

    init: function () {
      var self = this;
      self.bindEvents();
      self.fetchData();
    },

    bindEvents: function () {
      var self = this;

      // Close modal on escape
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
          self.closeModal();
          self.closeDrawer();
        }
      });
    },

    fetchData: function () {
      var self = this;
      var refreshBtn = document.getElementById('btnRefresh');
      if (refreshBtn) refreshBtn.classList.add('animate-spin');

      fetch('/api/timetable/oversight/status')
        .then(function (res) { return res.json(); })
        .then(function (res) {
          if (refreshBtn) refreshBtn.classList.remove('animate-spin');
          if (res.success) {
            self.data = res;
            self.reminders = res.reminders || [];
            self.renderAll();
          } else {
            self.showToast(res.error || 'Failed to load timetable oversight data', 'error');
          }
        })
        .catch(function (err) {
          if (refreshBtn) refreshBtn.classList.remove('animate-spin');
          console.error('Oversight fetch error:', err);
          self.showToast('Network error loading oversight status', 'error');
        });
    },

    renderAll: function () {
      var self = this;
      if (!self.data) return;

      self.renderWorkflowStages();
      self.renderSummaryKPIs();
      self.renderOutstandingTasks();
      self.renderTimetablePreview();
      self.renderReviewQueue();
      self.renderReminderHistory();
      self.renderActivityTimeline();
    },

    // ── 1. Workflow Stages Diagram ──────────────────────────────────────────
    renderWorkflowStages: function () {
      var self = this;
      var container = document.getElementById('workflowStagesContainer');
      if (!container || !self.data.stages) return;

      var stages = self.data.stages;
      var html = '';

      stages.forEach(function (stage, idx) {
        var statusBadgeClass = '';
        var statusDotClass = '';
        var status = stage.status;

        if (status === 'Completed') {
          statusBadgeClass = 'bg-emerald-50 text-emerald-700 border border-emerald-200';
          statusDotClass = 'bg-emerald-500';
        } else if (status === 'Needs Attention') {
          statusBadgeClass = 'bg-amber-50 text-amber-700 border border-amber-200';
          statusDotClass = 'bg-amber-500 animate-pulse';
        } else if (status === 'In Progress') {
          statusBadgeClass = 'bg-blue-50 text-blue-700 border border-blue-200';
          statusDotClass = 'bg-blue-500';
        } else if (status === 'Awaiting Review') {
          statusBadgeClass = 'bg-purple-50 text-purple-700 border border-purple-200';
          statusDotClass = 'bg-purple-500';
        } else {
          statusBadgeClass = 'bg-slate-50 text-slate-600 border border-slate-200';
          statusDotClass = 'bg-slate-400';
        }

        var isLast = idx === stages.length - 1;

        html += '<div class="relative flex-1 min-w-[200px] bg-white border border-[#E1E9E3] hover:border-emerald-600/40 rounded-2xl p-4 transition shadow-sm hover:shadow cursor-pointer group" onclick="TIMETABLE_OVERSIGHT.openStageDrawer(' + stage.step + ')">';
        html += '  <div class="flex items-center justify-between mb-2">';
        html += '    <span class="inline-flex items-center justify-center w-7 h-7 rounded-lg bg-emerald-50 text-emerald-800 text-xs font-medium border border-emerald-200/60">0' + stage.step + '</span>';
        html += '    <span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[11px] font-medium ' + statusBadgeClass + '">';
        html += '      <span class="w-1.5 h-1.5 rounded-full ' + statusDotClass + '"></span>' + status;
        html += '    </span>';
        html += '  </div>';

        html += '  <h3 class="text-sm font-medium text-slate-800 group-hover:text-emerald-700 transition flex items-center justify-between">';
        html += '    <span>' + stage.name + '</span>';
        html += '    <span class="material-symbols-outlined text-[16px] text-slate-400 group-hover:translate-x-0.5 transition">chevron_right</span>';
        html += '  </h3>';
        html += '  <p class="text-[11px] text-slate-500 font-normal mt-0.5">' + stage.name_kh + '</p>';

        html += '  <div class="mt-3 pt-2.5 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-600">';
        html += '    <span class="truncate max-w-[110px]" title="' + stage.responsible.name + '">' + stage.responsible.name.split(' ')[0] + ' (' + stage.responsible.role.split(' ')[0] + ')</span>';
        html += '    <span class="text-emerald-700 font-medium hover:underline">Details &rarr;</span>';
        html += '  </div>';
        html += '</div>';

        if (!isLast) {
          html += '<div class="hidden lg:flex items-center justify-center text-slate-300 px-1 shrink-0">';
          html += '  <span class="material-symbols-outlined text-[18px]">arrow_forward</span>';
          html += '</div>';
        }
      });

      container.innerHTML = html;
    },

    // ── 2. Completion Summary Cards ─────────────────────────────────────────
    renderSummaryKPIs: function () {
      var self = this;
      var d = self.data;
      if (!d) return;

      var elPct = document.getElementById('kpiProgressPct');
      var elPctBar = document.getElementById('kpiProgressBar');
      var elCompleted = document.getElementById('kpiCompletedTasks');
      var elOutstanding = document.getElementById('kpiOutstandingTasks');
      var elReview = document.getElementById('kpiAwaitingReview');

      if (elPct) elPct.textContent = d.overall_progress_pct + '%';
      if (elPctBar) elPctBar.style.width = Math.min(100, Math.max(0, d.overall_progress_pct)) + '%';
      if (elCompleted) elCompleted.textContent = d.completed_tasks_count;
      if (elOutstanding) elOutstanding.textContent = d.outstanding_tasks_count;
      if (elReview) elReview.textContent = d.awaiting_review_count;

      var elPeriodsDetail = document.getElementById('kpiPeriodsDetail');
      if (elPeriodsDetail) {
        elPeriodsDetail.textContent = d.metrics.total_placed + ' / ' + d.metrics.total_demand + ' lessons placed';
      }
    },

    // ── 3. Outstanding Work & Responsibility Table ──────────────────────────
    renderOutstandingTasks: function () {
      var self = this;
      var container = document.getElementById('outstandingTasksBody');
      if (!container || !self.data.outstanding_tasks) return;

      var tasks = self.data.outstanding_tasks;
      var filter = self.currentFilter;
      var gradeFilter = self.currentGradeFilter;
      var search = self.currentSearch.toLowerCase().trim();

      var filtered = tasks.filter(function (t) {
        // Tab filter
        if (filter !== 'all') {
          if (filter === 'needs_attention' && t.status !== 'Needs Attention') return false;
          if (filter === 'in_progress' && t.status !== 'In Progress') return false;
          if (filter === 'awaiting_review' && t.status !== 'Awaiting Review') return false;
          if (filter === 'completed' && t.status !== 'Completed') return false;
        }

        // Grade filter
        if (gradeFilter !== 'all' && t.grade !== gradeFilter) return false;

        // Search query
        if (search) {
          var matchStr = (t.task_name + ' ' + t.class_name + ' ' + t.responsible.name + ' ' + t.campus).toLowerCase();
          if (matchStr.indexOf(search) === -1) return false;
        }

        return true;
      });

      // Update badge count
      var badgeAll = document.getElementById('tabCountAll');
      var badgeNeeds = document.getElementById('tabCountNeeds');
      var badgeInProg = document.getElementById('tabCountInProg');
      var badgeRev = document.getElementById('tabCountRev');
      var badgeComp = document.getElementById('tabCountComp');

      if (badgeAll) badgeAll.textContent = tasks.length;
      if (badgeNeeds) badgeNeeds.textContent = tasks.filter(function (t) { return t.status === 'Needs Attention'; }).length;
      if (badgeInProg) badgeInProg.textContent = tasks.filter(function (t) { return t.status === 'In Progress'; }).length;
      if (badgeRev) badgeRev.textContent = tasks.filter(function (t) { return t.status === 'Awaiting Review'; }).length;
      if (badgeComp) badgeComp.textContent = tasks.filter(function (t) { return t.status === 'Completed'; }).length;

      if (filtered.length === 0) {
        container.innerHTML = '<div class="p-8 text-center text-slate-500 font-normal text-sm bg-white rounded-2xl border border-[#E1E9E3]"><span class="material-symbols-outlined text-3xl text-slate-400 mb-1">done_all</span><p>No outstanding tasks found matching your filter criteria.</p></div>';
        return;
      }

      var html = '';
      filtered.forEach(function (task) {
        var statusBadge = '';
        if (task.status === 'Completed') {
          statusBadge = '<span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200"><span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>Completed</span>';
        } else if (task.status === 'Needs Attention') {
          statusBadge = '<span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-amber-50 text-amber-700 border border-amber-200"><span class="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse"></span>Needs Attention</span>';
        } else if (task.status === 'In Progress') {
          statusBadge = '<span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-50 text-blue-700 border border-blue-200"><span class="w-1.5 h-1.5 rounded-full bg-blue-500"></span>In Progress</span>';
        } else {
          statusBadge = '<span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-50 text-purple-700 border border-purple-200"><span class="w-1.5 h-1.5 rounded-full bg-purple-500"></span>Awaiting Review</span>';
        }

        var progressPct = Math.round((task.assigned_periods / task.total_periods) * 100);

        html += '<div class="bg-white border border-[#E1E9E3] hover:border-slate-300 rounded-2xl p-4 transition shadow-sm space-y-3">';
        html += '  <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">';
        html += '    <div class="flex items-center gap-3">';
        html += '      <div class="w-10 h-10 rounded-xl bg-slate-100 border border-slate-200 flex items-center justify-center shrink-0 text-slate-700 font-medium text-sm">';
        html += task.class_name;
        html += '      </div>';
        html += '      <div>';
        html += '        <h4 class="text-sm font-medium text-slate-900 flex items-center gap-2">';
        html += '          <span>' + task.task_name + '</span>';
        html += '          <span class="text-[11px] px-2 py-0.5 rounded bg-slate-100 text-slate-600 font-normal">' + task.shift + ' · 6 Days</span>';
        html += '        </h4>';
        html += '        <p class="text-xs text-slate-500 font-normal mt-0.5">' + task.campus + ' · AY ' + task.academic_year + ' · Due: ' + task.due_date + '</p>';
        html += '      </div>';
        html += '    </div>';

        html += '    <div class="flex items-center gap-2 shrink-0 self-end sm:self-center">';
        html += statusBadge;
        html += '    </div>';
        html += '  </div>';

        // Details strip
        html += '  <div class="grid grid-cols-1 md:grid-cols-3 gap-3 pt-3 border-t border-slate-100 text-xs">';
        html += '    <div>';
        html += '      <span class="text-slate-400 block text-[11px] font-normal">Responsible Staff</span>';
        html += '      <span class="text-slate-700 font-medium flex items-center gap-1.5 mt-0.5">';
        html += '        <span class="material-symbols-outlined text-[15px] text-emerald-700">account_circle</span>' + task.responsible.name + ' (' + task.responsible.role + ')';
        html += '      </span>';
        html += '    </div>';

        html += '    <div>';
        html += '      <span class="text-slate-400 block text-[11px] font-normal">Scheduling Status</span>';
        html += '      <div class="flex items-center gap-2 mt-1">';
        html += '        <div class="flex-1 bg-slate-100 h-2 rounded-full overflow-hidden">';
        html += '          <div class="bg-emerald-600 h-full rounded-full transition-all" style="width:' + progressPct + '%"></div>';
        html += '        </div>';
        html += '        <span class="text-slate-600 font-medium shrink-0">' + task.assigned_periods + '/' + task.total_periods + '</span>';
        html += '      </div>';
        html += '      <span class="text-[11px] text-slate-500 font-normal">' + task.missing_requirements + '</span>';
        html += '    </div>';

        html += '    <div class="flex items-center justify-end gap-2 shrink-0 pt-1 md:pt-0">';
        html += '      <button type="button" onclick="TIMETABLE_OVERSIGHT.previewClass(\'' + task.class_id + '\')" class="px-2.5 py-1.5 rounded-xl border border-[#E1E9E3] hover:bg-slate-50 text-slate-700 text-xs font-medium transition flex items-center gap-1" title="View class schedule">';
        html += '        <span class="material-symbols-outlined text-[15px]">visibility</span><span>Preview</span>';
        html += '      </button>';

        if (task.status !== 'Completed') {
          html += '      <button type="button" onclick="TIMETABLE_OVERSIGHT.openReminderModal(\'' + task.id + '\')" class="px-3 py-1.5 rounded-xl bg-[#176B45] hover:bg-[#145939] text-white text-xs font-medium transition shadow-sm flex items-center gap-1.5">';
          html += '        <span class="material-symbols-outlined text-[15px]">send</span><span>Send Reminder</span>';
          html += '      </button>';
        } else {
          html += '      <span class="px-2.5 py-1 rounded-xl bg-slate-50 text-slate-400 text-xs font-normal">No Follow-up Required</span>';
        }
        html += '    </div>';
        html += '  </div>';

        html += '</div>';
      });

      container.innerHTML = html;
    },

    setFilter: function (filterName) {
      this.currentFilter = filterName;
      // Update tab styles
      var tabs = ['all', 'needs_attention', 'in_progress', 'awaiting_review', 'completed'];
      tabs.forEach(function (t) {
        var el = document.getElementById('tab_' + t);
        if (el) {
          if (t === filterName) {
            el.className = 'px-3 py-1.5 rounded-xl bg-[#176B45] text-white text-xs font-medium transition shadow-sm flex items-center gap-1.5';
          } else {
            el.className = 'px-3 py-1.5 rounded-xl text-slate-600 hover:bg-slate-100 text-xs font-medium transition flex items-center gap-1.5';
          }
        }
      });
      this.renderOutstandingTasks();
    },

    setGradeFilter: function (grade) {
      this.currentGradeFilter = grade;
      this.renderOutstandingTasks();
    },

    setSearch: function (val) {
      this.currentSearch = val;
      this.renderOutstandingTasks();
    },

    // ── 4. Read-Only Timetable Preview ──────────────────────────────────────
    previewClass: function (classId) {
      this.currentClassId = classId;
      var elSelect = document.getElementById('previewClassSelect');
      if (elSelect) elSelect.value = classId;

      var previewSec = document.getElementById('sectionTimetablePreview');
      if (previewSec) previewSec.scrollIntoView({ behavior: 'smooth' });

      this.renderTimetablePreview();
    },

    renderTimetablePreview: function () {
      var self = this;
      var container = document.getElementById('timetableGridPreview');
      if (!container || !self.data) return;

      var classId = self.currentClassId || 'class_7A';
      var state = self.data;
      var classTask = (self.data.outstanding_tasks || []).find(function (t) { return t.class_id === classId; }) || {
        class_name: classId.replace('class_', ''),
        shift: 'ព្រឹក',
        assigned_periods: 0,
        total_periods: 34,
        missing_requirements: 'Incomplete'
      };

      // Header summary for preview
      var elInfo = document.getElementById('previewClassInfo');
      if (elInfo) {
        var shiftLabel = classTask.shift === 'ព្រឹក' ? 'Morning Shift (07:00–11:30)' : 'Afternoon Shift (13:00–17:10)';
        var statColor = classTask.assigned_periods === classTask.total_periods ? 'text-emerald-700 bg-emerald-50 border-emerald-200' : 'text-amber-700 bg-amber-50 border-amber-200';
        elInfo.innerHTML = '<span class="text-slate-800 font-medium">Grade ' + classTask.class_name + '</span> · <span class="text-slate-500 font-normal">' + shiftLabel + '</span> · <span class="px-2 py-0.5 rounded text-[11px] font-medium border ' + statColor + '">' + classTask.assigned_periods + ' of ' + classTask.total_periods + ' Scheduled</span>';
      }

      // Fetch grid from authoritative API
      container.innerHTML = '<div class="py-12 text-center text-slate-400 font-normal text-sm"><span class="material-symbols-outlined text-2xl animate-spin mb-1">sync</span><p>Loading schedule grid for ' + classTask.class_name + '...</p></div>';

      fetch('/api/timetable/grid?class_id=' + classId)
        .then(function (r) { return r.json(); })
        .then(function (res) {
          if (!res.success) {
            container.innerHTML = '<div class="p-6 text-center text-red-500 font-normal text-sm">Failed to load grid.</div>';
            return;
          }
          self.renderGridHTML(res.grid || {}, classTask, res.state || {});
        })
        .catch(function (err) {
          console.error('Grid preview error:', err);
          container.innerHTML = '<div class="p-6 text-center text-slate-500 font-normal text-sm">Unable to fetch grid data: ' + err.message + '</div>';
        });
    },

    renderGridHTML: function (grid, classTask, rawState) {
      var container = document.getElementById('timetableGridPreview');
      if (!container) return;

      var days = ['ច័ន្ទ', 'អង្គារ', 'ពុធ', 'ព្រហស្បតិ៍', 'សុក្រ', 'សៅរ៍'];
      var dayNamesEn = { 'ច័ន្ទ': 'Mon', 'អង្គារ': 'Tue', 'ពុធ': 'Wed', 'ព្រហស្បតិ៍': 'Thu', 'សុក្រ': 'Fri', 'សៅរ៍': 'Sat' };
      var periods = [1, 2, 3, 4, 5];
      var shift = classTask.shift || 'ព្រឹក';
      var classId = classTask.class_id || this.currentClassId;

      var subjectsById = {};
      var teachersById = {};
      (rawState.subjects || []).forEach(function (s) { subjectsById[s.id] = s; });
      (rawState.teachers || []).forEach(function (t) { teachersById[t.id] = t; });

      var html = '<div class="overflow-x-auto"><table class="w-full text-xs text-left border-collapse">';
      html += '<thead><tr class="bg-slate-50 text-slate-600 border-b border-[#E1E9E3]">';
      html += '<th class="p-2.5 font-medium w-16 text-center">Period</th>';
      days.forEach(function (day) {
        html += '<th class="p-2.5 font-medium text-center border-l border-[#E1E9E3]">' + dayNamesEn[day] + '<br><span class="text-[10px] text-slate-400 font-normal">' + day + '</span></th>';
      });
      html += '</tr></thead><tbody>';

      periods.forEach(function (p) {
        html += '<tr class="border-b border-[#E1E9E3]/70 hover:bg-slate-50/50 transition">';
        html += '<td class="p-2.5 text-center font-medium text-slate-500 bg-slate-50/80">';
        html += '  <span class="block text-xs text-slate-800">P' + p + '</span>';
        html += '</td>';

        days.forEach(function (day) {
          var cellKey = day + '|' + shift + '|' + p + '|' + classId;
          var cell = grid[cellKey];

          html += '<td class="p-2 border-l border-[#E1E9E3]/70 align-top min-w-[130px] h-16">';

          if (cell) {
            var subj = subjectsById[cell.subject_id] || { name_kh: 'មុខវិជ្ជា', code: 'SUBJ', color: '#E2E8F0' };
            var tch = teachersById[cell.teacher_id] || { name_kh: 'គ្រូ', code: 'T' };

            html += '<div class="p-2 rounded-xl border border-[#E1E9E3] bg-white shadow-xs space-y-1">';
            html += '  <div class="flex items-center justify-between">';
            html += '    <span class="px-1.5 py-0.5 rounded text-[10px] font-medium" style="background-color:' + (cell.color || subj.color || '#E8F3ED') + '30; color:#176B45;">' + (cell.subject_code || subj.code) + '</span>';
            html += '    <span class="text-[10px] text-slate-400 font-mono">' + (cell.teacher_code || tch.code) + '</span>';
            html += '  </div>';
            html += '  <div class="font-medium text-slate-800 truncate text-[11px]" title="' + (cell.subject_name || subj.name_kh) + '">' + (cell.subject_name || subj.name_kh) + '</div>';
            html += '  <div class="text-[10px] text-slate-500 truncate flex items-center gap-1"><span class="material-symbols-outlined text-[12px] text-slate-400">person</span>' + (cell.teacher_name || tch.name_kh) + '</div>';
            html += '</div>';
          } else {
            html += '<div class="h-full min-h-[52px] rounded-xl border border-dashed border-slate-200 flex flex-col items-center justify-center text-slate-300 hover:border-amber-300 hover:bg-amber-50/30 transition p-1">';
            html += '  <span class="material-symbols-outlined text-[14px]">event_busy</span>';
            html += '  <span class="text-[10px] font-normal text-slate-400 mt-0.5">Unscheduled</span>';
            html += '</div>';
          }

          html += '</td>';
        });

        html += '</tr>';
      });

      html += '</tbody></table></div>';
      container.innerHTML = html;
    },

    // ── 5. Review Queue ─────────────────────────────────────────────────────
    renderReviewQueue: function () {
      var self = this;
      var container = document.getElementById('reviewQueueContainer');
      if (!container || !self.data) return;

      var queue = self.data.review_queue || [];
      if (queue.length === 0) {
        container.innerHTML = '<div class="p-6 text-center text-slate-400 text-xs font-normal border border-[#E1E9E3] rounded-2xl bg-white"><span class="material-symbols-outlined text-2xl text-slate-300 mb-1">inbox</span><p>No timetables currently awaiting approval.</p><p class="text-[11px] text-slate-400 mt-1">When the Principal completes scheduling for a cohort, it appears here for administrative verification.</p></div>';
        return;
      }

      var html = '';
      queue.forEach(function (item) {
        html += '<div class="p-3.5 bg-white border border-[#E1E9E3] rounded-2xl shadow-xs space-y-2">';
        html += '  <div class="flex items-center justify-between">';
        html += '    <h4 class="text-xs font-medium text-slate-900">Grade ' + item.class_name + ' Schedule</h4>';
        html += '    <span class="px-2 py-0.5 rounded-full text-[10px] font-medium bg-purple-50 text-purple-700 border border-purple-200">' + item.review_status + '</span>';
        html += '  </div>';
        html += '  <p class="text-[11px] text-slate-500 font-normal">Submitted by ' + item.submitted_by + ' · ' + item.submission_date + '</p>';
        html += '  <div class="flex items-center justify-between pt-1 border-t border-slate-100 text-[11px]">';
        html += '    <span class="text-slate-600 font-medium">' + item.periods_count + ' Lessons Scheduled</span>';
        html += '    <button onclick="TIMETABLE_OVERSIGHT.previewClass(\'' + item.class_id + '\')" class="text-emerald-700 font-medium hover:underline">Review &rarr;</button>';
        html += '  </div>';
        html += '</div>';
      });

      container.innerHTML = html;
    },

    // ── 6. Follow-up & Reminder History ──────────────────────────────────────
    renderReminderHistory: function () {
      var self = this;
      var container = document.getElementById('reminderHistoryContainer');
      if (!container) return;

      var reminders = self.reminders || [];
      if (reminders.length === 0) {
        container.innerHTML = '<div class="p-6 text-center text-slate-400 text-xs font-normal border border-[#E1E9E3] rounded-2xl bg-white"><span class="material-symbols-outlined text-2xl text-slate-300 mb-1">notifications_off</span><p>No follow-up reminders recorded yet.</p></div>';
        return;
      }

      var html = '<div class="space-y-2.5">';
      reminders.slice().reverse().forEach(function (rem) {
        var readStatus = rem.read
          ? '<span class="inline-flex items-center gap-1 text-[11px] font-medium text-emerald-700"><span class="material-symbols-outlined text-[13px]">done_all</span> Read (' + (rem.read_at ? rem.read_at.split(' ')[1] : 'Yes') + ')</span>'
          : '<span class="inline-flex items-center gap-1 text-[11px] font-medium text-amber-700"><span class="material-symbols-outlined text-[13px]">mail</span> Delivered (Unread)</span>';

        html += '<div class="p-3 bg-white border border-[#E1E9E3] rounded-2xl shadow-xs space-y-1.5">';
        html += '  <div class="flex items-center justify-between">';
        html += '    <span class="text-xs font-medium text-slate-800 truncate max-w-[200px]" title="' + rem.task_name + '">' + rem.task_name + '</span>';
        html += '    <span class="text-[10px] text-slate-400 font-normal">' + rem.created_at.split(' ')[0] + '</span>';
        html += '  </div>';
        html += '  <p class="text-[11px] text-slate-600 font-normal line-clamp-2">' + rem.message + '</p>';
        html += '  <div class="flex items-center justify-between pt-1 border-t border-slate-100 text-[11px]">';
        html += '    <span class="text-slate-500 font-normal">To: ' + rem.recipient_name + ' (' + rem.recipient_role + ')</span>';
        html += readStatus;
        html += '  </div>';
        html += '</div>';
      });
      html += '</div>';

      container.innerHTML = html;
    },

    // ── 7. Activity Timeline ────────────────────────────────────────────────
    renderActivityTimeline: function () {
      var self = this;
      var container = document.getElementById('activityTimelineContainer');
      if (!container || !self.data) return;

      var history = self.data.activity_history || [];
      if (history.length === 0) {
        container.innerHTML = '<div class="p-4 text-center text-slate-400 text-xs font-normal">No recent activities.</div>';
        return;
      }

      var html = '<div class="space-y-3 relative before:absolute before:inset-0 before:left-3.5 before:w-0.5 before:bg-slate-200">';
      history.slice(0, 6).forEach(function (act) {
        var icon = act.type === 'reminder' ? 'send' : 'history_toggle_off';
        var iconColor = act.type === 'reminder' ? 'text-amber-700 bg-amber-50 border-amber-200' : 'text-emerald-700 bg-emerald-50 border-emerald-200';

        html += '<div class="relative flex items-start gap-3 pl-1">';
        html += '  <div class="w-6 h-6 rounded-full border flex items-center justify-center shrink-0 ' + iconColor + ' z-10 bg-white">';
        html += '    <span class="material-symbols-outlined text-[13px]">' + icon + '</span>';
        html += '  </div>';
        html += '  <div class="flex-1 min-w-0">';
        html += '    <p class="text-xs font-medium text-slate-800">' + act.action + '</p>';
        html += '    <p class="text-[11px] text-slate-500 font-normal truncate">' + act.affected_record + ' · by ' + act.actor + '</p>';
        html += '    <span class="text-[10px] text-slate-400">' + act.timestamp + '</span>';
        html += '  </div>';
        html += '</div>';
      });
      html += '</div>';

      container.innerHTML = html;
    },

    // ── 8. Stage Detail Slide-over Drawer ────────────────────────────────────
    openStageDrawer: function (stepNumber) {
      var self = this;
      if (!self.data || !self.data.stages) return;

      var stage = self.data.stages.find(function (s) { return s.step === stepNumber; });
      if (!stage) return;

      self.currentStage = stage;
      var drawer = document.getElementById('stageDrawer');
      var backdrop = document.getElementById('stageDrawerBackdrop');
      var content = document.getElementById('stageDrawerContent');

      if (!drawer || !backdrop || !content) return;

      var statusBadgeClass = stage.status === 'Completed'
        ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
        : 'bg-amber-50 text-amber-700 border-amber-200';

      var checksHTML = '';
      (stage.checks || []).forEach(function (chk) {
        var icon = chk.ok ? 'check_circle' : 'pending';
        var iconColor = chk.ok ? 'text-emerald-600' : 'text-amber-500';

        checksHTML += '<div class="flex items-start gap-2.5 p-2.5 rounded-xl border border-slate-100 bg-slate-50/60">';
        checksHTML += '  <span class="material-symbols-outlined text-[18px] ' + iconColor + ' shrink-0 mt-0.5">' + icon + '</span>';
        checksHTML += '  <div class="flex-1 min-w-0 text-xs">';
        checksHTML += '    <span class="font-medium text-slate-800 block">' + chk.label + '</span>';
        checksHTML += '    <span class="text-slate-500 font-normal">' + chk.detail + '</span>';
        checksHTML += '  </div>';
        checksHTML += '</div>';
      });

      var html = '';
      html += '<div class="flex items-center justify-between pb-4 border-b border-[#E1E9E3]">';
      html += '  <div>';
      html += '    <div class="flex items-center gap-2">';
      html += '      <span class="px-2 py-0.5 rounded-lg bg-emerald-50 text-emerald-800 text-xs font-medium border border-emerald-200">Step 0' + stage.step + '</span>';
      html += '      <span class="px-2 py-0.5 rounded-full text-xs font-medium border ' + statusBadgeClass + '">' + stage.status + '</span>';
      html += '    </div>';
      html += '    <h3 class="text-base font-medium text-slate-900 mt-1">' + stage.name + '</h3>';
      html += '    <p class="text-xs text-slate-500 font-normal">' + stage.name_kh + '</p>';
      html += '  </div>';
      html += '  <button onclick="TIMETABLE_OVERSIGHT.closeDrawer()" class="p-2 rounded-xl text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition">';
      html += '    <span class="material-symbols-outlined text-[20px]">close</span>';
      html += '  </button>';
      html += '</div>';

      // Responsible Staff Card
      html += '<div class="my-4 p-3.5 rounded-2xl border border-[#E1E9E3] bg-slate-50/70 space-y-1.5">';
      html += '  <span class="text-[11px] font-normal text-slate-400 block">Responsible Staff Member</span>';
      html += '  <div class="flex items-center justify-between">';
      html += '    <div class="flex items-center gap-2.5">';
      html += '      <div class="w-9 h-9 rounded-xl bg-emerald-100/70 text-emerald-800 flex items-center justify-center font-medium text-sm">';
      html += stage.responsible.name.charAt(0);
      html += '      </div>';
      html += '      <div>';
      html += '        <h4 class="text-xs font-medium text-slate-800">' + stage.responsible.name + '</h4>';
      html += '        <p class="text-[11px] text-slate-500 font-normal">' + stage.responsible.role + ' · ' + stage.responsible.email + '</p>';
      html += '      </div>';
      html += '    </div>';
      if (stage.status !== 'Completed') {
        html += '    <button onclick="TIMETABLE_OVERSIGHT.openReminderModalFromStage(' + stage.step + ')" class="px-2.5 py-1.5 rounded-xl bg-[#176B45] text-white text-xs font-medium hover:bg-[#145939] transition flex items-center gap-1">';
        html += '      <span class="material-symbols-outlined text-[14px]">send</span><span>Remind</span>';
        html += '    </button>';
      }
      html += '  </div>';
      html += '</div>';

      // Checks & Criteria
      html += '<div class="space-y-2 mb-4">';
      html += '  <h4 class="text-xs font-medium text-slate-700">Verification Criteria & Real Database Evidence</h4>';
      html += checksHTML;
      html += '</div>';

      // Affected records section
      html += '<div class="space-y-2 pt-3 border-t border-slate-100">';
      html += '  <h4 class="text-xs font-medium text-slate-700">Stage Summary & System Impact</h4>';
      html += '  <p class="text-xs text-slate-600 font-normal leading-relaxed bg-white p-3 rounded-xl border border-slate-200">' + stage.summary + '</p>';
      html += '  <p class="text-[11px] text-slate-400 font-normal">Last updated: ' + stage.last_updated + '</p>';
      html += '</div>';

      content.innerHTML = html;

      // Show drawer
      backdrop.classList.remove('hidden');
      drawer.classList.remove('translate-x-full');
    },

    closeDrawer: function () {
      var drawer = document.getElementById('stageDrawer');
      var backdrop = document.getElementById('stageDrawerBackdrop');
      if (drawer) drawer.classList.add('translate-x-full');
      if (backdrop) backdrop.classList.add('hidden');
    },

    // ── 9. Send Reminder Modal ──────────────────────────────────────────────
    openReminderModal: function (taskId) {
      var self = this;
      var task = (self.data.outstanding_tasks || []).find(function (t) { return t.id === taskId; });
      if (!task) return;

      var modal = document.getElementById('reminderModal');
      if (!modal) return;

      document.getElementById('remindTaskId').value = task.id;
      document.getElementById('remindTaskName').value = task.task_name;
      document.getElementById('remindRecipientId').value = task.responsible.id || 'PRIN-2024-001';
      document.getElementById('remindRecipientName').value = task.responsible.name;
      document.getElementById('remindRecipientRole').value = task.responsible.role;
      document.getElementById('remindRecipientEmail').value = task.responsible.email;
      document.getElementById('remindMissingSummary').value = task.missing_requirements;
      document.getElementById('remindAuthorizedUrl').value = task.authorized_url;

      // Fill visual fields
      document.getElementById('modalTaskDisplay').textContent = task.task_name;
      document.getElementById('modalRecipientDisplay').textContent = task.responsible.name + ' (' + task.responsible.role + ')';
      document.getElementById('modalMissingDisplay').textContent = task.missing_requirements;
      document.getElementById('modalCampusDisplay').textContent = task.campus + ' · AY ' + task.academic_year;

      // Pre-fill message
      var defaultMsg = 'Dear ' + task.responsible.name + ',\nTimetable preparation for ' + task.class_name + ' requires your attention. ' + task.missing_requirements + '. Please review and complete the outstanding scheduling work.';
      document.getElementById('remindMessageText').value = defaultMsg;

      // Deadline (default 3 days)
      var d = new Date();
      d.setDate(d.getDate() + 3);
      document.getElementById('remindDeadlineInput').value = d.toISOString().split('T')[0];

      // Hide cooldown notice
      var warn = document.getElementById('remindCooldownWarning');
      if (warn) warn.classList.add('hidden');
      document.getElementById('remindForceDuplicate').value = 'false';

      modal.classList.remove('hidden');
    },

    openReminderModalFromStage: function (stepNumber) {
      var self = this;
      var stage = self.data.stages.find(function (s) { return s.step === stepNumber; });
      if (!stage) return;

      self.closeDrawer();
      var fakeTask = {
        id: 'stage_' + stage.id,
        task_name: 'Workflow Stage: ' + stage.name,
        campus: 'Tuol Kork Main Campus',
        academic_year: '2026–2027',
        responsible: stage.responsible,
        class_name: stage.name,
        missing_requirements: stage.summary,
        authorized_url: stage.step <= 3 ? 'pages/admin/admin-school-information.html' : 'pages/principal/principal-timetable-builder.html'
      };

      var modal = document.getElementById('reminderModal');
      if (!modal) return;

      document.getElementById('remindTaskId').value = fakeTask.id;
      document.getElementById('remindTaskName').value = fakeTask.task_name;
      document.getElementById('remindRecipientId').value = fakeTask.responsible.id || 'PRIN-2024-001';
      document.getElementById('remindRecipientName').value = fakeTask.responsible.name;
      document.getElementById('remindRecipientRole').value = fakeTask.responsible.role;
      document.getElementById('remindRecipientEmail').value = fakeTask.responsible.email;
      document.getElementById('remindMissingSummary').value = fakeTask.missing_requirements;
      document.getElementById('remindAuthorizedUrl').value = fakeTask.authorized_url;

      document.getElementById('modalTaskDisplay').textContent = fakeTask.task_name;
      document.getElementById('modalRecipientDisplay').textContent = fakeTask.responsible.name + ' (' + fakeTask.responsible.role + ')';
      document.getElementById('modalMissingDisplay').textContent = fakeTask.missing_requirements;
      document.getElementById('modalCampusDisplay').textContent = fakeTask.campus + ' · AY ' + fakeTask.academic_year;

      document.getElementById('remindMessageText').value = 'Dear ' + fakeTask.responsible.name + ',\nPlease review the requirements for ' + fakeTask.task_name + '. Outstanding tasks need attention before final timetable publication.';

      var d = new Date();
      d.setDate(d.getDate() + 3);
      document.getElementById('remindDeadlineInput').value = d.toISOString().split('T')[0];

      var warn = document.getElementById('remindCooldownWarning');
      if (warn) warn.classList.add('hidden');
      document.getElementById('remindForceDuplicate').value = 'false';

      modal.classList.remove('hidden');
    },

    closeModal: function () {
      var modal = document.getElementById('reminderModal');
      if (modal) modal.classList.add('hidden');
    },

    submitReminder: function () {
      var self = this;
      var taskId = document.getElementById('remindTaskId').value;
      var taskName = document.getElementById('remindTaskName').value;
      var recipientId = document.getElementById('remindRecipientId').value;
      var recipientName = document.getElementById('remindRecipientName').value;
      var recipientRole = document.getElementById('remindRecipientRole').value;
      var recipientEmail = document.getElementById('remindRecipientEmail').value;
      var missingSummary = document.getElementById('remindMissingSummary').value;
      var authorizedUrl = document.getElementById('remindAuthorizedUrl').value;
      var message = document.getElementById('remindMessageText').value.trim();
      var deadline = document.getElementById('remindDeadlineInput').value;
      var forceDuplicate = document.getElementById('remindForceDuplicate').value === 'true';

      if (!message) {
        self.showToast('Please enter a message for the reminder.', 'error');
        return;
      }

      var payload = {
        task_id: taskId,
        task_name: taskName,
        recipient_id: recipientId,
        recipient_name: recipientName,
        recipient_role: recipientRole,
        recipient_email: recipientEmail,
        missing_summary: missingSummary,
        authorized_url: authorizedUrl,
        message: message,
        deadline: deadline,
        force_duplicate: forceDuplicate
      };

      var btnSubmit = document.getElementById('btnSubmitReminder');
      if (btnSubmit) {
        btnSubmit.disabled = true;
        btnSubmit.innerHTML = '<span class="material-symbols-outlined text-[15px] animate-spin">sync</span><span>Sending...</span>';
      }

      fetch('/api/timetable/reminders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
        .then(function (res) { return res.json(); })
        .then(function (res) {
          if (btnSubmit) {
            btnSubmit.disabled = false;
            btnSubmit.innerHTML = '<span class="material-symbols-outlined text-[15px]">send</span><span>Send In-App Reminder</span>';
          }

          if (res.cooldown_warning) {
            var warn = document.getElementById('remindCooldownWarning');
            var warnMsg = document.getElementById('remindCooldownText');
            if (warn && warnMsg) {
              warnMsg.textContent = res.message;
              warn.classList.remove('hidden');
              document.getElementById('remindForceDuplicate').value = 'true';
            }
            return;
          }

          if (res.success) {
            self.showToast('Reminder successfully sent to ' + recipientName + '!', 'success');
            self.closeModal();
            self.fetchData(); // Refresh history
          } else {
            self.showToast(res.error || 'Failed to dispatch reminder.', 'error');
          }
        })
        .catch(function (err) {
          if (btnSubmit) {
            btnSubmit.disabled = false;
            btnSubmit.innerHTML = '<span class="material-symbols-outlined text-[15px]">send</span><span>Send In-App Reminder</span>';
          }
          console.error('Submit reminder error:', err);
          self.showToast('Network error dispatching reminder.', 'error');
        });
    },

    // ── 10. Toast Notification Helper ───────────────────────────────────────
    showToast: function (msg, type) {
      var toast = document.createElement('div');
      toast.className = 'fixed bottom-5 right-5 z-50 px-4 py-3 rounded-2xl shadow-lg border text-xs font-medium flex items-center gap-2 transform transition-all duration-300 ' +
        (type === 'error' ? 'bg-red-50 text-red-800 border-red-200' : 'bg-emerald-50 text-emerald-800 border-emerald-200');

      var icon = type === 'error' ? 'error' : 'check_circle';
      toast.innerHTML = '<span class="material-symbols-outlined text-[18px]">' + icon + '</span><span>' + msg + '</span>';
      document.body.appendChild(toast);

      setTimeout(function () {
        toast.style.opacity = '0';
        setTimeout(function () { if (toast.parentNode) toast.parentNode.removeChild(toast); }, 300);
      }, 4000);
    },

    refresh: function () {
      this.fetchData();
    }
  };

  window.TIMETABLE_OVERSIGHT = TIMETABLE_OVERSIGHT;

})(window, document);

