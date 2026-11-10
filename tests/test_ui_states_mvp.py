"""
NGIS ERP — Master UI States MVP Test Suite
Verifies all 10 essential UI states across portals:
1. Empty State
2. Loading State (Skeleton loaders)
3. Error State
4. Offline State
5. Slow Network State (Measurable progress & anti-duplicate guard)
6. No Search Results State
7. Permission Denied State
8. Session Expired State (with automatic draft preservation)
9. Form Validation State (inline accessible feedback)
10. Success State (accessible toasts with action buttons)
Plus Typography (strict <= 500 font weight) and Mobile Hamburger compliance.
"""

import asyncio
import json
from playwright.async_api import async_playwright

BASE_URL = "http://127.0.0.1:3000"

async def run_ui_states_tests():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1280, "height": 800})
        
        # Setup Teacher authenticated persona
        teacher_user = {
            "id": "teacher-jenkins",
            "name": "Dr. Sarah Jenkins",
            "role": "teacher",
            "email": "jenkins@ngis.edu"
        }
        await context.add_init_script(f"""
            localStorage.setItem('auth_user', JSON.stringify({json.dumps(teacher_user)}));
            localStorage.setItem('token', 'fake-jwt-token-teacher');
            localStorage.setItem('ngis-theme', 'light');
        """)
        
        page = await context.new_page()
        
        print("=======================================================")
        print(" NGIS ERP — MASTER UI STATES MVP TEST SUITE")
        print("=======================================================\n")
        
        passed_count = 0
        total_count = 0
        
        def record_check(name, passed, detail=""):
            nonlocal passed_count, total_count
            total_count += 1
            if passed:
                passed_count += 1
                print(f"  [PASS] {name} {detail}")
            else:
                print(f"  [FAIL] {name} {detail}")
        
        # Navigate to a base page
        await page.goto(f"{BASE_URL}/pages/teacher/teacher.html", wait_until="networkidle")
        
        # ---------------------------------------------------------------------
        # 1. EMPTY STATE
        # ---------------------------------------------------------------------
        print("\n--- Test State 1: Empty State ---")
        empty_res = await page.evaluate("""() => {
            const container = document.createElement('div');
            container.id = 'testEmptyContainer';
            document.body.appendChild(container);
            
            let actionClicked = false;
            window.NGISUI.renderEmptyState(container, {
                title: 'No classes assigned',
                description: 'You currently have no active course sections for Term 1.',
                icon: 'school',
                actionText: 'Request Section Assignment',
                onAction: () => { actionClicked = true; }
            });
            
            const card = container.querySelector('.ngis-empty-state');
            const title = container.querySelector('.ngis-state-title')?.textContent;
            const desc = container.querySelector('.ngis-state-desc')?.textContent;
            const btn = container.querySelector('.ngis-btn-primary');
            if (btn) btn.click();
            
            return {
                hasCard: Boolean(card),
                titleMatches: title === 'No classes assigned',
                descMatches: desc.includes('active course sections'),
                actionTriggered: actionClicked
            };
        }""")
        record_check("Empty State renders card", empty_res["hasCard"])
        record_check("Empty State displays title & description", empty_res["titleMatches"] and empty_res["descMatches"])
        record_check("Empty State action button executes callback", empty_res["actionTriggered"])
        
        # ---------------------------------------------------------------------
        # 2. LOADING STATE (SKELETON LOADERS)
        # ---------------------------------------------------------------------
        print("\n--- Test State 2: Loading State (Skeleton Loaders) ---")
        skeleton_res = await page.evaluate("""() => {
            const tableContainer = document.createElement('tbody');
            tableContainer.id = 'testTableSkeleton';
            document.body.appendChild(tableContainer);
            
            window.NGISUI.showSkeleton(tableContainer, 'table', 4);
            const rows = tableContainer.querySelectorAll('.ngis-skeleton-row');
            const pulses = tableContainer.querySelectorAll('.ngis-skeleton-pulse');
            const busy = tableContainer.getAttribute('aria-busy');
            
            // Hide skeleton
            window.NGISUI.hideSkeleton(tableContainer);
            const cleared = tableContainer.children.length === 0;
            
            // Test cards skeleton
            const cardContainer = document.createElement('div');
            window.NGISUI.showSkeleton(cardContainer, 'cards', 3);
            const cardPulses = cardContainer.querySelectorAll('.ngis-skeleton-pulse');
            
            return {
                tableRowCount: rows.length,
                pulseCount: pulses.length,
                ariaBusy: busy === 'true',
                clearedSuccessfully: cleared,
                cardSkeletonCount: cardPulses.length
            };
        }""")
        record_check("Loading State table skeleton generates 4 rows", skeleton_res["tableRowCount"] == 4)
        record_check("Loading State pulses and sets aria-busy='true'", skeleton_res["pulseCount"] > 0 and skeleton_res["ariaBusy"])
        record_check("Loading State hideSkeleton clears skeleton elements", skeleton_res["clearedSuccessfully"])
        record_check("Loading State card skeleton generates matching layout", skeleton_res["cardSkeletonCount"] > 0)
        
        # ---------------------------------------------------------------------
        # 3. ERROR STATE
        # ---------------------------------------------------------------------
        print("\n--- Test State 3: Error State ---")
        error_res = await page.evaluate("""() => {
            const container = document.createElement('div');
            document.body.appendChild(container);
            
            let retryInvoked = false;
            window.NGISUI.renderErrorState(container, {
                title: 'Unable to load academic roster',
                message: 'The grading and roster service is temporarily unreachable.',
                onRetry: () => { retryInvoked = true; }
            });
            
            const card = container.querySelector('.ngis-error-state');
            const title = container.querySelector('.ngis-state-title')?.textContent;
            const retryBtn = container.querySelector('.ngis-btn-retry');
            if (retryBtn) retryBtn.click();
            
            return {
                hasCard: Boolean(card),
                titleMatches: title === 'Unable to load academic roster',
                retryWorks: retryInvoked
            };
        }""")
        record_check("Error State renders error card", error_res["hasCard"])
        record_check("Error State displays clear problem explanation", error_res["titleMatches"])
        record_check("Error State retry action button triggers recovery", error_res["retryWorks"])
        
        # ---------------------------------------------------------------------
        # 4. OFFLINE STATE
        # ---------------------------------------------------------------------
        print("\n--- Test State 4: Offline State ---")
        offline_res = await page.evaluate("""() => {
            // Trigger offline event
            window.dispatchEvent(new Event('offline'));
            const banner = document.getElementById('ngisOfflineBanner');
            const isVisible = banner && !banner.classList.contains('hidden') && banner.offsetHeight > 0;
            const bannerText = banner?.textContent || '';
            
            // Trigger online event
            window.dispatchEvent(new Event('online'));
            const isHidden = banner && banner.classList.contains('hidden');
            
            return {
                bannerShownOnOffline: Boolean(isVisible),
                bannerExplainsPreservation: bannerText.includes('offline') || bannerText.includes('saved to local draft'),
                bannerHiddenOnOnline: Boolean(isHidden)
            };
        }""")
        record_check("Offline State displays non-intrusive banner on disconnection", offline_res["bannerShownOnOffline"])
        record_check("Offline State informs user of local draft preservation", offline_res["bannerExplainsPreservation"])
        record_check("Offline State removes banner when connection restored", offline_res["bannerHiddenOnOnline"])
        
        # ---------------------------------------------------------------------
        # 5. SLOW NETWORK STATE & ANTI-DUPLICATE GUARD
        # ---------------------------------------------------------------------
        print("\n--- Test State 5: Slow Network State & Anti-Duplicate Guard ---")
        slow_res = await page.evaluate("""async () => {
            const btn = document.createElement('button');
            btn.textContent = 'Submit Gradebook';
            document.body.appendChild(btn);
            
            let executedTimes = 0;
            const slowOperation = async () => {
                executedTimes++;
                await new Promise(r => setTimeout(r, 100));
            };
            
            // Initiate guarded submit
            const promise = window.NGISUI.guardSubmit(btn, slowOperation);
            
            // Inspect intermediate busy state immediately
            const isDisabledDuring = btn.disabled === true;
            const isBusyDuring = btn.getAttribute('aria-busy') === 'true';
            
            // Attempt duplicate click while busy
            btn.click();
            
            await promise;
            
            // Inspect completed state
            const isDisabledAfter = btn.disabled === false;
            
            // Test real measurable progress tracking
            const prog = document.createElement('div');
            window.NGISUI.trackProgress(prog, 3, 10);
            const valNow = prog.getAttribute('aria-valuenow');
            const widthPct = prog.style.width;
            
            return {
                disabledDuring: isDisabledDuring,
                ariaBusyDuring: isBusyDuring,
                singleExecutionOnly: executedTimes === 1,
                restoredAfter: isDisabledAfter,
                progressRealPct: valNow === '30' && widthPct === '30%'
            };
        }""")
        record_check("Slow Network guard immediately disables button and sets aria-busy='true'", slow_res["disabledDuring"] and slow_res["ariaBusyDuring"])
        record_check("Slow Network guard prevents duplicate submissions", slow_res["singleExecutionOnly"])
        record_check("Slow Network guard restores button state upon completion", slow_res["restoredAfter"])
        record_check("Measurable progress bar strictly displays real percentage (no fake math)", slow_res["progressRealPct"])
        
        # ---------------------------------------------------------------------
        # 6. NO SEARCH RESULTS STATE
        # ---------------------------------------------------------------------
        print("\n--- Test State 6: No Search Results State ---")
        # Test in teacher-lessons.html
        await page.goto(f"{BASE_URL}/pages/teacher/teacher-lessons.html", wait_until="networkidle")
        search_res = await page.evaluate("""() => {
            const input = document.getElementById('lessonSearch');
            if (input) {
                input.value = 'NonExistentLessonTopic12345XYZ';
                window.filterTable();
            }
            
            const cell = document.getElementById('lessonsEmptyCell');
            const hasNoResults = Boolean(cell?.querySelector('.ngis-no-results-state'));
            const desc = cell?.querySelector('.ngis-state-desc')?.textContent || '';
            const resetBtn = cell?.querySelector('.ngis-btn-reset');
            
            // Click reset
            if (resetBtn) resetBtn.click();
            const restoredRows = document.querySelectorAll('#lessonsTbody tr').length > 1;
            
            return {
                showsNoResultsCard: hasNoResults,
                clearActionRestoresTable: restoredRows
            };
        }""")
        record_check("No Search Results displays state card when filter yields 0 matches", search_res["showsNoResultsCard"])
        record_check("No Search Results reset button clears filter and restores table rows", search_res["clearActionRestoresTable"])
        
        # ---------------------------------------------------------------------
        # 7. PERMISSION DENIED STATE
        # ---------------------------------------------------------------------
        print("\n--- Test State 7: Permission Denied State ---")
        perm_res = await page.evaluate("""() => {
            const container = document.createElement('div');
            document.body.appendChild(container);
            
            window.NGISUI.renderPermissionDenied(container, {
                title: 'Section Roster Restricted',
                reason: 'Institutional policy restricts access to homeroom advisor records for Grade 12.',
                returnUrl: 'teacher.html'
            });
            
            const card = container.querySelector('.ngis-denied-state');
            const title = container.querySelector('.ngis-state-title')?.textContent;
            const badge = container.querySelector('.ngis-badge-danger')?.textContent;
            const action = container.querySelector('.ngis-btn-primary');
            
            return {
                hasCard: Boolean(card),
                titleMatches: title === 'Section Roster Restricted',
                badgeMatches: badge?.includes('Restricted'),
                hasReturnAction: Boolean(action)
            };
        }""")
        record_check("Permission Denied renders institutional restriction card", perm_res["hasCard"])
        record_check("Permission Denied displays why access is restricted", perm_res["titleMatches"] and perm_res["badgeMatches"])
        record_check("Permission Denied provides safe return navigation action", perm_res["hasReturnAction"])
        
        # Also verify shared/access-denied.html page
        await page.goto(f"{BASE_URL}/pages/shared/access-denied.html", wait_until="networkidle")
        page_denied_res = await page.evaluate("""() => {
            const title = document.querySelector('.denied-title')?.textContent || '';
            const theme = document.documentElement.getAttribute('data-theme');
            return {
                hasTitle: title.includes('Access') || title.includes('Restricted'),
                lightTheme: theme === 'light'
            };
        }""")
        record_check("Shared access-denied.html page renders cleanly with light theme", page_denied_res["hasTitle"] and page_denied_res["lightTheme"])
        
        # ---------------------------------------------------------------------
        # 8. SESSION EXPIRED STATE & AUTOMATIC DRAFT PRESERVATION
        # ---------------------------------------------------------------------
        print("\n--- Test State 8: Session Expired State & Draft Preservation ---")
        await page.goto(f"{BASE_URL}/pages/admin/admin-users.html?role=students", wait_until="networkidle")
        session_res = await page.evaluate("""() => {
            // Fill in student form
            const form = document.getElementById('addStudentForm');
            if (form) {
                const first = form.querySelector('input[name="firstName"]');
                const last = form.querySelector('input[name="lastName"]');
                if (first) first.value = 'Rithy';
                if (last) last.value = 'Samnang';
                
                // Save draft
                window.NGISUI.saveDraft('addStudentForm');
                
                // Clear fields to simulate reset/session loss
                if (first) first.value = '';
                if (last) last.value = '';
                
                // Restore draft
                const restored = window.NGISUI.restoreDraft('addStudentForm');
                const firstRestored = first?.value === 'Rithy';
                const lastRestored = last?.value === 'Samnang';
                
                // Show modal
                const modal = window.NGISUI.showSessionExpiredModal();
                const modalOpen = Boolean(document.getElementById('ngisSessionModal'));
                
                // Close modal
                if (modal && modal.remove) modal.remove();
                
                return {
                    draftRestored: Boolean(restored && firstRestored && lastRestored),
                    modalRendered: modalOpen
                };
            }
            return { draftRestored: false, modalRendered: false };
        }""")
        record_check("Session Expired preserves unsaved user form inputs to draft storage", session_res["draftRestored"])
        record_check("Session Expired displays re-authentication modal dialog", session_res["modalRendered"])
        
        # ---------------------------------------------------------------------
        # 9. FORM VALIDATION STATE
        # ---------------------------------------------------------------------
        print("\n--- Test State 9: Form Validation State (Inline Accessible Feedback) ---")
        val_res = await page.evaluate("""() => {
            const form = document.createElement('form');
            form.innerHTML = `
                <div class="field-wrap">
                    <input type="text" id="testReqInput" required name="testReq" />
                </div>
            `;
            document.body.appendChild(form);
            const input = document.getElementById('testReqInput');
            
            // Validate empty form
            const isValidEmpty = window.NGISUI.validateForm(form);
            const hasErrorClass = input.classList.contains('ngis-input-error');
            const hasAriaInvalid = input.getAttribute('aria-invalid') === 'true';
            const errorMsgEl = form.querySelector('.ngis-field-error-msg');
            const errorMsgText = errorMsgEl?.textContent || '';
            
            // Type valid value and trigger input
            input.value = 'Valid Entry';
            input.dispatchEvent(new Event('input', { bubbles: true }));
            
            const errorCleared = !input.classList.contains('ngis-input-error');
            const ariaCleared = input.getAttribute('aria-invalid') === 'false';
            const msgRemoved = !form.querySelector('.ngis-field-error-msg');
            
            form.remove();
            
            return {
                rejectedEmpty: isValidEmpty === false,
                highlightedField: hasErrorClass && hasAriaInvalid,
                displayedMessage: errorMsgText.includes('required') || errorMsgText.includes('fill'),
                clearedOnCorrection: errorCleared && ariaCleared && msgRemoved
            };
        }""")
        record_check("Form Validation detects missing required fields", val_res["rejectedEmpty"])
        record_check("Form Validation highlights problematic input with red border and aria-invalid", val_res["highlightedField"])
        record_check("Form Validation places accessible explanatory error message below field", val_res["displayedMessage"])
        record_check("Form Validation immediately clears error upon user correction", val_res["clearedOnCorrection"])
        
        # ---------------------------------------------------------------------
        # 10. SUCCESS STATE (TOASTS WITH ACTIONS)
        # ---------------------------------------------------------------------
        print("\n--- Test State 10: Success State (Toasts with Actions) ---")
        toast_res = await page.evaluate("""() => {
            let actionInvoked = false;
            window.NGISUI.toast.success('Grade published successfully', 'Score recorded for Sophea Chan.', {
                actionText: 'Export CSV',
                onAction: () => { actionInvoked = true; },
                duration: 10000
            });
            
            const toast = document.querySelector('.ngis-toast-success');
            const title = toast?.querySelector('.ngis-toast-title')?.textContent;
            const detail = toast?.querySelector('.ngis-toast-detail')?.textContent;
            const actionBtn = toast?.querySelector('.ngis-toast-action');
            if (actionBtn) actionBtn.click();
            
            return {
                toastExists: Boolean(toast),
                titleMatches: title === 'Grade published successfully',
                detailMatches: detail?.includes('Sophea Chan'),
                actionWorks: actionInvoked
            };
        }""")
        record_check("Success State displays rich toast notification", toast_res["toastExists"])
        record_check("Success State shows action title and detail description", toast_res["titleMatches"] and toast_res["detailMatches"])
        record_check("Success State action button responds to user clicks", toast_res["actionWorks"])
        
        # ---------------------------------------------------------------------
        # 11. STRICT TYPOGRAPHY & NO BOLD AUDIT
        # ---------------------------------------------------------------------
        print("\n--- Test Typography & Mobile Navigation Compliance ---")
        typo_res = await page.evaluate("""() => {
            // Check computed weights of all NGISUI rendered elements
            const stateEls = document.querySelectorAll(
                '.ngis-empty-state, .ngis-error-state, .ngis-denied-state, .ngis-no-results-state, ' +
                '.ngis-state-title, .ngis-state-desc, .ngis-toast-title, .ngis-toast-detail, .ngis-field-error-msg'
            );
            
            let heavyFound = [];
            stateEls.forEach(el => {
                const w = parseInt(window.getComputedStyle(el).fontWeight, 10);
                if (w > 500) {
                    heavyFound.push({ tag: el.tagName, cls: el.className, weight: w });
                }
            });
            
            return {
                heavyCount: heavyFound.length,
                heavySamples: heavyFound.slice(0, 3)
            };
        }""")
        record_check("Strict NO BOLD policy: all UI states use font-weight <= 500", typo_res["heavyCount"] == 0, f"(violators: {typo_res['heavyCount']})")
        
        # Check hamburger button on mobile viewport
        await page.set_viewport_size({"width": 390, "height": 844})
        await page.goto(f"{BASE_URL}/pages/teacher/teacher.html", wait_until="networkidle")
        hamburger_res = await page.evaluate("""() => {
            const btn = document.querySelector('[data-action=\"toggle-sidebar\"], .hamburger-btn, .mobile-hamburger-btn');
            return {
                exists: Boolean(btn),
                hasSidebarAction: btn?.getAttribute('data-action') === 'toggle-sidebar'
            };
        }""")
        record_check("Mobile Navigation: Mandatory hamburger menu button present with data-action='toggle-sidebar'", hamburger_res["exists"] and hamburger_res["hasSidebarAction"])
        
        await browser.close()
        
        print("\n=======================================================")
        print(f" RESULT: {passed_count} / {total_count} CHECKS PASSED")
        print("=======================================================\n")
        assert passed_count == total_count, f"{total_count - passed_count} checks failed!"

if __name__ == "__main__":
    asyncio.run(run_ui_states_tests())

