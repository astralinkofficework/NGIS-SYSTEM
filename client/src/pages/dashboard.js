import { el } from "../modules/dom.js";
import { icon } from "../modules/icons.js";
import * as d from "../modules/mockData.js";
import { getState } from "../modules/store.js";
import { StatCard, Card, Badge, Avatar, Meter, Btn } from "../components/ui.js";
import { lineChart, donut, barRow } from "../components/charts.js";
import { toast } from "../components/toast.js";

function greeting() {
  const h = new Date().getHours();
  return h < 12 ? "Good morning" : h < 18 ? "Good afternoon" : "Good evening";
}
const todayName = () => d.weekdays[Math.min(new Date().getDay() - 1, 4)] || "Monday";
const fmtDate = () => new Date().toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" });

const quickActions = (items) => `
  <div class="quick-actions">
    ${items.map(([label, ic, href]) => `
      <a class="qa" href="#${href}">${icon(ic)}<span>${label}</span></a>`).join("")}
  </div>`;

const statusBadge = (s) => ({
  present: Badge("Present", "ok", true), late: Badge("Late", "warn", true),
  absent: Badge("Absent", "danger", true), excused: Badge("Excused", "default", true),
}[s] || Badge(s));

const flagBadge = (f) => ({
  "at-risk": Badge("At risk", "danger"), "low-attendance": Badge("Low attendance", "warn"),
  excellent: Badge("Excellent", "gold"),
}[f] || "");

// =====================================================================
export function dashboardPage() {
  const { role, user, activeChild } = getState();
  const root = el("div");
  const fn = {
    student: studentDash, teacher: teacherDash, parent: parentDash,
    admin: adminDash, super_admin: superDash,
  }[role] || studentDash;
  fn(root, user, activeChild);
  return root;
}

// ---- shared hero ----------------------------------------------------
function hero(name, sub) {
  return `<div class="dash-hero">
    <div><p class="eyebrow">${fmtDate()}</p>
      <h1 class="display dash-greet">${greeting()}, ${name.split(" ")[0]}.</h1>
      <p class="muted">${sub}</p></div>
  </div>`;
}

// =====================================================================
// STUDENT
// =====================================================================
function studentDash(root, u) {
  const today = d.timetable[todayName()] || [];
  const pending = d.assignments.filter((a) => a.status === "pending" || a.status === "overdue");

  root.innerHTML = `
    ${hero(u.name, `${u.grade}-${u.section} · Homeroom ${u.homeroom} · ${d.school.term}`)}
    <div class="grid grid-4" style="margin-bottom:var(--s-5)">
      ${StatCard({ label: "Grade point average", value: u.gpa.toFixed(2), ic: "award", tone: "gold", delta: "▲ 0.08", deltaTone: "ok" })}
      ${StatCard({ label: "Attendance this term", value: u.attendancePct + "%", ic: "checkCircle", delta: "On track", deltaTone: "ok" })}
      ${StatCard({ label: "Class rank", value: `${u.rank} / ${u.rankOf}`, ic: "trend" })}
      ${StatCard({ label: "Pending tasks", value: pending.length, ic: "clipboard", delta: pending.some(p=>p.status==="overdue") ? "1 overdue" : "Up to date", deltaTone: pending.some(p=>p.status==="overdue") ? "danger" : "muted" })}
    </div>

    ${quickActions([
      ["Download report card", "download", "/grades"],
      ["Open assignments", "clipboard", "/assignments"],
      ["View timetable", "calendar", "/timetable"],
      ["Announcements", "megaphone", "/announcements"],
    ])}

    <div class="grid grid-3" style="margin-top:var(--s-5);align-items:start">
      <div class="span-2 col gap-4">
        ${Card({ title: `Today · ${todayName()}`, action: `<a class="link" href="#/timetable" style="font-size:var(--fs-sm)">Full week →</a>`, flush: true,
          body: today.length ? `<ul class="timeline">${today.map((c, i) => `
            <li class="${i === 1 ? "now" : ""}">
              <span class="tl-time mono">${c.start}</span>
              <span class="tl-dot"></span>
              <span class="col" style="gap:1px"><strong>${c.subject}</strong>
                <span class="muted" style="font-size:var(--fs-sm)">${c.teacher} · ${c.room}</span></span>
              ${i === 1 ? Badge("In progress", "accent") : ""}
            </li>`).join("")}</ul>`
            : `<div class="state"><p class="muted">No classes scheduled today.</p></div>` })}
        ${Card({ title: "Recent grades", flush: true, action: `<a class="link" href="#/grades" style="font-size:var(--fs-sm)">All grades →</a>`,
          body: `<div class="table-wrap"><table class="table"><thead><tr><th>Subject</th><th>Latest</th><th>Letter</th><th class="num">Trend</th></tr></thead>
            <tbody>${d.grades.slice(0, 5).map((g) => `<tr>
              <td><strong>${g.subject}</strong></td>
              <td class="tnum">${g.s2}%</td>
              <td>${Badge(g.letter, g.gpa >= 3.7 ? "gold" : g.gpa >= 3 ? "accent" : "warn")}</td>
              <td class="num" style="color:var(--${g.trend === "up" ? "ok" : g.trend === "down" ? "danger" : "text-faint"})">
                ${g.trend === "up" ? "▲" : g.trend === "down" ? "▼" : "—"}</td></tr>`).join("")}</tbody></table></div>` })}
      </div>

      <div class="col gap-4">
        ${Card({ title: "Upcoming exams", flush: true,
          body: `<ul class="mini-list">${d.exams.filter(e => e.status === "upcoming").slice(0,4).map((e) => `
            <li><span class="ml-ic">${icon("calendar")}</span>
              <span class="col grow" style="gap:1px;min-width:0"><strong>${e.subject}</strong>
                <span class="muted" style="font-size:var(--fs-xs)">${e.name.split("—")[1] || e.name}</span></span>
              <span class="ml-meta">${new Date(e.date).toLocaleDateString("en-US",{month:"short",day:"numeric"})}</span></li>`).join("")}</ul>` })}
        ${Card({ title: "To do", flush: true,
          body: `<ul class="mini-list">${pending.slice(0,4).map((a) => `
            <li><span class="ml-ic ${a.status === "overdue" ? "danger" : ""}">${icon("clipboard")}</span>
              <span class="col grow" style="gap:1px;min-width:0"><strong>${a.title}</strong>
                <span class="muted" style="font-size:var(--fs-xs)">${a.subject}</span></span>
              ${a.status === "overdue" ? Badge("Overdue", "danger") : Badge("Due " + new Date(a.due).toLocaleDateString("en-US",{month:"short",day:"numeric"}))}</li>`).join("")}</ul>` })}
        ${pinnedCard()}
      </div>
    </div>`;
}

function pinnedCard() {
  const a = d.announcements.find((x) => x.pinned) || d.announcements[0];
  return Card({ title: "Pinned", body: `
    <div class="col gap-2">${Badge(a.category, d.categoryTone[a.category] || "default")}
      <strong>${a.title}</strong>
      <p class="muted" style="font-size:var(--fs-sm)">${a.body}</p>
      <span class="faint" style="font-size:var(--fs-xs)">${a.author}</span></div>` });
}

// =====================================================================
// TEACHER
// =====================================================================
function teacherDash(root, u) {
  const today = d.timetable[todayName()].filter((c) => c.teacher.includes("Okafor"));
  const totalStudents = d.teacherClasses.reduce((s, c) => s + c.students, 0);
  const atRisk = d.roster.filter((s) => s.flag === "at-risk" || s.flag === "low-attendance");

  root.innerHTML = `
    ${hero(u.name, `${u.title} · ${u.department}`)}
    <div class="grid grid-4" style="margin-bottom:var(--s-5)">
      ${StatCard({ label: "Total students", value: totalStudents, ic: "users" })}
      ${StatCard({ label: "Classes today", value: today.length, ic: "calendar" })}
      ${StatCard({ label: "Pending reviews", value: 14, ic: "clipboard", delta: "Grade now →", deltaTone: "accent" })}
      ${StatCard({ label: "Attendance today", value: "95%", ic: "checkCircle", delta: "▲ 2%", deltaTone: "ok" })}
    </div>

    ${quickActions([
      ["Take attendance", "checkCircle", "/attendance"],
      ["Enter grades", "award", "/grades"],
      ["Create assignment", "clipboard", "/assignments"],
      ["Post announcement", "megaphone", "/announcements"],
    ])}

    <div class="grid grid-3" style="margin-top:var(--s-5);align-items:start">
      <div class="span-2 col gap-4">
        ${Card({ title: "Today's schedule", flush: true, action: `<a class="link" href="#/timetable" style="font-size:var(--fs-sm)">Full week →</a>`,
          body: `<ul class="timeline">${today.map((c, i) => `
            <li class="${i === 0 ? "now" : ""}"><span class="tl-time mono">${c.start}</span><span class="tl-dot"></span>
              <span class="col grow" style="gap:1px"><strong>${c.subject} · Grade 10-B</strong>
                <span class="muted" style="font-size:var(--fs-sm)">${c.room} · 32 students</span></span>
              <a class="btn btn-ghost btn-sm" href="#/attendance">Take attendance</a></li>`).join("")}</ul>` })}
        ${Card({ title: "My classes", flush: true, action: `<a class="link" href="#/classes" style="font-size:var(--fs-sm)">Manage →</a>`,
          body: `<div class="table-wrap"><table class="table"><thead><tr><th>Class</th><th>Subject</th><th class="num">Students</th><th class="num">Avg</th><th class="num">Attendance</th></tr></thead>
            <tbody>${d.teacherClasses.map((c) => `<tr>
              <td><strong>${c.name}</strong> ${c.homeroom ? Badge("Homeroom", "accent") : ""}</td>
              <td>${c.subject}</td><td class="num tnum">${c.students}</td>
              <td class="num tnum">${c.avg}%</td><td class="num tnum">${c.attendance}%</td></tr>`).join("")}</tbody></table></div>` })}
      </div>
      <div class="col gap-4">
        ${Card({ title: "Students needing attention", flush: true,
          body: atRisk.length ? `<ul class="mini-list">${atRisk.map((s) => `
            <li>${Avatar(s.name, "sm")}<span class="col grow" style="gap:1px;min-width:0"><strong>${s.name}</strong>
              <span class="muted" style="font-size:var(--fs-xs)">Avg ${s.avg}% · Att ${s.att}%</span></span>
              ${flagBadge(s.flag)}</li>`).join("")}</ul>`
            : `<div class="state"><p class="muted">All students on track.</p></div>` })}
        ${Card({ title: "Class performance", body: `<div class="col gap-3">
          ${barRow("Grade 11-A", 87, 100, "--ok")}
          ${barRow("Grade 10-B", 84, 100, "--accent")}
          ${barRow("Grade 9-C", 79, 100, "--warn")}</div>` })}
      </div>
    </div>`;
}

// =====================================================================
// PARENT
// =====================================================================
function parentDash(root, u, activeChild) {
  const kids = u.children.map((id) => d.children[id]);
  const child = d.children[activeChild] || kids[0];

  root.innerHTML = `
    ${hero(u.name, `Following ${kids.length} ${kids.length === 1 ? "child" : "children"} at ${d.school.short}`)}
    <div class="child-switch" style="margin-bottom:var(--s-5)">
      ${kids.map((c) => `<button class="child-pill ${c.id === child.id ? "active" : ""}" data-child="${c.id}">
        ${Avatar(c.name, "sm")}<span class="col" style="gap:0;text-align:left"><strong>${c.name}</strong>
          <span class="muted" style="font-size:var(--fs-xs)">${c.grade}</span></span>
        ${c.alert ? `<span class="dot-alert" title="Needs attention"></span>` : ""}</button>`).join("")}
    </div>

    <div class="grid grid-4" style="margin-bottom:var(--s-5)">
      ${StatCard({ label: "Grade point average", value: child.gpa.toFixed(2), ic: "award", tone: "gold" })}
      ${StatCard({ label: "Attendance", value: child.attendancePct + "%", ic: "checkCircle", delta: child.attendancePct < 90 ? "Below target" : "On track", deltaTone: child.attendancePct < 90 ? "warn" : "ok" })}
      ${StatCard({ label: "Pending assignments", value: child.pendingAssignments, ic: "clipboard" })}
      ${StatCard({ label: "Outstanding fees", value: d.fees.currency + d.fees.remaining.toLocaleString(), ic: "wallet", delta: "Due Jun 30", deltaTone: "warn" })}
    </div>

    ${quickActions([
      ["View attendance", "checkCircle", "/attendance"],
      ["View grades", "award", "/grades"],
      ["Pay fees", "wallet", "/fees"],
      ["Message teacher", "message", "/announcements"],
    ])}

    <div class="grid grid-3" style="margin-top:var(--s-5);align-items:start">
      <div class="span-2 col gap-4">
        ${Card({ title: `${child.name} — progress overview`, body: `<div class="grid grid-2" style="gap:var(--s-5)">
          <div class="col gap-3">
            ${barRow("Attendance", child.attendancePct, 100, child.attendancePct < 90 ? "--warn" : "--ok")}
            ${barRow("Assignments completed", 82, 100, "--accent")}
            ${barRow("Term GPA (of 4.0)", Math.round(child.gpa/4*100), 100, "--gold")}
          </div>
          <div class="col gap-2" style="justify-content:center">
            <div class="row gap-3"><span class="ml-ic">${icon("idcard")}</span>
              <span class="col" style="gap:0"><span class="muted" style="font-size:var(--fs-xs)">Student ID</span>
                <strong class="mono">${child.studentId}</strong></span></div>
            <div class="row gap-3"><span class="ml-ic">${icon("user")}</span>
              <span class="col" style="gap:0"><span class="muted" style="font-size:var(--fs-xs)">Homeroom</span>
                <strong>${child.homeroom}</strong></span></div>
          </div></div>` })}
        ${Card({ title: "Smart alerts", flush: true,
          body: `<ul class="mini-list">
            ${child.attendancePct < 90 ? `<li><span class="ml-ic warn">${icon("flag")}</span>
              <span class="col grow"><strong>Attendance below 90%</strong>
                <span class="muted" style="font-size:var(--fs-xs)">${child.name} missed 3 sessions this month</span></span></li>` : ""}
            <li><span class="ml-ic danger">${icon("clipboard")}</span>
              <span class="col grow"><strong>Overdue assignment</strong>
                <span class="muted" style="font-size:var(--fs-xs)">World History — Source Analysis</span></span>${Badge("Action needed","danger")}</li>
            <li><span class="ml-ic" style="color:var(--gold)">${icon("star")}</span>
              <span class="col grow"><strong>Excellent performance</strong>
                <span class="muted" style="font-size:var(--fs-xs)">Computer Science — 96% on final project</span></span></li>
          </ul>` })}
      </div>
      <div class="col gap-4">
        ${Card({ title: "Announcements", flush: true, action: `<a class="link" href="#/announcements" style="font-size:var(--fs-sm)">All →</a>`,
          body: `<ul class="mini-list">${d.announcements.slice(0,4).map((a) => `
            <li><span class="ml-ic">${icon("megaphone")}</span>
              <span class="col grow" style="min-width:0"><strong>${a.title}</strong>
                <span class="muted" style="font-size:var(--fs-xs)">${a.author}</span></span></li>`).join("")}</ul>` })}
        ${pinnedCard()}
      </div>
    </div>`;

  root.querySelectorAll(".child-pill").forEach((b) =>
    b.addEventListener("click", () => {
      import("../modules/store.js").then((m) => m.setActiveChild(b.dataset.child));
      parentDash(root, u, b.dataset.child);
    }));
}

// =====================================================================
// ADMIN
// =====================================================================
function adminDash(root, u) {
  const s = d.adminStats;
  root.innerHTML = `
    ${hero(u.name, `${u.title} · ${d.school.name}`)}
    <div class="grid grid-4" style="margin-bottom:var(--s-5)">
      ${StatCard({ label: "Students", value: s.students.toLocaleString(), ic: "graduation", delta: "▲ 22 this term", deltaTone: "ok" })}
      ${StatCard({ label: "Teachers", value: s.teachers, ic: "users" })}
      ${StatCard({ label: "Attendance today", value: s.attendanceToday + "%", ic: "checkCircle", delta: "▲ 1.2%", deltaTone: "ok" })}
      ${StatCard({ label: "Fees collected", value: s.feesCollectedPct + "%", ic: "wallet", tone: "gold" })}
    </div>

    ${quickActions([
      ["Add user", "plus", "/people"],
      ["Manage classes", "book", "/classes"],
      ["Post announcement", "megaphone", "/announcements"],
      ["View reports", "chart", "/grades"],
    ])}

    <div class="grid grid-3" style="margin-top:var(--s-5);align-items:start">
      <div class="span-2 col gap-4">
        ${Card({ title: "Enrollment trend", action: Badge("Last 6 terms", "default"), attrs: 'id="enroll-card"', body: '<div id="enroll-chart"></div>' })}
        ${Card({ title: "Recent users", flush: true, action: `<a class="link" href="#/people" style="font-size:var(--fs-sm)">Manage →</a>`,
          body: `<div class="table-wrap"><table class="table"><thead><tr><th>Name</th><th>Role</th><th>Status</th><th>Joined</th></tr></thead>
            <tbody>${d.recentUsers.map((r) => `<tr>
              <td class="row gap-2">${Avatar(r.name,"sm")}<strong>${r.name}</strong></td>
              <td>${d.roleLabels[r.role]}</td>
              <td>${Badge(r.status, r.status==="active"?"ok":r.status==="pending"?"warn":"danger", true)}</td>
              <td class="muted">${new Date(r.joined).toLocaleDateString("en-US",{month:"short",day:"numeric"})}</td></tr>`).join("")}</tbody></table></div>` })}
      </div>
      <div class="col gap-4">
        ${Card({ title: "School at a glance", body: `<div class="col gap-3">
          ${statRow("Total parents", s.parents.toLocaleString(), "users")}
          ${statRow("Active classes", s.classes, "book")}
          ${statRow("Open support issues", s.openIssues, "help")}
        </div>` })}
        ${Card({ title: "Fees collection", body: `<div class="col gap-3" id="fees-donut-wrap"></div>` })}
      </div>
    </div>`;

  document.getElementById("enroll-chart")?.append(
    lineChart(s.enrollmentTrend, { h: 170, labels: ["S1","S2","S3","S4","S5","Now"] }));

  const wrap = document.getElementById("fees-donut-wrap");
  if (wrap) {
    wrap.append(donut(
      [{ value: s.feesCollectedPct, color: "--gold" }, { value: 100 - s.feesCollectedPct, color: "--surface-3" }],
      { center: `<strong class="display" style="font-size:1.6rem">${s.feesCollectedPct}%</strong><span class="muted" style="font-size:var(--fs-xs)">collected</span>` }));
    wrap.style.alignItems = "center";
  }
}

const statRow = (label, value, ic) =>
  `<div class="row spread"><span class="row gap-2 muted" style="font-size:var(--fs-sm)"><span class="ml-ic">${icon(ic)}</span>${label}</span><strong class="tnum">${value}</strong></div>`;

// =====================================================================
// SUPER ADMIN
// =====================================================================
function superDash(root, u) {
  root.innerHTML = `
    ${hero(u.name, `${u.title} · full platform control`)}
    <div class="grid grid-4" style="margin-bottom:var(--s-5)">
      ${d.systemHealth.map((h) => `
        <div class="stat">
          <div class="stat-top"><div class="stat-ic">${icon(h.icon)}</div>
            ${Badge(h.status, h.status === "operational" ? "ok" : "warn", true)}</div>
          <div class="stat-val" style="font-size:1.3rem">${h.metric}</div>
          <div class="stat-label">${h.name} · ${h.sub}</div>
        </div>`).join("")}
    </div>

    ${quickActions([
      ["Run backup", "database", "/system"],
      ["Security logs", "shield", "/system"],
      ["Maintenance mode", "settings", "/system"],
      ["Branding", "star", "/system"],
    ])}

    <div class="grid grid-3" style="margin-top:var(--s-5);align-items:start">
      <div class="span-2 col gap-4">
        ${Card({ title: "Recent backups", flush: true, action: Btn("Run backup now", { variant: "ghost", size: "sm", ic: "refresh", id: "run-backup" }),
          body: `<div class="table-wrap"><table class="table"><thead><tr><th>When</th><th>Type</th><th class="num">Size</th><th>Location</th><th>Status</th></tr></thead>
            <tbody>${d.backups.map((b) => `<tr>
              <td class="mono" style="font-size:var(--fs-xs)">${b.date}</td><td>${b.type}</td>
              <td class="num tnum">${b.size}</td><td class="mono" style="font-size:var(--fs-xs)">${b.location}</td>
              <td>${Badge(b.status, b.status==="success"?"ok":"warn", true)}</td></tr>`).join("")}</tbody></table></div>` })}
        ${Card({ title: "Security & device log", flush: true,
          body: `<ul class="mini-list">${d.securityLog.map((l) => `
            <li><span class="ml-ic ${l.level==="warn"?"warn":l.level==="ok"?"":""}" style="${l.level==="ok"?"color:var(--ok)":""}">${icon(l.level==="warn"?"flag":"shield")}</span>
              <span class="col grow" style="min-width:0"><strong>${l.action}</strong>
                <span class="muted" style="font-size:var(--fs-xs)">${l.actor} · ${l.ip}</span></span>
              <span class="ml-meta mono">${l.time}</span></li>`).join("")}</ul>` })}
      </div>
      <div class="col gap-4">
        ${Card({ title: "Disaster recovery", body: `<div class="col gap-4">
          <div class="row spread"><span class="muted" style="font-size:var(--fs-sm)">RPO target</span><strong>≤ 24h</strong></div>
          <div class="row spread"><span class="muted" style="font-size:var(--fs-sm)">RTO target</span><strong>≤ 2h</strong></div>
          <div class="row spread"><span class="muted" style="font-size:var(--fs-sm)">Last restore test</span>${Badge("Passed · Jun 21","ok",true)}</div>
          <div class="hr"></div>
          ${Btn("Open restore runbook", { variant: "ghost", ic: "file", attrs: 'style="width:100%"' })}
        </div>` })}
        ${Card({ title: "Maintenance mode", body: `<div class="col gap-3">
          <p class="muted" style="font-size:var(--fs-sm)">When enabled, only Super Admins can sign in. A banner is shown to everyone else.</p>
          <label class="switch-row"><span>Maintenance mode</span>
            <span class="switch"><input type="checkbox" id="maint"><span class="slider"></span></span></label>
        </div>` })}
      </div>
    </div>`;

  root.querySelector("#run-backup")?.addEventListener("click", () =>
    toast("Backup started", { msg: "A full backup is running in the background.", type: "info" }));
  root.querySelector("#maint")?.addEventListener("change", (e) =>
    toast(e.target.checked ? "Maintenance mode on" : "Maintenance mode off",
      { msg: e.target.checked ? "Only Super Admins can sign in." : "The school can sign in normally.", type: e.target.checked ? "warn" : "ok" }));
}
