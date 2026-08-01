"use client";

import React from "react";
import { motion } from "framer-motion";
import { MessageSquare, FileText, Pill, Heart, Clock, Sparkles } from "lucide-react";

interface TimelineStatsProps {
  stats: {
    total_consultations: number;
    reports_uploaded: number;
    active_medications: number;
    health_score: number;
    last_consultation_date: string | null;
  };
}

export default function TimelineStats({ stats }: TimelineStatsProps) {
  const formatDate = (dateStr: string | null) => {
    if (!dateStr) return "No consultations yet";
    const date = new Date(dateStr);
    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

  const statItems = [
    {
      label: "Total Consultations",
      value: stats.total_consultations,
      subText: "AI clinical sessions",
      icon: MessageSquare,
      color: "text-cyan-400",
      bg: "bg-cyan-500/10 border-cyan-500/30",
    },
    {
      label: "Reports Uploaded",
      value: stats.reports_uploaded,
      subText: "Lab & diagnostic files",
      icon: FileText,
      color: "text-indigo-400",
      bg: "bg-indigo-500/10 border-indigo-500/30",
    },
    {
      label: "Active Medications",
      value: stats.active_medications,
      subText: "Rx & supplements",
      icon: Pill,
      color: "text-teal-400",
      bg: "bg-teal-500/10 border-teal-500/30",
    },
    {
      label: "Average Health Score",
      value: `${stats.health_score} / 100`,
      subText: "Personal index",
      icon: Heart,
      color: "text-emerald-400",
      bg: "bg-emerald-500/10 border-emerald-500/30",
    },
    {
      label: "Last Consultation",
      value: formatDate(stats.last_consultation_date),
      subText: "Latest AI triage",
      icon: Clock,
      color: "text-amber-400",
      bg: "bg-amber-500/10 border-amber-500/30",
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
      {statItems.map((item, idx) => {
        const Icon = item.icon;
        return (
          <motion.div
            key={idx}
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: idx * 0.08 }}
            className={`glass-panel p-4 rounded-2xl border ${item.bg} flex flex-col justify-between space-y-2`}
          >
            <div className="flex items-center justify-between">
              <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
                {item.label}
              </span>
              <Icon className={`w-4 h-4 ${item.color}`} />
            </div>
            <div>
              <p className="text-xl font-black text-white tracking-tight">{item.value}</p>
              <span className="text-[10px] text-slate-400 font-medium">{item.subText}</span>
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}
