import { el } from "../modules/dom.js";
import { icon } from "../modules/icons.js";
import * as d from "../modules/mockData.js";
import { getState } from "../modules/store.js";
import { Card, Badge, Btn, Avatar, Meter, PageHead } from "../components/ui.js";

export function childrenPage() {
  const { user } = getState();
  const root = el("div");
  const kids = user.children.map((id) => d.children[id]);

  root.innerHTML = `
    ${PageHead({ title: "My children", sub: `${kids.length} children at ${d.school.name}` })}
    <div class="grid grid-2" style="align-items:start">
      ${kids.map((c) => `<article class="card pad">
        <div class="row gap-3" style="align-items:flex-start">
          ${Avatar(c.name, "lg")}
          <div class="col grow" style="gap:2px;min-width:0">
            <div class="row spread"><strong class="h3">${c.name}</strong>${c.alert?Badge("Needs attention","warn",true):Badge("On track","ok",true)}</div>
            <span class="muted" style="font-size:var(--fs-sm)">${c.grade} · ${c.homeroom}</span>
            <span class="mono faint" style="font-size:var(--fs-xs)">${c.studentId}</span>
          </div>
        </div>
        <div class="hr" style="margin:var(--s-4) 0"></div>
        <div class="col gap-3">
          <div class="row spread" style="font-size:var(--fs-sm)"><span class="muted">GPA</span><strong class="tnum">${c.gpa.toFixed(2)} / 4.0</strong></div>
          ${Meter(Math.round(c.gpa/4*100), "gold")}
          <div class="row spread" style="font-size:var(--fs-sm)"><span class="muted">Attendance</span><strong class="tnum">${c.attendancePct}%</strong></div>
          ${Meter(c.attendancePct, c.attendancePct<90?"warn":"ok")}
          <div class="row spread" style="font-size:var(--fs-sm)"><span class="muted">Pending assignments</span><strong class="tnum">${c.pendingAssignments}</strong></div>
        </div>
        <div class="row gap-2" style="margin-top:var(--s-4)">
          ${Btn("Grades", { variant: "ghost", size: "sm", ic: "award", attrs: `onclick="location.hash='/grades'"` })}
          ${Btn("Attendance", { variant: "ghost", size: "sm", ic: "checkCircle", attrs: `onclick="location.hash='/attendance'"` })}
          ${Btn("Message teacher", { variant: "quiet", size: "sm", ic: "message" })}
        </div>
      </article>`).join("")}
    </div>`;
  return root;
}
