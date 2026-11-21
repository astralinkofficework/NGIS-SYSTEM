import os
import glob
from playwright.sync_api import sync_playwright

html_files = glob.glob("pages/**/*.html", recursive=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    anomalies = []
    
    for f in html_files:
        url_path = f.replace("\\", "/")
        url = f"http://127.0.0.1:3000/{url_path}"
        
        for w, vp in [(1440, "desktop"), (375, "mobile")]:
            page = browser.new_page(viewport={"width": w, "height": 800})
            try:
                page.goto(url, timeout=10000)
                page.wait_for_timeout(400)
                
                res = page.evaluate("""() => {
                    const nav = document.getElementById('ngisGlobalNavbar');
                    if (!nav) return { hasNav: false };
                    const r = nav.getBoundingClientRect();
                    
                    // Check what is above nav
                    let aboveNodes = [];
                    let el = nav.previousElementSibling;
                    while (el) {
                        const er = el.getBoundingClientRect();
                        if (er.height > 0 && window.getComputedStyle(el).display !== 'none') {
                            aboveNodes.push({ tag: el.tagName, id: el.id, class: el.className, height: er.height, top: er.top });
                        }
                        el = el.previousElementSibling;
                    }
                    
                    // Check if parent has padding-top or margin-top
                    const p = nav.parentElement;
                    const pStyle = p ? window.getComputedStyle(p) : null;
                    
                    return {
                        hasNav: true,
                        top: r.top,
                        y: r.y,
                        height: r.height,
                        aboveNodes: aboveNodes,
                        parentTag: p ? p.tagName : null,
                        parentId: p ? p.id : null,
                        parentClass: p ? p.className : null,
                        parentPadTop: pStyle ? pStyle.paddingTop : null,
                        parentMarginTop: pStyle ? pStyle.marginTop : null,
                        navStyleTop: window.getComputedStyle(nav).top,
                        navPadTop: window.getComputedStyle(nav).paddingTop,
                        navMarginTop: window.getComputedStyle(nav).marginTop,
                        bodyPadTop: window.getComputedStyle(document.body).paddingTop,
                        bodyMarginTop: window.getComputedStyle(document.body).marginTop
                    };
                }""")
                
                if res.get("hasNav"):
                    if res["top"] > 1 or res.get("aboveNodes") or (res["parentPadTop"] and res["parentPadTop"] != "0px"):
                        anomalies.append({
                            "file": f,
                            "vp": vp,
                            "res": res
                        })
                else:
                    anomalies.append({
                        "file": f,
                        "vp": vp,
                        "error": "No #ngisGlobalNavbar found"
                    })
            except Exception as e:
                anomalies.append({
                    "file": f,
                    "vp": vp,
                    "error": str(e)
                })
            finally:
                page.close()
                
    browser.close()

print(f"Total files checked: {len(html_files)}")
print(f"Anomalies found: {len(anomalies)}")
for a in anomalies[:30]:
    print("---", a["file"], a["vp"])
    print("   ", a)
