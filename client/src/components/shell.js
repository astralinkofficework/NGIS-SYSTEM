import { icon } from "../modules/icons.js";
import { el, initials } from "../modules/dom.js";
import { school, roleLabels, notifications, accounts, roles } from "../modules/mockData.js";
import { toggleTheme, getTheme } from "../modules/theme.js";
import { navigate, setOnChange } from "../modules/router.js";
import { Avatar } from "./ui.js";

// Per-role navigation. Order matters.
const NAV = {
  student: [
    ["/dashboard", "Dashboard", "grid"],
    ["/timetable", "Timetable", "calendar"],
    ["/attendance", "Attendance", "checkCircle"],
    ["/grades", "Grades & exams", "award"],
    ["/assignments", "Assignments", "clipboard"],
    ["/documents", "My documents", "folder"],
    ["/announcements", "Announcements", "megaphone"],
  ],
  teacher: [
    ["/dashboard", "Dashboard", "grid"],
    ["/classes", "My classes", "users"],
    ["/attendance", "Attendance", "checkCircle"],
    ["/grades", "Grades", "award"],
    ["/assignments", "Assignments", "clipboard"],
    ["/timetable", "Timetable", "calendar"],
    ["/announcements", "Announcements", "megaphone"],
  ],
  parent: [
    ["/dashboard", "Dashboard", "grid"],
    ["/children", "My children", "users"],
    ["/attendance", "Attendance", "checkCircle"],
    ["/grades", "Grades & exams", "award"],
    ["/assignments", "Assignments", "clipboard"],
    ["/fees", "Fees & payments", "wallet"],
    ["/announcements", "Announcements", "megaphone"],
    ["/documents", "Documents", "folder"],
  ],
  admin: [
    ["/dashboard", "Dashboard", "grid"],
    ["/people", "People", "users"],
    ["/classes", "Classes & subjects", "book"],
    ["/grades", "Academics", "award"],
    ["/fees", "Fees & payments", "wallet"],
    ["/announcements", "Announcements", "megaphone"],
  ],
  super_admin: [
    ["/dashboard", "Dashboard", "grid"],
    ["/people", "People", "users"],
    ["/system", "System health", "server"],
    ["/announcements", "Announcements", "megaphone"],
  ],
};

const SECTION_LABEL = {
  student: "Academics", teacher: "Teaching", parent: "Family", admin: "Administration", super_admin: "Operations",
};

export function buildShell(user) {
  const root = el("div", { class: "app" });

  // ---- Sidebar -------------------------------------------------------
  const aside = el("aside", { class: "sidebar" });
  const nav = (NAV[user.role] || []).map(([path, label, ic]) =>
    `<a class="nav-item" href="#${path}" data-path="${path}">${icon(ic)}<span>${label}</span></a>`
  ).join("");

  aside.innerHTML = `
    <div class="brand">
      <div class="brand-mark">${icon("graduation")}</div>
      <div class="brand-text">
        <strong>${school.short}</strong>
        <span>${school.year}</span>
      </div>
    </div>
    <nav class="nav" aria-label="Primary">
      <div class="nav-section">${SECTION_LABEL[user.role] || ""}</div>
      ${nav}
      <div class="nav-section" style="margin-top:auto">Account</div>
      <a class="nav-item" href="#/profile" data-path="/profile">${icon("user")}<span>Profile</span></a>
      <a class="nav-item" href="#/help" data-path="/help">${icon("help")}<span>Help center</span></a>
    </nav>`;

  // ---- Topbar --------------------------------------------------------
  const header = el("header", { class: "topbar" });
  header.innerHTML = `
    <button class="btn btn-quiet btn-icon menu-toggle" aria-label="Toggle menu">${icon("menu")}</button>
    <div class="search topbar-search">
      ${icon("search")}
      <input class="input" type="search" placeholder="Search students, classes, announcements…" aria-label="Global search">
      <kbd class="kbd">/</kbd>
    </div>
    <div class="topbar-actions row gap-2">
      <div class="role-switch" title="Preview another portal (demo)">
        <button class="btn btn-ghost btn-sm role-btn">${icon("layers")}<span>${roleLabels[user.role]}</span>${icon("chevronDown")}</button>
      </div>
      <button class="btn btn-quiet btn-icon theme-btn" aria-label="Toggle theme">${icon(getTheme() === "dark" ? "sun" : "moon")}</button>
      <button class="btn btn-quiet btn-icon notif-btn" aria-label="Notifications" style="position:relative">
        ${icon("bell")}<span class="notif-dot"></span>
      </button>
      <button class="profile-btn">${Avatar(user.name, "sm")}</button>
    </div>`;

  // ---- Layout --------------------------------------------------------
  const main = el("main", { class: "main" });
  const view = el("div", { class: "view", id: "view" });
  main.append(header, view);
  root.append(aside, main);

  const scrim = el("div", { class: "sidebar-scrim" });
  root.append(scrim);

  // ---- Interactions --------------------------------------------------
  const openSidebar = () => { aside.classList.add("open"); scrim.classList.add("show"); };
  const closeSidebar = () => { aside.classList.remove("open"); scrim.classList.remove("show"); };
  header.querySelector(".menu-toggle").addEventListener("click", () =>
    aside.classList.contains("open") ? closeSidebar() : openSidebar());
  scrim.addEventListener("click", closeSidebar);
  aside.addEventListener("click", (e) => { if (e.target.closest(".nav-item")) closeSidebar(); });

  header.querySelector(".theme-btn").addEventListener("click", (e) => {
    toggleTheme();
    e.currentTarget.innerHTML = icon(getTheme() === "dark" ? "sun" : "moon");
  });

  header.querySelector(".notif-btn").addEventListener("click", (e) => openNotifPanel(e.currentTarget));
  header.querySelector(".profile-btn").addEventListener("click", (e) => openProfileMenu(e.currentTarget, user));
  header.querySelector(".role-btn").addEventListener("click", (e) => openRoleMenu(e.currentTarget, user));

  // keyboard shortcut: "/" focuses search
  const searchInput = header.querySelector(".topbar-search input");
  document.addEventListener("keydown", (e) => {
    if (e.key === "/" && document.activeElement.tagName !== "INPUT" && document.activeElement.tagName !== "TEXTAREA") {
      e.preventDefault(); searchInput.focus();
    }
  });

  // highlight active nav on route change
  setOnChange((path) => {
    aside.querySelectorAll(".nav-item").forEach((a) =>
      a.classList.toggle("active", a.dataset.path === path));
  });

  return { root, view };
}

// ---- Dropdowns (shared popover helper) -------------------------------
function popover(anchor, html, { width = 280, onMount } = {}) {
  document.querySelector(".popover")?.remove();
  const pop = el("div", { class: "popover" });
  pop.style.width = width + "px";
  pop.innerHTML = html;
  document.body.append(pop);
  const r = anchor.getBoundingClientRect();
  const left = Math.min(r.right - width, window.innerWidth - width - 12);
  pop.style.top = r.bottom + 8 + "px";
  pop.style.left = Math.max(12, left) + "px";
  const close = () => { pop.remove(); document.removeEventListener("mousedown", out); };
  const out = (e) => { if (!pop.contains(e.target) && e.target !== anchor) close(); };
  setTimeout(() => document.addEventListener("mousedown", out), 0);
  onMount?.(pop, close);
  return close;
}

function openNotifPanel(anchor) {
  const items = notifications.map((n) => `
    <a class="pop-item ${n.unread ? "unread" : ""}" href="#/announcements">
      <span class="pop-ic">${icon(n.icon)}</span>
      <span class="col" style="gap:2px;min-width:0">
        <span class="pop-title">${n.title}</span>
        <span class="pop-sub">${n.body}</span>
        <span class="pop-time">${n.time}</span>
      </span>
    </a>`).join("");
  popover(anchor, `
    <div class="pop-head"><strong>Notifications</strong><button class="btn btn-quiet btn-sm pop-read">Mark all read</button></div>
    <div class="pop-list">${items}</div>`, {
    width: 340,
    onMount: (pop, close) => {
      pop.querySelector(".pop-read").addEventListener("click", () => {
        pop.querySelectorAll(".unread").forEach((x) => x.classList.remove("unread"));
        document.querySelector(".notif-dot")?.remove();
      });
      pop.querySelectorAll("a").forEach((a) => a.addEventListener("click", close));
    },
  });
}

function openProfileMenu(anchor, user) {
  popover(anchor, `
    <div class="pop-profile">
      ${Avatar(user.name, "md")}
      <div class="col" style="gap:1px;min-width:0">
        <strong style="font-size:var(--fs-sm)">${user.name}</strong>
        <span class="pop-sub">${user.email}</span>
      </div>
    </div>
    <div class="pop-divider"></div>
    <a class="pop-row" href="#/profile">${icon("user")}<span>Profile & settings</span></a>
    <a class="pop-row" href="#/help">${icon("help")}<span>Help center</span></a>
    <div class="pop-divider"></div>
    <button class="pop-row danger logout-btn">${icon("logout")}<span>Sign out</span></button>`, {
    width: 240,
    onMount: (pop, close) => {
      pop.querySelector(".logout-btn").addEventListener("click", () => { close(); window.dispatchEvent(new Event("ngis:logout")); });
      pop.querySelectorAll("a").forEach((a) => a.addEventListener("click", close));
    },
  });
}

function openRoleMenu(anchor, user) {
  const items = roles.map((r) => `
    <button class="pop-row ${r === user.role ? "active" : ""}" data-role="${r}">
      ${icon("user")}<span>${roleLabels[r]}</span>${r === user.role ? icon("check") : ""}
    </button>`).join("");
  popover(anchor, `
    <div class="pop-head"><strong>Preview portal</strong></div>
    <div class="pop-note">Demo only — switch roles to explore each portal without separate logins.</div>
    ${items}`, {
    width: 250,
    onMount: (pop, close) => {
      pop.querySelectorAll("[data-role]").forEach((b) =>
        b.addEventListener("click", () => { close(); window.dispatchEvent(new CustomEvent("ngis:switch-role", { detail: b.dataset.role })); }));
    },
  });
}
