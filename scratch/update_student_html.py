import re

# 1. Update student.html
with open('pages/student/student.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add tailwind CDN in head if not present
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

# Replace the 2-row desktop grid CSS with clean 3-col deck
old_style_block = '''/* Ensure 2-row grid on desktop matching reference layout */
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

new_style_block = '''/* Clean 3-column deck on desktop matching original reference layout */
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

if old_style_block in content:
    content = content.replace(old_style_block, new_style_block)

# Move promo-slideshow out of dash-overlap
promo_marker = '<!-- Row 2, Col 1+2: Promo Slideshow (Deadlines spans both rows) -->'
if promo_marker in content:
    # Find start of promo and end of dash-overlap
    idx_promo = content.find(promo_marker)
    idx_close_overlap = content.find('</div><!-- /.dash-overlap -->', idx_promo)
    promo_html = content[idx_promo:idx_close_overlap].strip()
    
    # We want promo_slideshow wrapped in dash-banner-section directly after dash-overlap
    banner_section = f'''</div><!-- /.dash-overlap -->

<!-- ═══════════════ DASHBOARD BANNER SECTION ═══════════════ -->
<div class="dash-banner-section">
{promo_html}
</div>'''
    content = content[:idx_promo] + banner_section + content[idx_close_overlap + len('</div><!-- /.dash-overlap -->'):]

# Fix closing structure around line 605-640
# Look for where .dash closes, and reorganize properly
pattern_closing = re.compile(r'</div><!-- /.dash -->\s*</div><!-- /.main -->[\s\S]*?<div class="student-mobile-view" id="studentMobileView">', re.MULTILINE)

fixed_transition = '''</div><!-- /.dash -->
</div><!-- /.student-desktop-view -->

<!-- ═══════════════ STUDENT MOBILE VIEW ═══════════════ -->
<div class="student-mobile-view" id="studentMobileView">'''

content = pattern_closing.sub(fixed_transition, content)

# Also ensure closing tags at end of student-mobile-view and .main
# In the original file:
#       </section>
#     </main>
#     <!-- Premium Floating Bottom Navigation Dock -->
#     ...
#     </nav>
#   </div>
# </div>
# </div>
# <div class="id-modal-overlay" id="idModal">

# Let's inspect where scripts and .main close
if '<!-- Digital Student ID Card Modal -->' in content:
    content = content.replace('<!-- Digital Student ID Card Modal -->\n</div><!-- /.student-desktop-view -->', '<!-- Digital Student ID Card Modal -->')

# Save updated student.html
with open('pages/student/student.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated student.html successfully!')
