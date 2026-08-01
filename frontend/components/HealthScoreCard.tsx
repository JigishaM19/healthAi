"use client";

import React from "react";
import { Activity, Droplet, Moon, Flame, Heart, Sparkles, TrendingUp } from "lucide-react";

interface HealthScoreCardProps {
  score: number;
  bmi: number;
  bmiCategory: string;
  hydrationGoal: string;
  activityRec: string;
  sleepTarget: string;
  wellnessFocus: string[];
}

export default function HealthScoreCard({
  score = 82,
  bmi = 23.4,
  bmiCategory = "Normal weight",
  hydrationGoal = "2.5 Liters / day",
  activityRec = "8,000 steps or 30 mins brisk walking",
  sleepTarget = "7.5 - 8.5 Hours of sleep",
  wellnessFocus = ["Improve sleep consistency", "Manage daily stress levels"],
}: HealthScoreCardProps) {
  // Score color calculation
  const getScoreColor = (val: number) => {
    if (val >= 80) return "from-teal-400 to-cyan-400 text-teal-400";
    if (val >= 60) return "from-amber-400 to-yellow-400 text-amber-400";
    return "from-rose-400 to-red-400 text-rose-400";
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      
      {/* 1. Main Health Score Circular Gauge */}
      <div className="md:col-span-1 glass-panel p-6 rounded-3xl border border-slate-800 flex flex-col items-center justify-center text-center relative overflow-hidden">
        <div className="absolute top-0 right-0 w-28 h-28 bg-cyan-500/10 rounded-full blur-xl pointer-events-none" />
        
        <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-4 flex items-center gap-1.5">
          <Sparkles className="w-4 h-4 text-cyan-400" />
          Personal Health Score
        </h3>

        {/* Circular Ring Graphic */}
        <div className="relative w-36 h-36 flex items-center justify-center my-2">
          <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
            <circle
              cx="50"
              cy="50"
              r="40"
              stroke="currentColor"
              strokeWidth="8"
              className="text-slate-800"
              fill="transparent"
            />
            <circle
              cx="50"
              cy="50"
              r="40"
              stroke="currentColor"
              strokeWidth="8"
              strokeDasharray={251.2}
              strokeDashoffset={251.2 - (251.2 * score) / 100}
              strokeLinecap="round"
              className={`text-cyan-400 transition-all duration-1000 ease-out`}
              fill="transparent"
            />
          </svg>
          <div className="absolute flex flex-col items-center justify-center text-center">
            <span className="text-4xl font-extrabold text-white tracking-tight">{score}</span>
            <span className="text-[10px] text-slate-400 uppercase font-semibold">out of 100</span>
          </div>
        </div>

        <p className="text-xs text-emerald-400 font-semibold flex items-center gap-1 mt-2">
          <TrendingUp className="w-3.5 h-3.5" />
          Optimal Health Index
        </p>
      </div>

      {/* 2. Vital Metrics Summary Grid */}
      <div className="md:col-span-2 space-y-4">
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
          
          {/* BMI Card */}
          <div className="glass-panel p-4 rounded-2xl border border-slate-800/80 hover:border-slate-700 transition-all">
            <div className="flex items-center gap-2 text-indigo-400 mb-2">
              <Activity className="w-4 h-4" />
              <span className="text-xs font-bold">BMI</span>
            </div>
            <p className="text-xl font-bold text-white">{bmi}</p>
            <span className="text-[11px] text-slate-400 font-medium">{bmiCategory}</span>
          </div>

          {/* Hydration Card */}
          <div className="glass-panel p-4 rounded-2xl border border-slate-800/80 hover:border-slate-700 transition-all">
            <div className="flex items-center gap-2 text-cyan-400 mb-2">
              <Droplet className="w-4 h-4" />
              <span className="text-xs font-bold">Hydration</span>
            </div>
            <p className="text-sm font-bold text-white">{hydrationGoal}</p>
            <span className="text-[11px] text-teal-400 font-medium">Daily Target</span>
          </div>

          {/* Sleep Target Card */}
          <div className="glass-panel p-4 rounded-2xl border border-slate-800/80 hover:border-slate-700 transition-all col-span-2 sm:col-span-1">
            <div className="flex items-center gap-2 text-teal-400 mb-2">
              <Moon className="w-4 h-4" />
              <span className="text-xs font-bold">Sleep Target</span>
            </div>
            <p className="text-sm font-bold text-white">{sleepTarget}</p>
            <span className="text-[11px] text-slate-400 font-medium">Restorative Sleep</span>
          </div>

        </div>

        {/* 3. Activity & Focus Areas Card */}
        <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-xs font-bold text-white uppercase tracking-wider">
              <Flame className="w-4 h-4 text-amber-400" />
              Activity Recommendation
            </div>
            <span className="text-xs text-amber-400 font-medium">{activityRec}</span>
          </div>

          <div className="pt-2 border-t border-slate-800/80">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block mb-2">
              Personalized Wellness Focus:
            </span>
            <div className="flex flex-wrap gap-2">
              {wellnessFocus.map((focus, i) => (
                <span
                  key={i}
                  className="px-3 py-1 rounded-full bg-cyan-950/40 border border-cyan-500/30 text-cyan-300 text-xs font-medium"
                >
                  ✓ {focus}
                </span>
              ))}
            </div>
          </div>
        </div>

      </div>

    </div>
  );
}
