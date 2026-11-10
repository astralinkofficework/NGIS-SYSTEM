/* ============================================================
   NGIS ERP — Global Action Icon & Dropdown Engine
   Single source of truth for every action SVG in the product.

   Public API
   ----------
   NGIS.icon(name)             -> SVG markup string (for JS templates)
   <span data-ngis-icon="x">   -> auto-hydrated into the SVG on load
                                     and on every dynamic insertion
   NGIS.hydrate(root)          -> hydrate a subtree on demand
   NGIS.ActionDropdown.open/close/toggle/closeAll

   Legacy aliases kept for existing callers:
   window.NGIS_ICONS, window.ActionDropdown

   Vanilla JS only — no build step, no dependencies.
   ============================================================ */

(function () {
  'use strict';

  /* ── 1. Icon catalogue (24×24 outline, stroke-based) ─────────
     Values are the inner markup of a 24×24 viewBox SVG so the
     stroke/fill/size rules always come from action-icons.css.   */
  var PATHS = {
    /* Core action set */
    /* Core navigation & Flaticon mapping additions */
    home: '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>',
    dashboard: '<rect x="3" y="3" width="7" height="9" rx="1"/><rect x="14" y="3" width="7" height="5" rx="1"/><rect x="14" y="12" width="7" height="9" rx="1"/><rect x="3" y="16" width="7" height="5" rx="1"/>',
    attendance: '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
    grades: '<path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/><path d="M9 14l2 2 4-4"/>',
    timetable: '<rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="M8 14h.01"/><path d="M12 14h.01"/><path d="M16 14h.01"/>',
    classes: '<path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>',
    documents: '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>',
    message: '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    view: '<path d="M1 12s4-7.5 11-7.5S23 12 23 12s-4 7.5-11 7.5S1 12 1 12z"/><circle cx="12" cy="12" r="3"/>',
    edit: '<path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4z"/>',
    delete: '<polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/>',
    more: '<circle cx="12" cy="5" r="1.4"/><circle cx="12" cy="12" r="1.4"/><circle cx="12" cy="19" r="1.4"/>',
    download: '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>',
    upload: '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>',
    add: '<line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>',
    minus: '<line x1="5" y1="12" x2="19" y2="12"/>',
    search: '<circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
    filter: '<polygon points="22 3 2 3 10 12.5 10 19 14 21 14 12.5 22 3"/>',
    sort: '<path d="M7 15l5 5 5-5"/><path d="M7 9l5-5 5 5"/>',
    refresh: '<polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10"/><path d="M20.49 15a9 9 0 0 1-14.85 3.36L1 14"/>',
    check: '<polyline points="20 6 9 17 4 12"/>',
    close: '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>',
    print: '<polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/>',
    copy: '<rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>',
    open: '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/>',
    play: '<circle cx="12" cy="12" r="9"/><polygon points="10 8 16 12 10 16 10 8"/>',
    settings: '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.6a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>',
    back: '<line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/>',
    chevronDown: '<polyline points="6 9 12 15 18 9"/>',
    chevronUp: '<polyline points="18 15 12 9 6 15"/>',
    chevronLeft: '<polyline points="15 18 9 12 15 6"/>',
    chevronRight: '<polyline points="9 18 15 12 9 6"/>',

    /* Identity, records & status */
    user: '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    users: '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    lock: '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    unlock: '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/>',
    key: '<path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"/>',
    block: '<circle cx="12" cy="12" r="9"/><line x1="5.6" y1="5.6" x2="18.4" y2="18.4"/>',
    shield: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    mail: '<rect x="2" y="4" width="20" height="16" rx="2"/><polyline points="22 6 12 13 2 6"/>',
    bell: '<path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/>',
    calendar: '<rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
    clock: '<circle cx="12" cy="12" r="9"/><polyline points="12 7 12 12 15 14"/>',
    folder: '<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>',
    file: '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>',
    book: '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
    school: '<path d="M3 10l9-6 9 6"/><path d="M5 10v9a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-9"/><path d="M9 20v-6h6v6"/>',
    archive: '<polyline points="21 8 21 21 3 21 3 8"/><rect x="1" y="3" width="22" height="5" rx="1"/><line x1="10" y1="12" x2="14" y2="12"/>',
    restore: '<polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/>',
    star: '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
    bookmark: '<path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>',
    bookmarkAdded: '<path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/><polyline points="9.5 11 11.5 13 14.5 9.5"/>',
    flag: '<path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" y1="22" x2="4" y2="15"/>',
    link: '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
    send: '<line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>',
    share: '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/>',
    tag: '<path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/>',
    info: '<circle cx="12" cy="12" r="9"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>',
    warning: '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
    eyeOff: '<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/>',
    grid: '<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>',
    list: '<line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/>',
    phone: '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
    mapPin: '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    power: '<path d="M18.36 6.64a9 9 0 1 1-12.73 0"/><line x1="12" y1="2" x2="12" y2="12"/>',
    logout: '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>',
    save: '<path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/>',
    image: '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/>',
    award: '<circle cx="12" cy="8" r="6"/><path d="M15.477 12.89L17 22l-5-3-5 3 1.523-9.11"/>',
    report: '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="8" y1="13" x2="16" y2="13"/><line x1="8" y1="17" x2="16" y2="17"/>',
    comment: '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8z"/>',
    zoomIn: '<circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/>',
    fullscreen: '<path d="M8 3H5a2 2 0 0 0-2 2v3"/><path d="M16 3h3a2 2 0 0 1 2 2v3"/><path d="M21 16v3a2 2 0 0 1-2 2h-3"/><path d="M3 16v3a2 2 0 0 0 2 2h3"/>',
    qr: '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><line x1="14" y1="14" x2="14" y2="21"/><line x1="21" y1="14" x2="17" y2="14"/><line x1="21" y1="21" x2="17" y2="17"/>'
  };

  /* Friendly aliases → canonical key */
  var ALIASES = {
    /* Master action mapping aliases */
    house: 'home', 'home-page': 'home', main: 'home',
    overview: 'dashboard', board: 'dashboard',
    gradebook: 'grades', scoring: 'grades',
    schedule: 'timetable', routine: 'timetable',
    roster: 'users', enrolled: 'users',
    student: 'user', teacher: 'user', principal: 'user', admin: 'shield',
    eye: 'view', 'eye-line': 'view', preview: 'view',
    pencil: 'edit', 'edit-2': 'edit', 'edit-3': 'edit', create: 'edit', write: 'edit',
    trash: 'delete', 'trash-2': 'delete', remove: 'delete', bin: 'delete', 'delete-forever': 'delete',
    ellipsis: 'more', 'more-vertical': 'more', 'more-horizontal': 'more', options: 'more', menu: 'more',
    'external-link': 'open', 'open-in-new': 'open', external: 'open', launch: 'open', linkExternal: 'open',
    'play-circle': 'play', 'play-circle-outline': 'play', 'play-circle-fill': 'play', enter: 'play', start: 'play',
    gear: 'settings', cog: 'settings', config: 'settings', sliders: 'settings',
    plus: 'add', 'plus-circle': 'add', new: 'add',
    magnifier: 'search', 'magnifying-glass': 'search', find: 'search',
    funnel: 'filter', funnelX: 'filter', 'filter-list': 'filter', filterList: 'filter',
    'sort-arrows': 'sort', arrowsSort: 'sort', swap: 'sort',
    reload: 'refresh', sync: 'refresh', 'rotate-cw': 'refresh',
    approve: 'check', ok: 'check', tick: 'check', done: 'check', accept: 'check', confirm: 'check',
    reject: 'close', x: 'close', cancel: 'close', 'x-circle': 'close', deny: 'close',
    printer: 'print', 'content-copy': 'copy', duplicate: 'copy', clone: 'copy',
    'arrow-back': 'back', 'arrow-left': 'back', previous: 'back',
    expand: 'chevronDown', 'expand-more': 'chevronDown', collapse: 'chevronUp', 'expand-less': 'chevronUp',
    'chevron-down': 'chevronDown', 'chevron-up': 'chevronUp', 'chevron-left': 'chevronLeft', 'chevron-right': 'chevronRight',
    person: 'user', profile: 'user', account: 'user', 'account-circle': 'user',
    group: 'users', people: 'users', teams: 'users',
    password: 'key', credential: 'key', credentials: 'key', 'lock-reset': 'key', reset: 'key',
    ban: 'block', suspend: 'block', forbidden: 'block', disabled: 'block',
    security: 'shield', privacy: 'shield', verified: 'shield',
    email: 'mail', message: 'mail', envelope: 'mail',
    notification: 'bell', alarm: 'bell', 'notifications': 'bell', campaign: 'bell',
    schedule: 'calendar', date: 'calendar', timetable: 'calendar',
    time: 'clock', history: 'clock', recent: 'clock',
    directory: 'folder', collections: 'folder', 'folder-open': 'folder',
    document: 'file', docs: 'file', 'file-text': 'file', transcript: 'file', assignment: 'file',
    lesson: 'book', curriculum: 'book', course: 'book', 'menu-book': 'book', subject: 'book', subjects: 'book',
    class: 'school', classes: 'school', 'graduation-cap': 'school', grade: 'school',
    archiveBox: 'archive', 'move-to-archive': 'archive', box: 'archive',
    undo: 'restore', 'restore-page': 'restore', recover: 'restore',
    favorite: 'star', favourite: 'star', featured: 'star', 'workspace-premium': 'star', premium: 'star',
    'bookmark-border': 'bookmark', 'bookmark-added': 'bookmarkAdded', bookmarked: 'bookmarkAdded', 'save-to-library': 'bookmark',
    reportFlag: 'flag', 'report-problem': 'flag', priority: 'flag',
    url: 'link', attach: 'link', 'insert-link': 'link',
    submit: 'send', paperPlane: 'send', publish: 'send', 'send': 'send',
    'share-2': 'share', 'ios-share': 'share', export: 'share',
    label: 'tag', tags: 'tag', category: 'tag', 'sell': 'tag',
    'info-circle': 'info', about: 'info', help: 'info',
    alert: 'warning', 'alert-triangle': 'warning', attention: 'warning',
    'eye-off': 'eyeOff', hide: 'eyeOff', 'visibility-off': 'eyeOff',
    dashboard: 'grid', 'dashboard-view': 'grid', 'view-module': 'grid', cards: 'grid',
    'list-view': 'list', rows: 'list', table: 'list', 'table-rows': 'list',
    telephone: 'phone', call: 'phone', contact: 'phone',
    location: 'mapPin', address: 'mapPin', place: 'mapPin', campus: 'mapPin', 'location-city': 'mapPin',
    shutdown: 'power', offline: 'power', deactivate: 'power',
    signout: 'logout', exit: 'logout', 'log-out': 'logout',
    disk: 'save', download2: 'download', picture: 'image', photo: 'image', avatar: 'image',
    certificate: 'award', medal: 'award', badge: 'award', 'workspace-premium-2': 'award',
    analytics: 'report', 'assessment': 'report', 'bar-chart': 'report', stats: 'report', reports: 'report',

    /* ── Legacy Material Symbols action names ─────────────────
       (underscores are normalised to hyphens by resolve(), so
        material `more_vert` reaches us as `more-vert`)         */
    visibility: 'view',
    'more-vert': 'more', 'more-horiz': 'more', 'more-vert-fill': 'more',
    'file-download': 'download', 'file-upload': 'upload', 'upload-file': 'upload',
    'download-for-offline': 'download', 'download-done': 'download',
    'edit-note': 'edit', 'edit-document': 'edit', 'edit-square': 'edit', 'edit-fill': 'edit',
    'delete-outline': 'delete', 'delete-forever-fill': 'delete',
    'filter-alt': 'filter', 'filter-alt-off': 'filter', 'filter-list-alt': 'filter',
    'swap-vert': 'sort', 'sort-by-alpha': 'sort', 'swap-vert-fill': 'sort',
    'arrow-forward': 'chevronRight', 'arrow-forward-ios': 'chevronRight',
    'arrow-back-ios': 'chevronLeft',
    'calendar-month': 'calendar', calendar_today: 'calendar',
    'power-settings-new': 'power', 'grid-view': 'grid', 'list-alt': 'list',
    'location-on': 'mapPin', 'place-fill': 'mapPin',
    description: 'file', drafts: 'file', 'article': 'file', 'task': 'file',
    unarchive: 'restore', 'settings-backup-restore': 'restore',
    remove: 'minus', 'add-circle': 'add', 'add-box': 'add', 'add-circle-outline': 'add',
    'check-circle': 'check', 'task-alt': 'check', 'done-all': 'check', 'rule': 'check',
    'mark-email-read': 'mail', 'forward-to-inbox': 'send', 'outbox': 'send',
    'person-add': 'user', 'manage-accounts': 'user', 'person-outline': 'user',
    groups: 'users', 'co-present': 'users', 'diversity-3': 'users',
    'admin-panel-settings': 'shield', 'gpp-good': 'shield', 'verified-user': 'shield',
    'lock-open': 'unlock', 'no-accounts': 'block', 'push-pin': 'flag',
    'local-offer': 'tag', tune: 'settings', insights: 'report', 'trending-up': 'report',
    pending: 'clock', 'hourglass-empty': 'clock', 'schedule-send': 'send',
    'toggle-on': 'check', 'toggle-off': 'close', 'launch-fill': 'open',
    'open-in-new-off': 'open', 'system-update-alt': 'refresh', 'autorenew': 'refresh',
    'view-list': 'list', 'view-module-fill': 'grid', 'table-chart': 'report',
    'school-fill': 'school', 'folder-fill': 'folder', 'badge-fill': 'award',
    'notifications-active': 'bell', 'notifications': 'bell', 'grid-on': 'grid',
    'account-tree': 'folder', 'zoom-in': 'zoomIn', 'qr-code': 'qr', 'qr-2': 'qr',
    calculate: 'book', 'function': 'book', 'comment': 'comment', 'chat-bubble': 'comment',
    'chat': 'comment', 'fullscreen': 'fullscreen', 'open-in-full': 'fullscreen',
    'unfolds-more': 'fullscreen', 'add-to-photos': 'fullscreen', 'key-vertical': 'key'
  };

  function resolve(name) {
    if (!name) return null;
    var k = String(name).trim();
    if (PATHS[k]) return k;
    if (ALIASES[k] && PATHS[ALIASES[k]]) return ALIASES[k];
    var lower = k.toLowerCase();
    if (PATHS[lower]) return lower;
    if (ALIASES[lower] && PATHS[ALIASES[lower]]) return ALIASES[lower];
    /* camelCase → kebab fallbacks */
    var kebab = lower.replace(/[_\s]+/g, '-');
    if (PATHS[kebab]) return kebab;
    if (ALIASES[kebab] && PATHS[ALIASES[kebab]]) return ALIASES[kebab];
    var compact = kebab.replace(/-/g, '');
    if (PATHS[compact]) return compact;
    return null;
  }

  function svgMarkup(name, size) {
    var key = resolve(name);
    if (!key) return '';
    size = size || 18;
    return '<svg viewBox="0 0 24 24" width="' + size + '" height="' + size +
      '" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" ' +
      'stroke-linejoin="round" aria-hidden="true" focusable="false">' + PATHS[key] + '</svg>';
  }

  /* ── 2. Hydration ─────────────────────────────────────────── */
  function hydrate(root) {
    root = root || document;
    var nodes = root.querySelectorAll ? root.querySelectorAll('[data-ngis-icon]') : [];
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      var markup = svgMarkup(el.getAttribute('data-ngis-icon'), el.getAttribute('data-icon-size'));
      if (!markup) continue;
      if (el.getAttribute('data-ngis-icon') === 'self') continue;
      el.innerHTML = markup;
    }
  }

  /* ── 2b. Icon-font → SVG normaliser (scoped to action controls) ──
     Converts leftover Material Symbols / Phosphor font glyphs that
     live inside genuine action controls into the shared outline SVG,
     so every row / button action uses one consistent icon system.
     Deliberately skips the sidebar, nav, hamburger and JS-managed
     (id'd) glyph so layout-critical icons are never touched.       */
  var GLYPH_SEL = 'span.material-symbols-outlined, span.material-symbols, i.ph';
  var EXCLUDE_CLOSEST = '#sidebar, .sidebar, [role="navigation"], nav, .bottom-nav, [data-purpose="primary-sidebar"], .hamburger-btn, .mobile-hamburger-btn, .htb-hamburger';
  var EXCLUDE_SELF = '.nav-link-icon, .nav-link-chevron, [class*="ngl-"], [class*="nav-"]';
  var ACTION_CLASS_RE = /action-icon|icon-btn|kebab|row-action|table-action|dropdown-toggle/i;
  var VERB_RE = /view|edit|delet|remove|close|download|upload|print|copy|approv|reject|refresh|reload|export|\bqr\b|zoom|fullscreen|full ?screen|previous|next|more|option|setting|\badd\b|\bnew\b|search|filter|\bsort\b|\bopen\b|\bback\b|expand|collapse|notif|bell|share|send|launch|\bnote|comment|feedback|preview|override|publish|restore|archiv|block|suspend|reset|password|override/i;

  function interactiveAncestor(el) {
    return el.closest ? el.closest('button, a[href], [role="button"], td, th, .action-group') : null;
  }

  function isActionContext(glyph, host) {
    if (!host) return false;
    var hay = (host.getAttribute('title') || '') + ' ' +
      (host.getAttribute('aria-label') || '') + ' ' +
      (host.getAttribute('onclick') || '') + ' ' +
      (host.className || '') + ' ' +
      ((host.textContent || '').slice(0, 40));
    if (ACTION_CLASS_RE.test(host.className || '')) return true;
    return VERB_RE.test(hay);
  }

  function normalizeIconFonts(root) {
    root = root || document;
    if (!root.querySelectorAll) return;
    var glyphs = root.querySelectorAll(GLYPH_SEL);
    for (var i = 0; i < glyphs.length; i++) {
      var g = glyphs[i];
      if (g.hasAttribute('data-ngis-icon')) continue;          /* already a slot   */
      if (g.getAttribute('data-ngis-converted')) continue;     /* already done     */
      if (g.id) continue;                                      /* JS-managed glyph */
      if (g.matches && g.matches(EXCLUDE_SELF)) continue;
      if (g.closest && g.closest(EXCLUDE_CLOSEST)) continue;
      var name = (g.textContent || '').trim();
      if (!name) continue;
      var key = resolve(name);
      if (!key) continue;
      var host = interactiveAncestor(g);
      if (!isActionContext(g, host)) continue;
      var svg = svgMarkup(key);
      if (!svg) continue;
      g.setAttribute('data-ngis-converted', key);
      /* Drop the font classes so the ligature font stops applying,
         keep any sizing/colour utility classes and inherit via 1em. */
      g.classList.remove('material-symbols-outlined', 'material-symbols', 'ph');
      g.classList.add('ngis-icon-inline');
      g.setAttribute('aria-hidden', 'true');
      g.textContent = '';
      g.insertAdjacentHTML('afterbegin', svg);
    }
  }

  /* ── 3. Action dropdown engine ────────────────────────────── */
  var openMenuEl = null;
  var openTriggerEl = null;

  function isVisible(el) {
    return !!(el && el.offsetParent !== null);
  }

  function hasClippingAncestor(el) {
    var p = el.parentElement;
    while (p && p !== document.body && p.nodeType === 1) {
      var st = window.getComputedStyle(p);
      if (st.overflow !== 'visible' || st.overflowX !== 'visible' || st.overflowY !== 'visible') {
        return true;
      }
      p = p.parentElement;
    }
    return false;
  }

  function placeMenu(menu, trigger) {
    var tr = trigger.getBoundingClientRect();
    var rect = menu.getBoundingClientRect();
    var vw = window.innerWidth || document.documentElement.clientWidth;
    var vh = window.innerHeight || document.documentElement.clientHeight;
    var margin = 8;

    var left = tr.right - rect.width;
    if (left < margin) left = margin;
    if (left + rect.width > vw - margin) left = vw - margin - rect.width;

    var top = tr.bottom + 6;
    if (top + rect.height > vh - margin) {
      top = tr.top - rect.height - 6;
      if (top < margin) top = Math.max(margin, vh - margin - rect.height);
    }

    menu.style.left = Math.round(left) + 'px';
    menu.style.top = Math.round(top) + 'px';
  }

  function closeAll() {
    var menus = document.querySelectorAll('.action-dropdown-menu.show');
    for (var i = 0; i < menus.length; i++) {
      menus[i].classList.remove('show', 'is-floating');
      menus[i].style.left = '';
      menus[i].style.top = '';
      var t = menus[i].__ngisTrigger;
      if (t) t.setAttribute('aria-expanded', 'false');
    }
    openMenuEl = null;
    openTriggerEl = null;
  }

  function dropMenuEl(el) {
    if (!el) return null;
    var direct = el.querySelector ? el.querySelector('.action-dropdown-menu') : null;
    if (direct) return direct;
    var dd = el.closest && el.closest('.action-dropdown');
    return dd ? dd.querySelector('.action-dropdown-menu') : null;
  }

  /* ── 4. Standalone-upgradable icon buttons ────────────────── */
  function openMenu(menu, trigger) {
    if (!menu) return;
    var isOpen = menu.classList.contains('show') && openMenuEl === menu;
    closeAll();
    if (isOpen) return;

    menu.classList.add('show');
    menu.__ngisTrigger = trigger || null;
    if (trigger) trigger.setAttribute('aria-expanded', 'true');

    if (hasClippingAncestor(menu)) {
      menu.classList.add('is-floating');
      placeMenu(menu, trigger || menu);
    }
    openMenuEl = menu;
    openTriggerEl = trigger || null;
  }

  function toggle(target, trigger) {
    var menu = dropMenuEl(target);
    if (!menu) return;
    if (menu.classList.contains('show') && openMenuEl === menu) closeAll();
    else openMenu(menu, trigger || target);
  }

  function items(menu) {
    return Array.prototype.filter.call(
      menu.querySelectorAll('.action-dropdown-item'),
      function (it) { return !it.disabled && it.getAttribute('aria-disabled') !== 'true'; }
    );
  }

  function focusItem(menu, index) {
    var list = items(menu);
    if (!list.length) return;
    if (index < 0) index = list.length - 1;
    if (index >= list.length) index = 0;
    list[index].focus();
  }

  /* ── 5. Global listeners (delegated, single instance) ─────── */
  function bind() {
    if (bind._done) return;
    bind._done = true;

    document.addEventListener('click', function (e) {
      var item = e.target.closest && e.target.closest('.action-dropdown-item');
      if (item) {
        /* Choosing an action always closes the menu it belongs to */
        closeAll();
        return;
      }
      var trigger = e.target.closest && e.target.closest('[data-dropdown-toggle], .action-dropdown > [data-ngis-icon="more"], .action-dropdown-toggle');
      if (trigger) {
        e.preventDefault();
        e.stopPropagation();
        toggle(trigger, trigger);
        return;
      }
      if (!e.target.closest || !e.target.closest('.action-dropdown-menu')) {
        closeAll();
      }
    }, true);

    document.addEventListener('keydown', function (e) {
      var menu = openMenuEl;
      if (!menu) return;
      if (e.key === 'Escape') {
        e.preventDefault();
        closeAll();
        if (openTriggerEl && openTriggerEl.focus) openTriggerEl.focus();
        return;
      }
      if (e.key === 'Tab') { closeAll(); return; }
      var active = document.activeElement;
      var insideMenu = menu.contains(active);
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (!insideMenu) focusItem(menu, 0);
        else {
          var list = items(menu);
          focusItem(menu, list.indexOf(active) + 1);
        }
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (!insideMenu) focusItem(menu, -1);
        else {
          var l2 = items(menu);
          focusItem(menu, l2.indexOf(active) - 1);
        }
      } else if (e.key === 'Home') {
        e.preventDefault(); focusItem(menu, 0);
      } else if (e.key === 'End') {
        e.preventDefault(); focusItem(menu, -1);
      }
    });

    /* Trigger keyboard: Enter/Space/ArrowDown opens */
    document.addEventListener('keydown', function (e) {
      var trigger = e.target.closest && e.target.closest('[data-dropdown-toggle], .action-dropdown-toggle');
      if (!trigger) return;
      if (e.key === 'ArrowDown' || e.key === 'Enter' || e.key === ' ') {
        var menu = dropMenuEl(trigger);
        if (!menu) return;
        e.preventDefault();
        openMenu(menu, trigger);
        focusItem(menu, 0);
      }
    });

    var reposition = function () {
      if (openMenuEl && openMenuEl.classList.contains('is-floating') && openMenuEl.__ngisTrigger) {
        placeMenu(openMenuEl, openMenuEl.__ngisTrigger);
      } else if (openMenuEl) {
        closeAll();
      }
    };
    window.addEventListener('resize', reposition, { passive: true });
    window.addEventListener('scroll', reposition, { passive: true, capture: true });
  }

  /* ── 6. Mutation observer: hydrate dynamically added rows ─── */
  function refresh(root) { hydrate(root); normalizeIconFonts(root); }

  function observe() {
    if (!window.MutationObserver || observe._done) return;
    observe._done = true;
    var pending = false;
    var observer = new MutationObserver(function (mutations) {
      if (pending) return;
      pending = true;
      window.requestAnimationFrame(function () {
        pending = false;
        var touched = false;
        for (var i = 0; i < mutations.length; i++) {
          var added = mutations[i].addedNodes;
          for (var j = 0; j < added.length; j++) {
            var node = added[j];
            if (node.nodeType !== 1) continue;
            if (node.matches && node.matches(GLYPH_SEL + ', [data-ngis-icon]')) touched = true;
            if (node.querySelector && node.querySelector(GLYPH_SEL + ', [data-ngis-icon]')) {
              refresh(node); touched = false;
            }
            if (node.hasAttribute && node.hasAttribute('data-ngis-icon') && !node.querySelector('svg')) {
              refresh(node.parentNode || document); touched = false;
            }
          }
        }
        if (touched) refresh(document);
        /* Keep any open menu anchored to its trigger */
        if (openMenuEl && openMenuEl.classList.contains('is-floating') && openMenuEl.__ngisTrigger) {
          placeMenu(openMenuEl, openMenuEl.__ngisTrigger);
        }
      });
    });
    observer.observe(document.documentElement, { childList: true, subtree: true });
  }

  /* ── 7. Boot ──────────────────────────────────────────────── */
  function boot() {
    refresh(document);
    bind();
    observe();
  }

  /* ── 8. Public API ────────────────────────────────────────── */
  var api = {
    icon: svgMarkup,
    iconNames: Object.keys(PATHS),
    hydrate: hydrate,
    hydrateAll: function () { refresh(document); },
    normalize: normalizeIconFonts,
    /* ActionDropdown */
    ActionDropdown: {
      open: function (target, trigger) { var m = dropMenuEl(target); if (m) openMenu(m, trigger || target); },
      close: closeAll,
      closeAll: closeAll,
      toggle: toggle
    }
  };

  window.NGIS = window.NGIS || {};
  window.NGIS.icon = svgMarkup;
  window.NGIS.hydrate = hydrate;
  window.NGIS.icons = PATHS;
  window.NGIS_ICONS = PATHS;
  window.ActionDropdown = api.ActionDropdown;
  window.NGISActionIcons = api.ActionDropdown;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }

  /* Hydrate immediately as well (icon slots may exist before DOMContentLoaded) */
  if (document.readyState === 'interactive' || document.readyState === 'complete') {
    refresh(document);
  }
})();
