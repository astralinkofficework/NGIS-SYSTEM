import { el } from "../modules/dom.js";
import { icon } from "../modules/icons.js";
import * as d from "../modules/mockData.js";
import { getState } from "../modules/store.js";
import { PageHead, Card, StatCard, Badge, Btn } from "../components/ui.js";
import { openModal } from "../components/modal.js";
import { toast } from "../components/toast.js";

export function gradesPage() {
  const { role } = getState();
  return role === "teacher" ? teacherGrades() : studentGrades();
}

// ---- Student / parent -----------------------------------------------
function studentGrades() {
  const root = el("div");
  const u = d.accounts.student;
  const avg = Math.round(d.grades.reduce((s, g) => s + g.s2, 0) / d.grades.length);

  root.innerHTML = `
    ${PageHead({ title: "Grades & exams", sub: `${d.school.year} · ${d.school.term}`,
      action: Btn("Download report card", { variant: "primary", ic: "download", id: "dl-report" }) })}
    <div class="grid grid-4" style="margin-bottom:var(--s-5)">
      ${StatCard({ label: "Cumulative GPA", value: u.gpa.toFixed(2), ic: "award", tone: "gold" })}
      ${StatCard({ label: "Term average", value: avg + "%", ic: "trend", delta: "▲ 2%", deltaTone: "ok" })}
      ${StatCard({ label: "Class rank", value: `${u.rank} / ${u.rankOf}`, ic: "users" })}
      ${StatCard({ label: "Honor roll", value: "Yes", ic: "star", tone: "gold" })}
    </div>
    <div class="tabs" style="margin-bottom:var(--s-5)" id="grade-tabs">
      <button class="active" data-tab="subjects">Subjects</button>
      <button data-tab="exams">Exam schedule</button>
    </div>
    <div id="grade-body"></div>`;

  const body = root.querySelector("#grade-body");
  const renderSubjects = () => {
    body.innerHTML = Card({ flush: true, body: `<div class="table-wrap"><table class="table">
      <thead><tr><th>Subject</th><th class="num">Sem 1</th><th class="num">Sem 2</th><th class="num">GPA</th><th>Grade</th><th>Teacher comment</th></tr></thead>
      <tbody>${d.grades.map((g) => `<tr>
        <td><strong>${g.subject}</strong> <span class="mono faint" style="font-size:var(--fs-xs)">${g.code}</span></td>
        <td class="num tnum">${g.s1}%</td>
        <td class="num tnum"><span class="row" style="justify-content:flex-end;gap:6px">${g.s2}% <span style="color:var(--${g.trend==="up"?"ok":g.trend==="down"?"danger":"text-faint"})">${g.trend==="up"?"▲":g.trend==="down"?"▼":"—"}</span></span></td>
        <td class="num tnum">${g.gpa.toFixed(1)}</td>
        <td>${Badge(g.letter, g.gpa>=3.7?"gold":g.gpa>=3?"accent":"warn")}</td>
        <td class="muted" style="max-width:280px">${g.comment}</td></tr>`).join("")}</tbody></table></div>` });
  };
  const renderExams = () => {
    body.innerHTML = Card({ flush: true, body: `<div class="table-wrap"><table class="table">
      <thead><tr><th>Exam</th><th>Subject</th><th>Date</th><th>Status</th><th class="num">Score</th></tr></thead>
      <tbody>${d.exams.map((e) => `<tr>
        <td><strong>${e.name}</strong></td><td>${e.subject}</td>
        <td>${new Date(e.date).toLocaleDateString("en-US",{weekday:"short",month:"short",day:"numeric"})} ${e.room?`· <span class="muted">${e.room}</span>`:""}</td>
        <td>${e.status==="upcoming"?Badge("Upcoming","accent",true):Badge("Completed","ok",true)}</td>
        <td class="num tnum">${e.score?e.score+"%":"—"}</td></tr>`).join("")}</tbody></table></div>` });
  };
  renderSubjects();
  root.querySelectorAll("#grade-tabs button").forEach((b) => b.addEventListener("click", () => {
    root.querySelectorAll("#grade-tabs button").forEach((x) => x.classList.remove("active"));
    b.classList.add("active");
    b.dataset.tab === "exams" ? renderExams() : renderSubjects();
  }));
  root.querySelector("#dl-report").addEventListener("click", () => openReportCard(u));
  return root;
}

function openReportCard(u) {
  const avg = Math.round(d.grades.reduce((s, g) => s + g.s2, 0) / d.grades.length);
  openModal({
    title: "Report card",
    maxWidth: "560px",
    body: `<div class="report-card">
      <div class="rc-head">
        <div class="brand-mark">${icon("graduation")}</div>
        <div><strong>${d.school.name}</strong><div class="muted" style="font-size:var(--fs-sm)">${d.school.year} · ${d.school.term}</div></div>
      </div>
      <div class="rc-meta">
        <div><span class="faint">Student</span><strong>${u.name}</strong></div>
        <div><span class="faint">Student ID</span><strong class="mono">${u.studentId}</strong></div>
        <div><span class="faint">Class</span><strong>${u.grade}-${u.section}</strong></div>
        <div><span class="faint">GPA</span><strong>${u.gpa.toFixed(2)} / 4.0</strong></div>
      </div>
      <table class="table" style="margin-top:var(--s-4)"><thead><tr><th>Subject</th><th class="num">Score</th><th>Grade</th></tr></thead>
        <tbody>${d.grades.map((g)=>`<tr><td>${g.subject}</td><td class="num tnum">${g.s2}%</td><td>${Badge(g.letter, g.gpa>=3.7?"gold":"accent")}</td></tr>`).join("")}</tbody>
        <tfoot><tr style="font-weight:700"><td>Term average</td><td class="num tnum">${avg}%</td><td>${Badge("Honor roll","gold")}</td></tr></tfoot>
      </table>
    </div>`,
    footer: `${Btn("Close", { variant: "ghost", attrs: 'data-close="1"' })}${Btn("Download PDF", { variant: "primary", ic: "download", id: "rc-dl" })}`,
  });
  document.querySelector("[data-close='1']")?.addEventListener("click", () => document.querySelector(".scrim")?.remove());
  document.getElementById("rc-dl")?.addEventListener("click", () => {
    toast("Report card downloaded", { msg: "Saved as report-card-sem2.pdf", type: "ok" });
    document.querySelector(".scrim")?.remove();
  });
}

// ---- Teacher: grade entry -------------------------------------------
function teacherGrades() {
  const root = el("div");
  root.innerHTML = `
    ${PageHead({ title: "Grade entry", sub: "Grade 10-B · Mathematics · Midterm",
      action: `<div class="row gap-2">
        <select class="select" style="width:auto"><option>Grade 10-B · Mathematics</option><option>Grade 11-A · Mathematics</option></select>
        ${Btn("Bulk import", { variant: "ghost", ic: "upload" })}
        ${Btn("Save grades", { variant: "primary", ic: "check", id: "save-grades" })}
      </div>` })}
    <div class="card" style="overflow:hidden"><div class="table-wrap"><table class="table">
      <thead><tr><th>Student</th><th>ID</th><th style="width:120px">Score / 100</th><th>Comment</th></tr></thead>
      <tbody>${d.roster.map((s) => `<tr>
        <td><strong>${s.name}</strong></td>
        <td class="mono" style="font-size:var(--fs-xs)">${s.sid}</td>
        <td><input class="input grade-in" type="number" min="0" max="100" value="${s.avg}" style="height:34px;text-align:center"></td>
        <td><input class="input" placeholder="Optional comment…" style="height:34px"></td></tr>`).join("")}</tbody>
    </table></div></div>`;
  root.querySelector("#save-grades").addEventListener("click", () =>
    toast("Grades saved", { msg: "30 grades recorded for Grade 10-B Midterm.", type: "ok" }));
  return root;
}
