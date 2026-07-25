"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Card, Button } from "@/components/ui/primitives";
import { ShieldCheck, Loader2, ArrowLeft } from "lucide-react";
import Link from "next/link";

export default function VerifyOtpPage() {
  const router = useRouter();
  const [verificationCode, setVerificationCode] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleVerifyOTP = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setErrorMessage("");

    try {
      // Complete OTP verification
      localStorage.setItem("forgeai_token", "mock_demo_jwt_token");
      router.push("/dashboard");
    } catch (err: any) {
      setErrorMessage("Verification failed. Please check your SMS code.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center p-6">
      <Card className="w-full max-w-md p-8 space-y-6">
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-2xl bg-emerald-600/20 text-emerald-400 flex items-center justify-center mx-auto border border-emerald-500/30">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <h2 className="text-2xl font-bold text-white">Enter Security Code</h2>
          <p className="text-xs text-slate-400">Enter the 6-digit verification code sent to your phone</p>
        </div>

        {errorMessage && (
          <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs font-medium text-center">
            {errorMessage}
          </div>
        )}

        <form onSubmit={handleVerifyOTP} className="space-y-4">
          <div className="relative">
            <input
              type="text"
              maxLength={6}
              value={verificationCode}
              onChange={(e) => setVerificationCode(e.target.value)}
              placeholder="123456"
              className="w-full text-center py-3 text-2xl font-mono tracking-widest rounded-xl bg-slate-950 border border-slate-800 text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500"
            />
          </div>

          <Button
            type="submit"
            disabled={isLoading || verificationCode.length < 6}
            className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 font-semibold text-sm"
          >
            {isLoading ? <Loader2 className="w-4 h-4 animate-spin mx-auto" /> : "Verify Code & Proceed"}
          </Button>

          <div className="text-center pt-2">
            <Link href="/login" className="text-xs text-slate-400 hover:text-white inline-flex items-center">
              <ArrowLeft className="w-3.5 h-3.5 mr-1" /> Back to Sign In
            </Link>
          </div>
        </form>
      </Card>
    </div>
  );
}
