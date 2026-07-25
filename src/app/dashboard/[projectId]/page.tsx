"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useBuildStore } from "@/store/useBuildStore";
import { BuildSocketClient } from "@/lib/socket";
import { apiClient } from "@/lib/apiClient";
import AgentStatusCard from "@/components/AgentStatusCard";
import LiveBuildConsole from "@/components/LiveBuildConsole";
import ProgressGraph from "@/components/ProgressGraph";
import { Card, Button, Badge } from "@/components/ui/primitives";
import { ExternalLink, Layers, FileCode, CheckCircle2, Play, ChevronRight } from "lucide-react";

export default function LiveBuildPage() {
  const params = useParams();
  const projectId = params.projectId as string;

  const {
    projectStatus,
    logs,
    tasks,
    files,
    activeAgent,
    previewUrl,
    setProject,
    handleSocketEvent,
  } = useBuildStore();

  const [selectedFile, setSelectedFile] = useState<string | null>(null);

  useEffect(() => {
    // 1. Fetch initial DB details
    async function loadProjectDetails() {
      try {
        const res = await apiClient.get(`/projects/${projectId}`);
        if (res.data) {
          setProject(
            res.data.id,
            res.data.status,
            res.data.tasks,
            res.data.logs,
            res.data.files
          );
          if (res.data.files?.length > 0) {
            setSelectedFile(res.data.files[0].path);
          }
        }
      } catch (err) {
        console.error("Error loading project detail:", err);
      }
    }
    loadProjectDetails();

    // 2. Connect WebSocket live event stream
    const socketClient = new BuildSocketClient(projectId, (event) => {
      handleSocketEvent(event);
    });
    socketClient.connect();

    return () => {
      socketClient.disconnect();
    };
  }, [projectId]);

  const activeFileObj = files.find((f) => f.path === selectedFile) || (files.length > 0 ? files[0] : null);

  return (
    <div className="max-w-7xl mx-auto py-8 px-6 space-y-6">
      {/* Header Bar */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center p-6 rounded-2xl border border-slate-800 bg-slate-900/60 backdrop-blur-xl">
        <div>
          <div className="flex items-center space-x-3">
            <Badge variant={projectStatus === "COMPLETED" ? "emerald" : "indigo"}>
              {projectStatus}
            </Badge>
            <span className="text-xs font-mono text-slate-500">ID: {projectId}</span>
          </div>
          <h1 className="text-2xl font-bold text-white mt-1 flex items-center">
            Autonomous Multi-Agent Build Stream
          </h1>
        </div>

        <div className="mt-4 md:mt-0 flex items-center space-x-3">
          <Link href={`/dashboard/${projectId}/preview`}>
            <Button className="flex items-center space-x-2 bg-emerald-600 hover:bg-emerald-500 font-semibold text-xs">
              <ExternalLink className="w-4 h-4" />
              <span>Open Live Container Preview</span>
            </Button>
          </Link>
        </div>
      </div>

      {/* Grid Layout: Agents & DAG on left, Live Console & Files on right */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Agent Cards & Task Graph */}
        <div className="lg:col-span-5 space-y-4">
          <h2 className="text-xs font-semibold uppercase tracking-wider text-slate-400 font-mono">Agent Status Telemetry</h2>
          
          <div className="space-y-3">
            <AgentStatusCard
              role="planner"
              name="Planner Agent"
              provider="Claude 3.5 Sonnet"
              status={activeAgent === "planner" ? "running" : tasks.find(t => t.agent_role === "planner")?.status === "SUCCESS" ? "completed" : "idle"}
              description="Constructs task execution DAG and page hierarchy"
            />
            <AgentStatusCard
              role="research"
              name="Research Agent"
              provider="Gemini + Tavily Search"
              status={activeAgent === "research" ? "running" : tasks.find(t => t.agent_role === "research")?.status === "SUCCESS" ? "completed" : "idle"}
              description="Synthesizes design tokens and competitor benchmarks"
            />
            <AgentStatusCard
              role="codegen"
              name="CodeGen Agent"
              provider="GPT-4o / DeepSeek"
              status={activeAgent === "codegen" ? "running" : tasks.find(t => t.agent_role === "codegen")?.status === "SUCCESS" ? "completed" : "idle"}
              description="Emits full Next.js 14 project file tree JSON"
            />
            <AgentStatusCard
              role="debug"
              name="Debug & Repair Agent"
              provider="GPT-4o + Node Sandbox"
              status={activeAgent === "debug" ? "running" : tasks.find(t => t.agent_role === "debug")?.status === "SUCCESS" ? "completed" : "idle"}
              description="Runs npm build inside sandbox with 3 retry repair loop"
            />
            <AgentStatusCard
              role="docs"
              name="Documentation Agent"
              provider="Claude 3.5 Sonnet"
              status={activeAgent === "docs" ? "running" : tasks.find(t => t.agent_role === "docs")?.status === "SUCCESS" ? "completed" : "idle"}
              description="Generates component architecture & README docs"
            />
          </div>

          <ProgressGraph tasks={tasks} />
        </div>

        {/* Right Column: Streaming Console & File Inspector */}
        <div className="lg:col-span-7 space-y-4">
          <LiveBuildConsole logs={logs} />

          {/* Generated Files Inspector */}
          {files.length > 0 && (
            <Card className="p-4 space-y-3">
              <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                <span className="text-xs font-semibold text-slate-300 flex items-center">
                  <FileCode className="w-4 h-4 text-indigo-400 mr-2" /> Generated Project Workspace ({files.length} files)
                </span>
              </div>

              <div className="flex flex-wrap gap-2 pt-1">
                {files.map((file) => (
                  <button
                    key={file.path}
                    onClick={() => setSelectedFile(file.path)}
                    className={`px-2.5 py-1 rounded-lg text-xs font-mono transition border ${
                      selectedFile === file.path
                        ? "bg-indigo-600/20 text-indigo-300 border-indigo-500/50"
                        : "bg-slate-900 text-slate-400 border-slate-800 hover:bg-slate-800"
                    }`}
                  >
                    {file.path}
                  </button>
                ))}
              </div>

              {activeFileObj && (
                <div className="rounded-xl bg-slate-950 p-4 font-mono text-xs text-slate-300 overflow-x-auto max-h-60 custom-scrollbar border border-slate-800">
                  <pre>{activeFileObj.content}</pre>
                </div>
              )}
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
