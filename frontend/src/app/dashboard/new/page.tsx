"use client";

import React, { useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { apiClient } from "@/lib/apiClient";
import PromptInput from "@/components/PromptInput";
import { Card } from "@/components/ui/primitives";
import { Sparkles, Layers } from "lucide-react";

export default function NewProjectPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleSubmitPrompt = async (prompt: string) => {
    setIsLoading(true);
    setErrorMessage("");

    try {
      const res = await apiClient.post("/projects", {
        name: prompt.slice(0, 40) + "...",
        prompt: prompt,
      });

      if (res.data?.id) {
        router.push(`/dashboard/${res.data.id}`);
      }
    } catch (err: any) {
      console.error("Project creation error:", err);
      // Fallback demo redirect if server offline
      const mockId = `demo-${Date.now()}`;
      router.push(`/dashboard/${mockId}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto py-16 px-6 space-y-8">
      <div className="text-center space-y-3">
        <div className="w-12 h-12 rounded-2xl bg-indigo-600/20 text-indigo-400 flex items-center justify-center mx-auto border border-indigo-500/30">
          <Sparkles className="w-6 h-6" />
        </div>
        <h1 className="text-3xl font-extrabold text-white">Describe Your Idea</h1>
        <p className="text-slate-400 text-sm max-w-md mx-auto">
          ForgeAI will automatically break your request into a DAG graph and invoke Planner, Research, CodeGen, Debug, and Docs agents.
        </p>
      </div>

      {errorMessage && (
        <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs font-medium text-center">
          {errorMessage}
        </div>
      )}

      <Card className="p-8">
        <PromptInput onSubmit={handleSubmitPrompt} isLoading={isLoading} />
      </Card>
    </div>
  );
}
