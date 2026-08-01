"use client";

import React from "react";
import { Activity, AlertTriangle, CheckCircle2, ShieldAlert, Sparkles, User, Stethoscope, Gauge } from "lucide-react";

interface AIAnalysis {
  possible_causes?: string[];
  recommended_actions?: string[];
  warning_signs?: string[];
  personalized_advice?: string;
  confidence?: number;
  ward?: string;
  assigned_doctor?: string;
}

interface ChatBubbleProps {
  role: "user" | "assistant";
  content: string;
  analysis?: AIAnalysis;
  timestamp?: string;
}

export default function ChatBubble({ role, content, analysis, timestamp }: ChatBubbleProps) {
  const isUser = role === "user";

  return (
    <div className={`flex gap-4 mb-6 ${isUser ? "justify-end" : "justify-start"}`}>
      {/* Avatar */}
      {!isUser && (
        <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-cyan-500 to-indigo-500 p-0.5 shadow-md shadow-cyan-500/20 shrink-0">
          <div className="w-full h-full bg-[#0b1329] rounded-[14px] flex items-center justify-center">
            <Stethoscope className="w-5 h-5 text-cyan-400" />
          </div>
        </div>
      )}

      {/* Bubble Container */}
      <div className={`max-w-3xl rounded-3xl p-5 sm:p-6 text-sm leading-relaxed ${
        isUser
          ? "bg-gradient-to-r from-cyan-600 to-teal-600 text-slate-950 font-medium rounded-tr-none shadow-lg shadow-cyan-500/15"
          : "glass-panel border-slate-700/80 text-slate-200 rounded-tl-none shadow-xl"
      }`}>
        
        {/* User Content */}
        {isUser ? (
          <p className="whitespace-pre-wrap">{content}</p>
        ) : (
          <div className="space-y-5">
            
            {/* AI Top Bar Badge */}
            <div className="flex flex-wrap items-center justify-between gap-2 pb-3 border-b border-slate-800">
              <div className="flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-cyan-400" />
                <span className="font-bold text-white text-sm">HealthAI Assessment</span>
                {analysis?.ward && (
                  <span className={`px-2.5 py-0.5 rounded-full text-[11px] font-bold uppercase tracking-wider ${
                    analysis.ward === "emergency"
                      ? "bg-rose-500/20 text-rose-300 border border-rose-500/40"
                      : analysis.ward === "mental_health"
                      ? "bg-purple-500/20 text-purple-300 border border-purple-500/40"
                      : "bg-cyan-500/20 text-cyan-300 border border-cyan-500/40"
                  }`}>
                    {analysis.ward.replace('_', ' ')} Ward
                  </span>
                )}
              </div>

              {analysis?.confidence && (
                <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-800 text-xs font-semibold text-emerald-400 border border-slate-700">
                  <Gauge className="w-3.5 h-3.5" />
                  Confidence: {Math.round(analysis.confidence * 100)}%
                </div>
              )}
            </div>

            {/* Doctor Triage Info */}
            {analysis?.assigned_doctor && (
              <div className="text-xs text-slate-400 bg-slate-900/60 px-3 py-2 rounded-xl border border-slate-800 flex items-center justify-between">
                <span>👨‍⚕️ Assigned Specialist: <strong className="text-cyan-300">{analysis.assigned_doctor}</strong></span>
              </div>
            )}

            {/* General Text Reply */}
            <p className="text-slate-300 whitespace-pre-wrap">{content}</p>

            {/* Structured AI Analysis Cards */}
            {analysis && (
              <div className="space-y-4 pt-2">
                
                {/* Personalized Advice Card */}
                {analysis.personalized_advice && (
                  <div className="p-4 rounded-2xl bg-cyan-950/40 border border-cyan-500/40 text-cyan-100">
                    <h4 className="font-bold text-cyan-300 text-xs uppercase tracking-wider mb-1 flex items-center gap-2">
                      <Activity className="w-4 h-4 text-cyan-400" />
                      Personalized Health Profile Context
                    </h4>
                    <p className="text-xs text-slate-200 leading-relaxed">
                      {analysis.personalized_advice}
                    </p>
                  </div>
                )}

                {/* Grid of Causes & Actions */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  
                  {/* Possible Causes */}
                  {analysis.possible_causes && analysis.possible_causes.length > 0 && (
                    <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800">
                      <h4 className="font-bold text-slate-200 text-xs uppercase tracking-wider mb-2 flex items-center gap-1.5 text-indigo-400">
                        <AlertTriangle className="w-4 h-4" />
                        Possible Causes
                      </h4>
                      <ul className="space-y-1 text-xs text-slate-300">
                        {analysis.possible_causes.map((cause, i) => (
                          <li key={i} className="flex items-start gap-1.5">
                            <span className="text-indigo-400 font-bold">•</span>
                            {cause}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Recommended Actions */}
                  {analysis.recommended_actions && analysis.recommended_actions.length > 0 && (
                    <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800">
                      <h4 className="font-bold text-slate-200 text-xs uppercase tracking-wider mb-2 flex items-center gap-1.5 text-teal-400">
                        <CheckCircle2 className="w-4 h-4" />
                        Recommended Actions
                      </h4>
                      <ul className="space-y-1 text-xs text-slate-300">
                        {analysis.recommended_actions.map((act, i) => (
                          <li key={i} className="flex items-start gap-1.5">
                            <span className="text-teal-400 font-bold">•</span>
                            {act}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>

                {/* Warning Signs (Red Flags) */}
                {analysis.warning_signs && analysis.warning_signs.length > 0 && (
                  <div className="p-4 rounded-2xl bg-rose-950/30 border border-rose-500/40 text-rose-200">
                    <h4 className="font-bold text-rose-400 text-xs uppercase tracking-wider mb-2 flex items-center gap-1.5">
                      <ShieldAlert className="w-4 h-4" />
                      Seek Emergency Care Immediately If You Notice:
                    </h4>
                    <ul className="grid grid-cols-1 sm:grid-cols-2 gap-1.5 text-xs text-slate-200">
                      {analysis.warning_signs.map((sign, i) => (
                        <li key={i} className="flex items-start gap-1.5">
                          <span className="text-rose-400 font-bold">•</span>
                          {sign}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Medical Disclaimer Banner */}
                <div className="text-[11px] text-slate-400 bg-slate-950/80 p-3 rounded-xl border border-slate-800/80 italic">
                  💡 <strong>Disclaimer:</strong> HealthAI provides automated triage and wellness guidance for informational purposes only. It does not replace professional emergency medical diagnosis or treatment.
                </div>

              </div>
            )}
          </div>
        )}
      </div>

      {/* User Avatar */}
      {isUser && (
        <div className="w-10 h-10 rounded-2xl bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-300 shrink-0">
          <User className="w-5 h-5" />
        </div>
      )}
    </div>
  );
}
