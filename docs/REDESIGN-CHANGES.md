# NGIS Redesign — Change Log (this pass)

Applied the "Additional Redesign Rules" prompt to the existing system.

## Sidebar (global — assets/js/layout.js + assets/css/app.css)
- Rebuilt from a flat icon list into categorised groups with section titles,
  divider lines, per-item icon chips, active-state indicator, hover animation,
  soft shadow, and rounded corners. Sticky + mobile-collapsible retained.
- Groups: MAIN · LEARNING/MANAGEMENT/TEACHING · COMMUNICATION · ACCOUNT.

## Department-centric structure
- Student & Parent sidebars no longer list Attendance, Assignments,
  Report Cards, Exams, Timetable or Lessons as top-level pages — they now
  live only inside Departments. Their sub-pages keep "Departments" highlighted.
- department.html now shows all SIX modules as box cards (added Exams).
- Teacher & Admin keep their operator tools (they take attendance / upload
  report cards), reorganised into the same clean categories.  ← confirm if you
  want the strict department-only removal applied to them too.

## Report Cards (no GPA) — student-grades.html, parent-grades.html
- Fully rebuilt to the file-based spec: teal hero header + breadcrumb,
  light-gray workspace, 25% / 75% asymmetric two-column grid.
- Left: Grade Book + light-teal academic-year dropdown (2025–2026), Active Term
  list (chevron + green badge), Historical Report Cards (blue badge).
- Right: Grade Book container, List/Table view toggle, subject rows on thin
  gray separators ("No grading period found."). Expanding a subject reveals
  uploaded PDF/PNG/JPG report-card cards with Teacher, Upload Date, View, Download.
- Removed: GPA, percentages, rank, grade scale, trend charts.

## GPA / progress / ranking removal
- Removed from: student dashboard profile strip, departments.html
  ("Academic Overview" progress+GPA panel deleted), department.html stats &
  report-card preview, parent-children.html (tiles + comparison row),
  student-profile.html (Current GPA + Class Rank tiles, "Top 10% GPA" badge),
  and reworded "Top 10% GPA" notification/announcement text to "Honor Roll".
- OUTSTANDING: admin-reports.html still contains GPA analytics (admin reporting
  dashboard) — left for a separate pass.

## New CSS components (assets/css/app.css)
.rc-layout/.rc-panel, .rc-yeardrop, .term-item/.year-badge, .viewtoggle/.vt-btn,
.subject-row/.subj-files, .rc-filecard/.rc-filetype, grouped-sidebar styles.
