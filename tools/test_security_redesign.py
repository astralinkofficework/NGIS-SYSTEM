from playwright.sync_api import sync_playwright

def test_full_security_suite():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        console_errors = []
        page_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type in ["error"] else None)
        page.on("pageerror", lambda err: page_errors.append(str(err)))

        print("=== 1. Desktop 1280x1024 Executive Layout & Telemetry ===")
        page.set_viewport_size({"width": 1280, "height": 1024})
        page.goto("http://127.0.0.1:3000/pages/admin/admin-security.html")
        page.wait_for_load_state("networkidle")

        print("Page Title:", page.title())
        sidebar = page.query_selector(".sidebar, [data-sidebar], .app-sidebar, #sidebar")
        print("Sidebar present on desktop:", bool(sidebar))
        
        scroll_w = page.evaluate("() => document.documentElement.scrollWidth")
        client_w = page.evaluate("() => document.documentElement.clientWidth")
        overflow_desktop = scroll_w - client_w
        print(f"Scroll width: {scroll_w}, Client width: {client_w}, Horizontal overflow: {overflow_desktop}px")
        assert overflow_desktop <= 0, f"Desktop has {overflow_desktop}px horizontal overflow!"

        radar = page.query_selector(".radar-grid svg")
        print("Radar SVG present:", bool(radar))
        feed_items = page.query_selector_all("[onclick*='openForensics']")
        print(f"Interactive forensics elements found: {len(feed_items)}")

        # 2. Tab Switching Verification
        print("\n=== 2. Tab Switching Test ===")
        tabs = ['overview', 'user-restrictions', 'security-events', 'rate-limiting', 'ip-activity', 'audit-history', 'security-settings']
        for t in tabs:
            btn = page.locator(f"[data-tab='{t}']").first
            btn.click()
            page.wait_for_timeout(80)
            is_hidden = page.evaluate(f"() => document.getElementById('tab-{t}').classList.contains('hidden')")
            print(f"  Tab '{t}': Pane visible = {not is_hidden}")
            assert not is_hidden, f"Tab pane #tab-{t} should be visible after clicking tab!"

        # Return to overview
        page.locator("[data-tab='overview']").first.click()

        # 3. Forensic Side Drawer Verification (matching media_1794919677484_76494917.jpg)
        print("\n=== 3. Forensic Side Drawer Test ===")
        node_btn = page.locator("[onclick*=\"openForensics('node-unauthorized')\"]:visible").first
        node_btn.click()
        page.wait_for_timeout(150)
        
        is_overlay_hidden = page.evaluate("() => document.getElementById('forensicDrawerOverlay').classList.contains('hidden')")
        title_text = page.eval_on_selector("#inspTitle", "el => el.textContent")
        src_ip = page.eval_on_selector("#inspSrcIp", "el => el.textContent")
        target_acc = page.eval_on_selector("#inspTargetAccount", "el => el.textContent")
        attack_type = page.eval_on_selector("#inspAttackType", "el => el.textContent")
        gw_action = page.eval_on_selector("#inspAction", "el => el.textContent")
        
        print(f"  Drawer visible: {not is_overlay_hidden}")
        print(f"  Attack title: {title_text}")
        print(f"  Attack type: {attack_type}")
        print(f"  Gateway action: {gw_action}")
        print(f"  Source IP: {src_ip}")
        print(f"  Target Account: {target_acc}")
        
        assert not is_overlay_hidden, "Forensic drawer should be visible after click!"
        assert "UNAUTHORIZED" in title_text, "Title should match unauthorized attack!"
        assert "127.0.0.1:49210" in src_ip, "Source IP should match 127.0.0.1:49210!"
        assert "Aiko Dubois" in target_acc, "Target account should match Aiko Dubois!"

        # 4. Instant Perimeter Mitigation Controls (Block IP & Suspend Account)
        print("\n=== 4. Instant Mitigation Controls Test ===")
        btn_block = page.locator("#btnBlockIp")
        btn_block.click()
        page.wait_for_timeout(300)
        btn_block_text = page.eval_on_selector("#btnBlockIpText", "el => el.textContent")
        print(f"  Block IP clicked -> button text: '{btn_block_text}'")
        assert "Blocked" in btn_block_text, "Block IP button should indicate blocked state!"

        btn_suspend = page.locator("#btnSuspend")
        btn_suspend.click()
        page.wait_for_timeout(300)
        btn_suspend_text = page.eval_on_selector("#btnSuspendText", "el => el.textContent")
        print(f"  Suspend Account clicked -> button text: '{btn_suspend_text}'")
        assert "Suspended" in btn_suspend_text, "Suspend Account button should indicate suspended state!"

        # 5. PCAP Bundle Export
        print("\n=== 5. PCAP Bundle Export Test ===")
        with page.expect_download() as download_info:
            page.locator("button:has-text('Export PCAP Bundle')").click()
        download = download_info.value
        print(f"  Downloaded PCAP filename: {download.suggested_filename}")
        assert "ngis-soc-pcap" in download.suggested_filename, "PCAP dump filename should contain ngis-soc-pcap!"

        # Close drawer via ESC
        page.keyboard.press("Escape")
        page.wait_for_timeout(150)
        is_closed = page.evaluate("() => document.getElementById('forensicDrawerOverlay').classList.contains('hidden')")
        print(f"  Drawer closed on ESC: {is_closed}")
        assert is_closed, "Drawer should close on ESC!"

        # 6. Fullscreen & Sidebar Collapse Verification
        print("\n=== 6. Fullscreen SOC Mode & Sidebar Collapse Test ===")
        fs_btn = page.locator("[onclick*='toggleFullscreenMap']:visible").first
        fs_btn.click()
        page.wait_for_timeout(350)
        is_fs = page.evaluate("() => document.body.classList.contains('fullscreen-soc-mode')")
        print(f"  body.fullscreen-soc-mode active: {is_fs}")
        assert is_fs, "fullscreen-soc-mode class should be added to body!"

        # Check sidebar is collapsed
        sb_transform = page.evaluate("() => window.getComputedStyle(document.querySelector('#sidebar, .sidebar')).transform")
        sb_opacity = page.evaluate("() => window.getComputedStyle(document.querySelector('#sidebar, .sidebar')).opacity")
        print(f"  Sidebar transform in Fullscreen mode: {sb_transform}")
        print(f"  Sidebar opacity in Fullscreen mode: {sb_opacity}")
        assert sb_opacity == "0", "Sidebar should be invisible (opacity 0) in fullscreen SOC mode!"

        # Exit fullscreen via ESC
        page.keyboard.press("Escape")
        page.wait_for_timeout(350)
        is_fs_restored = not page.evaluate("() => document.body.classList.contains('fullscreen-soc-mode')")
        print(f"  Fullscreen exited and layout restored on ESC: {is_fs_restored}")
        assert is_fs_restored, "Fullscreen SOC mode should deactivate on ESC!"

        # 7. Mobile Viewports (320px, 360px, 375px, 390px, 414px)
        print("\n=== 7. Mobile Responsiveness & Hamburger Menu Test ===")
        viewports = [
            ("Narrow Mobile (320px)", 320, 568),
            ("Standard Android (360px)", 360, 640),
            ("iPhone SE / 8 (375px)", 375, 667),
            ("iPhone 12 / 14 / 15 (390px)", 390, 844),
            ("iPhone Plus / Max (414px)", 414, 896),
        ]

        for name, w, h in viewports:
            page.set_viewport_size({"width": w, "height": h})
            page.wait_for_timeout(150)
            sw = page.evaluate("() => document.documentElement.scrollWidth")
            cw = page.evaluate("() => document.documentElement.clientWidth")
            diff = sw - cw
            print(f"  {name}: Scroll width = {sw}, Client width = {cw}, Overflow = {diff}px")
            assert diff <= 0, f"{name} has {diff}px horizontal overflow!"

        # Test mobile hamburger button
        page.set_viewport_size({"width": 375, "height": 667})
        page.wait_for_timeout(150)
        hamburger = page.locator("[data-action='toggle-sidebar']:visible").first
        is_h_visible = hamburger.is_visible()
        print(f"  Mobile hamburger visible: {is_h_visible}")
        assert is_h_visible, "Mobile hamburger menu must be visible on mobile!"

        # Click hamburger to verify sidebar toggle
        hamburger.click()
        page.wait_for_timeout(200)
        drawer_open = page.evaluate("() => document.body.classList.contains('sidebar-open') || !!document.querySelector('.sidebar.open, .mobile-sidebar-drawer.open, [data-sidebar-open=\"true\"]')")
        print(f"  Sidebar drawer opened on hamburger tap: {drawer_open}")

        # Check console and page errors
        print("\n=== 8. Console & Page Errors Audit ===")
        print(f"Console errors: {len(console_errors)}")
        for e in console_errors:
            print("  [ERROR]:", e)
        print(f"Page errors: {len(page_errors)}")
        for e in page_errors:
            print("  [PAGE ERROR]:", e)
        
        assert len(console_errors) == 0, f"Found {len(console_errors)} console errors!"
        assert len(page_errors) == 0, f"Found {len(page_errors)} page errors!"

        print("\n>>> ALL TEST SUITE STAGES PASSED FLAWLESSLY! <<<")
        browser.close()

if __name__ == "__main__":
    test_full_security_suite()
