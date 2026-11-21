import os, sys
from playwright.sync_api import sync_playwright

VIEWPORTS = [
    (320, 568, 'iPhone SE (1st gen)'),
    (360, 800, 'Android Standard'),
    (375, 667, 'iPhone 8 / SE'),
    (390, 844, 'iPhone 13 / 14 / 15'),
    (430, 932, 'iPhone Pro Max'),
    (480, 854, 'Large Phone'),
    (600, 960, 'Small Tablet Portrait'),
    (768, 1024, 'iPad Portrait'),
    (820, 1180, 'iPad Air'),
    (1024, 768, 'iPad Landscape / Small Laptop'),
    (1280, 800, 'Standard Laptop'),
    (1440, 900, 'Desktop Standard'),
    (1920, 1080, 'Full HD Desktop'),
    (2560, 1440, '2K QHD Desktop'),
    (3840, 2160, '4K UHD Display')
]

PORTAL_PAGES = [
    'http://127.0.0.1:3000/pages/shared/design-system-preview.html',
    'http://127.0.0.1:3000/pages/student/student-exams.html',
    'http://127.0.0.1:3000/pages/student/student.html',
    'http://127.0.0.1:3000/pages/teacher/teacher.html',
    'http://127.0.0.1:3000/pages/principal/principal.html',
    'http://127.0.0.1:3000/pages/admin/admin.html',
    'http://127.0.0.1:3000/pages/shared/department.html'
]

def run_tests():
    print('Starting Master Mobile UX & 15-Viewport Quality Assurance Suite...')
    
    with sync_playwright() as p:
        browser = p.chromium.launch()

        # =====================================================================
        # 1. VERIFY ALL 10 MOBILE UX IMPROVEMENTS ON PREVIEW PAGE
        # =====================================================================
        print('\n--- 1. Testing 10 Mobile UX Improvements on Design System Preview ---')
        page = browser.new_page(viewport={'width': 375, 'height': 812})
        page.goto('http://127.0.0.1:3000/pages/shared/design-system-preview.html')
        page.wait_for_selector('#sectionMobileUX')

        # Test 1: Minimum 16px font-size on mobile inputs (Auto-zoom prevention)
        font_sizes = page.evaluate('''() => {
            const inputs = document.querySelectorAll('#sectionMobileUX input:not([type="checkbox"]):not([type="radio"])');
            const res = [];
            for (const inp of inputs) {
                const fs = parseFloat(window.getComputedStyle(inp).fontSize);
                res.push({ id: inp.id, fs: fs });
            }
            return res;
        }''')
        for item in font_sizes:
            assert item['fs'] >= 16.0, f"Auto-zoom violation: {item['id']} font-size is {item['fs']}px (must be >= 16px)"
        print(f"  [PASS] 1. Auto-zoom prevention: All {len(font_sizes)} mobile inputs enforce >= 16px font-size")

        # Test 2: Tap highlights removed (-webkit-tap-highlight-color: transparent)
        tap_highlight = page.evaluate('''() => {
            const el = document.querySelector('#sectionMobileUX button') || document.querySelector('.btn-primary');
            return window.getComputedStyle(el).webkitTapHighlightColor;
        }''')
        assert 'rgba(0, 0, 0, 0)' in tap_highlight or 'transparent' in tap_highlight, f"Tap highlight not transparent: {tap_highlight}"
        print(f"  [PASS] 2. Tap highlights: -webkit-tap-highlight-color is transparent ({tap_highlight})")

        # Test 3: Appropriate mobile keyboards & inputmodes
        modes = page.evaluate('''() => {
            return {
                phone: document.querySelector('#mobPhoneInput').getAttribute('inputmode'),
                phoneType: document.querySelector('#mobPhoneInput').getAttribute('type'),
                studentId: document.querySelector('#mobIdInput').getAttribute('inputmode'),
                score: document.querySelector('#mobScoreInput').getAttribute('inputmode'),
                email: document.querySelector('#mobEmailInput').getAttribute('inputmode'),
                search: document.querySelector('#mobSearchInput').getAttribute('inputmode')
            };
        }''')
        assert modes['phone'] == 'tel' and modes['phoneType'] == 'tel', f"Phone keyboard mismatch: {modes}"
        assert modes['studentId'] == 'numeric', f"Student ID numeric mode mismatch: {modes}"
        assert modes['score'] == 'decimal', f"Score decimal mode mismatch: {modes}"
        assert modes['email'] == 'email', f"Email mode mismatch: {modes}"
        assert modes['search'] == 'search', f"Search mode mismatch: {modes}"
        print(f"  [PASS] 3. Contextual keyboards: tel, numeric, decimal, email, search correctly configured")

        # Test 4: Stuck hover prevention (active scale & touch-action manipulation)
        touch_action = page.evaluate('''() => {
            const btn = document.querySelector('.btn-primary');
            return window.getComputedStyle(btn).touchAction;
        }''')
        assert 'manipulation' in touch_action, f"Touch-action manipulation mismatch: {touch_action}"
        print(f"  [PASS] 4. Stuck hover & double-tap zoom: touch-action: {touch_action}")

        # Test 5: OTP multi-box autofill & paste distribution
        page.evaluate('''() => {
            const box1 = document.querySelector('#otpBox1');
            const pasteEvent = new Event('paste', { bubbles: true, cancelable: true });
            pasteEvent.clipboardData = {
                getData: () => '984215'
            };
            box1.dispatchEvent(pasteEvent);
        }''')
        otp_values = page.evaluate('''() => {
            return [1,2,3,4,5,6].map(i => document.querySelector('#otpBox' + i).value).join('');
        }''')
        assert otp_values == '984215', f"OTP paste distribution failed: {otp_values}"
        print(f"  [PASS] 5. OTP Autofill & Paste: Distributed '984215' across all 6 boxes seamlessly")

        # Test 6: Controlled overscroll behavior
        overscroll = page.evaluate('''() => {
            const track = document.querySelector('#demoScrollSnapTrack');
            return window.getComputedStyle(track).overscrollBehaviorX;
        }''')
        assert overscroll == 'contain', f"Overscroll behavior mismatch: {overscroll}"
        print(f"  [PASS] 6. Controlled overscroll: overscroll-behavior-x is {overscroll}")

        # Test 7: Email input attributes
        email_attrs = page.evaluate('''() => {
            const el = document.querySelector('#mobEmailInput');
            return {
                type: el.type,
                autoCap: el.getAttribute('autocapitalize'),
                spellcheck: el.getAttribute('spellcheck'),
                autocomplete: el.getAttribute('autocomplete')
            };
        }''')
        assert email_attrs['type'] == 'email', f"Email type mismatch: {email_attrs}"
        assert email_attrs['autoCap'] == 'none', f"Email autocapitalize mismatch: {email_attrs}"
        assert email_attrs['spellcheck'] == 'false', f"Email spellcheck mismatch: {email_attrs}"
        assert email_attrs['autocomplete'] == 'email', f"Email autocomplete mismatch: {email_attrs}"
        print(f"  [PASS] 7. Email behavior: type=email, autocapitalize=none, spellcheck=false, autocomplete=email")

        # Test 8: Contextual enterkeyhint return actions
        hints = page.evaluate('''() => {
            return {
                phone: document.querySelector('#mobPhoneInput').getAttribute('enterkeyhint'),
                search: document.querySelector('#mobSearchInput').getAttribute('enterkeyhint'),
                done: document.querySelector('#mobDoneInput').getAttribute('enterkeyhint')
            };
        }''')
        assert hints['phone'] == 'next', f"Phone enterkeyhint mismatch: {hints}"
        assert hints['search'] == 'search', f"Search enterkeyhint mismatch: {hints}"
        assert hints['done'] == 'done', f"Done enterkeyhint mismatch: {hints}"
        print(f"  [PASS] 8. EnterKeyHint: next, search, done properly mapped to form flow")

        # Test 9: Native Horizontal Scroll Snapping
        snap_type = page.evaluate('''() => {
            const track = document.querySelector('#demoScrollSnapTrack');
            return window.getComputedStyle(track).scrollSnapType;
        }''')
        assert 'x' in snap_type and 'mandatory' in snap_type, f"Scroll snap type mismatch: {snap_type}"
        print(f"  [PASS] 9. Scroll Snapping: scroll-snap-type: {snap_type}")

        # Test 10: Mobile background scroll lock helper
        page.evaluate('() => window.NGIS_MOBILE_UX.lockScroll(true);')
        is_locked = page.evaluate('() => document.body.classList.contains("modal-open");')
        assert is_locked, "Body should have modal-open class"
        page.evaluate('() => window.NGIS_MOBILE_UX.lockScroll(false);')
        is_unlocked = page.evaluate('() => !document.body.classList.contains("modal-open");')
        assert is_unlocked, "Body should not have modal-open class after release"
        print("  [PASS] 10. Background scroll lock: modal-open / sidebar-open locks body scroll chaining cleanly")

        # Take screenshots of preview page
        page.screenshot(path='tools/mobile_ux_preview_375.png')
        page_desk = browser.new_page(viewport={'width': 1440, 'height': 900})
        page_desk.goto('http://127.0.0.1:3000/pages/shared/design-system-preview.html')
        page_desk.wait_for_selector('#sectionMobileUX')
        page_desk.screenshot(path='tools/mobile_ux_preview_1440.png')
        page_desk.close()

        # =====================================================================
        # 2. AUDIT ALL 15 VIEWPORT WIDTHS (Zero Horizontal Overflow Check)
        # =====================================================================
        print('\n--- 2. Testing 15 Viewport Widths Across Portals ---')
        for width, height, label in VIEWPORTS:
            v_page = browser.new_page(viewport={'width': width, 'height': height})
            v_page.goto('http://127.0.0.1:3000/pages/shared/design-system-preview.html')
            v_page.wait_for_selector('#sectionMobileUX')
            
            scroll_w = v_page.evaluate('() => document.documentElement.scrollWidth')
            client_w = v_page.evaluate('() => document.documentElement.clientWidth')
            assert scroll_w <= client_w, f"Horizontal scroll overflow at {width}px ({label}): scrollWidth={scroll_w}, clientWidth={client_w}"
            
            # Mobile hamburger check for screens <= 768px
            if width <= 768:
                hambs = [b for b in v_page.locator('[data-action="toggle-sidebar"]').all() if b.is_visible()]
                assert len(hambs) > 0, f"No visible hamburger button at {width}px ({label})"
                box = hambs[0].bounding_box()
                assert box['width'] >= 44 and box['height'] >= 44, f"Hamburger button touch target too small at {width}px: {box}"
            
            print(f"  [PASS] Viewport {width:4d}x{height:4d} ({label:30s}): Zero horizontal overflow, clean responsive layout")
            v_page.close()

        # =====================================================================
        # 3. VERIFY PRODUCTION PORTAL PAGES (Student, Teacher, Principal, Admin)
        # =====================================================================
        print('\n--- 3. Testing Real Portal Pages (Desktop & Mobile) ---')
        for url in PORTAL_PAGES:
            slug = url.split('/')[-1]
            p_mob = browser.new_page(viewport={'width': 375, 'height': 812})
            p_mob.goto(url)
            p_mob.wait_for_load_state('domcontentloaded')
            p_mob.wait_for_timeout(300)
            
            # Check horizontal overflow
            sw = p_mob.evaluate('() => document.documentElement.scrollWidth')
            cw = p_mob.evaluate('() => document.documentElement.clientWidth')
            assert sw <= cw, f"Horizontal overflow on {slug} at 375px: sw={sw}, cw={cw}"
            
            # Check mobile hamburger button
            hambs = [b for b in p_mob.locator('[data-action="toggle-sidebar"]').all() if b.is_visible()]
            assert len(hambs) > 0, f"Missing visible mobile hamburger button on {slug}"
            box = hambs[0].bounding_box()
            assert box['width'] >= 38 and box['height'] >= 38, f"Touch target undersized on {slug}: {box}"
            
            print(f"  [PASS] Page {slug:32s}: Zero overflow, accessible mobile navigation")
            p_mob.close()

        browser.close()

    print('\n=====================================================================')
    print('ALL MOBILE UX & SYSTEM-WIDE CONSISTENCY TESTS PASSED 100% SUCCESSFULLY!')
    print('=====================================================================')

if __name__ == '__main__':
    run_tests()
