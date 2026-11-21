/**
 * NGIS-SYSTEM — Academic Adjustment & Collaboration Engine
 * Manages Principal-to-Admin academic requests, multi-step proposal drawer,
 * Admin review workspace, lifecycle progression, and real-time portal synchronization.
 */

(function (window) {
  'use strict';

  var STORAGE_KEY = 'ngis_academic_adjustment_requests';
  var JSON_PATH = (window.location.pathname.indexOf('/pages/') !== -1 ? '../../' : '') + 'data/academic_adjustment_requests.json';

  var AcademicRequests = {
    _data: null,
    _initialized: false,

    /**
     * Initialize data from localStorage or fallback to JSON file
     */
    init: function () {
      var self = this;
      if (self._initialized && self._data) {
        return Promise.resolve(self._data);
      }

      var cached = null;
      try {
        var raw = localStorage.getItem(STORAGE_KEY);
        if (raw) cached = JSON.parse(raw);
      } catch (e) {
        console.warn('[AcademicRequests] LocalStorage read error:', e);
      }

      if (cached && Array.isArray(cached) && cached.length > 0) {
        self._data = cached;
        self._initialized = true;
        return Promise.resolve(self._data);
      }

      return fetch(JSON_PATH)
        .then(function (res) {
          if (!res.ok) throw new Error('HTTP ' + res.status);
          return res.json();
        })
        .then(function (json) {
          self._data = json || [];
          self._save();
          self._initialized = true;
          return self._data;
        })
        .catch(function (err) {
          console.warn('[AcademicRequests] Fetch fallback:', err);
          self._data = [];
          self._initialized = true;
          return self._data;
        });
    },

    _save: function () {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(this._data));
        window.dispatchEvent(new CustomEvent('ngis:academic-request-updated', { detail: { requests: this._data } }));
      } catch (e) {
        console.warn('[AcademicRequests] LocalStorage save error:', e);
      }
    },

    getAll: function () {
      return this._data || [];
    },

    getById: function (id) {
      if (!this._data) return null;
      for (var i = 0; i < this._data.length; i++) {
        if (this._data[i].id === id) return this._data[i];
      }
      return null;
    },

    getByModule: function (moduleName) {
      if (!this._data) return [];
      return this._data.filter(function (req) {
        return req.module === moduleName;
      });
    },

    getUnresolvedCount: function (moduleName) {
      var list = moduleName ? this.getByModule(moduleName) : this.getAll();
      return list.filter(function (r) {
        return r.status !== 'completed' && r.status !== 'declined' && r.status !== 'cancelled';
      }).length;
    },

    createRequest: function (req) {
      var nextNum = (this._data.length + 101);
      req.id = req.id || ('AR-2026-0' + nextNum);
      req.createdAt = new Date().toISOString();
      req.updatedAt = req.createdAt;
      req.status = req.status || 'submitted';
      req.timeline = req.timeline || [
        {
          status: 'submitted',
          by: req.requestingPrincipal || 'Dr. Ly Bunheng (Principal)',
          role: 'Principal',
          timestamp: req.createdAt,
          note: req.reason || 'Initial adjustment submission.'
        }
      ];

      this._data.unshift(req);
      this._save();

      // Trigger contextual notification
      this._triggerNotification({
        title: 'New Academic Request — ' + (req.moduleLabel || req.module),
        message: req.title + ' (Submitted by ' + req.requestingPrincipal + ')',
        link: req.module === 'timetable' ? 'admin-timetables.html?req=' + req.id :
              req.module === 'teacher_assignment' ? 'admin-teacher-class-assignment.html?req=' + req.id :
              'admin-subjects.html?req=' + req.id
      });

      return req;
    },

    updateRequestStatus: function (id, newStatus, adminNote, byUser) {
      var req = this.getById(id);
      if (!req) return null;

      var now = new Date().toISOString();
      req.status = newStatus;
      req.updatedAt = now;
      if (adminNote) req.adminResponse = adminNote;

      req.timeline = req.timeline || [];
      req.timeline.push({
        status: newStatus,
        by: byUser || 'Sok Panha Heng (Admin)',
        role: 'Admin',
        timestamp: now,
        note: adminNote || ('Status updated to ' + newStatus)
      });

      this._save();

      // Notify Principal of status progression
      var statusLabels = {
        under_review: 'is now Under Review by Administration',
        accepted: 'was Accepted by Administration',
        in_progress: 'is now In Progress / Operationalizing',
        needs_clarification: 'requires Principal Clarification',
        declined: 'was Declined with Administrative explanation',
        completed: 'has been Implemented & Published'
      };

      this._triggerNotification({
        title: 'Request Update: ' + req.id,
        message: req.title + ' — ' + (statusLabels[newStatus] || newStatus),
        link: 'pages/principal/principal-requests.html?id=' + req.id
      });

      return req;
    },

    _triggerNotification: function (notif) {
      try {
        var notifKey = 'ngis_notifications_feed';
        var list = [];
        var raw = localStorage.getItem(notifKey);
        if (raw) list = JSON.parse(raw);
        list.unshift({
          id: 'notif-' + Date.now(),
          title: notif.title,
          message: notif.message,
          link: notif.link,
          time: 'Just now',
          timestamp: new Date().toISOString(),
          unread: true
        });
        localStorage.setItem(notifKey, JSON.stringify(list.slice(0, 30)));
      } catch (e) {}
    },

    /* ════════════════════════════════════════════════════════════════════════
       UNIVERSAL 5-STEP ADJUSTMENT REQUEST DRAWER (FOR PRINCIPAL PORTAL)
       ════════════════════════════════════════════════════════════════════════ */
    openRequestDrawer: function (options) {
      options = options || {};
      var module = options.module || 'timetable'; // 'timetable', 'teacher_assignment', 'curriculum_subject'
      var record = options.affectedRecord || {};
      var prefill = options.prefill || {};

      var moduleTitles = {
        timetable: 'Timetable Schedule Adjustment',
        teacher_assignment: 'Teacher Workload & Class Reassignment',
        curriculum_subject: 'Curriculum & Subject Syllabus Adjustment'
      };

      // Remove existing drawer if any
      var existing = document.getElementById('academicUniversalDrawer');
      if (existing) existing.remove();

      var drawerEl = document.createElement('div');
      drawerEl.id = 'academicUniversalDrawer';
      drawerEl.className = 'fixed inset-0 z-50 overflow-hidden flex justify-end';
      drawerEl.setAttribute('role', 'dialog');
      drawerEl.setAttribute('aria-modal', 'true');

      drawerEl.innerHTML =
        '<div class="fixed inset-0 bg-slate-900/40 backdrop-blur-xs transition-opacity duration-200" id="audBackdrop"></div>' +
        '<div class="relative w-full max-w-2xl bg-white h-full shadow-2xl flex flex-col z-10 transform transition-transform duration-250 ease-out translate-x-full" id="audPanel">' +
          
          '<!-- Drawer Header -->' +
          '<div class="p-5 border-b border-[#E1E9E3] bg-[#F7F9F7] flex items-center justify-between shrink-0">' +
            '<div class="flex items-center gap-3">' +
              '<div class="w-10 h-10 rounded-xl bg-[#E8F3ED] text-[#176B45] flex items-center justify-center">' +
                '<span class="material-symbols-outlined text-xl">assignment_return</span>' +
              '</div>' +
              '<div>' +
                '<h2 class="text-base font-medium text-slate-900 leading-tight">Request Academic Adjustment</h2>' +
                '<p class="text-xs text-slate-500 font-normal mt-0.5">' + (moduleTitles[module] || 'Academic Collaboration') + ' · Sensok Campus</p>' +
              '</div>' +
            '</div>' +
            '<button type="button" id="audCloseBtn" class="w-8 h-8 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-200/60 flex items-center justify-center transition cursor-pointer" aria-label="Close drawer">' +
              '<span class="material-symbols-outlined text-lg">close</span>' +
            '</button>' +
          '</div>' +

          '<!-- 5-Step Stepper -->' +
          '<div class="px-6 py-3 border-b border-[#E1E9E3] bg-white shrink-0">' +
            '<div class="flex items-center justify-between relative">' +
              '<div class="absolute left-0 top-1/2 -translate-y-1/2 w-full h-0.5 bg-slate-200 -z-0"></div>' +
              '<div class="step-pip z-10 flex flex-col items-center gap-1 active" data-step="1">' +
                '<div class="w-6 h-6 rounded-full bg-[#176B45] text-white text-xs font-medium flex items-center justify-center">1</div>' +
                '<span class="text-[10px] font-medium text-[#176B45]">Identify</span>' +
              '</div>' +
              '<div class="step-pip z-10 flex flex-col items-center gap-1" data-step="2">' +
                '<div class="w-6 h-6 rounded-full bg-slate-200 text-slate-600 text-xs font-medium flex items-center justify-center">2</div>' +
                '<span class="text-[10px] text-slate-500">Propose</span>' +
              '</div>' +
              '<div class="step-pip z-10 flex flex-col items-center gap-1" data-step="3">' +
                '<div class="w-6 h-6 rounded-full bg-slate-200 text-slate-600 text-xs font-medium flex items-center justify-center">3</div>' +
                '<span class="text-[10px] text-slate-500">Explain</span>' +
              '</div>' +
              '<div class="step-pip z-10 flex flex-col items-center gap-1" data-step="4">' +
                '<div class="w-6 h-6 rounded-full bg-slate-200 text-slate-600 text-xs font-medium flex items-center justify-center">4</div>' +
                '<span class="text-[10px] text-slate-500">Review</span>' +
              '</div>' +
              '<div class="step-pip z-10 flex flex-col items-center gap-1" data-step="5">' +
                '<div class="w-6 h-6 rounded-full bg-slate-200 text-slate-600 text-xs font-medium flex items-center justify-center">5</div>' +
                '<span class="text-[10px] text-slate-500">Submit</span>' +
              '</div>' +
            '</div>' +
          '</div>' +

          '<!-- Drawer Scrollable Body -->' +
          '<div class="p-6 overflow-y-auto flex-1 space-y-5" id="audBodyContainer">' +
            '<!-- Dynamic step content injected here -->' +
          '</div>' +

          '<!-- Drawer Footer Controls -->' +
          '<div class="p-4 border-t border-[#E1E9E3] bg-[#F7F9F7] flex items-center justify-between shrink-0">' +
            '<button type="button" id="audPrevBtn" class="px-4 py-2 text-xs font-medium text-slate-700 bg-white border border-[#E1E9E3] rounded-xl hover:bg-slate-50 transition cursor-pointer disabled:opacity-40 disabled:pointer-events-none">' +
              'Back' +
            '</button>' +
            '<div class="flex items-center gap-2">' +
              '<button type="button" id="audCancelBtn" class="px-3 py-2 text-xs font-medium text-slate-500 hover:text-slate-700 transition cursor-pointer">' +
                'Cancel' +
              '</button>' +
              '<button type="button" id="audNextBtn" class="px-5 py-2 text-xs font-medium text-white bg-[#176B45] hover:bg-[#125536] rounded-xl transition shadow-xs cursor-pointer">' +
                'Next Step' +
              '</button>' +
            '</div>' +
          '</div>' +

        '</div>';

      document.body.appendChild(drawerEl);

      // Animate in
      requestAnimationFrame(function () {
        document.getElementById('audPanel').classList.remove('translate-x-full');
      });

      // Wizard State
      var currentStep = 1;
      var wizardData = {
        module: module,
        moduleLabel: module === 'timetable' ? 'Timetable Matrix' : module === 'teacher_assignment' ? 'Teacher Assignments' : 'Curriculum Subjects',
        affectedRecordId: record.id || record.classId || 'REC-' + Date.now(),
        campus: 'Sensok Campus',
        department: record.department || 'Academic Department',
        requestingPrincipal: 'Dr. Ly Bunheng (Principal)',
        currentSnapshot: record,
        proposedChanges: {},
        title: prefill.title || '',
        reason: prefill.reason || '',
        priority: prefill.priority || 'high',
        requestedDeadline: prefill.requestedDeadline || '2026-11-28'
      };

      function renderStep(step) {
        currentStep = step;
        var container = document.getElementById('audBodyContainer');
        var prevBtn = document.getElementById('audPrevBtn');
        var nextBtn = document.getElementById('audNextBtn');

        // Update pip styling
        document.querySelectorAll('.step-pip').forEach(function (pip) {
          var s = parseInt(pip.getAttribute('data-step'), 10);
          var bubble = pip.querySelector('div');
          var text = pip.querySelector('span');
          if (s === step) {
            bubble.className = 'w-6 h-6 rounded-full bg-[#176B45] text-white text-xs font-medium flex items-center justify-center';
            text.className = 'text-[10px] font-medium text-[#176B45]';
          } else if (s < step) {
            bubble.className = 'w-6 h-6 rounded-full bg-emerald-100 text-[#176B45] text-xs font-medium flex items-center justify-center';
            text.className = 'text-[10px] text-slate-500';
          } else {
            bubble.className = 'w-6 h-6 rounded-full bg-slate-200 text-slate-600 text-xs font-medium flex items-center justify-center';
            text.className = 'text-[10px] text-slate-500';
          }
        });

        prevBtn.disabled = (step === 1);
        nextBtn.textContent = (step === 5 ? 'Confirm & Send to Admin' : 'Next Step');

        if (step === 1) {
          // STEP 1: IDENTIFY
          var recHtml = '';
          if (module === 'timetable') {
            recHtml =
              '<div class="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-2 text-xs text-slate-700">' +
                '<div class="flex justify-between py-1 border-b border-slate-200"><span class="text-slate-400">Class:</span><span class="font-medium">' + (record.className || 'Grade 10A') + '</span></div>' +
                '<div class="flex justify-between py-1 border-b border-slate-200"><span class="text-slate-400">Subject:</span><span class="font-medium">' + (record.subject || 'Chemistry') + '</span></div>' +
                '<div class="flex justify-between py-1 border-b border-slate-200"><span class="text-slate-400">Assigned Teacher:</span><span class="font-medium">' + (record.teacherName || 'Ms. Kiry Sokha') + '</span></div>' +
                '<div class="flex justify-between py-1 border-b border-slate-200"><span class="text-slate-400">Current Slot:</span><span class="font-medium">' + (record.day || 'Monday') + ' · Period ' + (record.period || 2) + ' (' + (record.time || '08:45 AM - 09:30 AM') + ')</span></div>' +
                '<div class="flex justify-between py-1"><span class="text-slate-400">Room:</span><span class="font-medium">' + (record.room || 'Lab 201') + '</span></div>' +
              '</div>';
          } else if (module === 'teacher_assignment') {
            recHtml =
              '<div class="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-2 text-xs text-slate-700">' +
                '<div class="flex justify-between py-1 border-b border-slate-200"><span class="text-slate-400">Teacher:</span><span class="font-medium">' + (record.teacherName || 'Dr. Sarah Jenkins') + '</span></div>' +
                '<div class="flex justify-between py-1 border-b border-slate-200"><span class="text-slate-400">Department:</span><span class="font-medium">' + (record.department || 'Mathematics') + '</span></div>' +
                '<div class="flex justify-between py-1 border-b border-slate-200"><span class="text-slate-400">Assigned Class:</span><span class="font-medium">' + (record.className || 'Grade 11B') + '</span></div>' +
                '<div class="flex justify-between py-1 border-b border-slate-200"><span class="text-slate-400">Assigned Subject:</span><span class="font-medium">' + (record.subjectName || 'Calculus I') + '</span></div>' +
                '<div class="flex justify-between py-1"><span class="text-slate-400">Weekly Workload:</span><span class="font-medium text-amber-600">' + (record.periodsPerWeek || 6) + ' periods (Total load: 28 periods/wk)</span></div>' +
              '</div>';
          } else {
            recHtml =
              '<div class="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-2 text-xs text-slate-700">' +
                '<div class="flex justify-between py-1 border-b border-slate-200"><span class="text-slate-400">Subject Name:</span><span class="font-medium">' + (record.name || record.subjectName || 'Applied AI & Digital Ethics') + '</span></div>' +
                '<div class="flex justify-between py-1 border-b border-slate-200"><span class="text-slate-400">Subject Code:</span><span class="font-medium">' + (record.code || record.subjectCode || 'CS-1202') + '</span></div>' +
                '<div class="flex justify-between py-1 border-b border-slate-200"><span class="text-slate-400">Department:</span><span class="font-medium">' + (record.department || 'Computer Science & IT') + '</span></div>' +
                '<div class="flex justify-between py-1 border-b border-slate-200"><span class="text-slate-400">Current Periods:</span><span class="font-medium">' + (record.periods || 2) + ' periods / week</span></div>' +
                '<div class="flex justify-between py-1"><span class="text-slate-400">Target Cohort:</span><span class="font-medium">' + (record.grade || 'Grade 12') + '</span></div>' +
              '</div>';
          }

          container.innerHTML =
            '<div>' +
              '<h3 class="text-sm font-medium text-slate-900">Step 1: Identify Academic Record</h3>' +
              '<p class="text-xs text-slate-500 font-normal mt-0.5 mb-4">Confirm the exact academic record and current parameters requiring adjustment.</p>' +
              recHtml +
              '<div class="mt-4 p-3 rounded-xl bg-emerald-50/70 border border-emerald-200/60 text-xs text-emerald-800 flex items-start gap-2.5">' +
                '<span class="material-symbols-outlined text-[18px] text-[#176B45] shrink-0 mt-0.5">verified_user</span>' +
                '<span>Academic records are synchronized with the 2025–26 official published master schedule. Proposing an adjustment preserves the active schedule until Admin validation.</span>' +
              '</div>' +
            '</div>';
        } else if (step === 2) {
          // STEP 2: PROPOSE
          var formHtml = '';
          if (module === 'timetable') {
            formHtml =
              '<div class="space-y-4">' +
                '<div>' +
                  '<label class="block text-xs font-medium text-slate-700 mb-1">Target Day</label>' +
                  '<select id="propDay" class="w-full text-xs px-3 py-2 border border-slate-200 rounded-xl bg-white text-slate-800">' +
                    '<option value="Monday">Monday</option>' +
                    '<option value="Tuesday">Tuesday</option>' +
                    '<option value="Wednesday" selected>Wednesday</option>' +
                    '<option value="Thursday">Thursday</option>' +
                    '<option value="Friday">Friday</option>' +
                  '</select>' +
                '</div>' +
                '<div>' +
                  '<label class="block text-xs font-medium text-slate-700 mb-1">Target Period Slot</label>' +
                  '<select id="propPeriod" class="w-full text-xs px-3 py-2 border border-slate-200 rounded-xl bg-white text-slate-800">' +
                    '<option value="1">Period 1 (08:00 AM - 08:45 AM)</option>' +
                    '<option value="2">Period 2 (08:45 AM - 09:30 AM)</option>' +
                    '<option value="3">Period 3 (09:45 AM - 10:30 AM)</option>' +
                    '<option value="4" selected>Period 4 (10:30 AM - 11:15 AM)</option>' +
                    '<option value="5">Period 5 (01:00 PM - 01:45 PM)</option>' +
                    '<option value="6">Period 6 (01:45 PM - 02:30 PM)</option>' +
                  '</select>' +
                '</div>' +
                '<div>' +
                  '<label class="block text-xs font-medium text-slate-700 mb-1">Proposed Classroom / Lab</label>' +
                  '<input type="text" id="propRoom" value="' + (record.room || 'Lab 201') + '" class="w-full text-xs px-3 py-2 border border-slate-200 rounded-xl bg-white text-slate-800" placeholder="e.g. Science Lab 102">' +
                '</div>' +
              '</div>';
          } else if (module === 'teacher_assignment') {
            formHtml =
              '<div class="space-y-4">' +
                '<div>' +
                  '<label class="block text-xs font-medium text-slate-700 mb-1">Action Type</label>' +
                  '<select id="propActionType" class="w-full text-xs px-3 py-2 border border-slate-200 rounded-xl bg-white text-slate-800">' +
                    '<option value="reassign_faculty" selected>Reassign to Different Teacher</option>' +
                    '<option value="reduce_workload">Reduce Teaching Periods</option>' +
                    '<option value="add_co_teacher">Assign Co-Instructor</option>' +
                  '</select>' +
                '</div>' +
                '<div>' +
                  '<label class="block text-xs font-medium text-slate-700 mb-1">Proposed Replacement Faculty</label>' +
                  '<select id="propTeacher" class="w-full text-xs px-3 py-2 border border-slate-200 rounded-xl bg-white text-slate-800">' +
                    '<option value="Mr. Chan Dara (TCH-2024-088)">Mr. Chan Dara (Mathematics · 16 periods/wk)</option>' +
                    '<option value="Ms. Vanna Chea (TCH-2024-055)">Ms. Vanna Chea (Mathematics · 18 periods/wk)</option>' +
                    '<option value="Coach Samreth Bora (TCH-2024-082)">Coach Samreth Bora (Mathematics · 14 periods/wk)</option>' +
                  '</select>' +
                '</div>' +
              '</div>';
          } else {
            formHtml =
              '<div class="space-y-4">' +
                '<div>' +
                  '<label class="block text-xs font-medium text-slate-700 mb-1">Proposed Weekly Teaching Hours</label>' +
                  '<input type="number" id="propPeriodsNum" value="4" min="1" max="10" class="w-full text-xs px-3 py-2 border border-slate-200 rounded-xl bg-white text-slate-800">' +
                '</div>' +
                '<div>' +
                  '<label class="block text-xs font-medium text-slate-700 mb-1">Curriculum Framework Requirement</label>' +
                  '<input type="text" id="propFramework" value="National STEM MoEYS 2026 Core" class="w-full text-xs px-3 py-2 border border-slate-200 rounded-xl bg-white text-slate-800">' +
                '</div>' +
              '</div>';
          }

          container.innerHTML =
            '<div>' +
              '<h3 class="text-sm font-medium text-slate-900">Step 2: Propose Desired Changes</h3>' +
              '<p class="text-xs text-slate-500 font-normal mt-0.5 mb-4">Define the proposed operational parameters. Administrators will inspect these during review.</p>' +
              formHtml +
            '</div>';
        } else if (step === 3) {
          // STEP 3: EXPLAIN
          container.innerHTML =
            '<div class="space-y-4">' +
              '<div>' +
                '<h3 class="text-sm font-medium text-slate-900">Step 3: Justification & Urgency</h3>' +
                '<p class="text-xs text-slate-500 font-normal mt-0.5 mb-4">Provide academic context, department reasoning, and preferred completion timeline.</p>' +
              '</div>' +
              '<div>' +
                '<label class="block text-xs font-medium text-slate-700 mb-1">Request Title</label>' +
                '<input type="text" id="audTitleInput" value="' + (wizardData.title || ('Adjust ' + (record.className || record.subjectName || 'Schedule'))) + '" class="w-full text-xs px-3 py-2 border border-slate-200 rounded-xl bg-white text-slate-800" placeholder="Concise title for admin review">' +
              '</div>' +
              '<div class="grid grid-cols-2 gap-3">' +
                '<div>' +
                  '<label class="block text-xs font-medium text-slate-700 mb-1">Priority Level</label>' +
                  '<select id="audPrioritySelect" class="w-full text-xs px-3 py-2 border border-slate-200 rounded-xl bg-white text-slate-800">' +
                    '<option value="urgent" ' + (wizardData.priority === 'urgent' ? 'selected' : '') + '>Urgent (Within 24h)</option>' +
                    '<option value="high" ' + (wizardData.priority === 'high' ? 'selected' : '') + '>High (Within 3 days)</option>' +
                    '<option value="medium" ' + (wizardData.priority === 'medium' ? 'selected' : '') + '>Medium (Weekly Cycle)</option>' +
                    '<option value="low" ' + (wizardData.priority === 'low' ? 'selected' : '') + '>Low (Next Term Prep)</option>' +
                  '</select>' +
                '</div>' +
                '<div>' +
                  '<label class="block text-xs font-medium text-slate-700 mb-1">Requested Implementation Date</label>' +
                  '<input type="date" id="audDeadlineInput" value="' + (wizardData.requestedDeadline || '2026-11-28') + '" class="w-full text-xs px-3 py-2 border border-slate-200 rounded-xl bg-white text-slate-800">' +
                '</div>' +
              '</div>' +
              '<div>' +
                '<label class="block text-xs font-medium text-slate-700 mb-1">Academic Rationale / Context</label>' +
                '<textarea id="audReasonInput" rows="4" class="w-full text-xs p-3 border border-slate-200 rounded-xl bg-white text-slate-800" placeholder="Describe pedagogical reasons, room constraints, student accessibility needs, or teacher workload balancing...">' + (wizardData.reason || '') + '</textarea>' +
              '</div>' +
            '</div>';
        } else if (step === 4) {
          // STEP 4: REVIEW (SIDE-BY-SIDE BEFORE & AFTER)
          container.innerHTML =
            '<div>' +
              '<h3 class="text-sm font-medium text-slate-900">Step 4: Review Before &amp; After Comparison</h3>' +
              '<p class="text-xs text-slate-500 font-normal mt-0.5 mb-4">Validate that the proposed adjustments are accurate and resolve the identified issue.</p>' +
              '<div class="grid grid-cols-2 gap-3">' +
                '<div class="p-4 bg-slate-50 rounded-xl border border-slate-200">' +
                  '<div class="text-[11px] font-medium text-slate-400 uppercase tracking-wider mb-2">Current Active State</div>' +
                  '<div class="text-xs text-slate-700 space-y-1.5">' +
                    '<div><span class="text-slate-400">Target:</span> ' + (record.className || record.teacherName || record.subjectName || 'Grade 10A') + '</div>' +
                    '<div><span class="text-slate-400">Slot:</span> ' + (record.day || 'Monday') + ' P' + (record.period || '2') + '</div>' +
                    '<div><span class="text-slate-400">Room:</span> ' + (record.room || 'Lab 201') + '</div>' +
                    '<div><span class="text-slate-400">Status:</span> <span class="px-2 py-0.5 rounded-full text-[10px] bg-slate-200 text-slate-700">Live Active</span></div>' +
                  '</div>' +
                '</div>' +
                '<div class="p-4 bg-emerald-50/50 rounded-xl border border-emerald-200">' +
                  '<div class="text-[11px] font-medium text-[#176B45] uppercase tracking-wider mb-2">Proposed Adjustment</div>' +
                  '<div class="text-xs text-slate-800 space-y-1.5">' +
                    '<div><span class="text-slate-500">Target:</span> ' + (record.className || record.teacherName || record.subjectName || 'Grade 10A') + '</div>' +
                    '<div><span class="text-slate-500">Slot:</span> ' + (wizardData.proposedChanges.day || 'Wednesday') + ' P' + (wizardData.proposedChanges.period || '4') + '</div>' +
                    '<div><span class="text-slate-500">Room:</span> ' + (wizardData.proposedChanges.room || 'Lab 201') + '</div>' +
                    '<div><span class="text-slate-500">Impact:</span> <span class="px-2 py-0.5 rounded-full text-[10px] bg-emerald-100 text-emerald-800 font-medium">Conflict Free</span></div>' +
                  '</div>' +
                '</div>' +
              '</div>' +
              '<div class="mt-4 p-3.5 bg-slate-50 rounded-xl border border-slate-200 text-xs text-slate-600">' +
                '<div class="font-medium text-slate-800 mb-1">Submission Summary</div>' +
                '<div>' + (wizardData.title || 'Academic Schedule Adjustment') + '</div>' +
                '<div class="text-slate-500 mt-1 italic">"' + (wizardData.reason || 'Requested by Principal for operational balance.') + '"</div>' +
              '</div>' +
            '</div>';
        } else if (step === 5) {
          // STEP 5: SUBMIT & DISPATCH
          container.innerHTML =
            '<div class="text-center py-6 space-y-4">' +
              '<div class="w-14 h-14 rounded-2xl bg-emerald-100 text-[#176B45] flex items-center justify-center mx-auto">' +
                '<span class="material-symbols-outlined text-3xl">send</span>' +
              '</div>' +
              '<div>' +
                '<h3 class="text-base font-medium text-slate-900">Ready to Submit to Administration</h3>' +
                '<p class="text-xs text-slate-500 font-normal max-w-md mx-auto mt-1">This request will be sent directly to authorized Administrators responsible for Sensok Campus and the Science Department. You can track progress in the Adjustment Requests workspace.</p>' +
              '</div>' +
              '<div class="p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs text-slate-600 max-w-sm mx-auto text-left">' +
                '<div class="flex justify-between py-0.5"><span class="text-slate-400">Recipient:</span><span class="font-medium text-slate-800">Sok Panha Heng (Admin)</span></div>' +
                '<div class="flex justify-between py-0.5"><span class="text-slate-400">Campus:</span><span class="font-medium text-slate-800">Sensok Campus</span></div>' +
                '<div class="flex justify-between py-0.5"><span class="text-slate-400">Priority:</span><span class="font-medium text-red-600 uppercase text-[10px]">' + (wizardData.priority || 'High') + '</span></div>' +
              '</div>' +
            '</div>';
        }
      }

      // Initial render step 1
      renderStep(1);

      // Event handlers
      function collectCurrentStepData() {
        if (currentStep === 2) {
          if (module === 'timetable') {
            var d = document.getElementById('propDay');
            var p = document.getElementById('propPeriod');
            var r = document.getElementById('propRoom');
            wizardData.proposedChanges = {
              day: d ? d.value : 'Wednesday',
              period: p ? parseInt(p.value, 10) : 4,
              room: r ? r.value : 'Lab 201'
            };
          } else if (module === 'teacher_assignment') {
            var t = document.getElementById('propTeacher');
            wizardData.proposedChanges = {
              replacementTeacher: t ? t.value : 'Mr. Chan Dara'
            };
          } else {
            var pn = document.getElementById('propPeriodsNum');
            wizardData.proposedChanges = {
              periodsPerWeek: pn ? parseInt(pn.value, 10) : 4
            };
          }
        } else if (currentStep === 3) {
          var titleIn = document.getElementById('audTitleInput');
          var prioIn = document.getElementById('audPrioritySelect');
          var deadIn = document.getElementById('audDeadlineInput');
          var reasIn = document.getElementById('audReasonInput');
          if (titleIn) wizardData.title = titleIn.value;
          if (prioIn) wizardData.priority = prioIn.value;
          if (deadIn) wizardData.requestedDeadline = deadIn.value;
          if (reasIn) wizardData.reason = reasIn.value;
        }
      }

      document.getElementById('audNextBtn').addEventListener('click', function () {
        collectCurrentStepData();
        if (currentStep < 5) {
          renderStep(currentStep + 1);
        } else {
          // SUBMIT
          AcademicRequests.createRequest({
            module: wizardData.module,
            moduleLabel: wizardData.moduleLabel,
            affectedRecordId: wizardData.affectedRecordId,
            title: wizardData.title || ('Adjustment for ' + (record.className || record.subjectName || 'Schedule')),
            campus: wizardData.campus,
            department: wizardData.department,
            requestingPrincipal: wizardData.requestingPrincipal,
            priority: wizardData.priority,
            requestedDeadline: wizardData.requestedDeadline,
            reason: wizardData.reason || 'Operational adjustment requested by Principal.',
            currentSnapshot: wizardData.currentSnapshot,
            proposedChanges: wizardData.proposedChanges
          });

          // Show confirmation toast
          closeDrawer();
          AcademicRequests._showToast('Adjustment request successfully sent to Administration!');
        }
      });

      document.getElementById('audPrevBtn').addEventListener('click', function () {
        collectCurrentStepData();
        if (currentStep > 1) {
          renderStep(currentStep - 1);
        }
      });

      function closeDrawer() {
        var panel = document.getElementById('audPanel');
        if (panel) panel.classList.add('translate-x-full');
        setTimeout(function () {
          var d = document.getElementById('academicUniversalDrawer');
          if (d) d.remove();
        }, 260);
      }

      document.getElementById('audCloseBtn').addEventListener('click', closeDrawer);
      document.getElementById('audCancelBtn').addEventListener('click', closeDrawer);
      document.getElementById('audBackdrop').addEventListener('click', closeDrawer);
    },

    /* ════════════════════════════════════════════════════════════════════════
       ADMIN REQUEST REVIEW WORKSPACE DRAWER
       ════════════════════════════════════════════════════════════════════════ */
    openAdminReviewDrawer: function (requestId) {
      var req = this.getById(requestId);
      if (!req) return;

      var existing = document.getElementById('adminReviewDrawer');
      if (existing) existing.remove();

      var drawerEl = document.createElement('div');
      drawerEl.id = 'adminReviewDrawer';
      drawerEl.className = 'fixed inset-0 z-50 overflow-hidden flex justify-end';
      drawerEl.setAttribute('role', 'dialog');

      var statusBadges = {
        submitted: '<span class="px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-slate-100 text-slate-700 border border-slate-200">Submitted</span>',
        under_review: '<span class="px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-amber-50 text-amber-700 border border-amber-200">Under Review</span>',
        accepted: '<span class="px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">Accepted</span>',
        in_progress: '<span class="px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">In Progress</span>',
        completed: '<span class="px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-emerald-100 text-emerald-800 border border-emerald-300">Completed &amp; Published</span>',
        declined: '<span class="px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-red-50 text-red-700 border border-red-200">Declined</span>'
      };

      var timelineItems = (req.timeline || []).map(function (item) {
        return (
          '<div class="relative pl-6 pb-4 border-l border-slate-200 last:border-l-0">' +
            '<div class="absolute -left-1.5 top-0.5 w-3 h-3 rounded-full bg-[#176B45]"></div>' +
            '<div class="text-xs font-medium text-slate-800">' + item.by + ' · ' + (item.role || 'System') + '</div>' +
            '<div class="text-[11px] text-slate-400 mt-0.5">' + new Date(item.timestamp).toLocaleString() + '</div>' +
            '<div class="text-xs text-slate-600 mt-1">' + item.note + '</div>' +
          '</div>'
        );
      }).join('');

      drawerEl.innerHTML =
        '<div class="fixed inset-0 bg-slate-900/40 backdrop-blur-xs transition-opacity" id="ardBackdrop"></div>' +
        '<div class="relative w-full max-w-2xl bg-white h-full shadow-2xl flex flex-col z-10 transform transition-transform duration-250 ease-out translate-x-full" id="ardPanel">' +
          
          '<!-- Header -->' +
          '<div class="p-5 border-b border-[#E1E9E3] bg-[#F7F9F7] flex items-center justify-between shrink-0">' +
            '<div class="flex items-center gap-3">' +
              '<div class="w-10 h-10 rounded-xl bg-blue-50 text-blue-700 flex items-center justify-center">' +
                '<span class="material-symbols-outlined text-xl">rate_review</span>' +
              '</div>' +
              '<div>' +
                '<div class="flex items-center gap-2">' +
                  '<h2 class="text-base font-medium text-slate-900 leading-tight">Admin Review: ' + req.id + '</h2>' +
                  (statusBadges[req.status] || req.status) +
                '</div>' +
                '<p class="text-xs text-slate-500 font-normal mt-0.5">' + req.moduleLabel + ' · Requested by ' + req.requestingPrincipal + '</p>' +
              '</div>' +
            '</div>' +
            '<button type="button" id="ardCloseBtn" class="w-8 h-8 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-200/60 flex items-center justify-center transition cursor-pointer">' +
              '<span class="material-symbols-outlined text-lg">close</span>' +
            '</button>' +
          '</div>' +

          '<!-- Body -->' +
          '<div class="p-6 overflow-y-auto flex-1 space-y-6">' +
            '<!-- Title & Reason -->' +
            '<div>' +
              '<h3 class="text-sm font-medium text-slate-900">' + req.title + '</h3>' +
              '<div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200 text-xs text-slate-700 mt-2.5 leading-relaxed">' +
                '<span class="text-slate-400 font-normal">Principal Rationale: </span>' + req.reason +
              '</div>' +
            '</div>' +

            '<!-- Before & After Comparison -->' +
            '<div>' +
              '<h4 class="text-xs font-medium uppercase text-slate-500 tracking-wider mb-2">Adjustment Scope Diff</h4>' +
              '<div class="grid grid-cols-2 gap-3">' +
                '<div class="p-4 bg-slate-50 rounded-xl border border-slate-200 text-xs space-y-1">' +
                  '<div class="text-[11px] font-medium text-slate-400 uppercase mb-2">Current Academic State</div>' +
                  '<pre class="text-[11px] text-slate-700 whitespace-pre-wrap font-sans">' + JSON.stringify(req.currentSnapshot, null, 2) + '</pre>' +
                '</div>' +
                '<div class="p-4 bg-emerald-50/60 rounded-xl border border-emerald-200 text-xs space-y-1">' +
                  '<div class="text-[11px] font-medium text-[#176B45] uppercase mb-2">Proposed New Parameters</div>' +
                  '<pre class="text-[11px] text-slate-800 whitespace-pre-wrap font-sans">' + JSON.stringify(req.proposedChanges, null, 2) + '</pre>' +
                '</div>' +
              '</div>' +
            '</div>' +

            '<!-- Administrative Activity Timeline -->' +
            '<div>' +
              '<h4 class="text-xs font-medium uppercase text-slate-500 tracking-wider mb-3">Activity &amp; Decision History</h4>' +
              '<div class="pt-2">' + timelineItems + '</div>' +
            '</div>' +
          '</div>' +

          '<!-- Admin Action Bar -->' +
          '<div class="p-4 border-t border-[#E1E9E3] bg-[#F7F9F7] flex items-center justify-between shrink-0">' +
            '<div class="flex items-center gap-2">' +
              '<button type="button" id="btnAdminClarify" class="px-3 py-1.5 text-xs font-medium text-amber-700 bg-amber-50 border border-amber-200 rounded-lg hover:bg-amber-100 transition cursor-pointer">' +
                'Request Clarification' +
              '</button>' +
              '<button type="button" id="btnAdminDecline" class="px-3 py-1.5 text-xs font-medium text-red-700 bg-red-50 border border-red-200 rounded-lg hover:bg-red-100 transition cursor-pointer">' +
                'Decline' +
              '</button>' +
            '</div>' +
            '<div class="flex items-center gap-2">' +
              '<button type="button" id="btnAdminAccept" class="px-3.5 py-1.5 text-xs font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition cursor-pointer">' +
                'Accept Request' +
              '</button>' +
              '<button type="button" id="btnAdminPublish" class="px-4 py-1.5 text-xs font-medium text-white bg-[#176B45] hover:bg-[#125536] rounded-lg transition shadow-xs cursor-pointer">' +
                'Publish &amp; Complete' +
              '</button>' +
            '</div>' +
          '</div>' +

        '</div>';

      document.body.appendChild(drawerEl);

      requestAnimationFrame(function () {
        document.getElementById('ardPanel').classList.remove('translate-x-full');
      });

      function closeReview() {
        var panel = document.getElementById('ardPanel');
        if (panel) panel.classList.add('translate-x-full');
        setTimeout(function () {
          var d = document.getElementById('adminReviewDrawer');
          if (d) d.remove();
        }, 260);
      }

      document.getElementById('ardCloseBtn').addEventListener('click', closeReview);
      document.getElementById('ardBackdrop').addEventListener('click', closeReview);

      document.getElementById('btnAdminAccept').addEventListener('click', function () {
        AcademicRequests.updateRequestStatus(req.id, 'accepted', 'Endorsed by academic committee. Scheduled for operational deployment.', 'Sok Panha Heng (Admin)');
        closeReview();
        AcademicRequests._showToast('Request ' + req.id + ' marked as Accepted.');
      });

      document.getElementById('btnAdminPublish').addEventListener('click', function () {
        AcademicRequests.updateRequestStatus(req.id, 'completed', 'Validated and published into official master schedule and faculty portals.', 'Sok Panha Heng (Admin)');
        closeReview();
        AcademicRequests._showToast('Adjustment ' + req.id + ' published successfully across all portals!');
      });

      document.getElementById('btnAdminClarify').addEventListener('click', function () {
        var note = prompt('Enter clarification request for Dr. Ly Bunheng (Principal):', 'Please confirm whether Grade 10B requires a co-teacher.');
        if (note) {
          AcademicRequests.updateRequestStatus(req.id, 'needs_clarification', note, 'Sok Panha Heng (Admin)');
          closeReview();
          AcademicRequests._showToast('Clarification requested from Principal.');
        }
      });

      document.getElementById('btnAdminDecline').addEventListener('click', function () {
        var reason = prompt('Enter operational reason for declining this request:', 'Room capacity conflicts with afternoon lecture.');
        if (reason) {
          AcademicRequests.updateRequestStatus(req.id, 'declined', reason, 'Sok Panha Heng (Admin)');
          closeReview();
          AcademicRequests._showToast('Request declined with logged rationale.');
        }
      });
    },

    _showToast: function (msg) {
      var toast = document.createElement('div');
      toast.className = 'fixed bottom-5 right-5 z-50 px-4 py-2.5 rounded-xl bg-slate-900 text-white text-xs font-medium shadow-xl flex items-center gap-2 transform transition-all duration-200 translate-y-3 opacity-0';
      toast.innerHTML = '<span class="material-symbols-outlined text-[18px] text-emerald-400">check_circle</span><span>' + msg + '</span>';
      document.body.appendChild(toast);
      requestAnimationFrame(function () {
        toast.classList.remove('translate-y-3', 'opacity-0');
      });
      setTimeout(function () {
        toast.classList.add('translate-y-3', 'opacity-0');
        setTimeout(function () { toast.remove(); }, 250);
      }, 3500);
    }
  };

  // Auto-init on load
  AcademicRequests.init();
  window.AcademicRequests = AcademicRequests;

})(window);
