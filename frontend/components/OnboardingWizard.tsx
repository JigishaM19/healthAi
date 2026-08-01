"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Activity, 
  Sparkles, 
  ChevronRight, 
  ChevronLeft, 
  Check, 
  Heart, 
  ShieldCheck, 
  Smile, 
  User, 
  Stethoscope,
  Flame,
  AlertCircle
} from "lucide-react";
import { api } from "@/lib/api";

interface OnboardingWizardProps {
  userName?: string;
}

export default function OnboardingWizard({ userName = "Friend" }: OnboardingWizardProps) {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Form State
  const [formData, setFormData] = useState({
    // Step 1: Basic Info
    age: 28,
    gender: "Male",
    height_cm: 175,
    weight_kg: 70,

    // Step 2: Medical Background
    conditions: [] as string[],
    allergies: [] as string[],
    medications: [] as string[],
    surgeries: "",
    pregnancy_status: "Not applicable",

    // Step 3: Lifestyle
    activity_level: "moderately_active",
    exercise_frequency: "3-4 times a week",
    sleep_hours: 7.5,
    smoking_status: "Never",
    alcohol_consumption: "Occasional",
    water_intake: 2.5,
    diet_type: "Balanced / Mediterranean",

    // Step 4: Health Goals
    goals: ["Better sleep", "Reduce stress", "Increase energy"] as string[],

    // Step 5: Risk & Emergency Info + Mental Wellness
    blood_group: "O+",
    emergency_contact: "+1 (555) 019-2831",
    city_country: "New York, USA",
    preferred_language: "English",
    family_history: [] as string[],
    notification_preferences: {
      medication_reminders: true,
      hydration_reminders: true,
      exercise_reminders: true,
      sleep_reminders: true,
      daily_checkins: true,
    },
    stress_level: 3,
    mood: "Calm",
  });

  // Common selections
  const conditionOptions = ["Diabetes", "Hypertension", "Asthma", "Thyroid", "Cholesterol", "Migraine", "Heart Condition"];
  const allergyOptions = ["Penicillin", "Peanuts", "Dust / Pollen", "Sulfa drugs", "Latex", "Shellfish", "Aspirin"];
  const goalOptions = [
    "Lose weight", "Gain muscle", "Improve fitness", "Better sleep", 
    "Reduce stress", "Manage diabetes", "Improve heart health", 
    "General wellness", "Increase energy", "Mental well-being"
  ];
  const familyHistoryOptions = ["Diabetes", "Heart disease", "Hypertension", "Cancer", "Stroke"];
  const moodOptions = ["Happy", "Calm", "Neutral", "Anxious", "Sad", "Stressed"];

  const toggleArrayItem = (field: "conditions" | "allergies" | "goals" | "family_history", item: string) => {
    setFormData((prev) => {
      const current = prev[field];
      const updated = current.includes(item)
        ? current.filter((x) => x !== item)
        : [...current, item];
      return { ...prev, [field]: updated };
    });
  };

  const handleFinish = async () => {
    setLoading(true);
    setError(null);
    try {
      await api.saveOnboarding(formData);
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message || "Failed to save health profile.");
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      
      {/* Header Banner */}
      <div className="glass-panel p-6 rounded-3xl border border-cyan-500/30 mb-8 relative overflow-hidden">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-cyan-500 to-indigo-500 p-0.5 shrink-0 shadow-lg shadow-cyan-500/20">
            <div className="w-full h-full bg-[#0b1329] rounded-[14px] flex items-center justify-center">
              <Stethoscope className="w-6 h-6 text-cyan-400" />
            </div>
          </div>
          <div>
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              Hi {userName} 👋 I’m HealthAI.
            </h2>
            <p className="text-xs text-slate-300">
              I’ll ask a few quick questions so I can provide personalized health guidance and medical triage.
            </p>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="mt-6 space-y-2">
          <div className="flex justify-between text-xs font-semibold text-slate-400">
            <span>Step {step} of 5</span>
            <span className="text-cyan-400">{step * 20}% Completed</span>
          </div>
          <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-gradient-to-r from-cyan-500 via-teal-400 to-indigo-500"
              initial={{ width: `${(step - 1) * 20}%` }}
              animate={{ width: `${step * 20}%` }}
              transition={{ duration: 0.4 }}
            />
          </div>
        </div>
      </div>

      {error && (
        <div className="mb-6 p-4 rounded-2xl bg-rose-950/40 border border-rose-500/40 text-rose-300 text-sm flex items-center gap-2">
          <AlertCircle className="w-5 h-5 shrink-0" />
          {error}
        </div>
      )}

      {/* Step Content Cards */}
      <AnimatePresence mode="wait">
        
        {/* STEP 1: Basic Info */}
        {step === 1 && (
          <motion.div
            key="step1"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="glass-panel p-8 rounded-3xl border border-slate-800 space-y-6"
          >
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <User className="w-5 h-5 text-cyan-400" />
              Step 1: Basic Information
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
                  Age ({formData.age} yrs)
                </label>
                <input
                  type="range"
                  min="12"
                  max="100"
                  value={formData.age}
                  onChange={(e) => setFormData({ ...formData, age: Number(e.target.value) })}
                  className="w-full accent-cyan-400"
                />
              </div>

              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
                  Biological Gender
                </label>
                <select
                  value={formData.gender}
                  onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
                  className="w-full bg-slate-900/90 border border-slate-700 rounded-xl px-4 py-3 text-slate-200 text-sm focus:border-cyan-400 focus:outline-none"
                >
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Other">Other / Prefer not to say</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
                  Height ({formData.height_cm} cm)
                </label>
                <input
                  type="range"
                  min="120"
                  max="220"
                  value={formData.height_cm}
                  onChange={(e) => setFormData({ ...formData, height_cm: Number(e.target.value) })}
                  className="w-full accent-teal-400"
                />
              </div>

              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
                  Weight ({formData.weight_kg} kg)
                </label>
                <input
                  type="range"
                  min="35"
                  max="180"
                  value={formData.weight_kg}
                  onChange={(e) => setFormData({ ...formData, weight_kg: Number(e.target.value) })}
                  className="w-full accent-indigo-400"
                />
              </div>
            </div>
          </motion.div>
        )}

        {/* STEP 2: Medical Background */}
        {step === 2 && (
          <motion.div
            key="step2"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="glass-panel p-8 rounded-3xl border border-slate-800 space-y-6"
          >
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <Activity className="w-5 h-5 text-teal-400" />
              Step 2: Medical Background
            </h3>

            {/* Existing Conditions */}
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">
                Existing Medical Conditions
              </label>
              <div className="flex flex-wrap gap-2">
                {conditionOptions.map((cond) => {
                  const isSelected = formData.conditions.includes(cond);
                  return (
                    <button
                      key={cond}
                      type="button"
                      onClick={() => toggleArrayItem("conditions", cond)}
                      className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                        isSelected
                          ? "bg-cyan-500 text-slate-950 shadow-md shadow-cyan-500/20 font-bold"
                          : "bg-slate-800/80 text-slate-300 hover:bg-slate-700"
                      }`}
                    >
                      {isSelected ? "✓ " : "+ "}{cond}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Allergies */}
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">
                Known Allergies
              </label>
              <div className="flex flex-wrap gap-2">
                {allergyOptions.map((alg) => {
                  const isSelected = formData.allergies.includes(alg);
                  return (
                    <button
                      key={alg}
                      type="button"
                      onClick={() => toggleArrayItem("allergies", alg)}
                      className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                        isSelected
                          ? "bg-teal-500 text-slate-950 shadow-md shadow-teal-500/20 font-bold"
                          : "bg-slate-800/80 text-slate-300 hover:bg-slate-700"
                      }`}
                    >
                      {isSelected ? "✓ " : "+ "}{alg}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Medications input */}
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
                Current Medications (comma separated)
              </label>
              <input
                type="text"
                placeholder="e.g. Amlodipine 5mg, Metformin 500mg"
                value={formData.medications.join(", ")}
                onChange={(e) => setFormData({ ...formData, medications: e.target.value.split(",").map(s => s.trim()).filter(Boolean) })}
                className="w-full bg-slate-900/90 border border-slate-700 rounded-xl px-4 py-3 text-slate-200 text-sm focus:border-cyan-400 focus:outline-none"
              />
            </div>
          </motion.div>
        )}

        {/* STEP 3: Lifestyle Assessment */}
        {step === 3 && (
          <motion.div
            key="step3"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="glass-panel p-8 rounded-3xl border border-slate-800 space-y-6"
          >
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <Flame className="w-5 h-5 text-amber-400" />
              Step 3: Lifestyle & Habit Assessment
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
                  Physical Activity Level
                </label>
                <select
                  value={formData.activity_level}
                  onChange={(e) => setFormData({ ...formData, activity_level: e.target.value })}
                  className="w-full bg-slate-900/90 border border-slate-700 rounded-xl px-4 py-3 text-slate-200 text-sm focus:border-cyan-400 focus:outline-none"
                >
                  <option value="sedentary">Sedentary (Desk Job / Little movement)</option>
                  <option value="lightly_active">Lightly Active (1-2 days/week)</option>
                  <option value="moderately_active">Moderately Active (3-4 days/week)</option>
                  <option value="very_active">Very Active (5+ days/week)</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
                  Sleep Duration ({formData.sleep_hours} hrs/night)
                </label>
                <input
                  type="range"
                  min="4"
                  max="12"
                  step="0.5"
                  value={formData.sleep_hours}
                  onChange={(e) => setFormData({ ...formData, sleep_hours: Number(e.target.value) })}
                  className="w-full accent-cyan-400"
                />
              </div>

              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
                  Daily Water Intake ({formData.water_intake} Liters)
                </label>
                <input
                  type="range"
                  min="1"
                  max="6"
                  step="0.5"
                  value={formData.water_intake}
                  onChange={(e) => setFormData({ ...formData, water_intake: Number(e.target.value) })}
                  className="w-full accent-teal-400"
                />
              </div>

              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
                  Dietary Preference
                </label>
                <select
                  value={formData.diet_type}
                  onChange={(e) => setFormData({ ...formData, diet_type: e.target.value })}
                  className="w-full bg-slate-900/90 border border-slate-700 rounded-xl px-4 py-3 text-slate-200 text-sm focus:border-cyan-400 focus:outline-none"
                >
                  <option value="Balanced / Mediterranean">Balanced / Mediterranean</option>
                  <option value="Vegetarian">Vegetarian</option>
                  <option value="Vegan">Vegan</option>
                  <option value="High Protein / Keto">High Protein / Keto</option>
                  <option value="Diabetic Friendly">Diabetic Friendly</option>
                </select>
              </div>
            </div>
          </motion.div>
        )}

        {/* STEP 4: Health Goals */}
        {step === 4 && (
          <motion.div
            key="step4"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="glass-panel p-8 rounded-3xl border border-slate-800 space-y-6"
          >
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-indigo-400" />
              Step 4: Your Health & Wellness Goals
            </h3>
            <p className="text-xs text-slate-400">
              Select all goals you wish to accomplish with HealthAI's personalized guidance:
            </p>

            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
              {goalOptions.map((goal) => {
                const isSelected = formData.goals.includes(goal);
                return (
                  <button
                    key={goal}
                    type="button"
                    onClick={() => toggleArrayItem("goals", goal)}
                    className={`p-4 rounded-2xl border text-left text-xs font-bold transition-all flex items-center justify-between ${
                      isSelected
                        ? "bg-gradient-to-r from-cyan-500/20 to-teal-500/20 border-cyan-400 text-cyan-300 shadow-lg shadow-cyan-500/10"
                        : "bg-slate-900/60 border-slate-800 text-slate-300 hover:border-slate-700"
                    }`}
                  >
                    <span>{goal}</span>
                    {isSelected && <Check className="w-4 h-4 text-cyan-400 shrink-0" />}
                  </button>
                );
              })}
            </div>
          </motion.div>
        )}

        {/* STEP 5: Risk & Emergency Info + Mental Wellness Check-In */}
        {step === 5 && (
          <motion.div
            key="step5"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="glass-panel p-8 rounded-3xl border border-slate-800 space-y-6"
          >
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <Heart className="w-5 h-5 text-rose-400" />
              Step 5: Emergency Profile & Mental Wellness Check-In
            </h3>

            {/* Emergency Info Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
                  Blood Group
                </label>
                <select
                  value={formData.blood_group}
                  onChange={(e) => setFormData({ ...formData, blood_group: e.target.value })}
                  className="w-full bg-slate-900/90 border border-slate-700 rounded-xl px-4 py-2.5 text-slate-200 text-sm focus:border-cyan-400 focus:outline-none"
                >
                  {["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"].map((b) => (
                    <option key={b} value={b}>{b}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
                  Emergency Contact Phone
                </label>
                <input
                  type="text"
                  value={formData.emergency_contact}
                  onChange={(e) => setFormData({ ...formData, emergency_contact: e.target.value })}
                  className="w-full bg-slate-900/90 border border-slate-700 rounded-xl px-4 py-2.5 text-slate-200 text-sm focus:border-cyan-400 focus:outline-none"
                />
              </div>
            </div>

            {/* Mood Selector */}
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">
                How are you feeling today? (Mental Mood Selection)
              </label>
              <div className="grid grid-cols-3 sm:grid-cols-6 gap-2">
                {moodOptions.map((m) => (
                  <button
                    key={m}
                    type="button"
                    onClick={() => setFormData({ ...formData, mood: m })}
                    className={`py-3 px-2 rounded-xl text-xs font-bold border transition-all text-center ${
                      formData.mood === m
                        ? "bg-cyan-500 text-slate-950 border-cyan-400 shadow-md shadow-cyan-500/20"
                        : "bg-slate-900/60 border-slate-800 text-slate-300 hover:bg-slate-800"
                    }`}
                  >
                    {m}
                  </button>
                ))}
              </div>
            </div>

            {/* Stress Level Slider */}
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
                Current Stress Level ({formData.stress_level} / 5)
              </label>
              <input
                type="range"
                min="1"
                max="5"
                value={formData.stress_level}
                onChange={(e) => setFormData({ ...formData, stress_level: Number(e.target.value) })}
                className="w-full accent-rose-400"
              />
            </div>
          </motion.div>
        )}

      </AnimatePresence>

      {/* Navigation Buttons Footer */}
      <div className="mt-8 flex items-center justify-between">
        {step > 1 ? (
          <button
            type="button"
            onClick={() => setStep(step - 1)}
            className="flex items-center gap-2 px-6 py-3 rounded-2xl glass-panel text-slate-300 font-semibold hover:border-slate-600 transition-all text-sm"
          >
            <ChevronLeft className="w-4 h-4" />
            Back
          </button>
        ) : <div />}

        {step < 5 ? (
          <button
            type="button"
            onClick={() => setStep(step + 1)}
            className="flex items-center gap-2 px-8 py-3 rounded-2xl bg-gradient-to-r from-cyan-500 to-teal-400 text-slate-950 font-bold hover:brightness-110 transition-all shadow-lg shadow-cyan-500/20 text-sm"
          >
            Next Step
            <ChevronRight className="w-4 h-4" />
          </button>
        ) : (
          <button
            type="button"
            disabled={loading}
            onClick={handleFinish}
            className="flex items-center gap-2 px-8 py-3.5 rounded-2xl bg-gradient-to-r from-cyan-400 via-teal-400 to-indigo-500 text-slate-950 font-extrabold hover:scale-[1.02] transition-all shadow-xl shadow-cyan-500/25 text-sm"
          >
            {loading ? "Generating Profile..." : "Complete Profile & Launch Dashboard →"}
          </button>
        )}
      </div>

    </div>
  );
}
