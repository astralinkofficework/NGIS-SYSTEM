import re

with open(r'pages/admin/admin-security.html', 'r', encoding='utf-8') as f:
    content = f.read()

single_header = '''  <!-- Hero Banner Anchor for layout.js -->
  <header id="heroBanner" role="banner"></header>

  <!-- Unified Sticky Responsive Header (Mobile Appbar + Desktop Executive + Tabs) -->
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

# Replace from mobile-appbar or heroBanner to end of header
header_matcher = re.compile(
    r'<header class="mobile-appbar md:hidden.*?</header>\s*'
    r'<header id="heroBanner" role="banner"></header>\s*'
    r'<div class="bg-white border-b border-slate-200 sticky.*?</nav>\s*</div>\s*</div>',
    re.DOTALL
)

if header_matcher.search(content):
    content = header_matcher.sub(single_header, content)
    print("Replaced with single unified header!")
else:
    print("Trying fallback regex...")
    fallback_matcher = re.compile(r'<header class="mobile-appbar.*?id="navTabs".*?</nav>\s*</div>\s*(?:</div>|</header>)', re.DOTALL)
    if fallback_matcher.search(content):
        content = fallback_matcher.sub(single_header, content)
        print("Replaced via fallback regex!")
    else:
        print("FAILED TO MATCH HEADER")

with open(r'pages/admin/admin-security.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved.")
