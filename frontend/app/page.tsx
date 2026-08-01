"use client";

import React from "react";
import Link from "next/link";
import Navbar from "@/components/Navbar";
import Hero from "@/components/Hero";
import FeatureCard from "@/components/FeatureCard";
import { 
  Stethoscope, 
  Brain, 
  Sparkles, 
  UserCheck, 
  History, 
  ShieldCheck, 
  Clock, 
  CheckCircle2, 
  ArrowRight,
  Heart,
  MessageSquare
} from "lucide-react";

export default function LandingPage() {
  const features = [
    {
      icon: Stethoscope,
      title: "AI Symptom Analysis",
      description: "Instant medical triage classifying symptoms into emergency, mental health, or general practice wards.",
      accentColor: "from-cyan-500 to-teal-400"
    },
    {
      icon: Brain,
      title: "Medical Guidance",
      description: "Context-aware clinical explanations offering probable causes and actionable wellness recommendations.",
      accentColor: "from-indigo-500 to-purple-500"
    },
    {
      icon: Sparkles,
      title: "Wellness Recommendations",
      description: "Tailored hydration, sleep, and physical activity goals designed around your personal health index.",
      accentColor: "from-teal-400 to-emerald-500"
    },
    {
      icon: UserCheck,
      title: "Health Profile Personalization",
      description: "AI automatically factors in your chronic conditions, allergies, current medications, and health goals.",
      accentColor: "from-cyan-400 to-indigo-500"
    },
    {
      icon: History,
      title: "Conversation History",
      description: "Secure persistent logging of past health consultations for seamless follow-up analysis.",
      accentColor: "from-amber-400 to-orange-500"
    },
    {
      icon: ShieldCheck,
      title: "Secure & Private",
      description: "JWT authenticated architecture with encrypted medical profile fields and strict data privacy.",
      accentColor: "from-emerald-400 to-teal-600"
    },
    {
      icon: Clock,
      title: "24/7 Assistance",
      description: "Always-on clinical AI ready to provide guidance whenever symptoms or health questions arise.",
      accentColor: "from-cyan-500 to-blue-600"
    }
  ];

  const steps = [
    { num: "01", title: "Create an account", desc: "Fast signup with email and encrypted security." },
    { num: "02", title: "Complete your Health Profile", desc: "5-step wizard capturing conditions, medications & goals." },
    { num: "03", title: "Describe your symptoms", desc: "Type or select symptoms in our ChatGPT-style interface." },
    { num: "04", title: "AI analyzes using personal data", desc: "Smart engine factors in your medical background." },
    { num: "05", title: "Receive personalized guidance", desc: "Get probable causes, red flags & doctor triage." }
  ];

  const testimonials = [
    {
      name: "Sarah Jenkins",
      role: "Fitness Enthusiast",
      quote: "HealthAI identified my dehydration-triggered migraines immediately by looking at my water intake during onboarding!",
      avatar: "👩‍⚕️"
    },
    {
      name: "Marcus Vance",
      role: "Software Engineer",
      quote: "The ChatGPT-style consultation paired with my health profile makes this feel like having a doctor in my pocket 24/7.",
      avatar: "👨‍💻"
    },
    {
      name: "Dr. Elena Rostova",
      role: "Clinical Advisor",
      quote: "The triage ward classification (Emergency vs General vs Mental Health) ensures patient safety before anything else.",
      avatar: "🩺"
    }
  ];

  return (
    <div className="min-h-screen bg-[#0b1329] text-slate-100 flex flex-col justify-between">
      <div>
        <Navbar />
        <Hero />

        {/* FEATURES SECTION */}
        <section id="features" className="py-20 relative">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-3xl mx-auto mb-16 space-y-4">
              <span className="text-xs font-bold uppercase tracking-widest text-cyan-400 bg-cyan-500/10 px-4 py-1.5 rounded-full border border-cyan-500/30">
                Core Capabilities
              </span>
              <h2 className="text-3xl sm:text-4xl font-extrabold text-white">
                Intelligent Medical AI <span className="text-gradient">Features</span>
              </h2>
              <p className="text-slate-400 text-base">
                Engineered with clinical safety guardrails, context awareness, and personalized wellness scoring.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {features.map((feat, idx) => (
                <FeatureCard
                  key={idx}
                  icon={feat.icon}
                  title={feat.title}
                  description={feat.description}
                  accentColor={feat.accentColor}
                  delay={idx * 0.1}
                />
              ))}
            </div>
          </div>
        </section>

        {/* HOW IT WORKS SECTION */}
        <section id="how-it-works" className="py-20 bg-slate-950/60 border-y border-slate-800/80 relative">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-3xl mx-auto mb-16 space-y-4">
              <span className="text-xs font-bold uppercase tracking-widest text-teal-400 bg-teal-500/10 px-4 py-1.5 rounded-full border border-teal-500/30">
                Simple Workflow
              </span>
              <h2 className="text-3xl sm:text-4xl font-extrabold text-white">
                How HealthAI <span className="text-gradient">Works</span>
              </h2>
              <p className="text-slate-400 text-base">
                From onboarding to consultation in 5 seamless steps.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
              {steps.map((st, i) => (
                <div
                  key={i}
                  className="glass-panel p-6 rounded-3xl border border-slate-800 flex flex-col justify-between relative group hover:border-cyan-500/40 transition-all"
                >
                  <span className="text-3xl font-black text-cyan-500/40 group-hover:text-cyan-400 transition-colors mb-4 block">
                    {st.num}
                  </span>
                  <div>
                    <h3 className="font-bold text-white text-base mb-2">{st.title}</h3>
                    <p className="text-xs text-slate-400 leading-relaxed">{st.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* TESTIMONIALS SECTION */}
        <section id="testimonials" className="py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-3xl mx-auto mb-16 space-y-4">
              <span className="text-xs font-bold uppercase tracking-widest text-indigo-400 bg-indigo-500/10 px-4 py-1.5 rounded-full border border-indigo-500/30">
                Trusted Experience
              </span>
              <h2 className="text-3xl sm:text-4xl font-extrabold text-white">
                What Users & Doctors <span className="text-gradient">Say</span>
              </h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {testimonials.map((t, idx) => (
                <div key={idx} className="glass-panel p-8 rounded-3xl border border-slate-800 space-y-4">
                  <div className="text-3xl">{t.avatar}</div>
                  <p className="text-sm text-slate-300 italic leading-relaxed">
                    "{t.quote}"
                  </p>
                  <div className="pt-4 border-t border-slate-800">
                    <h4 className="font-bold text-white text-sm">{t.name}</h4>
                    <span className="text-xs text-cyan-400">{t.role}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA BANNER */}
        <section className="py-16">
          <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="glass-panel p-10 rounded-3xl border border-cyan-500/40 text-center space-y-6 bg-gradient-to-r from-cyan-950/40 via-teal-950/30 to-indigo-950/40 relative overflow-hidden">
              <h2 className="text-3xl font-extrabold text-white">
                Ready to Experience Next-Gen Healthcare AI?
              </h2>
              <p className="text-slate-300 max-w-xl mx-auto text-sm">
                Get started today in less than 2 minutes. Complete your health profile and talk to HealthAI.
              </p>
              <Link
                href="/signup"
                className="inline-flex items-center gap-3 px-8 py-4 rounded-2xl bg-gradient-to-r from-cyan-500 to-teal-400 text-slate-950 font-extrabold text-base shadow-xl shadow-cyan-500/20 hover:scale-105 transition-all"
              >
                Start Free Consultation
                <ArrowRight className="w-5 h-5" />
              </Link>
            </div>
          </div>
        </section>
      </div>

      {/* FOOTER */}
      <footer className="border-t border-slate-800 bg-[#070d1e] py-12 text-xs text-slate-400">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-3">
            <span className="text-lg font-bold text-white">Health<span className="text-gradient">AI</span></span>
            <span>© 2026 HealthAI Inc. All rights reserved.</span>
          </div>

          <div className="flex items-center gap-6">
            <a href="#" className="hover:text-cyan-400 transition-colors">About</a>
            <a href="#" className="hover:text-cyan-400 transition-colors">Privacy Policy</a>
            <a href="#" className="hover:text-cyan-400 transition-colors">Contact</a>
            <a href="#" className="hover:text-cyan-400 transition-colors">Terms of Service</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
