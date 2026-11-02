with open('assets/css/portal-dashboard.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Append or ensure the gold standard overview deck rules exist in portal-dashboard.css
deck_rules = """
/* ══════════════════════════════════════════════════════════
   GOLD STANDARD 3-CARD OVERVIEW DECK (Student/Teacher/Principal/Admin)
   ══════════════════════════════════════════════════════════ */
@media (min-width: 992px) {
  .dash-overlap {
    display: grid !important;
    grid-template-columns: 240px minmax(0, 1fr) 280px !important;
    gap: 16px !important;
    max-width: 1280px !important;
    margin: -48px auto 20px !important;
    padding: 0 24px !important;
    align-items: stretch !important;
    box-sizing: border-box !important;
    position: relative !important;
    z-index: 20 !important;
  }

  .ov-profile,
  .ov-upcoming,
  .ov-deadlines {
    grid-column: auto !important;
    grid-row: 1 !important;
    height: 335px !important;
    max-height: 335px !important;
    display: flex !important;
    flex-direction: column !important;
    box-sizing: border-box !important;
  }

  .ov-profile {
    justify-content: space-between !important;
  }

  .ov-upcoming {
    padding: 14px 16px !important;
  }

  .ov-upcoming .ov-inner-grid {
    display: grid !important;
    grid-template-columns: 0.95fr 0.95fr 1.25fr !important;
    gap: 12px !important;
    flex: 1 !important;
    min-height: 0 !important;
    padding: 6px 0 0 !important;
  }

  .ov-inner-panel {
    display: flex !important;
    flex-direction: column !important;
    min-height: 0 !important;
  }

  .ov-inner-item {
    padding: 5px 0 !important;
  }
}

/* Inner panels clean & airy */
.ov-inner-panel,
.ov-deadline-panel,
.ov-panel-feed {
  background: transparent !important;
  background-color: transparent !important;
  border: none !important;
  box-shadow: none !important;
  outline: none !important;
}

/* Deadlines Panel Gold Standard */
.ov-deadline-panel {
  display: flex;
  flex-direction: column;
  margin-bottom: 8px;
  padding: 0 2px !important;
}

.ov-deadline-head {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  font-weight: 500;
  color: #000000;
  padding-bottom: 3px;
  border-bottom: none !important;
  margin-bottom: 3px;
  flex-shrink: 0;
}

.ov-deadline-head .material-symbols-outlined,
.ov-deadline-head .mi {
  font-size: 15px;
}

.ov-deadline-item {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 3px 0;
  border-bottom: none !important;
}

.ov-deadline-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}

.ov-deadline-info {
  flex: 1;
  min-width: 0;
}

.ov-deadline-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-top: 1px;
}

.ov-deadline-item-t {
  font-size: 10.5px;
  font-weight: 500;
  color: #000000;
  line-height: 1.25;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.ov-deadline-item-s {
  font-size: 9.5px;
  font-weight: 400;
  color: #555555;
  margin-top: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.ov-tag {
  display: inline-block;
  font-size: 8.5px;
  font-weight: 500;
  padding: 1px 6px;
  border-radius: 999px;
  white-space: nowrap;
  flex-shrink: 0;
  line-height: 1.2;
}

.ov-tag-urgent {
  background: #92243D !important;
  color: #ffffff !important;
}

.ov-tag-soon {
  background: #F3F3F5 !important;
  color: #202F63 !important;
  border: 1px solid #202F63 !important;
}

.ov-tag-neutral {
  background: #F3F3F5 !important;
  color: #000000 !important;
  border: 1px solid #E5E5E8 !important;
}
"""

if "GOLD STANDARD 3-CARD OVERVIEW DECK" not in css:
    css += "\n" + deck_rules
    with open('assets/css/portal-dashboard.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("Appended gold standard deck rules to portal-dashboard.css")
else:
    print("Gold standard rules already present")

