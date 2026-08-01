"use client";

import React from "react";
import { MessageSquare, FileText, Pill, Heart, UserCheck, Layers } from "lucide-react";

interface TimelineFiltersProps {
  activeFilter: string;
  onFilterChange: (filter: string) => void;
}

export default function TimelineFilters({ activeFilter, onFilterChange }: TimelineFiltersProps) {
  const filters = [
    { id: "all", label: "All Events", icon: Layers },
    { id: "consultation", label: "Consultations", icon: MessageSquare },
    { id: "report", label: "Uploaded Reports", icon: FileText },
    { id: "medication", label: "Medications", icon: Pill },
    { id: "wellness", label: "Wellness", icon: Heart },
    { id: "profile", label: "Profile Updates", icon: UserCheck },
  ];

  return (
    <div className="flex flex-wrap items-center gap-2 py-2">
      {filters.map((f) => {
        const Icon = f.icon;
        const isActive = activeFilter === f.id;

        return (
          <button
            key={f.id}
            onClick={() => onFilterChange(f.id)}
            className={`flex items-center gap-2 px-4 py-2 rounded-2xl text-xs font-bold transition-all border ${
              isActive
                ? "bg-gradient-to-r from-cyan-500 to-teal-400 text-slate-950 border-cyan-300 shadow-md shadow-cyan-500/20"
                : "glass-panel border-slate-800 text-slate-300 hover:border-slate-700 hover:text-white"
            }`}
          >
            <Icon className={`w-3.5 h-3.5 ${isActive ? "text-slate-950" : "text-cyan-400"}`} />
            {f.label}
          </button>
        );
      })}
    </div>
  );
}
