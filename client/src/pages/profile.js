import { el } from "../modules/dom.js";
import { icon } from "../modules/icons.js";
import * as d from "../modules/mockData.js";
import { getState } from "../modules/store.js";
import { PageHead, Card, Badge, Btn, Avatar } from "../components/ui.js";
import { toast } from "../components/toast.js";

export function profilePage() {
  const { user, role } = getState();
  const root = el("div");

  // Locked vs editable depend on role (matches the RBAC spec).
  const locked = role === "student"
    ? [["Student ID", user.studentId, "idcard"], ["Assigned class", `${user.grade}-${user.section}`, "book"], ["Enrolled", user.enrolled, "calendar"]]
    : role === "teacher"
    ? [["Employee ID", user.employeeId, "idcard"], ["Department", user.department, "users"], ["Subjects", (user.subjects||[]).join(", "), "book"]]
    : [["Account ID", user.id, "idcard"], ["Role", d.roleLabels[role], "shield"]];

  root.innerHTML = `
    ${PageHead({ title: "Profile & settings", sub: "Manage your account, contact details, and preferences" })}
    <div class="grid grid-3" style="align-items:start">
      <div class="col gap-4">
        ${Card({ body: `<div class="col center gap-3" style="text-align:center">
          ${Avatar(user.name, "xl")}
          <div class="col" style="gap:2px"><strong class="h3">${user.name}</strong>
            <span class="muted">${d.roleLabels[role]}</span>${Badge("Verified","ok",true)}</div>
          ${Btn("Change photo", { variant: "ghost", size: "sm", ic: "upload" })}
        </div>` })}
        ${Card({ title: "Locked records", body: `<div class="col gap-3">
          ${locked.map(([l,v,ic]) => `<div class="row gap-3"><span class="ml-ic">${icon(ic)}</span>
            <div class="col grow" style="gap:0"><span class="muted" style="font-size:var(--fs-xs)">${l}</span><strong>${v}</strong></div>
            <span class="faint" title="Locked">${icon("shield")}</span></div>`).join("")}
          <p class="faint" style="font-size:var(--fs-xs)">These are managed by the administration and can't be edited here.</p>
        </div>` })}
      </div>
      <div class="span-2 col gap-4">
        ${Card({ title: "Contact details", action: Badge("Editable","accent"), body: `<form class="grid grid-2" id="pf">
          <div class="field"><label>Full name</label><input class="input" value="${user.name}"></div>
          <div class="field"><label>Email</label><input class="input" value="${user.email}" type="email"></div>
          <div class="field"><label>Phone</label><input class="input" value="${user.phone||""}"></div>
          <div class="field"><label>Preferred language</label><select class="select"><option>English</option><option>Español</option><option>Français</option><option>中文</option></select></div>
          ${user.address?`<div class="field span-2"><label>Address</label><input class="input" value="${user.address}"></div>`:""}
          <div class="field span-2"><label>Emergency contact</label><input class="input" placeholder="Name & phone number"></div>
        </form>
        <div class="row gap-2" style="margin-top:var(--s-4);justify-content:flex-end">${Btn("Cancel", { variant: "ghost" })}${Btn("Save changes", { variant: "primary", ic: "check", id: "save-pf" })}</div>` })}
        ${Card({ title: "Security", body: `<div class="col gap-4">
          <div class="row spread"><div class="col" style="gap:1px"><strong>Password</strong><span class="muted" style="font-size:var(--fs-sm)">Last changed 2 months ago</span></div>${Btn("Change", { variant: "ghost", size: "sm" })}</div>
          <div class="hr"></div>
          <div class="row spread"><div class="col" style="gap:1px"><strong>Two-factor authentication</strong><span class="muted" style="font-size:var(--fs-sm)">Add an extra layer of security (Phase 2)</span></div>
            <label class="switch"><input type="checkbox"><span class="slider"></span></label></div>
          <div class="hr"></div>
          <div class="row spread"><div class="col" style="gap:1px"><strong>Active sessions</strong><span class="muted" style="font-size:var(--fs-sm)">2 devices signed in</span></div>${Btn("Sign out all", { variant: "ghost", size: "sm" })}</div>
        </div>` })}
      </div>
    </div>`;
  root.querySelector("#save-pf").addEventListener("click", (e) => { e.preventDefault(); toast("Profile updated", { type: "ok" }); });
  return root;
}
