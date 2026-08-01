"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { api } from "@/lib/api";
import { getToken } from "@/lib/auth";

export type LanguageCode = "English" | "Hindi" | "Spanish" | "French" | "German";
export type UnitSystem = "Metric" | "Imperial";
export type ThemeMode = "dark" | "light" | "system";

export const translations: Record<LanguageCode, Record<string, string>> = {
  English: {
    dashboard: "Dashboard",
    consultation: "AI Consultation Chat",
    chat: "AI Chat",
    healthProfile: "Health Profile",
    medicalReports: "Medical Reports",
    timeline: "Health Timeline",
    settings: "Settings & Account",
    save: "Save Changes",
    cancel: "Cancel",
    logout: "Logout",
    notifications: "Notifications",
    account: "Account Profile",
    security: "Security & Passwords",
    privacy: "Data & Export",
    appearance: "Appearance",
    language: "Language & Region",
    devices: "Connected Devices",
    dangerZone: "Danger Zone",
    deleteAccount: "Delete Account",
    welcomeBack: "Welcome back to HealthAI",
    healthSummary: "Personalized Health Summary",
    activeMedications: "Active Medications",
    allergies: "Allergies & Sensitivities",
    conditions: "Medical Conditions",
    recentReports: "Recent Medical Reports",
    labTrends: "Lab Trends & History",
    nutrition: "AI Nutrition Plan",
    medicationSafety: "Medication Safety",
    connected: "Connected",
    notConnected: "Not Connected",
    lastSynced: "Last Synced",
    theme: "Theme",
    units: "Unit System",
    metric: "Metric (kg, cm, °C, L)",
    imperial: "Imperial (lbs, ft/in, °F, oz)",
  },
  Hindi: {
    dashboard: "डैशबोर्ड",
    consultation: "एआई परामर्श चैट",
    chat: "एआई चैट",
    healthProfile: "स्वास्थ्य प्रोफ़ाइल",
    medicalReports: "मेडिकल रिपोर्ट",
    timeline: "स्वास्थ्य टाइमलाइन",
    settings: "सेटिंग्स और खाता",
    save: "सहेजें",
    cancel: "रद्द करें",
    logout: "लॉगआउट",
    notifications: "सूचनाएं",
    account: "खाता प्रोफ़ाइल",
    security: "सुरक्षा और पासवर्ड",
    privacy: "डेटा और निर्यात",
    appearance: "दिखावट",
    language: "भाषा और क्षेत्र",
    devices: "कनेक्ट किए गए डिवाइस",
    dangerZone: "खतरा क्षेत्र",
    deleteAccount: "खाता हटाएँ",
    welcomeBack: "HealthAI में आपका स्वागत है",
    healthSummary: "व्यक्तिगत स्वास्थ्य सारांश",
    activeMedications: "सक्रिय दवाएं",
    allergies: "एलर्जी और संवेदनशीलता",
    conditions: "चिकित्सा स्थितियां",
    recentReports: "हाल की मेडिकल रिपोर्ट",
    labTrends: "लैब रुझान और इतिहास",
    nutrition: "एआई पोषण योजना",
    medicationSafety: "दवा सुरक्षा",
    connected: "कनेक्टेड",
    notConnected: "कनेक्ट नहीं है",
    lastSynced: "अंतिम सिंक",
    theme: "थीम",
    units: "इकाई प्रणाली",
    metric: "मेट्रिक (किग्रा, सेमी, °C, लीटर)",
    imperial: "इंपीरियल (पाउंड, फीट/इंच, °F, औंस)",
  },
  Spanish: {
    dashboard: "Panel Principal",
    consultation: "Chat de Consulta IA",
    chat: "Chat IA",
    healthProfile: "Perfil de Salud",
    medicalReports: "Informes Médicos",
    timeline: "Cronología de Salud",
    settings: "Configuración y Cuenta",
    save: "Guardar Cambios",
    cancel: "Cancelar",
    logout: "Cerrar Sesión",
    notifications: "Notificaciones",
    account: "Perfil de Cuenta",
    security: "Seguridad y Contraseñas",
    privacy: "Datos y Exportación",
    appearance: "Apariencia",
    language: "Idioma y Región",
    devices: "Dispositivos Conectados",
    dangerZone: "Zona de Peligro",
    deleteAccount: "Eliminar Cuenta",
    welcomeBack: "Bienvenido de nuevo a HealthAI",
    healthSummary: "Resumen de Salud Personalizado",
    activeMedications: "Medicamentos Activos",
    allergies: "Alergias y Sensabilidades",
    conditions: "Condiciones Médicas",
    recentReports: "Informes Médicos Recientes",
    labTrends: "Tendencias de Laboratorio",
    nutrition: "Plan de Nutrición IA",
    medicationSafety: "Seguridad de Medicamentos",
    connected: "Conectado",
    notConnected: "No Conectado",
    lastSynced: "Última Sincronización",
    theme: "Tema",
    units: "Sistema de Unidades",
    metric: "Métrico (kg, cm, °C, L)",
    imperial: "Imperial (lbs, ft/in, °F, oz)",
  },
  French: {
    dashboard: "Tableau de Bord",
    consultation: "Chat de Consultation IA",
    chat: "Chat IA",
    healthProfile: "Profil de Santé",
    medicalReports: "Rapports Médicaux",
    timeline: "Chronologie de Santé",
    settings: "Paramètres et Compte",
    save: "Enregistrer",
    cancel: "Annuler",
    logout: "Déconnexion",
    notifications: "Notifications",
    account: "Profil de Compte",
    security: "Sécurité et Mots de Passe",
    privacy: "Données et Exportation",
    appearance: "Apparence",
    language: "Langue et Région",
    devices: "Appareils Connectés",
    dangerZone: "Zone de Danger",
    deleteAccount: "Supprimer le Compte",
    welcomeBack: "Bienvenue sur HealthAI",
    healthSummary: "Résumé de Santé Personnalisé",
    activeMedications: "Médicaments Actifs",
    allergies: "Allergies et Sensibilités",
    conditions: "Conditions Médicales",
    recentReports: "Rapports Médicaux Récents",
    labTrends: "Tendances de Laboratoire",
    nutrition: "Plan de Nutrition IA",
    medicationSafety: "Sécurité des Médicaments",
    connected: "Connecté",
    notConnected: "Non Connecté",
    lastSynced: "Dernière Synchronisation",
    theme: "Thème",
    units: "Système d'Unités",
    metric: "Métrique (kg, cm, °C, L)",
    imperial: "Impérial (lbs, ft/in, °F, oz)",
  },
  German: {
    dashboard: "Dashboard",
    consultation: "KI-Beratungs-Chat",
    chat: "KI-Chat",
    healthProfile: "Gesundheitsprofil",
    medicalReports: "Medizinische Berichte",
    timeline: "Gesundheits-Chronik",
    settings: "Einstellungen & Konto",
    save: "Speichern",
    cancel: "Abbrechen",
    logout: "Abmelden",
    notifications: "Benachrichtigungen",
    account: "Kontoprofil",
    security: "Sicherheit & Passwörter",
    privacy: "Daten & Export",
    appearance: "Erscheinungsbild",
    language: "Sprache & Region",
    devices: "Verbundene Geräte",
    dangerZone: "Gefahrenzone",
    deleteAccount: "Konto Löschen",
    welcomeBack: "Willkommen zurück bei HealthAI",
    healthSummary: "Personalisierte Gesundheitsübersicht",
    activeMedications: "Aktive Medikamente",
    allergies: "Allergien & Empfindlichkeiten",
    conditions: "Medizinische Zustände",
    recentReports: "Neueste Medizinische Berichte",
    labTrends: "Laborwerte & Verlauf",
    nutrition: "KI-Ernährungsplan",
    medicationSafety: "Medikamentensicherheit",
    connected: "Verbunden",
    notConnected: "Nicht Verbunden",
    lastSynced: "Zuletzt Synchronisiert",
    theme: "Design",
    units: "Einheitensystem",
    metric: "Metrisch (kg, cm, °C, L)",
    imperial: "Imperial (lbs, ft/in, °F, oz)",
  }
};

interface LanguageContextType {
  language: LanguageCode;
  units: UnitSystem;
  theme: ThemeMode;
  fontSize: string;
  reduceAnim: boolean;
  setLanguage: (lang: LanguageCode) => void;
  setUnits: (u: UnitSystem) => void;
  setTheme: (t: ThemeMode) => void;
  setFontSize: (size: string) => void;
  setReduceAnim: (reduce: boolean) => void;
  t: (key: string) => string;
  convertWeight: (kg?: number | null) => string;
  convertHeight: (cm?: number | null) => string;
  convertTemp: (celsius?: number | null) => string;
  convertVolume: (liters?: number | null) => string;
}

const LanguageContext = createContext<LanguageContextType>({
  language: "English",
  units: "Metric",
  theme: "dark",
  fontSize: "medium",
  reduceAnim: false,
  setLanguage: () => {},
  setUnits: () => {},
  setTheme: () => {},
  setFontSize: () => {},
  setReduceAnim: () => {},
  t: (key) => key,
  convertWeight: () => "",
  convertHeight: () => "",
  convertTemp: () => "",
  convertVolume: () => "",
});

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [language, setLanguageState] = useState<LanguageCode>("English");
  const [units, setUnitsState] = useState<UnitSystem>("Metric");
  const [theme, setThemeState] = useState<ThemeMode>("dark");
  const [fontSize, setFontSizeState] = useState<string>("medium");
  const [reduceAnim, setReduceAnimState] = useState<boolean>(false);

  const applyThemeToDOM = (tMode: ThemeMode) => {
    if (typeof document === "undefined") return;
    const root = document.documentElement;
    root.classList.remove("dark", "light");
    if (tMode === "system") {
      const isSystemDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
      root.classList.add(isSystemDark ? "dark" : "light");
    } else {
      root.classList.add(tMode);
    }
  };

  const applyFontSizeToDOM = (size: string) => {
    if (typeof document === "undefined") return;
    const root = document.documentElement;
    root.classList.remove("font-small", "font-medium", "font-large");
    root.classList.add(`font-${size}`);
  };

  const applyReduceAnimToDOM = (reduce: boolean) => {
    if (typeof document === "undefined") return;
    const root = document.documentElement;
    root.classList.toggle("reduce-motion", reduce);
  };

  useEffect(() => {
    // 1. Initial Load from LocalStorage
    const savedLang = localStorage.getItem("healthai_lang") as LanguageCode;
    const savedUnits = localStorage.getItem("healthai_units") as UnitSystem;
    const savedTheme = localStorage.getItem("healthai_theme") as ThemeMode;
    const savedFontSize = localStorage.getItem("healthai_fontsize");
    const savedReduceAnim = localStorage.getItem("healthai_reduce_anim");

    if (savedLang && translations[savedLang]) setLanguageState(savedLang);
    if (savedUnits) setUnitsState(savedUnits);
    if (savedTheme) {
      setThemeState(savedTheme);
      applyThemeToDOM(savedTheme);
    } else {
      applyThemeToDOM("dark");
    }

    if (savedFontSize) {
      setFontSizeState(savedFontSize);
      applyFontSizeToDOM(savedFontSize);
    }
    if (savedReduceAnim !== null) {
      const isRed = savedReduceAnim === "true";
      setReduceAnimState(isRed);
      applyReduceAnimToDOM(isRed);
    }

    // 2. Fetch from Backend if authenticated
    const token = getToken();
    if (token) {
      api.getSettings()
        .then((res) => {
          if (res.settings) {
            if (res.settings.language && translations[res.settings.language as LanguageCode]) {
              setLanguageState(res.settings.language as LanguageCode);
              localStorage.setItem("healthai_lang", res.settings.language);
            }
            if (res.settings.units) {
              setUnitsState(res.settings.units as UnitSystem);
              localStorage.setItem("healthai_units", res.settings.units);
            }
            if (res.settings.theme) {
              const th = res.settings.theme as ThemeMode;
              setThemeState(th);
              applyThemeToDOM(th);
              localStorage.setItem("healthai_theme", th);
            }
            if (res.settings.font_size) {
              setFontSizeState(res.settings.font_size);
              applyFontSizeToDOM(res.settings.font_size);
              localStorage.setItem("healthai_fontsize", res.settings.font_size);
            }
            if (res.settings.reduce_animations !== undefined) {
              const red = Boolean(res.settings.reduce_animations);
              setReduceAnimState(red);
              applyReduceAnimToDOM(red);
              localStorage.setItem("healthai_reduce_anim", red ? "true" : "false");
            }
          }
        })
        .catch(() => {});
    }
  }, []);

  const setLanguage = (lang: LanguageCode) => {
    setLanguageState(lang);
    localStorage.setItem("healthai_lang", lang);
  };

  const setUnits = (u: UnitSystem) => {
    setUnitsState(u);
    localStorage.setItem("healthai_units", u);
  };

  const setTheme = (tMode: ThemeMode) => {
    setThemeState(tMode);
    applyThemeToDOM(tMode);
    localStorage.setItem("healthai_theme", tMode);
  };

  const setFontSize = (size: string) => {
    setFontSizeState(size);
    applyFontSizeToDOM(size);
    localStorage.setItem("healthai_fontsize", size);
  };

  const setReduceAnim = (reduce: boolean) => {
    setReduceAnimState(reduce);
    applyReduceAnimToDOM(reduce);
    localStorage.setItem("healthai_reduce_anim", reduce ? "true" : "false");
  };

  const t = (key: string): string => {
    const langDict = translations[language] || translations["English"];
    return langDict[key] || translations["English"][key] || key;
  };

  const convertWeight = (kg?: number | null): string => {
    if (kg === undefined || kg === null || isNaN(kg)) return "";
    if (units === "Imperial") {
      const lbs = Math.round(kg * 2.20462);
      return `${lbs} lbs`;
    }
    return `${kg} kg`;
  };

  const convertHeight = (cm?: number | null): string => {
    if (cm === undefined || cm === null || isNaN(cm)) return "";
    if (units === "Imperial") {
      const totalInches = cm / 2.54;
      const feet = Math.floor(totalInches / 12);
      const inches = Math.round(totalInches % 12);
      return `${feet}′ ${inches}″`;
    }
    return `${cm} cm`;
  };

  const convertTemp = (celsius?: number | null): string => {
    if (celsius === undefined || celsius === null || isNaN(celsius)) return "";
    if (units === "Imperial") {
      const f = Math.round((celsius * 9) / 5 + 32);
      return `${f}°F`;
    }
    return `${celsius}°C`;
  };

  const convertVolume = (liters?: number | null): string => {
    if (liters === undefined || liters === null || isNaN(liters)) return "";
    if (units === "Imperial") {
      const oz = Math.round(liters * 33.814);
      return `${oz} oz`;
    }
    return `${liters} L`;
  };

  return (
    <LanguageContext.Provider value={{
      language, units, theme, fontSize, reduceAnim,
      setLanguage, setUnits, setTheme, setFontSize, setReduceAnim,
      t, convertWeight, convertHeight, convertTemp, convertVolume
    }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  return useContext(LanguageContext);
}
