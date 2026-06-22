// Front-end session store (mock auth). Holds the signed-in role/user.
// Replace with real JWT/session handling when the backend lands.
import { accounts } from "./mockData.js";

const KEY = "ngis:session";

const state = {
  user: null,        // current account object
  role: null,        // current role string
  activeChild: "u-stu-1", // for parent portal
};

const listeners = new Set();
export function subscribe(fn) { listeners.add(fn); return () => listeners.delete(fn); }
function emit() { listeners.forEach((fn) => fn(state)); }

export function getState() { return state; }

export function login(role) {
  state.user = accounts[role];
  state.role = role;
  localStorage.setItem(KEY, role);
  emit();
}

export function logout() {
  state.user = null; state.role = null;
  localStorage.removeItem(KEY);
}

export function restore() {
  const role = localStorage.getItem(KEY);
  if (role && accounts[role]) { state.user = accounts[role]; state.role = role; return true; }
  return false;
}

export function setActiveChild(id) { state.activeChild = id; emit(); }
