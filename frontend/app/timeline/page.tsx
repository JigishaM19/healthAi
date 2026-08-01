"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import TimelineStats from "@/components/TimelineStats";
import TimelineFilters from "@/components/TimelineFilters";
import TimelineItem from "@/components/TimelineItem";
import Loader from "@/components/Loader";
import { 
  Activity, 
  Calendar, 
  Plus, 
  FileText, 
  Sparkles, 
  Home, 
  MessageSquare, 
  History, 
  UserCheck, 
  Layers,
  Filter
} from "lucide-react";
import { api } from "@/lib/api";
import { getToken } from "@/lib/auth";

export default function TimelinePage() {
  const router = useRouter();
  const [events, setEvents] = useState<any[]>([]);
  const [stats, setStats] = useState<any>({
    total_consultations: 0,
    reports_uploaded: 0,
    active_medications: 0,
    health_score: 85,
    last_consultation_date: null,
  });
  const [activeFilter, setActiveFilter] = useState("all");
  const [loading, setLoading] = useState(true);
  const [uploadingReport, setUploadingReport] = useState(false);

  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.push("/login");
      return;
    }

    fetchTimelineData(activeFilter);
  }, [activeFilter, router]);

  async function fetchTimelineData(filterType: string) {
    setLoading(true);
    try {
      const [eventsData, statsData] = await Promise.all([
        api.getTimelineEvents(filterType),
        api.getTimelineStats(),
      ]);
      setEvents(eventsData || []);
      setStats(statsData || {});
    } catch (err) {
      console.error("Timeline data load error:", err);
    } finally {
      setLoading(false);
    }
  }

  // Placeholder function for future report uploads
  const handleSimulateReportUpload = async () => {
    setUploadingReport(true);
    try {
      await api.createTimelineEvent({
        event_type: "report",
        title: "Blood Test & Lipid Panel Report",
        summary: "Uploaded lab PDF. Key extracted findings: Total Cholesterol 185 mg/dL (Normal), HbA1c 5.4% (Normal), Fasting Glucose 92 mg/dL.",
        details: {
          file_name: "lipid_panel_aug2026.pdf",
          extracted_findings: [
            "Total Cholesterol: 185 mg/dL",
            "HbA1c: 5.4% (Optimal)",
            "Fasting Glucose: 92 mg/dL"
          ]
        }
      });
      await fetchTimelineData(activeFilter);
    } catch (err) {
      console.error("Report simulation failed:", err);
    } finally {
      setUploadingReport(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0b1329] flex">
      {/* Desktop Sidebar */}
      <Sidebar />

      {/* Main Content Area */}
      <main className="flex-1 p-4 sm:p-8 max-w-6xl mx-auto space-y-8 pb-24 lg:pb-10">
        
        {/* Header Bar */}
        <div className="glass-panel p-6 rounded-3xl border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-cyan-500 via-teal-400 to-indigo-500 p-0.5 shadow-lg shadow-cyan-500/20 shrink-0">
              <div className="w-full h-full bg-[#0b1329] rounded-[14px] flex items-center justify-center">
                <Calendar className="w-6 h-6 text-cyan-400" />
              </div>
            </div>
            <div>
              <h1 className="text-2xl font-extrabold text-white flex items-center gap-2">
                Health Timeline
                <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-500/40">
                  Medical Record
                </span>
              </h1>
              <p className="text-xs text-slate-300 mt-0.5">
                Your personal chronological medical history, AI consultations, and lab records.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={handleSimulateReportUpload}
              disabled={uploadingReport}
              className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-slate-900 border border-indigo-500/50 text-indigo-300 text-xs font-bold hover:bg-indigo-500 hover:text-white transition-all shadow-md shadow-indigo-500/10"
            >
              <FileText className="w-4 h-4" />
              {uploadingReport ? "Processing..." : "+ Upload Lab Report"}
            </button>
            <Link
              href="/chat"
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-teal-400 text-slate-950 text-xs font-extrabold hover:brightness-110 transition-all shadow-md shadow-cyan-500/20"
            >
              <Plus className="w-4 h-4" />
              New Consultation
            </Link>
          </div>
        </div>

        {/* 1. Metric Stats Cards */}
        <TimelineStats stats={stats} />

        {/* 2. Category Filters */}
        <div className="glass-panel p-4 rounded-3xl border border-slate-800 space-y-2">
          <div className="flex items-center gap-2 text-xs font-bold text-slate-400 uppercase tracking-wider">
            <Filter className="w-3.5 h-3.5 text-cyan-400" />
            Filter Timeline Category:
          </div>
          <TimelineFilters
            activeFilter={activeFilter}
            onFilterChange={(f) => setActiveFilter(f)}
          />
        </div>

        {/* 3. Timeline Items Stream */}
        {loading ? (
          <div className="py-12 flex justify-center">
            <Loader label="Loading your medical timeline events..." />
          </div>
        ) : events.length > 0 ? (
          <div className="pt-4 pl-2 sm:pl-4">
            {events.map((evt, idx) => (
              <TimelineItem
                key={evt.id}
                item={evt}
                isLast={idx === events.length - 1}
              />
            ))}
          </div>
        ) : (
          /* Empty State */
          <div className="glass-panel p-12 rounded-3xl border border-slate-800 text-center max-w-lg mx-auto space-y-4 my-8">
            <div className="w-16 h-16 rounded-3xl bg-cyan-500/10 border border-cyan-400/30 flex items-center justify-center mx-auto">
              <Layers className="w-8 h-8 text-cyan-400" />
            </div>
            <h3 className="text-lg font-bold text-white">Your Health Timeline is empty</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Start a consultation or complete your health profile to begin building your personal medical history.
            </p>
            <div className="flex items-center justify-center gap-3 pt-2">
              <Link
                href="/chat"
                className="px-6 py-2.5 rounded-xl bg-cyan-500 text-slate-950 font-bold text-xs hover:brightness-110 transition-all shadow-md shadow-cyan-500/20"
              >
                Start AI Consultation
              </Link>
              <Link
                href="/onboarding"
                className="px-6 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-slate-200 font-semibold text-xs hover:border-cyan-400 transition-all"
              >
                Update Profile
              </Link>
            </div>
          </div>
        )}

      </main>

      {/* Mobile Bottom Navigation Bar */}
      <nav className="fixed bottom-0 left-0 right-0 glass-panel border-t border-slate-800 py-3 px-6 flex items-center justify-around z-40 lg:hidden text-xs">
        <Link href="/dashboard" className="flex flex-col items-center text-slate-400 hover:text-cyan-400">
          <Home className="w-5 h-5" />
          <span>Home</span>
        </Link>
        <Link href="/timeline" className="flex flex-col items-center text-cyan-400 font-bold">
          <Calendar className="w-5 h-5" />
          <span>Timeline</span>
        </Link>
        <Link href="/chat" className="flex flex-col items-center text-slate-400 hover:text-cyan-400">
          <MessageSquare className="w-5 h-5" />
          <span>Chat</span>
        </Link>
        <Link href="/history" className="flex flex-col items-center text-slate-400 hover:text-cyan-400">
          <History className="w-5 h-5" />
          <span>History</span>
        </Link>
      </nav>
    </div>
  );
}
