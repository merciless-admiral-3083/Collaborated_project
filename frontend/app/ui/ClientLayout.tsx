"use client";

import { useState } from "react";
import Link from "next/link";

export default function ClientLayout({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="flex h-screen bg-gray-50 dark:bg-black">

      {/* DESKTOP SIDEBAR */}
      <aside className="
        hidden md:flex flex-col w-64 shrink-0 
        border-r border-gray-200 dark:border-neutral-800
        bg-white dark:bg-neutral-900 px-6 py-8
      ">
        <div className="text-xl font-bold mb-8">🌍 SupplyChainAI</div>
        <nav className="flex flex-col gap-3 text-gray-700 dark:text-gray-300">
          <Link href="/dashboard" className="nav-item">📊 Dashboard</Link>
          <Link href="/heatmap" className="nav-item">🔎 Risk Analyzer</Link>
        </nav>
      </aside>

      {/* MOBILE TOP BAR */}
      <header className="
        md:hidden fixed top-0 left-0 right-0 z-50
        backdrop-blur-lg bg-white/80 dark:bg-black/40
        border-b border-gray-200 dark:border-neutral-800
        flex items-center justify-between px-4 py-3
      ">
        <button className="text-2xl" onClick={() => setOpen(!open)}>
          ☰
        </button>
        <div className="font-semibold text-lg">SupplyChainAI</div>
      </header>

      {/* MOBILE DRAWER */}
      <div
        className={`
          fixed top-0 left-0 h-full w-64
          bg-white dark:bg-neutral-900
          border-r border-gray-200 dark:border-neutral-800
          transition-transform duration-300 z-50
          ${open ? "translate-x-0" : "-translate-x-full"}
        `}
      >
        <div className="p-6">
          <div className="text-xl font-bold mb-8">🌍 SupplyChainAI</div>
          <nav className="flex flex-col gap-3 text-lg">
            <Link href="/dashboard" className="nav-item-mobile" onClick={() => setOpen(false)}>
              📊 Dashboard
            </Link>
            <Link href="/heatmap" className="nav-item-mobile" onClick={() => setOpen(false)}>
              🔎 Risk Analyzer
            </Link>
          </nav>
        </div>
      </div>

      {/* MAIN CONTENT */}
      <main className="flex-1 overflow-y-auto px-6 py-8 md:ml-0 mt-16 md:mt-0">
        {children}
      </main>
    </div>
  );
}
