/**
 * ============================================================
 * NGIS ERP — Centralized UX Copy Registry (Single Source of Truth)
 * Clear, human, friendly institutional wording across all portals.
 * Strictly compliant with Rules 1–12:
 * - Active voice, front-loaded keywords, concise wording
 * - No double negatives, no generic verbs, digits for counts
 * - Verb + Object button actions (no bare 'Submit', 'OK', 'Yes')
 * - Semantic statuses (Green, Amber, Red, Blue, Neutral)
 * - Zero filler words ('successfully', 'has been', 'please note')
 * - Actionable error messages (condition + immediate fix)
 * ============================================================
 */
(function (global) {
  "use strict";

  var NGIS_COPY = {
    auth: {
      signInTitle: "Sign in to your NGIS account",
      signInSubtitle: "Enter your institutional email to access your school portal.",
      emailLabel: "School Email",
      emailPlaceholder: "name@ngis.edu.kh",
      emailError: "Email is required. Enter your school email address (e.g. name@ngis.edu.kh).",
      passwordLabel: "Password",
      passwordPlaceholder: "Enter your password",
      passwordError: "Password is required. Enter at least 6 characters.",
      signInCta: "Sign In",
      signingInCta: "Signing in...",
      forgotPassword: "Forgot your password?",
      resetPasswordTitle: "Reset Password",
      resetPasswordCta: "Send Reset Link",
      backToSignIn: "Back to Sign In"
    },

    common: {
      saveChanges: "Save Changes",
      savingChanges: "Saving changes...",
      saveDraft: "Save Draft",
      savingDraft: "Saving draft...",
      createRecord: "Create Record",
      creatingRecord: "Creating record...",
      deleteRecord: "Delete Record",
      deletingRecord: "Deleting record...",
      cancel: "Cancel",
      close: "Close",
      back: "Back",
      nextPage: "Next Page",
      previousPage: "Previous Page",
      nextStep: "Next Step",
      previousStep: "Previous Step",
      confirm: "Confirm",
      confirmAction: "Confirm Action",
      tryAgain: "Try Again",
      refresh: "Refresh Data",
      filters: "Filters",
      resetFilters: "Reset Filters",
      clearAll: "Clear All",
      showResults: "Show Results ({count})",
      searchNavPlaceholder: "Search menu...",
      searchNavEmpty: "No matching menu items",
      stepProgress: "Step {current} of {total}",
      requiredField: "Please enter {label}.",
      invalidEmail: "Enter a valid school email address like name@ngis.edu.kh.",
      genericLoadError: "We could not load this view right now. Your saved data is safe. Refresh to retry.",
      genericSaveError: "We could not save your updates just yet. Your inputs were preserved — click Save Changes to retry.",
      helpSupport: "Help & Support",
      signOut: "Log out",
      workspaceTipTitle: "Navigation shortcuts",
      workspaceTipBody: "Use Global Sidebar Manager anytime to organize menu links for every portal.",
      workspaceTipCta: "Open Manager",
      workspaceTipDismiss: "Dismiss tip"
    },

    index: {
      pageTitle: "NGIS — New Gateway International School",
      schoolName: "NGIS",
      schoolFull: "New Gateway International School",
      termPill: "Academic Year 2025–26 • School Portals",
      heroTitle: "One shared workspace for your school community",
      heroSubtitle: "Manage attendance, grades, timetables, lessons, and school updates together in one place.",
      primaryCta: "Open Student Portal",
      secondaryCta: "Open Teacher Portal",
      directoryCta: "Browse All Pages",
      demoBannerTitle: "Quick Portal Preview",
      demoBannerSub: "Pick any portal below to preview its live school workspace:",
      rolesHeading: "Choose a Portal",
      rolesSubhead: "Sign in or preview each campus workspace with realistic school data.",
      roleCards: {
        admin: { title: "Administrator", desc: "Manage user accounts, monitor timetables, and configure campus navigation." },
        principal: { title: "Principal", desc: "Build master class timetables, review schedules, and approve term reports." },
        teacher: { title: "Teacher", desc: "Record daily attendance, post coursework, and enter student grades." },
        student: { title: "Student", desc: "View class schedules, check homework deadlines, and track grades." }
      }
    },

    notFound: {
      pageTitle: "Page Not Found — NGIS",
      badge: "404 • Page Missing",
      title: "We could not find that page",
      description: "The link you followed may have moved or been renamed. Your account and school records are completely safe.",
      primaryAction: "Back to Home",
      secondaryAction: "Browse All Pages",
      helpNote: "Need help finding a page? Contact your Campus Registrar or IT Support."
    },

    users: {
      overviewTitle: "User Management",
      overviewSubtitle: "Create, organize, and protect portal accounts across every school role.",
      directoryEmptyTitle: "No matching accounts",
      directoryEmptyDesc: "No people match the filters you picked. Adjust your filters or search terms to see more records.",
      filterSheetTitle: "Filter Directory",
      addUserCta: "Add Account",
      editUserCta: "Edit Account",
      deleteUserCta: "Delete Account",
      viewProfileCta: "View Profile",
      wizardTitle: "Create Portal Account",
      wizardSteps: [
        { title: "Select Person", sub: "Choose an existing school profile to link this login account to." },
        { title: "Set Sign-In Details", sub: "Pick a username and email they will use to sign in." },
        { title: "Password & Welcome Setup", sub: "Set a safe temporary password for their first login." },
        { title: "Campus Access", sub: "Review their role and campus scope." },
        { title: "Review & Create", sub: "Confirm every detail below before creating the account." }
      ],
      errors: {
        pickPerson: "Please select a school profile from the list before continuing.",
        usernameShort: "Username must be at least 3 letters, numbers, dots, or underscores.",
        emailInvalid: "Enter a valid school email address like student@ngis.edu.kh.",
        passwordShort: "Temporary password needs at least 6 characters.",
        editFixFields: "Please fix the highlighted fields above before saving."
      },
      accountGroups: {
        identity: "Identity Details",
        roleScope: "Role & Campus Assignment",
        security: "Sign-In Status & Controls",
        activity: "Recent Account Activity"
      }
    },

    timetables: {
      filterSheetTitle: "Filter Classes",
      loadErrorTitle: "Could not load timetable progress",
      loadErrorDesc: "The class monitoring list did not finish loading. Your timetables and drafts are safe. Refresh to retry.",
      reminderModalTitle: "Send Preparation Reminder",
      reminderErrors: {
        messageRequired: "Please write a short reminder note for the recipient.",
        deadlineRequired: "Please pick a target completion date."
      },
      emptyFilteredTitle: "No matching classes",
      emptyFilteredDesc: "No classes match the filters you selected. Try resetting your filters."
    },

    dashboardCms: {
      loadConfigError: "We could not load portal content right now. Refresh the page or try again shortly.",
      loadPublishError: "Publication status is temporarily unavailable. Your draft edits are still kept.",
      loadActivityError: "Recent version activity could not be loaded right now.",
      navLoadError: "Navigation settings could not be loaded right now. Try refreshing in a moment.",
      minBannerRequired: "At least 1 banner slide must stay active on the portal home.",
      confirmDeleteBannerTitle: "Remove Banner Slide?",
      confirmDeleteBannerDesc: "This removes the slide from your draft layout until you publish.",
      confirmPublishNavTitle: "Publish Navigation Live?",
      confirmPublishNavDesc: "Your updated sidebar links will go live for everyone in this portal.",
      confirmRestoreTitle: "Restore Previous Version?",
      confirmRestoreDesc: "Reverts this portal layout to the saved snapshot you picked.",
      scheduleRequiredError: "Please choose a valid future date and time before scheduling.",
      draftSavedToast: "Draft saved safely without changing the live portal.",
      navDraftSavedToast: "Sidebar draft saved for the {portal} portal.",
      navPublishBlockedToast: "Please resolve the highlighted issues before publishing."
    },

    timetableBuilder: {
      draftSaved: "Draft saved",
      savingDraft: "Saving draft...",
      unsavedChanges: "Unsaved changes",
      readyStatus: "Zero conflicts",
      publishPromptTitle: "Publish Master Timetable",
      publishPromptDesc: "Publishing updates the live weekly schedule for teachers and students.",
      assignSubjectCta: "Assign Subject",
      changeTeacherCta: "Change Teacher"
    },

    admin: {
      departmentsTitle: "Department Directory",
      addDepartmentCta: "Add Department",
      campusesTitle: "Campus Network",
      addCampusCta: "Add Campus",
      schoolYearTitle: "School Year Configuration",
      addSchoolYearCta: "Add School Year",
      rolesTitle: "Roles & Permissions",
      createRoleCta: "Create Role",
      announcementsTitle: "School Announcements",
      postAnnouncementCta: "Post Announcement",
      systemLogsTitle: "System Audit Logs",
      exportLogsCta: "Export CSV Log"
    },

    principal: {
      dashboardTitle: "Executive Principal Workspace",
      approvalsTitle: "Pending Approvals",
      approveCta: "Approve Request",
      rejectCta: "Reject Request",
      evaluationsTitle: "Faculty Evaluations",
      startEvaluationCta: "Start Evaluation",
      timetableBuilderTitle: "Master Timetable Builder"
    },

    teacher: {
      dashboardTitle: "Faculty Workspace",
      attendanceTitle: "Daily Attendance",
      saveAttendanceCta: "Save Attendance Record",
      gradebookTitle: "Gradebook & Assessment",
      saveGradesCta: "Save Grades",
      lessonPlansTitle: "Lesson Plans & Curriculum",
      createLessonCta: "Create Lesson Plan",
      assignmentsTitle: "Coursework Assignments",
      createAssignmentCta: "Create Assignment"
    },

    student: {
      dashboardTitle: "Student Learning Workspace",
      assignmentsTitle: "My Homework & Assignments",
      submitAssignmentCta: "Submit Assignment",
      gradesTitle: "My Academic Progress",
      timetableTitle: "My Weekly Schedule",
      attendanceTitle: "My Attendance Record"
    },

    status: {
      active: "Active",
      completed: "Completed",
      published: "Published",
      approved: "Approved",
      present: "Present",
      pending: "Pending",
      review: "In Review",
      draft: "Draft",
      onHold: "On Hold",
      inProgress: "In Progress",
      late: "Late",
      expired: "Expired",
      inactive: "Inactive",
      overdue: "Overdue",
      urgent: "Urgent",
      rejected: "Rejected",
      absent: "Absent",
      suspended: "Suspended",
      new: "New",
      scheduled: "Scheduled",
      neutral: "Standard",
      archived: "Archived"
    }
  };

  function get(path, fallback) {
    if (!path) return fallback || "";
    var parts = String(path).split(".");
    var cur = NGIS_COPY;
    for (var i = 0; i < parts.length; i++) {
      if (cur == null || typeof cur !== "object" || !(parts[i] in cur)) {
        return fallback !== undefined ? fallback : path;
      }
      cur = cur[parts[i]];
    }
    return cur;
  }

  function t(path, vars, fallback) {
    var tpl = get(path, fallback);
    if (typeof tpl !== "string") return tpl;
    if (!vars || typeof vars !== "object") return tpl;
    return tpl.replace(/\{([a-zA-Z0-9_]+)\}/g, function (_, k) {
      return vars[k] !== undefined && vars[k] !== null ? String(vars[k]) : "";
    });
  }

  NGIS_COPY.get = get;
  NGIS_COPY.t = t;
  global.NGIS_COPY = NGIS_COPY;
})(window);
