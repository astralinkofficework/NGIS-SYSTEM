import { el } from "../modules/dom.js";
import { icon } from "../modules/icons.js";
import * as d from "../modules/mockData.js";
import { getState } from "../modules/store.js";
import { PageHead, Card, Badge, Btn, Avatar } from "../components/ui.js";
import { openModal } from "../components/modal.js";
import { toast } from "../components/toast.js";

export function announcementsPage() {
  const { role } = getState();
  const root = el("div");
  const canPost = ["teacher", "admin", "super_admin"].includes(role);
  const cats = ["all", "school", "class", "exams", "sports", "emergency", "events"];

  root.innerHTML = `
    ${PageHead({ title: "Announcements", sub: "School, class, and emergency notices",
      action: canPost ? Btn("Post announcement", { variant: "primary", ic: "plus", id: "new-ann" }) : "" })}
    <div class="row wrap gap-2" style="margin-bottom:var(--s-5)" id="cat-filters">
      ${cats.map((c, i) => `<button class="chip ${i===0?"active":""}" data-cat="${c}">${c[0].toUpperCase()+c.slice(1)}</button>`).join("")}
    </div>
    <div class="col gap-3" id="ann-list"></div>`;

  const list = root.querySelector("#ann-list");
  let cat = "all";
  const render = () => {
    const items = d.announcements.filter((a) => cat === "all" || a.category === cat || a.scope === cat)
      .sort((a, b) => (b.pinned - a.pinned) || (new Date(b.date) - new Date(a.date)));
    list.innerHTML = items.map((a) => `
      <article class="card pad ann ${a.pinned ? "pinned" : ""}">
        <div class="row gap-3" style="align-items:flex-start">
          <span class="ann-ic ${d.categoryTone[a.category]||"default"}">${icon(a.category==="emergency"?"flag":a.category==="sports"?"award":a.category==="exams"?"calendar":"megaphone")}</span>
          <div class="col gap-2 grow" style="min-width:0">
            <div class="row spread wrap gap-2">
              <div class="row gap-2 wrap">${a.pinned ? `<span class="row gap-1" style="color:var(--accent);font-size:var(--fs-xs);font-weight:700">${icon("pin")}PINNED</span>` : ""}
                ${Badge(a.category, d.categoryTone[a.category] || "default")}</div>
              <span class="faint" style="font-size:var(--fs-xs)">${new Date(a.date).toLocaleDateString("en-US",{month:"short",day:"numeric"})}</span>
            </div>
            <h3 class="h3">${a.title}</h3>
            <p class="muted" style="font-size:var(--fs-sm)">${a.body}</p>
            <div class="row gap-2" style="margin-top:4px">${Avatar(a.author,"sm")}<span class="muted" style="font-size:var(--fs-sm)">${a.author}</span></div>
          </div>
        </div>
      </article>`).join("");
  };
  root.querySelectorAll("#cat-filters .chip").forEach((b) => b.addEventListener("click", () => {
    root.querySelectorAll("#cat-filters .chip").forEach((x) => x.classList.remove("active"));
    b.classList.add("active"); cat = b.dataset.cat; render();
  }));
  root.querySelector("#new-ann")?.addEventListener("click", openCompose);
  render();
  return root;
}

function openCompose() {
  openModal({
    title: "Post announcement",
    body: `<div class="col gap-4">
      <div class="field"><label>Title</label><input class="input" placeholder="Short, clear headline"></div>
      <div class="row gap-3">
        <div class="field grow"><label>Category</label><select class="select"><option>School</option><option>Class</option><option>Exams</option><option>Sports</option><option>Events</option><option>Emergency</option></select></div>
        <div class="field grow"><label>Audience</label><select class="select"><option>Whole school</option><option>Grade 10-B</option><option>Parents only</option></select></div>
      </div>
      <div class="field"><label>Message</label><textarea class="textarea" placeholder="Write your announcement…"></textarea></div>
      <label class="row gap-2" style="font-size:var(--fs-sm);cursor:pointer"><input type="checkbox" style="width:16px;height:16px;accent-color:var(--accent)"> Pin to top</label>
    </div>`,
    footer: `${Btn("Cancel", { variant: "ghost", attrs: 'data-x="1"' })}${Btn("Publish", { variant: "primary", ic: "megaphone", id: "do-post" })}`,
  });
  document.querySelector("[data-x='1']")?.addEventListener("click", () => document.querySelector(".scrim")?.remove());
  document.getElementById("do-post")?.addEventListener("click", () => {
    toast("Announcement published", { msg: "Your notice is now visible to the audience.", type: "ok" });
    document.querySelector(".scrim")?.remove();
  });
}
