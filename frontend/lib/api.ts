const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

import { getToken, removeToken } from "./auth";

async function request(endpoint: string, options: RequestInit = {}) {
  const token = getToken();

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (res.status === 401) {
    removeToken();
    if (typeof window !== "undefined" && !window.location.pathname.startsWith("/login")) {
      window.location.href = "/login?expired=1";
    }
    throw new Error("Session expired. Please log in again.");
  }

  if (!res.ok) {
    let errorMsg = "An error occurred";
    try {
      const errData = await res.json();
      errorMsg = errData.detail || errData.message || errorMsg;
    } catch (e) {
      // Failed to parse JSON error
    }
    throw new Error(errorMsg);
  }

  // Handle binary PDF or file downloads
  const contentType = res.headers.get("content-type");
  if (contentType && (contentType.includes("application/pdf") || contentType.includes("application/octet-stream"))) {
    return res.blob();
  }

  return res.json();
}

async function uploadDocument(file: File | FormData, documentType: string = "general_medical") {
  const token = getToken();
  let bodyData: FormData;

  if (file instanceof FormData) {
    bodyData = file;
  } else {
    bodyData = new FormData();
    bodyData.append("file", file);
    bodyData.append("document_type", documentType);
  }

  const headers: Record<string, string> = {};
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE_URL}/documents/upload`, {
    method: "POST",
    headers,
    body: bodyData,
  });

  if (res.status === 401) {
    removeToken();
    if (typeof window !== "undefined" && !window.location.pathname.startsWith("/login")) {
      window.location.href = "/login?expired=1";
    }
    throw new Error("Session expired. Please log in again.");
  }

  if (!res.ok) {
    let errorMsg = "Upload failed";
    try {
      const errData = await res.json();
      errorMsg = errData.detail || errData.message || errorMsg;
    } catch (e) {
      // Failed to parse JSON
    }
    throw new Error(errorMsg);
  }

  return res.json();
}

export const api = {
  // Auth
  signup: (data: any) => request("/signup", { method: "POST", body: JSON.stringify(data) }),
  login: (data: any) => request("/login", { method: "POST", body: JSON.stringify(data) }),
  getProfile: () => request("/profile", { method: "GET" }),
  updateProfile: (data: any) => request("/profile", { method: "PUT", body: JSON.stringify(data) }),

  // Onboarding
  saveOnboarding: (data: any) => request("/onboarding", { method: "POST", body: JSON.stringify(data) }),
  getHealthProfile: () => request("/health-profile", { method: "GET" }),
  updateHealthProfile: (data: any) => request("/health-profile", { method: "PUT", body: JSON.stringify(data) }),
  getHealthSummary: () => request("/health-summary", { method: "GET" }),

  // Chat
  sendMessage: (message: string, conversation_id?: number) =>
    request("/chat", { method: "POST", body: JSON.stringify({ message, conversation_id }) }),
  listHistory: () => request("/history", { method: "GET" }),
  getChatHistory: () => request("/history", { method: "GET" }),
  deleteConversation: (id: number) => request(`/history/${id}`, { method: "DELETE" }),

  // Timeline
  getTimeline: (params?: { event_type?: string; start_date?: string; end_date?: string }) => {
    const query = new URLSearchParams(params as any).toString();
    return request(`/timeline${query ? `?${query}` : ""}`, { method: "GET" });
  },
  getTimelineEvents: (event_type?: string) => {
    const query = event_type && event_type !== "all" ? `?event_type=${encodeURIComponent(event_type)}` : "";
    return request(`/timeline${query}`, { method: "GET" });
  },
  createTimelineEvent: (data: any) => request("/timeline/event", { method: "POST", body: JSON.stringify(data) }),
  getTimelineStats: () => request("/timeline/stats", { method: "GET" }),

  // Medical Reports
  uploadDocument,
  listDocuments: (params?: { document_type?: string; date?: string }) => {
    const query = new URLSearchParams(params as any).toString();
    return request(`/documents${query ? `?${query}` : ""}`, { method: "GET" });
  },
  getDocumentDetails: (id: number) => request(`/documents/${id}`, { method: "GET" }),
  getDocument: (id: number) => request(`/documents/${id}`, { method: "GET" }),
  deleteDocument: (id: number) => request(`/documents/${id}`, { method: "DELETE" }),

  // Health Memory & Lab Trends Engine
  getHealthInsights: () => request("/health-insights", { method: "GET" }),
  getHealthTrends: () => request("/health-trends", { method: "GET" }),
  getParameterHistory: (testName: string) => request(`/health-trends/${encodeURIComponent(testName)}`, { method: "GET" }),
  askMemory: (question: string) => request("/ask-memory", { method: "POST", body: JSON.stringify({ question }) }),
  listHealthMemories: () => request("/health-memories", { method: "GET" }),

  // Settings & Account Management Center
  getSettings: () => request("/settings", { method: "GET" }),
  updateSettingsAccount: (data: any) => request("/settings/account", { method: "PUT", body: JSON.stringify(data) }),
  updateSettingsPassword: (data: any) => request("/settings/password", { method: "PUT", body: JSON.stringify(data) }),
  toggle2FA: (data: { enabled: boolean; preferred_method?: string }) => request("/settings/2fa/toggle", { method: "POST", body: JSON.stringify(data) }),
  getSessions: () => request("/settings/sessions", { method: "GET" }),
  updateSettingsNotifications: (data: any) => request("/settings/notifications", { method: "PUT", body: JSON.stringify(data) }),
  updateSettingsPrivacy: (data: { anonymized_research_sharing: number }) => request("/settings/privacy", { method: "PUT", body: JSON.stringify(data) }),
  updateSettingsAppearance: (data: any) => request("/settings/appearance", { method: "PUT", body: JSON.stringify(data) }),
  updateSettingsLanguage: (data: any) => request("/settings/language", { method: "PUT", body: JSON.stringify(data) }),
  getConnectedDevices: () => request("/settings/devices", { method: "GET" }),
  connectDevice: (provider: string, account_id?: string) => request("/settings/devices/connect", { method: "POST", body: JSON.stringify({ provider, account_id }) }),
  disconnectDevice: (provider: string) => request("/settings/devices/disconnect", { method: "POST", body: JSON.stringify({ provider }) }),
  exportHealthData: () => request("/settings/export", { method: "POST" }),
  logoutAllDevices: () => request("/settings/logout-all", { method: "POST" }),
  deleteAccount: (password: string) => request("/settings/account", { method: "DELETE", body: JSON.stringify({ password }) }),

  // Verification, Notifications & Device Security System
  sendVerificationEmail: () => request("/verification/send-email", { method: "POST" }),
  verifyEmail: (token: string) => request(`/verification/email/${token}`, { method: "GET" }),
  sendPhoneOtp: (phone_number: string) => request("/verification/send-otp", { method: "POST", body: JSON.stringify({ phone_number }) }),
  verifyPhoneOtp: (otp_code: string) => request("/verification/verify-otp", { method: "POST", body: JSON.stringify({ otp_code }) }),
  getNotificationHistory: () => request("/notifications/history", { method: "GET" }),
  listDevices: () => request("/devices", { method: "GET" }),
  deleteDevice: (id: number) => request(`/devices/${id}`, { method: "DELETE" }),
  trustDevice: (device_id: number) => request("/devices/trust", { method: "POST", body: JSON.stringify({ device_id }) }),
  triggerMedicationReminder: (medication_name: string) => request("/reminders/medication", { method: "POST", body: JSON.stringify({ medication_name }) }),
  triggerAppointmentReminder: (doctor_name: string, appointment_time: string) => request("/reminders/appointment", { method: "POST", body: JSON.stringify({ doctor_name, appointment_time }) }),
  listReminders: () => request("/reminders", { method: "GET" }),

  // Medical PDF Generation Engine
  getDocumentPdfUrl: (id: number) => `${API_BASE_URL}/documents/${id}/pdf`,
  regenerateDocumentPdf: (id: number) => request(`/documents/${id}/generate-pdf`, { method: "POST" }),

  // AI Nutrition & Diet Planning System
  getNutritionPlan: () => request("/nutrition/plan", { method: "GET" }),
  generateNutritionPlan: () => request("/nutrition/generate", { method: "POST" }),
  getNutritionHistory: () => request("/nutrition/history", { method: "GET" }),
  getGroceryList: () => request("/nutrition/grocery-list", { method: "GET" }),
  getWorkoutPlan: () => request("/nutrition/workout-plan", { method: "GET" }),
  getDailyRoutine: () => request("/nutrition/daily-routine", { method: "GET" }),

  // Medication Safety Intelligence Engine
  checkMedicationInteractions: (medications: string[]) => request("/medications/check-interactions", { method: "POST", body: JSON.stringify({ medications }) }),
  getMedicationSafetyReport: () => request("/medications/safety-report", { method: "GET" }),
  getMedicationSchedule: () => request("/medications/schedule", { method: "GET" }),
  analyzePrescriptionMedications: (extracted_medications: string[], document_id?: number) => request("/medications/analyze-prescription", { method: "POST", body: JSON.stringify({ extracted_medications, document_id }) }),
  getMedicationSafetyPdfUrl: () => `${API_BASE_URL}/medications/safety-report/pdf`
};
