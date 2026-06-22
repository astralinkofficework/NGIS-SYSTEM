import { initTheme } from "./modules/theme.js";
import { login, logout, restore, getState } from "./modules/store.js";
import { defineRoutes, setNotFound, setOutlet, startRouter, navigate } from "./modules/router.js";
import { buildShell } from "./components/shell.js";
import { loginPage } from "./pages/login.js";
import { dashboardPage } from "./pages/dashboard.js";
import { timetablePage } from "./pages/timetable.js";
import { attendancePage } from "./pages/attendance.js";
import { gradesPage } from "./pages/grades.js";
import { assignmentsPage } from "./pages/assignments.js";
import { announcementsPage } from "./pages/announcements.js";
import { documentsPage } from "./pages/documents.js";
import { feesPage } from "./pages/fees.js";
import { peoplePage } from "./pages/people.js";
import { classesPage } from "./pages/classes.js";
import { childrenPage } from "./pages/children.js";
import { systemPage } from "./pages/system.js";
import { profilePage } from "./pages/profile.js";
import { helpPage } from "./pages/help.js";
import { EmptyState } from "./components/ui.js";
import { el } from "./modules/dom.js";

const app = document.getElementById("app");

const ROUTES = {
  "/dashboard": dashboardPage,
  "/timetable": timetablePage,
  "/attendance": attendancePage,
  "/grades": gradesPage,
  "/assignments": assignmentsPage,
  "/announcements": announcementsPage,
  "/documents": documentsPage,
  "/fees": feesPage,
  "/people": peoplePage,
  "/classes": classesPage,
  "/children": childrenPage,
  "/system": systemPage,
  "/profile": profilePage,
  "/help": helpPage,
};

function renderLogin() {
  document.body.classList.add("on-auth");
  app.replaceChildren(loginPage((role) => { login(role); enterApp(); }));
}

function enterApp() {
  document.body.classList.remove("on-auth");
  const { user } = getState();
  const { root, view } = buildShell(user);
  app.replaceChildren(root);

  // Wrap each page so unknown routes get a graceful empty state.
  const routeMap = {};
  for (const [path, fn] of Object.entries(ROUTES)) routeMap[path] = async () => fn();
  defineRoutes(routeMap);
  setNotFound(async () => el("div", { html: EmptyState({ title: "Page not found", msg: "This page doesn't exist yet — it's on the roadmap." }) }));
  setOutlet(view);

  if (!location.hash || location.hash === "#/" || location.hash === "#/login") location.hash = "/dashboard";
  startRouter();
}

// --- global events ----------------------------------------------------
window.addEventListener("ngis:logout", () => { logout(); location.hash = "/login"; renderLogin(); });
window.addEventListener("ngis:switch-role", (e) => { login(e.detail); enterApp(); navigate("/dashboard"); });

// --- boot -------------------------------------------------------------
initTheme();
if (restore()) enterApp(); else renderLogin();
