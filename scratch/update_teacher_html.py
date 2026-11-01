import re

with open('pages/teacher/teacher.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add bottom-nav.css and tailwindcss in head
if 'bottom-nav.css' not in content:
    content = content.replace('<link rel="stylesheet" href="../../assets/css/design-system.css">', 
                              '<link rel="stylesheet" href="../../assets/css/design-system.css">\n<link rel="stylesheet" href="../../assets/css/bottom-nav.css">')

if 'cdn.tailwindcss.com' not in content:
    tailwind_script = '''<!-- Phosphor Icons for mobile UI glyphs -->
<script src="https://unpkg.com/@phosphor-icons/web"></script>
<!-- Tailwind CSS with preflight disabled to protect desktop styles -->
<script src="https://cdn.tailwindcss.com"></script>
<script>
  tailwind.config = {
    corePlugins: {
      preflight: false
    }
  };
</script>'''
    content = content.replace('<script src="https://unpkg.com/@phosphor-icons/web"></script>', tailwind_script)

# 2. Replace 2-row grid override with clean 3-column deck
old_style = '''/* Ensure 2-row grid on desktop matching reference layout */
@media (min-width: 992px) {
  .dash-overlap {
    display: grid !important;
    grid-template-columns: 240px minmax(0, 1fr) 260px !important;
    grid-template-rows: auto auto !important;
    gap: 16px !important;
  }
  .ov-profile {
    grid-column: 1 !important;
    grid-row: 1 !important;
  }
  .ov-upcoming {
    grid-column: 2 !important;
    grid-row: 1 !important;
  }
  .ov-deadlines {
    grid-column: 3 !important;
    grid-row: 1 / span 2 !important;
  }
  .dash-overlap .promo-slideshow {
    grid-column: 1 / span 2 !important;
    grid-row: 2 !important;
    margin-top: 0 !important;
  }
}'''

new_style = '''/* Clean 3-column deck on desktop matching original reference layout */
@media (min-width: 992px) {
  .dash-overlap {
    display: grid !important;
    grid-template-columns: 240px minmax(0, 1fr) 270px !important;
    gap: 18px !important;
    max-width: 1280px !important;
    margin: -48px auto 0 !important;
    padding: 0 24px !important;
    align-items: stretch !important;
  }
  .ov-profile, .ov-upcoming, .ov-deadlines {
    grid-column: auto !important;
    grid-row: 1 !important;
    height: 100% !important;
  }
}'''

if old_style in content:
    content = content.replace(old_style, new_style)

# 3. Move promo-slideshow out of dash-overlap
promo_marker = '<!-- Row 2, Col 1+2: Promo Slideshow (Priority Tasks spans both rows) -->'
if promo_marker in content:
    idx_promo = content.find(promo_marker)
    idx_close_overlap = content.find('</div><!-- /.dash-overlap -->', idx_promo)
    promo_html = content[idx_promo:idx_close_overlap].strip()
    
    banner_section = f'''</div><!-- /.dash-overlap -->

<!-- ═══════════════ TEACHER BANNER SECTION ═══════════════ -->
<div class="dash-banner-section">
{promo_html}
</div>'''
    content = content[:idx_promo] + banner_section + content[idx_close_overlap + len('</div><!-- /.dash-overlap -->'):]

with open('pages/teacher/teacher.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated teacher.html successfully!')

