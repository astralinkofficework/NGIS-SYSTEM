/* Hash router — framework-free, works from file:// and any static host.
   Routes are exact-match against the hash path. Supports a NotFound. */

const routes = new Map();
let notFound = () => '<div class="state"><h4>404 — Page not found</h4></div>';
let onNavigate = () => {};

export function route(path, handler) { routes.set(path, handler); }
export function setNotFound(fn) { notFound = fn; }
export function setOnNavigate(fn) { onNavigate = fn; }

export function currentPath() {
  const h = location.hash.replace(/^#/, '');
  return h.split('?')[0] || '/';
}

export function navigate(path) {
  if (currentPath() === path) { render(); return; }
  location.hash = path;
}

export function getHandler(path) { return routes.get(path) || notFound; }

export function render() {
  const path = currentPath();
  onNavigate(path);
}

export function startRouter() {
  window.addEventListener('hashchange', render);
  window.addEventListener('load', render);
  if (document.readyState !== 'loading') render();
}
