"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Activity, Lock, Mail, User, ArrowRight, ShieldCheck, Sparkles, AlertCircle } from "lucide-react";
import { api } from "@/lib/api";
import { setToken, setUser } from "@/lib/auth";

interface AuthFormProps {
  mode: "login" | "signup";
}

export default function AuthForm({ mode }: AuthFormProps) {
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (mode === "signup" && password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);

    try {
      let res;
      if (mode === "signup") {
        res = await api.signup({ name, email, password });
      } else {
        res = await api.login({ email, password });
      }

      setToken(res.access_token);
      setUser(res.user);

      if (!res.has_profile) {
        router.push("/onboarding");
      } else {
        router.push("/dashboard");
      }
    } catch (err: any) {
      setError(err.message || "Authentication failed.");
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-[85vh] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 overflow-hidden">
      {/* Background Decorative Blur Orbs */}
      <div className="absolute top-10 left-10 w-96 h-96 bg-cyan-500/10 rounded-full blur-[130px] pointer-events-none" />
      <div className="absolute bottom-10 right-10 w-96 h-96 bg-indigo-500/10 rounded-full blur-[130px] pointer-events-none" />

      {/* Centered Glass Card */}
      <div className="w-full max-w-md glass-panel p-8 sm:p-10 rounded-3xl border border-slate-700/80 shadow-2xl relative z-10">
        
        {/* Brand Header */}
        <div className="text-center mb-8">
          <Link href="/" className="inline-flex items-center gap-3 mb-3">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-cyan-500 to-indigo-500 p-0.5 shadow-lg shadow-cyan-500/20">
              <div className="w-full h-full bg-[#0b1329] rounded-[14px] flex items-center justify-center">
                <Activity className="w-6 h-6 text-cyan-400" />
              </div>
            </div>
          </Link>
          <h2 className="text-2xl font-extrabold text-white">
            {mode === "login" ? "Welcome back to HealthAI" : "Create your HealthAI Account"}
          </h2>
          <p className="text-xs text-slate-300 mt-1">
            {mode === "login"
              ? "Access your personalized health insights & consultations"
              : "Start your journey to intelligent personalized healthcare"}
          </p>
        </div>

        {error && (
          <div className="mb-6 p-4 rounded-2xl bg-rose-950/40 border border-rose-500/40 text-rose-300 text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          
          {mode === "signup" && (
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-1.5">
                Full Name
              </label>
              <div className="relative">
                <User className="w-5 h-5 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  required
                  placeholder="Rahul Sharma"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full bg-slate-900/90 border border-slate-700/80 rounded-2xl pl-11 pr-4 py-3 text-slate-200 text-sm focus:border-cyan-400 focus:outline-none transition-colors"
                />
              </div>
            </div>
          )}

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-1.5">
              Email Address
            </label>
            <div className="relative">
              <Mail className="w-5 h-5 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="email"
                required
                placeholder="rahul@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-slate-900/90 border border-slate-700/80 rounded-2xl pl-11 pr-4 py-3 text-slate-200 text-sm focus:border-cyan-400 focus:outline-none transition-colors"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-1.5">
              Password
            </label>
            <div className="relative">
              <Lock className="w-5 h-5 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="password"
                required
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-slate-900/90 border border-slate-700/80 rounded-2xl pl-11 pr-4 py-3 text-slate-200 text-sm focus:border-cyan-400 focus:outline-none transition-colors"
              />
            </div>
          </div>

          {mode === "signup" && (
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-1.5">
                Confirm Password
              </label>
              <div className="relative">
                <Lock className="w-5 h-5 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
                <input
                  type="password"
                  required
                  placeholder="••••••••"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="w-full bg-slate-900/90 border border-slate-700/80 rounded-2xl pl-11 pr-4 py-3 text-slate-200 text-sm focus:border-cyan-400 focus:outline-none transition-colors"
                />
              </div>
            </div>
          )}

          {mode === "login" && (
            <div className="flex items-center justify-between text-xs text-slate-400 pt-1">
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" className="rounded bg-slate-900 border-slate-700 text-cyan-500 focus:ring-0" />
                Remember me
              </label>
              <a href="#" className="hover:text-cyan-400 transition-colors">
                Forgot Password?
              </a>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full mt-4 flex items-center justify-center gap-2 py-3.5 px-6 rounded-2xl bg-gradient-to-r from-cyan-500 via-teal-400 to-indigo-500 text-slate-950 font-extrabold text-sm shadow-xl shadow-cyan-500/20 hover:brightness-110 transition-all"
          >
            {loading ? (
              "Authenticating..."
            ) : (
              <>
                {mode === "login" ? "Sign In to Account" : "Create Account & Onboard"}
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        {/* Mode Switch Footer */}
        <div className="text-center mt-6 pt-6 border-t border-slate-800 text-xs text-slate-400">
          {mode === "login" ? (
            <span>
              Don't have an account?{" "}
              <Link href="/signup" className="text-cyan-400 font-bold hover:underline">
                Create Account
              </Link>
            </span>
          ) : (
            <span>
              Already registered?{" "}
              <Link href="/login" className="text-cyan-400 font-bold hover:underline">
                Login here
              </Link>
            </span>
          )}
        </div>

      </div>
    </div>
  );
}
