# Open questions

Carried from the master prompt's §21 plus items raised while building the front-end.
Front-end placeholders are in place; these need confirmation before the backend phase.

## From the master prompt (§21)
1. **Tenancy** — single school now, or design the `school_id` tenant key from day one?
   _(Recommendation: keep `school_id` everywhere even if single-tenant.)_
2. **Grading scale + GPA formula** — percentage, 4.0, or letter grades? Provide the exact
   mapping and GPA formula. _The UI currently shows percentage + letter + 4.0 GPA as a
   placeholder; nothing is hard-coded into a calculation yet._
3. **Academic structure** — semesters, terms, or trimesters? How many grading periods?
   _The UI assumes two semesters._
4. **Fees** — currency, supported payment methods, and whether an online payment gateway is
   in scope for Phase 3. _The UI shows USD and records-only (gateway deferred), per the brief._
5. **Languages / i18n** — which locales, and is RTL needed? _The profile offers a language
   selector, but no translations are wired yet._
6. **Notification channels (Phase 2)** — in-app only, email, Telegram — and priority order?

## Raised by the front-end build
7. **Role switcher** — keep the demo portal-preview switcher behind a flag for QA, or remove
   it entirely once real auth lands?
8. **Report card** — confirm the exact layout, fields, grading legend, and whether a school
   logo/letterhead and signatures are required on the PDF.
9. **Avatars** — will user photos be uploaded (Supabase Storage), or should we keep
   generated initials as the default?
10. **Timetable periods** — confirm the canonical bell schedule (period times, breaks/lunch)
    and whether rooms/teachers can change per week.
11. **Attendance states** — confirm the set is exactly present / late / absent / excused, and
    who may edit after the fact (and within what window).
12. **Smart alerts thresholds** — confirm the triggers (e.g. "3 consecutive absences",
    "GPA drop") and the exact numeric thresholds for each.
