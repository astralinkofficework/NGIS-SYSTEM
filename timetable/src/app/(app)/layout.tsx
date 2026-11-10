"use client";

import { useState } from "react";
import Link from "next/link";
import { Menu, School, Users, Calendar, BarChart3, Clock, Print, Settings } from "lucide-react";

const NAV: { href: string; label: string; icon: React.ComponentType<any> }[] = [
  { href: "/schedule", label: "កាលវិភាគ", icon: Calendar },
  { href: "/assign", label: "ការប្រើគ្រូ", icon: BarChart3 },
  { href: "/teachers", label: "គ្រូរូបរាង", icon: Users },
  { href: "/classes", label: "ថ្នាក់", icon: School },
  { href: "/subjects", label: "មុខវិជ្ជា", icon: BarChart3 },
  { href: "/overtime", label: "ម៉ោលចំណងជើង", icon: Clock },
  { href: "/now", label: "បច្ចុប្បន្ន", icon: Clock },
  { href: "/print", label: "បោះពុម្ព", icon: Print },
];

export default function AppLayout({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex flex-col h-full min-h-[100dvh] surface-raised">
      <header className="sticky top-0 z-40 border-b border-hairline bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/[80]">
        <div className="flex items-center justify-between gap-2 px-4 sm:px-6 h-12">
          <button
            type="button"
            className="hamburger-btn mobile-hamburger-btn inline-flex items-center justify-center w-10 h-10 rounded-lg border border-hairline text-slate-600 hover:bg-slate-50 active:scale-95 transition-all md:hidden"
            data-action="toggle-sidebar"
            aria-label="Open menu"
            aria-expanded={sidebarOpen}
            title="Open navigation"
            onClick={() => setSidebarOpen((o) => !o)}
          >
            <Menu className="w-5 h-5" />
          </button>

          <Link href="/schedule" className="flex items-center gap-2.5 no-underline">
            <School className="w-5 h-5 text-amber-600" aria-hidden="true" />
            <span className="font-medium text-sm tracking-tight text-slate-800">កាលវិភាគសាលា</span>
          </Link>

          <div className="ml-auto flex items-center gap-3">
            <button type="button" className="text-slate-400 hover:text-slate-600 p-1.5 rounded-lg hover:bg-slate-100 active:scale-95 transition-all" aria-label="Settings">
              <Settings className="w-4 h-4" />
            </button>
          </div>
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden">
        <aside
          className="fixed inset-y-0 left-0 z-50 w-64 border-r border-hairline bg-white transform -translate-x-full transition-transform duration-300 ease-in-out sm:relative sm:translate-x-0 sm:static sm:inset-0 sm:border-0 sm:flex sm:flex-col"
          aria-label="Navigation sidebar"
        >
          <div className="flex flex-col h-full">
            <div className="p-4 border-b border-hairline">
              <Link href="/schedule" className="flex items-center gap-2.5 no-underline">
                <School className="w-5 h-5 text-amber-600" aria-hidden="true" />
                <span className="font-medium text-sm">កាលវិភាគសាលា</span>
              </Link>
            </div>
            <nav className="flex-1 overflow-y-auto py-3 space-y-1">
              {NAV.map((item) => {
                const Icon = item.icon;
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className="flex items-center gap-3 rounded-xl px-4 py-2.5 text-sm font-medium text-slate-600 hover:bg-slate-50 hover:text-slate-800 active:scale-95 transition-all no-underline"
                  >
                    <Icon className="w-4 h-4" aria-hidden="true" />
                    {item.label}
                  </Link>
                );
              })}
            </nav>
            <div className="p-4 border-t border-hairline text-xs text-slate-500 font-medium">
              ឆ្នាំសិក្សា 2026–2027
            </div>
          </div>

          {sidebarOpen && (
            <div
              className="fixed inset-0 z-40 bg-black/40 backdrop-blur-sm sm:hidden"
              aria-hidden="true"
              onClick={() => setSidebarOpen(false)}
            />
          )}
        </aside>

        <main id="main-content" className="flex-1 overflow-y-auto h-full w-full">
          <div className="px-4 sm:px-6 py-6">{children}</div>
        </main>
      </div>

      {sidebarOpen && (
        <div className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm md:hidden" aria-hidden="true" onClick={() => setSidebarOpen(false)} />
      )}
    </div>
  );
}
