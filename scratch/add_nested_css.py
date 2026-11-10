with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    c = f.read()

target = """.nav-link.nav-sub-link.active {
  color: #ffffff !important;
  background: transparent !important;
  box-shadow: none !important;
  font-weight: 500 !important;
  text-shadow: 0 0 12px rgba(255, 255, 255, 0.65);
}"""

replacement = target + """

/* ── 2nd-Level Nested Subgroup (e.g. Academic Result, School Year Configuration, Account Management) ── */
.nav-nested-group {
  display: flex;
  flex-direction: column;
  margin: 0;
}
.nav-nested-label {
  cursor: pointer;
  user-select: none;
  width: 100%;
  border: none !important;
  background: transparent !important;
  box-shadow: none !important;
  font: inherit;
  font-family: 'Kantumruy Pro', 'Plus Jakarta Sans', sans-serif;
  color: rgba(255, 255, 255, 0.78);
  font-size: 13px;
  font-weight: 400;
  display: flex;
  align-items: center;
  padding: 6px 12px 6px 48px;
  min-height: 32px;
  text-align: left;
  transition: color 150ms ease, background 150ms ease;
}
.nav-nested-label:hover {
  color: #ffffff !important;
  background: transparent !important;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
}
.nav-nested-label .nav-link-label {
  flex: 1 1 auto;
  min-width: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.nav-nested-label .ngl-nestedchevron {
  font-size: 18px !important;
  color: rgba(255, 255, 255, 0.6) !important;
  transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  margin-left: auto;
  flex-shrink: 0;
}
.nav-nested-group.expanded > .nav-nested-label {
  color: #ffffff !important;
}
.nav-nested-group.expanded > .nav-nested-label .ngl-nestedchevron {
  transform: rotate(180deg);
  color: #ffffff !important;
}
.nav-nested-links {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 0.24s cubic-bezier(0.4, 0, 0.2, 1);
}
.nav-nested-group.expanded .nav-nested-links {
  grid-template-rows: 1fr;
}
.nav-nested-links > div {
  overflow: hidden;
  min-height: 0;
  display: flex;
  flex-direction: column;
  gap: 1px;
}
.nav-link.nav-nested-link {
  padding: 5px 12px 5px 60px !important;
  font-size: 12.5px !important;
  font-weight: 400 !important;
  color: rgba(255, 255, 255, 0.72) !important;
  border-radius: 0 !important;
  background: transparent !important;
  box-shadow: none !important;
  min-height: 28px !important;
}
.nav-link.nav-nested-link:hover {
  color: #ffffff !important;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.5) !important;
}
.nav-link.nav-nested-link.active {
  color: #ffffff !important;
  font-weight: 500 !important;
  text-shadow: 0 0 12px rgba(255, 255, 255, 0.65) !important;
}"""

if target in c:
    c = c.replace(target, replacement, 1)
    with open('assets/css/app.css', 'w', encoding='utf-8') as f:
        f.write(c)
    print('Updated assets/css/app.css with nested subgroup styling')
else:
    print('Target not found in assets/css/app.css')

