# NGIS Teacher Portal - Quick Reference Guide

## Overview
Three new academic management pages for the Teacher Portal, accessible from the teacher sidebar under ACADEMIC TOOLS.

## New Pages

### 1. Roster & Profiles (`pages/teacher/teacher-roster.html`)
**Purpose:** Student directory with search and filtering  
**Sidebar Link:** My Class → View Roster  
**Access:** Teachers can view students in their assigned classes

**Features:**
- Search by name or student ID
- Filter by class, status, or sort order
- Pagination (10 students per page)
- Dark mode support
- Mobile card view

**Key Elements:**
```html
<!-- Main table -->
<table id="rosterTable">...</table>

<!-- Mobile list -->
<div id="rosterMobileList">...</div>

<!-- Filters -->
<input id="searchInput">
<select id="classFilter">
<select id="statusFilter">
<select id="sortBy">
```

**API Used:**
- `GET /api/students` - Fetch student list

---

### 2. Student Work Submissions (`pages/teacher/teacher-submissions.html`)
**Purpose:** Review student work and provide feedback  
**Sidebar Link:** Teaching & Learning → Student Submissions  
**Access:** Teachers can review submissions from their classes

**Features:**
- View all student submissions for assignments
- Filter by student, assignment, class, or status
- Review modal with feedback form
- Grade input (0-100)
- File preview section
- Dark mode support
- Mobile list view

**Key Elements:**
```html
<!-- Submission table -->
<table id="submissionsTable">...</table>

<!-- Review modal -->
<div class="modal-overlay" id="reviewModal">
  <textarea id="feedbackInput">
  <input id="gradeInput" type="number">
  <button id="saveReviewBtn">
</div>

<!-- Mobile submissions -->
<div id="submissionsMobileList">...</div>
```

**API Used:**
- `GET /api/assignments` - Fetch assignments with submissions
- `POST /api/assignments/:id/grade` - Save grade and feedback

**Key Functions:**
```javascript
window.openReview(submissionId)  // Opens review modal
```

---

### 3. Teacher Gradebook (`pages/teacher/teacher-gradebook.html`)
**Purpose:** Manage student grades inline  
**Sidebar Link:** Academic Tools → Gradebook  
**Access:** Teachers can edit grades for their classes

**Features:**
- Class selector
- Subject and term filters
- Inline grade editing (0-100)
- Total, average, and final grade calculations
- Unsaved changes indicator
- Save all changes at once
- Dark mode support
- Mobile grade cards

**Key Elements:**
```html
<!-- Class selector -->
<select id="classSelector">

<!-- Grade table -->
<table class="gradebook-table">
  <!-- Students as rows, assessments as columns -->
</table>

<!-- Save button -->
<button id="saveChangesBtn">

<!-- Unsaved indicator -->
<span id="unsavedIndicator">Unsaved Changes</span>
```

**API Used:**
- `GET /api/grades` - Fetch existing grades
- `POST /api/grades` - Save grade updates

**Key Functions:**
```javascript
window.handleGradeChange(input)  // Tracks modified grades
```

---

## Sidebar Navigation

The Gradebook appears in the teacher sidebar under **ACADEMIC TOOLS**:
```
ACADEMIC TOOLS
├── Gradebook ⭐ NEW
├── Timetable
├── Class Reports
└── Class Settings
```

**Location in Code:**
- File: `assets/js/layout.js` (line ~124)
- Configuration:
```javascript
{ id:"gradebook", label:"Gradebook", icon:"grade", 
  href:"pages/teacher/teacher-gradebook.html" }
```

---

## Dark Mode

All pages support light/dark theme switching:

**How it Works:**
1. Theme stored in `localStorage` as `ngis-theme`
2. Automatically applied on page load
3. User can toggle theme using existing system switcher
4. CSS classes use Tailwind `dark:` prefix

**Example:**
```html
<!-- Light mode (default) -->
<div class="bg-white dark:bg-slate-800">
  <!-- White background in light mode, dark slate in dark mode -->
</div>
```

---

## Responsive Design

### Breakpoints
- **Mobile:** < 640px (hamburger menu visible)
- **Tablet:** 640px - 1024px (adjusted layouts)
- **Desktop:** > 1024px (full interface)

### Mobile Features
- Hamburger menu for navigation
- Card-based layouts instead of tables
- Vertical form layouts
- Touch-friendly buttons (44px minimum)
- Scrollable tables without page overflow

**Mobile Class Selectors:**
```html
<!-- Desktop -->
<select id="classFilter">

<!-- Mobile (mirrors desktop) -->
<select id="classFilterMobile">
```

**JavaScript Sync:**
```javascript
// Keep selectors in sync
document.getElementById('classFilter').addEventListener('change', (e) => {
  document.getElementById('classFilterMobile').value = e.target.value;
});
```

---

## Authentication & Authorization

### How It Works
1. User logs in via existing auth system (`auth.js`)
2. JWT token stored in `localStorage` as `ngis_token`
3. Backend validates token on every API request
4. Access scoped to teacher's classes/students

### Protected Operations
```javascript
// Fetch with auth header (handled by auth.js)
const response = await fetch('/api/students', {
  headers: { 'Authorization': `Bearer ${token}` }
});
```

### Server-Side Checks
```
✅ Teacher can only view their own class students
✅ Teacher can only grade their own assignments
✅ Grade updates validated on backend
✅ No cross-class data access allowed
```

---

## Form Validation

### Grade Inputs
- **Range:** 0-100
- **Validation:** Numeric only
- **Feedback:** Invalid values rejected on submit

```javascript
const gradeInput = document.getElementById('gradeInput');
gradeInput.min = "0";
gradeInput.max = "100";
```

### Search Inputs
- **Case-insensitive** text matching
- **Works with:** Student name, ID, assignment title
- **Real-time** filtering as user types

### Modal Forms
```javascript
// Validate before save
if (!feedback && !grade) {
  alert('Please enter feedback or grade');
  return;
}
```

---

## API Integration Reference

### Roster Page
```
GET /api/students
├── Returns: Array of student objects
├── Scope: Only teacher's assigned students
└── Fallback: Mock data if API unavailable

Response:
{
  data: [
    { id, first_name, last_name, grade, class_id, 
      gpa, attendance_rate, status, email }
  ]
}
```

### Submissions Page
```
GET /api/assignments
├── Returns: Array of assignments with submission data
├── Scope: Only teacher's assignments
└── Includes: submission status, scores, submitted_at

POST /api/assignments/:id/grade
├── Body: { studentId, score, feedback }
├── Returns: Updated submission record
└── Side-effects: Creates notification for student
```

### Gradebook Page
```
GET /api/grades
├── Returns: Array of grade records
├── Scope: Only teacher's grades
└── Includes: student_id, score, max_score, letter_grade

POST /api/grades
├── Body: { studentId, subjectId, classId, score, comments }
├── Returns: Created/updated grade record
└── Side-effects: Audit log created
```

---

## Performance Tips

### For Developers
1. **Avoid N+1 queries** - Batch API calls where possible
2. **Lazy load modals** - Don't render until needed
3. **Debounce search** - Add delay before filtering
4. **Cache results** - Store in-memory for quick access
5. **Virtualize tables** - For large datasets (50+ rows)

### For Users
1. **Clear filters** - Use "Clear Filters" button to reset
2. **Use pagination** - Don't load all data at once
3. **Save frequently** - Don't lose unsaved gradebook changes
4. **Check network** - Verify API connection if slow

---

## Troubleshooting

### Issue: Pages not loading
**Solution:** 
- Check server is running
- Verify paths are correct
- Check browser console for errors

### Issue: Sidebar doesn't show Gradebook
**Solution:**
- Hard refresh browser (Ctrl+Shift+R)
- Check layout.js has Gradebook entry
- Verify user is logged in as teacher

### Issue: Dark mode not working
**Solution:**
- Clear browser cache
- Check localStorage has `ngis-theme` key
- Verify `data-theme="light"` on HTML element

### Issue: Grades not saving
**Solution:**
- Check internet connection
- Verify API endpoint is responding
- Check browser console for error messages
- Ensure all required fields are filled

### Issue: Mobile view broken
**Solution:**
- Check viewport meta tag is present
- Disable browser zoom
- Test with Chrome DevTools mobile emulation
- Clear CSS cache

---

## Code Structure

### File Organization
```
pages/teacher/
├── teacher-roster.html         (Student directory)
├── teacher-submissions.html    (Submission pipeline)
├── teacher-gradebook.html      (Grade management)
├── teacher-classes.html        (Updated with Roster link)
├── teacher-attendance.html     (Fixed responsive design)
└── _auth-bootstrap.js          (Auth initialization)

assets/js/
├── layout.js                   (Sidebar navigation)
├── auth.js                     (Authentication)
├── protect.js                  (Route protection)
└── hero.js                     (Header rendering)

backend/routes/
├── students.js                 (Student API)
├── assignments.js              (Assignment/submission API)
└── grades.js                   (Grades API)
```

### Design Patterns

**Self-Initializing IIFE:**
```javascript
(function() {
  // Private state
  let allStudents = [];
  
  // Public methods
  window.openReview = function(id) { /* ... */ };
  
  // Initialize on load
  document.addEventListener('DOMContentLoaded', () => {
    loadData();
  });
})();
```

**Two-Way Filter Sync:**
```javascript
// Keep desktop and mobile filters in sync
document.getElementById('classFilter').addEventListener('change', (e) => {
  document.getElementById('classFilterMobile').value = e.target.value;
  applyFilters();
});
```

---

## Browser DevTools Tips

### Check Page Health
```javascript
// In console:
console.log(window.NGIS_CURRENT_USER);  // Verify user is logged in
console.log(localStorage.getItem('ngis_token'));  // Check token
console.log(localStorage.getItem('ngis-theme'));  // Check theme
```

### Debug API Calls
```javascript
// Monitor network tab for /api/* requests
// Should see Bearer token in Authorization header
// Responses should include "data" field
```

### Test Dark Mode
```javascript
// In console:
localStorage.setItem('ngis-theme', 'dark');
location.reload();
```

---

## Future Enhancement Ideas

1. **Grade Weighting** - Support weighted assessments
2. **Bulk Import** - CSV grade upload
3. **Export Grades** - PDF/Excel download
4. **Analytics** - Grade distribution charts
5. **Notifications** - Auto-alert parents on grade changes
6. **Comments** - Rich text feedback with formatting
7. **Rubrics** - Structured grading templates
8. **Sync** - Real-time updates via WebSocket

---

## Support Resources

- **IMPLEMENTATION_REPORT.md** - Detailed technical documentation
- **AGENTS.md** - Design system and critical rules
- **backend/routes/*.js** - API documentation with comments
- **pages/teacher/teacher.html** - Existing dashboard (reference)

---

**Last Updated:** October 29, 2026  
**Version:** 1.0 MVP  
**Status:** ✅ Production Ready
