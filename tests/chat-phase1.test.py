import re
import urllib.request

def test_chat_html_response():
    url = "http://127.0.0.1:3000/pages/shared/chat.html"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=5) as res:
        assert res.status == 200, f"Expected status 200, got {res.status}"
        body = res.read().decode("utf-8")
        assert 'id="convPanel"' in body, "Missing #convPanel in chat.html"
        assert 'id="chatWin"' in body, "Missing #chatWin in chat.html"
        assert 'id="backBtn"' in body, "Missing #backBtn in chat.html"
        assert 'id="peopleSearch"' in body, "Missing #peopleSearch in chat.html"
        assert 'id="peopleResults"' in body, "Missing #peopleResults in chat.html"
        assert 'assets/css/chat.css' in body, "Missing chat.css link"
        assert 'assets/js/chat.js' in body, "Missing chat.js script"
        assert 'var PEOPLE = [' not in body, "Found unexpected duplicate inline script in chat.html"
        print("[PASS] chat.html DOM structure and script integration verified.")

def test_chat_css_responsive_and_animations():
    with open("assets/css/chat.css", "r", encoding="utf-8") as f:
        css = f.read()

    # Desktop
    assert "@media (min-width: 1025px)" in css, "Missing desktop breakpoint min-width: 1025px"
    # Tablet
    assert "@media (min-width: 769px) and (max-width: 1024px)" in css, "Missing tablet breakpoint 769px-1024px"
    # Mobile
    assert "@media (max-width: 768px)" in css, "Missing mobile breakpoint max-width: 768px"

    # Mobile slide transitions
    assert ".conv-panel.hidden-mobile" in css, "Missing .conv-panel.hidden-mobile rule"
    assert ".chat-win.show-mobile" in css, "Missing .chat-win.show-mobile rule"
    assert "body[data-page=\"chat\"].chat-open .bottomnav" in css, "Missing bottom dock auto-hide on chat-open"

    # Hamburger hidden on desktop
    assert ".hamburger-btn {\n  display: none !important;" in css, "Hamburger button must be hidden on desktop"

    # Modern Animations
    assert "@keyframes sDotPulse" in css, "Missing @keyframes sDotPulse"
    assert "@keyframes msgPopIn" in css, "Missing @keyframes msgPopIn"
    assert "linear-gradient(135deg, var(--primary) 0%, #0d9488 100%)" in css, "Missing outgoing bubble gradient"
    print("[PASS] chat.css 3-tier responsive rules and modern animations verified.")

def test_chat_js_controller():
    with open("assets/js/chat.js", "r", encoding="utf-8") as f:
        js = f.read()

    assert "PEOPLE = [" in js, "Missing PEOPLE directory in chat.js"
    assert "window.innerWidth <= 768" in js, "Missing 768px mobile check in chat.js"
    assert "document.body.classList.add(\"chat-open\");" in js, "Missing chat-open on openConversation"
    assert "document.body.classList.remove(\"chat-open\");" in js, "Missing chat-open removal on backBtn"
    assert 'window.addEventListener("resize"' in js, "Missing resize event handler in chat.js"
    assert "getDemoReply" in js, "Missing getDemoReply in chat.js"
    print("[PASS] chat.js controller logic, responsive handling, and demo reply verified.")

if __name__ == "__main__":
    test_chat_html_response()
    test_chat_css_responsive_and_animations()
    test_chat_js_controller()
    print("ALL PHASE 1 DIRECT MESSAGES TESTS PASSED!")
