"use client";

import React, { useState } from "react";
import { Sparkles, ArrowRight, Lightbulb } from "lucide-react";
import { Button } from "@/components/ui/primitives";

interface PromptInputProps {
  onSubmit: (prompt: str) => void;
  isLoading?: boolean;
}

const PRESET_IDEAS = [
  "A SaaS landing page for an AI video editor with pricing tables and dark glassmorphic hero",
  "A developer portfolio with interactive project cards, skill badges, and dynamic contact form",
  "A real-time crypto analytics dashboard with modern dark theme and interactive chart components",
];

export default function PromptInput({ onSubmit, isLoading }: PromptInputProps) {
  const [prompt, setPrompt] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (prompt.trim()) {
      onSubmit(prompt);
    }
  };

  return (
    <div className="w-full max-w-3xl mx-auto space-y-4">
      <form onSubmit={handleSubmit} className="relative group">
        <div className="absolute -inset-0.5 bg-gradient-to-r from-indigo-500 via-purple-500 to-emerald-500 rounded-3xl blur opacity-30 group-hover:opacity-60 transition duration-500" />
        
        <div className="relative rounded-2xl bg-slate-900 border border-slate-800 p-3 shadow-2xl flex flex-col md:flex-row items-stretch md:items-center space-y-3 md:space-y-0 md:space-x-3">
          <div className="pl-3 text-indigo-400">
            <Sparkles className="w-6 h-6 animate-pulse" />
          </div>

          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Describe your website idea in one line... (e.g. A sleek dark mode portfolio for a Web3 designer)"
            rows={2}
            className="w-full bg-transparent text-white placeholder-slate-500 focus:outline-none resize-none text-sm leading-relaxed"
          />

          <Button
            type="submit"
            disabled={isLoading || !prompt.trim()}
            className="md:self-end h-12 px-6 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-xl flex items-center justify-center space-x-2 whitespace-nowrap shadow-lg shadow-indigo-600/30"
          >
            <span>{isLoading ? "Starting Build..." : "Forge Website"}</span>
            <ArrowRight className="w-4 h-4" />
          </Button>
        </div>
      </form>

      <div className="flex flex-wrap items-center justify-center gap-2 pt-2 text-xs text-slate-400">
        <span className="flex items-center text-slate-500 mr-1">
          <Lightbulb className="w-3.5 h-3.5 mr-1 text-amber-400" /> Try an example:
        </span>
        {PRESET_IDEAS.map((idea, idx) => (
          <button
            key={idx}
            type="button"
            onClick={() => setPrompt(idea)}
            className="bg-slate-900/80 hover:bg-slate-800 border border-slate-800 hover:border-indigo-500/40 text-slate-300 px-3 py-1.5 rounded-lg transition duration-200 text-[11px] truncate max-w-xs"
          >
            {idea}
          </button>
        ))}
      </div>
    </div>
  );
}
