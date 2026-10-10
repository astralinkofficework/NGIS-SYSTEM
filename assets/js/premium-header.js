/**
 * ════════════════════════════════════════════════════════════════════════════════
 * PREMIUM STUDENT PORTAL HEADER
 * ════════════════════════════════════════════════════════════════════════════════
 *
 * A responsive, production-ready header component with:
 * - Mobile-first responsive design (320px → desktop)
 * - Vivid blue background with organic SVG curved bottom extension
 * - Optimized performance and accessibility
 * - Theme support (light/dark mode)
 * - Safe area support for notched devices
 *
 * Usage:
 *   PremiumHeader.init({
 *     title: 'Assignments',
 *     studentName: 'Akeem',
 *     studentInitial: 'A',
 *     avatarUrl: '/path/to/avatar.jpg',
 *     onBack: () => { window.history.back(); }
 *   });
 *
 * ════════════════════════════════════════════════════════════════════════════════
 */

const PremiumHeader = (() => {
  'use strict';

  // ────────────────────────────────────────────────────────────────────────────
  // STATE
  // ────────────────────────────────────────────────────────────────────────────
  const state = {
    isInitialized: false,
    title: 'Assignments',
    studentName: 'Student',
    studentInitial: 'S',
    avatarUrl: null,
    onBack: null,
    currentTheme: 'light',
  };

  const elements = {
    header: null,
    svgBg: null,
    svgPath: null,
    backButton: null,
    title: null,
    avatarContainer: null,
    avatarContent: null,
    avatarImg: null,
    studentName: null,
    studentNameSub: null,
  };

  // ────────────────────────────────────────────────────────────────────────────
  // INITIALIZATION
  // ────────────────────────────────────────────────────────────────────────────

  /**
   * Initialize the premium header with provided configuration
   * @param {Object} config - Configuration object
   * @param {string} config.title - Page title (e.g., "Assignments")
   * @param {string} config.studentName - Student's full name
   * @param {string} config.studentInitial - Avatar initial (single character)
   * @param {string} [config.avatarUrl] - URL to student avatar image
   * @param {Function} [config.onBack] - Callback when back button is clicked
   */
  function init(config = {}) {
    if (state.isInitialized) {
      console.warn('PremiumHeader: Already initialized. Call destroy() first to reinitialize.');
      return;
    }

    // Cache configuration
    Object.assign(state, config);

    // Cache DOM elements
    cacheElements();

    if (!elements.header) {
      console.error('PremiumHeader: Header element not found. Ensure premium-header.html is loaded.');
      return;
    }

    // Initialize theme detection
    detectTheme();

    // Bind event listeners
    bindEvents();

    // Update content
    updateContent();

    // Initialize SVG curve
    updateCurve();

    // Detect system color scheme changes
    if (window.matchMedia) {
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', onThemeChange);
    }

    state.isInitialized = true;
  }

  /**
   * Cache DOM elements for better performance
   */
  function cacheElements() {
    elements.header = document.getElementById('premiumHeader');
    elements.svgBg = document.getElementById('premiumHeaderSvgBg');
    elements.svgPath = document.getElementById('premiumHeaderSvgPath');
    elements.backButton = document.getElementById('premiumHeaderBack');
    elements.title = document.getElementById('premiumHeaderTitle');
    elements.avatarContainer = document.getElementById('premiumHeaderAvatar');
    elements.avatarContent = document.getElementById('premiumHeaderAvatarContent');
    elements.avatarImg = document.getElementById('premiumHeaderAvatarImg');
    elements.studentName = document.getElementById('premiumHeaderName');
    elements.studentNameSub = document.getElementById('premiumHeaderNameSub');
  }

  /**
   * Bind event listeners
   */
  function bindEvents() {
    if (elements.backButton) {
      elements.backButton.addEventListener('click', onBackClick);
      elements.backButton.addEventListener('keydown', onBackKeydown);
    }

    // SVG curve update on resize
    var resizeTimer;
    window.addEventListener('resize', function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(updateCurve, 16);
    });

    // Initial curve calculation after fonts load
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(function () {
        setTimeout(updateCurve, 50);
      });
    }

    // Multiple attempts for reliability
    setTimeout(updateCurve, 30);
    setTimeout(updateCurve, 150);
    setTimeout(updateCurve, 400);

    // ResizeObserver for the header element
    if (window.ResizeObserver && elements.header) {
      new ResizeObserver(updateCurve).observe(elements.header);
    }
  }

  /**
   * Unbind event listeners
   */
  function unbindEvents() {
    if (elements.backButton) {
      elements.backButton.removeEventListener('click', onBackClick);
      elements.backButton.removeEventListener('keydown', onBackKeydown);
    }

    if (window.matchMedia) {
      window.matchMedia('(prefers-color-scheme: dark)').removeEventListener('change', onThemeChange);
    }
  }

  // ────────────────────────────────────────────────────────────────────────────
  // SVG DIAGONAL CLIP-PATH GENERATOR
  // ────────────────────────────────────────────────────────────────────────────

  /**
   * Updates the SVG path for the diagonal cut at the bottom-right.
   * Creates an asymmetric angled edge that contrasts with the circular avatar.
   */
  function updateCurve() {
    if (!elements.header || !elements.svgPath) return;

    var w = elements.header.offsetWidth;
    if (w <= 0) return;

    var h = elements.header.scrollHeight || elements.header.offsetHeight;
    if (h <= 0) return;

    // Diagonal cut parameters
    var cutStartX = w * (w < 375 ? 0.75 : w < 768 ? 0.80 : 0.85);
    var cutEndX   = w;
    var bottomY   = h;

    // Small rounded corner at the cut point
    var r = 12;

    // Build diagonal clip-path
    var d = [
      'M 0 0',
      'L ' + cutStartX + ' 0',
      'Q ' + (cutStartX + r) + ' 0 ' + (cutStartX + r) + ' ' + r,
      'L ' + (cutEndX - r) + ' ' + (bottomY - r),
      'Q ' + cutEndX + ' ' + (bottomY - r) + ' ' + cutEndX + ' ' + bottomY,
      'L 0 ' + bottomY,
      'Z'
    ].join(' ');

    elements.svgPath.setAttribute('d', d);
  }

  // ────────────────────────────────────────────────────────────────────────────
  // EVENT HANDLERS
  // ────────────────────────────────────────────────────────────────────────────

  /**
   * Handle back button click
   */
  function onBackClick(e) {
    e.preventDefault();

    if (state.onBack && typeof state.onBack === 'function') {
      state.onBack();
    } else {
      window.history.back();
    }
  }

  /**
   * Handle back button keyboard navigation
   */
  function onBackKeydown(e) {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      onBackClick(e);
    }
  }

  /**
   * Handle system theme change
   */
  function onThemeChange(e) {
    state.currentTheme = e.matches ? 'dark' : 'light';
  }

  // ────────────────────────────────────────────────────────────────────────────
  // CONTENT UPDATES
  // ────────────────────────────────────────────────────────────────────────────

  /**
   * Update header content from state
   */
  function updateContent() {
    if (!state.isInitialized) return;

    if (elements.title) {
      elements.title.textContent = sanitizeText(state.title);
    }

    if (elements.studentName) {
      elements.studentName.textContent = sanitizeText(state.studentName);
    }

    if (elements.avatarContent) {
      elements.avatarContent.textContent = (state.studentInitial || 'S').toUpperCase().charAt(0);
    }

    if (state.avatarUrl && elements.avatarImg) {
      loadAvatarImage(state.avatarUrl);
    }
  }

  /**
   * Load and display avatar image
   * @param {string} url - Avatar image URL
   */
  function loadAvatarImage(url) {
    if (!url || !elements.avatarImg) return;

    const img = new Image();

    img.onload = () => {
      elements.avatarImg.src = url;
      elements.avatarImg.style.display = 'block';
      elements.avatarContent.style.display = 'none';
    };

    img.onerror = () => {
      elements.avatarContent.style.display = 'block';
      elements.avatarImg.style.display = 'none';
    };

    img.src = url;
  }

  /**
   * Sanitize text to prevent XSS
   * @param {string} text - Text to sanitize
   * @returns {string} Sanitized text
   */
  function sanitizeText(text) {
    const div = document.createElement('div');
    div.textContent = String(text || '');
    return div.innerHTML;
  }

  // ────────────────────────────────────────────────────────────────────────────
  // THEME DETECTION
  // ────────────────────────────────────────────────────────────────────────────

  /**
   * Detect current theme from system or DOM
   */
  function detectTheme() {
    const htmlTheme = document.documentElement.getAttribute('data-theme');
    if (htmlTheme) {
      state.currentTheme = htmlTheme;
      return;
    }

    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      state.currentTheme = 'dark';
    } else {
      state.currentTheme = 'light';
    }
  }

  // ────────────────────────────────────────────────────────────────────────────
  // PUBLIC API
  // ────────────────────────────────────────────────────────────────────────────

  function setTitle(newTitle) {
    state.title = newTitle;
    if (elements.title) {
      elements.title.textContent = sanitizeText(newTitle);
    }
  }

  function setStudentName(newName, newInitial = null) {
    state.studentName = newName;
    if (elements.studentName) {
      elements.studentName.textContent = sanitizeText(newName);
    }

    if (newInitial) {
      state.studentInitial = newInitial;
      if (elements.avatarContent) {
        elements.avatarContent.textContent = newInitial.toUpperCase().charAt(0);
      }
    }
  }

  function setAvatarImage(avatarUrl) {
    state.avatarUrl = avatarUrl;
    loadAvatarImage(avatarUrl);
  }

  function setOnBack(callback) {
    state.onBack = callback;
  }

  function getState() {
    return { ...state };
  }

  function destroy() {
    unbindEvents();
    state.isInitialized = false;
  }

  function reflow() {
    if (!elements.header) return;
    elements.header.offsetHeight;
    updateCurve();
  }

  // ────────────────────────────────────────────────────────────────────────────
  // RETURN PUBLIC API
  // ────────────────────────────────────────────────────────────────────────────

  return {
    init,
    setTitle,
    setStudentName,
    setAvatarImage,
    setOnBack,
    getState,
    destroy,
    reflow,
  };
})();
