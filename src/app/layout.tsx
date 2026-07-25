import "./globals.css";
import type { Metadata } from "next";
import Link from "next/link";
import { Cpu, Sparkles, Layers, User } from "lucide-react";

export const metadata: Metadata = {
  title: "ForgeAI — Multi-Agent AI Website Builder",
  description: "Turn a one-line idea into a live, running Next.js application powered by autonomous AI agent graphs.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-[#080c14] text-slate-100 flex flex-col selection:bg-indigo-500 selection:text-white">
        <header className="sticky top-0 z-50 border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-xl">
          <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
            <Link href="/" className="flex items-center space-x-3 group">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-purple-500 flex items-center justify-center text-white shadow-lg shadow-indigo-500/25 group-hover:scale-105 transition-transform duration-200">
                <Cpu className="w-5 h-5" />
              </div>
              <div className="flex flex-col">
                <span className="font-bold text-lg tracking-tight text-white flex items-center">
                  Forge<span className="text-indigo-400">AI</span>
                  <span className="ml-2 text-[10px] font-semibold px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/30 uppercase">v1.0</span>
                </span>
              </div>
            </Link>

            <nav className="flex items-center space-x-6 text-sm font-medium">
              <Link href="/dashboard" className="text-slate-300 hover:text-white transition flex items-center space-x-1.5">
                <Layers className="w-4 h-4 text-indigo-400" />
                <span>Projects</span>
              </Link>
              <Link href="/dashboard/new" className="text-slate-300 hover:text-white transition flex items-center space-x-1.5">
                <Sparkles className="w-4 h-4 text-purple-400" />
                <span>New Build</span>
              </Link>
              <Link
                href="/login"
                className="px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-200 transition flex items-center space-x-2 text-xs font-semibold"
              >
                <User className="w-3.5 h-3.5 text-indigo-400" />
                <span>Account Login</span>
              </Link>
            </nav>
          </div>
        </header>

        <main className="flex-1">{children}</main>

        <footer className="border-t border-slate-800/80 bg-slate-950 py-8 text-center text-xs text-slate-500">
          <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between">
            <p>© 2026 ForgeAI Platform. Multi-Agent DAG Architecture.</p>
            <div className="flex space-x-4 mt-4 md:mt-0">
              <span>OpenAI (CodeGen)</span>
              <span>•</span>
              <span>Anthropic (Planner/Docs)</span>
              <span>•</span>
              <span>DeepSeek (Fallback)</span>
              <span>•</span>
              <span>Gemini (Research)</span>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
