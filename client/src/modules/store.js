/* Tiny reactive store — pub/sub over a plain object. No framework. */

function createStore(initial) {
  let state = { ...initial };
  const subs = new Set();
  return {
    get: (k) => (k ? state[k] : state),
    set(patch) {
      state = { ...state, ...patch };
      subs.forEach((fn) => fn(state));
    },
    subscribe(fn) { subs.add(fn); return () => subs.delete(fn); },
  };
}

export const ui = createStore({
  sidebarCollapsed: localStorage.getItem('ngis-sidebar') === '1',
  mobileOpen: false,
});

export function setSidebarCollapsed(v) {
  localStorage.setItem('ngis-sidebar', v ? '1' : '0');
  ui.set({ sidebarCollapsed: v });
}
