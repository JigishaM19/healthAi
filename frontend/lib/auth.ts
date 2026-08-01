"use client";

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("healthai_token");
}

export function setToken(token: string): void {
  if (typeof window !== "undefined") {
    localStorage.setItem("healthai_token", token);
  }
}

export function removeToken(): void {
  if (typeof window !== "undefined") {
    localStorage.removeItem("healthai_token");
    localStorage.removeItem("healthai_user");
  }
}

export function getUser(): any | null {
  if (typeof window === "undefined") return null;
  const data = localStorage.getItem("healthai_user");
  return data ? JSON.parse(data) : null;
}

export function setUser(user: any): void {
  if (typeof window !== "undefined") {
    localStorage.setItem("healthai_user", JSON.stringify(user));
  }
}

export function getAuthHeaders(): Record<string, string> {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}
