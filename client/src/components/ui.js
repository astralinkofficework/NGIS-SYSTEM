/* UI primitives as string builders + a few imperative widgets (toast, modal).
   Keeps pages declarative: build HTML strings, mount once, wire events. */
import { icon } from '../modules/icons.js';

export const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => (
  { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
));

/* ---------------- String builders ---------------- */
export function statCard({ label, value, icon: ic, delta, deltaDir }) {
  return `<div class="card stat">
    <div class="stat-top">
      <span class="stat-label">${esc(label)}</span>
      ${ic ? `<span class="stat-icon">${icon(ic)}</span>` : ''}
    </div>
    <div class="stat-value">${esc(value)}</div>
    ${delta ? `<span class="stat-delta ${deltaDir === 'down' ? 'down' : 'up'}">${icon(deltaDir === 'down' ? 'arrowDown' : 'arrowUp')}${esc(delta)}</span>` : ''}
  </div>`;
}

export function badge(text, variant = '') {
  return `<span class="badge ${variant ? 'badge-' + variant : ''}">${esc(text)}</span>`;
}

const ATT = { present: 'success', late: 'warning', absent: 'danger', excused: 'info' };
export function attBadge(status) {
  return `<span class="badge badge-${ATT[status] || ''}"><span class="dot"></span>${esc(status[0].toUpperCase() + status.slice(1))}</span>`;
}

export function avatar(initials, cls = '') {
  return `<span class="avatar ${cls}">${esc(initials)}</span>`;
}

export function pageHead({ title, subtitle, actions = '' }) {
  return `<div class="page-head">
    <div><h1 class="page-title">${esc(title)}</h1>${subtitle ? `<p class="page-subtitle">${esc(subtitle)}</p>` : ''}</div>
    ${actions ? `<div class="row gap-2">${actions}</div>` : ''}
  </div>`;
}

export function emptyState({ icon: ic = 'inbox', title, text, action = '' }) {
  return `<div class="state">
    <div class="state-icon">${icon(ic)}</div>
    <h4>${esc(title)}</h4>${text ? `<p>${esc(text)}</p>` : ''}${action}
  </div>`;
}

export function errorState({ title = 'Something went wrong', text = 'We couldn’t load this. Please retry.', action = '' }) {
  return `<div class="state error">
    <div class="state-icon">${icon('alert')}</div>
    <h4>${esc(title)}</h4><p>${esc(text)}</p>${action}
  </div>`;
}

export function skeletonRows(n = 5) {
  return `<div class="card card-pad">${Array.from({ length: n }).map(() =>
    `<div class="row gap-3" style="padding:8px 0"><div class="skeleton" style="width:36px;height:36px;border-radius:50%"></div>
      <div class="grow"><div class="skeleton sk-line lg" style="width:40%"></div><div class="skeleton sk-line" style="width:70%"></div></div></div>`
  ).join('')}</div>`;
}

export function progress(pct, variant = '') {
  return `<div class="progress ${variant}"><span style="width:${Math.max(0, Math.min(100, pct))}%"></span></div>`;
}

/* ---------------- Toasts ---------------- */
let toastRegion;
export function toast(message, { type = 'info', title } = {}) {
  if (!toastRegion) {
    toastRegion = document.createElement('div');
    toastRegion.className = 'toast-region';
    toastRegion.setAttribute('aria-live', 'polite');
    document.body.appendChild(toastRegion);
  }
  const map = { success: 'checkCircle', error: 'xCircle', warning: 'alert', info: 'info' };
  const el = document.createElement('div');
  el.className = `toast ${type}`;
  el.setAttribute('role', 'status');
  el.innerHTML = `${icon(map[type] || 'info')}<div class="grow">
    ${title ? `<div class="t-title">${esc(title)}</div>` : ''}<div class="t-msg">${esc(message)}</div></div>`;
  toastRegion.appendChild(el);
  setTimeout(() => { el.style.transition = 'opacity .2s, transform .2s'; el.style.opacity = '0'; el.style.transform = 'translateX(16px)'; setTimeout(() => el.remove(), 220); }, 3200);
}

/* ---------------- Modal ---------------- */
export function modal({ title, body, footer }) {
  const overlay = document.createElement('div');
  overlay.className = 'overlay';
  overlay.innerHTML = `<div class="modal" role="dialog" aria-modal="true" aria-label="${esc(title)}">
    <div class="modal-header"><h3>${esc(title)}</h3>
      <button class="icon-btn" data-close aria-label="Close">${icon('x')}</button></div>
    <div class="modal-body">${body}</div>
    ${footer ? `<div class="modal-footer">${footer}</div>` : ''}
  </div>`;
  const close = () => { overlay.style.opacity = '0'; setTimeout(() => overlay.remove(), 180); };
  overlay.addEventListener('click', (e) => { if (e.target === overlay || e.target.closest('[data-close]')) close(); });
  document.addEventListener('keydown', function esc2(e) { if (e.key === 'Escape') { close(); document.removeEventListener('keydown', esc2); } });
  document.body.appendChild(overlay);
  return { el: overlay, close };
}

/* ---------------- Charts (hand-rolled SVG, no libs) ---------------- */
export function lineChart(data, { w = 520, h = 160, color = 'var(--chart-1)', labels = [] } = {}) {
  const max = Math.max(...data) * 1.1, min = Math.min(...data) * 0.9;
  const pad = 24, iw = w - pad * 2, ih = h - pad * 2;
  const pts = data.map((v, i) => {
    const x = pad + (i / (data.length - 1)) * iw;
    const y = pad + ih - ((v - min) / (max - min || 1)) * ih;
    return [x, y];
  });
  const line = pts.map((p, i) => (i ? 'L' : 'M') + p[0].toFixed(1) + ',' + p[1].toFixed(1)).join(' ');
  const area = line + ` L${pad + iw},${pad + ih} L${pad},${pad + ih} Z`;
  const grid = [0, 0.5, 1].map((g) => `<line x1="${pad}" y1="${pad + g * ih}" x2="${pad + iw}" y2="${pad + g * ih}" stroke="var(--chart-grid)" stroke-width="1"/>`).join('');
  const lab = labels.map((l, i) => `<text x="${pad + (i / (labels.length - 1)) * iw}" y="${h - 4}" text-anchor="middle" font-size="11" fill="var(--text-muted)">${esc(l)}</text>`).join('');
  return `<svg viewBox="0 0 ${w} ${h}" width="100%" height="${h}" role="img" aria-label="Line chart">
    <defs><linearGradient id="lg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${color}" stop-opacity="0.18"/><stop offset="1" stop-color="${color}" stop-opacity="0"/></linearGradient></defs>
    ${grid}<path d="${area}" fill="url(#lg)"/><path d="${line}" fill="none" stroke="${color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
    ${pts.map((p) => `<circle cx="${p[0].toFixed(1)}" cy="${p[1].toFixed(1)}" r="3" fill="var(--bg-elevated)" stroke="${color}" stroke-width="2"/>`).join('')}${lab}</svg>`;
}

export function barChart(items, { w = 360, h = 180, color = 'var(--chart-1)' } = {}) {
  const max = Math.max(...items.map((i) => i.value)) * 1.15;
  const pad = 24, iw = w - pad * 2, ih = h - pad * 2;
  const bw = iw / items.length * 0.55, gap = iw / items.length;
  return `<svg viewBox="0 0 ${w} ${h}" width="100%" height="${h}" role="img" aria-label="Bar chart">
    ${items.map((it, i) => {
      const bh = (it.value / max) * ih, x = pad + i * gap + (gap - bw) / 2, y = pad + ih - bh;
      return `<rect x="${x}" y="${y}" width="${bw}" height="${bh}" rx="4" fill="${color}"/>
      <text x="${x + bw / 2}" y="${y - 6}" text-anchor="middle" font-size="11" font-weight="600" fill="var(--text-secondary)">${it.value}</text>
      <text x="${x + bw / 2}" y="${h - 5}" text-anchor="middle" font-size="11" fill="var(--text-muted)">${esc(it.label)}</text>`;
    }).join('')}</svg>`;
}

export function ringChart(pct, { size = 120, color = 'var(--accent)', label } = {}) {
  const r = (size - 16) / 2, c = 2 * Math.PI * r, off = c - (pct / 100) * c;
  return `<div style="position:relative;width:${size}px;height:${size}px">
    <svg class="ring" width="${size}" height="${size}">
      <circle class="track" cx="${size / 2}" cy="${size / 2}" r="${r}"></circle>
      <circle class="value" cx="${size / 2}" cy="${size / 2}" r="${r}" stroke="${color}" stroke-dasharray="${c}" stroke-dashoffset="${off}"></circle>
    </svg>
    <div style="position:absolute;inset:0;display:grid;place-items:center;text-align:center">
      <div><div style="font-size:var(--text-2xl);font-weight:700;font-variant-numeric:tabular-nums">${pct}%</div>
      ${label ? `<div style="font-size:var(--text-xs);color:var(--text-muted)">${esc(label)}</div>` : ''}</div></div></div>`;
}
