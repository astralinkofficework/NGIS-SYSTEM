import os

css_block = """
/* ============================================================================
   NGIS ERP — GLOBAL STANDARDIZED PAGINATION & STATUS SYSTEM (SECTIONS 1–4)
   ============================================================================ */

/* ── 1. Global Standardized Pagination ── */
.ngis-pagination-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  padding: 12px 18px;
  background: var(--card-bg, #ffffff);
  border-top: 1px solid var(--border, #e2e8f0);
  box-sizing: border-box;
  width: 100%;
}

.ngis-pagination-summary {
  font-size: 12.5px;
  font-weight: 400;
  color: var(--muted, #64748b);
  line-height: 1.5;
}

.ngis-pagination-summary .font-medium {
  font-weight: 500;
  color: var(--text, #0f172a);
}

.ngis-pagination-controls {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

/* Base pagination button */
.ngis-pag-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  min-height: 38px;
  padding: 0 14px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
  user-select: none;
  box-sizing: border-box;
}

.ngis-pag-btn:active:not(:disabled) {
  transform: scale(0.97);
}

/* Previous button: neutral white/transparent */
.ngis-pag-prev {
  background: #ffffff;
  color: #334155;
  border: 1px solid #cbd5e1;
}

.ngis-pag-prev:hover:not(:disabled) {
  background: #f8fafc;
  border-color: #94a3b8;
  color: #0f172a;
}

.ngis-pag-prev:disabled,
.ngis-pag-prev.is-disabled {
  opacity: 0.4;
  cursor: not-allowed;
  pointer-events: none;
  background: #f8fafc;
  border-color: #e2e8f0;
}

/* Next button: NGIS primary institutional green */
.ngis-pag-next {
  background: #0f5132;
  color: #ffffff;
  border: 1px solid #0f5132;
}

.ngis-pag-next:hover:not(:disabled) {
  background: #146c43;
  border-color: #146c43;
}

.ngis-pag-next:disabled,
.ngis-pag-next.is-disabled {
  opacity: 0.4;
  cursor: not-allowed;
  pointer-events: none;
  background: #e2e8f0;
  color: #94a3b8;
  border-color: #cbd5e1;
}

/* Numerical Page Buttons */
.ngis-pagination-numbers {
  display: flex;
  align-items: center;
  gap: 4px;
}

.ngis-pag-number {
  min-width: 36px;
  height: 38px;
  padding: 0 10px;
  background: transparent;
  color: #475569;
  border: 1px solid transparent;
  border-radius: 8px;
}

.ngis-pag-number:hover:not(.is-active) {
  background: #f1f5f9;
  color: #0f172a;
}

.ngis-pag-number.is-active {
  background: #e2f4ea;
  color: #0f5132;
  border-color: #bbf7d0;
  font-weight: 500;
}

.ngis-pag-ellipsis {
  padding: 0 4px;
  color: #94a3b8;
  font-size: 13px;
  user-select: none;
}

/* Progress Dots Mode (for multi-step flows) */
.ngis-pagination-dots {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 0 8px;
}

.ngis-pag-dot {
  width: 8px;
  height: 8px;
  border-radius: 9999px;
  background: #cbd5e1;
  border: none;
  padding: 0;
  cursor: pointer;
  transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
}

.ngis-pag-dot:hover:not(.is-active) {
  background: #94a3b8;
}

.ngis-pag-dot.is-active {
  width: 22px;
  background: #0f5132;
}

/* Responsive mobile adjustments */
@media (max-width: 640px) {
  .ngis-pagination-wrapper {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
    padding: 12px 14px;
  }
  .ngis-pagination-summary {
    text-align: center;
  }
  .ngis-pagination-controls {
    justify-content: space-between;
    width: 100%;
  }
  .ngis-pag-prev,
  .ngis-pag-next {
    flex: 1;
    min-height: 42px; /* iOS 44px touch target standard */
  }
  .ngis-pagination-numbers {
    flex-wrap: wrap;
    justify-content: center;
  }
}

/* ── 2. Centralized Status Indicators ── */
.ngis-status-indicator {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
  font-weight: 500;
  transition: all 0.2s ease;
  line-height: 1;
  box-sizing: border-box;
}

.ngis-status-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  width: 14px;
  height: 14px;
  flex-shrink: 0;
}

.ngis-status-label {
  font-size: 12px;
  font-weight: 500;
}

/* Badge variant (soft tinted background pill) */
.ngis-status-badge {
  padding: 4px 10px;
  border-radius: 9999px;
  border: 1px solid transparent;
  min-height: 24px;
}

/* Color Tokens: Gray */
.ngis-status-badge.ngis-status--gray {
  background-color: #f1f5f9;
  color: #475569;
  border-color: #e2e8f0;
}

/* Color Tokens: Amber / Orange */
.ngis-status-badge.ngis-status--amber {
  background-color: #fffbeb;
  color: #b45309;
  border-color: #fde68a;
}

/* Color Tokens: Blue */
.ngis-status-badge.ngis-status--blue {
  background-color: #eff6ff;
  color: #1d4ed8;
  border-color: #bfdbfe;
}

/* Color Tokens: Green */
.ngis-status-badge.ngis-status--green {
  background-color: #ecfdf5;
  color: #047857;
  border-color: #a7f3d0;
}

/* Color Tokens: Red */
.ngis-status-badge.ngis-status--red {
  background-color: #fef2f2;
  color: #b91c1c;
  border-color: #fecaca;
}

/* Flat variant (dense tables: icon + colored text only, no pill box) */
.ngis-status-flat {
  background: transparent;
  border: none;
  padding: 0;
}

.ngis-status-flat.ngis-status--gray { color: #64748b; }
.ngis-status-flat.ngis-status--amber { color: #d97706; }
.ngis-status-flat.ngis-status--blue { color: #2563eb; }
.ngis-status-flat.ngis-status--green { color: #059669; }
.ngis-status-flat.ngis-status--red { color: #dc2626; }

/* Micro-interaction animations */
@keyframes ngisStatusShake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-3px); }
  75% { transform: translateX(3px); }
}

.ngis-status-shake {
  animation: ngisStatusShake 0.3s ease-in-out;
}

/* Dark mode token overrides */
[data-theme="dark"] .ngis-pagination-wrapper {
  background: #0f172a;
  border-color: #1e293b;
}

[data-theme="dark"] .ngis-pag-prev {
  background: #1e293b;
  color: #cbd5e1;
  border-color: #334155;
}

[data-theme="dark"] .ngis-pag-prev:hover:not(:disabled) {
  background: #334155;
  color: #f8fafc;
}

[data-theme="dark"] .ngis-pag-number {
  color: #94a3b8;
}

[data-theme="dark"] .ngis-pag-number:hover:not(.is-active) {
  background: #1e293b;
  color: #f8fafc;
}

[data-theme="dark"] .ngis-pag-number.is-active {
  background: #13241b;
  color: #86efac;
  border-color: #1e3a29;
}

[data-theme="dark"] .ngis-status-badge.ngis-status--gray {
  background-color: #1e293b;
  color: #cbd5e1;
  border-color: #334155;
}

[data-theme="dark"] .ngis-status-badge.ngis-status--amber {
  background-color: #2a1c0d;
  color: #fcd34d;
  border-color: #452a12;
}

[data-theme="dark"] .ngis-status-badge.ngis-status--blue {
  background-color: #111e38;
  color: #93c5fd;
  border-color: #1e3a8a;
}

[data-theme="dark"] .ngis-status-badge.ngis-status--green {
  background-color: #13241b;
  color: #86efac;
  border-color: #1e3a29;
}

[data-theme="dark"] .ngis-status-badge.ngis-status--red {
  background-color: #2a1215;
  color: #fca5a5;
  border-color: #4c1d24;
}
"""

with open('assets/css/interactions.css', 'a', encoding='utf-8') as f:
    f.write(css_block)
print("Successfully appended Pagination and Status CSS to interactions.css!")
