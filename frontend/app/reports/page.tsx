"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import ReportUploader from "@/components/ReportUploader";
import Loader from "@/components/Loader";
import { 
  FileText, 
  Download, 
  Trash2, 
  Sparkles, 
  Eye, 
  Home, 
  MessageSquare, 
  History, 
  UserCheck, 
  Calendar,
  AlertTriangle,
  Pill,
  CheckCircle2
} from "lucide-react";
import { api } from "@/lib/api";
import { getToken } from "@/lib/auth";

export default function ReportsPage() {
  const router = useRouter();
  const [documents, setDocuments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedDoc, setSelectedDoc] = useState<any | null>(null);

  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.push("/login");
      return;
    }

    fetchDocuments();
  }, [router]);

  async function fetchDocuments() {
    try {
      const data = await api.listDocuments();
      setDocuments(data || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  const handleDelete = async (id: number) => {
    try {
      await api.deleteDocument(id);
      setDocuments(documents.filter((d) => d.id !== id));
      if (selectedDoc?.id === id) {
        setSelectedDoc(null);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

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
                <FileText className="w-6 h-6 text-cyan-400" />
              </div>
            </div>
            <div>
              <h1 className="text-2xl font-extrabold text-white flex items-center gap-2">
                Medical Reports & Document Intelligence
                <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-teal-500/20 text-teal-300 border border-teal-500/40">
                  OCR Engine Active
                </span>
              </h1>
              <p className="text-xs text-slate-300 mt-0.5">
                Upload prescriptions, lab reports, discharge summaries, or medicine photos for AI extraction.
              </p>
            </div>
          </div>

          <Link
            href="/chat"
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-teal-400 text-slate-950 text-xs font-extrabold hover:brightness-110 transition-all shadow-md shadow-cyan-500/20 shrink-0"
          >
            <MessageSquare className="w-4 h-4" />
            Ask AI About Uploads
          </Link>
        </div>

        {/* Universal Document Drag & Drop Uploader */}
        <ReportUploader onUploadSuccess={() => fetchDocuments()} />

        {/* Ingested Medical History Library */}
        <div className="space-y-4 pt-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-cyan-400" />
              Ingested Document Library ({documents.length})
            </h3>
          </div>

          {loading ? (
            <div className="py-8 text-center">
              <Loader label="Fetching uploaded document library..." />
            </div>
          ) : documents.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {documents.map((doc) => {
                const abnormalCount = doc.abnormal_values?.length || 0;
                const medsCount = doc.structured_data?.medicines?.length || 0;

                return (
                  <div
                    key={doc.id}
                    className="glass-panel p-5 rounded-3xl border border-slate-800 hover:border-cyan-500/40 transition-all flex flex-col justify-between space-y-4 group"
                  >
                    <div>
                      <div className="flex items-center justify-between text-xs text-slate-500 mb-2">
                        <span className="px-2.5 py-0.5 rounded-full bg-slate-800 text-cyan-300 font-bold uppercase text-[10px]">
                          {doc.document_type.replace('_', ' ')}
                        </span>
                        <span>{new Date(doc.created_at).toLocaleDateString()}</span>
                      </div>

                      <h4 className="font-extrabold text-white text-base group-hover:text-cyan-300 transition-colors">
                        {doc.file_name}
                      </h4>
                      <p className="text-xs text-slate-400 line-clamp-2 mt-1">
                        {doc.ai_summary || "Document parsed and archived."}
                      </p>
                    </div>

                    <div className="flex items-center gap-2 text-[11px] font-semibold text-slate-300 pt-2 border-t border-slate-800/80">
                      {abnormalCount > 0 && (
                        <span className="px-2 py-0.5 rounded-md bg-rose-500/20 text-rose-300 border border-rose-500/30 flex items-center gap-1">
                          <AlertTriangle className="w-3 h-3" />
                          {abnormalCount} Abnormal Lab Values
                        </span>
                      )}
                      {medsCount > 0 && (
                        <span className="px-2 py-0.5 rounded-md bg-teal-500/20 text-teal-300 border border-teal-500/30 flex items-center gap-1">
                          <Pill className="w-3 h-3" />
                          {medsCount} Medicines Detected
                        </span>
                      )}
                    </div>

                    {/* Actions Bar */}
                    <div className="flex items-center justify-between pt-2">
                      <a
                        href={`${API_BASE_URL}/documents/${doc.id}/download`}
                        target="_blank"
                        rel="noreferrer"
                        className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-700 text-slate-300 hover:text-white text-xs font-bold transition-all"
                      >
                        <Download className="w-3.5 h-3.5" />
                        Download
                      </a>

                      <button
                        onClick={() => handleDelete(doc.id)}
                        className="p-2 rounded-xl text-slate-500 hover:text-rose-400 hover:bg-rose-500/10 transition-all text-xs flex items-center gap-1"
                      >
                        <Trash2 className="w-4 h-4" />
                        Delete
                      </button>
                    </div>

                  </div>
                );
              })}
            </div>
          ) : (
            <div className="glass-panel p-8 rounded-3xl border border-slate-800 text-center text-xs text-slate-400">
              No documents uploaded yet. Drag & drop any medical record above to get started.
            </div>
          )}
        </div>

      </main>

      {/* Mobile Bottom Navigation Bar */}
      <nav className="fixed bottom-0 left-0 right-0 glass-panel border-t border-slate-800 py-3 px-6 flex items-center justify-around z-40 lg:hidden text-xs">
        <Link href="/dashboard" className="flex flex-col items-center text-slate-400 hover:text-cyan-400">
          <Home className="w-5 h-5" />
          <span>Home</span>
        </Link>
        <Link href="/reports" className="flex flex-col items-center text-cyan-400 font-bold">
          <FileText className="w-5 h-5" />
          <span>Reports</span>
        </Link>
        <Link href="/chat" className="flex flex-col items-center text-slate-400 hover:text-cyan-400">
          <MessageSquare className="w-5 h-5" />
          <span>Chat</span>
        </Link>
        <Link href="/timeline" className="flex flex-col items-center text-slate-400 hover:text-cyan-400">
          <Calendar className="w-5 h-5" />
          <span>Timeline</span>
        </Link>
      </nav>
    </div>
  );
}
