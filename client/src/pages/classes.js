import { el } from "../modules/dom.js";
import { icon } from "../modules/icons.js";
import * as d from "../modules/mockData.js";
import { getState } from "../modules/store.js";
import { PageHead, Card, Badge, Btn, Avatar, Search, Meter } from "../components/ui.js";

export function classesPage() {
  const { role } = getState();
  const root = el("div");

  if (role === "teacher") {
    root.innerHTML = `
      ${PageHead({ title: "My classes", sub: `${d.teacherClasses.length} classes · ${d.teacherClasses.reduce((s,c)=>s+c.students,0)} students` })}
      <div class="grid grid-2" style="margin-bottom:var(--s-5)">
        ${d.teacherClasses.map((c) => `<article class="card pad class-card">
          <div class="row spread"><div class="row gap-2"><strong class="h3">${c.name}</strong>${c.homeroom?Badge("Homeroom","accent"):""}</div>
            <span class="muted" style="font-size:var(--fs-sm)">${c.next}</span></div>
          <p class="muted" style="font-size:var(--fs-sm);margin:6px 0 var(--s-4)">${c.subject} · ${c.students} students</p>
          <div class="col gap-3">
            <div class="row spread" style="font-size:var(--fs-sm)"><span class="muted">Class average</span><strong class="tnum">${c.avg}%</strong></div>
            ${Meter(c.avg, c.avg>=85?"ok":c.avg>=75?"":"warn")}
            <div class="row spread" style="font-size:var(--fs-sm)"><span class="muted">Attendance</span><strong class="tnum">${c.attendance}%</strong></div>
            ${Meter(c.attendance, "ok")}
          </div>
          <div class="row gap-2" style="margin-top:var(--s-4)">${Btn("Roster", { variant: "ghost", size: "sm", ic: "users" })}${Btn("Attendance", { variant: "ghost", size: "sm", ic: "checkCircle" })}</div>
        </article>`).join("")}
      </div>
      ${Card({ title: "Grade 10-B · roster", flush: true, action: `<div style="width:220px">${Search("Find student…")}</div>`, body: `
        <div class="table-wrap"><table class="table"><thead><tr><th>Student</th><th>ID</th><th class="num">Average</th><th class="num">Attendance</th><th>Flag</th></tr></thead>
        <tbody>${d.roster.map((s) => `<tr>
          <td class="row gap-2">${Avatar(s.name,"sm")}<strong>${s.name}</strong></td>
          <td class="mono" style="font-size:var(--fs-xs)">${s.sid}</td>
          <td class="num tnum">${s.avg}%</td><td class="num tnum">${s.att}%</td>
          <td>${s.flag?Badge(s.flag.replace("-"," "), s.flag==="excellent"?"gold":s.flag==="at-risk"?"danger":"warn"):'<span class="faint">—</span>'}</td></tr>`).join("")}</tbody></table></div>` })}`;
    return root;
  }

  // Admin: classes & subjects
  const classes = [
    { name: "Grade 10-B", grade: 10, homeroom: "D. Okafor", students: 32, subjects: 8 },
    { name: "Grade 11-A", grade: 11, homeroom: "E. Vargas", students: 28, subjects: 9 },
    { name: "Grade 9-C", grade: 9, homeroom: "P. Nair", students: 30, subjects: 8 },
    { name: "Grade 7-A", grade: 7, homeroom: "J. Holloway", students: 26, subjects: 7 },
  ];
  root.innerHTML = `
    ${PageHead({ title: "Classes & subjects", sub: `${d.adminStats.classes} classes · ${d.subjects.length} subjects`,
      action: `<div class="row gap-2">${Btn("New subject", { variant: "ghost", ic: "plus" })}${Btn("New class", { variant: "primary", ic: "plus" })}</div>` })}
    <div class="grid grid-3" style="align-items:start">
      <div class="span-2">${Card({ title: "Classes", flush: true, body: `<div class="table-wrap"><table class="table">
        <thead><tr><th>Class</th><th class="num">Grade</th><th>Homeroom</th><th class="num">Students</th><th class="num">Subjects</th></tr></thead>
        <tbody>${classes.map((c)=>`<tr><td><strong>${c.name}</strong></td><td class="num tnum">${c.grade}</td><td>${c.homeroom}</td><td class="num tnum">${c.students}</td><td class="num tnum">${c.subjects}</td></tr>`).join("")}</tbody></table></div>` })}</div>
      ${Card({ title: "Subjects", flush: true, body: `<ul class="mini-list">${d.subjects.map((s)=>`
        <li><span class="ml-ic">${icon("book")}</span><span class="col grow" style="gap:1px"><strong>${s.name}</strong>
          <span class="muted" style="font-size:var(--fs-xs)">${s.teacher}</span></span><span class="mono faint" style="font-size:var(--fs-xs)">${s.code}</span></li>`).join("")}</ul>` })}
    </div>`;
  return root;
}
