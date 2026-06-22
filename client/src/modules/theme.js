/* Theme — light/dark with persistence + system preference fallback. */
const KEY = 'ngis-theme';

export function getTheme() {
  return localStorage.getItem(KEY) ||
    (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
}

export function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  const meta = document.querySelector('meta[name="theme-color"]');
  if (meta) meta.content = theme === 'dark' ? '#0B1120' : '#FFFFFF';
}

export function setTheme(theme) {
  localStorage.setItem(KEY, theme);
  applyTheme(theme);
}

export function toggleTheme() {
  const next = getTheme() === 'dark' ? 'light' : 'dark';
  setTheme(next);
  return next;
}

export function initTheme() { applyTheme(getTheme()); }
