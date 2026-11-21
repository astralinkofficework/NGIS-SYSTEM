with open('pages/shared/design-system-preview.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Split by the sectionMobileUX markup
pattern = r'<!-- 09\. Native Mobile UX Standards \(10 Key Improvements\) -->.*?</div>\s*</div>'
# Let's extract the mobile UX block from the first occurrence
match = re.search(r'<!-- 09\. Native Mobile UX Standards \(10 Key Improvements\) -->.*?</div>\s*</div>', content, re.DOTALL)
if match:
    mobile_ux_block = match.group(0) + '\n      </section>'
    print('Found mobile UX block, length:', len(mobile_ux_block))
    
    # Remove all occurrences of the section
    cleaned = re.sub(r'\s*<!-- 09\. Native Mobile UX Standards \(10 Key Improvements\) -->.*?</div>\s*</div>', '', content, flags=re.DOTALL)
    
    # Place it cleanly right after sectionTables
    target = '        </div>\n      </section>'
    # We want the LAST occurrence of this before </div>\n  </main>
    idx = cleaned.rfind('</section>')
    if idx != -1:
        final_html = cleaned[:idx+len('</section>')] + '\n\n      ' + mobile_ux_block + cleaned[idx+len('</section>'):]
        with open('pages/shared/design-system-preview.html', 'w', encoding='utf-8') as out:
            out.write(final_html)
        print('Successfully cleaned up and placed sectionMobileUX once at the end!')
    else:
        print('Could not find </section>')
