// Minimal hash router. Routes map a path to an async render(ctx) -> Node.
// Supports a not-found fallback and an onChange hook (for nav highlighting).

const routes = new Map();
let notFound = null;
let onChange = null;
let outlet = null;

export function defineRoutes(map) { for (const [k, v] of Object.entries(map)) routes.set(k, v); }
export function setNotFound(fn) { notFound = fn; }
export function setOutlet(node) { outlet = node; }
export function setOnChange(fn) { onChange = fn; }

export function currentPath() {
  return (location.hash.replace(/^#/, "") || "/").split("?")[0];
}

export function navigate(path) {
  if (currentPath() === path) { resolve(); return; }
  location.hash = path;
}

async function resolve() {
  const path = currentPath();
  const render = routes.get(path) || notFound;
  if (!render || !outlet) return;
  outlet.classList.add("view-leaving");
  const node = await render({ path });
  outlet.replaceChildren(node);
  outlet.classList.remove("view-leaving");
  outlet.scrollTop = 0;
  window.scrollTo(0, 0);
  if (onChange) onChange(path);
}

export function startRouter() {
  window.addEventListener("hashchange", resolve);
  resolve();
}
