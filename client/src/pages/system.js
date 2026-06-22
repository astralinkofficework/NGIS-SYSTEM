import { el } from "../modules/dom.js";
import { icon } from "../modules/icons.js";
import * as d from "../modules/mockData.js";
import { PageHead, Card, Badge, Btn } from "../components/ui.js";
import { toast } from "../components/toast.js";

export function systemPage() {
  const root = el("div");
  root.innerHTML = `
    ${PageHead({ title: "System health", sub: "Infrastructure, backups, and security — Super Admin only" })}
    <div class="grid grid-4" style="margin-bottom:var(--s-5)">
      ${d.systemHealth.map((h) => `<div class="stat">
        <div class="stat-top"><div class="stat-ic">${icon(h.icon)}</div>${Badge(h.status, h.status==="operational"?"ok":"warn", true)}</div>
        <div class="stat-val" style="font-size:1.3rem">${h.metric}</div>
        <div class="stat-label">${h.name} · ${h.sub}</div></div>`).join("")}
    </div>
    <div class="grid grid-3" style="align-items:start">
      <div class="span-2 col gap-4">
        ${Card({ title: "Backups", flush: true, action: Btn("Run backup now", { variant: "ghost", size: "sm", ic: "refresh", id: "rb" }), body: `
          <div class="table-wrap"><table class="table"><thead><tr><th>When</th><th>Type</th><th class="num">Size</th><th>Location</th><th>Status</th><th></th></tr></thead>
          <tbody>${d.backups.map((b) => `<tr><td class="mono" style="font-size:var(--fs-xs)">${b.date}</td><td>${b.type}</td>
            <td class="num tnum">${b.size}</td><td class="mono" style="font-size:var(--fs-xs)">${b.location}</td>
            <td>${Badge(b.status, b.status==="success"?"ok":"warn", true)}</td>
            <td class="num"><button class="btn btn-quiet btn-sm" data-restore="1">Restore</button></td></tr>`).join("")}</tbody></table></div>` })}
        ${Card({ title: "Security & device log", flush: true, body: `<ul class="mini-list">${d.securityLog.map((l)=>`
          <li><span class="ml-ic ${l.level==="warn"?"warn":""}" ${l.level==="ok"?'style="color:var(--ok)"':""}>${icon(l.level==="warn"?"flag":"shield")}</span>
          <span class="col grow" style="min-width:0"><strong>${l.action}</strong><span class="muted" style="font-size:var(--fs-xs)">${l.actor} · ${l.ip}</span></span>
          <span class="ml-meta mono">${l.time}</span></li>`).join("")}</ul>` })}
      </div>
      <div class="col gap-4">
        ${Card({ title: "Cloudflare & edge", body: `<div class="col gap-3">
          <div class="row spread"><span class="muted" style="font-size:var(--fs-sm)">WAF</span>${Badge("Active","ok",true)}</div>
          <div class="row spread"><span class="muted" style="font-size:var(--fs-sm)">Rate limiting</span>${Badge("Enforced","ok",true)}</div>
          <div class="row spread"><span class="muted" style="font-size:var(--fs-sm)">Bot mitigation</span>${Badge("1 rule throttled","warn",true)}</div>
          <div class="row spread"><span class="muted" style="font-size:var(--fs-sm)">TLS</span><strong>TLS 1.3 · HSTS</strong></div>
        </div>` })}
        ${Card({ title: "Maintenance mode", body: `<div class="col gap-3">
          <p class="muted" style="font-size:var(--fs-sm)">When on, only Super Admins can sign in.</p>
          <label class="switch-row"><span>Maintenance mode</span><span class="switch"><input type="checkbox" id="maint"><span class="slider"></span></span></label>
        </div>` })}
        ${Card({ title: "Branding", body: `<div class="col gap-3">
          <div class="row spread"><span class="muted" style="font-size:var(--fs-sm)">School name</span><strong>${d.school.short}</strong></div>
          <div class="row spread"><span class="muted" style="font-size:var(--fs-sm)">Primary color</span><span class="row gap-2"><span class="swatch" style="background:var(--accent)"></span><span class="mono">#2B59C3</span></span></div>
          ${Btn("Edit branding", { variant: "ghost", ic: "edit", attrs: 'style="width:100%"' })}
        </div>` })}
      </div>
    </div>`;

  root.querySelector("#rb").addEventListener("click", () => toast("Backup started", { msg: "Running a full backup.", type: "info" }));
  root.querySelectorAll("[data-restore='1']").forEach((b) => b.addEventListener("click", () =>
    toast("Restore requires confirmation", { msg: "Follow the restore runbook before proceeding.", type: "warn" })));
  root.querySelector("#maint").addEventListener("change", (e) =>
    toast(e.target.checked ? "Maintenance mode on" : "Maintenance mode off", { type: e.target.checked ? "warn" : "ok" }));
  return root;
}
