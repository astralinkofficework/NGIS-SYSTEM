import re

# 1. Update assets/css/portal-dashboard.css
with open('assets/css/portal-dashboard.css', 'r', encoding='utf-8') as f:
    pd_css = f.read()

principal_css_additions = """
/* ══════════════════════════════════════
   PRINCIPAL EXECUTIVE DASHBOARD RESPONSIVE STYLES
   ══════════════════════════════════════ */

/* ── Live Campus Operations Feed (Column 2) ── */
.ov-feed-panel {
  border: 1px solid var(--border, #E5E5E8);
  border-radius: 10px;
  background: var(--surface-2, #F3F3F5);
  padding: 10px 12px;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.ov-feed-head {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11.5px;
  font-weight: 500;
  color: var(--heading, #000000);
  margin-bottom: 8px;
}

.ov-feed-live-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background-color: var(--accent, #92243D);
  animation: feedPulse 2s infinite ease-in-out;
  flex-shrink: 0;
}

.ov-feed-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.ov-feed-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 11px;
  line-height: 1.35;
  padding: 4px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.ov-feed-item:last-child {
  border-bottom: none;
}

.ov-feed-icon {
  font-size: 16px !important;
  flex-shrink: 0;
  margin-top: 1px;
}

.ov-feed-text {
  flex: 1;
  min-width: 0;
  color: var(--text, #000000);
}

.ov-feed-text strong {
  font-weight: 500;
}

.ov-feed-time {
  font-size: 10px;
  color: var(--muted, #555555);
  flex-shrink: 0;
  margin-left: auto;
  white-space: nowrap;
}

/* ── Priority Action Items (Column 3) ── */
.ov-task-list {
  padding: 8px 14px 14px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.ov-task-card {
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid var(--border, #E5E5E8);
  background: var(--surface-2, #F3F3F5);
  display: flex;
  flex-direction: column;
  gap: 3px;
  transition: all 0.15s ease;
}

.ov-task-card:hover {
  background: #FFFFFF !important;
  border-color: var(--primary, #202F63) !important;
}

.ov-task-card.ov-task-urgent {
  border-left: 3px solid var(--accent, #92243D) !important;
}

.ov-task-card.ov-task-warn {
  border-left: 3px solid var(--primary, #202F63) !important;
}

.ov-task-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2px;
}

.ov-task-badge-urgent {
  font-size: 10px;
  font-weight: 500;
  padding: 1px 7px;
  border-radius: 999px;
  background: #FFFFFF;
  color: var(--accent, #92243D);
  border: 1px solid var(--accent, #92243D);
}

.ov-task-badge-warn {
  font-size: 10px;
  font-weight: 500;
  padding: 1px 7px;
  border-radius: 999px;
  background: #FFFFFF;
  color: var(--primary, #202F63);
  border: 1px solid var(--border, #E5E5E8);
}

.ov-task-badge-ok {
  font-size: 10px;
  font-weight: 500;
  padding: 1px 7px;
  border-radius: 999px;
  background: #FFFFFF;
  color: var(--text, #000000);
  border: 1px solid var(--border, #E5E5E8);
}

.ov-task-due {
  font-size: 10px;
  color: var(--muted, #555555);
}

.ov-task-title {
  font-size: 12px;
  font-weight: 500;
  color: var(--heading, #000000);
  line-height: 1.3;
}

.ov-task-sub {
  font-size: 10.5px;
  color: var(--muted, #555555);
  line-height: 1.3;
}

/* ── Executive Metrics Row (dash-kpi-row) ── */
.dash-kpi-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  max-width: 1280px;
  margin: 0 auto 20px;
  padding: 0 24px;
  box-sizing: border-box;
}

@media (max-width: 1024px) {
  .dash-kpi-row {
    grid-template-columns: repeat(2, 1fr);
    padding: 0 16px;
  }
}

@media (max-width: 520px) {
  .dash-kpi-row {
    grid-template-columns: 1fr;
  }
}

.dash-kpi-card {
  background: var(--surface, #FFFFFF);
  border: 1px solid var(--border, #E5E5E8);
  border-radius: 14px;
  padding: 16px 20px;
  box-shadow: var(--shadow-sm, 0 1px 3px rgba(0, 0, 0, 0.04));
  display: flex;
  flex-direction: column;
  justify-content: center;
  transition: border-color 0.15s ease;
  min-width: 0;
  box-sizing: border-box;
}

.dash-kpi-card:hover {
  border-color: var(--primary, #202F63) !important;
}

.dash-kpi-val {
  font-size: 26px;
  font-weight: 500;
  line-height: 1.2;
  font-variant-numeric: tabular-nums;
}

.dash-kpi-lbl {
  font-size: 11.5px;
  font-weight: 500;
  color: var(--muted, #555555);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-top: 4px;
}

/* ── Executive Quick Action Buttons (dash-quick-row) ── */
.dash-quick-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  max-width: 1280px;
  margin: 0 auto 24px;
  padding: 0 24px;
  box-sizing: border-box;
}

@media (max-width: 1024px) {
  .dash-quick-row {
    grid-template-columns: repeat(2, 1fr);
    padding: 0 16px;
  }
}

@media (max-width: 520px) {
  .dash-quick-row {
    grid-template-columns: 1fr;
  }
}

.dash-quick-btn {
  background: var(--surface, #FFFFFF);
  border: 1px solid var(--border, #E5E5E8);
  border-radius: 14px;
  padding: 14px 18px;
  display: flex;
  align-items: center;
  gap: 14px;
  text-decoration: none;
  box-shadow: var(--shadow-sm, 0 1px 3px rgba(0, 0, 0, 0.04));
  transition: all 0.15s ease;
  min-width: 0;
  box-sizing: border-box;
}

.dash-quick-btn:hover {
  background: var(--surface-2, #F3F3F5) !important;
  border-color: var(--primary, #202F63) !important;
  transform: none !important;
}

.dash-quick-btn .material-symbols-outlined {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: var(--surface-2, #F3F3F5);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
  transition: background-color 0.15s ease;
}

.dash-quick-btn:hover .material-symbols-outlined {
  background: #FFFFFF;
}

.dash-quick-btn span:last-child {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.dash-quick-btn b {
  font-size: 13.5px;
  font-weight: 500;
  color: var(--heading, #000000);
  line-height: 1.3;
}

.dash-quick-btn small {
  font-size: 11px;
  color: var(--muted, #555555);
  margin-top: 1px;
}

/* ── Digital ID Modal Enhancements ── */
.id-card-wrapper {
  width: 100%;
  max-width: 440px;
  margin: 0 auto;
  position: relative;
}

.id-modal-close {
  position: absolute;
  top: 10px;
  right: 14px;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: #FFFFFF;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  transition: background 0.15s ease;
}

.id-modal-close:hover {
  background: rgba(255, 255, 255, 0.35);
}

/* ── Responsive Refinements for 769px - 1240px ── */
@media (max-width: 1240px) and (min-width: 961px) {
  .dash-overlap {
    grid-template-columns: minmax(0, 1fr) minmax(260px, 300px);
    padding: 0 20px;
    margin-top: -32px;
  }
  .ov-profile {
    grid-column: 1 / -1;
  }
  .ov-inner-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .ov-feed-panel {
    grid-column: 1 / -1;
  }
}

@media (max-width: 960px) and (min-width: 769px) {
  .dash-overlap {
    grid-template-columns: 1fr;
    padding: 0 16px;
    margin-top: -24px;
  }
  .ov-inner-grid {
    grid-template-columns: 1fr;
  }
}
"""

if "PRINCIPAL EXECUTIVE DASHBOARD RESPONSIVE STYLES" not in pd_css:
    pd_css += "\n" + principal_css_additions
    with open('assets/css/portal-dashboard.css', 'w', encoding='utf-8') as f:
        f.write(pd_css)
    print("Added principal responsive styles to assets/css/portal-dashboard.css")
else:
    print("Principal responsive styles already present in portal-dashboard.css")


# 2. Update pages/principal/principal.html
with open('pages/principal/principal.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace gradient on mobile executive card
old_grad = 'bg-gradient-to-br from-slate-900 via-slate-800 to-amber-950 text-white p-5 shadow-sm border border-slate-200'
new_card = 'bg-[#202F63] text-white p-5 shadow-xs border border-[#202F63]'
if old_grad in html:
    html = html.replace(old_grad, new_card)
    print("Replaced mobile executive card gradient.")

# Fix Authorize button in mobile view to use Burgundy #92243D
html = html.replace(
    'bg-[#000000] text-white text-[11px] font-medium rounded-lg shadow-xs hover:bg-[#000000]',
    'bg-[#92243D] text-white text-[11px] font-medium rounded-lg shadow-xs hover:bg-[#7E1E34]'
)

# Fix Inspect button in mobile view to use clean neutral soft gray
html = html.replace(
    'bg-gray-200 text-gray-700 text-[11px] font-medium rounded-lg hover:bg-gray-300',
    'bg-[#F3F3F5] text-[#000000] border border-[#E5E5E8] text-[11px] font-medium rounded-lg hover:bg-[#FFFFFF]'
)

# Replace id card front gradient with solid Navy #202F63
old_id_grad = 'style="background:linear-gradient(145deg, #000000 0%, #202F63 60%, #92243D 100%)"'
new_id_bg = 'style="background:#202F63;border:1px solid #202F63"'
if old_id_grad in html:
    html = html.replace(old_id_grad, new_id_bg)
    print("Replaced ID modal card gradient with solid Navy #202F63.")

# Optimize mobile 4-tile grid for extra-small screens
old_grid_4 = '<div class="grid grid-cols-4 gap-2.5">'
new_grid_4 = '<div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5">'
if old_grid_4 in html:
    html = html.replace(old_grid_4, new_grid_4, 1)
    print("Optimized mobile 4-tile quick action grid.")

with open('pages/principal/principal.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated pages/principal/principal.html successfully!")

