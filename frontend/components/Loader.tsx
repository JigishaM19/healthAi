"use client";

import React from "react";
import { Activity } from "lucide-react";

interface LoaderProps {
  label?: string;
  fullScreen?: boolean;
}

export default function Loader({ label = "Loading HealthAI...", fullScreen = false }: LoaderProps) {
  const content = (
    <div className="flex flex-col items-center justify-center p-8 space-y-4">
      <div className="relative flex items-center justify-center">
        <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-cyan-500 via-teal-400 to-indigo-500 p-0.5 animate-pulse shadow-xl shadow-cyan-500/20">
          <div className="w-full h-full bg-[#0b1329] rounded-[14px] flex items-center justify-center">
            <Activity className="w-8 h-8 text-cyan-400 animate-spin" style={{ animationDuration: "3s" }} />
          </div>
        </div>
      </div>
      <p className="text-sm font-semibold text-slate-300 tracking-wide animate-pulse">
        {label}
      </p>
    </div>
  );

  if (fullScreen) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-[#0b1329]/90 backdrop-blur-md">
        {content}
      </div>
    );
  }

  return content;
}
