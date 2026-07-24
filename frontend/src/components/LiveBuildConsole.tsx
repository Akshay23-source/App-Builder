"use client";

import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Terminal, ShieldAlert, CheckCircle, Info, FileCode } from "lucide-react";
import { LogEntry } from "@/store/useBuildStore";

interface LiveBuildConsoleProps {
  logs: LogEntry[];
}

export default function LiveBuildConsole({ logs }: LiveBuildConsoleProps) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-950 p-4 font-mono text-xs shadow-2xl flex flex-col h-[480px]">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-3">
        <div className="flex items-center space-x-2">
          <Terminal className="w-4 h-4 text-indigo-400" />
          <span className="font-semibold text-slate-200">ForgeAI Agent Live Stream</span>
        </div>
        <div className="flex items-center space-x-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping" />
          <span className="text-[11px] text-slate-400">Live Socket</span>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto space-y-2 pr-2 custom-scrollbar">
        {logs.length === 0 ? (
          <div className="text-slate-600 text-center py-20 italic">
            Waiting for agent execution tasks...
          </div>
        ) : (
          <AnimatePresence>
            {logs.map((log) => (
              <motion.div
                key={log.id}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0 }}
                className="flex items-start space-x-2.5 py-1 border-b border-slate-900/60"
              >
                <span className="text-slate-600 text-[10px] whitespace-nowrap mt-0.5">
                  {new Date(log.timestamp).toLocaleTimeString()}
                </span>
                
                <span className="px-1.5 py-0.5 rounded text-[10px] uppercase font-bold bg-slate-800 text-indigo-300">
                  {log.agent_role}
                </span>

                <div className="flex-1 text-slate-300">
                  {log.event_type === "error" ? (
                    <span className="text-rose-400 flex items-center">
                      <ShieldAlert className="w-3.5 h-3.5 inline mr-1 text-rose-500" /> {log.message}
                    </span>
                  ) : log.event_type === "file_created" ? (
                    <span className="text-emerald-400 flex items-center">
                      <FileCode className="w-3.5 h-3.5 inline mr-1 text-emerald-400" /> {log.message}
                    </span>
                  ) : (
                    <span>{log.message}</span>
                  )}
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        )}
      </div>
    </div>
  );
}
