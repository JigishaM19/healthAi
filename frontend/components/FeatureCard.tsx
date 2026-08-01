"use client";

import React from "react";
import { motion } from "framer-motion";
import { LucideIcon } from "lucide-react";

interface FeatureCardProps {
  icon: LucideIcon;
  title: string;
  description: string;
  accentColor?: string;
  delay?: number;
}

export default function FeatureCard({ icon: Icon, title, description, accentColor = "from-cyan-500 to-teal-400", delay = 0 }: FeatureCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5, delay }}
      whileHover={{ y: -6, transition: { duration: 0.2 } }}
      className="glass-panel p-7 rounded-3xl border border-slate-800/80 hover:border-cyan-500/40 transition-all group relative overflow-hidden"
    >
      {/* Background Subtle Gradient Glow */}
      <div className="absolute top-0 right-0 w-32 h-32 bg-cyan-500/5 rounded-full blur-2xl group-hover:bg-cyan-500/15 transition-all" />

      {/* Icon Badge */}
      <div className={`w-14 h-14 rounded-2xl bg-gradient-to-tr ${accentColor} p-0.5 shadow-lg shadow-cyan-500/10 mb-6 group-hover:scale-110 transition-transform duration-300`}>
        <div className="w-full h-full bg-[#0b1329] rounded-[14px] flex items-center justify-center">
          <Icon className="w-7 h-7 text-cyan-400 group-hover:text-cyan-300 transition-colors" />
        </div>
      </div>

      {/* Content */}
      <h3 className="text-xl font-bold text-white mb-2 group-hover:text-cyan-300 transition-colors">
        {title}
      </h3>
      <p className="text-sm text-slate-300 leading-relaxed">
        {description}
      </p>
    </motion.div>
  );
}
