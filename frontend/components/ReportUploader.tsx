"use client";

import React, { useState, useRef } from "react";
import { UploadCloud, FileText, CheckCircle2, AlertCircle, RefreshCw, X, Eye, Sparkles } from "lucide-react";
import { api } from "@/lib/api";
import ExtractionProgress from "./ExtractionProgress";
import AnalysisCard from "./AnalysisCard";
import MedicationCard from "./MedicationCard";
import DocumentViewer from "./DocumentViewer";

interface ReportUploaderProps {
  onUploadSuccess?: (doc: any) => void;
}

export default function ReportUploader({ onUploadSuccess }: ReportUploaderProps) {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [processingStep, setProcessingStep] = useState<"upload" | "ocr" | "extraction" | "analysis" | "complete" | null>(null);
  const [processedDoc, setProcessedDoc] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const allowedFormats = ".pdf,.doc,.docx,.rtf,.txt,.csv,.xls,.xlsx,.jpg,.jpeg,.png,.webp,.tif,.tiff,.bmp,.heic,.heif";

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (file: File) => {
    setError(null);
    if (file.size > 20 * 1024 * 1024) {
      setError("File size exceeds maximum limit of 20 MB.");
      return;
    }
    setSelectedFile(file);
    startUploadPipeline(file);
  };

  const startUploadPipeline = async (file: File) => {
    setError(null);
    setProcessingStep("upload");
    setProcessedDoc(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      // Step 1 & 2: Upload & OCR
      setTimeout(() => setProcessingStep("ocr"), 600);
      setTimeout(() => setProcessingStep("extraction"), 1400);

      const res = await api.uploadDocument(formData);

      setProcessingStep("analysis");
      
      // Step 3: Fetch Full Document Details
      const fullDoc = await api.getDocument(res.document_id);
      
      setProcessingStep("complete");
      setProcessedDoc(fullDoc);

      if (onUploadSuccess) {
        onUploadSuccess(fullDoc);
      }
    } catch (err: any) {
      setError(err.message || "Document processing failed. Please retry.");
      setProcessingStep(null);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setProcessingStep(null);
    setProcessedDoc(null);
    setError(null);
  };

  return (
    <div className="space-y-6">
      
      {/* Upload Zone Card */}
      {!processedDoc && (
        <div
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          className={`glass-panel p-8 sm:p-10 rounded-3xl border-2 border-dashed cursor-pointer transition-all duration-300 text-center relative overflow-hidden ${
            dragActive
              ? "border-cyan-400 bg-cyan-950/40 shadow-2xl shadow-cyan-500/20 scale-[1.01]"
              : "border-slate-700/80 hover:border-cyan-500/50 hover:bg-slate-900/60"
          }`}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept={allowedFormats}
            onChange={handleFileChange}
            className="hidden"
          />

          <div className="flex flex-col items-center justify-center space-y-4">
            <div className="w-16 h-16 rounded-3xl bg-cyan-500/10 border border-cyan-400/30 flex items-center justify-center">
              <UploadCloud className="w-8 h-8 text-cyan-400" />
            </div>

            <div>
              <h3 className="text-lg font-extrabold text-white">
                Drag & Drop any Medical Document or Click to Upload
              </h3>
              <p className="text-xs text-slate-300 mt-1">
                Supports PDF, Word, Excel, CSV, Text, Scanned Receipts, Prescriptions & Image Formats (Max 20 MB)
              </p>
            </div>

            <div className="flex flex-wrap items-center justify-center gap-2 pt-2">
              {["PDF", "DOCX", "JPG / PNG", "EXCEL / CSV", "PRESCRIPTIONS", "LAB REPORTS"].map((tag, i) => (
                <span key={i} className="px-3 py-1 rounded-full bg-slate-800 border border-slate-700 text-slate-300 text-[10px] font-bold uppercase">
                  {tag}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="p-4 rounded-2xl bg-rose-950/40 border border-rose-500/40 text-rose-300 text-xs flex items-center justify-between">
          <div className="flex items-center gap-2">
            <AlertCircle className="w-5 h-5 shrink-0 text-rose-400" />
            <span>{error}</span>
          </div>
          <button
            onClick={handleReset}
            className="flex items-center gap-1 px-3 py-1 rounded-xl bg-slate-900 text-slate-200 hover:text-white text-xs font-bold"
          >
            <RefreshCw className="w-3.5 h-3.5" /> Retry
          </button>
        </div>
      )}

      {/* Live Processing Pipeline Stepper */}
      {processingStep && processingStep !== "complete" && (
        <ExtractionProgress currentStep={processingStep} />
      )}

      {/* Processed Results View */}
      {processedDoc && (
        <div className="space-y-6">
          
          {/* Top Reset / Re-upload Bar */}
          <div className="flex items-center justify-between p-4 glass-panel rounded-2xl border border-slate-800">
            <div className="flex items-center gap-3">
              <CheckCircle2 className="w-5 h-5 text-teal-400" />
              <div>
                <h4 className="font-bold text-white text-sm">{processedDoc.file_name}</h4>
                <p className="text-xs text-slate-400">
                  Processed on {new Date(processedDoc.created_at).toLocaleString()}
                </p>
              </div>
            </div>

            <button
              onClick={handleReset}
              className="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-800 text-slate-300 hover:text-cyan-400 hover:bg-slate-700 font-bold text-xs transition-all"
            >
              <UploadCloud className="w-4 h-4" />
              Upload Another Document
            </button>
          </div>

          {/* AI Clinical Analysis Card */}
          <AnalysisCard
            fileName={processedDoc.file_name}
            documentType={processedDoc.document_type}
            summary={processedDoc.ai_summary}
            abnormalValues={processedDoc.abnormal_values}
            recommendations={processedDoc.structured_data?.recommendations || ["Follow up with primary healthcare provider"]}
            redFlags={processedDoc.structured_data?.red_flags || []}
          />

          {/* Extracted Medications & Safety Warnings */}
          <MedicationCard
            medicines={processedDoc.structured_data?.medicines || []}
            warnings={processedDoc.structured_data?.warnings || []}
          />

          {/* Extracted OCR Document Inspector */}
          <DocumentViewer
            fileName={processedDoc.file_name}
            fileType={processedDoc.file_type}
            documentType={processedDoc.document_type}
            extractedText={processedDoc.extracted_text}
            structuredData={processedDoc.structured_data}
          />
        </div>
      )}

    </div>
  );
}
