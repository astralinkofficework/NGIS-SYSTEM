/* ══════════════════════════════════════
   CALENDAR — Mini Grid + Date Popup
   ══════════════════════════════════════ */

(function () {
  const grid = document.getElementById('calGrid');
  const DOW  = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  const START = 0;
  const DAYS  = 30;
  const TODAY = 25;

  const dots = {
    5:  ['#2563eb'],
    12: ['#22c55e'],
    18: ['#f59e0b', '#ef4444'],
    22: ['#ef4444'],
    25: ['#2563eb', '#22c55e', '#f59e0b'],
    27: ['#f59e0b'],
    29: ['#ef4444'],
  };

  const events = {
    5:  [{ name: 'Math Quiz',         time: '07:30 AM – 08:30 AM', color: '#2563eb' }],
    12: [{ name: 'English Class',     time: '08:45 AM – 09:45 AM', color: '#22c55e' }],
    18: [
      { name: 'Science Lab',          time: '10:00 AM – 11:00 AM', color: '#f59e0b' },
      { name: 'History Test',         time: '02:00 PM – 03:00 PM', color: '#ef4444' },
    ],
    22: [{ name: 'Final Review',      time: '09:00 AM – 10:00 AM', color: '#ef4444' }],
    25: [
      { name: 'Math Class',           time: '07:30 AM – 08:30 AM', color: '#2563eb' },
      { name: 'English Class',        time: '08:45 AM – 09:45 AM', color: '#22c55e' },
      { name: 'Computer Lab',         time: '10:10 AM – 11:10 AM', color: '#f59e0b' },
      { name: 'Physics Class',        time: '01:00 PM – 02:00 PM', color: '#8b5cf6' },
    ],
    27: [{ name: 'Science Fair',      time: '09:00 AM – 12:00 PM', color: '#f59e0b' }],
    29: [{ name: 'History Essay Due', time: '11:59 PM',            color: '#ef4444' }],
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
              '<div class="cal-popup-month">June 2025</div>' +
              '<div class="cal-popup-date" id="calPopupDate">June 25</div>' +
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
    document.getElementById('calPopupDate').textContent = 'June ' + day;
    const body = document.getElementById('calPopupBody');
    body.innerHTML = '';

    if (!list || !list.length) {
      const empty = document.createElement('div');
      empty.className = 'cal-popup-empty';
      empty.innerHTML = '<span class="mi">event_busy</span><p>No data for this date</p>';
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
    side.querySelector('.cal-side-title').textContent = 'Events on Jun ' + day;
    side.querySelectorAll('.cal-ev, .cal-no-data').forEach(function (el) { el.remove(); });

    const list = events[day];
    if (!list || !list.length) {
      const nd = document.createElement('div');
      nd.className = 'cal-no-data';
      nd.textContent = 'No data';
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

  /* ── Build grid ── */
  function makeEl(tag, cls, text) {
    const el = document.createElement(tag);
    if (cls)  el.className   = cls;
    if (text) el.textContent = text;
    return el;
  }

  DOW.forEach(function (d) { grid.appendChild(makeEl('div', 'cal-dow', d)); });

  for (let i = 0; i < START; i++) {
    grid.appendChild(makeEl('div', 'cal-day prev-mo', String(31 - START + 1 + i)));
  }

  let selectedEl = null;

  for (let d = 1; d <= DAYS; d++) {
    const day = d;
    const el  = makeEl('div', 'cal-day' + (d === TODAY ? ' today' : ''), String(d));

    if (dots[d]) {
      const dv = makeEl('div', 'cal-dots');
      dots[d].forEach(function (colour) {
        const dot = makeEl('span', 'cal-dot');
        dot.style.background = colour;
        dv.appendChild(dot);
      });
      el.appendChild(dv);
    }

    el.addEventListener('click', function () {
      if (selectedEl) selectedEl.classList.remove('selected');
      el.classList.add('selected');
      selectedEl = el;
      renderSide(day);
      openPopup(day, events[day]);
    });

    if (d === TODAY) { el.classList.add('selected'); selectedEl = el; }
    grid.appendChild(el);
  }

  const rem = (7 - ((START + DAYS) % 7)) % 7;
  for (let n = 1; n <= rem; n++) {
    grid.appendChild(makeEl('div', 'cal-day next-mo', String(n)));
  }

  initPopup();
  renderSide(TODAY);
})();
