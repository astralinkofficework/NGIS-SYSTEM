import { el } from "../modules/dom.js";
import { icon } from "../modules/icons.js";
import * as d from "../modules/mockData.js";
import { PageHead, Card, StatCard, Badge, Btn, Meter } from "../components/ui.js";
import { toast } from "../components/toast.js";

export function feesPage() {
  const root = el("div");
  const f = d.fees;
  const paidPct = Math.round((f.paid / f.total) * 100);

  root.innerHTML = `
    ${PageHead({ title: "Fees & payments", sub: `${d.school.year} · Maya Chen`,
      action: Btn("Make a payment", { variant: "primary", ic: "wallet", id: "pay" }) })}
    <div class="grid grid-3" style="margin-bottom:var(--s-5)">
      ${StatCard({ label: "Total fees", value: f.currency + f.total.toLocaleString(), ic: "wallet" })}
      ${StatCard({ label: "Paid to date", value: f.currency + f.paid.toLocaleString(), ic: "checkCircle", delta: paidPct + "% complete", deltaTone: "ok" })}
      ${StatCard({ label: "Outstanding", value: f.currency + f.remaining.toLocaleString(), ic: "clock", tone: "gold", delta: "Due Jun 30", deltaTone: "warn" })}
    </div>

    <div class="grid grid-3" style="align-items:start">
      <div class="span-2 col gap-4">
        ${Card({ title: "Fee plan", flush: true, body: `<div class="table-wrap"><table class="table">
          <thead><tr><th>Item</th><th>Due date</th><th class="num">Amount</th><th>Status</th></tr></thead>
          <tbody>${f.plan.map((p) => `<tr>
            <td><strong>${p.label}</strong>${p.paid && p.status==="due"?`<div class="muted" style="font-size:var(--fs-xs)">${f.currency}${p.paid} paid · ${f.currency}${p.amount-p.paid} remaining</div>`:""}</td>
            <td class="muted">${new Date(p.due).toLocaleDateString("en-US",{month:"short",day:"numeric",year:"numeric"})}</td>
            <td class="num tnum">${f.currency}${p.amount.toLocaleString()}</td>
            <td>${p.status==="paid"?Badge("Paid","ok",true):Badge("Due","warn",true)}</td></tr>`).join("")}</tbody></table></div>` })}
        ${Card({ title: "Payment history", flush: true, body: `<div class="table-wrap"><table class="table">
          <thead><tr><th>Date</th><th>Description</th><th>Method</th><th class="num">Amount</th><th>Receipt</th></tr></thead>
          <tbody>${f.history.map((h) => `<tr>
            <td class="muted">${new Date(h.date).toLocaleDateString("en-US",{month:"short",day:"numeric",year:"numeric"})}</td>
            <td>${h.desc}</td><td>${h.method}</td><td class="num tnum">${f.currency}${h.amount.toLocaleString()}</td>
            <td><button class="btn btn-quiet btn-sm" data-receipt="1">${icon("download")}<span class="mono">${h.receipt}</span></button></td></tr>`).join("")}</tbody></table></div>` })}
      </div>
      <div class="col gap-4">
        ${Card({ title: "Payment progress", body: `<div class="col gap-3">
          <div class="row spread"><span class="muted" style="font-size:var(--fs-sm)">Paid</span><strong class="tnum">${paidPct}%</strong></div>
          ${Meter(paidPct, "gold")}
          <div class="row spread" style="font-size:var(--fs-sm)"><span class="muted">${f.currency}${f.paid.toLocaleString()} of ${f.currency}${f.total.toLocaleString()}</span></div>
        </div>` })}
        ${Card({ title: "Scholarships & discounts", body: `<div class="row gap-3">
          <span class="ml-ic" style="color:var(--gold)">${icon("award")}</span>
          <div class="col" style="gap:1px"><strong>${f.scholarship.name}</strong>
            <span class="muted" style="font-size:var(--fs-sm)">−${f.currency}${f.scholarship.amount} applied this year</span></div>
        </div>` })}
        ${Card({ title: "Need help?", body: `<p class="muted" style="font-size:var(--fs-sm)">Questions about fees or payment plans? Contact the bursar's office.</p>
          <div style="margin-top:var(--s-3)">${Btn("Contact bursar", { variant: "ghost", ic: "message", attrs: 'style="width:100%"' })}</div>` })}
      </div>
    </div>`;

  root.querySelector("#pay").addEventListener("click", () =>
    toast("Online payments coming in Phase 3", { msg: "For now, payments are recorded by the bursar's office.", type: "info" }));
  root.querySelectorAll("[data-receipt='1']").forEach((b) => b.addEventListener("click", () =>
    toast("Receipt downloaded", { type: "ok" })));
  return root;
}
