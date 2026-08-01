"use client";

import React from "react";
import Link from "next/link";
import { 
  Sparkles, 
  AlertTriangle, 
  CheckCircle2, 
  ShieldAlert, 
  MessageSquare, 
  Activity, 
  FileText,
  ArrowRight
} from "lucide-react";

interface AnalysisCardProps {
  fileName: string;
  documentType: string;
  summary: string;
  abnormalValues?: any[];
  recommendations?: string[];
  redFlags?: string[];
  personalizedAdvice?: string;
  onAskChat?: () => void;
}

export default function AnalysisCard({
  fileName,
  documentType,
  summary,
  abnormalValues = [],
  recommendations = [],
  redFlags = [],
  personalizedAdvice,
  onAskChat
}: AnalysisCardProps) {
  return (
    <div className="glass-panel p-6 rounded-3xl border border-cyan-500/40 space-y-6 bg-gradient-to-r from-cyan-950/20 to-indigo-950/20">
      
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 pb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-cyan-500/20 border border-cyan-400/40 flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-cyan-400" />
          </div>
          <div>
            <h3 className="font-extrabold text-white text-base">Clinical AI Document Analysis</h3>
            <span className="text-xs text-cyan-300 font-semibold uppercase tracking-wider">
              {documentType.replace('_', ' ')} • {fileName}
            </span>
          </div>
        </div>

        <Link
          href={`/chat?prompt=${encodeURIComponent(`Please explain my uploaded medical document: ${fileName}`)}`}
          className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-teal-400 text-slate-950 text-xs font-bold hover:brightness-110 transition-all shadow-md shadow-cyan-500/20"
        >
          <MessageSquare className="w-4 h-4" />
          Ask HealthAI About This Document
        </Link>
      </div>

      {/* AI Summary */}
      <div className="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-1">
        <h4 className="font-bold text-xs uppercase tracking-wider text-cyan-400 flex items-center gap-1.5">
          <FileText className="w-4 h-4" />
          AI Executive Summary
        </h4>
        <p className="text-xs sm:text-sm text-slate-200 leading-relaxed">
          {summary}
        </p>
      </div>

      {/* Abnormal Lab Values Table */}
      {abnormalValues && abnormalValues.length > 0 && (
        <div className="space-y-2">
          <h4 className="font-bold text-xs uppercase tracking-wider text-rose-400 flex items-center gap-1.5">
            <AlertTriangle className="w-4 h-4 text-rose-400" />
            Detected Abnormal Values ({abnormalValues.length})
          </h4>
          
          <div className="overflow-x-auto rounded-2xl border border-slate-800 bg-slate-950/80">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-900 text-slate-400 font-bold uppercase text-[10px] tracking-wider border-b border-slate-800">
                <tr>
                  <th className="p-3">Marker / Test</th>
                  <th className="p-3">Measured Value</th>
                  <th className="p-3">Unit</th>
                  <th className="p-3">Reference Range</th>
                  <th className="p-3">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {abnormalValues.map((val, idx) => (
                  <tr key={idx} className="hover:bg-slate-900/40">
                    <td className="p-3 font-semibold text-white">{val.name}</td>
                    <td className="p-3 font-bold text-rose-300">{val.value}</td>
                    <td className="p-3 text-slate-400">{val.unit}</td>
                    <td className="p-3 text-slate-400">{val.reference}</td>
                    <td className="p-3">
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase ${
                        val.status === "High" ? "bg-rose-500/20 text-rose-300 border border-rose-500/40" : "bg-amber-500/20 text-amber-300 border border-amber-500/40"
                      }`}>
                        {val.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Grid of Recommendations & Red Flags */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        
        {/* Recommendations */}
        {recommendations && recommendations.length > 0 && (
          <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-2">
            <h4 className="font-bold text-xs uppercase tracking-wider text-teal-400 flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4" />
              Follow-up Recommendations
            </h4>
            <ul className="space-y-1 text-xs text-slate-300">
              {recommendations.map((r, i) => (
                <li key={i} className="flex items-start gap-1.5">
                  <span className="text-teal-400 font-bold">•</span>
                  {r}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Red Flags */}
        {redFlags && redFlags.length > 0 && (
          <div className="p-4 rounded-2xl bg-rose-950/30 border border-rose-500/30 space-y-2 text-rose-200">
            <h4 className="font-bold text-xs uppercase tracking-wider text-rose-400 flex items-center gap-1.5">
              <ShieldAlert className="w-4 h-4" />
              Clinical Urgency & Red Flags
            </h4>
            <ul className="space-y-1 text-xs">
              {redFlags.map((rf, i) => (
                <li key={i} className="flex items-start gap-1.5">
                  <span className="text-rose-400 font-bold">•</span>
                  {rf}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

    </div>
  );
}
