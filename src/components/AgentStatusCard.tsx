"use client";

import React from "react";
import { motion } from "framer-motion";
import { Brain, Search, Code, Wrench, FileText, CheckCircle2, Loader2 } from "lucide-react";
import { Card, Badge } from "@/components/ui/primitives";

interface AgentStatusCardProps {
  role: "planner" | "research" | "codegen" | "debug" | "docs";
  name: string;
  provider: string;
  status: "idle" | "running" | "completed" | "failed";
  description: string;
}

const roleIcons = {
  planner: Brain,
  research: Search,
  codegen: Code,
  debug: Wrench,
  docs: FileText,
};

const roleColors = {
  planner: "from-purple-500 to-indigo-600",
  research: "from-blue-500 to-cyan-500",
  codegen: "from-emerald-500 to-teal-600",
  debug: "from-amber-500 to-orange-600",
  docs: "from-pink-500 to-rose-600",
};

export default function AgentStatusCard({ role, name, provider, status, description }: AgentStatusCardProps) {
  const Icon = roleIcons[role] || Brain;
  const gradient = roleColors[role];

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <Card className={`p-4 transition-all duration-300 ${status === "running" ? "border-indigo-500/50 shadow-indigo-500/10 shadow-lg" : ""}`}>
        <div className="flex items-start justify-between">
          <div className="flex items-center space-x-3">
            <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${gradient} flex items-center justify-center text-white shadow-md`}>
              <Icon className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h4 className="font-semibold text-white text-sm">{name}</h4>
                <Badge variant="slate" className="text-[10px] uppercase font-mono">{provider}</Badge>
              </div>
              <p className="text-xs text-slate-400 mt-0.5">{description}</p>
            </div>
          </div>

          <div>
            {status === "running" && (
              <span className="flex items-center text-xs text-indigo-400 font-medium bg-indigo-500/10 px-2.5 py-1 rounded-lg border border-indigo-500/20">
                <Loader2 className="w-3.5 h-3.5 animate-spin mr-1.5" /> Thinking...
              </span>
            )}
            {status === "completed" && (
              <span className="flex items-center text-xs text-emerald-400 font-medium bg-emerald-500/10 px-2.5 py-1 rounded-lg border border-emerald-500/20">
                <CheckCircle2 className="w-3.5 h-3.5 mr-1.5" /> Done
              </span>
            )}
            {status === "idle" && (
              <span className="text-xs text-slate-500 bg-slate-800/60 px-2.5 py-1 rounded-lg border border-slate-700">
                Standby
              </span>
            )}
          </div>
        </div>
      </Card>
    </motion.div>
  );
}
