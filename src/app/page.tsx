"use client";

import React from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Brain, Code, Search, Wrench, FileText, ArrowRight, Zap, CheckCircle } from "lucide-react";
import PromptInput from "@/components/PromptInput";
import { Card, Button } from "@/components/ui/primitives";

export default function LandingPage() {
  const router = useRouter();

  const handlePromptSubmit = (prompt: string) => {
    router.push(`/dashboard/new?prompt=${encodeURIComponent(prompt)}`);
  };

  return (
    <div className="space-y-24 py-16 px-6 max-w-7xl mx-auto">
      {/* Hero Section */}
      <section className="text-center space-y-8 relative">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-indigo-500/15 rounded-full blur-3xl pointer-events-none" />

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 text-xs font-semibold"
        >
          <Zap className="w-3.5 h-3.5 fill-indigo-400" />
          <span>Autonomous Multi-Agent Web Application Builder</span>
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="text-5xl md:text-7xl font-extrabold tracking-tight text-white max-w-4xl mx-auto leading-tight"
        >
          Turn a One-Line Idea into a <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-emerald-400">Running Website</span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="text-slate-400 text-lg md:text-xl max-w-2xl mx-auto font-normal leading-relaxed"
        >
          ForgeAI deploys 5 specialized AI agents working concurrently in a DAG task graph to plan, research, code, sandbox-debug, and document production Next.js apps.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="pt-4"
        >
          <PromptInput onSubmit={handlePromptSubmit} />
        </motion.div>
      </section>

      {/* Agent Network Graph Explanation */}
      <section className="space-y-12">
        <div className="text-center space-y-3">
          <h2 className="text-3xl font-bold text-white">Multi-Agent Task Graph Architecture</h2>
          <p className="text-slate-400 text-sm max-w-lg mx-auto">
            Not a linear chat thread. A parallel DAG workflow with automatic sandbox build repairs.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          {[
            { role: "Planner", model: "Claude 3.5", desc: "Decomposes prompts into structured task DAGs", icon: Brain, color: "text-purple-400" },
            { role: "Research", model: "Gemini + Tavily", desc: "Searches live benchmarks for UI/UX tokens", icon: Search, color: "text-blue-400" },
            { role: "CodeGen", model: "GPT-4o / DeepSeek", desc: "Emits complete Next.js 14 file tree JSON", icon: Code, color: "text-emerald-400" },
            { role: "Debug", model: "Node Sandbox", desc: "Executes npm build, repairs errors (max 3 retries)", icon: Wrench, color: "text-amber-400" },
            { role: "Docs", model: "Claude 3.5", desc: "Generates README and component specs", icon: FileText, color: "text-pink-400" },
          ].map((agent, idx) => (
            <Card key={idx} className="p-5 hover:border-indigo-500/40 transition duration-300">
              <div className="space-y-3">
                <div className={`w-10 h-10 rounded-xl bg-slate-800 flex items-center justify-center ${agent.color}`}>
                  <agent.icon className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-semibold text-white text-base">{agent.role} Agent</h3>
                  <span className="text-[11px] font-mono text-indigo-400">{agent.model}</span>
                </div>
                <p className="text-xs text-slate-400 leading-relaxed">{agent.desc}</p>
              </div>
            </Card>
          ))}
        </div>
      </section>

      {/* Features Grid */}
      <section className="rounded-3xl border border-slate-800 bg-gradient-to-b from-slate-900/80 to-slate-950 p-10 space-y-8">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center border-b border-slate-800 pb-6">
          <div>
            <h3 className="text-2xl font-bold text-white">Why ForgeAI stands apart</h3>
            <p className="text-slate-400 text-sm mt-1">Real file tree generation, isolated sandbox verification, live WebSocket streaming.</p>
          </div>
          <Link href="/dashboard/new" className="mt-4 md:mt-0">
            <Button className="flex items-center space-x-2">
              <span>Try ForgeAI Now</span>
              <ArrowRight className="w-4 h-4" />
            </Button>
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm text-slate-300">
          <div className="flex items-start space-x-3">
            <CheckCircle className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
            <div>
              <strong className="text-white block font-semibold mb-1">Adapter Pattern AI Layer</strong>
              Swappable provider router supporting OpenAI, Anthropic, DeepSeek, Gemini, and Tavily with automatic failure fallbacks.
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <CheckCircle className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
            <div>
              <strong className="text-white block font-semibold mb-1">Sandbox Build Repair Loop</strong>
              Debug Agent actually compiles the code inside an isolated environment and iteratively repairs errors.
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <CheckCircle className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
            <div>
              <strong className="text-white block font-semibold mb-1">Real-time WebSocket Console</strong>
              Streamed agent log telemetry, active thinking indicators, and animated task DAG execution.
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
