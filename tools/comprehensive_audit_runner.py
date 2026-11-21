import os
import json
from playwright.sync_api import sync_playwright

def run_comprehensive_audit():
    with open('tools/page_inventory.json', 'r', encoding='utf-8') as f:
        inventory = json.load(f)
    
    print(f"Loaded {len(inventory)} pages from inventory.")
    
    viewports = [
        {'name': 'mobile_375', 'width': 375, 'height': 812},
        {'name': 'tablet_768', 'width': 768, 'height': 1024},
        {'name': 'desktop_1024', 'width': 1024, 'height': 768},
        {'name': 'desktop_1440', 'width': 1440, 'height': 900}
    ]
    
    # Select key representative pages from each portal for deep diagnostic check
    test_pages = [
        # Admin
        'pages/admin/admin-departments.html',
        'pages/admin/admin-classes.html',
        'pages/admin/admin-campuses.html',
        'pages/admin/admin-attendance.html',
        'pages/admin/admin-users.html',
        'pages/admin/admin-timetable.html',
        # Principal
        'pages/principal/principal-classes.html',
        'pages/principal/principal-attendance.html',
        'pages/principal/principal-requests.html',
        'pages/principal/principal-dashboard.html',
        # Teacher
        'pages/teacher/teacher-reports.html',
        'pages/teacher/teacher-attendance.html',
        'pages/teacher/teacher-classes.html',
        'pages/teacher/teacher-submissions.html',
        # Student
        'pages/student/student.html',
        'pages/student/student-grades.html',
        'pages/student/student-attendance.html',
        'pages/student/student-assignments.html',
        # Shared & Auth
        'pages/shared/shared-calendar.html',
        'pages/shared/shared-notifications.html',
        'index.html'
    ]
    
    results = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        for ppath in test_pages:
            url = f"http://127.0.0.1:3000/{ppath}"
            page_name = os.path.basename(ppath)
            page_data = {'page': page_name, 'path': ppath, 'viewports': {}}
            
            for vp in viewports:
                page = browser.new_page(viewport={'width': vp['width'], 'height': vp['height']})
                console_errors = []
                page.on('console', lambda msg: console_errors.append(msg.text) if msg.type == 'error' else None)
                
                try:
                    resp = page.goto(url, wait_until='networkidle', timeout=12000)
                    status_code = resp.status if resp else 0
                    
                    # Layout checks
                    page_eval = page.evaluate('''() => {
                        const h1 = document.querySelector('main h1') || document.querySelector('h1');
                        const h1Box = h1 ? h1.getBoundingClientRect() : null;
                        const bodyScrollWidth = document.body.scrollWidth;
                        const docScrollWidth = document.documentElement.scrollWidth;
                        const windowWidth = window.innerWidth;
                        const hasOverflow = bodyScrollWidth > windowWidth || docScrollWidth > windowWidth;
                        
                        // Mobile hamburger check (viewport <= 768)
                        let hamburgerFound = false;
                        if (windowWidth <= 768) {
                            const hb = document.querySelector('[data-action="toggle-sidebar"]') || 
                                       document.querySelector('.hamburger-btn') || 
                                       document.querySelector('.mobile-hamburger-btn') ||
                                       document.querySelector('#htbHamburger');
                            if (hb && hb.getBoundingClientRect().width > 0) {
                                hamburgerFound = true;
                            }
                        }
                        
                        // Max font-weight check
                        const allNodes = document.querySelectorAll('h1, h2, h3, h4, h5, h6, th, button, p');
                        let maxWeight = 400;
                        for (let i = 0; i < Math.min(allNodes.length, 50); i++) {
                            const fw = parseInt(window.getComputedStyle(allNodes[i]).fontWeight) || 400;
                            if (fw > maxWeight) maxWeight = fw;
                        }

                        return {
                            hasH1: !!h1,
                            h1X: h1Box ? h1Box.x : null,
                            h1Y: h1Box ? h1Box.y : null,
                            hasOverflow: hasOverflow,
                            overflowDelta: Math.max(0, Math.max(bodyScrollWidth, docScrollWidth) - windowWidth),
                            hamburgerFound: hamburgerFound,
                            maxWeight: maxWeight
                        };
                    }''')
                    
                    page_data['viewports'][vp['name']] = {
                        'status': status_code,
                        'errors': console_errors,
                        'layout': page_eval
                    }
                except Exception as e:
                    page_data['viewports'][vp['name']] = {'error': str(e)}
                finally:
                    page.close()
                    
            results.append(page_data)
            print(f"Audited: {page_name}")
            
        browser.close()
        
    out_path = 'tools/audit_results_summary.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print(f"Comprehensive audit complete. Results saved to {out_path}.")

if __name__ == '__main__':
    run_comprehensive_audit()
