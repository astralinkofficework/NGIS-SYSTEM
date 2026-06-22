// Reusable UI primitives that return HTML strings (composable into pages).
import { icon } from "../modules/icons.js";
import { esc, initials } from "../modules/dom.js";

export const Avatar = (name, size = "md", url = null) =>
  `<span class="avatar avatar-${size}">${url ? `<img src="${esc(url)}" alt="${esc(name)}">` : esc(initials(name))}</span>`;

export const Badge = (label, tone = "default", dot = false) => {
  const cls = tone === "default" ? "badge" : `badge badge-${tone}`;
  return `<span class="${cls}">${dot ? '<span class="dot"></span>' : ""}${esc(label)}</span>`;
};

export const Btn = (label, { variant = "primary", size = "", ic = "", id = "", attrs = "" } = {}) =>
  `<button class="btn btn-${variant}${size ? " btn-" + size : ""}" ${id ? `id="${id}"` : ""} ${attrs}>${ic ? icon(ic) : ""}${label ? `<span>${esc(label)}</span>` : ""}</button>`;

export const IconBtn = (ic, { size = "", title = "", id = "", attrs = "" } = {}) =>
  `<button class="btn btn-ghost btn-icon${size ? " btn-" + size : ""}" ${id ? `id="${id}"` : ""} ${title ? `title="${esc(title)}" aria-label="${esc(title)}"` : ""} ${attrs}>${icon(ic)}</button>`;

export const Meter = (pct, tone = "") =>
  `<span class="meter ${tone}"><span style="width:${Math.max(0, Math.min(100, pct))}%"></span></span>`;

export const StatCard = ({ label, value, ic, tone = "", delta = "", deltaTone = "muted" }) => `
  <div class="stat ${tone}">
    <div class="stat-top">
      <div class="stat-ic">${icon(ic)}</div>
      ${delta ? `<span class="stat-delta" style="color:var(--${deltaTone})">${esc(delta)}</span>` : ""}
    </div>
    <div class="stat-val tnum">${esc(value)}</div>
    <div class="stat-label">${esc(label)}</div>
  </div>`;

export const Card = ({ title = "", action = "", body = "", pad = true, flush = false, attrs = "" } = {}) => `
  <section class="card" ${attrs}>
    ${title || action ? `<div class="card-head"><span class="title">${esc(title)}</span>${action || ""}</div>` : ""}
    <div class="card-body${flush ? " flush" : ""}" ${!pad && !flush ? 'style="padding:0"' : ""}>${body}</div>
  </section>`;

export const EmptyState = ({ ic = "inbox", title = "Nothing here yet", msg = "", action = "" }) => `
  <div class="state">
    <div class="state-ic">${icon(ic)}</div>
    <div class="state-title">${esc(title)}</div>
    ${msg ? `<p class="muted" style="max-width:34ch">${esc(msg)}</p>` : ""}
    ${action || ""}
  </div>`;

export const ErrorState = ({ title = "Something went wrong", msg = "We couldn't load this. Try again.", action = "" }) => `
  <div class="state error">
    <div class="state-ic">${icon("xCircle")}</div>
    <div class="state-title">${esc(title)}</div>
    <p class="muted" style="max-width:36ch">${esc(msg)}</p>
    ${action || ""}
  </div>`;

export const SkeletonRows = (rows = 5) =>
  Array.from({ length: rows }, () =>
    `<div class="row gap-3" style="padding:12px 16px"><div class="skel" style="width:30px;height:30px;border-radius:50%"></div><div class="col gap-2 grow"><div class="skel line short"></div><div class="skel line" style="width:60%"></div></div></div>`
  ).join("");

export const PageHead = ({ eyebrow = "", title, sub = "", action = "" }) => `
  <div class="page-head">
    <div>
      ${eyebrow ? `<div class="eyebrow" style="margin-bottom:6px">${esc(eyebrow)}</div>` : ""}
      <h1 class="ptitle">${esc(title)}</h1>
      ${sub ? `<div class="psub">${esc(sub)}</div>` : ""}
    </div>
    ${action ? `<div class="row gap-2">${action}</div>` : ""}
  </div>`;

export const Search = (placeholder = "Search…", id = "") =>
  `<div class="search">${icon("search")}<input class="input" type="search" placeholder="${esc(placeholder)}" ${id ? `id="${id}"` : ""} aria-label="${esc(placeholder)}"></div>`;
