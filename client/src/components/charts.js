// Lightweight canvas charts — theme-aware (read CSS custom properties).
// Each returns a <canvas> wrapped in a sized container.
import { el } from "../modules/dom.js";

function cssVar(name) {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

function setup(canvas, w, h) {
  const dpr = window.devicePixelRatio || 1;
  canvas.width = w * dpr; canvas.height = h * dpr;
  canvas.style.width = w + "px"; canvas.style.height = h + "px";
  const ctx = canvas.getContext("2d");
  ctx.scale(dpr, dpr);
  return ctx;
}

// Smooth area + line chart
export function lineChart(values, { w = 520, h = 160, accent = "--accent", labels = [] } = {}) {
  const wrap = el("div", { style: { width: "100%" } });
  const canvas = el("canvas");
  wrap.append(canvas);
  const draw = () => {
    const width = wrap.clientWidth || w;
    const ctx = setup(canvas, width, h);
    ctx.clearRect(0, 0, width, h);
    const pad = { l: 8, r: 8, t: 14, b: 22 };
    const max = Math.max(...values) * 1.08, min = Math.min(...values) * 0.92;
    const x = (i) => pad.l + (i * (width - pad.l - pad.r)) / (values.length - 1);
    const y = (v) => pad.t + (1 - (v - min) / (max - min || 1)) * (h - pad.t - pad.b);
    const col = cssVar(accent), grid = cssVar("--border");

    // gridlines
    ctx.strokeStyle = grid; ctx.lineWidth = 1;
    for (let g = 0; g <= 3; g++) {
      const gy = pad.t + (g / 3) * (h - pad.t - pad.b);
      ctx.beginPath(); ctx.moveTo(pad.l, gy); ctx.lineTo(width - pad.r, gy); ctx.stroke();
    }
    // area
    const grad = ctx.createLinearGradient(0, pad.t, 0, h - pad.b);
    grad.addColorStop(0, col + "33"); grad.addColorStop(1, col + "00");
    ctx.beginPath(); ctx.moveTo(x(0), y(values[0]));
    for (let i = 1; i < values.length; i++) {
      const xc = (x(i - 1) + x(i)) / 2;
      ctx.bezierCurveTo(xc, y(values[i - 1]), xc, y(values[i]), x(i), y(values[i]));
    }
    ctx.lineTo(x(values.length - 1), h - pad.b); ctx.lineTo(x(0), h - pad.b); ctx.closePath();
    ctx.fillStyle = grad; ctx.fill();
    // line
    ctx.beginPath(); ctx.moveTo(x(0), y(values[0]));
    for (let i = 1; i < values.length; i++) {
      const xc = (x(i - 1) + x(i)) / 2;
      ctx.bezierCurveTo(xc, y(values[i - 1]), xc, y(values[i]), x(i), y(values[i]));
    }
    ctx.strokeStyle = col; ctx.lineWidth = 2.5; ctx.lineJoin = "round"; ctx.stroke();
    // last point
    ctx.fillStyle = col; ctx.beginPath();
    ctx.arc(x(values.length - 1), y(values[values.length - 1]), 4, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = cssVar("--surface"); ctx.beginPath();
    ctx.arc(x(values.length - 1), y(values[values.length - 1]), 1.8, 0, Math.PI * 2); ctx.fill();
    // labels
    if (labels.length) {
      ctx.fillStyle = cssVar("--text-faint"); ctx.font = "600 10px " + cssVar("--font-ui");
      ctx.textAlign = "center";
      labels.forEach((l, i) => ctx.fillText(l, x(i), h - 6));
    }
  };
  requestAnimationFrame(draw);
  new ResizeObserver(draw).observe(wrap);
  window.addEventListener("ngis:theme", draw);
  return wrap;
}

// Donut chart from [{value, color}] (color = css var name)
export function donut(segments, { size = 132, thickness = 16, center = "" } = {}) {
  const wrap = el("div", { style: { position: "relative", width: size + "px", height: size + "px", flex: "none" } });
  const canvas = el("canvas");
  wrap.append(canvas);
  if (center) {
    const c = el("div", { class: "col center", style: { position: "absolute", inset: "0", textAlign: "center" }, html: center });
    wrap.append(c);
  }
  const draw = () => {
    const ctx = setup(canvas, size, size);
    ctx.clearRect(0, 0, size, size);
    const total = segments.reduce((s, x) => s + x.value, 0) || 1;
    const cx = size / 2, cy = size / 2, r = size / 2 - thickness / 2;
    let a = -Math.PI / 2;
    ctx.lineWidth = thickness; ctx.lineCap = "round";
    // track
    ctx.strokeStyle = cssVar("--surface-3");
    ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.stroke();
    segments.forEach((s) => {
      const ang = (s.value / total) * Math.PI * 2;
      if (s.value <= 0) return;
      ctx.strokeStyle = cssVar(s.color);
      ctx.beginPath(); ctx.arc(cx, cy, r, a, a + ang - 0.04); ctx.stroke();
      a += ang;
    });
  };
  requestAnimationFrame(draw);
  window.addEventListener("ngis:theme", draw);
  return wrap;
}

// Horizontal mini-bars from [{label, value, max, color}]
export function barRow(label, value, max, color = "--accent") {
  return `<div class="col gap-1"><div class="row spread" style="font-size:var(--fs-sm)">
    <span>${label}</span><span class="muted tnum">${value}</span></div>
    <span class="meter"><span style="width:${(value / max) * 100}%;background:var(${color})"></span></span></div>`;
}
