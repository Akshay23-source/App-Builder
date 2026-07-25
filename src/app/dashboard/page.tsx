"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { apiClient } from "@/lib/apiClient";
import { Card, Button, Badge } from "@/components/ui/primitives";
import { Plus, Layers, ExternalLink, Clock, Play } from "lucide-react";

interface ProjectItem {
  id: string;
  name: string;
  prompt: string;
  status: string;
  preview_url: string | null;
  created_at: string;
}

export default function DashboardPage() {
  const [projects, setProjects] = useState<ProjectItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function fetchProjects() {
      try {
        const res = await apiClient.get("/projects");
        setProjects(res.data || []);
      } catch (err) {
        console.error("Error fetching projects:", err);
        // Fallback demo mock project
        setProjects([
          {
            id: "demo-proj-1",
            name: "AI SaaS Video Platform",
            prompt: "A SaaS landing page for an AI video editor with pricing tables and dark glassmorphic hero",
            status: "COMPLETED",
            preview_url: "/dashboard/demo-proj-1/preview",
            created_at: new Date().toISOString(),
          },
        ]);
      } finally {
        setIsLoading(false);
      }
    }
    fetchProjects();
  }, []);

  return (
    <div className="max-w-7xl mx-auto py-12 px-6 space-y-8">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center">
        <div>
          <h1 className="text-3xl font-bold text-white flex items-center">
            <Layers className="w-7 h-7 text-indigo-400 mr-3" /> My Generated Projects
          </h1>
          <p className="text-slate-400 text-sm mt-1">Manage and inspect your autonomous multi-agent builds.</p>
        </div>

        <Link href="/dashboard/new" className="mt-4 md:mt-0">
          <Button className="flex items-center space-x-2 bg-indigo-600 hover:bg-indigo-500 text-white">
            <Plus className="w-4 h-4" />
            <span>New Project Idea</span>
          </Button>
        </Link>
      </div>

      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[1, 2, 3].map((i) => (
            <Card key={i} className="h-44 animate-pulse bg-slate-900/40" />
          ))}
        </div>
      ) : projects.length === 0 ? (
        <Card className="p-12 text-center space-y-4">
          <Layers className="w-12 h-12 text-slate-600 mx-auto" />
          <h3 className="text-lg font-semibold text-white">No project builds found yet</h3>
          <p className="text-slate-400 text-xs max-w-sm mx-auto">
            Submit a single prompt idea to launch your first multi-agent web application generation.
          </p>
          <Link href="/dashboard/new">
            <Button className="mt-2">Create First Project</Button>
          </Link>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {projects.map((proj) => (
            <Card key={proj.id} className="p-5 flex flex-col justify-between hover:border-indigo-500/40 transition duration-300">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <Badge variant={proj.status === "COMPLETED" ? "emerald" : "indigo"}>
                    {proj.status}
                  </Badge>
                  <span className="text-[11px] text-slate-500 flex items-center">
                    <Clock className="w-3 h-3 mr-1" />
                    {new Date(proj.created_at).toLocaleDateString()}
                  </span>
                </div>

                <h3 className="font-bold text-white text-lg line-clamp-1">{proj.name}</h3>
                <p className="text-slate-400 text-xs line-clamp-2 leading-relaxed">
                  "{proj.prompt}"
                </p>
              </div>

              <div className="pt-6 flex items-center justify-between border-t border-slate-800/80 mt-4">
                <Link href={`/dashboard/${proj.id}`} className="text-xs font-semibold text-indigo-400 hover:text-indigo-300 flex items-center">
                  <Play className="w-3.5 h-3.5 mr-1" /> View Live Build Console
                </Link>

                <Link href={`/dashboard/${proj.id}/preview`} className="text-xs font-semibold text-emerald-400 hover:text-emerald-300 flex items-center">
                  <ExternalLink className="w-3.5 h-3.5 mr-1" /> Preview
                </Link>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
