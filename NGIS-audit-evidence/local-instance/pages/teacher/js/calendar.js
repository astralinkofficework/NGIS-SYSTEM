/* ══════════════════════════════════════
   CALENDAR — Mini Grid + Schedule Popup (Teacher Portal)
   ══════════════════════════════════════ */

(function () {
  const grid = document.getElementById('calGrid');
  if (!grid) return;

  const DOW  = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  const START = 0; // Nov 1, 2026 is Sunday
  const DAYS  = 30;
  const TODAY = 1;

  const dots = {
    1:  ['#2455D6', '#059669', '#7c3aed'],
    2:  ['#2455D6', '#2563eb'],
    4:  ['#059669'],
    8:  ['#7c3aed', '#ea580c'],
    12: ['#2455D6'],
    15: ['#059669', '#2563eb'],
    19: ['#ea580c'],
    22: ['#2455D6', '#7c3aed'],
    25: ['#2563eb'],
    28: ['#059669']
  };

  const events = {
    1: [
      { name: 'Grade 11-A · Calculus',      time: '08:00 AM – 10:00 AM · Room 302', color: '#2455D6' },
      { name: 'Grade 10-C · Statistics',    time: '10:15 AM – 12:00 PM · Room 305', color: '#059669' },
      { name: 'Grade 12-B · Pure Math',     time: '01:30 PM – 03:00 PM · Room 304', color: '#2563eb' },
      { name: 'Office Hours & Mentoring',   time: '03:15 PM – 04:30 PM · Room 302', color: '#7c3aed' },
    ],
    2: [
      { name: 'Grade 10-A · Geometry',      time: '08:00 AM – 09:30 AM · Room 301', color: '#7c3aed' },
      { name: 'Grade 11-B · Applied Math',  time: '10:00 AM – 11:30 AM · Room 303', color: '#ea580c' },
    ],
    4: [
      { name: 'Dept Coordination Meeting', time: '03:30 PM – 04:45 PM · Room B',   color: '#059669' },
    ],
    8: [
      { name: 'Grade 11-A Assessment Quiz', time: '08:00 AM – 09:30 AM · Room 302', color: '#2455D6' },
      { name: 'Math Olympiad Practice',    time: '04:30 PM – 05:45 PM · Hall A',   color: '#ea580c' },
    ],
    12: [
      { name: 'Faculty Senate Session',     time: '02:00 PM – 03:30 PM · Main Hall', color: '#2455D6' },
    ],
    15: [
      { name: 'Calculus Mid-Term Revision', time: '08:00 AM – 10:00 AM · Room 302', color: '#059669' },
      { name: 'Statistics Term Review',     time: '10:15 AM – 11:45 AM · Room 305', color: '#2563eb' },
    ],
    22: [
      { name: 'Cambridge AS Moderation',    time: '01:00 PM – 03:00 PM · Boardroom', color: '#7c3aed' },
    ],
  };

  /* ── Popup ── */
  function initPopup() {
    const overlay = document.createElement('div');
    overlay.className = 'cal-popup-overlay';
    overlay.id = 'calPopupOverlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.innerHTML =
      '<div class="cal-popup">' +
        '<div class="cal-popup-head">' +
          '<div class="cal-popup-head-l">' +
            '<span class="cal-popup-icon mi">calendar_today</span>' +
            '<div>' +
              '<div class="cal-popup-month">November 2026</div>' +
              '<div class="cal-popup-date" id="calPopupDate">November 1</div>' +
            '</div>' +
          '</div>' +
          '<button class="cal-popup-close" id="calPopupClose" aria-label="Close">' +
            '<span class="mi">close</span>' +
          '</button>' +
        '</div>' +
        '<div class="cal-popup-body" id="calPopupBody"></div>' +
      '</div>';
    document.body.appendChild(overlay);

    document.getElementById('calPopupClose').addEventListener('click', closePopup);
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) closePopup();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closePopup();
    });
  }

  function openPopup(day, list) {
    document.getElementById('calPopupDate').textContent = 'November ' + day;
    const body = document.getElementById('calPopupBody');
    body.innerHTML = '';

    if (!list || !list.length) {
      const empty = document.createElement('div');
      empty.className = 'cal-popup-empty';
      empty.innerHTML = '<span class="mi">event_busy</span><p>No teaching sessions scheduled</p>';
      body.appendChild(empty);
    } else {
      list.forEach(function (ev) {
        const row  = document.createElement('div');
        row.className = 'cal-popup-ev';
        const dot  = document.createElement('span');
        dot.className = 'cal-popup-ev-dot';
        dot.style.background = ev.color;
        const info = document.createElement('div');
        info.className = 'cal-popup-ev-info';
        const name = document.createElement('div');
        name.className = 'cal-popup-ev-name';
        name.textContent = ev.name;
        const time = document.createElement('div');
        time.className = 'cal-popup-ev-time';
        time.innerHTML = '<span class="mi">schedule</span>' + ev.time;
        info.appendChild(name);
        info.appendChild(time);
        row.appendChild(dot);
        row.appendChild(info);
        body.appendChild(row);
      });
    }

    requestAnimationFrame(function () {
      document.getElementById('calPopupOverlay').classList.add('open');
    });
  }

  function closePopup() {
    const overlay = document.getElementById('calPopupOverlay');
    if (overlay) overlay.classList.remove('open');
  }

  /* ── Sidebar (always-visible quick view) ── */
  function renderSide(day) {
    const side = document.getElementById('calSide');
    if (!side) return;
    side.querySelector('.cal-side-title').textContent = 'Schedule on Nov ' + day;
    side.querySelectorAll('.cal-ev, .cal-no-data').forEach(function (el) { el.remove(); });

    const list = events[day];
    if (!list || !list.length) {
      const nd = document.createElement('div');
      nd.className = 'cal-no-data';
      nd.textContent = 'No teaching sessions';
      side.appendChild(nd);
      return;
    }
    list.forEach(function (ev) {
      const row  = document.createElement('div');
      row.className = 'cal-ev';
      const dot  = document.createElement('span');
      dot.className = 'cal-ev-dot';
      dot.style.background = ev.color;
      const info = document.createElement('div');
      const name = document.createElement('div');
      name.className = 'cal-ev-name';
      name.textContent = ev.name;
      const time = document.createElement('div');
      time.className = 'cal-ev-time';
      time.textContent = ev.time;
      info.appendChild(name);
      info.appendChild(time);
      row.appendChild(dot);
      row.appendChild(info);
      side.appendChild(row);
    });
  }

  function makeEl(tag, cls, text) {
    const el = document.createElement(tag);
    if (cls)  el.className   = cls;
    if (text) el.textContent = text;
    return el;
  }

  /* Day of week headers */
  DOW.forEach(function (d) {
    grid.appendChild(makeEl('div', 'cal-dow', d));
  });

  /* Empty offset cells before day 1 */
  for (let i = 0; i < START; i++) {
    grid.appendChild(makeEl('div', 'cal-day other-month'));
  }

  /* Month days */
  let activeDayEl = null;

  for (let d = 1; d <= DAYS; d++) {
    const dayEl = makeEl('div', 'cal-day');
    dayEl.appendChild(makeEl('span', 'cal-num', d));

    if (dots[d]) {
      const dw = makeEl('div', 'cal-dots');
      dots[d].forEach(function (c) {
        const dot = makeEl('span', 'cal-dot');
        dot.style.background = c;
        dw.appendChild(dot);
      });
      dayEl.appendChild(dw);
    }

    if (d === TODAY) {
      dayEl.classList.add('today');
      activeDayEl = dayEl;
    }

    (function (dayNum) {
      dayEl.addEventListener('click', function () {
        if (activeDayEl) activeDayEl.classList.remove('today');
        dayEl.classList.add('today');
        activeDayEl = dayEl;
        renderSide(dayNum);
        if (window.innerWidth <= 640) {
          openPopup(dayNum, events[dayNum]);
        }
      });
    })(d);

    grid.appendChild(dayEl);
  }

  initPopup();
  renderSide(TODAY);
})();

