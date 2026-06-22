import { el } from "../modules/dom.js";
import { icon } from "../modules/icons.js";
import * as d from "../modules/mockData.js";
import { PageHead, Card, StatCard, Badge, Btn, Avatar, Search } from "../components/ui.js";
import { toast } from "../components/toast.js";

// Expanded directory built from roster + recent users + demo accounts.
const people = [
  ...d.roster.slice(0, 8).map((s) => ({ name: s.name, role: "student", email: s.name.toLowerCase().replace(/\s/g, ".") + "@ngis.edu", status: "active", id: s.sid })),
  { name: "David Okafor", role: "teacher", email: "teacher@ngis.edu", status: "active", id: "NGIS-T-0091" },
  { name: "Priya Nair", role: "teacher", email: "p.nair@ngis.edu", status: "active", id: "NGIS-T-0104" },
  { name: "Linda Chen", role: "parent", email: "parent@ngis.edu", status: "active", id: "NGIS-P-0552" },
  { name: "Robert Fox", role: "parent", email: "r.fox@ngis.edu", status: "pending", id: "NGIS-P-0561" },
  { name: "Sarah Whitfield", role: "admin", email: "admin@ngis.edu", status: "active", id: "NGIS-A-0007" },
  { name: "Hana Suzuki", role: "student", email: "hana.s@ngis.edu", status: "suspended", id: "NGIS-2025-0440" },
];

export function peoplePage() {
  const root = el("div");
  root.innerHTML = `
    ${PageHead({ title: "People", sub: "Students, teachers, parents, and staff",
      action: Btn("Add user", { variant: "primary", ic: "plus", id: "add-user" }) })}
    <div class="grid grid-4" style="margin-bottom:var(--s-5)">
      ${StatCard({ label: "Students", value: d.adminStats.students.toLocaleString(), ic: "graduation" })}
      ${StatCard({ label: "Teachers", value: d.adminStats.teachers, ic: "users" })}
      ${StatCard({ label: "Parents", value: d.adminStats.parents.toLocaleString(), ic: "user" })}
      ${StatCard({ label: "Pending approvals", value: 3, ic: "clock", delta: "Review →", deltaTone: "warn" })}
    </div>
    <div class="row spread wrap gap-3" style="margin-bottom:var(--s-4)">
      <div class="segmented" id="role-filter">
        ${["all","student","teacher","parent","admin"].map((r,i)=>`<button class="${i===0?"active":""}" data-r="${r}">${r==="all"?"All":d.roleLabels[r]||r}</button>`).join("")}
      </div>
      <div style="width:260px">${Search("Search people…", "people-search")}</div>
    </div>
    <div class="card" style="overflow:hidden"><div class="table-wrap"><table class="table">
      <thead><tr><th>Name</th><th>Role</th><th>ID</th><th>Email</th><th>Status</th><th></th></tr></thead>
      <tbody id="people-rows"></tbody></table></div></div>`;

  const rows = root.querySelector("#people-rows");
  let role = "all", q = "";
  const render = () => {
    const items = people.filter((p) => (role === "all" || p.role === role) &&
      (p.name.toLowerCase().includes(q) || p.email.toLowerCase().includes(q)));
    rows.innerHTML = items.map((p) => `<tr>
      <td class="row gap-2">${Avatar(p.name,"sm")}<strong>${p.name}</strong></td>
      <td>${d.roleLabels[p.role]||p.role}</td>
      <td class="mono" style="font-size:var(--fs-xs)">${p.id}</td>
      <td class="muted">${p.email}</td>
      <td>${Badge(p.status, p.status==="active"?"ok":p.status==="pending"?"warn":"danger", true)}</td>
      <td class="num"><button class="btn btn-quiet btn-icon btn-sm" title="Edit">${icon("edit")}</button></td></tr>`).join("");
  };
  root.querySelectorAll("#role-filter button").forEach((b) => b.addEventListener("click", () => {
    root.querySelectorAll("#role-filter button").forEach((x) => x.classList.remove("active"));
    b.classList.add("active"); role = b.dataset.r; render();
  }));
  root.querySelector("#people-search").addEventListener("input", (e) => { q = e.target.value.toLowerCase(); render(); });
  root.querySelector("#add-user").addEventListener("click", () => toast("Add user", { msg: "The new-user form opens here.", type: "info" }));
  render();
  return root;
}
