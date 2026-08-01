"use client";

import React from "react";
import { Pill, AlertTriangle, CheckCircle2, Clock } from "lucide-react";

interface MedicineItem {
  name: string;
  dosage?: string;
  frequency?: string;
  duration?: string;
  instructions?: string;
  purpose?: string;
}

interface MedicationCardProps {
  medicines: MedicineItem[];
  warnings?: string[];
}

export default function MedicationCard({ medicines = [], warnings = [] }: MedicationCardProps) {
  if (medicines.length === 0 && warnings.length === 0) return null;

  return (
    <div className="space-y-4">
      
      {/* Allergy / Drug Conflict Warnings */}
      {warnings.length > 0 && (
        <div className="p-4 rounded-2xl bg-rose-950/50 border border-rose-500/50 text-rose-200 space-y-2">
          <div className="flex items-center gap-2 font-extrabold text-rose-400 text-xs uppercase tracking-wider">
            <AlertTriangle className="w-4 h-4 text-rose-400 animate-bounce" />
            Medical Safety & Allergy Warning
          </div>
          <ul className="space-y-1 text-xs">
            {warnings.map((w, idx) => (
              <li key={idx} className="flex items-start gap-1.5 font-semibold">
                <span>•</span>
                {w}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Extracted Medicine Schedule */}
      {medicines.length > 0 && (
        <div className="glass-panel p-5 rounded-3xl border border-slate-800 space-y-3">
          <div className="flex items-center justify-between">
            <h4 className="font-bold text-white text-xs uppercase tracking-wider flex items-center gap-2 text-teal-400">
              <Pill className="w-4 h-4" />
              Extracted Prescription & Medication Schedule ({medicines.length})
            </h4>
            <span className="text-[10px] text-teal-400 font-semibold bg-teal-500/10 px-2 py-0.5 rounded-full border border-teal-500/30">
              Auto-Synced to Profile
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
            {medicines.map((med, i) => (
              <div key={i} className="p-3 rounded-2xl bg-slate-900/80 border border-slate-800 text-xs space-y-1.5">
                <div className="flex items-center justify-between font-bold text-slate-100">
                  <span className="text-cyan-300">{med.name}</span>
                  <span className="text-slate-400 text-[11px]">{med.dosage || "Standard dose"}</span>
                </div>
                
                <div className="flex flex-wrap gap-2 text-[11px] text-slate-400">
                  <span className="flex items-center gap-1">
                    <Clock className="w-3 h-3 text-teal-400" />
                    {med.frequency || "Daily"}
                  </span>
                  {med.duration && <span>• Duration: {med.duration}</span>}
                </div>

                {med.instructions && (
                  <p className="text-[10px] text-slate-400 italic pt-1 border-t border-slate-800">
                    💡 {med.instructions}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

    </div>
  );
}
