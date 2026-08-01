"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Activity, Shield, User, LogOut, Moon, Sun, ChevronRight, Menu, X } from "lucide-react";
import { getToken, removeToken, getUser } from "@/lib/auth";

export default function Navbar() {
  const router = useRouter();
  const [token, setTokenState] = useState<string | null>(null);
  const [user, setUserState] = useState<any>(null);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [darkMode, setDarkMode] = useState(true);

  useEffect(() => {
    setTokenState(getToken());
    setUserState(getUser());
  }, []);

  const handleLogout = () => {
    removeToken();
    setTokenState(null);
    setUserState(null);
    router.push("/login");
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    if (darkMode) {
      document.documentElement.classList.remove("dark");
    } else {
      document.documentElement.classList.add("dark");
    }
  };

  return (
    <header className="sticky top-0 z-50 backdrop-blur-xl bg-[#0b1329]/80 border-b border-slate-800/80 transition-all duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          
          {/* Brand Logo */}
          <Link href="/" className="flex items-center gap-3 group">
            <div className="w-11 h-11 rounded-xl bg-gradient-to-tr from-cyan-500 via-teal-400 to-indigo-500 p-0.5 shadow-lg shadow-cyan-500/20 group-hover:scale-105 transition-transform duration-300">
              <div className="w-full h-full bg-[#0b1329] rounded-[10px] flex items-center justify-center">
                <Activity className="w-6 h-6 text-cyan-400 animate-pulse" />
              </div>
            </div>
            <div className="flex flex-col">
              <span className="text-2xl font-extrabold tracking-tight text-white flex items-center gap-1">
                Health<span className="text-gradient">AI</span>
              </span>
              <span className="text-[10px] text-cyan-400 font-medium tracking-widest uppercase -mt-1">
                AI Clinical Assistant
              </span>
            </div>
          </Link>

          {/* Desktop Navigation Links */}
          <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-300">
            <Link href="/#features" className="hover:text-cyan-400 transition-colors">
              Features
            </Link>
            <Link href="/#how-it-works" className="hover:text-cyan-400 transition-colors">
              How it Works
            </Link>
            <Link href="/#testimonials" className="hover:text-cyan-400 transition-colors">
              Testimonials
            </Link>
          </nav>

          {/* User Auth Controls */}
          <div className="hidden md:flex items-center gap-4">
            <button
              onClick={toggleDarkMode}
              className="p-2 rounded-xl bg-slate-800/60 border border-slate-700/50 text-slate-300 hover:text-cyan-400 transition-all hover:scale-105"
              aria-label="Toggle theme"
            >
              {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </button>

            {token ? (
              <div className="flex items-center gap-3">
                <Link
                  href="/dashboard"
                  className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-teal-500 text-slate-950 font-semibold hover:brightness-110 transition-all shadow-md shadow-cyan-500/20"
                >
                  <User className="w-4 h-4" />
                  Dashboard
                </Link>
                <button
                  onClick={handleLogout}
                  className="p-2 rounded-xl bg-slate-800/60 border border-slate-700/50 text-slate-400 hover:text-rose-400 transition-all hover:bg-rose-500/10"
                  title="Logout"
                >
                  <LogOut className="w-5 h-5" />
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-3">
                <Link
                  href="/login"
                  className="px-5 py-2.5 rounded-xl border border-slate-700/70 text-slate-200 hover:border-cyan-500 hover:text-cyan-400 font-medium transition-all"
                >
                  Login
                </Link>
                <Link
                  href="/signup"
                  className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 via-teal-400 to-indigo-500 text-slate-950 font-bold hover:opacity-95 transition-all shadow-lg shadow-cyan-500/25 hover:scale-[1.02]"
                >
                  Get Started
                  <ChevronRight className="w-4 h-4" />
                </Link>
              </div>
            )}
          </div>

          {/* Mobile Menu Toggle */}
          <div className="flex md:hidden items-center gap-2">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-xl bg-slate-800 text-slate-200"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden glass-panel border-b border-slate-800 px-6 py-6 space-y-4">
          <Link
            href="/#features"
            onClick={() => setMobileMenuOpen(false)}
            className="block text-slate-300 hover:text-cyan-400 py-1"
          >
            Features
          </Link>
          <Link
            href="/#how-it-works"
            onClick={() => setMobileMenuOpen(false)}
            className="block text-slate-300 hover:text-cyan-400 py-1"
          >
            How it Works
          </Link>
          <Link
            href="/#testimonials"
            onClick={() => setMobileMenuOpen(false)}
            className="block text-slate-300 hover:text-cyan-400 py-1"
          >
            Testimonials
          </Link>

          <div className="pt-4 border-t border-slate-800 space-y-3">
            {token ? (
              <>
                <Link
                  href="/dashboard"
                  onClick={() => setMobileMenuOpen(false)}
                  className="block w-full text-center py-3 rounded-xl bg-cyan-500 text-slate-950 font-bold"
                >
                  Go to Dashboard
                </Link>
                <button
                  onClick={() => {
                    handleLogout();
                    setMobileMenuOpen(false);
                  }}
                  className="block w-full text-center py-3 rounded-xl bg-rose-500/20 text-rose-300 font-medium"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link
                  href="/login"
                  onClick={() => setMobileMenuOpen(false)}
                  className="block w-full text-center py-3 rounded-xl border border-slate-700 text-slate-200"
                >
                  Login
                </Link>
                <Link
                  href="/signup"
                  onClick={() => setMobileMenuOpen(false)}
                  className="block w-full text-center py-3 rounded-xl bg-cyan-400 text-slate-950 font-bold"
                >
                  Create Account
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </header>
  );
}
