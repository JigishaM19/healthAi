"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import HealthScoreCard from "@/components/HealthScoreCard";
import Loader from "@/components/Loader";
import { 
  MessageSquare, 
  Plus, 
  History, 
  Activity, 
  Pill, 
  Droplet, 
  Bookmark, 
  User, 
  Sparkles,
  ArrowRight,
  ShieldCheck,
  Home,
  FileText,
  UserCheck
} from "lucide-react";
import { api } from "@/lib/api";
import { getToken, getUser } from "@/lib/auth";
import { useLanguage } from "@/context/LanguageContext";

export default function DashboardPage() {
  const router = useRouter();
  const { t } = useLanguage();
  const [user, setUserState] = useState<any>(null);
  const [summary, setSummary] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.push("/login");
      return;
    }
    setUserState(getUser());

    async function loadData() {
      try {
        const [sumRes, histRes] = await Promise.all([
          api.getHealthSummary(),
          api.getChatHistory(),
        ]);
        setSummary(sumRes);
        setHistory(histRes || []);
      } catch (err) {
        console.error("Dashboard error:", err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [router]);

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0b1329] flex items-center justify-center">
        <Loader label="Loading your personalized health dashboard..." />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0b1329] flex">
      {/* Desktop Sidebar */}
      <Sidebar />

      {/* Main Content Area */}
      <main className="flex-1 p-4 sm:p-8 lg:p-10 max-w-7xl mx-auto space-y-8 pb-24 lg:pb-10">
        
        {/* Welcome Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 glass-panel p-6 sm:p-8 rounded-3xl border border-slate-800">
          <div>
            <span className="text-xs font-bold text-cyan-400 uppercase tracking-widest block mb-1">
              {t("healthSummary")}
            </span>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white">
              {t("welcomeBack")}, <span className="text-gradient">{user?.name || "Friend"}</span> 👋
            </h1>
            <p className="text-xs sm:text-sm text-slate-300 mt-1">
              Here is your daily medical intelligence summary & wellness status.
            </p>
          </div>

          <Link
            href="/chat"
            className="inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-2xl bg-gradient-to-r from-cyan-500 via-teal-400 to-indigo-500 text-slate-950 font-extrabold text-sm shadow-xl shadow-cyan-500/20 hover:scale-[1.02] transition-all shrink-0"
          >
            <Plus className="w-5 h-5" />
            {t("consultation")}
          </Link>
        </div>

        {/* Health Score & Vitals Section */}
        {summary && (
          <HealthScoreCard
            score={summary.health_score}
            bmi={summary.bmi}
            bmiCategory={summary.bmi_category}
            hydrationGoal={summary.hydration_goal}
            activityRec={summary.activity_recommendation}
            sleepTarget={summary.sleep_target}
            wellnessFocus={summary.personalized_wellness_focus}
          />
        )}

        {/* Action Prompt Banner */}
        <div className="glass-panel p-6 rounded-3xl border border-cyan-500/30 bg-gradient-to-r from-cyan-950/40 to-teal-950/30 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-2xl bg-cyan-500/20 border border-cyan-400/40 flex items-center justify-center shrink-0">
              <Sparkles className="w-6 h-6 text-cyan-400" />
            </div>
            <div>
              <h3 className="font-bold text-white text-sm">Suggested AI Health Prompt</h3>
              <p className="text-xs text-cyan-200 italic">
                "{summary?.suggested_consultation || "How can I improve my energy levels?"}"
              </p>
            </div>
          </div>
          <Link
            href="/chat"
            className="px-5 py-2.5 rounded-xl bg-slate-900 border border-cyan-500/50 text-cyan-300 text-xs font-bold hover:bg-cyan-500 hover:text-slate-950 transition-all shrink-0"
          >
            Ask HealthAI →
          </Link>
        </div>

        {/* Health Overview Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          {/* Active Medications */}
          <div className="glass-panel p-6 rounded-3xl border border-slate-800 space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="p-2.5 rounded-2xl bg-indigo-500/10 border border-indigo-500/30 text-indigo-400">
                  <Pill className="w-5 h-5" />
                </div>
                <h3 className="font-bold text-white text-sm">{t("activeMedications")}</h3>
              </div>
              <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-indigo-500/20 text-indigo-300">
                {summary?.medications?.length || 0}
              </span>
            </div>

            <div className="space-y-2">
              {summary?.medications?.length > 0 ? (
                summary.medications.map((med: string, i: number) => (
                  <div key={i} className="p-3 rounded-2xl bg-slate-900/60 border border-slate-800/80 text-xs text-slate-200 flex items-center justify-between font-medium">
                    <span>{med}</span>
                    <span className="text-[10px] text-indigo-400 font-bold">Active</span>
                  </div>
                ))
              ) : (
                <p className="text-xs text-slate-400 italic">No active medications registered.</p>
              )}
            </div>
          </div>

          {/* Known Conditions */}
          <div className="glass-panel p-6 rounded-3xl border border-slate-800 space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="p-2.5 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
                  <Activity className="w-5 h-5" />
                </div>
                <h3 className="font-bold text-white text-sm">{t("conditions")}</h3>
              </div>
              <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-cyan-500/20 text-cyan-300">
                {summary?.conditions?.length || 0}
              </span>
            </div>

            <div className="space-y-2">
              {summary?.conditions?.length > 0 ? (
                summary.conditions.map((cond: string, i: number) => (
                  <div key={i} className="p-3 rounded-2xl bg-slate-900/60 border border-slate-800/80 text-xs text-slate-200 flex items-center justify-between font-medium">
                    <span>{cond}</span>
                    <span className="text-[10px] text-cyan-400 font-bold">Monitored</span>
                  </div>
                ))
              ) : (
                <p className="text-xs text-slate-400 italic">No chronic medical conditions listed.</p>
              )}
            </div>
          </div>

          {/* Allergies & Sensitivities */}
          <div className="glass-panel p-6 rounded-3xl border border-slate-800 space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="p-2.5 rounded-2xl bg-rose-500/10 border border-rose-500/30 text-rose-400">
                  <Bookmark className="w-5 h-5" />
                </div>
                <h3 className="font-bold text-white text-sm">{t("allergies")}</h3>
              </div>
              <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-rose-500/20 text-rose-300">
                {summary?.allergies?.length || 0}
              </span>
            </div>

            <div className="space-y-2">
              {summary?.allergies?.length > 0 ? (
                summary.allergies.map((all: string, i: number) => (
                  <div key={i} className="p-3 rounded-2xl bg-slate-900/60 border border-slate-800/80 text-xs text-slate-200 flex items-center justify-between font-medium">
                    <span>{all}</span>
                    <span className="text-[10px] text-rose-400 font-bold">Avoid</span>
                  </div>
                ))
              ) : (
                <p className="text-xs text-slate-400 italic">No known drug/food allergies registered.</p>
              )}
            </div>
          </div>

        </div>

      </main>

      {/* Mobile Bottom Navigation Bar */}
      <nav className="fixed bottom-0 left-0 right-0 glass-panel border-t border-slate-800 py-3 px-6 flex items-center justify-around z-40 lg:hidden text-xs">
        <Link href="/dashboard" className="flex flex-col items-center text-cyan-400 font-bold">
          <Home className="w-5 h-5" />
          <span>{t("dashboard")}</span>
        </Link>
        <Link href="/chat" className="flex flex-col items-center text-slate-400 hover:text-cyan-400">
          <MessageSquare className="w-5 h-5" />
          <span>{t("chat")}</span>
        </Link>
        <Link href="/timeline" className="flex flex-col items-center text-slate-400 hover:text-cyan-400">
          <FileText className="w-5 h-5" />
          <span>{t("timeline")}</span>
        </Link>
        <Link href="/settings" className="flex flex-col items-center text-slate-400 hover:text-cyan-400">
          <UserCheck className="w-5 h-5" />
          <span>{t("settings")}</span>
        </Link>
      </nav>
    </div>
  );
}
