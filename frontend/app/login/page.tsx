"use client";

import React from "react";
import Navbar from "@/components/Navbar";
import AuthForm from "@/components/AuthForm";

export default function LoginPage() {
  return (
    <div className="min-h-screen bg-[#0b1329]">
      <Navbar />
      <AuthForm mode="login" />
    </div>
  );
}
