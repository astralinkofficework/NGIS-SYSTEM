const KEY = "ngis:theme";

export function initTheme() {
  const saved = localStorage.getItem(KEY);
  const sys = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  setTheme(saved || sys, false);
}

export function getTheme() {
  return document.documentElement.getAttribute("data-theme") || "light";
}

export function setTheme(theme, persist = true) {
  document.documentElement.setAttribute("data-theme", theme);
  if (persist) localStorage.setItem(KEY, theme);
  window.dispatchEvent(new CustomEvent("ngis:theme", { detail: theme }));
}

export function toggleTheme() {
  setTheme(getTheme() === "dark" ? "light" : "dark");
}
