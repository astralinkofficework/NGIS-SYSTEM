import re

# 1. Update pages/teacher/teacher.html
teacher_path = r'pages/teacher/teacher.html'
with open(teacher_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the media query in style block
old_media = '''/* Ensure 2-row grid on desktop matching student reference layout */
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

new_media = '''/* Responsive Grid for Teacher Dashboard */
.dash-overlap {
  display: grid !important;
  grid-template-columns: 240px minmax(0, 1fr) 280px !important;
  grid-template-rows: auto !important;
  gap: 16px !important;
  max-width: 1280px !important;
  margin: -48px auto 0 !important;
  padding: 0 24px !important;
  align-items: stretch !important;
  box-sizing: border-box !important;
  position: relative !important;
  z-index: 20 !important;
}

.ov-profile,
.ov-upcoming,
.ov-deadlines {
  height: 100% !important;
  display: flex !important;
  flex-direction: column !important;
  box-sizing: border-box !important;
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
  grid-row: 1 !important;
}

.dash-banner-section {
  max-width: 1280px !important;
  margin: 18px auto !important;
  padding: 0 24px !important;
  position: relative !important;
  z-index: 10 !important;
  width: 100% !important;
  box-sizing: border-box !important;
}

.dash-banner-section .promo-slideshow {
  width: 100% !important;
  height: 165px !important;
  border-radius: 16px !important;
  overflow: hidden !important;
  position: relative !important;
  margin: 0 !important;
}

/* Tablet Responsive (769px to 1200px) */
@media (max-width: 1200px) and (min-width: 769px) {
  .dash-overlap {
    grid-template-columns: minmax(0, 1fr) minmax(260px, 300px) !important;
    padding: 0 16px !important;
    margin-top: -32px !important;
  }
  .ov-profile {
    grid-column: 1 / -1 !important;
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    flex-wrap: wrap !important;
    gap: 12px !important;
    padding: 14px 18px !important;
  }
  .ov-upcoming {
    grid-column: 1 !important;
    grid-row: auto !important;
  }
  .ov-deadlines {
    grid-column: 2 !important;
    grid-row: auto !important;
  }
  .dash-banner-section {
    padding: 0 16px !important;
  }
}

/* Small Tablets & Mobile Landscape (< 768px) */
@media (max-width: 768px) {
  .dash-overlap {
    grid-template-columns: 1fr !important;
    padding: 0 12px !important;
    gap: 12px !important;
    margin-top: -20px !important;
  }
  .ov-profile,
  .ov-upcoming,
  .ov-deadlines {
    grid-column: 1 !important;
    grid-row: auto !important;
  }
  .dash-banner-section {
    padding: 0 12px !important;
  }
}'''

if old_media in text:
    text = text.replace(old_media, new_media)
    print("Replaced CSS in teacher.html")
else:
    print("old_media not found directly, checking regex")
    text = re.sub(
        r'/\* Ensure 2-row grid on desktop matching student reference layout \*/.*?\.dash-overlap \.promo-slideshow \{[^}]*\}\s*\}',
        new_media,
        text,
        flags=re.DOTALL
    )
    print("Replaced CSS via regex")

# Move .promo-slideshow out of .dash-overlap into .dash-banner-section
slideshow_pattern = re.compile(
    r'(<!-- Row 2, Col 1\+2: Promo Slideshow.*?</div>\s*</div>)\s*</div><!-- /\.dash-overlap -->',
    re.DOTALL
)

m = slideshow_pattern.search(text)
if m:
    slideshow_html = m.group(1)
    replacement = '''</div><!-- /.dash-overlap -->

<!-- ═══════════════ DASHBOARD BANNER SECTION ═══════════════ -->
<div class="dash-banner-section">
''' + slideshow_html + '''
</div>'''
    text = text[:m.start()] + replacement + text[m.end():]
    print("Moved promo slideshow into .dash-banner-section in teacher.html")
else:
    print("slideshow_pattern not matched, checking exact string")
    old_block_marker = '<!-- Row 2, Col 1+2: Promo Slideshow (Deadlines spans both rows) -->'
    idx_promo = text.find(old_block_marker)
    if idx_promo != -1:
        end_overlap = text.find('</div><!-- /.dash-overlap -->', idx_promo)
        promo_part = text[idx_promo:end_overlap].strip()
        replacement = '''</div><!-- /.dash-overlap -->

<!-- ═══════════════ DASHBOARD BANNER SECTION ═══════════════ -->
<div class="dash-banner-section">
  ''' + promo_part + '''
</div>'''
        text = text[:idx_promo] + replacement + text[end_overlap + len('</div><!-- /.dash-overlap -->'):]
        print("Moved promo slideshow via substring search")

with open(teacher_path, 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(text)
print("Updated teacher.html")


# 2. Update pages/student/css/overlap.css to explicitly support teacher banner section
overlap_css_path = r'pages/student/css/overlap.css'
with open(overlap_css_path, 'r', encoding='utf-8') as f:
    ocss = f.read()

if 'body[data-role="teacher"] .dash-banner-section' not in ocss:
    ocss = ocss.replace(
        '.dash-banner-section,\nbody[data-role="student"] .dash-banner-section {',
        '.dash-banner-section,\nbody[data-role="student"] .dash-banner-section,\nbody[data-role="teacher"] .dash-banner-section {'
    )
    ocss = ocss.replace(
        '.promo-slideshow,\nbody[data-role="student"] .promo-slideshow {',
        '.promo-slideshow,\nbody[data-role="student"] .promo-slideshow,\nbody[data-role="teacher"] .promo-slideshow {'
    )
    with open(overlap_css_path, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(ocss)
    print("Updated overlap.css with teacher support")
else:
    print("overlap.css already supports teacher")

print("Responsive fixes completed!")

