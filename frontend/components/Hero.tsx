"use client";

import React from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { Activity, ShieldCheck, Heart, Sparkles, Stethoscope, ArrowRight, CheckCircle2 } from "lucide-react";

export default function Hero() {
  return (
    <section className="relative overflow-hidden pt-12 pb-24 lg:pt-20 lg:pb-32">
      {/* Dynamic Background Glows */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-cyan-500/15 rounded-full blur-[140px] pointer-events-none" />
      <div className="absolute top-1/3 right-10 w-[400px] h-[400px] bg-indigo-500/10 rounded-full blur-[120px] pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          
          {/* Left Hero Column */}
          <motion.div 
            className="lg:col-span-7 space-y-8 text-left"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            {/* Pill Tag */}
            <div className="inline-flex items-center gap-2.5 px-4 py-2 rounded-full glass-panel border-cyan-500/30 text-cyan-300 text-xs font-semibold tracking-wide uppercase shadow-lg shadow-cyan-500/10">
              <Sparkles className="w-4 h-4 text-cyan-400 animate-spin" style={{ animationDuration: '8s' }} />
              Next-Gen Medical AI Guidance & Triage
            </div>

            {/* Main Title */}
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-white leading-[1.15]">
              HealthAI – Your Personal <br />
              <span className="text-gradient">AI Health Assistant</span>
            </h1>

            {/* Subtitle */}
            <p className="text-lg sm:text-xl text-slate-300 max-w-2xl font-normal leading-relaxed">
              Instant symptom guidance, wellness insights, and intelligent health support powered by AI tailored directly to your personal medical profile.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-wrap items-center gap-4 pt-2">
              <Link
                href="/signup"
                className="flex items-center gap-3 px-8 py-4 rounded-2xl bg-gradient-to-r from-cyan-500 via-teal-400 to-indigo-500 text-slate-950 font-extrabold text-base shadow-xl shadow-cyan-500/25 hover:scale-[1.03] transition-all duration-300"
              >
                Get Started Free
                <ArrowRight className="w-5 h-5" />
              </Link>
              <Link
                href="/login"
                className="flex items-center gap-2 px-7 py-4 rounded-2xl glass-panel text-slate-200 font-semibold text-base hover:border-cyan-500/50 hover:text-cyan-300 transition-all duration-300"
              >
                Login to Portal
              </Link>
            </div>

            {/* Trust Markers */}
            <div className="pt-6 grid grid-cols-3 gap-4 border-t border-slate-800/80 text-slate-400 text-xs font-medium">
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-cyan-400" />
                HIPAA & Privacy Aware
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-teal-400" />
                Personalized Profile AI
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-indigo-400" />
                24/7 Clinical Triage
              </div>
            </div>
          </motion.div>

          {/* Right Hero Column - Interactive Glass Mockup */}
          <motion.div 
            className="lg:col-span-5 relative"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            {/* Main Interactive Card */}
            <div className="glass-panel p-6 sm:p-8 rounded-3xl border border-slate-700/60 shadow-2xl relative z-10 backdrop-blur-2xl">
              <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-6">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-cyan-500/20 border border-cyan-400/40 flex items-center justify-center">
                    <Stethoscope className="w-5 h-5 text-cyan-400" />
                  </div>
                  <div>
                    <h3 className="font-bold text-white text-base">HealthAI Consultation</h3>
                    <p className="text-xs text-emerald-400 flex items-center gap-1">
                      <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
                      Live Triage Engine Connected
                    </p>
                  </div>
                </div>
                <span className="px-3 py-1 rounded-full bg-slate-800 text-cyan-300 text-xs font-semibold">
                  v2.4 AI
                </span>
              </div>

              {/* Chat Preview Snippet */}
              <div className="space-y-4">
                <div className="bg-slate-800/80 rounded-2xl p-4 border border-slate-700/50">
                  <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
                    User Query
                  </span>
                  <p className="text-sm text-slate-200">
                    "I've had a persistent headache and mild dizziness for 2 days. Should I be concerned?"
                  </p>
                </div>

                <div className="bg-cyan-950/40 rounded-2xl p-4 border border-cyan-500/30">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-bold text-cyan-400 flex items-center gap-1.5">
                      <Sparkles className="w-3.5 h-3.5" />
                      HealthAI Clinical Analysis
                    </span>
                    <span className="text-[11px] font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-md border border-emerald-500/20">
                      Confidence 92%
                    </span>
                  </div>
                  <p className="text-xs text-slate-300 leading-relaxed mb-3">
                    Based on your reported history of <span className="text-cyan-300 font-semibold">hypertension</span> during onboarding, monitor blood pressure closely.
                  </p>
                  
                  <div className="grid grid-cols-2 gap-2 text-[11px]">
                    <div className="bg-slate-900/80 p-2.5 rounded-xl border border-slate-800">
                      <span className="text-cyan-400 font-bold block mb-1">Recommended:</span>
                      • Rest & Hydrate (2.5L)<br />• Check Blood Pressure
                    </div>
                    <div className="bg-rose-950/30 p-2.5 rounded-xl border border-rose-500/30">
                      <span className="text-rose-400 font-bold block mb-1">Red Flags:</span>
                      • Sudden severe pain<br />• Vision changes
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Floating Healthcare Badges */}
            <motion.div 
              className="absolute -top-6 -left-6 glass-panel px-4 py-3 rounded-2xl border border-cyan-500/40 flex items-center gap-3 shadow-xl z-20 hidden sm:flex"
              animate={{ y: [0, -8, 0] }}
              transition={{ repeat: Infinity, duration: 5, ease: "easeInOut" }}
            >
              <div className="w-9 h-9 rounded-xl bg-rose-500/20 flex items-center justify-center">
                <Heart className="w-5 h-5 text-rose-400 fill-rose-400/30 animate-pulse" />
              </div>
              <div>
                <p className="text-[10px] text-slate-400 font-medium">Heart Rate</p>
                <p className="text-sm font-bold text-white">72 BPM <span className="text-xs font-normal text-emerald-400">Normal</span></p>
              </div>
            </motion.div>

            <motion.div 
              className="absolute -bottom-6 -right-6 glass-panel px-4 py-3 rounded-2xl border border-teal-500/40 flex items-center gap-3 shadow-xl z-20 hidden sm:flex"
              animate={{ y: [0, 8, 0] }}
              transition={{ repeat: Infinity, duration: 6, ease: "easeInOut" }}
            >
              <div className="w-9 h-9 rounded-xl bg-teal-500/20 flex items-center justify-center">
                <ShieldCheck className="w-5 h-5 text-teal-400" />
              </div>
              <div>
                <p className="text-[10px] text-slate-400 font-medium">Wellness Score</p>
                <p className="text-sm font-bold text-white">88 / 100 <span className="text-xs font-normal text-teal-400">Optimal</span></p>
              </div>
            </motion.div>

          </motion.div>

        </div>
      </div>
    </section>
  );
}
