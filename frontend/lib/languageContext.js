'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { translations, getTranslation as getT, formatTranslation as formatT } from './translations';

const LanguageContext = createContext();

export function LanguageProvider({ children }) {
  const [language, setLanguage] = useState('es');

  // Load language from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('vozpublica_language');
    if (saved && (saved === 'es' || saved === 'en')) {
      setLanguage(saved);
    }
  }, []);

  // Save language to localStorage when it changes
  const changeLanguage = (newLang) => {
    setLanguage(newLang);
    localStorage.setItem('vozpublica_language', newLang);
  };

  const t = (keyPath) => getT(language, keyPath);
  const tf = (keyPath, params) => formatT(getT(language, keyPath), params);

  return (
    <LanguageContext.Provider value={{ language, changeLanguage, t, tf, translations: translations[language] }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
}
