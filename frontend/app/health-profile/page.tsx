"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import Loader from "@/components/Loader";
import { UserCheck, Activity, Save, AlertCircle, Heart, Flame, ShieldCheck, Home, MessageSquare, History } from "lucide-react";
import { api } from "@/lib/api";
import { getToken } from "@/lib/auth";
import Link from "next/link";

export default function HealthProfilePage() {
  const router = useRouter();
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.push("/login");
      return;
    }

    async function fetchProfile() {
      try {
        const data = await api.getHealthProfile();
        setProfile(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    fetchProfile();
  }, [router]);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setMessage(null);
    try {
      const updated = await api.updateHealthProfile(profile);
      setProfile(updated);
      setMessage("Health Profile updated successfully!");
    } catch (err: any) {
      setMessage(`Failed: ${err.message}`);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0b1329] flex items-center justify-center">
        <Loader label="Loading your medical health profile..." />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0b1329] flex">
      <Sidebar />

      <main className="flex-1 p-4 sm:p-8 max-w-5xl mx-auto space-y-8 pb-24 lg:pb-10">
        
        {/* Header */}
        <div className="glass-panel p-6 rounded-3xl border border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-cyan-500/20 border border-cyan-400/40 flex items-center justify-center">
              <UserCheck className="w-5 h-5 text-cyan-400" />
            </div>
            <div>
              <h1 className="text-xl font-extrabold text-white">Your Health Profile</h1>
              <p className="text-xs text-slate-400">
                Manage chronic conditions, medications, allergies, and lifestyle factors.
              </p>
            </div>
          </div>

          <button
            onClick={handleSave}
            disabled={saving}
            className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-teal-400 text-slate-950 font-bold text-xs hover:brightness-110 transition-all shadow-md shadow-cyan-500/20"
          >
            <Save className="w-4 h-4" />
            {saving ? "Saving..." : "Save Changes"}
          </button>
        </div>

        {message && (
          <div className="p-4 rounded-2xl bg-cyan-950/40 border border-cyan-500/40 text-cyan-300 text-xs">
            {message}
          </div>
        )}

        {profile && (
          <form onSubmit={handleSave} className="space-y-6">
            
            {/* Basic Info */}
            <div className="glass-panel p-6 rounded-3xl border border-slate-800 space-y-4">
              <h3 className="text-sm font-bold text-white flex items-center gap-2 uppercase tracking-wider text-cyan-400">
                Basic Physical Measurements
              </h3>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
                <div>
                  <label className="block text-slate-400 font-semibold mb-1">Age</label>
                  <input
                    type="number"
                    value={profile.age || 30}
                    onChange={(e) => setProfile({ ...profile, age: Number(e.target.value) })}
                    className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-white"
                  />
                </div>
                <div>
                  <label className="block text-slate-400 font-semibold mb-1">Gender</label>
                  <select
                    value={profile.gender || "Male"}
                    onChange={(e) => setProfile({ ...profile, gender: e.target.value })}
                    className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-white"
                  >
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
                <div>
                  <label className="block text-slate-400 font-semibold mb-1">Height (cm)</label>
                  <input
                    type="number"
                    value={profile.height_cm || 170}
                    onChange={(e) => setProfile({ ...profile, height_cm: Number(e.target.value) })}
                    className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-white"
                  />
                </div>
                <div>
                  <label className="block text-slate-400 font-semibold mb-1">Weight (kg)</label>
                  <input
                    type="number"
                    value={profile.weight_kg || 70}
                    onChange={(e) => setProfile({ ...profile, weight_kg: Number(e.target.value) })}
                    className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-white"
                  />
                </div>
              </div>
            </div>

            {/* Medical Background */}
            <div className="glass-panel p-6 rounded-3xl border border-slate-800 space-y-4">
              <h3 className="text-sm font-bold text-white flex items-center gap-2 uppercase tracking-wider text-teal-400">
                Medical Background & Medications
              </h3>

              <div>
                <label className="block text-xs text-slate-400 font-semibold mb-1">
                  Conditions (comma separated)
                </label>
                <input
                  type="text"
                  value={(profile.conditions || []).join(", ")}
                  onChange={(e) => setProfile({ ...profile, conditions: e.target.value.split(",").map(s => s.trim()).filter(Boolean) })}
                  className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white"
                />
              </div>

              <div>
                <label className="block text-xs text-slate-400 font-semibold mb-1">
                  Allergies (comma separated)
                </label>
                <input
                  type="text"
                  value={(profile.allergies || []).join(", ")}
                  onChange={(e) => setProfile({ ...profile, allergies: e.target.value.split(",").map(s => s.trim()).filter(Boolean) })}
                  className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white"
                />
              </div>

              <div>
                <label className="block text-xs text-slate-400 font-semibold mb-1">
                  Current Medications (comma separated)
                </label>
                <input
                  type="text"
                  value={(profile.medications || []).join(", ")}
                  onChange={(e) => setProfile({ ...profile, medications: e.target.value.split(",").map(s => s.trim()).filter(Boolean) })}
                  className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white"
                />
              </div>
            </div>

            {/* Emergency & Risk */}
            <div className="glass-panel p-6 rounded-3xl border border-slate-800 space-y-4">
              <h3 className="text-sm font-bold text-white flex items-center gap-2 uppercase tracking-wider text-rose-400">
                Emergency & Blood Group
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
                <div>
                  <label className="block text-slate-400 font-semibold mb-1">Blood Group</label>
                  <input
                    type="text"
                    value={profile.blood_group || "O+"}
                    onChange={(e) => setProfile({ ...profile, blood_group: e.target.value })}
                    className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-white"
                  />
                </div>
                <div>
                  <label className="block text-slate-400 font-semibold mb-1">Emergency Phone Contact</label>
                  <input
                    type="text"
                    value={profile.emergency_contact || ""}
                    onChange={(e) => setProfile({ ...profile, emergency_contact: e.target.value })}
                    className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-white"
                  />
                </div>
              </div>
            </div>

          </form>
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
        <Link href="/history" className="flex flex-col items-center text-slate-400 hover:text-cyan-400">
          <History className="w-5 h-5" />
          <span>History</span>
        </Link>
        <Link href="/health-profile" className="flex flex-col items-center text-cyan-400 font-bold">
          <UserCheck className="w-5 h-5" />
          <span>Health</span>
        </Link>
      </nav>
    </div>
  );
}
