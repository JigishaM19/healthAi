"use client";

import React from "react";
import { CheckCircle2, Loader2, Sparkles, FileSearch, ShieldCheck, Database } from "lucide-react";

interface ExtractionProgressProps {
  currentStep: "upload" | "ocr" | "extraction" | "analysis" | "complete";
}

export default function ExtractionProgress({ currentStep }: ExtractionProgressProps) {
  const steps = [
    { id: "upload", label: "Uploading File", icon: FileSearch },
    { id: "ocr", label: "OCR Text Extraction", icon: Sparkles },
    { id: "extraction", label: "Entity Detection", icon: Database },
    { id: "analysis", label: "AI Medical Analysis", icon: ShieldCheck },
  ];

  const getStepStatus = (stepId: string) => {
    const order = ["upload", "ocr", "extraction", "analysis", "complete"];
    const currIdx = order.indexOf(currentStep);
    const stepIdx = order.indexOf(stepId);

    if (stepIdx < currIdx || currentStep === "complete") return "complete";
    if (stepIdx === currIdx) return "active";
    return "pending";
  };

  return (
    <div className="glass-panel p-5 rounded-3xl border border-cyan-500/30 space-y-4">
      <div className="flex items-center justify-between text-xs font-bold text-slate-300 uppercase tracking-wider">
        <span className="flex items-center gap-1.5 text-cyan-400">
          <Sparkles className="w-4 h-4" />
          Universal Medical Processing Pipeline
        </span>
        <span className="text-cyan-300 font-semibold">{currentStep.toUpperCase()}</span>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {steps.map((st) => {
          const status = getStepStatus(st.id);
          const Icon = st.icon;

          return (
            <div
              key={st.id}
              className={`p-3 rounded-2xl border text-xs flex items-center gap-2.5 transition-all ${
                status === "complete"
                  ? "bg-teal-950/40 border-teal-500/40 text-teal-300"
                  : status === "active"
                  ? "bg-cyan-950/60 border-cyan-400 text-cyan-200 shadow-md shadow-cyan-500/20 font-bold"
                  : "bg-slate-900/60 border-slate-800 text-slate-500"
              }`}
            >
              {status === "complete" ? (
                <CheckCircle2 className="w-4 h-4 text-teal-400 shrink-0" />
              ) : status === "active" ? (
                <Loader2 className="w-4 h-4 text-cyan-400 animate-spin shrink-0" />
              ) : (
                <Icon className="w-4 h-4 shrink-0" />
              )}
              <span className="truncate">{st.label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
