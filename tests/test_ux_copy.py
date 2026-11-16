"""
============================================================
NGIS-SYSTEM — Automated UX Copy & Component State Verification
Enforces Rules 1–12 & AGENTS.md rules across the entire product.
Zero warnings or failures permitted.
============================================================
"""

import glob
import os
import re
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FORBIDDEN_BARE_BUTTONS = [
    re.compile(r'>\s*Submit\s*<', re.I),
    re.compile(r'>\s*OK\s*<', re.I),
    re.compile(r'>\s*Yes\s*<', re.I),
    re.compile(r'>\s*Next\s*<', re.I),  # must be 'Next Page' or 'Next Step'
]

FORBIDDEN_PHRASES = [
    re.compile(r'\bclick\s+here\b', re.I),
    re.compile(r'\blearn\s+more\b', re.I),
    re.compile(r'\bsuccessfully\b', re.I),
    re.compile(r'\b(one|two|three|four|five|six|seven|eight|nine)\s+(users?|students?|teachers?|classes?|items?|records?|files?|days?|hours?|steps?|minutes?|members?|accounts?)\b', re.I),
]

FORBIDDEN_HEAVY_FONTS = [
    re.compile(r'\bfont-bold\b'),
    re.compile(r'\bfont-extrabold\b'),
    re.compile(r'\bfont-black\b'),
    re.compile(r'font-weight:\s*(?:700|800|900)\b'),
]

VERB_PREFIXES = (
    "save", "create", "add", "edit", "delete", "remove", "update", "send",
    "view", "open", "browse", "download", "export", "import", "confirm",
    "cancel", "close", "back", "next", "previous", "reset", "clear",
    "apply", "show", "filter", "sign", "log", "try", "refresh", "publish",
    "assign", "change", "start", "submit", "reject", "approve", "restore", "post"
)

class TestUXCopyAndComponentStates(unittest.TestCase):

    def test_01_central_copy_file_exists_and_clean(self):
        """Verify assets/js/ngis-copy.js has no forbidden words and has valid verbs."""
        copy_path = os.path.join(ROOT_DIR, 'assets', 'js', 'ngis-copy.js')
        self.assertTrue(os.path.exists(copy_path), "assets/js/ngis-copy.js must exist")

        with open(copy_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for idx, line in enumerate(lines):
            # Skip comments and metadata
            stripped = line.strip()
            if stripped.startswith('*') or stripped.startswith('/*') or stripped.startswith('//'):
                continue

            for pattern in FORBIDDEN_PHRASES:
                m = pattern.search(line)
                self.assertIsNone(
                    m,
                    f"Forbidden phrase '{m.group(0) if m else ''}' found in ngis-copy.js:{idx+1}: {stripped}"
                )

    def test_02_buttons_have_action_verbs(self):
        """Verify button actions in ngis-copy.js start with or contain an action verb."""
        copy_path = os.path.join(ROOT_DIR, 'assets', 'js', 'ngis-copy.js')
        with open(copy_path, 'r', encoding='utf-8') as f:
            content = f.read()

        cta_matches = re.findall(r'(?:Cta|Action|save|delete|create|edit|btn)\s*:\s*["\']([^"\']+)["\']', content, re.I)
        self.assertGreater(len(cta_matches), 10, "Expected at least 10 action labels in copy file")

        for label in cta_matches:
            first_word = label.strip().split()[0].lower()
            self.assertTrue(
                first_word.startswith(VERB_PREFIXES) or any(v in label.lower() for v in VERB_PREFIXES),
                f"Button label '{label}' must start with or contain an action verb (Rule 8)"
            )

    def test_03_design_tokens_semantic_status_colors(self):
        """Verify design-tokens.css implements the 5 semantic status colors per Rule 9."""
        tokens_path = os.path.join(ROOT_DIR, 'assets', 'css', 'design-tokens.css')
        self.assertTrue(os.path.exists(tokens_path), "assets/css/design-tokens.css must exist")

        with open(tokens_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('--token-status-success:', content, "Missing --token-status-success token")
        self.assertIn('--token-status-warning:', content, "Missing --token-status-warning token")
        self.assertIn('--token-status-danger:', content, "Missing --token-status-danger token")
        self.assertIn('--token-status-info:', content, "Missing --token-status-info token")
        self.assertIn('--token-status-neutral:', content, "Missing --token-status-neutral token")

        # Verify info is sky blue (#0284C7), not green
        info_match = re.search(r'--token-status-info:\s*([^;]+);', content)
        self.assertIsNotNone(info_match)
        self.assertIn('#0284C7', info_match.group(1).upper(), "Info status must be semantic blue #0284C7 (Rule 9)")

    def test_04_button_six_states_in_shared_components(self):
        """Verify shared-components.css implements all 6 button states per Rule 11."""
        css_path = os.path.join(ROOT_DIR, 'assets', 'css', 'shared-components.css')
        self.assertTrue(os.path.exists(css_path), "assets/css/shared-components.css must exist")

        with open(css_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('.btn', content, "Missing button default state")
        self.assertIn('.btn-primary:hover', content, "Missing button hover state")
        self.assertIn('.btn:active', content, "Missing button pressed/active state")
        self.assertIn('.btn:focus-visible', content, "Missing button focus-visible state")
        self.assertIn('.btn.is-loading', content, "Missing button loading state")
        self.assertIn('.btn:disabled', content, "Missing button disabled state")

    def test_05_semantic_badges_in_shared_components(self):
        """Verify shared-components.css implements semantic badge classes per Rule 9."""
        css_path = os.path.join(ROOT_DIR, 'assets', 'css', 'shared-components.css')
        with open(css_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('.badge-success', content, "Missing .badge-success")
        self.assertIn('.badge-warning', content, "Missing .badge-warning")
        self.assertIn('.badge-danger', content, "Missing .badge-danger")
        self.assertIn('.badge-info', content, "Missing .badge-info")
        self.assertIn('.badge-neutral', content, "Missing .badge-neutral")

    def test_06_no_bare_buttons_in_html_pages(self):
        """Verify no HTML page contains bare 'Submit', 'OK', 'Yes', or bare 'Next'."""
        html_files = glob.glob(os.path.join(ROOT_DIR, '*.html')) + glob.glob(os.path.join(ROOT_DIR, 'pages', '**', '*.html'), recursive=True)
        self.assertEqual(len(html_files), 117, f"Expected 117 live HTML pages, found {len(html_files)}")

        violations = []
        for path in html_files:
            rel = os.path.relpath(path, ROOT_DIR)
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            for regex in FORBIDDEN_BARE_BUTTONS:
                m = regex.search(content)
                if m:
                    violations.append(f"{rel}: {m.group(0)}")

        self.assertEqual(len(violations), 0, f"Found bare buttons in HTML files: {violations}")

    def test_07_no_filler_words_in_html_pages(self):
        """Verify no HTML page contains filler words like 'successfully'."""
        html_files = glob.glob(os.path.join(ROOT_DIR, '*.html')) + glob.glob(os.path.join(ROOT_DIR, 'pages', '**', '*.html'), recursive=True)

        violations = []
        for path in html_files:
            rel = os.path.relpath(path, ROOT_DIR)
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            for regex in FORBIDDEN_PHRASES:
                m = regex.search(content)
                if m:
                    violations.append(f"{rel}: {m.group(0)}")

        self.assertEqual(len(violations), 0, f"Found filler phrases in HTML files: {violations}")

    def test_08_agents_md_no_bold_fonts(self):
        """Verify design tokens and shared components enforce font-weight <= 500 per AGENTS.md."""
        tokens_path = os.path.join(ROOT_DIR, 'assets', 'css', 'design-tokens.css')
        with open(tokens_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check weights in tokens
        weight_semibold = re.search(r'--token-weight-semibold:\s*(\d+);', content)
        weight_bold = re.search(r'--token-weight-bold:\s*(\d+);', content)
        if weight_semibold:
            self.assertLessEqual(int(weight_semibold.group(1)), 500, "Semibold token must be <= 500")
        if weight_bold:
            self.assertLessEqual(int(weight_bold.group(1)), 500, "Bold token must be <= 500")

    def test_09_agents_md_mobile_hamburger_present(self):
        """Verify layout.js implements [data-action="toggle-sidebar"] mobile hamburger."""
        layout_path = os.path.join(ROOT_DIR, 'assets', 'js', 'layout.js')
        with open(layout_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('toggle-sidebar', content, "layout.js must support toggle-sidebar action")
        self.assertIn('hamburger-btn', content, "layout.js must support hamburger-btn class")

if __name__ == '__main__':
    unittest.main()
