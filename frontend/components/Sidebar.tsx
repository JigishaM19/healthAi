"use client";

import React from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { 
  LayoutDashboard, 
  MessageSquare, 
  UserCheck, 
  History, 
  Settings, 
  LogOut, 
  Activity,
  Heart,
  ChevronRight,
  Calendar,
  FileText
} from "lucide-react";
import { removeToken } from "@/lib/auth";
import { useLanguage } from "@/context/LanguageContext";

export default function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();
  const { t } = useLanguage();

  const handleLogout = () => {
    removeToken();
    router.push("/login");
  };

  const navItems = [
    { label: t("dashboard"), href: "/dashboard", icon: LayoutDashboard },
    { label: t("timeline"), href: "/timeline", icon: Calendar },
    { label: t("medicalReports"), href: "/reports", icon: FileText },
    { label: t("consultation"), href: "/chat", icon: MessageSquare },
    { label: t("healthProfile"), href: "/health-profile", icon: UserCheck },
    { label: t("consultationHistory") || "Consultation History", href: "/history", icon: History },
    { label: t("settings"), href: "/settings", icon: Settings },
  ];

  return (
    <aside className="w-64 glass-panel border-r border-slate-800/80 h-screen sticky top-0 flex flex-col justify-between p-6 z-30 hidden lg:flex">
      <div>
        {/* Brand Header */}
        <Link href="/" className="flex items-center gap-3 mb-10 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-indigo-500 p-0.5 shadow-lg shadow-cyan-500/20 group-hover:scale-105 transition-transform">
            <div className="w-full h-full bg-[#0b1329] rounded-[10px] flex items-center justify-center">
              <Activity className="w-5 h-5 text-cyan-400" />
            </div>
          </div>
          <div className="flex flex-col">
            <span className="text-xl font-extrabold tracking-tight text-white">
              Health<span className="text-gradient">AI</span>
            </span>
            <span className="text-[9px] text-cyan-400 font-semibold tracking-widest uppercase -mt-1">
              Portal v2.4
            </span>
          </div>
        </Link>

        {/* Navigation Items */}
        <nav className="space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;

            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center justify-between px-4 py-3.5 rounded-2xl font-medium text-sm transition-all duration-200 ${
                  isActive
                    ? "bg-gradient-to-r from-cyan-500/20 to-teal-500/10 border border-cyan-500/40 text-cyan-300 shadow-md shadow-cyan-500/10 font-bold"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon className={`w-5 h-5 ${isActive ? "text-cyan-400" : "text-slate-400"}`} />
                  <span>{item.label}</span>
                </div>
                {isActive && <ChevronRight className="w-4 h-4 text-cyan-400" />}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Emergency & Logout Footer */}
      <div className="space-y-4 pt-6 border-t border-slate-800/80">
        
        {/* Quick Emergency Card */}
        <div className="p-3.5 rounded-2xl bg-rose-950/20 border border-rose-500/30 text-rose-300 text-xs">
          <div className="flex items-center gap-2 font-bold mb-1">
            <Heart className="w-4 h-4 text-rose-400 animate-pulse" />
            Medical Emergency?
          </div>
          <p className="text-[11px] text-slate-400">
            For urgent life-threatening symptoms, dial <strong>911</strong> immediately.
          </p>
        </div>

        <button
          onClick={handleLogout}
          className="flex items-center gap-3 w-full px-4 py-3 rounded-2xl text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 font-medium text-sm transition-all border border-transparent hover:border-rose-500/30"
        >
          <LogOut className="w-5 h-5" />
          {t("logout")}
        </button>
      </div>
    </aside>
  );
}
