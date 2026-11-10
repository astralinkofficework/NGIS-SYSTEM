/**
 * NGIS Data Dictionary Module Engine
 * Powers the 5 Data Dictionary sub-modules for Admin & Principal portals:
 * - School Data
 * - Student's Data
 * - Teacher's Data
 * - Additional Data
 * - Timetable's Data
 * 
 * Strict AGENTS.md compliance:
 * - NO BOLD FONTS (font-normal / font-medium only, max weight 500)
 * - Accessible controls, responsive tables, clear empty states & toast feedback.
 */

(function (window, document) {
  'use strict';

  var DD = window.DATA_DICT = window.DATA_DICT || {};

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function toast(msg, type) {
    var existing = document.getElementById('ddToast');
    if (existing) existing.remove();
    var t = document.createElement('div');
    t.id = 'ddToast';
    var bg = type === 'error' ? 'bg-rose-600' : (type === 'info' ? 'bg-slate-800' : 'bg-[#176B45]');
    t.className = 'fixed bottom-5 right-5 z-50 flex items-center gap-2.5 px-4 py-2.5 rounded-xl shadow-lg text-white text-xs font-medium transition-all transform translate-y-0 ' + bg;
    t.innerHTML = '<span class="material-symbols-outlined text-sm">' + (type === 'error' ? 'error' : 'check_circle') + '</span><span>' + esc(msg) + '</span>';
    document.body.appendChild(t);
    setTimeout(function () {
      t.classList.add('opacity-0', 'translate-y-2');
      setTimeout(function () { t.remove(); }, 300);
    }, 3200);
  }

  var SECTION_TITLES = {
    school: 'School Data Reference Schema',
    students: "Student's Data Reference Schema",
    teachers: "Teacher's Data Reference Schema",
    additional: 'Additional Data Reference Schema',
    timetable: "Timetable's Data Reference Schema"
  };

  var TABLE_PRETTY_NAMES = {
    campuses: 'Campus Locations & Branches',
    buildings: 'School Buildings & Facilities',
    departments: 'Academic Departments',
    gradeLevels: 'Grade Levels & Divisions',
    academicTerms: 'Academic Semesters & Terms',
    gradingScales: 'Official Grading Scales & GPA Bounds',
    enrollmentStatuses: 'Student Enrollment Statuses',
    admissionTypes: 'Admission & Matriculation Categories',
    identityDocumentTypes: 'Identity & Legal Document Types',
    exemptionCategories: 'Course & Exemption Dispensations',
    disciplinaryInfractions: 'Student Disciplinary Infractions',
    studentAwards: 'Student Commendation & Honor Categories',
    employmentTypes: 'Faculty Employment Classifications',
    facultyPositions: 'Faculty Academic Positions & Ranks',
    qualifications: 'Academic Degrees & Professional Licenses',
    effortCategories: 'Beyond-Classroom Effort Categories',
    disciplineCategories: 'Faculty Conduct & Compliance Codes',
    documentCategories: 'Institutional Document Types',
    supportedLanguages: 'Supported Instruction Languages',
    transitRoutes: 'Transportation & Campus Transit Routes',
    relationshipCodes: 'Guardian & Emergency Relationship Codes',
    auditEventTypes: 'System Audit Event Classifications',
    periodSlots: 'Bell Schedule Period Slots',
    instructionalDays: 'Instructional Week Days',
    roomTypes: 'Classroom & Facility Types',
    subjectTypes: 'Curriculum & Subject Classifications',
    schedulingConstraints: 'Timetable Scheduling Constraints & Rules'
  };

  DD.init = function (containerId, portalRole, defaultSection) {
    var root = document.getElementById(containerId);
    if (!root) return;

    var state = {
      section: defaultSection || 'school',
      tables: {},
      activeTable: null,
      items: [],
      search: '',
      loading: true
    };

    function loadSection(secName) {
      state.section = secName;
      state.loading = true;
      root.innerHTML = '<div class="flex items-center justify-center py-20 text-slate-400"><span class="w-2.5 h-2.5 rounded-full bg-[#176B45] animate-ping mr-2"></span><span class="text-xs font-medium">Loading ' + esc(SECTION_TITLES[secName] || secName) + '...</span></div>';

      fetch('/api/dictionary/section/' + encodeURIComponent(secName))
        .then(function (res) { return res.json(); })
        .then(function (res) {
          state.tables = res.tables || {};
          var keys = Object.keys(state.tables);
          state.activeTable = keys[0] || null;
          state.items = state.activeTable ? (state.tables[state.activeTable] || []) : [];
          state.loading = false;
          render();
        })
        .catch(function () {
          root.innerHTML = '<div class="p-6 text-center text-xs text-rose-600">Failed to load data dictionary section.</div>';
        });
    }

    function render() {
      var secKeys = ['school', 'students', 'teachers', 'additional', 'timetable'];
      var secLabels = {
        school: 'School Data',
        students: "Student's Data",
        teachers: "Teacher's Data",
        additional: 'Additional Data',
        timetable: "Timetable's Data"
      };

      // Navigation tabs across the 5 sections
      var secTabsHtml = secKeys.map(function (k) {
        var isAct = k === state.section;
        return '<button type="button" class="btn-sec-tab px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all cursor-pointer ' +
          (isAct ? 'bg-[#176B45] text-white shadow-2xs' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100') +
          '" data-section="' + k + '">' +
          esc(secLabels[k]) +
        '</button>';
      }).join('');

      // Pills for tables in current section
      var tableKeys = Object.keys(state.tables);
      var tablePillsHtml = tableKeys.map(function (tk) {
        var isAct = tk === state.activeTable;
        var count = (state.tables[tk] || []).length;
        var label = TABLE_PRETTY_NAMES[tk] || tk;
        return '<button type="button" class="btn-table-pill flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all cursor-pointer border ' +
          (isAct ? 'bg-emerald-50 text-[#176B45] border-emerald-300 shadow-2xs' : 'bg-white text-slate-600 border-slate-200 hover:border-slate-300') +
          '" data-table="' + tk + '">' +
          '<span>' + esc(label) + '</span>' +
          '<span class="text-[10px] px-1.5 py-0.2 rounded-full ' + (isAct ? 'bg-[#176B45] text-white' : 'bg-slate-100 text-slate-500') + '">' + count + '</span>' +
        '</button>';
      }).join('');

      // Columns and items for active table
      var currentItems = state.tables[state.activeTable] || [];
      var filteredItems = currentItems.filter(function (it) {
        if (!state.search) return true;
        var q = state.search.toLowerCase();
        return Object.values(it).some(function (val) {
          return String(val).toLowerCase().indexOf(q) !== -1;
        });
      });

      var cols = [];
      if (currentItems.length > 0) {
        cols = Object.keys(currentItems[0]);
      }

      var theadHtml = cols.map(function (c) {
        var cleanCol = c.replace(/([A-Z])/g, ' $1').replace(/^./, function (str) { return str.toUpperCase(); });
        return '<th class="py-2.5 px-3 text-[11px] font-medium text-slate-500 uppercase tracking-wider">' + esc(cleanCol) + '</th>';
      }).join('');

      var tbodyHtml = filteredItems.map(function (item) {
        var tds = cols.map(function (c) {
          var val = item[c];
          var cellContent = '';
          if (typeof val === 'boolean') {
            cellContent = val ? '<span class="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">Active / Yes</span>' :
                                '<span class="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-medium bg-slate-100 text-slate-500">No</span>';
          } else if (c.toLowerCase().indexOf('color') !== -1 || c.toLowerCase().indexOf('badge') !== -1) {
            cellContent = '<span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-slate-100 text-slate-700">' + esc(val) + '</span>';
          } else if (c === 'id' || c === 'code') {
            cellContent = '<span class="font-mono text-slate-700 font-medium">' + esc(val) + '</span>';
          } else {
            cellContent = esc(val == null ? '--' : val);
          }
          return '<td class="py-2.5 px-3 text-xs text-slate-700">' + cellContent + '</td>';
        }).join('');

        return '<tr class="border-b border-slate-100 hover:bg-slate-50/60 transition-colors">' +
          tds +
          '<td class="py-2.5 px-3 text-right">' +
            '<button type="button" class="btn-edit-item p-1.5 rounded-lg text-slate-400 hover:text-[#176B45] hover:bg-emerald-50 transition-colors cursor-pointer" data-id="' + esc(item.id) + '" title="Edit Entry">' +
              '<span class="material-symbols-outlined text-[16px]">edit</span>' +
            '</button>' +
          '</td>' +
        '</tr>';
      }).join('');

      root.innerHTML = '' +
        '<div class="space-y-4">' +
          // Section Switcher Banner
          '<div class="bg-white border border-slate-200 rounded-xl p-3 shadow-2xs flex flex-wrap items-center justify-between gap-3">' +
            '<div class="flex flex-wrap items-center gap-1.5">' +
              secTabsHtml +
            '</div>' +
            '<div class="flex items-center gap-2">' +
              '<span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-[11px] font-medium bg-slate-50 border border-slate-200 text-slate-600">' +
                '<span class="material-symbols-outlined text-xs text-[#176B45]">sync</span>' +
                '<span>MoEYS Standard Master Schema</span>' +
              '</span>' +
            '</div>' +
          '</div>' +

          // Table Pills Header
          '<div class="bg-white border border-slate-200 rounded-xl p-3 shadow-2xs">' +
            '<div class="text-[11px] font-medium uppercase tracking-wider text-slate-400 mb-2">Reference Tables in ' + esc(secLabels[state.section]) + ':</div>' +
            '<div class="flex flex-wrap gap-2">' +
              tablePillsHtml +
            '</div>' +
          '</div>' +

          // Controls & Filter Bar
          '<div class="bg-white border border-slate-200 rounded-xl p-3 shadow-2xs flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">' +
            '<div class="relative flex-1 max-w-md">' +
              '<span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm">search</span>' +
              '<input type="text" id="tmDictSearch" placeholder="Filter definitions across all fields..." value="' + esc(state.search) + '" class="w-full pl-9 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-[#176B45] text-slate-800">' +
            '</div>' +
            '<div class="flex items-center gap-2">' +
              '<button type="button" id="btnExportDict" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 hover:border-[#176B45] text-xs font-medium text-slate-700 hover:text-[#176B45] bg-white transition-all cursor-pointer shadow-2xs">' +
                '<span class="material-symbols-outlined text-sm">download</span>' +
                '<span>Export CSV</span>' +
              '</button>' +
              '<button type="button" id="btnAddNewEntry" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#176B45] text-white hover:bg-[#125638] text-xs font-medium transition-all shadow-xs cursor-pointer">' +
                '<span class="material-symbols-outlined text-sm">add</span>' +
                '<span>+ Add Definition</span>' +
              '</button>' +
            '</div>' +
          '</div>' +

          // Main Data Table
          '<div class="bg-white border border-slate-200 rounded-xl shadow-2xs overflow-hidden">' +
            '<div class="px-4 py-2.5 border-b border-slate-100 flex items-center justify-between bg-slate-50/60">' +
              '<div class="flex items-center gap-2">' +
                '<span class="material-symbols-outlined text-[#176B45] text-base">table_chart</span>' +
                '<span class="text-xs font-medium text-slate-800">' + esc(TABLE_PRETTY_NAMES[state.activeTable] || state.activeTable) + '</span>' +
                '<span class="text-[11px] text-slate-400 font-mono">(' + filteredItems.length + ' records)</span>' +
              '</div>' +
              '<span class="text-[11px] text-slate-400 font-mono">Table: ' + esc(state.activeTable) + '</span>' +
            '</div>' +
            '<div class="overflow-x-auto">' +
              '<table class="w-full text-left border-collapse">' +
                '<thead>' +
                  '<tr class="border-b border-slate-200 bg-slate-50/40">' +
                    theadHtml +
                    '<th class="py-2.5 px-3 text-right text-[11px] font-medium text-slate-500 uppercase tracking-wider">Action</th>' +
                  '</tr>' +
                '</thead>' +
                '<tbody>' +
                  (tbodyHtml || '<tr><td colspan="' + (cols.length + 1) + '" class="text-center py-10 text-xs text-slate-400">No definitions found matching search criteria.</td></tr>') +
                '</tbody>' +
              '</table>' +
            '</div>' +
          '</div>' +
        '</div>' +

        // Add/Edit Modal
        '<div id="tmDictModal" class="hidden fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-xs p-4">' +
          '<div class="bg-white border border-slate-200 rounded-2xl shadow-xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in-95 duration-150">' +
            '<div class="px-5 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50/60">' +
              '<div class="flex items-center gap-2">' +
                '<span class="material-symbols-outlined text-[#176B45]">post_add</span>' +
                '<span class="text-sm font-medium text-slate-800" id="tmModalTitle">New Dictionary Definition</span>' +
              '</div>' +
              '<button type="button" id="tmCloseDictModal" class="text-slate-400 hover:text-slate-600 p-1 rounded-lg hover:bg-slate-100 transition-colors cursor-pointer"><span class="material-symbols-outlined text-lg">close</span></button>' +
            '</div>' +
            '<div class="p-5 space-y-3" id="tmModalForm"></div>' +
            '<div class="px-5 py-3.5 border-t border-slate-100 flex items-center justify-end gap-2 bg-slate-50/60">' +
              '<button type="button" id="btnCancelDict" class="px-3.5 py-1.5 rounded-lg border border-slate-200 text-slate-700 hover:bg-slate-100 text-xs font-medium transition-all cursor-pointer">Cancel</button>' +
              '<button type="button" id="btnSaveDict" class="px-4 py-1.5 rounded-lg bg-[#176B45] text-white hover:bg-[#125638] text-xs font-medium transition-all shadow-xs cursor-pointer">Save Definition</button>' +
            '</div>' +
          '</div>' +
        '</div>';

      // Event Listeners
      root.querySelectorAll('.btn-sec-tab').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var sec = btn.getAttribute('data-section');
          loadSection(sec);
        });
      });

      root.querySelectorAll('.btn-table-pill').forEach(function (btn) {
        btn.addEventListener('click', function () {
          state.activeTable = btn.getAttribute('data-table');
          state.search = '';
          render();
        });
      });

      var searchInput = document.getElementById('tmDictSearch');
      if (searchInput) {
        searchInput.addEventListener('input', function (e) {
          state.search = e.target.value;
          render();
        });
      }

      var modal = document.getElementById('tmDictModal');
      var closeModal = document.getElementById('tmCloseDictModal');
      var cancelBtn = document.getElementById('btnCancelDict');
      if (closeModal) closeModal.onclick = function () { modal.classList.add('hidden'); };
      if (cancelBtn) cancelBtn.onclick = function () { modal.classList.add('hidden'); };

      var addBtn = document.getElementById('btnAddNewEntry');
      if (addBtn) {
        addBtn.addEventListener('click', function () {
          document.getElementById('tmModalTitle').textContent = 'Add Entry to ' + (TABLE_PRETTY_NAMES[state.activeTable] || state.activeTable);
          var formHtml = cols.map(function (c) {
            if (c === 'id') return '';
            var cleanCol = c.replace(/([A-Z])/g, ' $1').replace(/^./, function (str) { return str.toUpperCase(); });
            return '<div>' +
              '<label class="text-xs text-slate-500 font-medium">' + esc(cleanCol) + ':</label>' +
              '<input type="text" data-field="' + esc(c) + '" class="w-full mt-1 p-2 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-[#176B45] text-slate-800" placeholder="Enter ' + esc(cleanCol) + '...">' +
            '</div>';
          }).join('');

          document.getElementById('tmModalForm').innerHTML = formHtml;
          modal.classList.remove('hidden');

          document.getElementById('btnSaveDict').onclick = function () {
            var newEntry = {};
            document.querySelectorAll('#tmModalForm input').forEach(function (inp) {
              var f = inp.getAttribute('data-field');
              newEntry[f] = inp.value;
            });

            fetch('/api/dictionary/table/' + encodeURIComponent(state.section) + '/' + encodeURIComponent(state.activeTable), {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(newEntry)
            })
              .then(function (r) { return r.json(); })
              .then(function (res) {
                if (res.success) {
                  toast('Definition added successfully.');
                  modal.classList.add('hidden');
                  loadSection(state.section);
                }
              });
          };
        });
      }

      var exportBtn = document.getElementById('btnExportDict');
      if (exportBtn) {
        exportBtn.addEventListener('click', function () {
          toast('Exporting ' + (TABLE_PRETTY_NAMES[state.activeTable] || state.activeTable) + ' to CSV...');
        });
      }
    }

    loadSection(state.section);
  };

  // Specific view helpers
  DD.initSchoolData = function (containerId, portalRole) { DD.init(containerId, portalRole, 'school'); };
  DD.initStudentData = function (containerId, portalRole) { DD.init(containerId, portalRole, 'students'); };
  DD.initTeacherData = function (containerId, portalRole) { DD.init(containerId, portalRole, 'teachers'); };
  DD.initAdditionalData = function (containerId, portalRole) { DD.init(containerId, portalRole, 'additional'); };
  DD.initTimetableData = function (containerId, portalRole) { DD.init(containerId, portalRole, 'timetable'); };

})(window, document);
