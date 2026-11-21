/* ══════════════════════════════════════════════════════════════
   NGIS SYSTEM — 3D FLUENCY ICON INTEGRATION ENGINE
   Official Icons8 3D Fluency Assets · Academic Workspace Mapping
   ══════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  // Base directory resolver based on current execution path
  function getAssetRoot() {
    var p = window.location.pathname || '';
    if (p.indexOf('/pages/') !== -1) {
      return '../../assets/images/icons-3d/';
    }
    return 'assets/images/icons-3d/';
  }

  // Canonical mapping of academic concepts to 3D Fluency image filenames
  var ICON_MAP = {
    // 1. Core Academic Navigation
    'calendar': 'calendar.png',
    'timetable': 'timetable.png',
    'classes': 'classroom.png',
    'classroom': 'classroom.png',
    'assignments': 'notepad.png',
    'assignment': 'notepad.png',
    'notepad': 'notepad.png',
    'lessons': 'open-book.png',
    'lesson': 'open-book.png',
    'book': 'open-book.png',
    'open-book': 'open-book.png',
    'grades': 'trophy.png',
    'grade': 'trophy.png',
    'trophy': 'trophy.png',
    'exams': 'graduation-cap.png',
    'exam': 'graduation-cap.png',
    'graduation-cap': 'graduation-cap.png',
    'attendance': 'fingerprint.png',
    'fingerprint': 'fingerprint.png',
    'announcements': 'megaphone.png',
    'announcement': 'megaphone.png',
    'megaphone': 'megaphone.png',
    'profile': 'student-male.png',
    'student': 'student-male.png',
    'student-male': 'student-male.png',
    'reports': 'business-report.png',
    'report': 'business-report.png',
    'business-report': 'business-report.png',
    'documents': 'documents.png',
    'document': 'documents.png',
    'portfolio': 'briefcase.png',
    'briefcase': 'briefcase.png',
    'library': 'books.png',
    'books': 'books.png',
    'deadlines': 'alarm-clock.png',
    'deadline': 'alarm-clock.png',
    'alarm-clock': 'alarm-clock.png',
    'events': 'confetti.png',
    'event': 'confetti.png',
    'confetti': 'confetti.png',
    'teachers': 'training.png',
    'teacher': 'training.png',
    'training': 'training.png',
    'curriculum': 'compass.png',
    'compass': 'compass.png',
    'completed': 'ok.png',
    'ok': 'ok.png',
    'checkmark': 'ok.png',
    'empty': 'empty-box.png',
    'empty-box': 'empty-box.png',
    'calculator': 'calculator.png',
    'math': 'calculator.png',
    'microscope': 'microscope.png',
    'science': 'microscope.png',
    'pencil': 'pencil.png',
    'grade-work': 'pencil.png',
    'grading': 'pencil.png',
    'test-passed': 'test-passed.png',
    'tests': 'test-passed.png',
    'quizzes': 'test-passed.png',
    'diploma': 'diploma.png',
    'certificates': 'diploma.png',
    'honors': 'diploma.png',
    'chat': 'chat.png',
    'messages': 'chat.png',
    'bell': 'bell.png',
    'notification': 'bell.png',
    'notifications': 'bell.png',
    'bar-chart': 'bar-chart.png',
    'gradebook': 'bar-chart.png',
    'analytics': 'bar-chart.png',
    'school': 'school.png',
    'campus': 'school.png',
    'inbox': 'inbox.png',
    'submissions': 'inbox.png',
    'submission': 'inbox.png',
    'physics': 'physics.png',
    'stem': 'physics.png',
    'music': 'music.png',
    'arts': 'music.png',
    'roster': 'training.png',
    'register': 'fingerprint.png',
    'take-register': 'fingerprint.png'
  };

  /**
   * Get the relative path for an icon key
   */
  function getUrl(name) {
    var key = String(name || '').toLowerCase().trim();
    var filename = ICON_MAP[key] || 'documents.png';
    return getAssetRoot() + filename;
  }

  /**
   * Render an <img> HTML string with responsive dimensions, lazy loading, and fallback
   */
  function renderHtml(name, options) {
    options = options || {};
    var size = options.size || 28;
    var cls = options.className ? ' ' + options.className : '';
    var alt = options.alt || (name + ' icon');
    var url = getUrl(name);

    return (
      '<img class="ngis-3d-icon' + cls + '" ' +
      'src="' + url + '" ' +
      'width="' + size + '" ' +
      'height="' + size + '" ' +
      'alt="' + alt + '" ' +
      'loading="lazy" ' +
      'decoding="async" ' +
      'onerror="this.onerror=null; this.style.display=\'none\';">'
    );
  }

  /**
   * Hydrate all elements in the DOM matching <span data-ngis-3d="name"></span>
   */
  function hydrate(root) {
    var container = root || document;
    var slots = container.querySelectorAll('[data-ngis-3d]');
    slots.forEach(function (slot) {
      var name = slot.getAttribute('data-ngis-3d');
      var size = parseInt(slot.getAttribute('data-size'), 10) || 28;
      var cls = slot.getAttribute('data-class') || '';
      var alt = slot.getAttribute('data-alt') || name;
      
      var imgHtml = renderHtml(name, {
        size: size,
        className: cls,
        alt: alt
      });
      slot.outerHTML = imgHtml;
    });
  }

  // Export to global namespace
  window.NGIS3D = {
    get: getUrl,
    html: renderHtml,
    hydrate: hydrate,
    map: ICON_MAP
  };

  // Auto-hydrate on DOM ready if document is loaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      hydrate();
    });
  } else {
    hydrate();
  }
})();
