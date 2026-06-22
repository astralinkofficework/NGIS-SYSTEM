import { el } from "../modules/dom.js";
import { icon } from "../modules/icons.js";
import * as d from "../modules/mockData.js";
import { getState } from "../modules/store.js";
import { PageHead, Card, StatCard, Badge, Avatar } from "../components/ui.js";
import { donut } from "../components/charts.js";
import { toast } from "../components/toast.js";

export function attendancePage() {
  const { role } = getState();
  return role === "teacher" || role === "admin" ? teacherAttendance() : studentAttendance();
}

// ---- Student / parent view ------------------------------------------
function studentAttendance() {
  const root = el("div");
  const s = d.attendanceSummary;
  const total = s.present + s.late + s.absent + s.excused;
  const pct = Math.round((s.present / total) * 100);
  const tag = { present: "P", late: "L", absent: "A", excused: "E" };
  // June 2026 lays out cleanly: the 1st is a Monday, so the grid needs no leading blanks.
  const cells = Array.from({ length: 35 }, (_, i) => {
    const day = i + 1;
    const weekend = i % 7 >= 5;
    if (day > 30 || weekend) return `<span class="cal-cell off"></span>`;
    const st = d.attendanceMonth[day];
    if (!st) return `<span class="cal-cell"><span class="cal-num">${day}</span></span>`;
    return `<span class="cal-cell ${st}" title="${day} June — ${st}"><span class="cal-num">${day}</span><i>${tag[st]}</i></span>`;
  }).join("");

  root.innerHTML = `
    ${PageHead({ title: "Attendance", sub: `${d.school.term} · ${total} school days recorded` })}
    <div class="grid grid-4" style="margin-bottom:var(--s-5)">
      ${StatCard({ label: "Present", value: s.present, ic: "checkCircle", delta: pct + "%", deltaTone: "ok" })}
      ${StatCard({ label: "Late", value: s.late, ic: "clock" })}
      ${StatCard({ label: "Absent", value: s.absent, ic: "xCircle" })}
      ${StatCard({ label: "Excused", value: s.excused, ic: "file" })}
    </div>
    <div class="grid grid-3" style="align-items:start">
      <div class="span-2">${Card({ title: "June 2026", action: Badge("Mon – Fri", "default"), body: `
        <div class="cal">
          ${["Mon","Tue","Wed","Thu","Fri","Sat","Sun"].map((w) => `<span class="cal-h">${w}</span>`).join("")}
          ${cells}
        </div>
        <div class="row gap-4 wrap" style="margin-top:var(--s-4)">
          ${["present","late","absent","excused"].map((k) => `<span class="row gap-2" style="font-size:var(--fs-sm)"><span class="dot-key ${k}"></span>${k[0].toUpperCase()+k.slice(1)}</span>`).join("")}
        </div>` })}
      </div>
      <div id="att-donut-card">${Card({ title: "Term overview", body: `<div class="col center gap-4" id="att-donut"></div>` })}</div>
    </div>`;

  const wrap = root.querySelector("#att-donut");
  wrap.append(donut([
    { value: s.present, color: "--present" }, { value: s.late, color: "--late" },
    { value: s.absent, color: "--absent" }, { value: s.excused, color: "--excused" },
  ], { size: 150, center: `<strong class="display" style="font-size:1.8rem">${pct}%</strong><span class="muted" style="font-size:var(--fs-xs)">present</span>` }));
  const legend = el("div", { class: "col gap-2", style: { width: "100%" } });
  legend.innerHTML = ["present","late","absent","excused"].map((k) =>
    `<div class="row spread" style="font-size:var(--fs-sm)"><span class="row gap-2"><span class="dot-key ${k}"></span>${k[0].toUpperCase()+k.slice(1)}</span><strong class="tnum">${s[k]}</strong></div>`).join("");
  wrap.append(legend);
  return root;
}

// ---- Teacher: take attendance ---------------------------------------
function teacherAttendance() {
  const root = el("div");
  const today = new Date().toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" });
  const states = ["present", "late", "absent", "excused"];
  const stateIc = { present: "check", late: "clock", absent: "x", excused: "file" };

  root.innerHTML = `
    ${PageHead({ title: "Take attendance", sub: `${today}`,
      action: `<div class="row gap-2">
        <select class="select" style="width:auto" id="att-class">${d.teacherClasses.map((c,i)=>`<option>${c.name} · ${c.subject}</option>`).join("")}</select>
        <button class="btn btn-ghost btn-sm" id="mark-all">${icon("checkCircle")}<span>All present</span></button>
        <button class="btn btn-primary" id="save-att">${icon("check")}<span>Save</span></button>
      </div>` })}
    <div class="card" style="overflow:hidden">
      <div class="att-summary" id="att-summary"></div>
      <div class="table-wrap"><table class="table"><thead><tr><th>Student</th><th>ID</th><th style="text-align:center">Status</th><th>Note</th></tr></thead>
        <tbody>${d.roster.map((s) => `<tr data-id="${s.id}">
          <td class="row gap-2">${Avatar(s.name,"sm")}<strong>${s.name}</strong></td>
          <td class="mono" style="font-size:var(--fs-xs)">${s.sid}</td>
          <td><div class="att-toggle" style="justify-content:center">${states.map((st) =>
            `<button class="att-opt ${st} ${s.status===st?"on":""}" data-state="${st}" title="${st}">${icon(stateIc[st])}</button>`).join("")}</div></td>
          <td><input class="input att-note" placeholder="Add note…" style="height:34px"></td></tr>`).join("")}</tbody></table></div>
    </div>`;

  const recompute = () => {
    const counts = { present: 0, late: 0, absent: 0, excused: 0 };
    root.querySelectorAll("tbody tr").forEach((tr) => {
      const on = tr.querySelector(".att-opt.on"); if (on) counts[on.dataset.state]++;
    });
    root.querySelector("#att-summary").innerHTML = states.map((st) =>
      `<div class="att-sum ${st}"><strong class="tnum">${counts[st]}</strong><span>${st}</span></div>`).join("");
  };

  root.querySelectorAll(".att-opt").forEach((b) => b.addEventListener("click", () => {
    b.parentElement.querySelectorAll(".att-opt").forEach((x) => x.classList.remove("on"));
    b.classList.add("on"); recompute();
  }));
  root.querySelector("#mark-all").addEventListener("click", () => {
    root.querySelectorAll("tbody tr").forEach((tr) => {
      tr.querySelectorAll(".att-opt").forEach((x) => x.classList.remove("on"));
      tr.querySelector(".att-opt.present").classList.add("on");
    });
    recompute();
  });
  root.querySelector("#save-att").addEventListener("click", () =>
    toast("Attendance saved", { msg: "Today's attendance has been recorded.", type: "ok" }));
  recompute();
  return root;
}
