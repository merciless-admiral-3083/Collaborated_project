'use client'

import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="w-full flex items-center justify-between px-6 py-4 bg-gray-900 text-white border-b border-gray-700">
      <Link href="/" className="text-xl font-bold">
        SupplyChainAI
      </Link>

      <div className="flex gap-4">
        <Link href="/dashboard" className="hover:text-blue-400">Dashboard</Link>
        <Link href="/login" className="hover:text-blue-400">Login</Link>
        <Link href="/register" className="hover:text-blue-400">Register</Link>
      </div>
    </nav>
  );
}
