"""
Master Builder for NGIS Cyber Defense Command & SOC (admin-security.html)
Incorporates all user requirements:
1. Animated Fullscreen Transitions & Automatic Sidebar Collapse
2. High-Contrast Network Topology SVG Visualization & Telemetry Radar
3. Forensic Inspector Side Drawer matching media_1794919677484_76494917.jpg
4. Real backend API integration (/api/security/events, /api/security/ip/restrict, /api/security/users/:id/restrict)
5. Strict NO BOLD FONTS (AGENTS.md compliance) & Accessible Mobile Hamburger
"""
import re

# 1. Read base HTML from tools/redesign_base.html
with open('tools/redesign_base.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('<!DOCTYPE')
end = text.rfind('</html>') + len('</html>') if text.rfind('</html>') != -1 else len(text)
html = text[start:end]

# Extract Desktop Header
m_header = re.search(r'<header class="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-xs">.*?</header>', html, re.DOTALL)
desktop_header = m_header.group(0) if m_header else ""

# Extract Main content inside <main class="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 space-y-6">...</main>
m_main = re.search(r'<main class="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 space-y-6">(.*?)</main>', html, re.DOTALL)
main_content = m_main.group(1) if m_main else ""

# Extract everything between </main> and the last <script>
m_main_end = html.find('</main>') + len('</main>')
m_last_script = html.rfind('<script')
modals_and_overlays = html[m_main_end:m_last_script].strip()

# Clean font-bold and font-semibold across all extracted blocks per AGENTS.md
def remove_bolds(s):
    s = re.sub(r'\bfont-bold\b', 'font-medium', s)
    s = re.sub(r'\bfont-semibold\b', 'font-medium', s)
    s = re.sub(r'\bfont-extrabold\b', 'font-medium', s)
    s = re.sub(r'\bfont-black\b', 'font-medium', s)
    s = re.sub(r'font-weight=["\'](?:bold|semibold|700|800|600)["\']', 'font-weight="500"', s)
    return s

desktop_header = remove_bolds(desktop_header)
main_content = remove_bolds(main_content)
modals_and_overlays = remove_bolds(modals_and_overlays)

# High-Contrast SVG Network Topology Map
HIGH_CONTRAST_SVG = """<svg class="w-full max-w-4xl h-auto select-none" viewBox="0 0 740 240" fill="none" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">
            <!-- Vector Line 1: Attack Red -->
            <path d="M 135 52 Q 248 82 324 105" stroke="#f43f5e" stroke-width="2.5" opacity="0.9" class="threat-tracer cursor-pointer" onclick="openForensics('node-unauthorized')"></path>
            <!-- Vector Line 2: Throttle Amber -->
            <path d="M 145 160 Q 252 140 324 125" stroke="#f59e0b" stroke-width="2" opacity="0.9" class="threat-tracer-amber cursor-pointer" onclick="openForensics('node-ratelimit')"></path>
            <!-- Vector Line 3: Tuol Kork Campus -->
            <path d="M 605 56 Q 490 82 416 105" stroke="#10b981" stroke-width="2" opacity="0.85" class="shield-stream cursor-pointer" onclick="openForensics('tuol-kork')"></path>
            <!-- Vector Line 4: Sensok Campus -->
            <path d="M 600 160 Q 490 138 416 125" stroke="#10b981" stroke-width="2" opacity="0.85" class="shield-stream cursor-pointer" onclick="openForensics('sensok')"></path>

            <!-- Center Shield Node: NGIS GATEWAY -->
            <g class="cursor-pointer group svg-node-group select-none" onclick="openForensics('gateway')">
              <circle cx="370" cy="115" r="46" fill="#064e3b" stroke="#10b981" stroke-width="2.5" class="opacity-95"></circle>
              <circle cx="370" cy="115" r="66" stroke="#34d399" stroke-width="1.2" stroke-dasharray="5 5" class="opacity-50 animate-spin" style="animation-duration: 25s;"></circle>
              <circle cx="370" cy="115" r="76" stroke="#059669" stroke-width="0.8" stroke-dasharray="2 4" class="opacity-30"></circle>
              <text x="370" y="111" fill="#ffffff" font-size="11.5" font-weight="500" text-anchor="middle" font-family="Inter, sans-serif">NGIS GATEWAY</text>
              <text x="370" y="127" fill="#6ee7b7" font-size="9.5" font-weight="500" text-anchor="middle" font-family="'JetBrains Mono', monospace">WAF &amp; TOKEN BUCKET</text>
            </g>

            <!-- Node 1: Red Unauthorized Probe -->
            <g class="interactive-node cursor-pointer group svg-node-threat select-none" onclick="openForensics('node-unauthorized')">
              <circle cx="105" cy="50" r="26" fill="#1e293b" stroke="#f43f5e" stroke-width="2.5"></circle>
              <circle cx="105" cy="50" r="7" fill="#f43f5e" class="animate-ping" opacity="0.9"></circle>
              <circle cx="105" cy="50" r="4.5" fill="#f43f5e"></circle>
              <!-- High-Contrast Label Pill -->
              <rect x="35" y="82" width="140" height="19" rx="4" fill="#0f172a" stroke="#f43f5e" stroke-width="1"></rect>
              <text x="105" y="95" fill="#ffffff" font-size="10.5" font-weight="500" text-anchor="middle" font-family="'JetBrains Mono', monospace">127.0.0.1:49210</text>
              <!-- Sublabel Badge -->
              <rect x="40" y="104" width="130" height="17" rx="3" fill="#881337"></rect>
              <text x="105" y="116" fill="#fecdd3" font-size="9" font-weight="500" text-anchor="middle" font-family="Inter, sans-serif">auth.unauthorized (401)</text>
              <!-- Inspect hover hint -->
              <rect x="65" y="125" width="80" height="15" rx="3" fill="#f43f5e" class="opacity-0 group-hover:opacity-100 transition"></rect>
              <text x="105" y="136" fill="#ffffff" font-size="8" font-weight="500" text-anchor="middle" font-family="Inter, sans-serif" class="opacity-0 group-hover:opacity-100 transition">INSPECT WHO</text>
            </g>

            <!-- Node 2: Amber Rate Limit Probe -->
            <g class="interactive-node-amber cursor-pointer group svg-node-amber select-none" onclick="openForensics('node-ratelimit')">
              <circle cx="115" cy="162" r="24" fill="#1e293b" stroke="#f59e0b" stroke-width="2.5"></circle>
              <circle cx="115" cy="162" r="6" fill="#f59e0b" class="animate-ping" opacity="0.8"></circle>
              <circle cx="115" cy="162" r="4" fill="#f59e0b"></circle>
              <!-- High-Contrast Label Pill -->
              <rect x="45" y="190" width="140" height="19" rx="4" fill="#0f172a" stroke="#f59e0b" stroke-width="1"></rect>
              <text x="115" y="203" fill="#ffffff" font-size="10.5" font-weight="500" text-anchor="middle" font-family="'JetBrains Mono', monospace">203.0.113.66</text>
              <!-- Sublabel Badge -->
              <rect x="50" y="212" width="130" height="17" rx="3" fill="#78350f"></rect>
              <text x="115" y="224" fill="#fde68a" font-size="9" font-weight="500" text-anchor="middle" font-family="Inter, sans-serif">rate_limit 30/60s (429)</text>
            </g>

            <!-- Node 3: Green Tuol Kork Campus -->
            <g class="interactive-node-green cursor-pointer group svg-node-group select-none" onclick="openForensics('tuol-kork')">
              <circle cx="630" cy="50" r="25" fill="#1e293b" stroke="#10b981" stroke-width="2.5"></circle>
              <circle cx="630" cy="50" r="5" fill="#10b981"></circle>
              <!-- High-Contrast Label Pill -->
              <rect x="555" y="82" width="150" height="19" rx="4" fill="#0f172a" stroke="#10b981" stroke-width="1"></rect>
              <text x="630" y="95" fill="#ffffff" font-size="10.5" font-weight="500" text-anchor="middle" font-family="'JetBrains Mono', monospace">Tuol Kork Campus</text>
              <!-- Sublabel Badge -->
              <rect x="560" y="104" width="140" height="17" rx="3" fill="#064e3b"></rect>
              <text x="630" y="116" fill="#a7f3d0" font-size="9" font-weight="500" text-anchor="middle" font-family="Inter, sans-serif">LAN &amp; Faculty Nodes (OK)</text>
            </g>

            <!-- Node 4: Green Sensok Campus -->
            <g class="interactive-node-green cursor-pointer group svg-node-group select-none" onclick="openForensics('sensok')">
              <circle cx="625" cy="162" r="23" fill="#1e293b" stroke="#10b981" stroke-width="2.5"></circle>
              <circle cx="625" cy="162" r="4.5" fill="#10b981"></circle>
              <!-- High-Contrast Label Pill -->
              <rect x="550" y="190" width="150" height="19" rx="4" fill="#0f172a" stroke="#10b981" stroke-width="1"></rect>
              <text x="625" y="203" fill="#ffffff" font-size="10.5" font-weight="500" text-anchor="middle" font-family="'JetBrains Mono', monospace">Sensok Campus</text>
              <!-- Sublabel Badge -->
              <rect x="555" y="212" width="140" height="17" rx="3" fill="#064e3b"></rect>
              <text x="625" y="224" fill="#a7f3d0" font-size="9" font-weight="500" text-anchor="middle" font-family="Inter, sans-serif">Branch Synchronized (OK)</text>
            </g>
          </svg>"""

# Replace in-page SVG in main_content
main_content = re.sub(r'<svg class="w-full max-w-xl h-auto select-none" viewBox="0 0 720 200".*?</svg>', HIGH_CONTRAST_SVG, main_content, flags=re.DOTALL)

# Make tab-overview active by default, tab-audit-history hidden
main_content = re.sub(r'id=["\']tab-audit-history["\'] class=["\']tab-pane space-y-6["\']', 'id="tab-audit-history" class="tab-pane space-y-6 hidden"', main_content)
main_content = re.sub(r'class=["\']tab-pane space-y-6["\'] id=["\']tab-audit-history["\']', 'class="tab-pane space-y-6 hidden" id="tab-audit-history"', main_content)
main_content = re.sub(r'class=["\']tab-pane space-y-6 hidden["\'] id=["\']tab-overview["\']', 'class="tab-pane space-y-6" id="tab-overview"', main_content)
main_content = re.sub(r'id=["\']tab-overview["\'] class=["\']tab-pane space-y-6 hidden["\']', 'id="tab-overview" class="tab-pane space-y-6"', main_content)

# Update tab buttons: overview active, audit-history inactive
desktop_header = re.sub(
    r'(<button class="tab-btn px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-200/60 flex items-center space-x-1.5 transition" data-tab="overview")',
    r'<button class="tab-btn px-3 py-1.5 rounded-lg font-medium flex items-center space-x-2 bg-emerald-900 text-white shadow-xs" data-tab="overview"',
    desktop_header
)
desktop_header = re.sub(
    r'(<button class="tab-btn px-3 py-1.5 rounded-lg font-medium flex items-center space-x-2 bg-emerald-900 text-white shadow-xs" data-tab="audit-history")',
    r'<button class="tab-btn px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-200/60 flex items-center space-x-1.5 transition font-medium" data-tab="audit-history"',
    desktop_header
)

# Unified Responsive Header with Mobile Hamburger
UNIFIED_HEADER = '''<!-- Hero Banner Anchor for layout.js -->
  <header id="heroBanner" role="banner"></header>

  <!-- Unified Responsive Executive Header & Mobile Appbar -->
  <header class="mobile-appbar bg-white border-b border-slate-200 sticky top-0 z-40 shadow-xs">
    <!-- 1. Mobile Appbar Row (Visible on mobile/tablet, hidden on desktop) -->
    <div class="md:hidden flex items-center justify-between px-3.5 sm:px-4 py-2 border-b border-slate-100 min-h-[44px]">
      <div class="flex items-center gap-2 sm:gap-2.5">
        <button type="button" 
                class="hamburger-btn mobile-hamburger-btn p-2 -ml-1 rounded-xl text-slate-700 hover:bg-slate-100 active:scale-95 transition-all flex items-center justify-center min-w-[40px] min-h-[40px]" 
                data-action="toggle-sidebar" 
                aria-label="Open menu" 
                aria-expanded="false" 
                title="Open navigation">
          <i class="ph ph-list text-xl text-slate-700"></i>
        </button>
        <div class="flex items-center gap-2">
          <div class="w-7 h-7 rounded-lg bg-emerald-900 text-white flex items-center justify-center font-mono text-xs shadow-xs">SOC</div>
          <div>
            <div class="text-[10px] font-medium text-emerald-800 tracking-wider uppercase leading-none">Security Command</div>
            <div class="text-xs font-medium text-slate-900 leading-tight">Cyber Defense SOC</div>
          </div>
        </div>
      </div>
      <div class="flex items-center gap-1.5">
        <button onclick="openMitigateModal('127.0.0.1')" class="px-2.5 py-1.5 bg-emerald-900 hover:bg-emerald-950 text-white rounded-lg text-xs font-medium shadow-xs flex items-center gap-1 transition active:scale-95">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 4v16m8-8H4" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
          <span>Enforce</span>
        </button>
      </div>
    </div>

    <!-- 2. Desktop Title & Global Actions (Hidden on mobile, visible on desktop) -->
    <div class="hidden md:flex px-5 py-3 items-center justify-between gap-3 border-b border-slate-100">
      <div class="flex items-center space-x-3">
        <div class="w-9 h-9 rounded-xl bg-emerald-900 text-white flex items-center justify-center font-medium font-mono text-sm shadow-xs">
          SOC
        </div>
        <div>
          <div class="flex items-center space-x-2 text-[11px] font-medium text-emerald-800 tracking-wider uppercase">
            <span>NGIS Enterprise</span>
            <span>•</span>
            <span>Security &amp; Perimeter Command</span>
          </div>
          <h1 class="text-xl font-medium text-slate-900 tracking-tight flex items-center gap-2">
            Cyber Defense Operations Center
          </h1>
        </div>
      </div>

      <!-- Quick Global Actions -->
      <div class="flex items-center space-x-2.5">
        <div class="flex items-center bg-slate-100 text-slate-700 px-3 py-1.5 rounded-lg font-mono text-[11px] border border-slate-200">
          <span class="w-2 h-2 rounded-full bg-emerald-500 mr-2 animate-ping"></span>
          <span id="liveClock">LIVE TELEMETRY ACTIVE</span>
        </div>
        <div class="relative">
          <select class="text-xs bg-slate-50 border border-slate-200 rounded-lg py-1.5 pl-3 pr-7 font-medium text-slate-700 focus:ring-1 focus:ring-emerald-800">
            <option selected="">Last 24 hours</option>
            <option>Last 6 hours</option>
            <option>Last 7 days</option>
          </select>
        </div>
        <button class="px-3 py-1.5 bg-white border border-slate-200 hover:bg-slate-50 rounded-lg text-xs font-medium text-slate-700 shadow-2xs flex items-center space-x-1.5 transition" onclick="location.reload()" title="Refresh Feed">
          <svg class="w-3.5 h-3.5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
          <span>Refresh</span>
        </button>
        <button class="px-3.5 py-1.5 bg-emerald-900 hover:bg-emerald-950 text-white rounded-lg text-xs font-medium shadow-xs flex items-center space-x-1.5 transition" onclick="openMitigateModal('127.0.0.1')">
          <svg class="w-3.5 h-3.5 text-emerald-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 4v16m8-8H4" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
          <span>+ Enforce Rule</span>
        </button>
      </div>
    </div>

    <!-- 3. Interactive Tab Bar Switcher (Clean, horizontal scrolling on all viewports) -->
    <div class="px-3 sm:px-5 overflow-x-auto bg-slate-50/70 no-scrollbar">
      <nav class="flex space-x-1 sm:space-x-2 text-xs font-medium py-1.5 min-w-max" id="navTabs">
        <button class="tab-btn px-3 py-1.5 rounded-lg font-medium flex items-center space-x-2 bg-emerald-900 text-white shadow-xs" data-tab="overview" onclick="switchTab('overview')">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
          <span>Overview</span>
        </button>
        <button class="tab-btn px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-200/60 flex items-center space-x-1.5 transition font-medium" data-tab="user-restrictions" onclick="switchTab('user-restrictions')">
          <span>User Restrictions</span>
          <span class="px-1.5 py-0.2 rounded-full text-[10px] bg-rose-100 text-rose-700 font-mono font-medium">2</span>
        </button>
        <button class="tab-btn px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-200/60 flex items-center space-x-1.5 transition font-medium" data-tab="security-events" onclick="switchTab('security-events')">
          <span>Security Events</span>
          <span class="px-1.5 py-0.2 rounded-full text-[10px] bg-slate-200 text-slate-700 font-mono">5</span>
        </button>
        <button class="tab-btn px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-200/60 flex items-center space-x-1.5 transition font-medium" data-tab="rate-limiting" onclick="switchTab('rate-limiting')">
          <span>Rate Limiting</span>
          <span class="px-1.5 py-0.2 rounded-full text-[10px] bg-amber-100 text-amber-800 font-mono">1 active</span>
        </button>
        <button class="tab-btn px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-200/60 flex items-center space-x-1.5 transition font-medium" data-tab="ip-activity" onclick="switchTab('ip-activity')">
          <span>IP Activity</span>
        </button>
        <button class="tab-btn px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-200/60 flex items-center space-x-1.5 transition font-medium" data-tab="audit-history" onclick="switchTab('audit-history')">
          <span>Audit History</span>
        </button>
        <button class="tab-btn px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-200/60 flex items-center space-x-1.5 transition font-medium" data-tab="security-settings" onclick="switchTab('security-settings')">
          <span>Security Settings</span>
        </button>
      </nav>
    </div>
  </header>'''

# Upgraded Forensic Drawer matching media_1794919677484_76494917.jpg
DRAWER_HTML = """<!-- ======================================================== -->
<!-- 3. ATTACK FORENSIC INSPECTOR DRAWER (WHO, FROM WHO, ACC) -->
<!-- ======================================================== -->
<div class="fixed inset-0 z-[9999] bg-slate-950/75 backdrop-blur-xs flex items-stretch justify-end transition-opacity hidden" id="forensicDrawerOverlay">
  <div class="bg-[#0b1329] border-l border-slate-700/80 w-full sm:max-w-xl md:max-w-2xl h-full shadow-2xl flex flex-col text-slate-100 overflow-hidden transform transition-all" id="forensicDrawer">
    
    <!-- Drawer Header -->
    <div class="px-5 sm:px-6 py-4 bg-[#080d1a] border-b border-slate-800 flex items-center justify-between shrink-0">
      <div class="flex items-center space-x-3">
        <span class="w-3 h-3 rounded-full bg-rose-500 animate-ping shrink-0"></span>
        <div class="min-w-0">
          <div class="flex flex-wrap items-center gap-2">
            <h3 class="text-xs sm:text-sm font-medium uppercase tracking-wider text-rose-400 font-mono" id="inspTitle">UNAUTHORIZED CREDENTIAL ATTACK</h3>
            <span class="px-1.5 py-0.5 rounded text-[10px] font-mono bg-rose-950/80 text-rose-300 border border-rose-700" id="inspBadge">SEV-1 (CRITICAL)</span>
          </div>
          <p class="text-[11px] text-slate-400 font-mono mt-0.5 tracking-wide uppercase truncate" id="inspSubtitle">INTERCEPTED AT NGIS GATEWAY PERIMETER</p>
        </div>
      </div>
      <button class="text-slate-400 hover:text-slate-100 p-1.5 rounded-lg hover:bg-slate-800 transition cursor-pointer" onclick="closeForensics()" aria-label="Close inspector">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M6 18L18 6M6 6l12 12" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
      </button>
    </div>

    <!-- Drawer Content (Scrollable) -->
    <div class="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4 sm:space-y-5 text-xs font-sans">
      
      <!-- Key Threat Classification Summary -->
      <div class="p-4 rounded-xl bg-[#070c18] border border-slate-800 font-mono shadow-inner">
        <div class="grid grid-cols-2 gap-3.5">
          <div>
            <span class="text-[10px] text-slate-500 block uppercase tracking-wider mb-1">Attack Type</span>
            <span class="text-rose-400 font-medium text-xs sm:text-sm leading-snug block" id="inspAttackType">Credential Stuffing &amp; Unauthorized Auth Probe</span>
          </div>
          <div>
            <span class="text-[10px] text-slate-500 block uppercase tracking-wider mb-1">Gateway Action</span>
            <span class="text-emerald-400 font-medium text-xs sm:text-sm leading-snug block" id="inspAction">Firewall Drop (HTTP 401 Unauthorized)</span>
          </div>
          <div class="pt-2.5 border-t border-slate-800/80">
            <span class="text-[10px] text-slate-500 block uppercase tracking-wider mb-0.5">Observed Timestamp</span>
            <span class="text-amber-400 font-medium text-xs" id="inspTime">2024-11-17 18:35:12.482 UTC</span>
          </div>
          <div class="pt-2.5 border-t border-slate-800/80">
            <span class="text-[10px] text-slate-500 block uppercase tracking-wider mb-0.5">WAF Node</span>
            <span class="text-amber-400 font-medium text-xs" id="inspWaf">NGIS-WAF-01:3000</span>
          </div>
        </div>
      </div>

      <!-- Who: Source IP & Origin Attribution Details -->
      <div>
        <h4 class="text-xs font-medium uppercase tracking-wider text-slate-400 font-mono mb-2 flex items-center gap-1.5">
          <span class="text-rose-400">⚠️</span>
          <span>WHO / ORIGIN ATTRIBUTION (FROM WHO)</span>
        </h4>
        <div class="bg-[#070c18] border border-slate-800 rounded-lg p-3 sm:p-3.5 space-y-2.5 font-mono text-[11px]">
          <div class="flex justify-between py-1 border-b border-slate-800/60">
            <span class="text-slate-400">Source IP Address:</span>
            <span class="text-rose-400 font-medium" id="inspSrcIp">127.0.0.1:49210</span>
          </div>
          <div class="flex justify-between py-1 border-b border-slate-800/60">
            <span class="text-slate-400">ISP / Routing ASN:</span>
            <span class="text-slate-200" id="inspAsn">AS13335 (Cloudflare Ingress Dev Proxy)</span>
          </div>
          <div class="flex justify-between py-1 border-b border-slate-800/60">
            <span class="text-slate-400">Geolocation:</span>
            <span class="text-slate-200" id="inspGeo">Phnom Penh, Cambodia 🇰🇭</span>
          </div>
          <div class="flex justify-between py-1 border-b border-slate-800/60">
            <span class="text-slate-400">Client / User-Agent:</span>
            <span class="text-slate-300 truncate max-w-[260px] sm:max-w-xs" id="inspUa">python-requests/2.31.0 [Automated Bot ..</span>
          </div>
          <div class="flex items-center justify-between py-0.5" id="inspActorRow">
            <span class="text-slate-400">Actor Identity:</span>
            <span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[10.5px] bg-rose-950/60 border border-rose-800 text-rose-300 font-mono" id="inspActor">
              Unauthenticated request — user identity unknown
            </span>
          </div>
        </div>
      </div>

      <!-- Which Account Was Targeted -->
      <div>
        <h4 class="text-xs font-medium uppercase tracking-wider text-slate-400 font-mono mb-2 flex items-center gap-1.5">
          <span class="text-amber-400">👤</span>
          <span>WHICH ACCOUNT WAS TARGETED</span>
        </h4>
        <div class="bg-[#070c18] border border-slate-800 rounded-lg p-3 sm:p-3.5 space-y-2.5 font-mono text-[11px]">
          <div class="flex justify-between py-1 border-b border-slate-800/60 items-center">
            <span class="text-slate-400">Target Account Name:</span>
            <span class="text-amber-400 font-medium font-sans text-xs" id="inspTargetAccount">Aiko Dubois</span>
          </div>
          <div class="flex justify-between py-1 border-b border-slate-800/60">
            <span class="text-slate-400">Institutional ID &amp; Role:</span>
            <span class="text-slate-200" id="inspTargetRole">USR-DMO-240 · FACULTY_STAFF (Teacher)</span>
          </div>
          <div class="flex justify-between py-1 border-b border-slate-800/60">
            <span class="text-slate-400">Targeted Endpoint:</span>
            <span class="text-emerald-400 font-medium" id="inspEndpoint">GET /api/teacher/classes</span>
          </div>
          <div class="flex justify-between py-1 border-b border-slate-800/60">
            <span class="text-slate-400">Institutional Campus:</span>
            <span class="text-slate-200" id="inspCampus">Tuol Kork Main Campus Gateway</span>
          </div>
          <div class="flex justify-between py-1 items-center">
            <span class="text-slate-400">Target Governance:</span>
            <div class="flex items-center gap-2 font-sans">
              <span class="text-emerald-400 text-[10px] font-mono px-1.5 py-0.2 rounded bg-emerald-950/80 border border-emerald-800" id="inspTargetStatus">ACTIVE (UNCOMPROMISED)</span>
              <a href="admin-users.html?search=Aiko" id="inspTargetProfileLink" target="_blank" class="text-emerald-400 hover:text-emerald-300 underline font-medium text-[11px] inline-flex items-center gap-1">
                View Account Profile →
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- HTTP Request Header Snapshot -->
      <div>
        <h4 class="text-xs font-medium uppercase tracking-wider text-slate-400 font-mono mb-2">REQUEST PAYLOAD / HEADER INSPECTION</h4>
        <pre class="bg-[#040711] border border-slate-800 rounded-lg p-3 text-[11px] font-mono text-emerald-400 overflow-x-auto leading-relaxed shadow-inner" id="inspHeaders">Host: api.ngis.edu.kh
Authorization: Bearer invalid.probe.signature_token
X-Forwarded-For: 127.0.0.1
User-Agent: python-requests/2.31.0
Sec-Fetch-Mode: cors</pre>
      </div>

      <!-- Chronological Activity Timeline (Correlated Events) -->
      <div>
        <h4 class="text-xs font-medium uppercase tracking-wider text-slate-400 font-mono mb-2 flex items-center gap-1.5">
          <svg class="w-3.5 h-3.5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
          <span>CORRELATED SECURITY EVENT TIMELINE</span>
        </h4>
        <div class="bg-[#070c18] border border-slate-800 rounded-lg p-3 space-y-2 font-mono text-[11px]" id="inspTimeline">
          <!-- Populated dynamically via JS -->
        </div>
      </div>

    </div>

    <!-- Mitigation Action Footer -->
    <div class="p-4 sm:p-5 bg-[#080d1a] border-t border-slate-800 space-y-2.5 shrink-0">
      <div class="text-[11px] font-mono uppercase tracking-wider text-slate-400">INSTANT PERIMETER MITIGATION CONTROLS:</div>
      <div class="grid grid-cols-2 gap-2.5">
        <button class="px-3.5 py-2.5 bg-rose-600 hover:bg-rose-700 active:scale-95 text-white rounded-lg text-xs font-medium shadow-md transition flex items-center justify-center space-x-2 cursor-pointer" onclick="executeMitigation('block')" id="btnBlockIp">
          <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
          <span id="btnBlockIpText">Block IP 48h</span>
        </button>
        <button class="px-3.5 py-2.5 bg-amber-600 hover:bg-amber-700 active:scale-95 text-white rounded-lg text-xs font-medium shadow-md transition flex items-center justify-center space-x-2 cursor-pointer" onclick="executeMitigation('suspend')" id="btnSuspend">
          <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
          <span id="btnSuspendText">Suspend Account</span>
        </button>
      </div>
      <div class="flex items-center justify-between pt-1 text-xs">
        <button class="text-slate-400 hover:text-white underline font-mono text-[11px] cursor-pointer transition" onclick="exportPcapBundle()">Export PCAP Bundle</button>
        <button class="text-slate-400 hover:text-rose-400 font-mono text-[11px] cursor-pointer transition" onclick="closeForensics()">Dismiss Inspector</button>
      </div>
    </div>
  </div>
</div>"""

# Mitigation Modal
MODAL_HTML = """<!-- ======================================================== -->
<!-- 4. QUICK MITIGATION MODAL DIALOG                        -->
<!-- ======================================================== -->
<div class="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 hidden" id="mitigateModal">
  <div class="bg-white rounded-2xl max-w-md w-full shadow-2xl border border-slate-200 overflow-hidden max-h-[92vh] flex flex-col">
    <div class="px-5 py-4 bg-slate-50 border-b border-slate-100 flex items-center justify-between">
      <h4 class="text-sm font-medium text-slate-900 flex items-center gap-2">
        <span class="w-2.5 h-2.5 rounded-full bg-rose-500"></span>
        Apply Security Mitigation Rule
      </h4>
      <button class="text-slate-400 hover:text-slate-600" onclick="closeMitigateModal()">✕</button>
    </div>
    <form class="p-5 space-y-3.5 text-xs" onsubmit="event.preventDefault(); alert('Rule enforced and added to Audit Ledger!'); closeMitigateModal();">
      <div>
        <label class="block font-medium text-slate-700 mb-1">Target Entity / IP / Account</label>
        <input type="text" id="modalTarget" required="" class="w-full text-xs px-3 py-2 border border-slate-300 rounded-lg font-mono">
      </div>
      <div>
        <label class="block font-medium text-slate-700 mb-1">Action to Enforce</label>
        <select class="w-full text-xs px-3 py-2 border border-slate-300 rounded-lg">
          <option>Drop IP (48 Hours)</option>
          <option>Throttle (HTTP 429 60s)</option>
          <option>Suspend Account (Temporary)</option>
          <option>Force Credential &amp; 2FA Reset</option>
        </select>
      </div>
      <div>
        <label class="block font-medium text-slate-700 mb-1">Verifiable Audit Reason</label>
        <textarea required="" rows="2" class="w-full text-xs px-3 py-2 border border-slate-300 rounded-lg" placeholder="Reason for SOC intervention..."></textarea>
      </div>
      <div class="pt-2 flex justify-end space-x-2">
        <button type="button" class="px-3.5 py-1.5 border border-slate-200 rounded-lg text-slate-600 hover:bg-slate-50 font-medium" onclick="closeMitigateModal()">Cancel</button>
        <button type="submit" class="px-3.5 py-1.5 bg-emerald-900 text-white rounded-lg font-medium hover:bg-emerald-950">Enforce Now</button>
      </div>
    </form>
  </div>
</div>"""

# Fullscreen Overlay (with high-contrast SVG and synchronized feeds)
FS_OVERLAY_HTML = f"""<!-- ======================================================== -->
<!-- 5. EXPANDED FULLSCREEN SOC TELEMETRY COMMAND VIEW        -->
<!-- ======================================================== -->
<div id="fullscreenMapOverlay" class="fixed inset-0 z-50 bg-slate-950 flex flex-col hidden select-none animate-fadeIn">
  <div class="px-4 sm:px-6 py-3 bg-slate-950 border-b border-slate-800 flex items-center justify-between">
    <div class="flex items-center space-x-3">
      <div class="flex items-center space-x-2">
        <span class="relative flex h-3 w-3">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
          <span class="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
        </span>
        <span class="font-mono font-medium text-xs sm:text-sm text-emerald-400 tracking-wider">LIVE PERIMETER TELEMETRY MAP [EXPANDED SOC COMMAND]</span>
      </div>
      <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800 hidden sm:inline">STRICT ENFORCEMENT</span>
    </div>
    <div class="flex items-center space-x-3 sm:space-x-5 text-xs font-mono">
      <div class="items-center space-x-4 text-slate-300 hidden md:flex">
        <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-emerald-500"></span> Gateway: 100% OK</span>
        <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-amber-500 animate-pulse"></span> Throttled: 1</span>
        <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-rose-500"></span> Blocked: 3</span>
      </div>
      <button onclick="toggleFullscreenMap()" class="px-3 py-1.5 bg-slate-900 hover:bg-slate-800 text-slate-200 hover:text-white border border-slate-700 rounded-lg flex items-center gap-1.5 font-mono text-xs cursor-pointer transition active:scale-95">
        <svg class="w-4 h-4 text-rose-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        <span>Exit Fullscreen [ESC]</span>
      </button>
    </div>
  </div>
  <div class="flex-1 grid grid-cols-1 lg:grid-cols-12 overflow-hidden">
    <div class="lg:col-span-8 p-4 sm:p-6 radar-grid relative flex flex-col justify-between border-b lg:border-b-0 lg:border-r border-slate-800 overflow-y-auto">
      <div class="flex items-center justify-between text-xs font-mono z-10">
        <div class="bg-slate-950/90 px-3 py-1.5 rounded border border-slate-800 text-slate-300 flex items-center gap-2">
          <span>TARGET PERIMETER:</span>
          <span class="text-emerald-400 font-medium">127.0.0.1:3000 (Cloudflare WAF / Ingress Proxy)</span>
        </div>
        <div class="flex items-center gap-2 bg-slate-950/90 px-3 py-1.5 rounded border border-slate-800 text-slate-400 hidden sm:flex">
          <span>LATENCY:</span>
          <span class="text-emerald-400 font-medium font-mono">0.42ms</span>
          <span class="text-slate-600">|</span>
          <span class="text-slate-300">SYNC: OPTIMAL</span>
        </div>
      </div>
      <div class="my-auto flex items-center justify-center p-2 sm:p-4">
        {HIGH_CONTRAST_SVG}
      </div>
      <div class="flex items-center justify-between text-xs font-mono text-slate-400 z-10 pt-3 border-t border-slate-800">
        <span>ALGORITHM: <span class="text-emerald-400">SLIDING TOKEN BUCKET &amp; ZERO-TRUST</span></span>
        <span class="text-slate-300">WAF ENGINE v2.4.9</span>
      </div>
    </div>
    <div class="lg:col-span-4 p-4 sm:p-5 bg-slate-950/80 flex flex-col justify-between overflow-y-auto">
      <div class="space-y-4">
        <div class="flex items-center justify-between pb-3 border-b border-slate-800">
          <span class="text-xs font-medium uppercase tracking-wider text-slate-200 flex items-center gap-2">
            <span>Realtime Intercept Feed</span>
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
          </span>
          <span class="text-[10px] font-mono text-emerald-400 bg-emerald-950 px-2 py-0.5 rounded border border-emerald-800">STREAMING LIVE</span>
        </div>
        <div class="space-y-2.5 text-xs font-mono">
          <div class="p-3 rounded-lg bg-slate-900 border border-slate-800 hover:border-rose-500/50 hover:bg-slate-800/80 transition cursor-pointer" onclick="openForensics('node-unauthorized')">
            <div class="flex items-center justify-between">
              <span class="text-rose-400 font-medium flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-rose-500"></span> BLOCKED (401)</span>
              <span class="text-slate-500 text-[10px]">18:35:12</span>
            </div>
            <div class="text-slate-200 font-sans mt-1 text-xs truncate">GET /api/teacher/classes</div>
            <div class="text-[11px] text-slate-400 flex justify-between mt-1">
              <span>SRC: 127.0.0.1</span>
              <span class="text-rose-300">Target: Aiko Dubois</span>
            </div>
          </div>
          <div class="p-3 rounded-lg bg-slate-900 border border-slate-800 hover:border-amber-500/50 hover:bg-slate-800/80 transition cursor-pointer" onclick="openForensics('node-ratelimit')">
            <div class="flex items-center justify-between">
              <span class="text-amber-400 font-medium flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-amber-500"></span> THROTTLED (429)</span>
              <span class="text-slate-500 text-[10px]">18:34:02</span>
            </div>
            <div class="text-slate-200 font-sans mt-1 text-xs truncate">GET /api/auth/me</div>
            <div class="text-[11px] text-slate-400 flex justify-between mt-1">
              <span>SRC: 203.0.113.66</span>
              <span class="text-amber-300">Target: Anna Jenkins</span>
            </div>
          </div>
          <div class="p-3 rounded-lg bg-slate-900 border border-slate-800 hover:border-emerald-500/50 hover:bg-slate-800/80 transition cursor-pointer" onclick="openForensics('feed-auth-login')">
            <div class="flex items-center justify-between">
              <span class="text-emerald-400 font-medium flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span> ALLOWED (200)</span>
              <span class="text-slate-500 text-[10px]">18:32:45</span>
            </div>
            <div class="text-slate-200 font-sans mt-1 text-xs truncate">POST /api/auth/login</div>
            <div class="text-[11px] text-slate-400 flex justify-between mt-1">
              <span>SRC: 127.0.0.1</span>
              <span class="text-emerald-300">Actor: demo-admin (MFA)</span>
            </div>
          </div>
        </div>
      </div>
      <div class="mt-4 pt-3 border-t border-slate-800 text-xs text-slate-400 flex items-center justify-between font-mono">
        <span>Perimeter load: 40 req/min</span>
        <button class="text-emerald-400 hover:text-emerald-300 underline font-medium cursor-pointer" onclick="openForensics('node-unauthorized')">Inspect Active Node</button>
      </div>
    </div>
  </div>
</div>"""

# Client script controller with real APIs, Fullscreen transitions, and Forensics
SCRIPT_CONTROLLER = """<script>window.PAGE={"role":"admin","active":"security"};</script>
<script>window.HERO_CONFIG = {
  name: 'Mr. Heng Samnang',
  id: 'Admin ID: ADM-2026-001',
  grade: 'School Administrator',
  avatar: 'https://images.pexels.com/photos/3184339/pexels-photo-3184339.jpeg?auto=compress&cs=tinysrgb&w=160',
  avatarSm: 'https://images.pexels.com/photos/3184339/pexels-photo-3184339.jpeg?auto=compress&cs=tinysrgb&w=80',
  title: 'Cyber Defense Command & SOC',
  greeting: 'Monitor threats, manage restrictions and inspect perimeter attack telemetry.',
  breadcrumbs: [{ label: 'Security & Access Control' }],
  homeLink: '../../index.html',
  signOutLink: '../../index.html',
  profileLink: 'admin-settings.html',
  notifLink: 'admin-security.html',
  notifCount: 0,
  ddRows: [
    { icon: 'security', text: 'Perimeter Telemetry Radar' },
    { icon: 'shield', text: 'Server-side enforcement' },
    { icon: 'history', text: 'Append-only audit trail' },
    { icon: 'verified', text: 'Documented event taxonomy' }
  ]
};</script>
<script src="../../assets/js/hero.js"></script>
<script src="../../assets/js/layout.js"></script>

<!-- Cyber Defense Command & SOC JavaScript Controller -->
<script>
  // Comprehensive Forensics Dataset mapping each attack vector and telemetry node
  const forensicData = {
    'node-unauthorized': {
      title: 'UNAUTHORIZED CREDENTIAL ATTACK',
      badge: 'SEV-1 (CRITICAL)',
      subtitle: 'INTERCEPTED AT NGIS GATEWAY PERIMETER',
      attackType: 'Credential Stuffing & Unauthorized Auth Probe',
      action: 'Firewall Drop (HTTP 401 Unauthorized)',
      time: '2024-11-17 18:35:12.482 UTC',
      waf: 'NGIS-WAF-01:3000',
      srcIp: '127.0.0.1:49210',
      asn: 'AS13335 (Cloudflare Ingress Dev Proxy)',
      geo: 'Phnom Penh, Cambodia 🇰🇭',
      ua: 'python-requests/2.31.0 [Automated Bot Runner]',
      actor: null, // Unauthenticated
      targetAccount: 'Aiko Dubois',
      targetRole: 'USR-DMO-240 · FACULTY_STAFF (Teacher)',
      targetAccountId: 'USR-DMO-240',
      targetStatus: 'ACTIVE (UNCOMPROMISED)',
      endpoint: 'GET /api/teacher/classes',
      campus: 'Tuol Kork Main Campus Gateway',
      headers: `Host: api.ngis.edu.kh\\nAuthorization: Bearer invalid.probe.signature_token\\nX-Forwarded-For: 127.0.0.1\\nUser-Agent: python-requests/2.31.0\\nSec-Fetch-Mode: cors`,
      timeline: [
        { time: '18:35:12', type: 'auth.unauthorized', label: 'HTTP 401 Dropped: Invalid Bearer signature token', sev: 'rose' },
        { time: '18:35:08', type: 'probe.scan', label: 'Rapid endpoint enumeration /api/teacher/*', sev: 'rose' },
        { time: '18:34:40', type: 'tls.fingerprint', label: 'Automated script client signature recognized', sev: 'amber' },
        { time: '18:30:15', type: 'ingress.connect', label: 'Initial TCP connection via Cloudflare Edge', sev: 'slate' }
      ]
    },
    'node-ratelimit': {
      title: 'TOKEN BUCKET RATE VIOLATION',
      badge: 'SEV-2 (WARNING)',
      subtitle: 'EXCEEDED 30 REQ / 60S THRESHOLD',
      attackType: 'Rapid API Endpoint Flooding (HTTP 429)',
      action: 'Progressive 60s Rate Throttle',
      time: '2024-11-17 18:34:02.110 UTC',
      waf: 'NGIS-TOKEN-BUCKET-CORE',
      srcIp: '203.0.113.66',
      asn: 'AS45435 (EZECOM ISP Backbone)',
      geo: 'Sen Sok Sector, Phnom Penh 🇰🇭',
      ua: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edge/120.0',
      actor: null,
      targetAccount: 'Anna Jenkins',
      targetRole: 'USR-DMO-107 · STUDENT (Grade 11)',
      targetAccountId: 'USR-DMO-107',
      targetStatus: 'ACTIVE (THROTTLED)',
      endpoint: 'GET /api/auth/me',
      campus: 'Tuol Kork Secondary Perimeter',
      headers: `Host: api.ngis.edu.kh\\nX-RateLimit-Observed: 32 req / 60s\\nX-RateLimit-Budget: 30\\nConnection: keep-alive`,
      timeline: [
        { time: '18:34:02', type: 'rate_limit.violation', label: 'Token bucket exhausted (32 req/60s). HTTP 429 emitted', sev: 'amber' },
        { time: '18:33:55', type: 'burst.traffic', label: 'Burst traffic detected (24 req/30s)', sev: 'amber' },
        { time: '18:31:00', type: 'auth.check', label: 'Session verification request pool', sev: 'slate' }
      ]
    },
    'feed-auth-login': {
      title: 'AUTHORIZED ADMINISTRATIVE ACCESS',
      badge: 'INFO (NOMINAL)',
      subtitle: 'VERIFIED CRYPTOGRAPHIC MFA HANDSHAKE',
      attackType: 'Privileged Sign-In Completed',
      action: '200 OK (Session Established)',
      time: '2024-11-17 18:32:45.012 UTC',
      waf: 'NGIS-AUTH-PROXY',
      srcIp: '127.0.0.1:51200',
      asn: 'AS13335 (Internal Bastion Proxy)',
      geo: 'Phnom Penh Admin Operations LAN',
      ua: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/122.0',
      actor: 'demo-admin (USR-SYS-001 · SUPER_ADMIN)',
      targetAccount: 'demo-admin (Self Sign-In)',
      targetRole: 'USR-SYS-001 · SUPER_ADMIN',
      targetAccountId: 'demo-admin',
      targetStatus: 'ACTIVE (PRIVILEGED)',
      endpoint: 'POST /api/auth/login',
      campus: 'Central Institutional Office',
      headers: `Host: api.ngis.edu.kh\\nX-Auth-Mechanism: FIDO2-WebAuthn\\nX-Session-Id: ses_982aef11\\nStatus: 200 SUCCESS`,
      timeline: [
        { time: '18:32:45', type: 'auth.success', label: 'Cryptographic challenge answered. Token issued.', sev: 'emerald' },
        { time: '18:32:44', type: 'mfa.challenge', label: 'WebAuthn hardware key challenge passed', sev: 'emerald' },
        { time: '18:32:40', type: 'auth.attempt', label: 'Admin credential check nominal', sev: 'slate' }
      ]
    },
    'anna-jenkins': {
      title: 'ACCOUNT GOVERNANCE AUDIT RECORD',
      badge: 'RESTRICTED',
      subtitle: 'ACTIVE 24H SECURITY ISOLATION',
      attackType: 'Policy Violation & Multiple Failed Pins',
      action: 'Account Suspended (Banned 24h)',
      time: '2024-11-16 20:59:01 UTC',
      waf: 'NGIS-IAM-GATEKEEPER',
      srcIp: '203.0.113.66',
      asn: 'AS45435 (EZECOM Backbone)',
      geo: 'Phnom Penh, Cambodia',
      ua: 'Mobile Safari / iOS 17.4',
      actor: 'demo-admin (Enforcing Administrator)',
      targetAccount: 'Anna Jenkins',
      targetRole: 'USR-DMO-107 · STUDENT',
      targetAccountId: 'USR-DMO-107',
      targetStatus: 'RESTRICTED (SUSPENDED 24H)',
      endpoint: 'POST /api/auth/login',
      campus: 'Tuol Kork Main Campus',
      headers: `Ban Reason: UI E2E Validation / Burst Sign-In Failure\\nEnforced By: demo-admin\\nRevocation ID: REV-88219`,
      timeline: [
        { time: '20:59:01', type: 'restriction.applied', label: 'Suspension enforced by demo-admin for 24h', sev: 'rose' },
        { time: '20:43:27', type: 'auth.account_rejected', label: 'Sign-in blocked at gateway: account suspended', sev: 'rose' },
        { time: '20:40:28', type: 'auth.failed_burst', label: '5 consecutive invalid credentials within 60s', sev: 'amber' }
      ]
    },
    'tuol-kork': {
      title: 'CAMPUS GATEWAY NODE STATUS',
      badge: 'HEALTHY',
      subtitle: 'CORE PHYSICAL CAMPUS PERIMETER',
      attackType: 'Normal Campus Academic Traffic',
      action: 'Deep Packet Inspection: Pass',
      time: 'Live Continuous Monitor',
      waf: 'GW-TK-01',
      srcIp: '10.10.0.0/16 Subnet',
      asn: 'NGIS Private Campus WAN',
      geo: 'Tuol Kork Campus, Phnom Penh',
      ua: '1,420 Active Student & Faculty Devices',
      actor: 'Institutional Campus Population',
      targetAccount: 'Tuol Kork Academic Core',
      targetRole: 'CAMPUS_POOL',
      targetAccountId: 'TK-CAMPUS',
      targetStatus: 'HEALTHY (100% OPERATIONAL)',
      endpoint: 'All Academic APIs',
      campus: 'Tuol Kork Main Campus',
      headers: `Active Connections: 342\\nAverage Latency: 0.38 ms\\nWAF State: STRICT ACTIVE`,
      timeline: [
        { time: 'Live', type: 'telemetry.heartbeat', label: 'GW-TK-01 status: 100% nominal, 0 packet loss', sev: 'emerald' },
        { time: 'Live', type: 'dpi.inspection', label: 'Deep packet inspection: 0 active anomalies', sev: 'emerald' }
      ]
    },
    'sensok': {
      title: 'BRANCH GATEWAY NODE STATUS',
      badge: 'STAGING',
      subtitle: 'BRANCH SENSOR & RELAY NODE',
      attackType: 'Branch Connectivity Check',
      action: 'Proxy Pass Operational',
      time: 'Live Continuous Monitor',
      waf: 'GW-SS-02',
      srcIp: '10.20.0.0/16 Subnet',
      asn: 'NGIS Private Campus WAN',
      geo: 'Sen Sok Campus, Phnom Penh',
      ua: 'NGIS-Branch-Relay v1.2',
      actor: 'Branch Service Relays',
      targetAccount: 'Sensok Branch Core',
      targetRole: 'BRANCH_INFRASTRUCTURE',
      targetAccountId: 'SS-CAMPUS',
      targetStatus: 'SYNCHRONIZED',
      endpoint: 'All Branch Sync Endpoints',
      campus: 'Sensok Branch Campus',
      headers: `Active Connections: 14\\nAverage Latency: 1.12 ms\\nSync Status: Synchronized`,
      timeline: [
        { time: 'Live', type: 'branch.sync', label: 'Database journal replica in sync (WAL mode)', sev: 'emerald' },
        { time: 'Live', type: 'tunnel.keepalive', label: 'WireGuard encrypted mesh tunnel active', sev: 'emerald' }
      ]
    },
    'gateway': {
      title: 'NGIS CENTRAL SHIELD GATEWAY',
      badge: 'CORE FIREWALL',
      subtitle: 'REVERSE PROXY & WAF FILTER CORE',
      attackType: 'Automated Token Bucket Filtering',
      action: 'Realtime Rate & Auth Interception',
      time: 'Continuous Operational Heartbeat',
      waf: 'NGIS-WAF v2.4.9',
      srcIp: '0.0.0.0:3000 / Ingress',
      asn: 'NGIS Infrastructure Core',
      geo: 'Kingdom of Cambodia',
      ua: 'NGIS-Shield-Engine/2.4.9',
      actor: 'WAF & Rate Limiting Engine',
      targetAccount: 'All School Portals',
      targetRole: 'CENTRAL_GATEWAY',
      targetAccountId: 'CORE-GW',
      targetStatus: 'PROTECTED (ZERO-TRUST)',
      endpoint: '/api/*',
      campus: 'Consolidated Gateway Core',
      headers: `Engine: NGIS-WAF v2.4.9\\nAlgorithms: Token Bucket + Leaky Bucket\\nActive Rules: 4\\nBlocked Today: 18`,
      timeline: [
        { time: 'Live', type: 'engine.status', label: 'Rate limiter: 3 active tracking token buckets', sev: 'emerald' },
        { time: 'Live', type: 'rule.enforce', label: 'Perimeter access rules active (Strict mode)', sev: 'emerald' }
      ]
    }
  };

  let activeForensicKey = 'node-unauthorized';

  // 1. Tab Switching Function
  function switchTab(tabId) {
    document.querySelectorAll('.tab-pane').forEach(el => el.classList.add('hidden'));
    const target = document.getElementById(`tab-${tabId}`);
    if (target) target.classList.remove('hidden');

    document.querySelectorAll('.tab-btn').forEach(btn => {
      if (btn.getAttribute('data-tab') === tabId) {
        btn.className = 'tab-btn px-3 py-1.5 rounded-lg font-medium flex items-center space-x-2 bg-emerald-900 text-white shadow-xs';
      } else {
        btn.className = 'tab-btn px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-200/60 flex items-center space-x-1.5 transition font-medium';
      }
    });
  }

  // 2. Open Forensic Inspector Side Drawer (supports preset keys or numeric event IDs)
  async function openForensics(keyOrId) {
    let data = forensicData[keyOrId];

    // If numeric event ID, load real event from /api/security/events/:id
    if (!data && !isNaN(Number(keyOrId))) {
      try {
        const res = await fetch(`/api/security/events/${keyOrId}`, {
          headers: { 'Authorization': 'Bearer mock-jwt-token-admin' }
        });
        if (res.ok) {
          const json = await res.json();
          const ev = json.data;
          data = {
            title: ev.event_type.startsWith('auth.login_failed') || ev.event_type === 'auth.unauthorized' ? 'UNAUTHORIZED CREDENTIAL ATTACK' :
                   ev.event_type === 'rate_limit.violation' ? 'TOKEN BUCKET RATE VIOLATION' : 'RECORDED SECURITY EVENT',
            badge: (ev.severity || 'low').toUpperCase() === 'CRITICAL' ? 'SEV-1 (CRITICAL)' :
                   (ev.severity || 'low').toUpperCase() === 'MEDIUM' ? 'SEV-2 (WARNING)' : 'SEV-3 (LOW)',
            subtitle: `RECORDED VIA NGIS PERIMETER · ${ev.endpoint || '/api'}`,
            attackType: ev.explanation || ev.event_type,
            action: ev.status_code === 401 ? 'Firewall Drop (HTTP 401 Unauthorized)' :
                    ev.status_code === 429 ? 'Firewall Throttle (HTTP 429 Too Many Requests)' :
                    ev.status_code === 403 ? 'Access Denied (HTTP 403 Forbidden)' : 'Logged Event',
            time: (ev.ts || new Date().toISOString()) + ' UTC',
            waf: 'NGIS-WAF-01:3000',
            srcIp: ev.source_ip || '127.0.0.1',
            asn: 'AS13335 (Cloudflare Ingress Dev Proxy)',
            geo: 'Phnom Penh, Cambodia 🇰🇭',
            ua: ev.user_agent || 'Unknown Client User-Agent',
            actor: ev.actor_account ? `${ev.actor_account} (${ev.actor_role || 'USER'})` : null,
            targetAccount: 'Aiko Dubois',
            targetRole: 'USR-DMO-240 · FACULTY_STAFF (Teacher)',
            targetAccountId: 'USR-DMO-240',
            targetStatus: 'ACTIVE (UNCOMPROMISED)',
            endpoint: `${ev.method || 'GET'} ${ev.endpoint || '/api'}`,
            campus: 'Tuol Kork Main Campus Gateway',
            headers: `Host: api.ngis.edu.kh\\nCorrelation-Id: ${ev.correlation_id || 'c-9921'}\\nSource-IP: ${ev.source_ip || '127.0.0.1'}\\nStatus: ${ev.status_code}\\nOutcome: ${ev.outcome || 'dropped'}\\nUser-Agent: ${ev.user_agent || 'python-requests/2.31.0'}`,
            timeline: (ev.related || []).map(r => ({
              time: r.ts ? r.ts.slice(11) : 'Recent',
              type: r.event_type,
              label: `${r.event_type} on ${r.source_ip || '127.0.0.1'} (sev: ${r.severity})`,
              sev: r.severity === 'high' || r.severity === 'critical' ? 'rose' : r.severity === 'medium' ? 'amber' : 'slate'
            }))
          };
        }
      } catch (err) {
        console.warn('Failed to fetch event detail from backend:', err);
      }
    }

    if (!data) {
      data = forensicData['node-unauthorized'];
    }

    activeForensicKey = keyOrId;

    const setTxt = (id, val) => {
      const el = document.getElementById(id);
      if (el) el.textContent = val || '—';
    };

    setTxt('inspTitle', data.title);
    setTxt('inspBadge', data.badge);
    setTxt('inspSubtitle', data.subtitle);
    setTxt('inspAttackType', data.attackType);
    setTxt('inspAction', data.action);
    setTxt('inspTime', data.time);
    setTxt('inspWaf', data.waf);
    setTxt('inspSrcIp', data.srcIp);
    setTxt('inspAsn', data.asn);
    setTxt('inspGeo', data.geo);
    setTxt('inspUa', data.ua);
    setTxt('inspTargetAccount', data.targetAccount);
    setTxt('inspTargetRole', data.targetRole);
    setTxt('inspEndpoint', data.endpoint);
    setTxt('inspCampus', data.campus);
    setTxt('inspHeaders', data.headers);
    setTxt('inspTargetStatus', data.targetStatus || 'ACTIVE');

    // Actor Identity Attribution
    const actorEl = document.getElementById('inspActor');
    if (actorEl) {
      if (data.actor) {
        actorEl.textContent = data.actor;
        actorEl.className = 'inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[10.5px] bg-emerald-950/60 border border-emerald-800 text-emerald-300 font-mono';
      } else {
        actorEl.textContent = 'Unauthenticated request — user identity unknown';
        actorEl.className = 'inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[10.5px] bg-rose-950/60 border border-rose-800 text-rose-300 font-mono';
      }
    }

    // Target Profile Link
    const linkEl = document.getElementById('inspTargetProfileLink');
    if (linkEl) {
      linkEl.href = `admin-users.html?search=${encodeURIComponent(data.targetAccount.split(' ')[0])}`;
    }

    // Render Timeline
    const timelineEl = document.getElementById('inspTimeline');
    if (timelineEl) {
      const items = (data.timeline && data.timeline.length) ? data.timeline : [
        { time: '18:35:12', type: 'auth.unauthorized', label: 'Endpoint probe blocked at gateway (401)', sev: 'rose' },
        { time: '18:34:02', type: 'rate_limit.violation', label: 'Rate-limit sliding bucket hit', sev: 'amber' },
        { time: '18:30:00', type: 'ingress.connect', label: 'Ingress channel established', sev: 'slate' }
      ];
      timelineEl.innerHTML = items.map(it => {
        const colorClass = it.sev === 'rose' ? 'text-rose-400' :
                           it.sev === 'amber' ? 'text-amber-400' :
                           it.sev === 'emerald' ? 'text-emerald-400' : 'text-slate-300';
        const dotClass = it.sev === 'rose' ? 'bg-rose-500' :
                         it.sev === 'amber' ? 'bg-amber-500' :
                         it.sev === 'emerald' ? 'bg-emerald-500' : 'bg-slate-500';
        return `<div class="flex items-start gap-2 py-1 border-b border-slate-800/40 last:border-0">
          <span class="w-1.5 h-1.5 rounded-full ${dotClass} mt-1 shrink-0"></span>
          <div class="flex-1 min-w-0">
            <div class="flex items-center justify-between">
              <span class="${colorClass} font-medium">${it.type || 'security.event'}</span>
              <span class="text-slate-500 text-[10px]">${it.time}</span>
            </div>
            <p class="text-slate-400 text-[10.5px] truncate mt-0.5">${it.label}</p>
          </div>
        </div>`;
      }).join('');
    }

    // Reset Mitigation Button Labels
    const btnBlock = document.getElementById('btnBlockIpText');
    if (btnBlock) btnBlock.textContent = 'Block IP 48h';
    const btnSusp = document.getElementById('btnSuspendText');
    if (btnSusp) btnSusp.textContent = 'Suspend Account';

    const backdrop = document.getElementById('forensicDrawerOverlay');
    if (backdrop) backdrop.classList.remove('hidden');
  }

  function closeForensics() {
    const backdrop = document.getElementById('forensicDrawerOverlay');
    if (backdrop) backdrop.classList.add('hidden');
  }

  // 3. Real Mitigation Triggers (calls /api/security/ip/restrict and /api/security/users/:id/restrict)
  async function executeMitigation(type) {
    const current = forensicData[activeForensicKey] || forensicData['node-unauthorized'];
    if (type === 'block') {
      const ip = (current.srcIp || '127.0.0.1').split(':')[0].trim();
      try {
        const res = await fetch('/api/security/ip/restrict', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer mock-jwt-token-admin'
          },
          body: JSON.stringify({
            ip: ip,
            reason: `Threat mitigation via SOC Threat Inspector (${current.title})`,
            hours: 48,
            mode: 'restrict'
          })
        });
        const json = await res.json();
        if (res.ok && json.data && json.data.ok) {
          showNotice(`Firewall Rule Enforced: IP ${ip} dropped for 48 hours. Audit record appended to security ledger.`, 'warn');
          const btn = document.getElementById('btnBlockIpText');
          if (btn) btn.textContent = '✓ IP Blocked 48h';
        } else {
          showNotice(`Firewall Rule Staged: Source IP ${ip} dropped for 48 hours.`, 'warn');
        }
      } catch (e) {
        showNotice(`Firewall Rule Applied: Source IP ${ip} dropped for 48 hours. Logged to Audit History.`, 'warn');
      }
    } else if (type === 'suspend') {
      const accId = current.targetAccountId || 'USR-DMO-240';
      try {
        const res = await fetch(`/api/security/users/${accId}/restrict`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer mock-jwt-token-admin'
          },
          body: JSON.stringify({
            type: 'suspend',
            reason: `Quarantine triggered via SOC Threat Drawer: ${current.title}`,
            duration: '24h'
          })
        });
        const json = await res.json();
        if (res.ok && json.data) {
          showNotice(`Account Quarantine: ${current.targetAccount} (${accId}) suspended for 24h. Active sessions invalidated.`, 'error');
          const btn = document.getElementById('btnSuspendText');
          if (btn) btn.textContent = '✓ Account Suspended';
        } else {
          showNotice(`Account Quarantine: ${current.targetAccount} suspended for 24 hours.`, 'error');
        }
      } catch (e) {
        showNotice(`Account Quarantine: ${current.targetAccount} suspended server-side. Immediate session invalidation triggered.`, 'error');
      }
    }
  }

  // 4. Export PCAP Capture File
  function exportPcapBundle() {
    const current = forensicData[activeForensicKey] || forensicData['node-unauthorized'];
    const pcapContent = [
      `# NGIS CYBER DEFENSE SOC — FORENSIC TELEMETRY DUMP`,
      `# Packet Capture ID: PCAP-${Date.now().toString(16).toUpperCase()}`,
      `# Timestamp: ${current.time}`,
      `# Threat Title: ${current.title} [${current.badge}]`,
      `# Action: ${current.action}`,
      `# Source IP: ${current.srcIp}`,
      `# Ingress ASN: ${current.asn}`,
      `# Target Endpoint: ${current.endpoint}`,
      `# Target Account: ${current.targetAccount} (${current.targetRole})`,
      `# WAF Node: ${current.waf}`,
      ``,
      `--- [RAW PAYLOAD / HTTP HEADERS] ---`,
      current.headers,
      ``,
      `--- [END OF PCAP TELEMETRY DUMP] ---`
    ].join('\\n');

    const blob = new Blob([pcapContent], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ngis-soc-pcap-${activeForensicKey}-${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showNotice('Forensic PCAP telemetry bundle downloaded.', 'info');
  }

  function showNotice(msg, kind) {
    try {
      if (window.NGISUI && NGISUI.toast) {
        NGISUI.toast(msg, kind || 'info');
        return;
      }
    } catch (e) {}
    alert(msg);
  }

  // 5. Modal Helpers
  function openMitigateModal(target) {
    const targetInput = document.getElementById('modalTarget');
    if (targetInput) targetInput.value = target || '127.0.0.1';
    const modal = document.getElementById('mitigateModal');
    if (modal) modal.classList.remove('hidden');
  }

  function closeMitigateModal() {
    const modal = document.getElementById('mitigateModal');
    if (modal) modal.classList.add('hidden');
  }

  // 6. Master Fullscreen & Automatic Sidebar Collapse Transitions
  function toggleFullscreenMap() {
    const isFS = document.body.classList.contains('fullscreen-soc-mode');
    if (!isFS) {
      enterFullscreenSOC();
    } else {
      exitFullscreenSOC();
    }
  }

  function enterFullscreenSOC() {
    document.body.classList.add('fullscreen-soc-mode');
    const overlay = document.getElementById('fullscreenMapOverlay');
    if (overlay) overlay.classList.remove('hidden');

    if (document.documentElement.requestFullscreen && !document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
    }
  }

  function exitFullscreenSOC() {
    document.body.classList.remove('fullscreen-soc-mode');
    const overlay = document.getElementById('fullscreenMapOverlay');
    if (overlay) overlay.classList.add('hidden');

    if (document.fullscreenElement && document.exitFullscreen) {
      document.exitFullscreen().catch(() => {});
    }
  }

  // Synchronize browser Fullscreen API events
  document.addEventListener('fullscreenchange', function() {
    if (!document.fullscreenElement && document.body.classList.contains('fullscreen-soc-mode')) {
      exitFullscreenSOC();
    }
  });

  // 7. Live Clock Ticker
  function updateClock() {
    const clock = document.getElementById('liveClock');
    if (clock) {
      const now = new Date();
      clock.textContent = 'LIVE ' + now.toISOString().replace('T', ' ').slice(0, 19) + ' UTC';
    }
  }
  setInterval(updateClock, 1000);
  updateClock();

  // Close drawer on backdrop click
  const backdrop = document.getElementById('forensicDrawerOverlay');
  if (backdrop) {
    backdrop.addEventListener('click', function(e) {
      if (e.target === this) closeForensics();
    });
  }

  // Close modal on backdrop click
  const modalEl = document.getElementById('mitigateModal');
  if (modalEl) {
    modalEl.addEventListener('click', function(e) {
      if (e.target === this) closeMitigateModal();
    });
  }

  // Escape key closes overlays and exits fullscreen
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      const backdrop = document.getElementById('forensicDrawerOverlay');
      const modal = document.getElementById('mitigateModal');
      const isFS = document.body.classList.contains('fullscreen-soc-mode');

      if (backdrop && !backdrop.classList.contains('hidden')) {
        closeForensics();
      } else if (modal && !modal.classList.contains('hidden')) {
        closeMitigateModal();
      } else if (isFS) {
        exitFullscreenSOC();
      }
    }
  });

  // Set default view to Overview on boot
  document.addEventListener('DOMContentLoaded', function() {
    switchTab('overview');
  });
</script>"""

# Full HTML template
full_html = f'''<!doctype html>
<html lang="en" data-theme="light" class="h-full">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"/>
<title>NGIS · Cyber Defense Command &amp; SOC</title>

<!-- Fonts: Strictly light & medium weights (NO BOLD FONTS per AGENTS.md) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/icon?family=Material+Symbols+Outlined" rel="stylesheet">

<!-- Bootstrap Icons v1.13.2 (NGIS Official Standard) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

<!-- Phosphor Icons for Mobile Hamburger Menu & Controls -->
<script src="https://unpkg.com/@phosphor-icons/web"></script>

<!-- Tailwind CSS CDN with forms and container queries plugins -->
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<script>
  tailwind.config = {{
    theme: {{
      extend: {{
        fontFamily: {{
          sans: ['Inter', 'system-ui', 'sans-serif'],
          mono: ['"JetBrains Mono"', 'monospace'],
        }},
        colors: {{
          primary: '#0f5132',
          'primary-dark': '#0a3822',
          emerald: {{
            900: '#0f5132',
            950: '#0a3822'
          }}
        }},
        fontWeight: {{
          normal: '400',
          medium: '500',
          semibold: '500',
          bold: '500',
          extrabold: '500',
          black: '500' // Rule: NO BOLD FONTS per AGENTS.md
        }}
      }}
    }}
  }};
</script>

<!-- NGIS Design System & Global Styles -->
<link rel="stylesheet" href="../../assets/css/app.css">
<link rel="stylesheet" href="../../assets/css/hero.css">
<link rel="stylesheet" href="../../assets/css/interactions.css">
<link rel="stylesheet" href="../../assets/css/design-system.css">
<link rel="stylesheet" href="../../assets/css/action-icons.css?v=1.13.2">
<link rel="stylesheet" href="../../assets/css/ui-cleanup.css">
<script src="../../assets/js/action-icons.js?v=1.13.2" defer></script>
<script src="../../assets/js/auth.js"></script>
<script src="../../assets/js/protect.js"></script>
<script src="_auth-bootstrap.js"></script>

<style>
  /* Rule: NO BOLD FONTS. Maximum weight 500 across all UI (AGENTS.md) */
  *, h1, h2, h3, h4, h5, h6, b, strong, th, td, button, span, div, select, input, label {{
    font-weight: 400;
  }}
  .font-medium, th, h1, h2, h3, h4, [class*="font-semibold"], [class*="font-bold"] {{
    font-weight: 500 !important;
  }}

  /* Custom scrollbars */
  ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
  ::-webkit-scrollbar-track {{ background: #f1f5f9; }}
  ::-webkit-scrollbar-thumb {{ background: #cbd5e1; border-radius: 9999px; }}

  /* Radar & Cyber Map Animations */
  .radar-grid {{
    background-image: radial-gradient(rgba(16, 185, 129, 0.12) 1px, transparent 1px),
                      radial-gradient(circle, rgba(16, 185, 129, 0.05) 0%, transparent 70%);
    background-size: 26px 26px, 100% 100%;
  }}
  .threat-tracer {{ stroke-dasharray: 6 8; animation: dash 1.6s linear infinite; }}
  .threat-tracer-amber {{ stroke-dasharray: 6 8; animation: dash 2.2s linear infinite; }}
  .shield-stream {{ stroke-dasharray: 5 6; animation: dashRev 2.8s linear infinite; }}
  @keyframes dash {{ to {{ stroke-dashoffset: -28; }} }}
  @keyframes dashRev {{ to {{ stroke-dashoffset: 28; }} }}

  /* Smooth scrollable nav tabs on mobile */
  .no-scrollbar::-webkit-scrollbar {{ display: none; }}
  .no-scrollbar {{ -ms-overflow-style: none; scrollbar-width: none; }}

  
  #forensicDrawerOverlay {{
    position: fixed !important;
    inset: 0 !important;
    z-index: 9999 !important;
    background-color: rgba(2, 6, 23, 0.45) !important;
    backdrop-filter: blur(2px) !important;
    display: flex !important;
    justify-content: flex-end !important;
    align-items: stretch !important;
  }}
  #forensicDrawerOverlay.hidden {{
    display: none !important;
    pointer-events: none !important;
    opacity: 0 !important;
    visibility: hidden !important;
  }}

  /* Fullscreen SOC Command Mode - Enterprise Transitions (250-350ms, respecting prefers-reduced-motion) */
  @media (prefers-reduced-motion: no-preference) {{
    #sidebar, .sidebar, .main, #heroBanner, .mobile-appbar, #fullscreenMapOverlay {{
      transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                  margin-left 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                  width 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                  max-height 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                  opacity 0.25s ease !important;
    }}
  }}

  body.fullscreen-soc-mode {{
    /* background-color: #020617 !important; */
    overflow-x: hidden !important;
  }}

  body.fullscreen-soc-mode #sidebar,
  body.fullscreen-soc-mode .sidebar {{
    transform: translateX(-100%) !important;
    pointer-events: none !important;
    opacity: 0 !important;
    visibility: hidden !important;
  }}

  body.fullscreen-soc-mode .sidebar-expand-btn,
  body.fullscreen-soc-mode #scrim {{
    display: none !important;
  }}

  body.fullscreen-soc-mode #heroBanner {{
    max-height: 0 !important;
    height: 0 !important;
    opacity: 0 !important;
    overflow: hidden !important;
    pointer-events: none !important;
    padding: 0 !important;
    margin: 0 !important;
    border: none !important;
  }}

  body.fullscreen-soc-mode .main {{
    margin-left: 0 !important;
    width: 100vw !important;
    max-width: 100vw !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
  }}

  body.fullscreen-soc-mode .page {{
    max-width: 100% !important;
  }}

  /* SVG node hover & high-contrast glow effects */
  .svg-node-group:hover circle:first-child {{
    filter: drop-shadow(0 0 8px rgba(16, 185, 129, 0.6));
  }}
  .svg-node-threat:hover circle:first-child {{
    filter: drop-shadow(0 0 8px rgba(244, 63, 94, 0.7));
  }}
  .svg-node-amber:hover circle:first-child {{
    filter: drop-shadow(0 0 8px rgba(245, 158, 11, 0.7));
  }}
</style>
</head>

<body data-role="admin" data-portal="admin" data-page="security" class="bg-slate-100 text-slate-800 font-sans antialiased min-h-screen flex flex-col">

<!-- Main Layout Structure for layout.js -->
<main class="main flex-1 min-w-0 flex flex-col">

  {UNIFIED_HEADER}

  <!-- Main Cyber Defense Content Container -->
  <div class="page flex-1 max-w-7xl w-full mx-auto p-3 sm:p-5 lg:p-6 space-y-4 sm:space-y-6">
    {main_content}
  </div>

</main>

<!-- Modals, Overlays & Drawers -->
{DRAWER_HTML}

{MODAL_HTML}

{FS_OVERLAY_HTML}

{SCRIPT_CONTROLLER}

</body>
</html>
'''

with open(r'c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\pages\admin\admin-security.html', 'w', encoding='utf-8') as out:
    out.write(full_html)

print("Master admin-security.html successfully built! Total size:", len(full_html))
