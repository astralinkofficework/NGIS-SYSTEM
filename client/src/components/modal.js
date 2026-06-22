import { icon } from "../modules/icons.js";
import { el } from "../modules/dom.js";

// openModal({ title, body (html string or node), footer (html), onMount })
export function openModal({ title = "", body = "", footer = "", maxWidth = "" } = {}) {
  const scrim = el("div", { class: "scrim", role: "dialog", "aria-modal": "true" });
  const modal = el("div", { class: "modal" });
  if (maxWidth) modal.style.maxWidth = maxWidth;

  const head = el("div", { class: "modal-head" });
  head.innerHTML = `<h2 class="h2 display">${title}</h2>`;
  const closeBtn = el("button", { class: "btn btn-quiet btn-icon btn-sm", "aria-label": "Close", html: icon("x") });
  head.append(closeBtn);

  const bodyEl = el("div", { class: "modal-body" });
  if (typeof body === "string") bodyEl.innerHTML = body; else bodyEl.append(body);

  modal.append(head, bodyEl);
  if (footer) {
    const foot = el("div", { class: "modal-foot" });
    if (typeof footer === "string") foot.innerHTML = footer; else foot.append(footer);
    modal.append(foot);
  }
  scrim.append(modal);

  const close = () => { scrim.style.opacity = "0"; setTimeout(() => scrim.remove(), 150); document.removeEventListener("keydown", onKey); };
  const onKey = (e) => { if (e.key === "Escape") close(); };
  closeBtn.addEventListener("click", close);
  scrim.addEventListener("mousedown", (e) => { if (e.target === scrim) close(); });
  document.addEventListener("keydown", onKey);

  document.body.append(scrim);
  setTimeout(() => modal.querySelector("input,button,textarea,select")?.focus(), 50);
  return { scrim, modal, close };
}
