"use client";

import React, { useState } from "react";
import { FileText, Code, Eye, FileSearch } from "lucide-react";

interface DocumentViewerProps {
  fileName: string;
  fileType: string;
  documentType: string;
  extractedText: string;
  structuredData?: any;
}

export default function DocumentViewer({
  fileName,
  fileType,
  documentType,
  extractedText,
  structuredData
}: DocumentViewerProps) {
  const [tab, setTab] = useState<"text" | "json">("text");

  return (
    <div className="glass-panel p-5 rounded-3xl border border-slate-800 space-y-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2 text-xs font-bold text-white uppercase tracking-wider">
          <FileSearch className="w-4 h-4 text-cyan-400" />
          Extracted Document Inspection ({fileType.toUpperCase()})
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setTab("text")}
            className={`px-3 py-1 rounded-xl text-xs font-bold transition-all ${
              tab === "text"
                ? "bg-cyan-500 text-slate-950 font-bold shadow-md shadow-cyan-500/20"
                : "bg-slate-900 text-slate-400 hover:text-white"
            }`}
          >
            Raw OCR Text
          </button>
          <button
            onClick={() => setTab("json")}
            className={`px-3 py-1 rounded-xl text-xs font-bold transition-all ${
              tab === "json"
                ? "bg-cyan-500 text-slate-950 font-bold shadow-md shadow-cyan-500/20"
                : "bg-slate-900 text-slate-400 hover:text-white"
            }`}
          >
            Structured JSON
          </button>
        </div>
      </div>

      {tab === "text" ? (
        <div className="bg-slate-950/90 p-4 rounded-2xl border border-slate-800 max-h-60 overflow-y-auto font-mono text-xs text-slate-300 whitespace-pre-wrap leading-relaxed">
          {extractedText || "[No text extracted]"}
        </div>
      ) : (
        <pre className="bg-slate-950/90 p-4 rounded-2xl border border-slate-800 max-h-60 overflow-y-auto font-mono text-xs text-cyan-300 leading-relaxed">
          {JSON.stringify(structuredData || {}, null, 2)}
        </pre>
      )}
    </div>
  );
}
