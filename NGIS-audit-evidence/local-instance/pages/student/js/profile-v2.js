/* ══════════════════════════════════════════════════════════════
   NGIS Student Profile v2 — tab switching + session user data
   ══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var TABS = [
    { key: 'personal', tab: 'pf2TabPersonal', pane: 'pf2PanePersonal' },
    { key: 'academic', tab: 'pf2TabAcademic', pane: 'pf2PaneAcademic' },
    { key: 'security', tab: 'pf2TabSecurity', pane: 'pf2PaneSecurity' }
  ];

  window.pf2SwitchTab = function (key) {
    TABS.forEach(function (t) {
      var active = t.key === key;
      var tab = document.getElementById(t.tab);
      var pane = document.getElementById(t.pane);
      if (tab) {
        tab.classList.toggle('active', active);
        tab.setAttribute('aria-selected', active ? 'true' : 'false');
      }
      if (pane) pane.hidden = !active;
    });
  };

  window.pf2Toast = function (msg, kind) {
    if (window.toast) window.toast(msg, kind || 'info');
    else console.log('[NGIS]', msg);
  };

  window.pf2Strength = function (value) {
    var bars = document.querySelectorAll('#pf2Strength span');
    var label = document.querySelector('#pf2Strength em');
    var score = 0;
    if (value.length >= 8) score++;
    if (/[A-Z]/.test(value) && /[a-z]/.test(value)) score++;
    if (/\d|[^A-Za-z0-9]/.test(value)) score++;
    score = Math.min(3, score);
    bars.forEach(function (b, i) { b.classList.toggle('on', i < score); });
    if (label) label.textContent = !value ? 'Enter a new password' : score >= 3 ? 'Strong' : score >= 2 ? 'Good' : 'Weak';
  };

  /* Populate identity fields from the signed-in session where available */
  function hydrateUser() {
    var u = null;
    try { u = window.NGISAuth && NGISAuth.getUser && NGISAuth.getUser(); } catch (e) {}
    if (!u) return;
    var full = [u.firstName, u.lastName].filter(Boolean).join(' ');
    if (full) {
      var nameEl = document.getElementById('pf2Name');
      if (nameEl) nameEl.textContent = full;
      var first = document.getElementById('pf2First');
      var last = document.getElementById('pf2Last');
      if (first) first.value = u.firstName || '';
      if (last) last.value = u.lastName || '';
    }
    if (u.id) {
      var idEl = document.getElementById('pf2StudentId');
      if (idEl) idEl.textContent = u.id;
    }
    if (u.email) {
      var mailEl = document.getElementById('pf2Mail');
      var sideMail = document.getElementById('pf2Email');
      if (mailEl) mailEl.value = u.email;
      if (sideMail) sideMail.textContent = u.email;
    }
    if (u.title) {
      var gradeEl = document.getElementById('pf2Grade');
      if (gradeEl) gradeEl.textContent = u.title;
    }
    if (u.avatar) {
      var avatar = document.getElementById('pf2Avatar');
      if (avatar) avatar.src = u.avatar;
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', hydrateUser);
  } else {
    hydrateUser();
  }
})();
