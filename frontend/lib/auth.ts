"use client";

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  const token =
    localStorage.getItem("access_token") ||
    localStorage.getItem("healthai_token") ||
    localStorage.getItem("token");
  if (token === "null" || token === "undefined" || !token) return null;
  return token;
}

export function setToken(token: string): void {
  if (typeof window !== "undefined" && token) {
    localStorage.setItem("healthai_token", token);
    localStorage.setItem("access_token", token);
  }
}

export function removeToken(): void {
  if (typeof window !== "undefined") {
    localStorage.removeItem("healthai_token");
    localStorage.removeItem("access_token");
    localStorage.removeItem("token");
    localStorage.removeItem("healthai_user");
    localStorage.removeItem("user");
  }
}

export function getUser(): any | null {
  if (typeof window === "undefined") return null;
  const data = localStorage.getItem("healthai_user") || localStorage.getItem("user");
  if (!data) return null;
  try {
    return JSON.parse(data);
  } catch (_) {
    return null;
  }
}

export function setUser(user: any): void {
  if (typeof window !== "undefined" && user) {
    localStorage.setItem("healthai_user", JSON.stringify(user));
  }
}

export function getAuthHeaders(): Record<string, string> {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

