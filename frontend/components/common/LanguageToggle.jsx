'use client';

import React from 'react';
import { useLanguage } from '@/lib/languageContext';

export default function LanguageToggle() {
  const { language, changeLanguage } = useLanguage();

  return (
    <div className="language-toggle">
      <button
        className={`lang-button ${language === 'es' ? 'active' : ''}`}
        onClick={() => changeLanguage('es')}
        aria-label="Cambiar a español"
      >
        🇪🇸 ES
      </button>
      <button
        className={`lang-button ${language === 'en' ? 'active' : ''}`}
        onClick={() => changeLanguage('en')}
        aria-label="Switch to English"
      >
        🇬🇧 EN
      </button>
    </div>
  );
}
