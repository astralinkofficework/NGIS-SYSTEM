import { el } from "../modules/dom.js";
import { icon } from "../modules/icons.js";
import * as d from "../modules/mockData.js";
import { getState } from "../modules/store.js";
import { PageHead, Card, Badge, Btn, Search, EmptyState } from "../components/ui.js";
import { openModal } from "../components/modal.js";
import { toast } from "../components/toast.js";

const statusTone = { submitted: "ok", pending: "warn", overdue: "danger" };
const daysLeft = (due) => Math.ceil((new Date(due) - new Date("2026-06-22")) / 864e5);

export function assignmentsPage() {
  const { role } = getState();
  const root = el("div");
  const isTeacher = role === "teacher" || role === "admin";

  root.innerHTML = `
    ${PageHead({ title: "Assignments", sub: isTeacher ? "Create, track, and grade work" : `${d.school.term} · ${d.assignments.length} assignments`,
      action: isTeacher ? Btn("Create assignment", { variant: "primary", ic: "plus", id: "new-assign" }) : "" })}
    <div class="row spread wrap gap-3" style="margin-bottom:var(--s-5)">
      <div class="segmented" id="filters">
        <button class="active" data-f="all">All</button>
        <button data-f="pending">Pending</button>
        <button data-f="submitted">Submitted</button>
        <button data-f="overdue">Overdue</button>
      </div>
      <div style="width:260px">${Search("Search assignments…", "assign-search")}</div>
    </div>
    <div class="assign-grid" id="assign-list"></div>`;

  const list = root.querySelector("#assign-list");
  let filter = "all", q = "";

  const render = () => {
    const items = d.assignments.filter((a) =>
      (filter === "all" || a.status === filter) &&
      (a.title.toLowerCase().includes(q) || a.subject.toLowerCase().includes(q)));
    if (!items.length) { list.innerHTML = EmptyState({ ic: "clipboard", title: "No assignments here", msg: "Try a different filter or search term." }); return; }
    list.innerHTML = items.map((a) => {
      const left = daysLeft(a.due);
      const due = a.status === "submitted" ? "Submitted"
        : left < 0 ? `${-left}d overdue` : left === 0 ? "Due today" : `${left}d left`;
      return `<article class="card assign-card" data-id="${a.id}">
        <div class="row spread">${Badge(a.subject, "default")}${Badge(a.status, statusTone[a.status], true)}</div>
        <h3 class="h3" style="margin-top:var(--s-3)">${a.title}</h3>
        <p class="muted" style="font-size:var(--fs-sm);margin-top:6px">${a.desc}</p>
        <div class="hr" style="margin:var(--s-4) 0"></div>
        <div class="row spread">
          <span class="row gap-2 ${a.status!=="submitted"&&left<0?"":""}" style="font-size:var(--fs-sm);color:${a.status!=="submitted"&&left<0?"var(--danger)":"var(--text-muted)"}">
            ${icon("clock")} ${due}</span>
          ${a.status === "submitted" && a.grade ? Badge("Graded " + a.grade, "gold")
            : isTeacher ? Btn("Review", { variant: "ghost", size: "sm" })
            : Btn(a.status === "submitted" ? "View" : "Submit", { variant: a.status==="submitted"?"ghost":"primary", size: "sm" })}
        </div></article>`;
    }).join("");
    list.querySelectorAll(".assign-card").forEach((c) => c.addEventListener("click", () => openAssignment(c.dataset.id, isTeacher)));
  };

  root.querySelectorAll("#filters button").forEach((b) => b.addEventListener("click", () => {
    root.querySelectorAll("#filters button").forEach((x) => x.classList.remove("active"));
    b.classList.add("active"); filter = b.dataset.f; render();
  }));
  root.querySelector("#assign-search").addEventListener("input", (e) => { q = e.target.value.toLowerCase(); render(); });
  root.querySelector("#new-assign")?.addEventListener("click", openCreate);
  render();
  return root;
}

function openAssignment(id, isTeacher) {
  const a = d.assignments.find((x) => x.id === id);
  openModal({
    title: a.title,
    body: `<div class="col gap-4">
      <div class="row gap-2">${Badge(a.subject, "default")}${Badge(a.status, statusTone[a.status], true)}</div>
      <p>${a.desc}</p>
      <div class="row spread"><span class="muted" style="font-size:var(--fs-sm)">Due date</span><strong>${new Date(a.due).toLocaleDateString("en-US",{weekday:"long",month:"long",day:"numeric"})}</strong></div>
      ${a.feedback ? `<div class="card pad" style="background:var(--ok-soft);border-color:transparent"><strong>Feedback · ${a.grade}</strong><p class="muted" style="margin-top:4px;font-size:var(--fs-sm)">${a.feedback}</p></div>` : ""}
      ${!isTeacher && a.status !== "submitted" ? `<div class="upload-zone" id="uz">${icon("upload")}<strong>Drop files or click to upload</strong><span class="muted" style="font-size:var(--fs-sm)">PDF, images, or documents · max 20 MB</span></div>` : ""}
    </div>`,
    footer: isTeacher
      ? `${Btn("Close", { variant: "ghost", attrs: 'data-x="1"' })}${Btn("Open submissions", { variant: "primary", ic: "folder" })}`
      : a.status === "submitted"
        ? Btn("Close", { variant: "ghost", attrs: 'data-x="1"' })
        : `${Btn("Cancel", { variant: "ghost", attrs: 'data-x="1"' })}${Btn("Submit assignment", { variant: "primary", ic: "check", id: "do-submit" })}`,
  });
  document.querySelector("[data-x='1']")?.addEventListener("click", () => document.querySelector(".scrim")?.remove());
  document.getElementById("do-submit")?.addEventListener("click", () => {
    toast("Assignment submitted", { msg: a.title, type: "ok" });
    document.querySelector(".scrim")?.remove();
  });
}

function openCreate() {
  openModal({
    title: "New assignment",
    body: `<div class="col gap-4">
      <div class="field"><label>Title</label><input class="input" placeholder="e.g. Quadratic Functions — Problem Set 8"></div>
      <div class="row gap-3">
        <div class="field grow"><label>Subject</label><select class="select">${d.subjects.map((s)=>`<option>${s.name}</option>`).join("")}</select></div>
        <div class="field grow"><label>Class</label><select class="select"><option>Grade 10-B</option><option>Grade 11-A</option></select></div>
      </div>
      <div class="field"><label>Description</label><textarea class="textarea" placeholder="Instructions for students…"></textarea></div>
      <div class="field"><label>Due date</label><input class="input" type="date" value="2026-06-30"></div>
    </div>`,
    footer: `${Btn("Cancel", { variant: "ghost", attrs: 'data-x="1"' })}${Btn("Create & notify class", { variant: "primary", ic: "check", id: "do-create" })}`,
  });
  document.querySelector("[data-x='1']")?.addEventListener("click", () => document.querySelector(".scrim")?.remove());
  document.getElementById("do-create")?.addEventListener("click", () => {
    toast("Assignment created", { msg: "Grade 10-B has been notified.", type: "ok" });
    document.querySelector(".scrim")?.remove();
  });
}
