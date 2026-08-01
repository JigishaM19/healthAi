"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import Sidebar from "@/components/Sidebar";
import Loader from "@/components/Loader";
import { 
  Settings, 
  User, 
  ShieldCheck, 
  Bell, 
  Palette, 
  Globe, 
  Activity, 
  AlertTriangle, 
  Save, 
  Download, 
  CheckCircle2, 
  Smartphone, 
  Moon, 
  Home,
  MessageSquare,
  Calendar,
  X
} from "lucide-react";
import { api } from "@/lib/api";
import { getToken, removeToken, setUser } from "@/lib/auth";
import { useLanguage, LanguageCode, UnitSystem } from "@/context/LanguageContext";

interface DeviceItem {
  provider: string;
  name: string;
  connected: boolean;
  account_id?: string | null;
  last_sync?: string | null;
}

export default function SettingsPage() {
  const router = useRouter();
  const { 
    language: currentLang, units: currentUnits, 
    setLanguage: setGlobalLanguage, setUnits: setGlobalUnits, 
    setTheme: setGlobalTheme, setFontSize: setGlobalFontSize, setReduceAnim: setGlobalReduceAnim,
    t 
  } = useLanguage();

  const [activeTab, setActiveTab] = useState<"account" | "security" | "notifications" | "privacy" | "appearance" | "language" | "devices" | "danger">("account");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{ text: string; type: "success" | "error" } | null>(null);

  // Account State
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");

  // Security State
  const [currentPass, setCurrentPass] = useState("");
  const [newPass, setNewPass] = useState("");
  const [confirmPass, setConfirmPass] = useState("");
  const [passStrength, setPassStrength] = useState<"Weak" | "Medium" | "Strong" | "">("");

  // Notifications State
  const [notifs, setNotifs] = useState({
    medication: true,
    hydration: true,
    exercise: true,
    sleep: true,
    appointment: true,
    report: true,
    email: true,
    push: true
  });

  // Appearance State
  const [theme, setTheme] = useState<"dark" | "light" | "system">("dark");
  const [fontSize, setFontSize] = useState("medium");
  const [reduceAnim, setReduceAnim] = useState(false);
  const [highContrast, setHighContrast] = useState(false);

  // Language & Region State
  const [language, setLanguage] = useState<string>("English");
  const [dateFormat, setDateFormat] = useState("YYYY-MM-DD");
  const [timeFormat, setTimeFormat] = useState("12h");
  const [units, setUnits] = useState<string>("Metric");

  // Connected Devices State
  const [deviceList, setDeviceList] = useState<DeviceItem[]>([]);

  // Danger Zone Delete Modal
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [deletePass, setDeletePass] = useState("");
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.push("/login");
      return;
    }

    async function loadData() {
      try {
        const res = await api.getSettings();
        setName(res.user.name || "");
        setEmail(res.user.email || "");
        if (res.settings) {
          setPhone(res.settings.phone_number || "");
          setTheme(res.settings.theme || "dark");
          
          const backendLang = res.settings.language || "English";
          const backendUnits = res.settings.units || "Metric";
          setLanguage(backendLang);
          setUnits(backendUnits);
          setGlobalLanguage(backendLang as LanguageCode);
          setGlobalUnits(backendUnits as UnitSystem);

          setDateFormat(res.settings.date_format || "YYYY-MM-DD");
          setTimeFormat(res.settings.time_format || "12h");
          setReduceAnim(Boolean(res.settings.reduce_animations));
          setHighContrast(Boolean(res.settings.high_contrast));
          setFontSize(res.settings.font_size || "medium");
        }

        // Fetch Connected Devices
        const devData = await api.getConnectedDevices();
        if (Array.isArray(devData)) {
          setDeviceList(devData);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [router]);

  const handleNewPassChange = (val: string) => {
    setNewPass(val);
    if (!val) setPassStrength("");
    else if (val.length < 6) setPassStrength("Weak");
    else if (val.length >= 8 && /[A-Z]/.test(val) && /[0-9]/.test(val)) setPassStrength("Strong");
    else setPassStrength("Medium");
  };

  const handleAccountSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setMessage(null);
    try {
      const res = await api.updateSettingsAccount({ name, email, phone_number: phone });
      setUser(res.user);
      setMessage({ text: "Account details saved successfully!", type: "success" });
    } catch (err: any) {
      setMessage({ text: err.message || "Account update failed", type: "error" });
    } finally {
      setSaving(false);
    }
  };

  const handlePasswordSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (newPass !== confirmPass) {
      setMessage({ text: "New passwords do not match", type: "error" });
      return;
    }
    setSaving(true);
    setMessage(null);
    try {
      await api.updateSettingsPassword({ current_password: currentPass, new_password: newPass });
      setMessage({ text: "Security password updated successfully!", type: "success" });
      setCurrentPass("");
      setNewPass("");
      setConfirmPass("");
      setPassStrength("");
    } catch (err: any) {
      setMessage({ text: err.message || "Password update failed", type: "error" });
    } finally {
      setSaving(false);
    }
  };

  const handleNotificationSave = async () => {
    setSaving(true);
    try {
      await api.updateSettingsNotifications({
        medication_reminders: notifs.medication ? 1 : 0,
        hydration_reminders: notifs.hydration ? 1 : 0,
        exercise_reminders: notifs.exercise ? 1 : 0,
        sleep_reminders: notifs.sleep ? 1 : 0,
        appointment_reminders: notifs.appointment ? 1 : 0,
        report_notifications: notifs.report ? 1 : 0,
      });
      setMessage({ text: "Notification preferences updated!", type: "success" });
    } catch (err: any) {
      setMessage({ text: err.message || "Notification save failed", type: "error" });
    } finally {
      setSaving(false);
    }
  };

  const handleAppearanceSave = async (selectedTheme?: "dark" | "light" | "system") => {
    const tVal = selectedTheme || theme;
    setSaving(true);
    try {
      setGlobalTheme(tVal);
      setGlobalFontSize(fontSize);
      setGlobalReduceAnim(reduceAnim);
      await api.updateSettingsAppearance({
        theme: tVal,
        font_size: fontSize,
        reduce_animations: reduceAnim ? 1 : 0,
        high_contrast: highContrast ? 1 : 0
      });
      setMessage({ text: "Appearance preferences updated successfully!", type: "success" });
    } catch (err: any) {
      setMessage({ text: err.message || "Appearance save failed", type: "error" });
    } finally {
      setSaving(false);
    }
  };

  const handleLanguageSave = async () => {
    setSaving(true);
    try {
      setGlobalLanguage(language as LanguageCode);
      setGlobalUnits(units as UnitSystem);
      await api.updateSettingsLanguage({
        language,
        date_format: dateFormat,
        time_format: timeFormat,
        units
      });
      setMessage({ text: "Language & Region preferences saved successfully!", type: "success" });
    } catch (err: any) {
      setMessage({ text: err.message || "Language save failed", type: "error" });
    } finally {
      setSaving(false);
    }
  };

  const handleToggleDevice = async (providerKey: string, currentlyConnected: boolean) => {
    try {
      if (currentlyConnected) {
        await api.disconnectDevice(providerKey);
      } else {
        await api.connectDevice(providerKey, `${name.toLowerCase().replace(/\s+/g, '_')}_${providerKey}`);
      }
      const updated = await api.getConnectedDevices();
      if (Array.isArray(updated)) {
        setDeviceList(updated);
      }
      setMessage({
        text: `${providerKey.replace('_', ' ').toUpperCase()} ${currentlyConnected ? "disconnected" : "connected"} successfully!`,
        type: "success"
      });
    } catch (err: any) {
      setMessage({ text: err.message || "Device connection toggle failed", type: "error" });
    }
  };

  const handleExportData = async () => {
    try {
      const data = await api.exportHealthData();
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `HealthAI_Data_Export_${new Date().toISOString().slice(0, 10)}.json`;
      a.click();
      setMessage({ text: "Health data exported successfully!", type: "success" });
    } catch (err: any) {
      setMessage({ text: "Export failed", type: "error" });
    }
  };

  const handleLogoutAll = async () => {
    try {
      await api.logoutAllDevices();
      removeToken();
      router.push("/login");
    } catch (err) {
      removeToken();
      router.push("/login");
    }
  };

  const handleDeleteAccount = async () => {
    if (!deletePass) return;
    setDeleting(true);
    try {
      await api.deleteAccount(deletePass);
      removeToken();
      router.push("/signup");
    } catch (err: any) {
      setMessage({ text: err.message || "Account deletion failed", type: "error" });
      setDeleting(false);
      setShowDeleteModal(false);
    }
  };

  const tabs = [
    { id: "account", label: t("account"), icon: User },
    { id: "security", label: t("security"), icon: ShieldCheck },
    { id: "notifications", label: t("notifications"), icon: Bell },
    { id: "privacy", label: t("privacy"), icon: Download },
    { id: "appearance", label: t("appearance"), icon: Palette },
    { id: "language", label: t("language"), icon: Globe },
    { id: "devices", label: t("devices"), icon: Smartphone },
    { id: "danger", label: t("dangerZone"), icon: AlertTriangle },
  ];

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0b1329] flex items-center justify-center">
        <Loader label="Opening Healthcare Settings Center..." />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0b1329] flex text-slate-100">
      <Sidebar />

      <main className="flex-1 p-4 sm:p-8 max-w-6xl mx-auto space-y-6 pb-28 lg:pb-12">
        
        {/* Header Banner */}
        <div className="glass-panel p-6 rounded-3xl border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-cyan-500 via-indigo-500 to-teal-400 p-0.5 shadow-lg shadow-cyan-500/20 shrink-0">
              <div className="w-full h-full bg-[#0b1329] rounded-[14px] flex items-center justify-center">
                <Settings className="w-6 h-6 text-cyan-400" />
              </div>
            </div>
            <div>
              <h1 className="text-2xl font-extrabold text-white">{t("settings")}</h1>
              <p className="text-xs text-slate-400 mt-0.5">
                Manage your credentials, security preferences, health reminders, and data exports.
              </p>
            </div>
          </div>
        </div>

        {/* Global Toast Alert Message */}
        {message && (
          <div className={`p-4 rounded-2xl border text-xs font-bold flex items-center justify-between transition-all ${
            message.type === "success" 
              ? "bg-teal-950/50 border-teal-500/40 text-teal-300" 
              : "bg-rose-950/50 border-rose-500/40 text-rose-300"
          }`}>
            <div className="flex items-center gap-2">
              {message.type === "success" ? <CheckCircle2 className="w-4 h-4 text-teal-400" /> : <AlertTriangle className="w-4 h-4 text-rose-400" />}
              <span>{message.text}</span>
            </div>
            <button onClick={() => setMessage(null)} className="text-slate-400 hover:text-white">
              <X className="w-4 h-4" />
            </button>
          </div>
        )}

        {/* Settings Master Layout Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          
          {/* Navigation Tab List */}
          <div className="glass-panel p-3 rounded-3xl border border-slate-800 h-fit space-y-1">
            {tabs.map((tb) => {
              const Icon = tb.icon;
              const isActive = activeTab === tb.id;

              return (
                <button
                  key={tb.id}
                  onClick={() => setActiveTab(tb.id as any)}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-2xl font-bold text-xs transition-all text-left ${
                    isActive
                      ? tb.id === "danger"
                        ? "bg-rose-500/20 text-rose-300 border border-rose-500/40 shadow-md shadow-rose-500/10"
                        : "bg-gradient-to-r from-cyan-500/20 to-teal-500/10 border border-cyan-500/40 text-cyan-300 shadow-md shadow-cyan-500/10"
                      : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/40"
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? (tb.id === "danger" ? "text-rose-400" : "text-cyan-400") : "text-slate-400"}`} />
                  <span className="truncate">{tb.label}</span>
                </button>
              );
            })}
          </div>

          {/* Settings Tab Content View */}
          <div className="lg:col-span-3">
            <AnimatePresence mode="wait">
              <motion.div
                key={activeTab}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -8 }}
                transition={{ duration: 0.2 }}
                className="glass-panel p-6 sm:p-8 rounded-3xl border border-slate-800 space-y-6"
              >
                
                {/* 1. Account Section */}
                {activeTab === "account" && (
                  <form onSubmit={handleAccountSave} className="space-y-6">
                    <div className="border-b border-slate-800 pb-4 flex items-center justify-between">
                      <div>
                        <h3 className="text-base font-extrabold text-white">{t("account")}</h3>
                        <p className="text-xs text-slate-400">Update your primary identity and contact details.</p>
                      </div>
                      <span className="px-3 py-1 rounded-full bg-cyan-500/10 text-cyan-300 border border-cyan-500/30 text-[10px] font-bold uppercase">
                        Verified Profile
                      </span>
                    </div>

                    <div className="space-y-4 text-xs">
                      <div>
                        <label className="block text-slate-400 font-bold mb-1.5">Full Name</label>
                        <input
                          type="text"
                          value={name}
                          onChange={(e) => setName(e.target.value)}
                          className="w-full bg-slate-900 border border-slate-700 rounded-2xl px-4 py-3 text-white focus:border-cyan-500 focus:outline-none"
                          required
                        />
                      </div>

                      <div>
                        <label className="block text-slate-400 font-bold mb-1.5">Email Address</label>
                        <input
                          type="email"
                          value={email}
                          onChange={(e) => setEmail(e.target.value)}
                          className="w-full bg-slate-900 border border-slate-700 rounded-2xl px-4 py-3 text-white focus:border-cyan-500 focus:outline-none"
                          required
                        />
                      </div>

                      <div>
                        <label className="block text-slate-400 font-bold mb-1.5">Phone Number (For Security SMS Alerts)</label>
                        <input
                          type="tel"
                          value={phone}
                          onChange={(e) => setPhone(e.target.value)}
                          placeholder="+1 234 567 8900"
                          className="w-full bg-slate-900 border border-slate-700 rounded-2xl px-4 py-3 text-white focus:border-cyan-500 focus:outline-none"
                        />
                      </div>
                    </div>

                    <div className="pt-4 border-t border-slate-800 flex justify-end">
                      <button
                        type="submit"
                        disabled={saving}
                        className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-cyan-500 text-slate-950 font-bold text-xs hover:brightness-110 transition-all disabled:opacity-50 shadow-md shadow-cyan-500/20"
                      >
                        <Save className="w-4 h-4" /> {saving ? "Saving..." : t("save")}
                      </button>
                    </div>
                  </form>
                )}

                {/* 2. Security Section */}
                {activeTab === "security" && (
                  <form onSubmit={handlePasswordSave} className="space-y-6">
                    <div className="border-b border-slate-800 pb-4">
                      <h3 className="text-base font-extrabold text-white">{t("security")}</h3>
                      <p className="text-xs text-slate-400">Manage password security, 2FA, and active session devices.</p>
                    </div>

                    <div className="space-y-4 text-xs">
                      <div>
                        <label className="block text-slate-400 font-bold mb-1.5">Current Password</label>
                        <input
                          type="password"
                          value={currentPass}
                          onChange={(e) => setCurrentPass(e.target.value)}
                          className="w-full bg-slate-900 border border-slate-700 rounded-2xl px-4 py-3 text-white focus:border-cyan-500 focus:outline-none"
                          required
                        />
                      </div>

                      <div>
                        <label className="block text-slate-400 font-bold mb-1.5">New Password</label>
                        <input
                          type="password"
                          value={newPass}
                          onChange={(e) => handleNewPassChange(e.target.value)}
                          className="w-full bg-slate-900 border border-slate-700 rounded-2xl px-4 py-3 text-white focus:border-cyan-500 focus:outline-none"
                          required
                        />
                        {passStrength && (
                          <div className="mt-2 flex items-center gap-2 text-[11px]">
                            <span className="text-slate-400 font-bold">Strength:</span>
                            <span className={`font-extrabold ${
                              passStrength === "Weak" ? "text-rose-400" : passStrength === "Medium" ? "text-amber-400" : "text-teal-400"
                            }`}>{passStrength}</span>
                          </div>
                        )}
                      </div>

                      <div>
                        <label className="block text-slate-400 font-bold mb-1.5">Confirm New Password</label>
                        <input
                          type="password"
                          value={confirmPass}
                          onChange={(e) => setConfirmPass(e.target.value)}
                          className="w-full bg-slate-900 border border-slate-700 rounded-2xl px-4 py-3 text-white focus:border-cyan-500 focus:outline-none"
                          required
                        />
                      </div>
                    </div>

                    <div className="pt-4 border-t border-slate-800 flex justify-between items-center">
                      <button
                        type="button"
                        onClick={handleLogoutAll}
                        className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold text-xs transition-all"
                      >
                        Logout All Other Devices
                      </button>

                      <button
                        type="submit"
                        disabled={saving}
                        className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-cyan-500 text-slate-950 font-bold text-xs hover:brightness-110 transition-all disabled:opacity-50 shadow-md shadow-cyan-500/20"
                      >
                        <Save className="w-4 h-4" /> {saving ? "Updating..." : "Update Password"}
                      </button>
                    </div>
                  </form>
                )}

                {/* 3. Notifications Section */}
                {activeTab === "notifications" && (
                  <div className="space-y-6">
                    <div className="border-b border-slate-800 pb-4">
                      <h3 className="text-base font-extrabold text-white">{t("notifications")}</h3>
                      <p className="text-xs text-slate-400">Configure medication, hydration, and report notification alerts.</p>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
                      {[
                        { key: "medication", label: "Medication Reminders", desc: "Daily dosage & schedule alerts" },
                        { key: "hydration", label: "Hydration Reminders", desc: "Water intake prompts" },
                        { key: "exercise", label: "Exercise & Activity Reminders", desc: "Workout and step targets" },
                        { key: "sleep", label: "Sleep Reminders", desc: "Bedtime & sleep schedule alerts" },
                        { key: "appointment", label: "Doctor Appointments", desc: "Clinical appointment notifications" },
                        { key: "report", label: "Lab Report Alerts", desc: "OCR analysis completion updates" }
                      ].map((item) => (
                        <div key={item.key} className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 flex items-center justify-between">
                          <div>
                            <h4 className="font-bold text-white">{item.label}</h4>
                            <p className="text-slate-400 text-[11px]">{item.desc}</p>
                          </div>
                          <input
                            type="checkbox"
                            checked={notifs[item.key as keyof typeof notifs]}
                            onChange={(e) => setNotifs(prev => ({ ...prev, [item.key]: e.target.checked }))}
                            className="w-5 h-5 rounded accent-cyan-500"
                          />
                        </div>
                      ))}
                    </div>

                    <div className="pt-4 border-t border-slate-800 flex justify-end">
                      <button
                        onClick={handleNotificationSave}
                        className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-cyan-500 text-slate-950 font-bold text-xs hover:brightness-110 transition-all shadow-md shadow-cyan-500/20"
                      >
                        <Save className="w-4 h-4" /> {t("save")}
                      </button>
                    </div>
                  </div>
                )}

                {/* 4. Privacy & Data Export Section */}
                {activeTab === "privacy" && (
                  <div className="space-y-6">
                    <div className="border-b border-slate-800 pb-4">
                      <h3 className="text-base font-extrabold text-white">{t("privacy")}</h3>
                      <p className="text-xs text-slate-400">Export your complete personal health record data.</p>
                    </div>

                    <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-3 text-xs">
                      <h4 className="font-bold text-white text-sm">Download Full Health Record Archive</h4>
                      <p className="text-slate-400 leading-relaxed">
                        Generate a comprehensive JSON export containing your health profile, lab measurements, timeline events, AI consultations, and medication safety reports.
                      </p>
                      <button
                        onClick={handleExportData}
                        className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-teal-500 text-slate-950 font-extrabold text-xs hover:brightness-110 transition-all shadow-md shadow-teal-500/20"
                      >
                        <Download className="w-4 h-4" /> Export Health JSON Data
                      </button>
                    </div>
                  </div>
                )}

                {/* 5. Appearance Section */}
                {activeTab === "appearance" && (
                  <div className="space-y-6">
                    <div className="border-b border-slate-800 pb-4">
                      <h3 className="text-base font-extrabold text-white">{t("appearance")}</h3>
                      <p className="text-xs text-slate-400">Customize color themes, fonts, and animation speeds.</p>
                    </div>

                    <div>
                      <label className="block text-slate-400 font-bold mb-2 text-xs">{t("theme")}</label>
                      <div className="grid grid-cols-3 gap-3">
                        {[
                          { id: "dark", label: "Dark Mode", icon: Moon },
                          { id: "light", label: "Light Mode", icon: Activity },
                          { id: "system", label: "System", icon: Settings }
                        ].map((th) => {
                          const Icon = th.icon;
                          const isSel = theme === th.id;
                          return (
                            <button
                              key={th.id}
                              onClick={() => { setTheme(th.id as any); handleAppearanceSave(th.id as any); }}
                              className={`p-4 rounded-2xl border text-xs font-bold flex flex-col items-center gap-2 transition-all ${
                                isSel ? "bg-cyan-500/20 border-cyan-400 text-cyan-300" : "bg-slate-900 border-slate-800 text-slate-400 hover:text-white"
                              }`}
                            >
                              <Icon className="w-5 h-5" />
                              <span>{th.label}</span>
                            </button>
                          );
                        })}
                      </div>
                    </div>
                  </div>
                )}

                {/* 6. Language & Region Section */}
                {activeTab === "language" && (
                  <div className="space-y-6">
                    <div className="border-b border-slate-800 pb-4">
                      <h3 className="text-base font-extrabold text-white">{t("language")}</h3>
                      <p className="text-xs text-slate-400">Configure localization, date formats, and measurement units.</p>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
                      <div>
                        <label className="block text-slate-400 font-bold mb-1.5">Primary Interface Language</label>
                        <select
                          value={language}
                          onChange={(e) => setLanguage(e.target.value)}
                          className="w-full bg-slate-900 border border-slate-700 rounded-2xl px-4 py-3 text-white focus:border-cyan-500 focus:outline-none"
                        >
                          <option value="English">English</option>
                          <option value="Hindi">Hindi (हिंदी)</option>
                          <option value="Spanish">Spanish (Español)</option>
                          <option value="French">French (Français)</option>
                          <option value="German">German (Deutsch)</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-slate-400 font-bold mb-1.5">{t("units")}</label>
                        <select
                          value={units}
                          onChange={(e) => setUnits(e.target.value)}
                          className="w-full bg-slate-900 border border-slate-700 rounded-2xl px-4 py-3 text-white focus:border-cyan-500 focus:outline-none"
                        >
                          <option value="Metric">{t("metric")}</option>
                          <option value="Imperial">{t("imperial")}</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-slate-400 font-bold mb-1.5">Date Display Format</label>
                        <select
                          value={dateFormat}
                          onChange={(e) => setDateFormat(e.target.value)}
                          className="w-full bg-slate-900 border border-slate-700 rounded-2xl px-4 py-3 text-white focus:border-cyan-500 focus:outline-none"
                        >
                          <option value="YYYY-MM-DD">YYYY-MM-DD (2026-08-01)</option>
                          <option value="MM/DD/YYYY">MM/DD/YYYY (08/01/2026)</option>
                          <option value="DD/MM/YYYY">DD/MM/YYYY (01/08/2026)</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-slate-400 font-bold mb-1.5">Time Format</label>
                        <select
                          value={timeFormat}
                          onChange={(e) => setTimeFormat(e.target.value)}
                          className="w-full bg-slate-900 border border-slate-700 rounded-2xl px-4 py-3 text-white focus:border-cyan-500 focus:outline-none"
                        >
                          <option value="12h">12-Hour (AM / PM)</option>
                          <option value="24h">24-Hour (Military Time)</option>
                        </select>
                      </div>
                    </div>

                    <div className="pt-4 border-t border-slate-800 flex justify-end">
                      <button
                        onClick={handleLanguageSave}
                        disabled={saving}
                        className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-cyan-500 text-slate-950 font-bold text-xs hover:brightness-110 transition-all shadow-md shadow-cyan-500/20 disabled:opacity-50"
                      >
                        <Save className="w-4 h-4" /> {saving ? "Saving..." : t("save")}
                      </button>
                    </div>
                  </div>
                )}

                {/* 7. Connected Devices Section */}
                {activeTab === "devices" && (
                  <div className="space-y-6">
                    <div className="border-b border-slate-800 pb-4">
                      <h3 className="text-base font-extrabold text-white">{t("devices")}</h3>
                      <p className="text-xs text-slate-400">Sync fitness wearables and smart health platforms.</p>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
                      {deviceList.map((dev) => {
                        const isConn = dev.connected;
                        const syncFormatted = dev.last_sync 
                          ? `${t("lastSynced")}: ${new Date(dev.last_sync).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}` 
                          : "Not Synced Yet";

                        return (
                          <div key={dev.provider} className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 flex items-center justify-between">
                            <div className="flex items-center gap-3">
                              <div className={`w-10 h-10 rounded-2xl flex items-center justify-center border ${
                                isConn ? "bg-teal-500/20 border-teal-400/40 text-teal-300" : "bg-slate-800 border-slate-700 text-slate-400"
                              }`}>
                                <Activity className="w-5 h-5" />
                              </div>
                              <div>
                                <h4 className="font-bold text-white">{dev.name}</h4>
                                <p className="text-slate-400 text-[11px]">{syncFormatted}</p>
                              </div>
                            </div>

                            <button
                              onClick={() => handleToggleDevice(dev.provider, isConn)}
                              className={`px-3 py-1.5 rounded-xl font-extrabold text-[11px] transition-all ${
                                isConn ? "bg-teal-500/20 text-teal-300 border border-teal-500/40 hover:bg-rose-500/20 hover:text-rose-300 hover:border-rose-500/40" : "bg-slate-800 text-slate-400 border border-slate-700 hover:text-white"
                              }`}
                            >
                              {isConn ? t("connected") : "Connect"}
                            </button>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}

                {/* 8. Danger Zone Section */}
                {activeTab === "danger" && (
                  <div className="space-y-6">
                    <div className="border-b border-rose-500/30 pb-4">
                      <h3 className="text-base font-extrabold text-rose-400 flex items-center gap-2">
                        <AlertTriangle className="w-5 h-5" /> {t("dangerZone")}
                      </h3>
                      <p className="text-xs text-rose-300/80">Irreversible account destruction actions.</p>
                    </div>

                    <div className="p-5 rounded-2xl bg-rose-950/20 border border-rose-500/30 space-y-4 text-xs text-rose-200">
                      <div>
                        <h4 className="font-extrabold text-sm text-rose-300">{t("deleteAccount")}</h4>
                        <p className="text-slate-400 mt-1 leading-relaxed">
                          Once you delete your account, all health profiles, consultation histories, timeline events, uploaded medical documents, and AI memory records will be permanently erased.
                        </p>
                      </div>

                      <button
                        onClick={() => setShowDeleteModal(true)}
                        className="px-6 py-2.5 rounded-xl bg-rose-600 text-white font-extrabold hover:bg-rose-500 transition-all shadow-lg shadow-rose-600/30"
                      >
                        {t("deleteAccount")}
                      </button>
                    </div>
                  </div>
                )}

              </motion.div>
            </AnimatePresence>
          </div>

        </div>

      </main>

      {/* Delete Account Modal */}
      {showDeleteModal && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4">
          <div className="glass-panel p-6 sm:p-8 rounded-3xl border border-rose-500/40 max-w-md w-full space-y-4 relative">
            <div className="flex items-center gap-3 text-rose-400 font-extrabold text-base border-b border-slate-800 pb-3">
              <AlertTriangle className="w-6 h-6" /> Confirm Account Destruction
            </div>

            <p className="text-xs text-slate-300 leading-relaxed">
              Please enter your password to confirm permanent deletion of your account and all associated health records.
            </p>

            <div>
              <label className="block text-xs font-bold text-slate-400 mb-1">Confirm Password</label>
              <input
                type="password"
                value={deletePass}
                onChange={(e) => setDeletePass(e.target.value)}
                placeholder="Enter account password"
                className="w-full bg-slate-900 border border-slate-700 rounded-2xl px-4 py-3 text-xs text-white focus:border-rose-500 focus:outline-none"
              />
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                onClick={() => setShowDeleteModal(false)}
                className="px-4 py-2 rounded-xl bg-slate-800 text-slate-300 font-bold text-xs hover:text-white"
              >
                {t("cancel")}
              </button>
              <button
                onClick={handleDeleteAccount}
                disabled={deleting || !deletePass}
                className="px-5 py-2 rounded-xl bg-rose-600 text-white font-extrabold text-xs hover:bg-rose-500 disabled:opacity-50"
              >
                {deleting ? "Deleting..." : t("deleteAccount")}
              </button>
            </div>
          </div>
        </div>
      )}

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
        <Link href="/timeline" className="flex flex-col items-center text-slate-400 hover:text-cyan-400">
          <Calendar className="w-5 h-5" />
          <span>Timeline</span>
        </Link>
        <Link href="/settings" className="flex flex-col items-center text-cyan-400 font-bold">
          <Settings className="w-5 h-5" />
          <span>Settings</span>
        </Link>
      </nav>
    </div>
  );
}
