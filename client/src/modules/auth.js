/* Mock auth — front-end only. Demonstrates the session shape the real API
   (§8) returns. No real tokens; persists chosen demo role to localStorage. */
import { USERS } from '../data/mock.js';

const KEY = 'ngis-session';

export function getSession() {
  const raw = localStorage.getItem(KEY);
  if (!raw) return null;
  try { return JSON.parse(raw); } catch { return null; }
}

export function login(roleKey) {
  const user = USERS[roleKey];
  if (!user) throw new Error('Unknown role');
  const session = { user, loginAt: Date.now() };
  localStorage.setItem(KEY, JSON.stringify(session));
  return session;
}

export function logout() { localStorage.removeItem(KEY); }
export function isAuthed() { return !!getSession(); }
export function currentUser() { return getSession()?.user || null; }
