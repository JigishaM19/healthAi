import { getAuthHeaders, removeToken } from "./auth";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function request(endpoint: string, options: RequestInit = {}) {
  const headers = {
    "Content-Type": "application/json",
    ...getAuthHeaders(),
    ...(options.headers || {}),
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let errorDetail = "An unexpected error occurred.";
    try {
      const errJson = await response.json();
      errorDetail = errJson.detail || JSON.stringify(errJson);
    } catch (_) {}

    if (response.status === 401) {
      removeToken();
      if (typeof window !== "undefined" && !window.location.pathname.startsWith("/login")) {
        window.location.href = "/login?expired=1";
      }
      throw new Error("Session expired. Please log in again.");
    }

    throw new Error(errorDetail);
  }

  return response.json();
}

export const api = {
  // Auth
  signup: (data: any) => request("/signup", { method: "POST", body: JSON.stringify(data) }),
  login: (data: any) => request("/login", { method: "POST", body: JSON.stringify(data) }),
  getMe: () => request("/me", { method: "GET" }),
  logout: () => request("/logout", { method: "POST" }),

  // Health Profile & Onboarding
  saveOnboarding: (data: any) => request("/onboarding", { method: "POST", body: JSON.stringify(data) }),
  getHealthProfile: () => request("/health-profile", { method: "GET" }),
  updateHealthProfile: (data: any) => request("/health-profile", { method: "PUT", body: JSON.stringify(data) }),
  getHealthSummary: () => request("/health-summary", { method: "GET" }),

  // Chat
  sendMessage: (message: string, conversation_id?: number) =>
    request("/chat", {
      method: "POST",
      body: JSON.stringify({ message, conversation_id }),
    }),
  getChatHistory: () => request("/history", { method: "GET" }),
  deleteConversation: (id: number) => request(`/history/${id}`, { method: "DELETE" }),

  // User Profile
  getUserProfile: () => request("/profile", { method: "GET" }),
  updateUserProfile: (data: any) => request("/profile", { method: "PUT", body: JSON.stringify(data) }),

  // Timeline
  getTimelineEvents: (filterType: string = "all") => request(`/timeline?type=${filterType}`, { method: "GET" }),
  getTimelineStats: () => request("/timeline/stats", { method: "GET" }),
  createTimelineEvent: (data: any) => request("/timeline/event", { method: "POST", body: JSON.stringify(data) }),

  // Universal Medical Document Intelligence
  uploadDocument: async (formData: FormData) => {
    const response = await fetch(`${API_BASE_URL}/documents/upload`, {
      method: "POST",
      headers: {
        ...getAuthHeaders(),
      },
      body: formData,
    });
    if (!response.ok) {
      if (response.status === 401) {
        removeToken();
        if (typeof window !== "undefined" && !window.location.pathname.startsWith("/login")) {
          window.location.href = "/login?expired=1";
        }
        throw new Error("Session expired. Please log in again.");
      }
      const err = await response.json().catch(() => ({}));
      throw new Error(err.detail || "Document upload failed");
    }
    return response.json();
  },
  extractDocument: (id: number) => request(`/documents/${id}/extract`, { method: "POST" }),
  analyzeDocument: (id: number) => request(`/documents/${id}/analyze`, { method: "POST" }),
  listDocuments: () => request("/documents", { method: "GET" }),
  getDocument: (id: number) => request(`/documents/${id}`, { method: "GET" }),
  deleteDocument: (id: number) => request(`/documents/${id}`, { method: "DELETE" }),
  listMedications: () => request("/medications", { method: "GET" }),

  // Health Memory & Lab Trend Comparison
  getHealthInsights: () => request("/health-insights", { method: "GET" }),
  getHealthTrends: () => request("/health-trends", { method: "GET" }),
  getParameterHistory: (testName: string) => request(`/health-trends/${encodeURIComponent(testName)}`, { method: "GET" }),
  askMemory: (question: string) => request("/ask-memory", { method: "POST", body: JSON.stringify({ question }) }),
  listHealthMemories: () => request("/health-memories", { method: "GET" }),

  // Settings & Account Management Center
  getSettings: () => request("/settings", { method: "GET" }),
  updateSettingsAccount: (data: any) => request("/settings/account", { method: "PUT", body: JSON.stringify(data) }),
  updateSettingsPassword: (data: any) => request("/settings/password", { method: "PUT", body: JSON.stringify(data) }),
  updateSettingsNotifications: (data: any) => request("/settings/notifications", { method: "PUT", body: JSON.stringify(data) }),
  updateSettingsAppearance: (data: any) => request("/settings/appearance", { method: "PUT", body: JSON.stringify(data) }),
  updateSettingsLanguage: (data: any) => request("/settings/language", { method: "PUT", body: JSON.stringify(data) }),
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
};
