import { el } from "../modules/dom.js";
import { icon } from "../modules/icons.js";
import * as d from "../modules/mockData.js";
import { PageHead, Badge, Btn, Search } from "../components/ui.js";
import { toast } from "../components/toast.js";

const typeIc = { report_card: "award", certificate: "star", exam_slip: "calendar", letter: "mail", lesson_plan: "book" };

export function documentsPage() {
  const root = el("div");
  root.innerHTML = `
    ${PageHead({ title: "My documents", sub: "Report cards, certificates, and letters — secured with signed links",
      action: `<div style="width:240px">${Search("Search documents…")}</div>` })}
    <div class="doc-grid">${d.documents.map((doc) => `
      <article class="card pad doc-card">
        <div class="row spread"><span class="doc-ic">${icon(typeIc[doc.type]||"file")}</span>${Badge(d.docTypeLabel[doc.type]||doc.type,"default")}</div>
        <h3 class="h3" style="margin-top:var(--s-3)">${doc.name}</h3>
        <p class="muted" style="font-size:var(--fs-sm);margin-top:4px">${new Date(doc.date).toLocaleDateString("en-US",{year:"numeric",month:"long",day:"numeric"})} · ${doc.size}</p>
        <div class="row gap-2" style="margin-top:var(--s-4)">
          ${Btn("Download", { variant: "ghost", size: "sm", ic: "download", attrs: 'data-dl="1"' })}
          ${Btn("Preview", { variant: "quiet", size: "sm" })}
        </div>
      </article>`).join("")}</div>`;
  root.querySelectorAll("[data-dl='1']").forEach((b) => b.addEventListener("click", () =>
    toast("Download started", { msg: "Generating a secure signed link…", type: "info" })));
  return root;
}
