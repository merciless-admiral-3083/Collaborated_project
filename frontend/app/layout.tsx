import "./globals.css";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";


import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "SupplyChainAI",
  description: "AI powered supply chain risk analyzer",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-black text-white">
        <Navbar />
        <main className="min-h-screen px-6 py-10">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
