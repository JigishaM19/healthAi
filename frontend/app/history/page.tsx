"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import Loader from "@/components/Loader";
import { History, Trash2, ArrowRight, MessageSquare, Home, UserCheck } from "lucide-react";
import { api } from "@/lib/api";
import { getToken } from "@/lib/auth";

export default function HistoryPage() {
  const router = useRouter();
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.push("/login");
      return;
    }

    async function loadHistory() {
      try {
        const data = await api.getChatHistory();
        setHistory(data || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadHistory();
  }, [router]);

  const handleDelete = async (id: number) => {
    try {
      await api.deleteConversation(id);
      setHistory(history.filter((c) => c.id !== id));
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0b1329] flex items-center justify-center">
        <Loader label="Loading consultation records..." />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0b1329] flex">
      <Sidebar />

      <main className="flex-1 p-4 sm:p-8 max-w-5xl mx-auto space-y-6 pb-24 lg:pb-10">
        <div className="glass-panel p-6 rounded-3xl border border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-cyan-500/20 border border-cyan-400/40 flex items-center justify-center">
              <History className="w-5 h-5 text-cyan-400" />
            </div>
            <div>
              <h1 className="text-xl font-extrabold text-white">Consultation History</h1>
              <p className="text-xs text-slate-400">
                Review past AI triage responses and medical symptom assessments.
              </p>
            </div>
          </div>
        </div>

        {history.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {history.map((conv) => (
              <div
                key={conv.id}
                className="glass-panel p-5 rounded-3xl border border-slate-800 hover:border-cyan-500/40 transition-all flex flex-col justify-between space-y-4 group"
              >
                <div>
                  <div className="flex items-center justify-between text-xs text-slate-500 mb-2">
                    <span>{new Date(conv.created_at).toLocaleString()}</span>
                    <span className="bg-slate-800 text-cyan-300 px-2 py-0.5 rounded-full font-bold text-[10px]">
                      {conv.messages?.length || 0} Messages
                    </span>
                  </div>
                  <h3 className="font-bold text-white text-sm group-hover:text-cyan-300 transition-colors">
                    {conv.title}
                  </h3>
                </div>

                <div className="flex items-center justify-between pt-3 border-t border-slate-800/80">
                  <button
                    onClick={() => handleDelete(conv.id)}
                    className="p-2 rounded-xl text-slate-500 hover:text-rose-400 hover:bg-rose-500/10 transition-all text-xs flex items-center gap-1"
                  >
                    <Trash2 className="w-4 h-4" />
                    Delete
                  </button>

                  <Link
                    href={`/chat?id=${conv.id}`}
                    className="flex items-center gap-1 text-xs font-bold text-cyan-400 hover:underline"
                  >
                    Open Session
                    <ArrowRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="glass-panel p-12 rounded-3xl border border-slate-800 text-center space-y-3">
            <History className="w-10 h-10 text-slate-600 mx-auto" />
            <h3 className="text-base font-bold text-white">No Consultations Yet</h3>
            <p className="text-xs text-slate-400">
              Start your first session with HealthAI to generate medical advice.
            </p>
            <Link
              href="/chat"
              className="inline-block px-6 py-2.5 rounded-xl bg-cyan-500 text-slate-950 font-bold text-xs"
            >
              Start New Consultation
            </Link>
          </div>
        )}
      </main>

      {/* Mobile Bottom Navigation Bar */}
      <nav className="fixed bottom-0 left-0 right-0 glass-panel border-t border-slate-800 py-3 px-6 flex items-center justify-around z-40 lg:hidden text-xs">
        <Link href="/dashboard" className="flex flex-col items-center text-slate-400 hover:text-cyan-400">
          <Home className="w-5 h-5" />
          <span>Home</span>
        </Link>
        <Link href="/chat" className="flex flex-col items-center text-slate-400 hover:text-cyan-400">
          <MessageSquare className="w-5 h-5" />
          <span>Chat</span>
        </Link>
        <Link href="/history" className="flex flex-col items-center text-cyan-400 font-bold">
          <History className="w-5 h-5" />
          <span>History</span>
        </Link>
        <Link href="/health-profile" className="flex flex-col items-center text-slate-400 hover:text-cyan-400">
          <UserCheck className="w-5 h-5" />
          <span>Health</span>
        </Link>
      </nav>
    </div>
  );
}
