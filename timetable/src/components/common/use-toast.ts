"use client";

import { useCallback, useEffect, useState } from "react";

export interface Toast {
  id: string;
  title: string;
  description?: string;
  variant?: "default" | "destructive" | "success";
  duration?: number;
}

type Message = { type: "add"; toast: Toast } | { type: "remove"; id: string };
const listeners = new Set<(m: Message) => void>();
let seq = 0;

export function toast(props: Omit<Toast, "id">) {
  const id = String(++seq);
  const t: Toast = { id, variant: "default", duration: 4000, ...props };
  listeners.forEach((l) => l({ type: "add", toast: t }));
  if (t.duration && t.duration > 0) {
    setTimeout(() => listeners.forEach((l) => l({ type: "remove", id })), t.duration);
  }
  return id;
}

export function dismiss(id: string) {
  listeners.forEach((l) => l({ type: "remove", id }));
}

export function useToast() {
  const [toasts, setToasts] = useState<Toast[]>([]);
  const handle = useCallback((m: Message) => {
    setToasts((ts) => {
      if (m.type === "add") return [...ts, m.toast];
      return ts.filter((x) => x.id !== m.id);
    });
  }, []);
  useEffect(() => {
    listeners.add(handle);
    return () => listeners.delete(handle);
  }, [handle]);
  return { toasts, dismiss };
}
