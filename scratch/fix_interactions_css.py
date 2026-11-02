with open('assets/css/interactions.css', 'r', encoding='utf-8') as f:
    c = f.read()

target = """/* ============================================================
   TOUCH: Neutralize all tap overlays — no colored flash
   The rounded colored overlay seen when touching a card is
   the browser-native tap highlight plus latched :hover states
   on touch devices. Cards must stay surface-colored on tap.
   ============================================================ */

/* 1. Kill the native rounded tap-highlight overlay everywhere */
*,
*::before,
*::after {
  -webkit-tap-highlight-color: transparent !important;
}

/* 2. Pressed cards hold their neutral surface — no color change */
.card:active, .portal-card:active, .stat-card:active, .module-card:active,
.dept-card:active, .hub-card:active, .card-hover:active, .card-hover-sm:active,
.candidate-card:active, .club-card:active, .cert-card:active, .role-card:active,
.news-card:active, .subj-card:active, .cal-card:active, .att-card:active,
.ql-card:active, .pf-card:active, .task-card:active, .lesson-card:active,
.ann-card:active, .exam-card:active, .rc-filecard:active, .ov-deadline-card:active,
.ov-task-card:active, .dash-kpi-card:active, .sh-card:active, .box:active,
.panel:active, .widget:active, [class~="card"]:active {
  background-color: #ffffff !important;
  border-color: #E5E5E8 !important;
  box-shadow: none !important;
  transform: none !important;
  translate: none !important;
  scale: 1 !important;
}

/* 3. On touch-only devices, taps latch :hover styles — hold them neutral too */
@media (hover: none), (pointer: coarse) {
  .card:hover, .portal-card:hover, .stat-card:hover, .module-card:hover,
  .dept-card:hover, .hub-card:hover, .task-card:hover, .lesson-card:hover,
  .ann-card:hover, .exam-card:hover, .club-card:hover, .news-card:hover,
  [class~="card"]:hover, [class*="-card"]:hover {
    background-color: #ffffff !important;
    border-color: #E5E5E8 !important;
    box-shadow: none !important;
    transform: none !important;
    translate: none !important;
    scale: 1 !important;
  }
}"""

replacement = """/* ============================================================
   ZERO CARD OVERLAYS & NEUTRAL CARD INTERACTION ENGINE
   Strict 5-Color Palette: Navy #202F63, Burgundy #92243D,
   White #FFFFFF, Black #000000, Soft Gray #F3F3F5.
   Cards remain visually neutral on hover, touch, click, and active.
   Zero colored circular ripples, no gradient overlays, no tints,
   and zero child badge flashes.
   ============================================================ */

/* 1. Global kill on all native tap highlights and touch ripples */
*,
*::before,
*::after {
  -webkit-tap-highlight-color: transparent !important;
  -webkit-touch-callout: none;
}

/* 2. Strip ALL pseudo-element overlays (circles, ripples, gradients) from cards */
:where(
  .card, .ws-card, .module-card, .dept-card, .hub-card, .stat-card, .stat,
  .lesson-card, .ann-card, .exam-card, .candidate-card, .club-card, .cert-card,
  .portal-card, .role-card, .news-card, .subj-card, .cal-card, .att-card, .ql-card,
  .pf-card, .task-card, .sh-card, .sh-stat-card, .ov-profile, .ov-upcoming, .ov-deadlines,
  .ov-inner-panel, .ov-deadline-panel, .ov-deadline-card, .ov-task-card, .dash-kpi-card,
  .oak-preview-modal-card, .oak-modal-card, .id-card-wrapper,
  .box, .panel, .widget, .demo-pill, [class~="card"], [class*="-card"]
)::before,
:where(
  .card, .ws-card, .module-card, .dept-card, .hub-card, .stat-card, .stat,
  .lesson-card, .ann-card, .exam-card, .candidate-card, .club-card, .cert-card,
  .portal-card, .role-card, .news-card, .subj-card, .cal-card, .att-card, .ql-card,
  .pf-card, .task-card, .sh-card, .sh-stat-card, .ov-profile, .ov-upcoming, .ov-deadlines,
  .ov-inner-panel, .ov-deadline-panel, .ov-deadline-card, .ov-task-card, .dash-kpi-card,
  .oak-preview-modal-card, .oak-modal-card, .id-card-wrapper,
  .box, .panel, .widget, .demo-pill, [class~="card"], [class*="-card"]
)::after {
  content: none !important;
  display: none !important;
  background: transparent !important;
}

/* 3. Keep cards visually neutral and unmodified during hover, active, focus, and touch */
:where(
  .card, .ws-card, .module-card, .dept-card, .hub-card, .stat-card, .stat,
  .lesson-card, .ann-card, .exam-card, .candidate-card, .club-card, .cert-card,
  .portal-card, .role-card, .news-card, .subj-card, .cal-card, .att-card, .ql-card,
  .pf-card, .task-card, .sh-card, .sh-stat-card, .card-hover, .card-hover-sm,
  .ov-profile, .ov-upcoming, .ov-deadlines, .ov-inner-panel, .ov-deadline-panel,
  .ov-deadline-card, .ov-task-card, .dash-kpi-card, .sh-request-item,
  .box, .panel, .widget, .demo-pill, [class~="card"], [class*="-card"]
):hover,
:where(
  .card, .ws-card, .module-card, .dept-card, .hub-card, .stat-card, .stat,
  .lesson-card, .ann-card, .exam-card, .candidate-card, .club-card, .cert-card,
  .portal-card, .role-card, .news-card, .subj-card, .cal-card, .att-card, .ql-card,
  .pf-card, .task-card, .sh-card, .sh-stat-card, .card-hover, .card-hover-sm,
  .ov-profile, .ov-upcoming, .ov-deadlines, .ov-inner-panel, .ov-deadline-panel,
  .ov-deadline-card, .ov-task-card, .dash-kpi-card, .sh-request-item,
  .box, .panel, .widget, .demo-pill, [class~="card"], [class*="-card"]
):active,
:where(
  .card, .ws-card, .module-card, .dept-card, .hub-card, .stat-card, .stat,
  .lesson-card, .ann-card, .exam-card, .candidate-card, .club-card, .cert-card,
  .portal-card, .role-card, .news-card, .subj-card, .cal-card, .att-card, .ql-card,
  .pf-card, .task-card, .sh-card, .sh-stat-card, .card-hover, .card-hover-sm,
  .ov-profile, .ov-upcoming, .ov-deadlines, .ov-inner-panel, .ov-deadline-panel,
  .ov-deadline-card, .ov-task-card, .dash-kpi-card, .sh-request-item,
  .box, .panel, .widget, .demo-pill, [class~="card"], [class*="-card"]
):focus {
  background: #ffffff !important;
  background-color: #ffffff !important;
  border-color: #E5E5E8 !important;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04) !important;
  transform: none !important;
  translate: none !important;
  scale: 1 !important;
  outline: none !important;
  -webkit-tap-highlight-color: transparent !important;
}

/* 4. Neutralize child icon badges and shapes inside cards */
:where(
  .card, .ws-card, .module-card, .dept-card, .hub-card, .stat-card,
  .group, [class*="card"]
):hover [class*="group-hover:bg-"],
:where(
  .card, .ws-card, .module-card, .dept-card, .hub-card, .stat-card,
  .group, [class*="card"]
):active [class*="group-hover:bg-"],
:where(
  .card, .ws-card, .module-card, .dept-card, .hub-card, .stat-card,
  .group, [class*="card"]
):focus [class*="group-hover:bg-"] {
  background-color: #F3F3F5 !important;
  color: #202F63 !important;
  box-shadow: none !important;
  transform: none !important;
}"""

target_crlf = target.replace('\r\n', '\n').replace('\n', '\r\n')
replacement_crlf = replacement.replace('\r\n', '\n').replace('\n', '\r\n')

if target in c:
    c = c.replace(target, replacement)
    print('Replaced in interactions.css (LF)')
elif target_crlf in c:
    c = c.replace(target_crlf, replacement_crlf)
    print('Replaced in interactions.css (CRLF)')
else:
    print('Target not matched in interactions.css')

with open('assets/css/interactions.css', 'w', encoding='utf-8') as f:
    f.write(c)

