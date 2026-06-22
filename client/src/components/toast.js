import { icon } from "../modules/icons.js";
import { el } from "../modules/dom.js";

const icons = { ok: "checkCircle", info: "bell", warn: "flag", danger: "xCircle" };

export function toast(title, { msg = "", type = "ok", timeout = 3800 } = {}) {
  let host = document.getElementById("toasts");
  if (!host) { host = el("div", { id: "toasts" }); document.body.append(host); }

  const node = el("div", { class: `toast ${type}`, role: "status" });
  node.innerHTML = `
    <span class="t-ic">${icon(icons[type] || "bell")}</span>
    <div class="col" style="gap:2px">
      <span class="t-title">${title}</span>
      ${msg ? `<span class="t-msg">${msg}</span>` : ""}
    </div>`;
  host.append(node);

  const close = () => {
    node.style.transition = "opacity .2s, transform .2s";
    node.style.opacity = "0"; node.style.transform = "translateX(8px)";
    setTimeout(() => node.remove(), 200);
  };
  if (timeout) setTimeout(close, timeout);
  node.addEventListener("click", close);
  return close;
}
