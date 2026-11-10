/**
 * NGIS SYSTEM — Admin Operations & IT Control Center Controller
 * Strictly font-medium and font-normal (NO BOLD FONTS)
 */

(function (window, document) {
  'use strict';

  var OPS_CONTROL = {
    data: null,
    currentFilterCategory: 'all',
    currentFilterSeverity: 'all',

    init: function () {
      var self = this;
      self.fetchData();
      self.bindEvents();
    },

    bindEvents: function () {
      var self = this;
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
          self.closeAuditModal();
          self.closeReminderModal();
        }
      });
    },

    fetchData: function () {
      var self = this;
      var btn = document.getElementById('btnOpsRefresh');
      if (btn) btn.classList.add('animate-spin');

      fetch('/api/admin/operations/status')
        .then(function (res) { return res.json(); })
        .then(function (res) {
          if (btn) btn.classList.remove('animate-spin');
          if (res.success) {
            self.data = res;
            self.renderAll();
          } else {
            console.error('Failed to load operations data:', res.error);
          }
        })
        .catch(function (err) {
          if (btn) btn.classList.remove('animate-spin');
          console.error('Ops fetch error:', err);
        });
    },

    renderAll: function () {
      var self = this;
      if (!self.data) return;

      self.renderKPIs();
      self.renderCards();
      self.renderWorkflowPipeline();
      self.renderIssues();
      self.renderStaffFollowups();
      self.renderSystemHealth();
      self.renderAuditTimeline();
    },

    // ── 1. Top Overview (5 Indicators) ──────────────────────────────────────
    renderKPIs: function () {
      var self = this;
      var s = self.data.summary || {};

      var elOp = document.getElementById('kpiOpsModules');
      var elInc = document.getElementById('kpiOpsIncomplete');
      var elMiss = document.getElementById('kpiOpsMissing');
      var elErr = document.getElementById('kpiOpsErrors');
      var elRev = document.getElementById('kpiOpsReviews');

      if (elOp) elOp.textContent = s.modules_operational || 0;
      if (elInc) elInc.textContent = s.workflows_incomplete || 0;
      if (elMiss) elMiss.textContent = s.records_missing || 0;
      if (elErr) elErr.textContent = s.errors_detected || 0;
      if (elRev) elRev.textContent = s.pending_reviews || 0;
    },

    // ── 2. Six Monitoring Cards (3x2 Grid) ───────────────────────────────────
    renderCards: function () {
      var self = this;
      var container = document.getElementById('opsMonitoringCardsContainer');
      if (!container || !self.data.cards) return;

      var html = '';
      self.data.cards.forEach(function (card) {
        var badgeClass = 'badge-ok';
        if (card.badge_type === 'warn') badgeClass = 'badge-warn';
        else if (card.badge_type === 'danger') badgeClass = 'badge-danger';
        else if (card.badge_type === 'info') badgeClass = 'badge-info';

        var onClickAttr = card.action_url
          ? 'onclick="window.location.href=\'' + card.action_url + '\'"'
          : 'onclick="OPS_CONTROL.openAuditModal(\'' + card.id + '\')"';

        html += '<div class="ops-card group" ' + onClickAttr + ' tabindex="0" role="button" aria-label="' + card.title + ' Monitoring">';
        
        // Card Top
        html += '  <div class="ops-card-top">';
        html += '    <div class="ops-card-icon">';
        html += '      <span class="material-symbols-outlined">' + card.icon + '</span>';
        html += '    </div>';
        html += '    <span class="ops-card-badge ' + badgeClass + '">' + card.badge + '</span>';
        html += '  </div>';

        // Card Body
        html += '  <div class="ops-card-body">';
        html += '    <h3 class="ops-card-title group-hover:text-emerald-800 transition">' + card.title + '</h3>';
        html += '    <p class="ops-card-desc">' + card.description + '</p>';
        html += '  </div>';

        // Card Footer
        html += '  <div class="ops-card-footer">';
        html += '    <span>' + card.action_label + '</span>';
        html += '    <span class="material-symbols-outlined text-[16px] group-hover:translate-x-0.5 transition">chevron_right</span>';
        html += '  </div>';

        html += '</div>';
      });

      container.innerHTML = html;
    },

    // ── 3. Connected Workflow Visualization ─────────────────────────────────
    renderWorkflowPipeline: function () {
      var self = this;
      var container = document.getElementById('opsWorkflowPipelineContainer');
      if (!container || !self.data.workflows) return;

      var html = '';
      var list = self.data.workflows;
      list.forEach(function (wf, idx) {
        var statusBadge = '';
        if (wf.status === 'Completed') {
          statusBadge = '<span class="inline-flex items-center gap-1 text-[11px] font-medium text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-full"><span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>Complete</span>';
        } else if (wf.status === 'Needs Attention') {
          statusBadge = '<span class="inline-flex items-center gap-1 text-[11px] font-medium text-amber-700 bg-amber-50 border border-amber-200 px-2 py-0.5 rounded-full"><span class="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse"></span>Needs Attention</span>';
        } else if (wf.status === 'In Progress') {
          statusBadge = '<span class="inline-flex items-center gap-1 text-[11px] font-medium text-blue-700 bg-blue-50 border border-blue-200 px-2 py-0.5 rounded-full"><span class="w-1.5 h-1.5 rounded-full bg-blue-500"></span>In Progress</span>';
        } else {
          statusBadge = '<span class="inline-flex items-center gap-1 text-[11px] font-medium text-slate-600 bg-slate-50 border border-slate-200 px-2 py-0.5 rounded-full"><span class="w-1.5 h-1.5 rounded-full bg-slate-400"></span>Pending</span>';
        }

        var isLast = idx === list.length - 1;

        html += '<div class="flex-1 min-w-[170px] bg-white border border-[#E1E9E3] rounded-2xl p-3.5 shadow-xs flex flex-col justify-between">';
        html += '  <div>';
        html += '    <div class="flex items-center justify-between mb-1.5">';
        html += '      <span class="text-[10px] font-medium text-slate-400">Step 0' + (idx + 1) + '</span>';
        html += statusBadge;
        html += '    </div>';
        html += '    <h4 class="text-xs font-medium text-slate-800">' + wf.name + '</h4>';
        html += '    <p class="text-[11px] text-slate-500 font-normal mt-1 leading-snug">' + wf.detail + '</p>';
        html += '  </div>';
        html += '  <div class="mt-2.5 pt-2 border-t border-slate-100 text-[10px] text-slate-400 font-normal truncate" title="' + wf.responsible + '">' + wf.responsible.split(' ')[0] + ' ' + (wf.responsible.split(' ')[1] || '') + '</div>';
        html += '</div>';

        if (!isLast) {
          html += '<div class="hidden xl:flex items-center text-slate-300 px-0.5 shrink-0">';
          html += '  <span class="material-symbols-outlined text-[16px]">arrow_forward</span>';
          html += '</div>';
        }
      });

      container.innerHTML = html;
    },

    // ── 4. System-Wide Issue Registry ───────────────────────────────────────
    renderIssues: function () {
      var self = this;
      var container = document.getElementById('opsIssuesTableBody');
      if (!container || !self.data.issues) return;

      var issues = self.data.issues;
      var cat = self.currentFilterCategory;
      var sev = self.currentFilterSeverity;

      var filtered = issues.filter(function (it) {
        if (cat !== 'all' && it.category !== cat) return false;
        if (sev !== 'all' && it.severity !== sev) return false;
        return true;
      });

      if (filtered.length === 0) {
        container.innerHTML = '<div class="p-6 text-center text-slate-400 text-xs font-normal">Zero issues found matching active filters.</div>';
        return;
      }

      var html = '<div class="space-y-2.5">';
      filtered.forEach(function (issue) {
        var sevBadge = '';
        if (issue.severity === 'Critical') {
          sevBadge = '<span class="px-2 py-0.5 rounded-full text-[10px] font-medium bg-red-50 text-red-700 border border-red-200">Critical</span>';
        } else if (issue.severity === 'High') {
          sevBadge = '<span class="px-2 py-0.5 rounded-full text-[10px] font-medium bg-amber-50 text-amber-700 border border-amber-200">High</span>';
        } else if (issue.severity === 'Medium') {
          sevBadge = '<span class="px-2 py-0.5 rounded-full text-[10px] font-medium bg-blue-50 text-blue-700 border border-blue-200">Medium</span>';
        } else {
          sevBadge = '<span class="px-2 py-0.5 rounded-full text-[10px] font-medium bg-slate-50 text-slate-600 border border-slate-200">Low</span>';
        }

        html += '<div class="p-3.5 bg-white border border-[#E1E9E3] hover:border-slate-300 rounded-2xl shadow-xs transition flex flex-col md:flex-row md:items-center justify-between gap-3">';
        html += '  <div class="flex items-start gap-3 min-w-0">';
        html += '    <div class="w-8 h-8 rounded-xl bg-slate-100 border border-slate-200 flex items-center justify-center shrink-0 text-slate-700">';
        html += '      <span class="material-symbols-outlined text-[16px]">report_problem</span>';
        html += '    </div>';
        html += '    <div class="min-w-0">';
        html += '      <div class="flex items-center gap-2 flex-wrap">';
        html += '        <span class="text-xs font-medium text-slate-900">' + issue.description + '</span>';
        html += '        <span class="text-[10px] px-2 py-0.5 rounded bg-slate-100 text-slate-600 font-normal">' + issue.module + '</span>';
        html += sevBadge;
        html += '      </div>';
        html += '      <p class="text-[11px] text-slate-500 font-normal mt-0.5">' + issue.campus + ' · Target: ' + issue.affected_record + ' · Owner: ' + issue.responsible + ' · Detected: ' + issue.first_detected + '</p>';
        html += '    </div>';
        html += '  </div>';

        html += '  <div class="flex items-center gap-2 shrink-0 self-end md:self-center">';
        html += '    <button type="button" onclick="OPS_CONTROL.openReminderModalFromIssue(\'' + issue.id + '\')" class="px-3 py-1.5 rounded-xl bg-[#176B45] hover:bg-[#145939] text-white text-xs font-medium transition shadow-xs flex items-center gap-1.5">';
        html += '      <span class="material-symbols-outlined text-[14px]">send</span><span>Remind Owner</span>';
        html += '    </button>';
        html += '  </div>';
        html += '</div>';
      });
      html += '</div>';

      container.innerHTML = html;
    },

    setIssueCategory: function (cat) {
      this.currentFilterCategory = cat;
      this.renderIssues();
    },

    setIssueSeverity: function (sev) {
      this.currentFilterSeverity = sev;
      this.renderIssues();
    },

    // ── 5. Staff Follow-Up ──────────────────────────────────────────────────
    renderStaffFollowups: function () {
      var self = this;
      var container = document.getElementById('opsStaffFollowupContainer');
      if (!container || !self.data.staff_followups) return;

      var html = '<div class="grid grid-cols-1 md:grid-cols-3 gap-3">';
      self.data.staff_followups.forEach(function (staff) {
        html += '<div class="bg-white border border-[#E1E9E3] rounded-2xl p-4 shadow-xs space-y-2.5">';
        html += '  <div class="flex items-center gap-2.5">';
        html += '    <div class="w-9 h-9 rounded-xl bg-emerald-50 text-emerald-800 border border-emerald-200/60 flex items-center justify-center font-medium text-xs shrink-0">';
        html += staff.name.split(' ')[0].charAt(0);
        html += '    </div>';
        html += '    <div class="min-w-0">';
        html += '      <h4 class="text-xs font-medium text-slate-800 truncate">' + staff.name + '</h4>';
        html += '      <p class="text-[11px] text-slate-500 font-normal truncate">' + staff.role + '</p>';
        html += '    </div>';
        html += '  </div>';

        html += '  <div class="pt-2 border-t border-slate-100 text-[11px] space-y-1">';
        html += '    <div class="text-slate-600 font-medium">' + staff.pending_tasks + '</div>';
        html += '    <div class="text-slate-400 font-normal flex items-center justify-between">';
        html += '      <span>Last reminder: ' + staff.last_reminder + '</span>';
        html += '      <span class="text-emerald-700 font-medium">' + staff.reminder_status + '</span>';
        html += '    </div>';
        html += '  </div>';

        html += '  <button type="button" onclick="OPS_CONTROL.openReminderModalDirect(\'' + staff.name + '\', \'' + staff.role + '\', \'' + staff.email + '\')" class="w-full mt-1 px-3 py-1.5 rounded-xl border border-[#E1E9E3] hover:bg-slate-50 text-slate-700 text-xs font-medium transition flex items-center justify-center gap-1.5">';
        html += '    <span class="material-symbols-outlined text-[14px]">send</span><span>Send Action Notice</span>';
        html += '  </button>';
        html += '</div>';
      });
      html += '</div>';

      container.innerHTML = html;
    },

    // ── 6. Technical System Health ──────────────────────────────────────────
    renderSystemHealth: function () {
      var self = this;
      var container = document.getElementById('opsSystemHealthContainer');
      if (!container || !self.data.system_health) return;

      var services = self.data.system_health.services || [];
      var html = '<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">';

      services.forEach(function (s) {
        var isOk = s.status === 'Operational';
        var badge = isOk
          ? '<span class="px-2 py-0.5 rounded-full text-[10px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">Operational</span>'
          : '<span class="px-2 py-0.5 rounded-full text-[10px] font-medium bg-red-50 text-red-700 border border-red-200">Incident</span>';

        html += '<div class="bg-white border border-[#E1E9E3] rounded-2xl p-3.5 shadow-xs space-y-2">';
        html += '  <div class="flex items-center justify-between">';
        html += '    <span class="text-xs font-medium text-slate-800">' + s.name + '</span>';
        html += badge;
        html += '  </div>';
        html += '  <p class="text-[11px] text-slate-500 font-normal">' + s.details + '</p>';
        html += '  <div class="flex items-center justify-between pt-1 border-t border-slate-100 text-[10px] text-slate-400 font-normal">';
        html += '    <span>Latency: ' + s.latency_ms + 'ms</span>';
        html += '    <span>Uptime: ' + s.uptime + '</span>';
        html += '  </div>';
        html += '</div>';
      });

      html += '</div>';
      container.innerHTML = html;
    },

    // ── 7. Audit Activity Timeline ──────────────────────────────────────────
    renderAuditTimeline: function () {
      var self = this;
      var container = document.getElementById('opsAuditTimelineContainer');
      if (!container || !self.data.audit_activity) return;

      var logs = self.data.audit_activity || [];
      var html = '<div class="space-y-2.5">';

      logs.forEach(function (log) {
        html += '<div class="flex items-center justify-between p-2.5 rounded-xl border border-slate-100 bg-slate-50/50 text-xs">';
        html += '  <div class="flex items-center gap-2 min-w-0">';
        html += '    <span class="material-symbols-outlined text-[16px] text-emerald-700 shrink-0">check_circle</span>';
        html += '    <div class="truncate">';
        html += '      <span class="font-medium text-slate-800">' + log.action + '</span>';
        html += '      <span class="text-slate-500 font-normal"> · ' + log.affected_record + ' (by ' + log.actor + ')</span>';
        html += '    </div>';
        html += '  </div>';
        html += '  <span class="text-[10px] text-slate-400 shrink-0 font-normal ml-2">' + log.timestamp + '</span>';
        html += '</div>';
      });

      html += '</div>';
      container.innerHTML = html;
    },

    // ── 8. Module Audit Modal (On Card Click) ───────────────────────────────
    openAuditModal: function (moduleId) {
      var self = this;
      var card = (self.data.cards || []).find(function (c) { return c.id === moduleId; });
      if (!card) return;

      var modal = document.getElementById('opsAuditModal');
      var title = document.getElementById('opsAuditModalTitle');
      var subtitle = document.getElementById('opsAuditModalSubtitle');
      var body = document.getElementById('opsAuditModalBody');

      if (!modal || !body) return;

      if (title) title.textContent = card.title + ' — Operational Audit';
      if (subtitle) subtitle.textContent = card.description;

      var items = card.audit_items || [];
      var html = '';

      if (moduleId === 'attendance') {
        html += '<div class="overflow-x-auto"><table class="w-full text-xs text-left border-collapse">';
        html += '<thead><tr class="bg-slate-50 text-slate-600 border-b border-[#E1E9E3]"><th class="p-2.5 font-medium">Class</th><th class="p-2.5 font-medium">Shift</th><th class="p-2.5 font-medium">Assigned Teacher</th><th class="p-2.5 font-medium">Submitted</th><th class="p-2.5 font-medium">Status</th><th class="p-2.5 font-medium text-right">Action</th></tr></thead>';
        html += '<tbody>';
        items.forEach(function (it) {
          var isMissing = it.status === 'Missing Submission';
          var statBadge = isMissing
            ? '<span class="px-2 py-0.5 rounded-full text-[10px] font-medium bg-amber-50 text-amber-700 border border-amber-200">Missing</span>'
            : '<span class="px-2 py-0.5 rounded-full text-[10px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">Submitted</span>';

          html += '<tr class="border-b border-slate-100">';
          html += '  <td class="p-2.5 font-medium text-slate-800">' + it.class + '</td>';
          html += '  <td class="p-2.5 text-slate-500 font-normal">' + it.shift + '</td>';
          html += '  <td class="p-2.5 text-slate-700 font-normal">' + it.teacher + '</td>';
          html += '  <td class="p-2.5 text-slate-500 font-normal">' + it.submitted + '/' + it.expected + '</td>';
          html += '  <td class="p-2.5">' + statBadge + '</td>';
          html += '  <td class="p-2.5 text-right">';
          if (isMissing) {
            html += '<button type="button" onclick="OPS_CONTROL.openReminderModalDirect(\'' + it.teacher + '\', \'Homeroom Teacher\', \'teacher@ngis.edu.kh\', \'Attendance for Class ' + it.class + '\')" class="px-2 py-1 rounded-lg bg-[#176B45] text-white text-[11px] font-medium hover:bg-[#145939]">Notify</button>';
          } else {
            html += '<span class="text-slate-400 text-[11px]">Verified</span>';
          }
          html += '  </td>';
          html += '</tr>';
        });
        html += '</tbody></table></div>';
      } else if (moduleId === 'grades') {
        html += '<div class="space-y-2">';
        items.forEach(function (it) {
          html += '<div class="p-3 rounded-xl border border-slate-200 bg-white flex items-center justify-between text-xs">';
          html += '  <div>';
          html += '    <h4 class="font-medium text-slate-800">' + it.cohort + ' — ' + it.subject + '</h4>';
          html += '    <p class="text-[11px] text-slate-500 font-normal">Educator: ' + it.teacher + ' · Deficiencies: ' + it.missing + ' entries missing</p>';
          html += '  </div>';
          html += '  <span class="px-2 py-0.5 rounded-full text-[10px] font-medium bg-slate-100 text-slate-700">' + it.status + '</span>';
          html += '</div>';
        });
        html += '</div>';
      } else if (moduleId === 'lessons') {
        html += '<div class="space-y-2">';
        items.forEach(function (it) {
          html += '<div class="p-3 rounded-xl border border-slate-200 bg-white flex items-center justify-between text-xs">';
          html += '  <div>';
          html += '    <h4 class="font-medium text-slate-800">' + it.title + '</h4>';
          html += '    <p class="text-[11px] text-slate-500 font-normal">' + it.subject + ' (' + it.class + ') · Teacher: ' + it.teacher + ' · File: ' + (it.file || 'None') + '</p>';
          html += '  </div>';
          html += '  <span class="px-2 py-0.5 rounded-full text-[10px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">' + it.status + '</span>';
          html += '</div>';
        });
        html += '</div>';
      } else if (moduleId === 'tasks') {
        html += '<div class="space-y-2">';
        items.forEach(function (it) {
          html += '<div class="p-3 rounded-xl border border-slate-200 bg-white flex items-center justify-between text-xs">';
          html += '  <div>';
          html += '    <h4 class="font-medium text-slate-800">' + it.title + '</h4>';
          html += '    <p class="text-[11px] text-slate-500 font-normal">' + it.class + ' · Due: ' + it.due + ' · Submissions: ' + it.submitted + ' received</p>';
          html += '  </div>';
          html += '  <span class="px-2 py-0.5 rounded-full text-[10px] font-medium bg-amber-50 text-amber-700 border border-amber-200">' + it.status + '</span>';
          html += '</div>';
        });
        html += '</div>';
      } else if (moduleId === 'exams') {
        html += '<div class="space-y-2">';
        items.forEach(function (it) {
          html += '<div class="p-3 rounded-xl border border-slate-200 bg-white flex items-center justify-between text-xs">';
          html += '  <div>';
          html += '    <h4 class="font-medium text-slate-800">' + it.name + '</h4>';
          html += '    <p class="text-[11px] text-slate-500 font-normal">' + it.department + ' Department · Date: ' + it.date + ' · Target: ' + it.classes + '</p>';
          html += '  </div>';
          html += '  <span class="px-2 py-0.5 rounded-full text-[10px] font-medium bg-slate-100 text-slate-700">' + it.status + '</span>';
          html += '</div>';
        });
        html += '</div>';
      }

      body.innerHTML = html;
      modal.classList.remove('hidden');
    },

    closeAuditModal: function () {
      var modal = document.getElementById('opsAuditModal');
      if (modal) modal.classList.add('hidden');
    },

    // ── 9. Send Reminder Modal ──────────────────────────────────────────────
    openReminderModalFromIssue: function (issueId) {
      var self = this;
      var issue = (self.data.issues || []).find(function (i) { return i.id === issueId; });
      if (!issue) return;

      self.openReminderModalDirect(issue.responsible, issue.module + ' Lead', 'staff@ngis.edu.kh', issue.description);
    },

    openReminderModalDirect: function (name, role, email, context) {
      var modal = document.getElementById('opsReminderModal');
      if (!modal) return;

      document.getElementById('opsRemindRecipientName').value = name;
      document.getElementById('opsRemindRecipientRole').value = role;
      document.getElementById('opsRemindRecipientEmail').value = email;
      document.getElementById('opsModalRecipientDisplay').textContent = name + ' (' + role + ')';
      document.getElementById('opsModalTaskDisplay').textContent = context || 'Academic Workflow Action Required';

      var defaultMsg = 'Dear ' + name + ',\nOperational monitoring indicates that ' + (context || 'an academic workflow') + ' requires your attention. Please review and complete the outstanding items.';
      document.getElementById('opsRemindMessageText').value = defaultMsg;

      var d = new Date();
      d.setDate(d.getDate() + 2);
      document.getElementById('opsRemindDeadlineInput').value = d.toISOString().split('T')[0];

      modal.classList.remove('hidden');
    },

    closeReminderModal: function () {
      var modal = document.getElementById('opsReminderModal');
      if (modal) modal.classList.add('hidden');
    },

    submitReminder: function () {
      var self = this;
      var recipientName = document.getElementById('opsRemindRecipientName').value;
      var recipientRole = document.getElementById('opsRemindRecipientRole').value;
      var recipientEmail = document.getElementById('opsRemindRecipientEmail').value;
      var taskName = document.getElementById('opsModalTaskDisplay').textContent;
      var message = document.getElementById('opsRemindMessageText').value.trim();
      var deadline = document.getElementById('opsRemindDeadlineInput').value;

      if (!message) {
        alert('Please enter a message for the reminder.');
        return;
      }

      var payload = {
        task_id: 'ops_' + Date.now(),
        task_name: taskName,
        recipient_id: 'PRIN-2024-001',
        recipient_name: recipientName,
        recipient_role: recipientRole,
        recipient_email: recipientEmail,
        missing_summary: taskName,
        authorized_url: 'pages/admin/admin.html',
        message: message,
        deadline: deadline,
        force_duplicate: true
      };

      var btn = document.getElementById('btnOpsSubmitReminder');
      if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<span class="material-symbols-outlined text-[15px] animate-spin">sync</span><span>Sending...</span>';
      }

      fetch('/api/admin/operations/reminders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
        .then(function (r) { return r.json(); })
        .then(function (res) {
          if (btn) {
            btn.disabled = false;
            btn.innerHTML = '<span class="material-symbols-outlined text-[15px]">send</span><span>Send In-App Reminder</span>';
          }
          if (res.success) {
            alert('Reminder delivered to ' + recipientName + ' successfully!');
            self.closeReminderModal();
            self.fetchData();
          } else {
            alert(res.error || 'Failed to dispatch reminder.');
          }
        })
        .catch(function (err) {
          if (btn) {
            btn.disabled = false;
            btn.innerHTML = '<span class="material-symbols-outlined text-[15px]">send</span><span>Send In-App Reminder</span>';
          }
          console.error('Reminder error:', err);
          alert('Network error dispatching reminder.');
        });
    },

    refresh: function () {
      this.fetchData();
    }
  };

  window.OPS_CONTROL = OPS_CONTROL;

})(window, document);

