/**
 * NGIS Academic File Library Component
 * Reusable, responsive academic file library with recognizable file type icons,
 * compact date indicators, rich metadata display, preview, and download capabilities.
 * 
 * Strict Scope: Student Portal
 */
(function() {
  'use strict';

  var MONTH_NAMES_SHORT = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
  var MONTH_NAMES_FULL = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  function parseDate(dateStr) {
    if (!dateStr) {
      var now = new Date();
      return {
        monthShort: MONTH_NAMES_SHORT[now.getMonth()],
        monthFull: MONTH_NAMES_FULL[now.getMonth()],
        day: String(now.getDate()).padStart(2, '0'),
        year: String(now.getFullYear())
      };
    }
    // Handle 'YYYY-MM-DD' or ISO format
    var parts = String(dateStr).split('T')[0].split('-');
    if (parts.length === 3) {
      var y = parseInt(parts[0], 10);
      var m = parseInt(parts[1], 10) - 1;
      var d = parseInt(parts[2], 10);
      return {
        monthShort: MONTH_NAMES_SHORT[m] || 'NOV',
        monthFull: MONTH_NAMES_FULL[m] || 'November',
        day: String(d).padStart(2, '0'),
        year: String(y)
      };
    }
    var dt = new Date(dateStr);
    if (!isNaN(dt.getTime())) {
      return {
        monthShort: MONTH_NAMES_SHORT[dt.getMonth()],
        monthFull: MONTH_NAMES_FULL[dt.getMonth()],
        day: String(dt.getDate()).padStart(2, '0'),
        year: String(dt.getFullYear())
      };
    }
    return { monthShort: 'NOV', monthFull: 'November', day: '21', year: '2026' };
  }

  function getFileExtension(filename, fallbackType) {
    if (!filename) return (fallbackType || 'pdf').toLowerCase();
    var parts = filename.split('.');
    if (parts.length > 1) {
      return parts.pop().toLowerCase();
    }
    return (fallbackType || 'pdf').toLowerCase();
  }

  function getFileCategory(ext) {
    switch (ext) {
      case 'pdf':
        return { label: 'PDF Document', cssClass: 'type-pdf' };
      case 'doc':
      case 'docx':
        return { label: 'Word Document', cssClass: 'type-docx' };
      case 'xls':
      case 'xlsx':
      case 'csv':
        return { label: 'Excel Spreadsheet', cssClass: 'type-xlsx' };
      case 'ppt':
      case 'pptx':
        return { label: 'Presentation Deck', cssClass: 'type-pptx' };
      case 'png':
      case 'jpg':
      case 'jpeg':
      case 'webp':
      case 'image':
        return { label: 'Image File', cssClass: 'type-image' };
      case 'zip':
      case 'rar':
      case '7z':
        return { label: 'Compressed Archive', cssClass: 'type-zip' };
      case 'js':
      case 'py':
      case 'html':
      case 'css':
        return { label: 'Source Code', cssClass: 'type-code' };
      default:
        return { label: 'Academic File', cssClass: 'type-file' };
    }
  }

  function getFileTypeIconSvg(ext) {
    var cat = getFileCategory(ext);
    switch (cat.cssClass) {
      case 'type-pdf':
        return '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 2h7l5 5v13a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2zm6 1.5V8h4.5L13 3.5zM8 12v5h1.5v-1.8h1.2c1.1 0 1.8-.6 1.8-1.6 0-1-.7-1.6-1.8-1.6H8zm1.5 1.2h1c.4 0 .6.2.6.5s-.2.5-.6.5h-1v-1zm4.5-1.2v5h1.6c1.3 0 2.2-.8 2.2-2.5s-.9-2.5-2.2-2.5H14zm1.5 1.2h.5c.6 0 1 .4 1 1.3s-.4 1.3-1 1.3h-.5v-2.6z"/></svg>';
      case 'type-docx':
        return '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6zm-1 1.5L18.5 9H13V3.5zM7.5 17l1.2-5.5h1.4l.8 3.5.8-3.5h1.4L14.3 17h-1.3l-.8-3.6-.8 3.6H7.5z"/></svg>';
      case 'type-xlsx':
        return '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6zm-1 1.5L18.5 9H13V3.5zM8 11.5l1.8 2.7L8 16.9h1.5l1.1-1.8 1.1 1.8h1.5L11.4 14.2l1.8-2.7h-1.5l-1.1 1.8-1.1-1.8H8z"/></svg>';
      case 'type-pptx':
        return '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6zm-1 1.5L18.5 9H13V3.5zM8.5 11.5h2.8c1.2 0 2 .7 2 1.8 0 1.2-.8 1.8-2 1.8h-1.3V17H8.5v-5.5zm1.5 2.4h1.1c.4 0 .7-.2.7-.6s-.3-.6-.7-.6H10v1.2z"/></svg>';
      case 'type-image':
        return '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M21 19V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/></svg>';
      case 'type-zip':
        return '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6zm-4 4h2v2h-2V6zm2 2h2v2h-2V8zm-2 2h2v2h-2v-2zm2 2h2v2h-2v-2zm-3 4h4v3H9v-3zm4-10.5L18.5 9H13V3.5z"/></svg>';
      default:
        return '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6zm-1 1.5L18.5 9H13V3.5zM7 11h10v1.5H7V11zm0 3h10v1.5H7V14zm0 3h7v1.5H7V17z"/></svg>';
    }
  }

  function esc(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  var NGISFileLibrary = {
    /**
     * Parse date into compact and full components
     */
    parseDate: parseDate,

    /**
     * Get document metadata from filename/extension
     */
    getFileCategory: getFileCategory,

    /**
     * Render single compact academic file row
     */
    renderRow: function(file, options) {
      options = options || {};
      var ext = getFileExtension(file.src || file.name, file.fileType);
      var cat = getFileCategory(ext);
      var dt = parseDate(file.date || file.uploadedAt);
      var fullDate = dt.monthFull + ' ' + parseInt(dt.day, 10) + ', ' + dt.year;
      var size = file.size || '1.8 MB';
      var uploader = file.uploader || file.author || file.teacher || 'Department Faculty';
      var title = file.fullName || file.name || 'Academic Handout';
      var src = file.src || '../../assets/uploads/lessons/sample-lesson.pdf';
      var fileId = file.id || ('f_' + Math.random().toString(36).substr(2, 6));

      var iconSvg = getFileTypeIconSvg(ext);

      return [
        '<article class="ngis-file-row" data-file-id="' + esc(fileId) + '" data-ext="' + esc(ext) + '" data-topic="' + esc(file.topic || '') + '">',
        '  <div class="ngis-file-date-badge" title="Published: ' + esc(fullDate) + '">',
        '    <span class="ngis-file-date-month">' + esc(dt.monthShort) + '</span>',
        '    <span class="ngis-file-date-day">' + esc(dt.day) + '</span>',
        '  </div>',
        '  <div class="ngis-file-type-icon ' + cat.cssClass + '" title="' + esc(cat.label) + '">',
        '    ' + iconSvg,
        '  </div>',
        '  <div class="ngis-file-info">',
        '    <a href="javascript:void(0)" class="ngis-file-name" onclick="window.NGISFileLibrary.preview(\'' + esc(fileId) + '\')" title="' + esc(title) + '">',
        '      ' + esc(title),
        '    </a>',
        '    <div class="ngis-file-metadata">',
        '      <span class="ngis-file-meta-pill">' + esc(ext.toUpperCase()) + '</span>',
        '      <span class="ngis-file-meta-dot">•</span>',
        '      <span>' + esc(cat.label) + '</span>',
        '      <span class="ngis-file-meta-dot">•</span>',
        '      <span>' + esc(size) + '</span>',
        '      <span class="ngis-file-meta-dot">•</span>',
        '      <span>' + esc(fullDate) + '</span>',
        '      <span class="ngis-file-meta-dot">•</span>',
        '      <span class="text-slate-500 font-medium">' + esc(uploader) + '</span>',
        '    </div>',
        '  </div>',
        '  <div class="ngis-file-actions">',
        '    <button type="button" class="ngis-file-btn" onclick="window.NGISFileLibrary.preview(\'' + esc(fileId) + '\')" title="Preview ' + esc(title) + '">',
        '      <span data-ngis-icon="view"></span>',
        '      <span class="hidden sm:inline">Preview</span>',
        '    </button>',
        '    <button type="button" class="ngis-file-btn ngis-file-btn-primary" onclick="window.NGISFileLibrary.download(\'' + esc(fileId) + '\')" title="Download ' + esc(title) + '">',
        '      <span data-ngis-icon="download"></span>',
        '      <span class="hidden sm:inline">Download</span>',
        '    </button>',
        '  </div>',
        '</article>'
      ].join('\n');
    },

    /**
     * Render full file library container with search/filter
     */
    renderList: function(files, containerOrSelector, options) {
      var container = typeof containerOrSelector === 'string'
        ? document.querySelector(containerOrSelector)
        : containerOrSelector;
      if (!container) return;

      options = options || {};
      window._ngisCurrentFiles = files || [];

      if (!files || files.length === 0) {
        container.innerHTML = [
          '<div class="p-8 text-center bg-white border border-slate-200 rounded-xl">',
          '  <img src="../../assets/images/icons-3d/empty-box.png" width="48" height="48" class="ngis-3d-icon mx-auto mb-2" alt="No files">',
          '  <h4 class="text-sm font-medium text-slate-800">No Learning Materials Found</h4>',
          '  <p class="text-xs text-slate-500 mt-1">There are currently no files uploaded for this section.</p>',
          '</div>'
        ].join('\n');
        return;
      }

      var rowsHtml = files.map(function(f) {
        return NGISFileLibrary.renderRow(f, options);
      }).join('\n');

      container.innerHTML = '<div class="ngis-file-library">' + rowsHtml + '</div>';

      // Hydrate Bootstrap icons if available
      if (window.NGIS && typeof window.NGIS.hydrateIcons === 'function') {
        window.NGIS.hydrateIcons(container);
      }
    },

    /**
     * Preview file handler
     */
    preview: function(fileId) {
      var files = window._ngisCurrentFiles || [];
      var f = files.find(function(x) { return x.id === fileId; });
      var title = f ? (f.fullName || f.name) : 'Academic Document';
      var src = (f && f.src) ? f.src : '../../assets/uploads/lessons/sample-lesson.pdf';

      // Check if oakOpenPreview exists on page
      if (typeof window.oakOpenPreview === 'function' && f) {
        window.oakOpenPreview(f.id, f.fullName || f.name, src);
        return;
      }

      // Check if global modal exists or create lightweight clean modal
      var modalId = 'ngisDocPreviewModal';
      var modal = document.getElementById(modalId);
      if (!modal) {
        modal = document.createElement('div');
        modal.id = modalId;
        modal.style.cssText = 'position:fixed;inset:0;background:rgba(15,23,42,0.65);backdrop-filter:blur(4px);z-index:9999;display:flex;align-items:center;justify-content:center;padding:16px;';
        modal.innerHTML = [
          '<div style="background:#fff;border-radius:16px;width:100%;max-width:880px;height:90vh;max-height:800px;display:flex;flex-direction:column;box-shadow:0 25px 50px -12px rgba(0,0,0,0.25);overflow:hidden;border:1px solid #E1E9E3;">',
          '  <div style="padding:14px 20px;border-bottom:1px solid #E1E9E3;display:flex;align-items:center;justify-content:space-between;background:#F7F9F7;">',
          '    <div style="display:flex;align-items:center;gap:10px;min-width:0;">',
          '      <img src="../../assets/images/icons-3d/documents.png" width="24" height="24" class="ngis-3d-icon" alt="Document">',
          '      <h3 id="ngisModalPreviewTitle" style="font-size:14px;font-weight:500;color:#29352E;margin:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">Document Preview</h3>',
          '    </div>',
          '    <div style="display:flex;align-items:center;gap:8px;">',
          '      <a id="ngisModalDownloadBtn" href="' + esc(src) + '" download class="ngis-file-btn ngis-file-btn-primary" style="text-decoration:none;"><span data-ngis-icon="download"></span> Download</a>',
          '      <button type="button" class="ngis-file-btn" onclick="document.getElementById(\'' + modalId + '\').style.display=\'none\'" style="padding:6px 8px;" aria-label="Close"><span data-ngis-icon="close"></span></button>',
          '    </div>',
          '  </div>',
          '  <div style="flex:1;background:#525659;position:relative;">',
          '    <iframe id="ngisModalPreviewIframe" src="' + esc(src) + '" style="width:100%;height:100%;border:none;"></iframe>',
          '  </div>',
          '</div>'
        ].join('\n');
        document.body.appendChild(modal);
        if (window.NGIS && typeof window.NGIS.hydrateIcons === 'function') {
          window.NGIS.hydrateIcons(modal);
        }
      } else {
        var titleEl = document.getElementById('ngisModalPreviewTitle');
        var iframe = document.getElementById('ngisModalPreviewIframe');
        var dlBtn = document.getElementById('ngisModalDownloadBtn');
        if (titleEl) titleEl.textContent = title;
        if (iframe) iframe.src = src;
        if (dlBtn) {
          dlBtn.href = src;
          dlBtn.download = title.replace(/\s+/g, '_') + '.pdf';
        }
        modal.style.display = 'flex';
      }
    },

    /**
     * Download file handler
     */
    download: function(fileId) {
      var files = window._ngisCurrentFiles || [];
      var f = files.find(function(x) { return x.id === fileId; });
      var title = f ? (f.fullName || f.name) : 'Academic_Document';
      var src = (f && f.src) ? f.src : '../../assets/uploads/lessons/sample-lesson.pdf';

      if (window.toast) {
        window.toast('Downloading ' + title + '...', 'info');
      } else if (window.NGISUI && typeof window.NGISUI.toast === 'function') {
        window.NGISUI.toast('Downloading ' + title + '...', 'info');
      }

      var a = document.createElement('a');
      a.href = src;
      a.download = title.replace(/[^a-zA-Z0-9_-]/g, '_') + '.pdf';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    }
  };

  window.NGISFileLibrary = NGISFileLibrary;
})();
