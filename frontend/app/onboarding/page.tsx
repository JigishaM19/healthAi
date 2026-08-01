"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Navbar from "@/components/Navbar";
import OnboardingWizard from "@/components/OnboardingWizard";
import { getToken, getUser } from "@/lib/auth";

export default function OnboardingPage() {
  const router = useRouter();
  const [user, setUserState] = useState<any>(null);

  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.push("/login");
    } else {
      setUserState(getUser());
    }
  }, [router]);

  return (
    <div className="min-h-screen bg-[#0b1329]">
      <Navbar />
      <OnboardingWizard userName={user?.name || "Friend"} />
    </div>
  );
}
