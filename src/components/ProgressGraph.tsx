"use client";

import React from "react";
import { motion } from "framer-motion";
import { CheckCircle2, Clock, Loader2, AlertCircle } from "lucide-react";
import { TaskNodeData } from "@/store/useBuildStore";

interface ProgressGraphProps {
  tasks: TaskNodeData[];
}

export default function ProgressGraph({ tasks }: ProgressGraphProps) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/60 backdrop-blur-xl p-5 shadow-xl">
      <h3 className="text-sm font-semibold text-white mb-4 flex items-center">
        <span className="w-2 h-2 rounded-full bg-indigo-500 mr-2" /> Execution Task DAG
      </h3>

      <div className="relative pl-6 space-y-6 before:absolute before:left-3 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-800">
        {tasks.map((task, idx) => {
          const isSuccess = task.status === "SUCCESS";
          const isRunning = task.status === "RUNNING";
          const isFailed = task.status === "FAILED";

          return (
            <motion.div
              key={task.id || idx}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.1 }}
              className="relative flex items-start justify-between"
            >
              {/* Node Bullet */}
              <div
                className={`absolute -left-[31px] top-0.5 w-6 h-6 rounded-full flex items-center justify-center border text-xs ${
                  isSuccess
                    ? "bg-emerald-500/20 border-emerald-500 text-emerald-400"
                    : isRunning
                    ? "bg-indigo-500/20 border-indigo-500 text-indigo-400 animate-pulse"
                    : isFailed
                    ? "bg-rose-500/20 border-rose-500 text-rose-400"
                    : "bg-slate-900 border-slate-700 text-slate-500"
                }`}
              >
                {isSuccess ? (
                  <CheckCircle2 className="w-3.5 h-3.5" />
                ) : isRunning ? (
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                ) : isFailed ? (
                  <AlertCircle className="w-3.5 h-3.5" />
                ) : (
                  <Clock className="w-3.5 h-3.5" />
                )}
              </div>

              <div>
                <h4 className={`text-xs font-semibold ${isSuccess ? "text-slate-200" : isRunning ? "text-indigo-400" : "text-slate-400"}`}>
                  {task.name}
                </h4>
                <p className="text-[11px] text-slate-500 capitalize">
                  Agent: {task.agent_role} {task.dependencies?.length > 0 && `(After ${task.dependencies.join(", ")})`}
                </p>
              </div>

              <span className={`text-[10px] font-mono font-semibold px-2 py-0.5 rounded border uppercase ${
                isSuccess ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/30" :
                isRunning ? "bg-indigo-500/10 text-indigo-400 border-indigo-500/30" : "bg-slate-800 text-slate-500 border-slate-700"
              }`}>
                {task.status}
              </span>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
