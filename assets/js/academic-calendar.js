/**
 * NGIS Academic Calendar Engine
 * Shared across Admin, Principal, and Shared Portals.
 * Fully compatible with layout.js, hero.js, and action-icons.js.
 */
(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.NGISAcademicCalendar = factory();
  }
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  var DEFAULT_EVENTS = [
    {
      id: 'EVT-2026-101',
      title: 'Grade 12 Saturday Review & Student Council Session',
      category: 'academic',
      date: '2026-11-21',
      startTime: '08:00',
      endTime: '11:30',
      location: 'Academic Hall B / Room 302',
      audience: 'Grade 12 & Student Leaders',
      organizer: 'Academic Directorate',
      description: 'Extended academic tutorial on Senior Mathematics and weekly student government agenda planning.'
    },
    {
      id: 'EVT-2026-102',
      title: 'Law Project & IB Essay Submissions Due',
      category: 'academic',
      date: '2026-11-24',
      startTime: '16:00',
      endTime: '17:00',
      location: 'Online Portal / Library Desk',
      audience: 'Senior High School Students',
      organizer: 'Humanities Department',
      description: 'Final submission deadline for Term 1 research papers and case study portfolios.'
    },
    {
      id: 'EVT-2026-103',
      title: 'Midterm Examination Period Begins',
      category: 'exam',
      date: '2026-11-26',
      startTime: '07:30',
      endTime: '15:00',
      location: 'All Main Examination Halls',
      audience: 'Grades 7–12',
      organizer: 'Examination Board',
      description: 'Formal school-wide midterm testing block. Morning and afternoon sessions apply.'
    },
    {
      id: 'EVT-2026-104',
      title: 'Water Festival Holiday (Bon Om Touk) — Day 1',
      category: 'holiday',
      date: '2026-11-28',
      startTime: '00:00',
      endTime: '23:59',
      location: 'National Observance',
      audience: 'All Campus Community',
      organizer: 'Ministry of Education',
      description: 'Campus closed in observance of the Cambodian Water Festival. Digital e-learning portal remains active.'
    },
    {
      id: 'EVT-2026-105',
      title: 'Water Festival Holiday (Bon Om Touk) — Day 2',
      category: 'holiday',
      date: '2026-11-29',
      startTime: '00:00',
      endTime: '23:59',
      location: 'National Observance',
      audience: 'All Campus Community',
      organizer: 'Ministry of Education',
      description: 'Official national holiday. Campus grounds and administration offices closed.'
    },
    {
      id: 'EVT-2026-106',
      title: 'Water Festival Holiday (Bon Om Touk) — Day 3',
      category: 'holiday',
      date: '2026-11-30',
      startTime: '00:00',
      endTime: '23:59',
      location: 'National Observance',
      audience: 'All Campus Community',
      organizer: 'Ministry of Education',
      description: 'Final day of official national water festival break. Classes resume on Tuesday, Dec 1.'
    },
    {
      id: 'EVT-2026-107',
      title: 'Annual Science & Technology Fair 2026',
      category: 'event',
      date: '2026-12-04',
      startTime: '08:30',
      endTime: '16:00',
      location: 'Central Gymnasium & STEM Courtyard',
      audience: 'All Students, Teachers & Parents',
      organizer: 'Science Department',
      description: 'Student exhibits covering autonomous robotics, environmental sensors, AI models, and bio-science.'
    },
    {
      id: 'EVT-2026-108',
      title: 'Faculty Professional Development Workshop',
      category: 'faculty',
      date: '2026-12-08',
      startTime: '13:30',
      endTime: '16:30',
      location: 'Conference Center West',
      audience: 'All Teaching Faculty',
      organizer: 'Office of the Principal',
      description: 'Curriculum harmonization, formative rubrics, and modern digital classroom assessment methods.'
    },
    {
      id: 'EVT-2026-109',
      title: 'Parent-Teacher Academic Consultation Day',
      category: 'academic',
      date: '2026-12-12',
      startTime: '08:00',
      endTime: '17:00',
      location: 'Campus Classrooms & Main Auditorium',
      audience: 'Parents & Guardians',
      organizer: 'Student Affairs',
      description: 'Individual progress review meetings between parents and subject teachers.'
    },
    {
      id: 'EVT-2026-110',
      title: 'Semester 1 Final Examinations — Day 1',
      category: 'exam',
      date: '2026-12-15',
      startTime: '07:30',
      endTime: '15:30',
      location: 'Examination Halls 1–4',
      audience: 'Grades 9–12',
      organizer: 'Examination Office',
      description: 'Mathematics, Khmer Literature, and Natural Sciences assessment papers.'
    },
    {
      id: 'EVT-2026-111',
      title: 'Semester 1 Final Examinations — Day 2',
      category: 'exam',
      date: '2026-12-16',
      startTime: '07:30',
      endTime: '15:30',
      location: 'Examination Halls 1–4',
      audience: 'Grades 9–12',
      organizer: 'Examination Office',
      description: 'English Language Arts, Social Studies, and Foreign Language papers.'
    },
    {
      id: 'EVT-2026-112',
      title: 'Board of Directors Year-End Executive Session',
      category: 'board',
      date: '2026-12-22',
      startTime: '09:00',
      endTime: '13:00',
      location: 'Executive Boardroom',
      audience: 'Board & School Leadership',
      organizer: 'Director General',
      description: 'Review of institutional capital developments, annual audit results, and 2027 strategic initiatives.'
    },
    {
      id: 'EVT-2026-113',
      title: 'Winter Break & Christmas Recess Begins',
      category: 'holiday',
      date: '2026-12-24',
      startTime: '00:00',
      endTime: '23:59',
      location: 'School-wide',
      audience: 'All Campus Community',
      organizer: 'Administration',
      description: 'Official winter recess. School administrative offices open on modified holiday schedule.'
    },
    {
      id: 'EVT-2027-114',
      title: 'Term 2 Classes Resume',
      category: 'academic',
      date: '2027-01-04',
      startTime: '07:00',
      endTime: '16:00',
      location: 'All Campuses',
      audience: 'All Students & Teachers',
      organizer: 'Academic Affairs',
      description: 'First instructional day of Academic Term 2 for all grades.'
    },
    {
      id: 'EVT-2027-115',
      title: 'Victory Over Genocide Day (National Holiday)',
      category: 'holiday',
      date: '2027-01-07',
      startTime: '00:00',
      endTime: '23:59',
      location: 'National Observance',
      audience: 'All Campus Community',
      organizer: 'National Holiday',
      description: 'Campus closed in honor of Victory Over Genocide Day.'
    }
  ];

  var CATEGORIES = [
    { id: 'all', label: 'All Events', color: '#176B45' },
    { id: 'academic', label: 'Academic', color: '#2563EB' },
    { id: 'exam', label: 'Examinations', color: '#DC2626' },
    { id: 'holiday', label: 'Holidays & Recesses', color: '#D97706' },
    { id: 'faculty', label: 'Faculty & PD', color: '#7C3AED' },
    { id: 'event', label: 'School Events', color: '#0D9488' },
    { id: 'board', label: 'Board & Governance', color: '#475569' }
  ];

  var MONTH_NAMES = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  var DAY_NAMES_SHORT = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

  function pad(n) {
    return (n < 10 ? '0' : '') + n;
  }

  function formatDateStr(y, m, d) {
    return y + '-' + pad(m + 1) + '-' + pad(d);
  }

  function Calendar(config) {
    config = config || {};
    this.container = typeof config.container === 'string'
      ? document.querySelector(config.container)
      : (config.container || document.getElementById('academicCalendarApp'));

    this.role = config.role || 'admin';
    this.canManage = config.canManage !== undefined
      ? config.canManage
      : ['admin', 'superadmin', 'principal'].indexOf(this.role) !== -1;

    // Fixed default date: Nov 21, 2026 (or today if configured)
    this.currentDate = config.initialDate ? new Date(config.initialDate) : new Date(2026, 10, 21);
    this.view = config.initialView || 'month';
    this.category = 'all';
    this.searchQuery = '';
    this.hideFilterChips = config.hideFilterChips !== undefined ? config.hideFilterChips : (this.role === 'student');

    this.events = this.loadEvents();
    this.selectedEvent = null;

    if (this.container) {
      this.init();
    }
  }

  Calendar.prototype.loadEvents = function () {
    try {
      var saved = localStorage.getItem('ngis_calendar_events_v2');
      if (saved) {
        var parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length > 0) return parsed;
      }
    } catch (e) {
      console.warn('Failed to load local calendar events', e);
    }
    return DEFAULT_EVENTS.slice();
  };

  Calendar.prototype.saveEvents = function () {
    try {
      localStorage.setItem('ngis_calendar_events_v2', JSON.stringify(this.events));
    } catch (e) {
      console.warn('Failed to persist calendar events', e);
    }
  };

  Calendar.prototype.init = function () {
    this.render();
    this.bindGlobalEvents();
  };

  Calendar.prototype.bindGlobalEvents = function () {
    var self = this;

    // Keyboard navigation
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        self.closeModals();
      }
    });
  };

  Calendar.prototype.setView = function (mode) {
    if (['month', 'week', 'agenda'].indexOf(mode) === -1) return;
    this.view = mode;
    this.render();
  };

  Calendar.prototype.prev = function () {
    if (this.view === 'month') {
      this.currentDate.setMonth(this.currentDate.getMonth() - 1);
    } else if (this.view === 'week') {
      this.currentDate.setDate(this.currentDate.getDate() - 7);
    } else {
      this.currentDate.setMonth(this.currentDate.getMonth() - 1);
    }
    this.render();
  };

  Calendar.prototype.next = function () {
    if (this.view === 'month') {
      this.currentDate.setMonth(this.currentDate.getMonth() + 1);
    } else if (this.view === 'week') {
      this.currentDate.setDate(this.currentDate.getDate() + 7);
    } else {
      this.currentDate.setMonth(this.currentDate.getMonth() + 1);
    }
    this.render();
  };

  Calendar.prototype.today = function () {
    this.currentDate = new Date(2026, 10, 21);
    this.render();
  };

  Calendar.prototype.filterCategory = function (cat) {
    this.category = cat || 'all';
    this.render();
  };

  Calendar.prototype.search = function (query) {
    this.searchQuery = (query || '').trim().toLowerCase();
    this.render();
  };

  Calendar.prototype.getFilteredEvents = function () {
    var self = this;
    return this.events.filter(function (evt) {
      if (self.category !== 'all' && evt.category !== self.category) return false;
      if (self.searchQuery) {
        var matchTitle = evt.title.toLowerCase().indexOf(self.searchQuery) !== -1;
        var matchLoc = (evt.location || '').toLowerCase().indexOf(self.searchQuery) !== -1;
        var matchDesc = (evt.description || '').toLowerCase().indexOf(self.searchQuery) !== -1;
        if (!matchTitle && !matchLoc && !matchDesc) return false;
      }
      return true;
    });
  };

  Calendar.prototype.render = function () {
    if (!this.container) return;
    var filtered = this.getFilteredEvents();

    var html = '';
    html += '<div class="cal-card">';
    html += this.renderToolbar();
    html += this.renderFilterBar();

    if (this.view === 'month') {
      html += this.renderMonthView(filtered);
    } else if (this.view === 'week') {
      html += this.renderWeekView(filtered);
    } else {
      html += this.renderAgendaView(filtered);
    }

    html += '</div>';

    // Render Modals inside container or root
    html += this.renderDetailModal();
    if (this.canManage) {
      html += this.renderAddModal();
    }

    this.container.innerHTML = html;
    this.attachEventListeners();
  };

  Calendar.prototype.renderToolbar = function () {
    var year = this.currentDate.getFullYear();
    var month = this.currentDate.getMonth();
    var heading = MONTH_NAMES[month] + ' ' + year;

    var html = '<div class="cal-toolbar">';
    
    // Left: Nav & Period Heading
    html += '<div class="cal-nav-group">';
    html += '  <h2 class="cal-period-heading">' + heading + '</h2>';
    html += '  <div class="cal-nav-btns">';
    html += '    <button type="button" class="cal-nav-btn" data-action="prev" title="Previous" aria-label="Previous"><span data-ngis-icon="chevronLeft"></span></button>';
    html += '    <button type="button" class="cal-today-btn" data-action="today">Today</button>';
    html += '    <button type="button" class="cal-nav-btn" data-action="next" title="Next" aria-label="Next"><span data-ngis-icon="chevronRight"></span></button>';
    html += '  </div>';
    html += '</div>';

    // Center: Segmented View Selector
    html += '<div class="cal-view-pills" role="tablist">';
    html += '  <button type="button" role="tab" class="cal-view-pill ' + (this.view === 'month' ? 'active' : '') + '" data-view="month" aria-selected="' + (this.view === 'month') + '">Month</button>';
    html += '  <button type="button" role="tab" class="cal-view-pill ' + (this.view === 'week' ? 'active' : '') + '" data-view="week" aria-selected="' + (this.view === 'week') + '">Week</button>';
    html += '  <button type="button" role="tab" class="cal-view-pill ' + (this.view === 'agenda' ? 'active' : '') + '" data-view="agenda" aria-selected="' + (this.view === 'agenda') + '">Agenda</button>';
    html += '</div>';

    // Right: Actions
    html += '<div class="cal-actions">';
    html += '  <button type="button" class="cal-btn-action" data-action="export" title="Download iCalendar file"><span data-ngis-icon="download"></span><span>Export (.ICS)</span></button>';
    html += '  <button type="button" class="cal-btn-action" onclick="window.print()" title="Print Calendar"><span data-ngis-icon="print"></span><span>Print</span></button>';
    if (this.canManage) {
      html += '  <button type="button" class="cal-btn-action primary" data-action="add-event"><span data-ngis-icon="add"></span><span>Add Event</span></button>';
    }
    html += '</div>';

    html += '</div>';
    return html;
  };

  Calendar.prototype.renderFilterBar = function () {
    var self = this;
    var html = '<div class="cal-filter-bar">';

    // Chips
    if (!this.hideFilterChips) {
      html += '<div class="cal-filter-chips">';
      CATEGORIES.forEach(function (cat) {
        var isActive = self.category === cat.id;
        html += '<button type="button" class="cal-chip ' + (isActive ? 'active' : '') + '" data-category="' + cat.id + '">';
        if (cat.id !== 'all') {
          html += '<span class="cal-chip-dot" style="background-color:' + cat.color + '"></span>';
        }
        html += cat.label;
        html += '</button>';
      });
      html += '</div>';
    }

    // Search input
    html += '<div class="cal-search-wrap">';
    html += '  <span class="cal-search-icon" data-ngis-icon="search"></span>';
    html += '  <input type="text" id="calSearchInput" placeholder="Filter events…" value="' + (this.searchQuery || '') + '" aria-label="Filter calendar events">';
    html += '</div>';

    html += '</div>';
    return html;
  };

  Calendar.prototype.renderMonthView = function (events) {
    var year = this.currentDate.getFullYear();
    var month = this.currentDate.getMonth();

    var firstDayOfMonth = new Date(year, month, 1);
    var lastDayOfMonth = new Date(year, month + 1, 0);

    // Days in week: Mon=0 ... Sun=6 (Standard ISO academic calendar)
    var startDay = (firstDayOfMonth.getDay() + 6) % 7;
    var totalDays = lastDayOfMonth.getDate();

    // Days from previous month
    var prevMonthLastDay = new Date(year, month, 0).getDate();

    var html = '<div class="cal-month-grid">';

    // 7-column header
    DAY_NAMES_SHORT.forEach(function (name) {
      html += '<div class="cal-month-head">' + name + '</div>';
    });

    // Helper map of events by YYYY-MM-DD
    var eventMap = {};
    events.forEach(function (evt) {
      if (!eventMap[evt.date]) eventMap[evt.date] = [];
      eventMap[evt.date].push(evt);
    });

    // Previous month filler cells
    for (var i = startDay - 1; i >= 0; i--) {
      var d = prevMonthLastDay - i;
      var dateStr = formatDateStr(month === 0 ? year - 1 : year, (month + 11) % 12, d);
      html += this.renderDayCell(d, dateStr, true, eventMap[dateStr] || []);
    }

    // Current month cells
    for (var day = 1; day <= totalDays; day++) {
      var currDateStr = formatDateStr(year, month, day);
      var isToday = (currDateStr === '2026-11-21');
      html += this.renderDayCell(day, currDateStr, false, eventMap[currDateStr] || [], isToday);
    }

    // Next month filler cells to complete 35 or 42 grid cells
    var filledCount = startDay + totalDays;
    var totalSlots = filledCount <= 35 ? 35 : 42;
    var nextMonthDays = totalSlots - filledCount;
    for (var n = 1; n <= nextMonthDays; n++) {
      var nextDateStr = formatDateStr(month === 11 ? year + 1 : year, (month + 1) % 12, n);
      html += this.renderDayCell(n, nextDateStr, true, eventMap[nextDateStr] || []);
    }

    html += '</div>';
    return html;
  };

  Calendar.prototype.renderDayCell = function (dayNum, dateStr, isOutOfMonth, dayEvents, isToday) {
    var cellClass = 'cal-day-cell';
    if (isOutOfMonth) cellClass += ' out-of-month';
    if (isToday) cellClass += ' is-today';

    var html = '<div class="' + cellClass + '" data-date="' + dateStr + '">';
    html += '<div class="cal-day-header">';
    html += '<span class="cal-day-num">' + dayNum + '</span>';
    html += '</div>';

    html += '<div class="cal-events-list">';
    var maxVisible = 3;
    var visibleEvents = dayEvents.slice(0, maxVisible);
    var remaining = dayEvents.length - maxVisible;

    visibleEvents.forEach(function (evt) {
      var catClass = 'cat-' + evt.category;
      html += '<div class="cal-event-chip ' + catClass + '" data-event-id="' + evt.id + '" title="' + evt.title + '">';
      if (evt.startTime && evt.startTime !== '00:00') {
        html += '<span style="font-size:10px;opacity:0.8;margin-right:3px;">' + evt.startTime + '</span>';
      }
      html += evt.title;
      html += '</div>';
    });

    if (remaining > 0) {
      html += '<span class="cal-overflow-badge" data-action="overflow" data-date="' + dateStr + '">+' + remaining + ' more</span>';
    }

    html += '</div>';
    html += '</div>';
    return html;
  };

  Calendar.prototype.renderWeekView = function (events) {
    var self = this;
    var curr = new Date(this.currentDate);
    var dayOfWeek = (curr.getDay() + 6) % 7;
    var monday = new Date(curr);
    monday.setDate(curr.getDate() - dayOfWeek);

    var weekDates = [];
    for (var i = 0; i < 7; i++) {
      var d = new Date(monday);
      d.setDate(monday.getDate() + i);
      weekDates.push(d);
    }

    var html = '<div class="cal-week-container">';
    html += '<div class="cal-week-grid">';

    // Top Header Row
    html += '<div class="cal-week-head-cell" style="background:var(--cal-surface)">Time</div>';
    weekDates.forEach(function (dateObj, idx) {
      var dStr = formatDateStr(dateObj.getFullYear(), dateObj.getMonth(), dateObj.getDate());
      var isToday = (dStr === '2026-11-21');
      html += '<div class="cal-week-head-cell ' + (isToday ? 'is-today' : '') + '">';
      html += '<div>' + DAY_NAMES_SHORT[idx] + '</div>';
      html += '<div style="font-size:14px;font-weight:500;margin-top:2px;">' + dateObj.getDate() + '</div>';
      html += '</div>';
    });

    // Time Slots 07:00 through 18:00
    var hours = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18];
    hours.forEach(function (h) {
      var timeLabel = pad(h) + ':00';
      html += '<div class="cal-time-col-cell">' + timeLabel + '</div>';

      weekDates.forEach(function (dObj) {
        var dStr = formatDateStr(dObj.getFullYear(), dObj.getMonth(), dObj.getDate());
        var isToday = (dStr === '2026-11-21');

        // Events that fall in this hour slot
        var slotEvents = events.filter(function (e) {
          if (e.date !== dStr) return false;
          var evtHour = parseInt(e.startTime.split(':')[0], 10);
          return evtHour === h;
        });

        html += '<div class="cal-hour-cell ' + (isToday ? 'is-today' : '') + '" data-date="' + dStr + '" data-hour="' + h + '">';
        slotEvents.forEach(function (evt) {
          html += '<div class="cal-event-chip cat-' + evt.category + '" data-event-id="' + evt.id + '">';
          html += '<span style="font-weight:500">' + evt.startTime + '</span> ' + evt.title;
          html += '</div>';
        });
        html += '</div>';
      });
    });

    html += '</div>';
    html += '</div>';
    return html;
  };

  Calendar.prototype.renderAgendaView = function (events) {
    if (events.length === 0) {
      return (
        '<div class="cal-empty-state">' +
        '  <div class="cal-empty-icon"><span data-ngis-icon="calendar"></span></div>' +
        '  <div class="cal-empty-title">No Academic Events Found</div>' +
        '  <div class="cal-empty-sub">No schedule records match your selected filter criteria.</div>' +
        '</div>'
      );
    }

    // Group events by date
    var grouped = {};
    events.slice().sort(function (a, b) {
      return a.date.localeCompare(b.date) || a.startTime.localeCompare(b.startTime);
    }).forEach(function (evt) {
      if (!grouped[evt.date]) grouped[evt.date] = [];
      grouped[evt.date].push(evt);
    });

    var html = '<div class="cal-agenda-view">';
    Object.keys(grouped).forEach(function (dateStr) {
      var dateEvents = grouped[dateStr];
      var d = new Date(dateStr + 'T00:00:00');
      var dayName = DAY_NAMES_SHORT[(d.getDay() + 6) % 7];
      var monthName = MONTH_NAMES[d.getMonth()];
      var dateDisplay = dayName + ', ' + monthName + ' ' + d.getDate() + ', ' + d.getFullYear();

      html += '<div class="cal-agenda-group">';
      html += '  <div class="cal-agenda-date-header">';
      html += '    <span>' + dateDisplay + '</span>';
      html += '    <span style="font-size:12px;color:var(--cal-text-muted)">' + dateEvents.length + ' event' + (dateEvents.length > 1 ? 's' : '') + '</span>';
      html += '  </div>';

      html += '  <div class="cal-agenda-events">';
      dateEvents.forEach(function (evt) {
        var catObj = CATEGORIES.filter(function (c) { return c.id === evt.category; })[0] || { label: evt.category, color: '#176B45' };
        var timeStr = (evt.startTime && evt.startTime !== '00:00') ? (evt.startTime + ' – ' + evt.endTime) : 'All Day';

        html += '<div class="cal-agenda-row" data-event-id="' + evt.id + '">';
        html += '  <div class="cal-agenda-time">' + timeStr + '</div>';
        html += '  <div class="cal-agenda-details">';
        html += '    <div class="cal-agenda-title">' + evt.title + '</div>';
        html += '    <div class="cal-agenda-meta">';
        html += '      <span class="cal-agenda-pill" style="background-color:rgba(23,107,69,0.08);color:var(--cal-text)">' + catObj.label + '</span>';
        if (evt.location) {
          html += '    <span><span data-ngis-icon="pin" style="margin-right:2px"></span>' + evt.location + '</span>';
        }
        if (evt.audience) {
          html += '    <span><span data-ngis-icon="users" style="margin-right:2px"></span>' + evt.audience + '</span>';
        }
        html += '    </div>';
        html += '  </div>';
        html += '</div>';
      });

      html += '  </div>';
      html += '</div>';
    });

    html += '</div>';
    return html;
  };

  Calendar.prototype.renderDetailModal = function () {
    return (
      '<div class="cal-modal-backdrop" id="calDetailModal">' +
      '  <div class="cal-modal-card" role="dialog" aria-modal="true" aria-labelledby="calDetailTitle">' +
      '    <div class="cal-modal-header">' +
      '      <h3 class="cal-modal-title" id="calDetailTitle">Event Details</h3>' +
      '      <button type="button" class="cal-modal-close" data-action="close-modal" aria-label="Close modal"><span data-ngis-icon="close"></span></button>' +
      '    </div>' +
      '    <div class="cal-modal-body" id="calDetailBody"></div>' +
      '    <div class="cal-modal-footer" id="calDetailFooter">' +
      '      <button type="button" class="cal-btn-action" data-action="close-modal">Close</button>' +
      '    </div>' +
      '  </div>' +
      '</div>'
    );
  };

  Calendar.prototype.renderAddModal = function () {
    return (
      '<div class="cal-modal-backdrop" id="calAddModal">' +
      '  <div class="cal-modal-card" role="dialog" aria-modal="true" aria-labelledby="calAddTitle">' +
      '    <div class="cal-modal-header">' +
      '      <h3 class="cal-modal-title" id="calAddTitle">Add Academic Event</h3>' +
      '      <button type="button" class="cal-modal-close" data-action="close-modal" aria-label="Close modal"><span data-ngis-icon="close"></span></button>' +
      '    </div>' +
      '    <form id="calAddForm">' +
      '      <div class="cal-modal-body">' +
      '        <div class="cal-form-group">' +
      '          <label class="cal-form-label" for="addEvtTitle">Event Title *</label>' +
      '          <input type="text" class="cal-form-input" id="addEvtTitle" required placeholder="e.g. Science Olympiad Briefing">' +
      '        </div>' +
      '        <div class="cal-form-row">' +
      '          <div class="cal-form-group">' +
      '            <label class="cal-form-label" for="addEvtCat">Category *</label>' +
      '            <select class="cal-form-select" id="addEvtCat">' +
      '              <option value="academic">Academic Milestone</option>' +
      '              <option value="exam">Examination</option>' +
      '              <option value="holiday">Holiday / Recess</option>' +
      '              <option value="faculty">Faculty / PD</option>' +
      '              <option value="event">School Event</option>' +
      '              <option value="board">Board & Governance</option>' +
      '            </select>' +
      '          </div>' +
      '          <div class="cal-form-group">' +
      '            <label class="cal-form-label" for="addEvtDate">Date *</label>' +
      '            <input type="date" class="cal-form-input" id="addEvtDate" value="2026-11-21" required>' +
      '          </div>' +
      '        </div>' +
      '        <div class="cal-form-row">' +
      '          <div class="cal-form-group">' +
      '            <label class="cal-form-label" for="addEvtStart">Start Time</label>' +
      '            <input type="time" class="cal-form-input" id="addEvtStart" value="08:00">' +
      '          </div>' +
      '          <div class="cal-form-group">' +
      '            <label class="cal-form-label" for="addEvtEnd">End Time</label>' +
      '            <input type="time" class="cal-form-input" id="addEvtEnd" value="10:00">' +
      '          </div>' +
      '        </div>' +
      '        <div class="cal-form-group">' +
      '          <label class="cal-form-label" for="addEvtLoc">Location / Venue</label>' +
      '          <input type="text" class="cal-form-input" id="addEvtLoc" placeholder="e.g. Main Auditorium / Room 302">' +
      '        </div>' +
      '        <div class="cal-form-group">' +
      '          <label class="cal-form-label" for="addEvtAudience">Target Audience</label>' +
      '          <input type="text" class="cal-form-input" id="addEvtAudience" placeholder="e.g. All Students, Faculty">' +
      '        </div>' +
      '        <div class="cal-form-group">' +
      '          <label class="cal-form-label" for="addEvtDesc">Description</label>' +
      '          <textarea class="cal-form-textarea" id="addEvtDesc" rows="3" placeholder="Provide schedule details, room numbers, or links..."></textarea>' +
      '        </div>' +
      '      </div>' +
      '      <div class="cal-modal-footer">' +
      '        <button type="button" class="cal-btn-action" data-action="close-modal">Cancel</button>' +
      '        <button type="submit" class="cal-btn-action primary">Publish Event</button>' +
      '      </div>' +
      '    </form>' +
      '  </div>' +
      '</div>'
    );
  };

  Calendar.prototype.attachEventListeners = function () {
    var self = this;

    // Navigation buttons
    var prevBtn = this.container.querySelector('[data-action="prev"]');
    if (prevBtn) prevBtn.addEventListener('click', function () { self.prev(); });

    var nextBtn = this.container.querySelector('[data-action="next"]');
    if (nextBtn) nextBtn.addEventListener('click', function () { self.next(); });

    var todayBtn = this.container.querySelector('[data-action="today"]');
    if (todayBtn) todayBtn.addEventListener('click', function () { self.today(); });

    // View Pills
    var pills = this.container.querySelectorAll('.cal-view-pill');
    pills.forEach(function (pill) {
      pill.addEventListener('click', function () {
        self.setView(pill.getAttribute('data-view'));
      });
    });

    // Category Chips
    var chips = this.container.querySelectorAll('.cal-chip');
    chips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        self.filterCategory(chip.getAttribute('data-category'));
      });
    });

    // Search Input
    var searchInput = this.container.querySelector('#calSearchInput');
    if (searchInput) {
      var searchTimeout = null;
      searchInput.addEventListener('input', function (e) {
        clearTimeout(searchTimeout);
        var val = e.target.value;
        searchTimeout = setTimeout(function () {
          self.search(val);
        }, 220);
      });
    }

    // Export button
    var exportBtn = this.container.querySelector('[data-action="export"]');
    if (exportBtn) {
      exportBtn.addEventListener('click', function () {
        self.exportICS();
      });
    }

    // Add Event button
    var addBtn = this.container.querySelector('[data-action="add-event"]');
    if (addBtn) {
      addBtn.addEventListener('click', function () {
        self.openAddModal();
      });
    }

    // Event chips & Agenda rows
    var eventItems = this.container.querySelectorAll('[data-event-id]');
    eventItems.forEach(function (item) {
      item.addEventListener('click', function (e) {
        e.stopPropagation();
        var id = item.getAttribute('data-event-id');
        self.openEventModal(id);
      });
    });

    // Modals close triggers
    var closeBtns = this.container.querySelectorAll('[data-action="close-modal"]');
    closeBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        self.closeModals();
      });
    });

    // Form submit
    var form = this.container.querySelector('#calAddForm');
    if (form) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        self.handleCreateEvent();
      });
    }

    // Hydrate action icons
    if (window.NGIS && window.NGIS.renderIcons) {
      window.NGIS.renderIcons(this.container);
    }
  };

  Calendar.prototype.openEventModal = function (eventId) {
    var evt = this.events.filter(function (e) { return e.id === eventId; })[0];
    if (!evt) return;

    var modal = this.container.querySelector('#calDetailModal');
    var body = this.container.querySelector('#calDetailBody');
    var footer = this.container.querySelector('#calDetailFooter');
    if (!modal || !body) return;

    var catObj = CATEGORIES.filter(function (c) { return c.id === evt.category; })[0] || { label: evt.category };

    var html = '';
    html += '<div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">';
    html += '  <span class="cal-agenda-pill" style="background-color:rgba(23,107,69,0.08);color:var(--cal-text);font-size:11px;">' + catObj.label + '</span>';
    html += '  <span style="font-size:12px;color:var(--cal-text-muted)">ID: ' + evt.id + '</span>';
    html += '</div>';

    html += '<h4 style="font-size:17px;font-weight:500;margin:0 0 12px;color:var(--cal-text);line-height:1.35;">' + evt.title + '</h4>';

    html += '<div style="display:flex;flex-direction:column;gap:8px;font-size:13px;color:var(--cal-text-muted);border-top:1px solid var(--cal-border);border-bottom:1px solid var(--cal-border);padding:12px 0;">';
    html += '  <div style="display:flex;align-items:center;gap:8px;"><span data-ngis-icon="calendar"></span><span>' + evt.date + ' (' + (evt.startTime ? evt.startTime + ' – ' + evt.endTime : 'All Day') + ')</span></div>';
    if (evt.location) {
      html += '  <div style="display:flex;align-items:center;gap:8px;"><span data-ngis-icon="pin"></span><span>' + evt.location + '</span></div>';
    }
    if (evt.audience) {
      html += '  <div style="display:flex;align-items:center;gap:8px;"><span data-ngis-icon="users"></span><span>' + evt.audience + '</span></div>';
    }
    if (evt.organizer) {
      html += '  <div style="display:flex;align-items:center;gap:8px;"><span data-ngis-icon="badge"></span><span>Organized by: ' + evt.organizer + '</span></div>';
    }
    html += '</div>';

    if (evt.description) {
      html += '<div style="font-size:13px;color:var(--cal-text);line-height:1.5;margin-top:4px;">' + evt.description + '</div>';
    }

    body.innerHTML = html;

    // Footer actions
    var self = this;
    var footerHtml = '<button type="button" class="cal-btn-action" data-action="close-modal">Close</button>';
    if (this.canManage) {
      footerHtml = '<button type="button" class="cal-btn-action" id="btnDeleteCalEvt" style="color:#DC2626;border-color:#FCA5A5;">Delete</button>' + footerHtml;
    }
    footer.innerHTML = footerHtml;

    var delBtn = footer.querySelector('#btnDeleteCalEvt');
    if (delBtn) {
      delBtn.addEventListener('click', function () {
        if (confirm('Are you sure you want to delete this event from the academic schedule?')) {
          self.deleteEvent(evt.id);
        }
      });
    }

    var closeBtn = footer.querySelector('[data-action="close-modal"]');
    if (closeBtn) {
      closeBtn.addEventListener('click', function () {
        self.closeModals();
      });
    }

    modal.classList.add('is-open');
    if (window.NGIS && window.NGIS.renderIcons) {
      window.NGIS.renderIcons(body);
    }
  };

  Calendar.prototype.openAddModal = function () {
    var modal = this.container.querySelector('#calAddModal');
    if (modal) modal.classList.add('is-open');
  };

  Calendar.prototype.closeModals = function () {
    var modals = this.container.querySelectorAll('.cal-modal-backdrop');
    modals.forEach(function (m) {
      m.classList.remove('is-open');
    });
  };

  Calendar.prototype.handleCreateEvent = function () {
    var title = this.container.querySelector('#addEvtTitle').value.trim();
    var category = this.container.querySelector('#addEvtCat').value;
    var date = this.container.querySelector('#addEvtDate').value;
    var startTime = this.container.querySelector('#addEvtStart').value || '08:00';
    var endTime = this.container.querySelector('#addEvtEnd').value || '10:00';
    var location = this.container.querySelector('#addEvtLoc').value.trim();
    var audience = this.container.querySelector('#addEvtAudience').value.trim();
    var description = this.container.querySelector('#addEvtDesc').value.trim();

    if (!title || !date) return;

    var newId = 'EVT-' + Date.now().toString(36).toUpperCase();
    var newEvt = {
      id: newId,
      title: title,
      category: category,
      date: date,
      startTime: startTime,
      endTime: endTime,
      location: location || 'Campus Main',
      audience: audience || 'School Community',
      organizer: this.role.toUpperCase() + ' Administration',
      description: description
    };

    this.events.unshift(newEvt);
    this.saveEvents();
    this.closeModals();
    this.render();

    if (window.toast) {
      window.toast('Academic event published successfully', 'success');
    }
  };

  Calendar.prototype.deleteEvent = function (id) {
    this.events = this.events.filter(function (e) { return e.id !== id; });
    this.saveEvents();
    this.closeModals();
    this.render();

    if (window.toast) {
      window.toast('Academic event removed', 'info');
    }
  };

  Calendar.prototype.exportICS = function () {
    var events = this.getFilteredEvents();
    var lines = [
      'BEGIN:VCALENDAR',
      'VERSION:2.0',
      'PRODID:-//NGIS International School//Academic Calendar//EN',
      'CALSCALE:GREGORIAN',
      'METHOD:PUBLISH'
    ];

    events.forEach(function (evt) {
      var dClean = evt.date.replace(/-/g, '');
      var startClean = (evt.startTime || '08:00').replace(/:/g, '') + '00';
      var endClean = (evt.endTime || '10:00').replace(/:/g, '') + '00';

      lines.push('BEGIN:VEVENT');
      lines.push('UID:' + evt.id + '@ngis.edu.kh');
      lines.push('DTSTAMP:' + dClean + 'T000000Z');
      lines.push('DTSTART:' + dClean + 'T' + startClean);
      lines.push('DTEND:' + dClean + 'T' + endClean);
      lines.push('SUMMARY:' + evt.title.replace(/,/g, '\\,'));
      if (evt.description) lines.push('DESCRIPTION:' + evt.description.replace(/\n/g, '\\n'));
      if (evt.location) lines.push('LOCATION:' + evt.location.replace(/,/g, '\\,'));
      lines.push('STATUS:CONFIRMED');
      lines.push('END:VEVENT');
    });

    lines.push('END:VCALENDAR');
    var icsContent = lines.join('\r\n');

    var blob = new Blob([icsContent], { type: 'text/calendar;charset=utf-8' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = 'NGIS_Academic_Calendar_2026-2027.ics';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return Calendar;
});
