import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "HealthAI - Full Stack AI Health Assistant",
  description: "Instant symptom guidance, clinical triage, wellness insights, and intelligent health support powered by AI.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#0b1329] text-slate-100 min-h-screen antialiased selection:bg-cyan-500 selection:text-slate-950">
        {children}
      </body>
    </html>
  );
}
