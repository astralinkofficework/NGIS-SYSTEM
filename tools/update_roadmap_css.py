import re

# ==============================================================
# 1. UPDATE CSS (assets/css/exams-simple.css)
# ==============================================================
css_path = 'assets/css/exams-simple.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Replace the previous roadmap CSS section if present
start_mark = "/* ==========================================================================\n   SUBSEQUENT EXAMINATIONS ROADMAP"
if start_mark in css:
    css = css[:css.find(start_mark)].rstrip()

roadmap_css = """
/* ==========================================================================
   SUBSEQUENT EXAMINATIONS ROADMAP (Student Portal Reference Design)
   ========================================================================== */
.exw-roadmap-card {
  background: #ffffff;
  border-radius: 24px;
  border: 1px solid #eef2f6;
  box-shadow: 0 2px 14px -2px rgba(15, 23, 42, 0.04), 0 1px 3px -1px rgba(15, 23, 42, 0.02);
  padding: 24px 20px;
  margin: 0 auto;
  width: 100%;
}
@media (min-width: 640px) {
  .exw-roadmap-card {
    padding: 32px 36px;
  }
}
.exw-roadmap-head {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding-bottom: 22px;
  margin-bottom: 24px;
  border-bottom: 1px solid #f1f5f9;
}
@media (min-width: 640px) {
  .exw-roadmap-head {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
}
.exw-roadmap-title-row {
  display: flex;
  align-items: center;
  gap: 8px;
}
.exw-roadmap-dot {
  width: 8px;
  height: 8px;
  border-radius: 9999px;
  background-color: #0284c7;
  flex-shrink: 0;
}
.exw-roadmap-title {
  font-size: 18px;
  font-weight: 500; /* STRICT NO BOLD */
  color: #0f172a;
  letter-spacing: -0.01em;
  margin: 0;
}
.exw-roadmap-subtitle {
  font-size: 13px;
  color: #94a3b8;
  font-weight: 400;
  margin: 3px 0 0 0;
}
.exw-roadmap-tools {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}
.exw-roadmap-search-wrap {
  position: relative;
}
.exw-roadmap-search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #94a3b8;
  font-size: 16px;
  pointer-events: none;
  display: flex;
  align-items: center;
  line-height: 1;
}
.exw-roadmap-search {
  padding: 6px 14px 6px 34px;
  font-size: 12px;
  font-weight: 400;
  background-color: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 9999px;
  color: #334155;
  width: 175px;
  outline: none;
  transition: all 0.15s ease;
}
.exw-roadmap-search:focus {
  background-color: #ffffff;
  border-color: #3b82f6;
  box-shadow: 0 0 0 1px #3b82f6;
  width: 210px;
}
.exw-roadmap-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  border-radius: 9999px;
  font-size: 12px;
  font-weight: 500;
  background-color: #f0f9ff;
  color: #0284c7;
  border: 1px solid #e0f2fe;
  white-space: nowrap;
}

/* Timeline Layout */
.exw-timeline-item {
  display: flex;
  align-items: stretch;
  position: relative;
  margin-bottom: 20px;
}
.exw-timeline-item:last-child {
  margin-bottom: 0;
}
.exw-timeline-spine {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-right: 22px;
  flex-shrink: 0;
  position: relative;
  width: 34px;
}
@media (max-width: 640px) {
  .exw-timeline-spine {
    margin-right: 12px;
    width: 28px;
  }
}
.exw-timeline-node {
  width: 34px;
  height: 34px;
  border-radius: 9999px;
  background-color: #0b1527;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 500;
  z-index: 2;
  flex-shrink: 0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.15);
}
@media (max-width: 640px) {
  .exw-timeline-node {
    width: 28px;
    height: 28px;
    font-size: 11px;
  }
}
.exw-timeline-line {
  width: 2px;
  background-color: #3b82f6;
  position: absolute;
  top: 34px;
  bottom: -20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1;
}
@media (max-width: 640px) {
  .exw-timeline-line {
    top: 28px;
  }
}
.exw-timeline-item:last-child .exw-timeline-line {
  display: none !important;
}
.exw-timeline-card {
  flex: 1;
  min-width: 0;
  border-radius: 16px;
  background-color: #f8fafc;
  border: 1px solid #f1f5f9;
  padding: 16px 20px;
  transition: all 0.15s ease;
  cursor: pointer;
  text-align: left;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.exw-timeline-card:hover {
  background-color: #f1f5f9;
  border-color: #e2e8f0;
  box-shadow: 0 4px 14px -2px rgba(15, 23, 42, 0.04);
}
.exw-card-top {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}
.exw-pill-time {
  display: inline-flex;
  align-items: center;
  padding: 2.5px 10px;
  border-radius: 9999px;
  font-size: 11px;
  font-weight: 500;
  background-color: #f0f9ff;
  color: #0284c7;
  border: 1px solid #e0f2fe;
  letter-spacing: 0.02em;
  white-space: nowrap;
}
.exw-pill-room {
  display: inline-flex;
  align-items: center;
  padding: 2.5px 10px;
  border-radius: 9999px;
  font-size: 11px;
  font-weight: 400;
  background-color: #f1f5f9;
  color: #475569;
  white-space: nowrap;
}
.exw-card-format {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 400;
  margin-left: auto;
  white-space: nowrap;
}
.exw-card-title {
  font-size: 15px;
  font-weight: 500; /* STRICT NO BOLD */
  color: #0f172a;
  margin: 10px 0 6px 0;
  line-height: 1.35;
  transition: color 0.15s ease;
}
.exw-timeline-card:hover .exw-card-title {
  color: #2563eb;
}
.exw-card-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}
.exw-card-desc {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 400;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  min-width: 0;
  flex: 1;
}
.exw-card-action {
  font-size: 12px;
  font-weight: 500;
  color: #2563eb;
  display: inline-flex;
  align-items: center;
  gap: 3px;
  flex-shrink: 0;
  text-decoration: none;
  transition: color 0.15s ease;
}
.exw-card-action:hover {
  color: #1d4ed8;
}

/* Dark mode adjustments */
[data-theme="dark"] .exw-roadmap-card {
  background: #1e293b;
  border-color: #334155;
}
[data-theme="dark"] .exw-roadmap-head {
  border-color: #334155;
}
[data-theme="dark"] .exw-roadmap-title {
  color: #f8fafc;
}
[data-theme="dark"] .exw-roadmap-search {
  background: #0f172a;
  border-color: #334155;
  color: #e2e8f0;
}
[data-theme="dark"] .exw-timeline-node {
  background-color: #0f172a;
  box-shadow: 0 0 0 2px #334155;
}
[data-theme="dark"] .exw-timeline-card {
  background-color: #0f172a;
  border-color: #334155;
}
[data-theme="dark"] .exw-timeline-card:hover {
  background-color: #1e293b;
}
[data-theme="dark"] .exw-card-title {
  color: #f8fafc;
}
[data-theme="dark"] .exw-pill-room {
  background-color: #1e293b;
  color: #cbd5e1;
}
"""

css += "\n" + roadmap_css
with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated assets/css/exams-simple.css successfully!")
