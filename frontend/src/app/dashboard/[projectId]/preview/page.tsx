"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { Card, Button } from "@/components/ui/primitives";
import { ArrowLeft, Monitor, Smartphone, RefreshCw, ExternalLink } from "lucide-react";

export default function ProjectPreviewPage() {
  const params = useParams();
  const projectId = params.projectId as string;
  const [deviceMode, setDeviceMode] = useState<"desktop" | "mobile">("desktop");
  const [refreshKey, setRefreshKey] = useState(0);

  const previewTargetUrl = `/api/v1/projects/${projectId}/preview`;

  return (
    <div className="max-w-7xl mx-auto py-6 px-6 space-y-4">
      {/* Control Bar */}
      <div className="flex flex-col md:flex-row justify-between items-center p-4 rounded-2xl border border-slate-800 bg-slate-900/80 backdrop-blur-xl">
        <div className="flex items-center space-x-3">
          <Link href={`/dashboard/${projectId}`}>
            <Button variant="outline" className="text-xs flex items-center space-x-1 py-1.5 px-3">
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>Back to Console</span>
            </Button>
          </Link>
          <span className="text-sm font-semibold text-white">Live Container Preview</span>
        </div>

        <div className="flex items-center space-x-2 mt-3 md:mt-0">
          <div className="bg-slate-950 p-1 rounded-xl border border-slate-800 flex space-x-1">
            <button
              onClick={() => setDeviceMode("desktop")}
              className={`p-2 rounded-lg text-xs font-medium flex items-center space-x-1.5 transition ${
                deviceMode === "desktop" ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"
              }`}
            >
              <Monitor className="w-4 h-4" />
              <span>Desktop</span>
            </button>
            <button
              onClick={() => setDeviceMode("mobile")}
              className={`p-2 rounded-lg text-xs font-medium flex items-center space-x-1.5 transition ${
                deviceMode === "mobile" ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"
              }`}
            >
              <Smartphone className="w-4 h-4" />
              <span>Mobile</span>
            </button>
          </div>

          <button
            onClick={() => setRefreshKey((k) => k + 1)}
            className="p-2 rounded-xl border border-slate-800 bg-slate-950 text-slate-400 hover:text-white"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Frame Sandbox Wrapper */}
      <div className="flex justify-center items-center py-4">
        <div
          className={`transition-all duration-300 rounded-2xl border border-slate-800 bg-slate-950 overflow-hidden shadow-2xl ${
            deviceMode === "desktop" ? "w-full h-[720px]" : "w-[375px] h-[667px] border-4 border-slate-800"
          }`}
        >
          <iframe
            key={refreshKey}
            src={previewTargetUrl}
            className="w-full h-full border-none"
            title="Project Preview"
          />
        </div>
      </div>
    </div>
  );
}
