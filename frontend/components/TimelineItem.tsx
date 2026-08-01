"use client";

import React, { useState } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import { 
  MessageSquare, 
  FileText, 
  Pill, 
  Heart, 
  UserCheck, 
  ChevronDown, 
  ChevronUp, 
  Stethoscope, 
  Gauge, 
  AlertTriangle, 
  CheckCircle2, 
  ShieldAlert, 
  Calendar,
  Clock
} from "lucide-react";

interface TimelineItemProps {
  item: {
    id: string;
    type: string;
    title: string;
    summary: string;
    timestamp: string;
    doctor?: string;
    ward?: string;
    confidence?: number;
    details?: any;
  };
  isLast?: boolean;
}

export default function TimelineItem({ item, isLast = false }: TimelineItemProps) {
  const [expanded, setExpanded] = useState(false);

  // Date and time formatting
  const dateObj = new Date(item.timestamp);
  const formattedDate = dateObj.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
  const formattedTime = dateObj.toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
  });

  // Type styling configuration
  const getTypeConfig = (type: string) => {
    switch (type) {
      case "consultation":
        return {
          icon: Stethoscope,
          badgeColor: "bg-cyan-500/20 text-cyan-300 border-cyan-500/40",
          iconBg: "from-cyan-500 to-indigo-500 shadow-cyan-500/20",
          glowColor: "border-cyan-500/30",
          typeLabel: "AI Consultation",
        };
      case "report":
        return {
          icon: FileText,
          badgeColor: "bg-indigo-500/20 text-indigo-300 border-indigo-500/40",
          iconBg: "from-indigo-500 to-purple-500 shadow-indigo-500/20",
          glowColor: "border-indigo-500/30",
          typeLabel: "Uploaded Report",
        };
      case "medication":
        return {
          icon: Pill,
          badgeColor: "bg-teal-500/20 text-teal-300 border-teal-500/40",
          iconBg: "from-teal-500 to-emerald-500 shadow-teal-500/20",
          glowColor: "border-teal-500/30",
          typeLabel: "Medication Event",
        };
      case "wellness":
        return {
          icon: Heart,
          badgeColor: "bg-rose-500/20 text-rose-300 border-rose-500/40",
          iconBg: "from-rose-500 to-amber-500 shadow-rose-500/20",
          glowColor: "border-rose-500/30",
          typeLabel: "Wellness Check",
        };
      case "profile":
      default:
        return {
          icon: UserCheck,
          badgeColor: "bg-blue-500/20 text-blue-300 border-blue-500/40",
          iconBg: "from-blue-500 to-cyan-500 shadow-blue-500/20",
          glowColor: "border-blue-500/30",
          typeLabel: "Profile Update",
        };
    }
  };

  const config = getTypeConfig(item.type);
  const Icon = config.icon;

  return (
    <div className="relative flex gap-4 sm:gap-6 group">
      
      {/* Timeline Vertical Spine */}
      <div className="flex flex-col items-center">
        {/* Event Icon Badge */}
        <div className={`w-10 h-10 sm:w-12 sm:h-12 rounded-2xl bg-gradient-to-tr ${config.iconBg} p-0.5 shadow-lg shrink-0 z-10 group-hover:scale-110 transition-transform duration-300`}>
          <div className="w-full h-full bg-[#0b1329] rounded-[14px] flex items-center justify-center">
            <Icon className="w-5 h-5 sm:w-6 sm:h-6 text-white" />
          </div>
        </div>

        {/* Vertical Connecting Line */}
        {!isLast && (
          <div className="w-0.5 flex-1 bg-gradient-to-b from-slate-700 via-slate-800 to-slate-900 my-2" />
        )}
      </div>

      {/* Main Glassmorphism Card */}
      <div className="flex-1 pb-8">
        <div className={`glass-panel p-5 sm:p-6 rounded-3xl border ${config.glowColor} transition-all duration-300 hover:border-cyan-500/50 shadow-xl space-y-3`}>
          
          {/* Header Row */}
          <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 pb-3">
            <div className="flex items-center gap-2">
              <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-extrabold uppercase tracking-wider border ${config.badgeColor}`}>
                {config.typeLabel}
              </span>
              {item.ward && (
                <span className="px-2 py-0.5 rounded-md bg-slate-800 text-[10px] font-bold text-slate-300 uppercase">
                  {item.ward} Ward
                </span>
              )}
            </div>

            {/* Date & Time Badge */}
            <div className="flex items-center gap-3 text-xs text-slate-400 font-medium">
              <span className="flex items-center gap-1">
                <Calendar className="w-3.5 h-3.5 text-cyan-400" />
                {formattedDate}
              </span>
              <span className="flex items-center gap-1">
                <Clock className="w-3.5 h-3.5 text-slate-500" />
                {formattedTime}
              </span>
            </div>
          </div>

          {/* Title & Summary */}
          <div>
            <h3 className="text-base sm:text-lg font-extrabold text-white group-hover:text-cyan-300 transition-colors">
              {item.title}
            </h3>
            <p className="text-xs sm:text-sm text-slate-300 mt-1 leading-relaxed">
              {item.summary}
            </p>
          </div>

          {/* Key Quick Attributes */}
          <div className="flex flex-wrap items-center gap-4 text-xs pt-1 text-slate-400">
            {item.doctor && (
              <span>👨‍⚕️ Specialist: <strong className="text-cyan-300">{item.doctor}</strong></span>
            )}
            {item.confidence && (
              <span className="flex items-center gap-1 text-emerald-400 font-semibold bg-emerald-500/10 px-2 py-0.5 rounded-md border border-emerald-500/20">
                <Gauge className="w-3.5 h-3.5" />
                Confidence: {Math.round(item.confidence * 100)}%
              </span>
            )}
          </div>

          {/* Expandable Details Button */}
          {item.details && Object.keys(item.details).length > 0 && (
            <div className="pt-2">
              <button
                onClick={() => setExpanded(!expanded)}
                className="flex items-center gap-1.5 text-xs font-bold text-cyan-400 hover:text-cyan-300 transition-colors"
              >
                {expanded ? (
                  <>Hide Clinical Details <ChevronUp className="w-4 h-4" /></>
                ) : (
                  <>View Details <ChevronDown className="w-4 h-4" /></>
                )}
              </button>

              <AnimatePresence>
                {expanded && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: "auto" }}
                    exit={{ opacity: 0, height: 0 }}
                    transition={{ duration: 0.3 }}
                    className="mt-3 pt-3 border-t border-slate-800 space-y-3 text-xs text-slate-300 overflow-hidden"
                  >
                    {/* Causes */}
                    {item.details.possible_causes && item.details.possible_causes.length > 0 && (
                      <div className="bg-slate-900/80 p-3 rounded-2xl border border-slate-800">
                        <span className="font-bold text-indigo-400 block mb-1 flex items-center gap-1">
                          <AlertTriangle className="w-3.5 h-3.5" /> Possible Causes:
                        </span>
                        <ul className="list-disc list-inside space-y-0.5 text-slate-300">
                          {item.details.possible_causes.map((c: string, idx: number) => (
                            <li key={idx}>{c}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Actions */}
                    {item.details.recommended_actions && item.details.recommended_actions.length > 0 && (
                      <div className="bg-slate-900/80 p-3 rounded-2xl border border-slate-800">
                        <span className="font-bold text-teal-400 block mb-1 flex items-center gap-1">
                          <CheckCircle2 className="w-3.5 h-3.5" /> Recommended Actions:
                        </span>
                        <ul className="list-disc list-inside space-y-0.5 text-slate-300">
                          {item.details.recommended_actions.map((a: string, idx: number) => (
                            <li key={idx}>{a}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Warning Signs */}
                    {item.details.warning_signs && item.details.warning_signs.length > 0 && (
                      <div className="bg-rose-950/30 p-3 rounded-2xl border border-rose-500/30 text-rose-200">
                        <span className="font-bold text-rose-400 block mb-1 flex items-center gap-1">
                          <ShieldAlert className="w-3.5 h-3.5" /> Warning Signs:
                        </span>
                        <ul className="list-disc list-inside space-y-0.5">
                          {item.details.warning_signs.map((w: string, idx: number) => (
                            <li key={idx}>{w}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Medications / Conditions Array details */}
                    {item.details.medications && item.details.medications.length > 0 && (
                      <div className="bg-slate-900/80 p-3 rounded-2xl border border-slate-800">
                        <span className="font-bold text-cyan-400 block mb-1">Medication List:</span>
                        <p>{item.details.medications.join(", ")}</p>
                      </div>
                    )}

                    {/* Extracted Text Preview */}
                    {item.details.extracted_text_preview && (
                      <div className="bg-slate-950 p-3 rounded-2xl border border-slate-800 text-[11px] font-mono text-slate-300">
                        <span className="font-bold text-cyan-400 block mb-1 font-sans text-xs">Extracted Document Preview:</span>
                        <p className="line-clamp-3">{item.details.extracted_text_preview}</p>
                      </div>
                    )}

                    {/* Action Buttons for Reports & Consultations */}
                    <div className="flex flex-wrap items-center gap-2 pt-2">
                      <Link
                        href="/reports"
                        className="px-3.5 py-1.5 rounded-xl bg-cyan-500 text-slate-950 font-extrabold text-[11px] hover:brightness-110 transition-all shadow-md shadow-cyan-500/20"
                      >
                        Open Full Report →
                      </Link>

                      <Link
                        href={`/chat?prompt=${encodeURIComponent("Please explain my uploaded medical report and compare it with my previous medical history.")}`}
                        className="px-3.5 py-1.5 rounded-xl bg-slate-900 border border-cyan-500/50 text-cyan-300 font-extrabold text-[11px] hover:bg-cyan-500 hover:text-slate-950 transition-all"
                      >
                        💬 Ask HealthAI About This Report
                      </Link>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          )}

        </div>
      </div>

    </div>
  );
}
