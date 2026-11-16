/**
 * NGIS — Register New User wizard (shared by all Admin account directories)
 * ---------------------------------------------------------------------------
 * Implements the mandated 3-step registration flow:
 *   [1] Information (personal + institutional)  [2] Credentials  [3] Review & Create  ->  Success
 *
 * Vanilla JS only. The component owns its own DOM inside the shared
 * NGIS modal shell, so every directory (students / teachers / staff /
 * principals / admins) gets the exact same design with role-specific
 * placement fields driven by ctx.cfg.type.
 *
 * Design adaptations that keep the production flows honest:
 *   - No artificial timers. The provisioning state follows the real
 *     /api/user-mgmt/create-person request (inline button progress only).
 *   - No bold weights, no gradients, no infinite pulsing animation.
 *   - Failed submissions surface an error banner with Retry.
 *   - The wizard never blocks the sidebar/topbar behind a full-screen loader.
 */
(function (window, document) {
  'use strict';

  var R = window.NGIS_REGISTER = window.NGIS_REGISTER || {};
  R.version = '1.0';

  var STEPS = [
    { n: 1, label: 'Information', full: 'Personal and institutional information' },
    { n: 2, label: 'Credentials', full: 'Generate account credentials' },
    { n: 3, label: 'Review', full: 'Review and create' }
  ];

  var CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 13l4 4L19 7"/></svg>';
  var LOCK = '<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>';
  var REFRESH = '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>';
  var EYE = '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/></svg>';

  R.open = function (ctx, prefill) {
    var cfg = ctx.cfg;
    var type = cfg.type;
    var roleTitle = ctx.roleTitle;
    var esc = ctx.esc;
    var q = ctx.q;

    var step = 1;
    var busy = false;
    var busyLabel = '';
    var created = null;
    var lastStep = 0;
    var checkSeq = 0;
    var checkTimer = null;

    var form = {
      firstName: (prefill && prefill.firstName) || '',
      lastName: (prefill && prefill.lastName) || '',
      khmerName: '',
      gender: 'M',
      dob: '',
      email: (prefill && prefill.email) || '',
      phone: (prefill && prefill.phone) || '',
      photo: (prefill && prefill.photo) || '',
      campus: (prefill && prefill.campus) || '',
      academicYear: '2025-26',
      department: '',
      klass: '',
      enrollments: [],
      assignments: [],
      enrollmentStatus: 'active',
      parentName: '',
      parentContact: '',
      position: '',
      subjects: [],
      scope: '',
      status: 'active',
      institutionalId: '',
      username: '',
      temporaryPassword: '',
      accountType: ctx.accountType,
      usernameEdited: false,
      usernameValid: true,
      usernameChecking: false,
      usernameMessage: '',
      showPassword: false,
      dispatch: true,
      error: '',
      errorRetry: false
    };

    var opts = {
      campuses: [], departments: [], classes: [], grades: [],
      department_structure: {},
      dept_subjects_map: {},
      subjects_by_department: {},
      subjects: [], positions: [], academic_years: ['2025-26', '2026-27']
    };

    // ── modal shell ──────────────────────────────────────────────────────
    // Part 10.2: the header carries the title only — no subtitle.
    var wrap = ctx.openModal(
      'Register New ' + roleTitle,
      '',
      '<div class="nrg-scope" id="nrg-shell"></div>',
      '<div class="nrg-foot-inner" id="nrg-foot"></div>',
      true,
      { confirmUnsaved: true }
    );
    wrap.classList.add('nrg-backdrop', 'nrg-scope');
    var titleEl = q(wrap, '.ngis-modal-title');
    if (titleEl) {
      titleEl.id = 'nrg-registration-title';
      wrap.setAttribute('aria-labelledby', titleEl.id);
      wrap.removeAttribute('aria-label');
    }
    var shell = q(wrap, '#nrg-shell');
    var foot = q(wrap, '#nrg-foot');
    var footWrap = q(wrap, '.ngis-modal-foot');

    // ── small markup helpers ─────────────────────────────────────────────
    function optionsHtml(list, current) {
      return (list || []).map(function (v) {
        var val, text;
        if (v && typeof v === 'object') {
          val = v.short || v.name || v.id || '';
          text = v.name || v.short || val;
        } else { val = v; text = v; }
        return '<option value="' + esc(val) + '"' +
          (String(current) === String(val) ? ' selected' : '') + '>' + esc(text) + '</option>';
      }).join('');
    }

    function input(id, inputType, value, placeholder, extra) {
      return '<input class="nrg-input" type="' + inputType + '" id="' + id +
        '" value="' + esc(value || '') + '" placeholder="' + esc(placeholder || '') +
        '"' + (extra || '') + '>';
    }

    function select(id, list, current) {
      return '<select class="nrg-select" id="' + id + '">' + optionsHtml(list, current) + '</select>';
    }

    function field(label, id, control, o) {
      o = o || {};
      return '<div class="nrg-field' + (o.span ? ' nrg-span-2' : '') + '">' +
        '<label class="nrg-label" for="' + id + '"><span>' + esc(label) +
        (o.required ? ' <span class="nrg-req">*</span>' : '') + '</span>' +
        (o.optional ? '<span class="nrg-optional">Optional</span>' : '') + '</label>' +
        control + '</div>';
    }

    function sectionHead(label, hint) {
      return '<div class="nrg-section-head"><span>' + esc(label) + '</span>' +
        (hint ? '<span class="nrg-hint">' + esc(hint) + '</span>' : '') + '</div>';
    }

    function paneOpen(n) {
      return '<div class="nrg-pane" data-nrg-pane="' + n + '" aria-busy="' +
        (busy ? 'true' : 'false') + '">';
    }

    // ── stepper ──────────────────────────────────────────────────────────
    function stepperHtml() {
      if (step === 4) return '';
      var out = '<nav class="nrg-stepbar" aria-label="Registration progress">';
      STEPS.forEach(function (s, i) {
        if (i) out += '<span class="nrg-divider" aria-hidden="true"></span>';
        var done = s.n < step;
        var cls = s.n === step ? 'is-active' : (done ? 'is-done' : 'is-upcoming');
        out += '<button type="button" class="nrg-step ' + cls + '" data-nrg-step="' + s.n + '"' +
          (s.n === step ? ' aria-current="step"' : '') +
          (done && !busy ? '' : ' disabled') +
          ' aria-label="Step ' + s.n + ' of 3: ' + esc(s.full) + '">' +
          '<span class="nrg-badge" aria-hidden="true">' + (done ? CHECK : s.n) + '</span>' +
          '<span class="nrg-step-label">' + esc(s.label) + '</span></button>';
      });
      return out + '</nav>';
    }

    function errorHtml() {
      if (!form.error) return '';
      return '<div class="nrg-error" role="alert">' +
        '<span class="nrg-error-text">' + esc(form.error) + '</span>' +
        (form.errorRetry ? '<button type="button" class="nrg-link" data-nrg-retry>Retry</button>' : '') +
        '<button type="button" class="nrg-error-dismiss" data-nrg-error-dismiss aria-label="Dismiss message">&times;</button>' +
        '</div>';
    }

    // ── step 1: personal + institutional information ────────────────────
    function genderField() {
      var items = [['M', 'Male'], ['F', 'Female'], ['Other', 'Other']];
      var out = '<div class="nrg-field"><span class="nrg-label"><span>Gender</span></span>' +
        '<div class="nrg-segmented" role="radiogroup" aria-label="Gender">';
      items.forEach(function (g) {
        out += '<label class="nrg-segment' + (form.gender === g[0] ? ' is-selected' : '') + '">' +
          '<input type="radio" name="nrg-gender" value="' + g[0] + '"' +
          (form.gender === g[0] ? ' checked' : '') + '><span>' + g[1] + '</span></label>';
      });
      return out + '</div></div>';
    }

    function personalFields() {
      var h = '';
      h += field('First Name', 'nrg-first', input('nrg-first', 'text', form.firstName, 'e.g. Seila'), { required: true });
      h += field('Last Name', 'nrg-last', input('nrg-last', 'text', form.lastName, 'e.g. Oudom'), { required: true });
      h += field('Khmer Full Name', 'nrg-khmer', input('nrg-khmer', 'text', form.khmerName, 'ឈ្មោះជាភាសាខ្មែរ'), { optional: true });
      h += genderField();
      h += field('Contact Email', 'nrg-email', input('nrg-email', 'email', form.email, 'e.g. s.meas@example.com'), { required: true });
      h += field('Phone Number', 'nrg-phone', input('nrg-phone', 'tel', form.phone, 'e.g. +855 12 345 678'), { required: true });
      h += field('Date of Birth', 'nrg-dob', input('nrg-dob', 'date', form.dob, ''));
      h += field('Photo URL', 'nrg-photo', input('nrg-photo', 'url', form.photo, 'https://...'), { optional: true });
      return h;
    }

    function getDepartmentGrades(deptName) {
      if (!deptName) return ['7', '8', '9', '10', '11', '12'];
      var ds = opts.department_structure && opts.department_structure[deptName];
      if (ds && ds.grades && ds.grades.length) return ds.grades;
      var matched = (opts.classes || []).filter(function (c) {
        return c.department === deptName || c.department_id === deptName;
      });
      if (matched.length) {
        var gSet = {};
        matched.forEach(function (c) { if (c.grade) gSet[c.grade] = true; });
        var gArr = Object.keys(gSet);
        if (gArr.length) return gArr.sort(function (a, b) { return (parseInt(a, 10) || 0) - (parseInt(b, 10) || 0); });
      }
      return ['7', '8', '9', '10', '11', '12'];
    }

    function getDepartmentClasses(deptName, gradeVal) {
      gradeVal = String(gradeVal || '').replace('Grade ', '').trim();
      var ds = opts.department_structure && opts.department_structure[deptName];
      if (ds && ds.classes_by_grade && ds.classes_by_grade[gradeVal] && ds.classes_by_grade[gradeVal].length) {
        return ds.classes_by_grade[gradeVal];
      }
      var matched = (opts.classes || []).filter(function (c) {
        var deptMatch = !deptName || c.department === deptName || c.department_id === deptName;
        var gradeMatch = !gradeVal || String(c.grade || '') === gradeVal;
        return deptMatch && gradeMatch;
      });
      if (matched.length) {
        return matched.map(function (c) {
          return { id: c.id, name: c.name || ('Grade ' + c.short), short: c.short || c.name };
        });
      }
      return [
        { id: 'cls-' + gradeVal + 'a', name: 'Grade ' + gradeVal + 'A', short: gradeVal + 'A' },
        { id: 'cls-' + gradeVal + 'b', name: 'Grade ' + gradeVal + 'B', short: gradeVal + 'B' }
      ];
    }

    function studentEnrollmentsHtml() {
      if (!form.enrollments || !form.enrollments.length) {
        var firstDept = (opts.departments && opts.departments[0]) || 'Khmer Studies Department';
        var firstGrades = getDepartmentGrades(firstDept);
        var firstG = firstGrades[0] || '12';
        var firstClasses = getDepartmentClasses(firstDept, firstG);
        var firstC = firstClasses[0] ? firstClasses[0].short : '12A';
        form.enrollments = [{
          id: 'enr-init-1',
          department: firstDept,
          grade: 'Grade ' + firstG,
          class: firstC,
          classId: firstClasses[0] ? firstClasses[0].id : '',
          status: 'active'
        }];
      }

      var h = '<div class="nrg-span-2 nrg-enrollments-wrapper">';
      h += '<div class="nrg-enr-section-header">' +
        '<div>' +
          '<div class="nrg-enr-title">Academic Department Enrollments <span class="nrg-req">*</span></div>' +
          '<div class="nrg-enr-subtitle">A student can study in 1, 2, or 3+ departments (e.g. Khmer, English, Chinese) with distinct grades and classes.</div>' +
        '</div>' +
      '</div>';

      h += '<div class="nrg-enr-list" id="nrg-enr-list">';
      form.enrollments.forEach(function (enr, idx) {
        var dept = enr.department || (opts.departments && opts.departments[0]) || '';
        var validGrades = getDepartmentGrades(dept);
        var curGradeNum = String(enr.grade || validGrades[0] || '10').replace('Grade ', '').trim();
        var validClasses = getDepartmentClasses(dept, curGradeNum);
        var curClass = enr.class || (validClasses[0] ? validClasses[0].short : '');

        var deptOptsHtml = (opts.departments || []).map(function (d) {
          var dName = typeof d === 'object' ? (d.name || d.short) : d;
          var isCurrent = dName === dept;
          var isChosenElsewhere = form.enrollments.some(function (other, otherIdx) {
            return otherIdx !== idx && other.department === dName;
          });
          return '<option value="' + esc(dName) + '"' + (isCurrent ? ' selected' : '') + (isChosenElsewhere ? ' disabled' : '') + '>' +
            esc(dName) + (isChosenElsewhere ? ' (Already selected)' : '') + '</option>';
        }).join('');

        var gradeOptsHtml = validGrades.map(function (g) {
          var gNum = String(g).replace('Grade ', '').trim();
          var isSelected = String(curGradeNum) === gNum;
          return '<option value="Grade ' + esc(gNum) + '"' + (isSelected ? ' selected' : '') + '>Grade ' + esc(gNum) + '</option>';
        }).join('');

        var classOptsHtml = validClasses.map(function (c) {
          var cVal = c.short || c.name;
          var isSelected = String(curClass) === String(cVal);
          return '<option value="' + esc(cVal) + '" data-cid="' + esc(c.id || '') + '"' + (isSelected ? ' selected' : '') + '>' + esc(cVal) + '</option>';
        }).join('');

        h += '<div class="nrg-enr-card" data-enr-card-idx="' + idx + '">' +
          '<div class="nrg-enr-card-head">' +
            '<div class="nrg-enr-badge-row">' +
              '<span class="nrg-enr-num-badge">Enrollment ' + (idx + 1) + '</span>' +
              '<span class="nrg-enr-dept-tag">' + esc(dept) + '</span>' +
            '</div>' +
            (form.enrollments.length > 1
              ? '<button type="button" class="nrg-enr-remove-btn" data-enr-remove="' + idx + '" title="Remove this department enrollment" aria-label="Remove enrollment ' + (idx + 1) + '">' +
                '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>' +
                '<span>Remove</span></button>'
              : '') +
          '</div>' +
          '<div class="nrg-enr-grid">' +
            '<div class="nrg-enr-field">' +
              '<label class="nrg-enr-label" for="nrg-enr-dept-' + idx + '">Department <span class="nrg-req">*</span></label>' +
              '<select class="nrg-select nrg-enr-dept-select" id="nrg-enr-dept-' + idx + '" data-enr-idx="' + idx + '">' + deptOptsHtml + '</select>' +
            '</div>' +
            '<div class="nrg-enr-field">' +
              '<label class="nrg-enr-label" for="nrg-enr-grade-' + idx + '">Grade Level <span class="nrg-req">*</span></label>' +
              '<select class="nrg-select nrg-enr-grade-select" id="nrg-enr-grade-' + idx + '" data-enr-idx="' + idx + '">' + gradeOptsHtml + '</select>' +
            '</div>' +
            '<div class="nrg-enr-field">' +
              '<label class="nrg-enr-label" for="nrg-enr-class-' + idx + '">Class Section <span class="nrg-req">*</span></label>' +
              '<select class="nrg-select nrg-enr-class-select" id="nrg-enr-class-' + idx + '" data-enr-idx="' + idx + '">' + classOptsHtml + '</select>' +
            '</div>' +
          '</div>' +
        '</div>';
      });
      h += '</div>';

      h += '<div class="nrg-enr-add-wrap">' +
        '<button type="button" class="nrg-add-dept-btn" id="nrg-add-dept-btn">' +
          '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>' +
          '<span>+ Add Another Department</span>' +
        '</button>' +
      '</div>';
      h += '</div>';
      return h;
    }

    function getDepartmentSubjects(deptName) {
      if (!deptName) return opts.subjects || [];
      if (opts.subjects_by_department && opts.subjects_by_department[deptName]) {
        return opts.subjects_by_department[deptName];
      }
      if (opts.dept_subjects_map && opts.dept_subjects_map[deptName]) {
        return opts.dept_subjects_map[deptName];
      }
      var ds = opts.department_structure && opts.department_structure[deptName];
      if (ds && ds.subjects && ds.subjects.length) {
        return ds.subjects;
      }
      for (var k in (opts.subjects_by_department || {})) {
        if (k.toLowerCase() === deptName.toLowerCase() ||
            k.toLowerCase().indexOf(deptName.toLowerCase()) !== -1 ||
            deptName.toLowerCase().indexOf(k.toLowerCase()) !== -1) {
          return opts.subjects_by_department[k];
        }
      }
      return opts.subjects || [];
    }

    function teacherAssignmentsHtml() {
      if (!form.assignments || !form.assignments.length) {
        var firstDept = (opts.departments && opts.departments[0]) || 'Khmer Studies Department';
        var firstGrades = getDepartmentGrades(firstDept);
        var firstG = firstGrades[0] || '12';
        var firstClasses = getDepartmentClasses(firstDept, firstG);
        var firstC = firstClasses[0] ? firstClasses[0].short : '12A';
        var firstSubjs = getDepartmentSubjects(firstDept);
        var firstSubj = firstSubjs[0] ? (typeof firstSubjs[0] === 'object' ? (firstSubjs[0].name || firstSubjs[0].id) : firstSubjs[0]) : 'General';
        var firstSubjId = firstSubjs[0] && typeof firstSubjs[0] === 'object' ? firstSubjs[0].id : '';
        form.assignments = [{
          id: 'asgn-init-1',
          department: firstDept,
          grade: 'Grade ' + firstG,
          class: firstC,
          classId: firstClasses[0] ? firstClasses[0].id : '',
          subject: firstSubj,
          subjectId: firstSubjId
        }];
      }

      var h = '<div class="nrg-span-2 nrg-teaching-assignments-wrap">';
      h += '<div class="nrg-enr-section-header">' +
        '<div>' +
          '<div class="nrg-enr-title">Teaching Assignments <span class="nrg-req">*</span></div>' +
          '<div class="nrg-enr-subtitle">Assign classes and subjects across single or multiple academic departments. Teachers can be assigned to multiple classes (e.g. 3, 5, 10+ classes).</div>' +
        '</div>' +
      '</div>';

      h += '<div class="nrg-asgn-cards" id="nrg-asgn-list">';
      form.assignments.forEach(function (asgn, idx) {
        var dept = asgn.department || (opts.departments && opts.departments[0]) || '';
        var validGrades = getDepartmentGrades(dept);
        var curGradeNum = String(asgn.grade || validGrades[0] || '12').replace('Grade ', '').trim();
        var validClasses = getDepartmentClasses(dept, curGradeNum);
        var curClass = asgn.class || (validClasses[0] ? validClasses[0].short : '');
        var validSubjs = getDepartmentSubjects(dept);
        var curSubject = asgn.subject || (validSubjs[0] ? (typeof validSubjs[0] === 'object' ? (validSubjs[0].name || validSubjs[0].id) : validSubjs[0]) : '');

        var deptOptsHtml = (opts.departments || []).map(function (d) {
          var dName = typeof d === 'object' ? (d.name || d.short) : d;
          var isCurrent = dName === dept;
          return '<option value="' + esc(dName) + '"' + (isCurrent ? ' selected' : '') + '>' + esc(dName) + '</option>';
        }).join('');

        var gradeOptsHtml = validGrades.map(function (g) {
          var gNum = String(g).replace('Grade ', '').trim();
          var isSelected = String(curGradeNum) === gNum;
          return '<option value="Grade ' + esc(gNum) + '"' + (isSelected ? ' selected' : '') + '>Grade ' + esc(gNum) + '</option>';
        }).join('');

        var classOptsHtml = validClasses.map(function (c) {
          var cVal = c.short || c.name;
          var isSelected = String(curClass) === String(cVal);
          return '<option value="' + esc(cVal) + '" data-cid="' + esc(c.id || '') + '"' + (isSelected ? ' selected' : '') + '>' + esc(cVal) + '</option>';
        }).join('');

        var subjOptsHtml = validSubjs.map(function (s) {
          var sName = typeof s === 'object' ? (s.name || s.id) : s;
          var sId = typeof s === 'object' ? (s.id || s.name) : s;
          var isSelected = String(curSubject).toLowerCase() === String(sName).toLowerCase() || String(curSubject).toLowerCase() === String(sId).toLowerCase();
          return '<option value="' + esc(sName) + '" data-sid="' + esc(sId) + '"' + (isSelected ? ' selected' : '') + '>' + esc(sName) + '</option>';
        }).join('');

        h += '<div class="nrg-asgn-card" data-asgn-idx="' + idx + '">' +
          '<div class="nrg-asgn-head">' +
            '<div class="nrg-asgn-head-l">' +
              '<span class="nrg-asgn-num-badge">Assignment ' + (idx + 1) + '</span>' +
              '<span class="nrg-asgn-title" style="color:var(--nrg-text);margin-left:6px;font-weight:500;">' + esc(dept) + ' &bull; ' + esc(asgn.class || '') + ' &bull; ' + esc(asgn.subject || '') + '</span>' +
            '</div>' +
            (form.assignments.length > 1
              ? '<button type="button" class="nrg-asgn-remove-btn" data-asgn-remove="' + idx + '" title="Remove this teaching assignment" aria-label="Remove assignment ' + (idx + 1) + '">' +
                '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>' +
                '<span>Remove</span></button>'
              : '') +
          '</div>' +
          '<div class="nrg-asgn-grid">' +
            '<div class="nrg-asgn-field">' +
              '<label class="nrg-asgn-label" for="nrg-asgn-dept-' + idx + '">Department <span class="nrg-req">*</span></label>' +
              '<select class="nrg-select nrg-asgn-dept-select" id="nrg-asgn-dept-' + idx + '" data-asgn-idx="' + idx + '">' + deptOptsHtml + '</select>' +
            '</div>' +
            '<div class="nrg-asgn-field">' +
              '<label class="nrg-asgn-label" for="nrg-asgn-grade-' + idx + '">Grade Level <span class="nrg-req">*</span></label>' +
              '<select class="nrg-select nrg-asgn-grade-select" id="nrg-asgn-grade-' + idx + '" data-asgn-idx="' + idx + '">' + gradeOptsHtml + '</select>' +
            '</div>' +
            '<div class="nrg-asgn-field">' +
              '<label class="nrg-asgn-label" for="nrg-asgn-class-' + idx + '">Class Section <span class="nrg-req">*</span></label>' +
              '<select class="nrg-select nrg-asgn-class-select" id="nrg-asgn-class-' + idx + '" data-asgn-idx="' + idx + '">' + classOptsHtml + '</select>' +
            '</div>' +
            '<div class="nrg-asgn-field">' +
              '<label class="nrg-asgn-label" for="nrg-asgn-subj-' + idx + '">Subject <span class="nrg-req">*</span></label>' +
              '<select class="nrg-select nrg-asgn-subj-select" id="nrg-asgn-subj-' + idx + '" data-asgn-idx="' + idx + '">' + subjOptsHtml + '</select>' +
            '</div>' +
          '</div>' +
        '</div>';
      });
      h += '</div>';

      h += '<div class="nrg-asgn-add-wrap" style="margin-top:12px;">' +
        '<button type="button" class="nrg-add-dept-btn" id="nrg-add-class-btn">' +
          '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>' +
          '<span>+ Add Another Class</span>' +
        '</button>' +
      '</div>';
      h += '</div>';
      return h;
    }

    function placementFields() {
      var campuses = opts.campuses.length ? opts.campuses : ['Sensok', 'Tuol Kork Main Campus', 'Chamkarmon High School Branch'];
      var h = '';
      h += field('Campus Assignment', 'nrg-campus', select('nrg-campus', campuses, form.campus), { required: true });
      if (type === 'student') {
        h += field('Academic Year', 'nrg-year', select('nrg-year', opts.academic_years, form.academicYear), { required: true });
        h += field('Enrollment Status', 'nrg-enroll', select('nrg-enroll', [
          { short: 'active', name: 'Active (Enrolled)' },
          { short: 'pending', name: 'Pending Placement' },
          { short: 'probationary', name: 'Probationary' }
        ], form.enrollmentStatus));
        // Dynamic Multi-Department Academic Placement
        h += studentEnrollmentsHtml();
        h += field('Parent / Guardian Full Name', 'nrg-parent', input('nrg-parent', 'text', form.parentName, 'e.g. Kim Sovann'));
        h += field('Parent Contact (Phone / Email)', 'nrg-parent-contact', input('nrg-parent-contact', 'text', form.parentContact, 'e.g. +855 12 777 888'));
      } else if (type === 'teacher') {
        var teacherDepts = opts.departments.length ? opts.departments :
          ['Khmer Studies Department', 'English Department', 'Chinese Department'];
        h += field('Primary Academic Department', 'nrg-dept', select('nrg-dept', teacherDepts, form.department), { required: true });
        var positions = opts.positions.length ? opts.positions :
          ['Subject Teacher', 'Lead / Senior Faculty', 'Head of Department', 'Adjunct Instructor'];
        h += field('Employment Position', 'nrg-position', select('nrg-position', positions, form.position), { required: true });
        h += field('Initial Status', 'nrg-status', select('nrg-status', [
          { short: 'active', name: 'Active Faculty (Immediate)' },
          { short: 'probationary', name: 'Probationary Period' },
          { short: 'on_leave', name: 'Pending Semester Start' }
        ], form.status));
        var spec = Array.isArray(form.subjects) ? form.subjects.join(', ') : (form.subjects || '');
        h += field('Primary Specialization / Notes', 'nrg-subjects',
          input('nrg-subjects', 'text', spec, 'e.g. Khmer Literature, Mathematics'), { optional: true });
        // Dynamic Multi-Class & Multi-Department Teaching Assignments
        h += teacherAssignmentsHtml();
      } else if (type === 'staff') {
        var staffDepts = ['Campus Operations', 'Finance & Accounting', 'IT & Infrastructure', 'Student Affairs', 'Facilities & Logistics'];
        h += field('Department', 'nrg-dept', select('nrg-dept', staffDepts, form.department), { required: true });
        h += field('Job Position / Role', 'nrg-position', select('nrg-position',
          ['Campus Operations Officer', 'IT Systems Technician', 'Accounts Officer', 'Registrar Staff', 'Facilities Coordinator'], form.position), { required: true });
      } else if (type === 'principal') {
        h += field('Leadership Position', 'nrg-position', select('nrg-position',
          ['Campus Principal', 'Vice Principal', 'Associate Academic Director'], form.position), { required: true });
        h += field('Authorized School Scope', 'nrg-scope', input('nrg-scope', 'text', form.scope || (form.campus + ' Scope'), 'e.g. Sensok Campus Scope'));
      } else if (type === 'admin') {
        h += field('Administrative Position', 'nrg-position', select('nrg-position',
          ['School Systems Administrator', 'Registrar Administrator', 'IT Infrastructure Administrator', 'Data & Operations Admin'], form.position), { required: true });
        h += field('Authorized Access Scope', 'nrg-scope', select('nrg-scope',
          ['Standard Administrative Scope', 'Campus Scope', 'Executive Console Scope'], form.scope || 'Standard Administrative Scope'));
      }
      return h;
    }

    function pane1() {
      var h = paneOpen(1) + sectionHead('Basic Identity', '* Required fields') + '<div class="nrg-grid">';
      h += personalFields();
      h += '</div>';
      h += sectionHead('Institutional Placement', 'Reuses existing campus, class and department records') + '<div class="nrg-grid">';
      h += placementFields();
      return h + '</div></div>';
    }

    // ── step 2: generate account credentials ─────────────────────────────
    function statusTag() {
      var cls = form.usernameChecking ? 'is-muted' :
        (form.usernameValid ? '' : 'is-bad');
      var text = form.usernameMessage || (form.usernameValid ? 'Available' : 'Invalid format');
      return '<span class="nrg-tag ' + cls + '" id="nrg-username-status">' +
        (form.usernameValid && !form.usernameChecking ? CHECK : '') + esc(text) + '</span>';
    }

    function pane2() {
      var h = paneOpen(2) + sectionHead('Generate Account Credentials', 'Issued by the server — finalized only on creation') + '<div class="nrg-grid">';
      h += '<div class="nrg-cred-card">' +
        '<span class="nrg-cred-label">Institutional ID</span>' +
        '<div class="nrg-cred-row"><span class="nrg-cred-value nrg-mono" id="nrg-inst-id">' +
        esc(form.institutionalId || 'Assigning sequence...') + '</span>' +
        '<span class="nrg-tag is-muted">' + LOCK + 'Read-only</span></div></div>';

      h += '<div class="nrg-cred-card">' +
        '<div class="nrg-cred-row"><span class="nrg-cred-label">Assigned Username</span>' + statusTag() + '</div>' +
        '<input class="nrg-input nrg-mono" type="text" id="nrg-username" aria-label="Assigned username" ' +
        'placeholder="username" value="' + esc(form.username) + '"></div>';
      h += '</div>';

      h += '<div class="nrg-pass-box">' +
        '<div class="nrg-cred-row"><span class="nrg-cred-label">Initial Temporary Password</span>' +
        '<button type="button" class="nrg-link" id="nrg-regen" data-nrg-regen>' + REFRESH + 'Regenerate</button></div>' +
        '<div class="nrg-pass-row">' +
        '<input class="nrg-input nrg-mono" type="' + (form.showPassword ? 'text' : 'password') +
        '" id="nrg-password" aria-label="Initial temporary password" value="' + esc(form.temporaryPassword) + '">' +
        '<button type="button" class="nrg-link" id="nrg-toggle-pass" data-nrg-toggle-pass>' + EYE +
        (form.showPassword ? 'Hide' : 'Show') + '</button></div>' +
        '<div class="nrg-hint" style="margin-top:8px">Stored as a salted PBKDF2 hash. The user must change it on first sign-in.</div>' +
        '</div>';

      var recipient = form.email || (form.username ? '@' + form.username : 'the new user');
      h += '<label class="nrg-check"><input type="checkbox" id="nrg-dispatch"' + (form.dispatch ? ' checked' : '') + '>' +
        '<span>Dispatch welcome packet and login credentials to <span class="nrg-strong" id="nrg-dispatch-to">' +
        esc(recipient) + '</span></span></label>';
      return h + '</div>';
    }

    // ── step 3: review & create ──────────────────────────────────────────
    function reviewRow(label, value, mono) {
      if (!value) return '';
      return '<div class="nrg-review-row"><span class="nrg-review-label">' + esc(label) + '</span>' +
        '<span class="nrg-review-value' + (mono ? ' nrg-mono' : '') + '">' + esc(value) + '</span></div>';
    }

    function pane3() {
      var h = paneOpen(3) + sectionHead('Review Registration', 'Nothing is created until you confirm');
      h += '<div class="nrg-review-card">';
      h += '<div class="nrg-summary-head"><span class="nrg-avatar">' + esc(initials()) + '</span>' +
        '<div><div class="nrg-summary-label">New ' + esc(roleTitle) + ' &mdash; ' + esc(form.accountType || ctx.accountType) + '</div>' +
        '<div class="nrg-summary-name">' + esc((form.firstName + ' ' + form.lastName).trim()) + '</div></div></div>';
      h += reviewRow('Institutional ID', form.institutionalId || 'Finalized on creation', true);
      h += reviewRow('Username', form.username ? '@' + form.username : '', true);
      h += reviewRow('Campus', form.campus);
      if (type === 'student') {
        h += reviewRow('Academic Year', form.academicYear);
        if (form.enrollments && form.enrollments.length > 0) {
          h += '<div class="nrg-review-enr-box">' +
            '<div class="nrg-review-enr-title">Academic Department Enrollments (' + form.enrollments.length + ')</div>' +
            '<div class="nrg-review-enr-table-wrap">' +
              '<table class="nrg-review-enr-table">' +
                '<thead><tr><th>Department</th><th>Grade</th><th>Class</th><th>Status</th></tr></thead>' +
                '<tbody>' +
                  form.enrollments.map(function (en) {
                    return '<tr>' +
                      '<td style="font-weight:500;color:var(--nrg-text);">' + esc(en.department) + '</td>' +
                      '<td>' + esc(en.grade) + '</td>' +
                      '<td class="nrg-mono" style="font-weight:500;color:var(--nrg-accent);">' + esc(en.class) + '</td>' +
                      '<td><span class="nrg-tag">' + esc(titleCase_(en.status || 'Active')) + '</span></td>' +
                    '</tr>';
                  }).join('') +
                '</tbody>' +
              '</table>' +
            '</div>' +
          '</div>';
        } else {
          h += reviewRow('Grade & Class', form.klass);
        }
        h += reviewRow('Enrollment Status', titleCase_(form.enrollmentStatus));
        h += reviewRow('Guardian', form.parentName);
      } else {
        h += reviewRow('Department', form.department);
        h += reviewRow('Position', form.position || (type === 'admin' ? form.scope : ''));
        if (type === 'teacher') {
          if (form.assignments && form.assignments.length > 0) {
            h += '<div class="nrg-review-enr-box">' +
              '<div class="nrg-review-enr-title">Teaching Assignments (' + form.assignments.length + ')</div>' +
              '<div class="nrg-review-enr-table-wrap">' +
                '<table class="nrg-review-enr-table">' +
                  '<thead><tr><th>Department</th><th>Grade</th><th>Class</th><th>Subject</th></tr></thead>' +
                  '<tbody>' +
                    form.assignments.map(function (as) {
                      return '<tr>' +
                        '<td style="font-weight:500;color:var(--nrg-text);">' + esc(as.department) + '</td>' +
                        '<td>' + esc(as.grade) + '</td>' +
                        '<td class="nrg-mono" style="font-weight:500;color:var(--nrg-accent);">' + esc(as.class) + '</td>' +
                        '<td>' + esc(as.subject) + '</td>' +
                      '</tr>';
                    }).join('') +
                  '</tbody>' +
                '</table>' +
              '</div>' +
            '</div>';
          } else {
            h += reviewRow('Subjects', (Array.isArray(form.subjects) ? form.subjects.join(', ') : form.subjects || ''));
          }
          h += reviewRow('Initial Status', titleCase_(form.status));
        }
        if (type === 'principal' || type === 'admin') h += reviewRow('Access Scope', form.scope);
      }
      h += reviewRow('Contact Email', form.email);
      h += '</div>';
      h += '<div class="nrg-review-note">The institutional profile and login account are created together — the temporary password is stored only as a salted PBKDF2 hash and must be changed at first sign-in.</div>';
      return h + '</div>';
    }

    function titleCase_(s) {
      return String(s == null ? '' : s).replace(/_/g, ' ').replace(/\b\w/g, function (c) { return c.toUpperCase(); });
    }

    // ── success view ─────────────────────────────────────────────────────
    function initials() {
      return ((form.firstName || '').charAt(0) + (form.lastName || '').charAt(0)).toUpperCase() || 'NG';
    }

    function copyBtn(value, label) {
      return '<button type="button" class="nrg-copy" data-nrg-copy="' + esc(value) + '">' + esc(label) + '</button>';
    }

    function successHtml() {
      var res = created || {};
      var fullName = (form.firstName + ' ' + form.lastName).trim();
      var instId = res.institutional_id || form.institutionalId || '';
      var uname = res.username || form.username || '';
      var pwd = res.temporary_password || form.temporaryPassword || '';

      var h = '<div class="nrg-success">' +
        '<div class="nrg-check-ring"><svg viewBox="0 0 52 52" aria-hidden="true">' +
        '<circle class="nrg-check-circle" cx="26" cy="26" r="23"/>' +
        '<path class="nrg-check-mark" d="M14 27l8 8 16-16"/></svg></div>' +
        '<h3 class="nrg-success-title">' + esc(roleTitle) + ' Account Created Successfully!</h3>' +
        '<p class="nrg-success-sub">The institutional profile and sign-in credentials were created and synchronized across school management pages.</p>' +
        '<div class="nrg-summary">' +
          '<div class="nrg-summary-head"><span class="nrg-avatar">' + esc(initials()) + '</span>' +
            '<div><div class="nrg-summary-label">' + esc(roleTitle) + ' Name</div>' +
            '<div class="nrg-summary-name">' + esc(fullName) + '</div></div></div>' +
          '<div class="nrg-summary-grid">' +
            '<div class="nrg-summary-item"><span class="nrg-cred-label">Institutional ID</span>' +
              '<span class="nrg-cred-value nrg-mono">' + esc(instId) + '</span>' + copyBtn(instId, 'Copy') + '</div>' +
            '<div class="nrg-summary-item"><span class="nrg-cred-label">Username</span>' +
              '<span class="nrg-cred-value nrg-mono">@' + esc(uname) + '</span>' + copyBtn(uname, 'Copy') + '</div>' +
            '<div class="nrg-summary-item nrg-span-2" style="grid-column:1/-1">' +
              '<span class="nrg-cred-label">Initial Temporary Password (shown once)</span>' +
              '<span class="nrg-cred-value nrg-mono">' + esc(pwd) + '</span>' + copyBtn(pwd, 'Copy') + '</div>' +
          '</div>' +
        '</div>' +
        '<div class="nrg-actions">' +
          (cfg.fallbackUrl && (res.institutional_id || form.institutionalId)
            ? '<button type="button" class="nrg-btn nrg-btn-outline" data-nrg-profile>View ' + esc(roleTitle) + ' Profile</button>'
            : '') +
          '<button type="button" class="nrg-btn nrg-btn-quiet" data-nrg-close>Back to Directory</button>' +
          '<button type="button" class="nrg-btn nrg-btn-primary" data-nrg-view>Go to ' + esc(roleTitle) + ' Directory</button>' +
        '</div></div>';
      return h;
    }

    // ── footer ───────────────────────────────────────────────────────────
    function footerHtml() {
      if (step === 4) return '';
      var back = step === 1
        ? '<button type="button" class="nrg-btn nrg-btn-quiet" data-nrg-cancel' + (busy ? ' disabled' : '') + '>Cancel</button>'
        : '<button type="button" class="nrg-btn nrg-btn-quiet" data-nrg-back' + (busy ? ' disabled' : '') + '>&larr; Back</button>';
      var label = step === 1 ? 'Continue to Credentials' :
        (step === 2 ? 'Continue to Review' : 'Create ' + roleTitle + ' Account');
      var primary = '<button type="button" class="nrg-btn nrg-btn-primary" data-nrg-primary' +
        (busy ? ' disabled' : '') + '>' +
        (busy ? '<span class="nrg-spinner" aria-hidden="true"></span><span>' + esc(busyLabel) + '</span>'
              : '<span>' + esc(label) + '</span>') +
        '</button>';
      return back + primary;
    }

    function renderFooter() { foot.innerHTML = footerHtml(); }

    function setBusy(isBusy, label) {
      busy = !!isBusy;
      busyLabel = label || '';
      var pane = q(shell, '.nrg-pane');
      if (pane) pane.setAttribute('aria-busy', busy ? 'true' : 'false');
      shell.setAttribute('aria-busy', busy ? 'true' : 'false');
      renderFooter();
    }

    // ── data ─────────────────────────────────────────────────────────────
    function loadOptions(done) {
      ctx.fetchJson('/api/user-mgmt/form-options?type=' + encodeURIComponent(type))
        .then(function (j) {
          if (j && j.success) {
            opts.campuses = j.campuses || [];
            opts.departments = j.departments || [];
            opts.classes = j.classes || [];
            opts.grades = j.grades || [];
            opts.subjects = j.subjects || [];
            opts.positions = j.positions || [];
            opts.department_structure = j.department_structure || {};
            opts.dept_subjects_map = j.dept_subjects_map || {};
            opts.subjects_by_department = j.subjects_by_department || {};
            opts.academic_years = j.academic_years || opts.academic_years;
            if (!form.campus && opts.campuses.length) form.campus = opts.campuses[0];
            if (!form.department && opts.departments.length) form.department = opts.departments[0];
            if (!form.klass && opts.classes.length) {
              var c = opts.classes[0];
              form.klass = (c && (c.short || c.name)) || '';
            }
            if (!form.position && opts.positions.length) {
              var p = opts.positions[0];
              form.position = (p && (p.short || p.name)) || p || '';
            }
            if (type === 'student') {
              if (!form.enrollments || !form.enrollments.length) {
                var initialDept = (opts.departments && opts.departments[0]) || 'Khmer Studies Department';
                var initialGrades = getDepartmentGrades(initialDept);
                var initialG = initialGrades[0] || '12';
                var initialClasses = getDepartmentClasses(initialDept, initialG);
                form.enrollments = [{
                  id: 'enr-init-1',
                  department: initialDept,
                  grade: 'Grade ' + initialG,
                  class: initialClasses[0] ? initialClasses[0].short : '12A',
                  classId: initialClasses[0] ? initialClasses[0].id : '',
                  status: 'active'
                }];
                form.department = initialDept;
                form.klass = form.enrollments[0].class;
              }
            }
            if (type === 'teacher') {
              if (!form.assignments || !form.assignments.length) {
                var tDept = (opts.departments && opts.departments[0]) || 'Khmer Studies Department';
                var tGrades = getDepartmentGrades(tDept);
                var tG = tGrades[0] || '12';
                var tClasses = getDepartmentClasses(tDept, tG);
                var tSubjs = getDepartmentSubjects(tDept);
                var tSubj = tSubjs[0] ? (typeof tSubjs[0] === 'object' ? (tSubjs[0].name || tSubjs[0].id) : tSubjs[0]) : 'Khmer Literature';
                var tSubjId = tSubjs[0] && typeof tSubjs[0] === 'object' ? tSubjs[0].id : '';
                form.assignments = [{
                  id: 'asgn-init-1',
                  department: tDept,
                  grade: 'Grade ' + tG,
                  class: tClasses[0] ? tClasses[0].short : '12A',
                  classId: tClasses[0] ? tClasses[0].id : '',
                  subject: tSubj,
                  subjectId: tSubjId
                }];
                form.department = tDept;
                form.klass = form.assignments[0].class;
                form.subjects = [tSubj];
              }
            }
          }
        })
        .catch(function () { /* offline: fall back to built-in option lists */ })
        .then(function () { if (done) done(); });
    }

    function generateCredentials(done) {
      setBusy(true, 'Preparing Credentials...');
      var url = '/api/user-mgmt/generate-credentials?type=' + encodeURIComponent(type) +
        '&first_name=' + encodeURIComponent(form.firstName.trim()) +
        '&last_name=' + encodeURIComponent(form.lastName.trim());
      ctx.fetchJson(url).then(function (res) {
        if (res && res.success) {
          form.institutionalId = res.institutional_id || '';
          if (!form.usernameEdited || !form.username) form.username = res.username || '';
          if (!form.temporaryPassword) form.temporaryPassword = res.temporary_password || '';
          form.accountType = res.account_type || ctx.accountType;
        }
      }).catch(function () {
        form.error = 'Could not generate institutional credentials. Check your connection and try again.';
        form.errorRetry = true;
      }).then(function () {
        setBusy(false, '');
        if (done) done();
      });
    }

    function updateUsernameStatus() {
      var tag = q(shell, '#nrg-username-status');
      if (!tag) return;
      tag.className = 'nrg-tag ' + (form.usernameChecking ? 'is-muted' : (form.usernameValid ? '' : 'is-bad'));
      tag.innerHTML = (form.usernameValid && !form.usernameChecking ? CHECK : '') +
        esc(form.usernameMessage || (form.usernameValid ? 'Available' : 'Invalid format'));
    }

    function checkUsername(val) {
      var seq = ++checkSeq;
      if (!val || !/^[a-z0-9][a-z0-9._@-]{2,39}$/.test(val)) {
        form.usernameValid = false;
        form.usernameChecking = false;
        form.usernameMessage = 'Invalid username format';
        updateUsernameStatus();
        return;
      }
      form.usernameChecking = true;
      form.usernameMessage = 'Checking...';
      updateUsernameStatus();
      ctx.fetchJson('/api/user-mgmt/check-username?username=' + encodeURIComponent(val))
        .then(function (res) {
          if (seq !== checkSeq) return; // stale response must not overwrite newer input
          form.usernameChecking = false;
          form.usernameValid = !!(res && res.available);
          form.usernameMessage = form.usernameValid ? 'Available' : 'Username taken';
          updateUsernameStatus();
        })
        .catch(function () {
          if (seq !== checkSeq) return;
          form.usernameChecking = false;
          form.usernameValid = false;
          form.usernameMessage = 'Could not verify';
          updateUsernameStatus();
        });
    }

    function readInputs() {
      function val(id) { var el = q(shell, '#' + id); return el ? el.value.trim() : null; }
      if (step === 1) {
        var v, x;
        // personal identity
        if ((v = val('nrg-first')) !== null) form.firstName = v;
        if ((v = val('nrg-last')) !== null) form.lastName = v;
        if ((v = val('nrg-khmer')) !== null) form.khmerName = v;
        var g = q(shell, 'input[name="nrg-gender"]:checked'); if (g) form.gender = g.value;
        if ((v = val('nrg-dob')) !== null) form.dob = v;
        if ((v = val('nrg-email')) !== null) form.email = v;
        if ((v = val('nrg-phone')) !== null) form.phone = v;
        if ((v = val('nrg-photo')) !== null) form.photo = v;
        // institutional placement (same pane)
        if ((x = val('nrg-campus')) !== null) form.campus = x;
        if ((x = val('nrg-year')) !== null) form.academicYear = x;
        if ((x = val('nrg-dept')) !== null) form.department = x;
        if ((x = val('nrg-class')) !== null) form.klass = x;
        if ((x = val('nrg-enroll')) !== null) form.enrollmentStatus = x;
        if ((x = val('nrg-parent')) !== null) form.parentName = x;
        if ((x = val('nrg-parent-contact')) !== null) form.parentContact = x;
        if ((x = val('nrg-position')) !== null) form.position = x;
        if ((x = val('nrg-status')) !== null) form.status = x;
        if ((x = val('nrg-scope')) !== null) form.scope = x;
        if ((x = val('nrg-subjects')) !== null) form.subjects = x.split(',').map(function (s) { return s.trim(); }).filter(Boolean);

        // Read dynamic academic department enrollments for student
        if (type === 'student') {
          Array.prototype.forEach.call(shell.querySelectorAll('.nrg-enr-card'), function (card, idx) {
            if (!form.enrollments[idx]) return;
            var dSel = card.querySelector('.nrg-enr-dept-select');
            if (dSel) form.enrollments[idx].department = dSel.value;
            var gSel = card.querySelector('.nrg-enr-grade-select');
            if (gSel) form.enrollments[idx].grade = gSel.value;
            var cSel = card.querySelector('.nrg-enr-class-select');
            if (cSel) {
              form.enrollments[idx].class = cSel.value;
              var opt = cSel.options[cSel.selectedIndex];
              form.enrollments[idx].classId = (opt && opt.getAttribute('data-cid')) || '';
            }
          });
          if (form.enrollments.length > 0) {
            form.department = form.enrollments[0].department;
            form.klass = form.enrollments[0].class;
          }
        }

        // Read dynamic teaching assignments for teacher
        if (type === 'teacher') {
          Array.prototype.forEach.call(shell.querySelectorAll('.nrg-asgn-card'), function (card, idx) {
            if (!form.assignments[idx]) return;
            var dSel = card.querySelector('.nrg-asgn-dept-select');
            if (dSel) form.assignments[idx].department = dSel.value;
            var gSel = card.querySelector('.nrg-asgn-grade-select');
            if (gSel) form.assignments[idx].grade = gSel.value;
            var cSel = card.querySelector('.nrg-asgn-class-select');
            if (cSel) {
              form.assignments[idx].class = cSel.value;
              var cOpt = cSel.options[cSel.selectedIndex];
              form.assignments[idx].classId = (cOpt && cOpt.getAttribute('data-cid')) || '';
            }
            var sSel = card.querySelector('.nrg-asgn-subj-select');
            if (sSel) {
              form.assignments[idx].subject = sSel.value;
              var sOpt = sSel.options[sSel.selectedIndex];
              form.assignments[idx].subjectId = (sOpt && sOpt.getAttribute('data-sid')) || '';
            }
          });
          if (form.assignments.length > 0) {
            form.department = form.assignments[0].department;
            form.klass = form.assignments[0].class;
            var subjs = [];
            form.assignments.forEach(function (a) {
              if (a.subject && subjs.indexOf(a.subject) === -1) subjs.push(a.subject);
            });
            if (subjs.length) form.subjects = subjs;
          }
        }
      } else if (step === 2) {
        var u = val('nrg-username'); if (u !== null) form.username = u.toLowerCase();
        var p = q(shell, '#nrg-password'); if (p) form.temporaryPassword = p.value;
        var d = q(shell, '#nrg-dispatch'); if (d) form.dispatch = d.checked;
      }
      // step 3 (Review) is read-only — no inputs
    }

    function validate() {
      form.error = '';
      form.errorRetry = false;
      readInputs();
      if (step === 1) {
        // personal identity
        if (!form.firstName) { form.error = 'First name is required.'; return false; }
        if (!form.lastName) { form.error = 'Last name is required.'; return false; }
        if (!form.email) { form.error = 'Contact email is required.'; return false; }
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) { form.error = 'Email address format is invalid.'; return false; }
        // institutional placement
        if (!form.campus) { form.error = 'Campus assignment is required.'; return false; }
        if (type === 'student') {
          if (!form.enrollments || form.enrollments.length === 0) {
            form.error = 'At least one academic department enrollment is required.';
            return false;
          }
          var seenDepts = {};
          for (var i = 0; i < form.enrollments.length; i++) {
            var en = form.enrollments[i];
            if (!en.department || !en.grade || !en.class) {
              form.error = 'Please complete Department, Grade, and Class for Enrollment ' + (i + 1) + '.';
              return false;
            }
            if (seenDepts[en.department]) {
              form.error = 'Duplicate department enrollment: "' + en.department + '" cannot be added multiple times for the same student.';
              return false;
            }
            seenDepts[en.department] = true;
          }
        }
        if (type === 'teacher') {
          if (!form.department || !form.position) {
            form.error = 'Department and Position are required for faculty registration.';
            return false;
          }
          if (!form.assignments || form.assignments.length === 0) {
            form.error = 'At least one teaching assignment is required.';
            return false;
          }
          var seenAssignments = {};
          for (var tIdx = 0; tIdx < form.assignments.length; tIdx++) {
            var asgn = form.assignments[tIdx];
            if (!asgn.department || !asgn.grade || !asgn.class || !asgn.subject) {
              form.error = 'Please complete Department, Grade, Class, and Subject for Teaching Assignment ' + (tIdx + 1) + '.';
              return false;
            }
            var asgnKey = (asgn.department + '::' + asgn.class + '::' + asgn.subject).toLowerCase();
            if (seenAssignments[asgnKey]) {
              form.error = 'Duplicate assignment: Class "' + asgn.class + '" with Subject "' + asgn.subject + '" is already assigned in ' + asgn.department + '.';
              return false;
            }
            seenAssignments[asgnKey] = true;
          }
        }
        if (type === 'staff' && (!form.department || !form.position)) { form.error = 'Department and Position are required for staff registration.'; return false; }
        if (type === 'principal' && !form.position) { form.error = 'Leadership Position is required for principal registration.'; return false; }
        if (type === 'admin' && !form.position) { form.error = 'Administrative Position is required for administrator registration.'; return false; }
      } else if (step === 2) {
        if (!form.username) { form.error = 'Username is required.'; return false; }
        if (!/^[a-z0-9][a-z0-9._@-]{2,39}$/.test(form.username)) { form.error = 'Username must be 3-40 lowercase letters, digits, dots, or dashes.'; return false; }
        if (form.usernameChecking) { form.error = 'Username availability is still being checked.'; return false; }
        if (!form.usernameValid) { form.error = form.usernameMessage || 'Please choose an available username.'; return false; }
        if (!form.temporaryPassword || form.temporaryPassword.length < 8) { form.error = 'Temporary password must be at least 8 characters long.'; return false; }
      }
      // step 3 (Review) — everything already validated
      return true;
    }

    function payload() {
      var p = {
        person_type: type,
        first_name: form.firstName.trim(),
        last_name: form.lastName.trim(),
        khmer_name: form.khmerName.trim(),
        gender: form.gender,
        dob: form.dob,
        email: form.email.trim() || null,
        phone: form.phone.trim() || null,
        photo: form.photo.trim() || null,
        campus: form.campus,
        academic_year: form.academicYear,
        class: form.klass,
        enrollment_status: form.enrollmentStatus,
        parent_name: form.parentName.trim(),
        parent_email: form.parentContact && form.parentContact.indexOf('@') >= 0 ? form.parentContact.trim() : null,
        parent_phone: form.parentContact && form.parentContact.indexOf('@') < 0 ? form.parentContact.trim() : null,
        department: form.department,
        position: form.position,
        subjects: Array.isArray(form.subjects) ? form.subjects : (form.subjects ? [form.subjects] : []),
        scope: form.scope,
        institutional_id: form.institutionalId,
        username: form.username.trim().toLowerCase(),
        temporary_password: form.temporaryPassword,
        activation: 'password',
        dispatch_welcome: !!form.dispatch
      };
      if (type === 'student' && form.enrollments && form.enrollments.length > 0) {
        p.enrollments = form.enrollments.map(function (e) {
          return {
            department: e.department,
            grade: e.grade,
            class: e.class,
            class_id: e.classId || '',
            status: e.status || form.enrollmentStatus || 'active',
            academic_year: form.academicYear || '2025-26'
          };
        });
        p.class = form.enrollments[0].class;
        p.grade = form.enrollments[0].grade;
        p.department = form.enrollments[0].department;
      }
      if (type === 'teacher' && form.assignments && form.assignments.length > 0) {
        p.assignments = form.assignments.map(function (a) {
          return {
            department: a.department,
            grade: a.grade,
            class: a.class,
            class_id: a.classId || '',
            subject: a.subject,
            subject_id: a.subjectId || ''
          };
        });
        p.class = form.assignments[0].class;
        p.department = form.assignments[0].department;
        var distinctSubjs = [];
        form.assignments.forEach(function (a) {
          if (a.subject && distinctSubjs.indexOf(a.subject) === -1) distinctSubjs.push(a.subject);
        });
        if (distinctSubjs.length) p.subjects = distinctSubjs;
      }
      return p;
    }

    function submit() {
      setBusy(true, 'Creating Account...');
      ctx.postJson('/api/user-mgmt/create-person', payload()).then(function (res) {
        setBusy(false, '');
        if (res && res.success) {
          created = res;
          step = 4;
          render();
          if (ctx.fetchDirectory) ctx.fetchDirectory();
        } else {
          form.error = (res && res.error) || 'Failed to create account. Please review the details and try again.';
          form.errorRetry = true;
          render();
        }
      }).catch(function (err) {
        setBusy(false, '');
        form.error = (err && err.payload && err.payload.error) ||
          (err && err.message) || 'Error creating account. Please try again.';
        form.errorRetry = true;
        render();
      });
    }

    // ── render / wire ────────────────────────────────────────────────────
    function render() {
      var changed = step !== lastStep;
      lastStep = step;
      wrap.classList.toggle('nrg-success-mode', step === 4);
      if (footWrap) footWrap.style.display = step === 4 ? 'none' : '';
      if (step === 4) {
        shell.innerHTML = successHtml();
      } else {
        shell.innerHTML = stepperHtml() + errorHtml() +
          (step === 1 ? pane1() : (step === 2 ? pane2() : pane3()));
      }
      renderFooter();
      wire();
      if (changed && !busy && step < 4) {
        var first = shell.querySelector('.nrg-pane input:not([type="radio"]):not([type="checkbox"]), .nrg-pane select');
        if (first) { try { first.focus({ preventScroll: true }); } catch (e) { first.focus(); } }
      }
    }

    function wire() {
      // Stepper: completed steps are navigable
      Array.prototype.forEach.call(shell.querySelectorAll('[data-nrg-step]'), function (btn) {
        btn.onclick = function () {
          var n = parseInt(btn.getAttribute('data-nrg-step'), 10);
          if (busy || n >= step) return;
          readInputs();
          form.error = '';
          step = n;
          render();
        };
      });

      var primary = q(foot, '[data-nrg-primary]');
      if (primary) {
        primary.onclick = function () {
          if (busy) return;
          if (!validate()) { render(); return; }
          if (step === 1) {
            form.error = '';
            step = 2;
            render();
            generateCredentials(function () { render(); });
          } else if (step === 2) {
            form.error = '';
            step = 3;
            render();
          } else {
            submit();
          }
        };
      }

      var back = q(foot, '[data-nrg-back]');
      if (back) back.onclick = function () {
        if (busy) return;
        readInputs(); form.error = ''; step -= 1; render();
      };
      var cancel = q(foot, '[data-nrg-cancel]');
      if (cancel) cancel.onclick = function () { if (!busy) ctx.closeModal(true); };

      var dismiss = q(shell, '[data-nrg-error-dismiss]');
      if (dismiss) dismiss.onclick = function () { form.error = ''; form.errorRetry = false; render(); };
      var retry = q(shell, '[data-nrg-retry]');
      if (retry) retry.onclick = function () { form.error = ''; form.errorRetry = false; render(); submit(); };

      // Gender segmented control
      Array.prototype.forEach.call(shell.querySelectorAll('input[name="nrg-gender"]'), function (radio) {
        radio.onchange = function () {
          form.gender = radio.value;
          Array.prototype.forEach.call(shell.querySelectorAll('.nrg-segment'), function (seg) {
            seg.classList.toggle('is-selected', !!seg.querySelector('input:checked'));
          });
        };
      });

      // Multi-Department Academic Enrollment controls for students
      if (type === 'student' && step === 1) {
        // Department select change: cascade resets grade and class
        Array.prototype.forEach.call(shell.querySelectorAll('.nrg-enr-dept-select'), function (sel) {
          sel.onchange = function () {
            var idx = parseInt(sel.getAttribute('data-enr-idx'), 10);
            readInputs();
            if (form.enrollments[idx]) {
              var newDept = sel.value;
              form.enrollments[idx].department = newDept;
              var validGrades = getDepartmentGrades(newDept);
              var firstG = validGrades[0] || '10';
              form.enrollments[idx].grade = 'Grade ' + firstG;
              var validClasses = getDepartmentClasses(newDept, firstG);
              form.enrollments[idx].class = validClasses[0] ? validClasses[0].short : '';
              form.enrollments[idx].classId = validClasses[0] ? validClasses[0].id : '';
            }
            render();
          };
        });

        // Grade select change: cascade resets class
        Array.prototype.forEach.call(shell.querySelectorAll('.nrg-enr-grade-select'), function (sel) {
          sel.onchange = function () {
            var idx = parseInt(sel.getAttribute('data-enr-idx'), 10);
            readInputs();
            if (form.enrollments[idx]) {
              var newGrade = sel.value;
              form.enrollments[idx].grade = newGrade;
              var gNum = newGrade.replace('Grade ', '').trim();
              var validClasses = getDepartmentClasses(form.enrollments[idx].department, gNum);
              form.enrollments[idx].class = validClasses[0] ? validClasses[0].short : '';
              form.enrollments[idx].classId = validClasses[0] ? validClasses[0].id : '';
            }
            render();
          };
        });

        // Class select change: updates class & classId
        Array.prototype.forEach.call(shell.querySelectorAll('.nrg-enr-class-select'), function (sel) {
          sel.onchange = function () {
            var idx = parseInt(sel.getAttribute('data-enr-idx'), 10);
            if (form.enrollments[idx]) {
              form.enrollments[idx].class = sel.value;
              var opt = sel.options[sel.selectedIndex];
              form.enrollments[idx].classId = (opt && opt.getAttribute('data-cid')) || '';
            }
          };
        });

        // Remove enrollment button
        Array.prototype.forEach.call(shell.querySelectorAll('[data-enr-remove]'), function (btn) {
          btn.onclick = function () {
            var idx = parseInt(btn.getAttribute('data-enr-remove'), 10);
            readInputs();
            if (form.enrollments.length > 1) {
              form.enrollments.splice(idx, 1);
              render();
            }
          };
        });

        // Add Another Department button
        var addDeptBtn = q(shell, '#nrg-add-dept-btn');
        if (addDeptBtn) {
          addDeptBtn.onclick = function () {
            readInputs();
            var chosenDepts = form.enrollments.map(function (e) { return e.department; });
            var nextDept = (opts.departments || []).find(function (d) {
              var dName = typeof d === 'object' ? (d.name || d.short) : d;
              return chosenDepts.indexOf(dName) === -1;
            });
            if (!nextDept) {
              nextDept = (opts.departments && opts.departments[0]) || 'English Department';
            }
            var nextDeptName = typeof nextDept === 'object' ? (nextDept.name || nextDept.short) : nextDept;
            var validGrades = getDepartmentGrades(nextDeptName);
            var firstG = validGrades[0] || '10';
            var validClasses = getDepartmentClasses(nextDeptName, firstG);
            form.enrollments.push({
              id: 'enr-' + Date.now(),
              department: nextDeptName,
              grade: 'Grade ' + firstG,
              class: validClasses[0] ? validClasses[0].short : '',
              classId: validClasses[0] ? validClasses[0].id : '',
              status: 'active'
            });
            render();
          };
        }
      }

      // Multi-Class & Multi-Department Teaching Assignment controls for teachers
      if (type === 'teacher' && step === 1) {
        // Department select change: cascade resets grade, class, and subjects
        Array.prototype.forEach.call(shell.querySelectorAll('.nrg-asgn-dept-select'), function (sel) {
          sel.onchange = function () {
            var idx = parseInt(sel.getAttribute('data-asgn-idx'), 10);
            readInputs();
            if (form.assignments[idx]) {
              var newDept = sel.value;
              form.assignments[idx].department = newDept;
              var validGrades = getDepartmentGrades(newDept);
              var firstG = validGrades[0] || '12';
              form.assignments[idx].grade = 'Grade ' + firstG;
              var validClasses = getDepartmentClasses(newDept, firstG);
              form.assignments[idx].class = validClasses[0] ? validClasses[0].short : '';
              form.assignments[idx].classId = validClasses[0] ? validClasses[0].id : '';
              var validSubjs = getDepartmentSubjects(newDept);
              var firstSubj = validSubjs[0] ? (typeof validSubjs[0] === 'object' ? (validSubjs[0].name || validSubjs[0].id) : validSubjs[0]) : 'General';
              form.assignments[idx].subject = firstSubj;
              form.assignments[idx].subjectId = validSubjs[0] && typeof validSubjs[0] === 'object' ? validSubjs[0].id : '';
            }
            render();
          };
        });

        // Grade select change: cascade resets class
        Array.prototype.forEach.call(shell.querySelectorAll('.nrg-asgn-grade-select'), function (sel) {
          sel.onchange = function () {
            var idx = parseInt(sel.getAttribute('data-asgn-idx'), 10);
            readInputs();
            if (form.assignments[idx]) {
              var newGrade = sel.value;
              form.assignments[idx].grade = newGrade;
              var gNum = newGrade.replace('Grade ', '').trim();
              var validClasses = getDepartmentClasses(form.assignments[idx].department, gNum);
              form.assignments[idx].class = validClasses[0] ? validClasses[0].short : '';
              form.assignments[idx].classId = validClasses[0] ? validClasses[0].id : '';
            }
            render();
          };
        });

        // Class select change: updates class & classId
        Array.prototype.forEach.call(shell.querySelectorAll('.nrg-asgn-class-select'), function (sel) {
          sel.onchange = function () {
            var idx = parseInt(sel.getAttribute('data-asgn-idx'), 10);
            if (form.assignments[idx]) {
              form.assignments[idx].class = sel.value;
              var opt = sel.options[sel.selectedIndex];
              form.assignments[idx].classId = (opt && opt.getAttribute('data-cid')) || '';
            }
          };
        });

        // Subject select change: updates subject & subjectId
        Array.prototype.forEach.call(shell.querySelectorAll('.nrg-asgn-subj-select'), function (sel) {
          sel.onchange = function () {
            var idx = parseInt(sel.getAttribute('data-asgn-idx'), 10);
            if (form.assignments[idx]) {
              form.assignments[idx].subject = sel.value;
              var opt = sel.options[sel.selectedIndex];
              form.assignments[idx].subjectId = (opt && opt.getAttribute('data-sid')) || '';
            }
          };
        });

        // Remove assignment button
        Array.prototype.forEach.call(shell.querySelectorAll('[data-asgn-remove]'), function (btn) {
          btn.onclick = function () {
            var idx = parseInt(btn.getAttribute('data-asgn-remove'), 10);
            readInputs();
            if (form.assignments.length > 1) {
              form.assignments.splice(idx, 1);
              render();
            }
          };
        });

        // Add Another Class button
        var addClassBtn = q(shell, '#nrg-add-class-btn');
        if (addClassBtn) {
          addClassBtn.onclick = function () {
            readInputs();
            var prevDept = (form.assignments.length && form.assignments[form.assignments.length - 1].department) ||
                           (opts.departments && opts.departments[0]) || 'Khmer Studies Department';
            var validGrades = getDepartmentGrades(prevDept);
            var firstG = validGrades[0] || '12';
            var validClasses = getDepartmentClasses(prevDept, firstG);
            var validSubjs = getDepartmentSubjects(prevDept);
            var prevSubj = (form.assignments.length && form.assignments[form.assignments.length - 1].subject) ||
                           (validSubjs[0] ? (typeof validSubjs[0] === 'object' ? (validSubjs[0].name || validSubjs[0].id) : validSubjs[0]) : 'General');
            var firstSubjId = validSubjs[0] && typeof validSubjs[0] === 'object' ? validSubjs[0].id : '';

            // Pick a class section not yet assigned for this department & subject
            var curClass = validClasses[0] ? validClasses[0].short : '';
            var curClassId = validClasses[0] ? validClasses[0].id : '';
            for (var ci = 0; ci < validClasses.length; ci++) {
              var candidateCode = validClasses[ci].short;
              var isUsed = form.assignments.some(function (a) {
                return a.department === prevDept && a.class === candidateCode && a.subject === prevSubj;
              });
              if (!isUsed) {
                curClass = candidateCode;
                curClassId = validClasses[ci].id;
                break;
              }
            }

            form.assignments.push({
              id: 'asgn-' + Date.now() + '-' + Math.random().toString(36).substr(2, 4),
              department: prevDept,
              grade: 'Grade ' + firstG,
              class: curClass,
              classId: curClassId,
              subject: prevSubj,
              subjectId: firstSubjId
            });
            render();
          };
        }
      }

      // Credentials step controls
      var un = q(shell, '#nrg-username');
      if (un) un.oninput = function () {
        form.usernameEdited = true;
        form.username = un.value.trim().toLowerCase();
        clearTimeout(checkTimer);
        checkTimer = setTimeout(function () { checkUsername(form.username); }, 280);
      };
      var regen = q(shell, '#nrg-regen');
      if (regen) regen.onclick = function () {
        if (busy) return;
        form.temporaryPassword = '';
        ctx.fetchJson('/api/user-mgmt/generate-credentials?type=' + encodeURIComponent(type) +
          '&first_name=' + encodeURIComponent(form.firstName.trim()) +
          '&last_name=' + encodeURIComponent(form.lastName.trim()))
          .then(function (res) {
            if (res && res.success) form.temporaryPassword = res.temporary_password || '';
            var pw = q(shell, '#nrg-password'); if (pw) pw.value = form.temporaryPassword;
          }).catch(function () {
            form.error = 'Could not regenerate the temporary password.';
            render();
          });
      };
      var toggle = q(shell, '#nrg-toggle-pass');
      if (toggle) toggle.onclick = function () {
        form.showPassword = !form.showPassword;
        var pw = q(shell, '#nrg-password');
        if (pw) pw.type = form.showPassword ? 'text' : 'password';
        toggle.innerHTML = EYE + (form.showPassword ? 'Hide' : 'Show');
      };

      // Success actions
      Array.prototype.forEach.call(shell.querySelectorAll('[data-nrg-copy]'), function (btn) {
        btn.onclick = function () {
          var value = btn.getAttribute('data-nrg-copy') || '';
          try {
            if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(value);
          } catch (e) {}
          btn.textContent = 'Copied';
        };
      });
      var close = q(shell, '[data-nrg-close]');
      if (close) close.onclick = function () { ctx.closeModal(true); };
      var profile = q(shell, '[data-nrg-profile]');
      if (profile) profile.onclick = function () {
        var id = (created && created.institutional_id) || form.institutionalId || '';
        ctx.closeModal(true);
        window.location.href = (cfg.fallbackUrl || '') + '?open-profile=' + encodeURIComponent(id);
      };
      var view = q(shell, '[data-nrg-view]');
      if (view) view.onclick = function () {
        ctx.closeModal(true);
        var uname = (created && created.username) || form.username;
        if (uname && ctx.state && ctx.root) {
          ctx.state.search = uname;
          var s = ctx.root.querySelector('[data-action="search"]');
          if (s) s.value = uname;
          if (ctx.fetchDirectory) ctx.fetchDirectory();
        }
      };
    }

    loadOptions(function () { render(); });
  };
})(window, document);
