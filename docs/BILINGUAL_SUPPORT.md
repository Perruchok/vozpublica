# Bilingual Support (ES/EN) - VozPública

**Last Updated:** January 9, 2026  
**Status:** ✅ Implemented (Landing, Search, Q&A) | 🔄 Pending (Narrative Evolution)  
**Languages:** 🇪🇸 Spanish (100%) | 🇬🇧 English (100%)

---

## 📋 Overview

VozPública features complete bilingual support for Spanish and English, implemented with a simple approach without external i18n dependencies. The system allows users to interact with the UI in their preferred language while maintaining the original Spanish corpus for search results.

### Key Features

- ✅ Real-time language switching
- ✅ localStorage persistence
- ✅ Dynamic translations with variables
- ✅ Locale-aware date formatting
- ✅ Visual toggle with flags 🇪🇸 🇬🇧
- ✅ Responsive design (mobile-friendly)
- ✅ Zero external dependencies
- ✅ Multilingual query support

---

## 🏗️ Architecture

### 1. Translation Dictionary (`/frontend/lib/translations.js`)

Central dictionary with hierarchical structure:

```javascript
export const translations = {
  es: {
    landing: {
      tagline: "Plataforma de Análisis...",
      hero: { ... },
      services: { ... },
      // ...
    },
    search: { ... },
    qa: { ... },
    narrative: { ... }
  },
  en: {
    landing: {
      tagline: "AI-Powered Platform...",
      hero: { ... },
      services: { ... },
      // Complete English translations
    },
    search: { ... },
    qa: { ... },
    narrative: { ... }
  }
};
```

**450+ lines** covering all UI elements across:
- Landing Page
- Semantic Search
- Q&A with LLM
- Narrative Evolution (ready, pending implementation)
- Contact & Footer

### 2. Helper Functions

#### `getTranslation(lang, keyPath)`
Retrieves a translation using dot notation:

```javascript
getTranslation('es', 'landing.tagline')
// → "Plataforma de Análisis y Consulta de Discurso Político con IA"

getTranslation('en', 'landing.tagline')
// → "AI-Powered Platform for Political Discourse Analysis"
```

#### `formatTranslation(text, params)`
Replaces `{variable}` placeholders:

```javascript
formatTranslation("Found {count} results", { count: 10 })
// → "Found 10 results"

formatTranslation("Resultados para '{query}'", { query: "seguridad" })
// → "Resultados para 'seguridad'"
```

### 3. React Context (`/frontend/lib/languageContext.js`)

Context provider to manage language state throughout the app:

```javascript
import { useLanguage } from '@/lib/languageContext';

function MyComponent() {
  const { language, changeLanguage, t, tf } = useLanguage();
  
  return (
    <div>
      <h1>{t('landing.hero.title')}</h1>
      <p>{tf('search.results.count', { count: 5 })}</p>
    </div>
  );
}
```

**Context API:**
- `language`: current language ('es' | 'en')
- `changeLanguage(newLang)`: changes language and saves to localStorage
- `t(keyPath)`: shortcut for `getTranslation(language, keyPath)`
- `tf(keyPath, params)`: shortcut for translations with formatting
- `translations`: complete translations object for current language

### 4. Language Toggle Component (`/frontend/components/common/LanguageToggle.jsx`)

Visual language switcher with flags:

```jsx
import LanguageToggle from '@/components/common/LanguageToggle';

<LanguageToggle />
```

Features:
- Glassmorphism design
- Hover effects
- Active state highlighting
- Responsive (repositions on mobile)

---

## 📄 Pages with Bilingual Support

### ✅ Implemented

#### 1. Landing Page (`/app/page.jsx`)
- All text translated
- Language toggle in header
- "Back to home" link translated

**Translated sections:**
- Header and tagline
- Hero section
- AI Services (4 services)
- Value Proposition (4 audiences)
- Architecture & Pipeline (5 steps)
- Project Context
- Contact Information
- Footer

#### 2. Semantic Search (`/app/search/page.jsx`)
- Fully translated UI
- Accepts queries in Spanish and English
- Results always in Spanish (original corpus)

**Translated elements:**
- Title and description
- Input placeholder
- Search button
- Hints and tips
- Loading messages
- Results and badges
- Source links

#### 3. Q&A with LLM (`/app/qa/page.jsx`)
- Fully translated UI
- Accepts questions in both languages
- Answers generated in corpus language (Spanish)

**Translated elements:**
- Title and description
- Textarea placeholder
- Action buttons
- Answers and sources
- Dynamic counters
- Links and badges

### 🔄 Pending

**Narrative Evolution** (`/app/narrative/*`)
- Components: `NarrativeEvolutionPage.jsx`, `ConceptForm.jsx`, etc.
- Translations already available in dictionary
- Only needs to import context and use `t()` and `tf()`

---

## 🚀 Quick Start Guide

### Adding Translations to a Page

#### Step 1: Import Context

```javascript
'use client';

import { useLanguage } from '@/lib/languageContext';
import LanguageToggle from '@/components/common/LanguageToggle';
```

#### Step 2: Use the Hook

```javascript
export default function MyPage() {
  const { t, tf } = useLanguage();
  
  return (
    <div>
      <LanguageToggle />
      <h1>{t('mypage.title')}</h1>
      <p>{tf('mypage.message', { name: 'User' })}</p>
    </div>
  );
}
```

#### Step 3: Add Translations to Dictionary

In `/frontend/lib/translations.js`:

```javascript
export const translations = {
  es: {
    // ... other translations
    mypage: {
      title: "Mi Página",
      message: "Hola {name}, bienvenido"
    }
  },
  en: {
    // ... other translations
    mypage: {
      title: "My Page",
      message: "Hello {name}, welcome"
    }
  }
};
```

---

## 💡 Usage Examples

### 1. Basic Component Translation

```jsx
'use client';

import { useLanguage } from '@/lib/languageContext';

export default function ExampleComponent() {
  const { t, language } = useLanguage();
  
  return (
    <div>
      <h1>{t('example.title')}</h1>
      <p>Current language: {language}</p>
    </div>
  );
}
```

### 2. Translations with Variables

```jsx
'use client';

import { useLanguage } from '@/lib/languageContext';

export default function ResultsComponent({ results }) {
  const { tf } = useLanguage();
  
  return (
    <div>
      <h2>{tf('search.results.count', { count: results.length })}</h2>
      <p>{tf('search.results.found', { 
        count: results.length, 
        query: 'public security' 
      })}</p>
    </div>
  );
}
```

Dictionary:
```javascript
es: {
  search: {
    results: {
      count: "{count} fragmentos encontrados",
      found: "Encontrados {count} resultados para '{query}'"
    }
  }
},
en: {
  search: {
    results: {
      count: "{count} fragments found",
      found: "Found {count} results for '{query}'"
    }
  }
}
```

### 3. Programmatic Language Change

```jsx
'use client';

import { useLanguage } from '@/lib/languageContext';

export default function LanguageSelector() {
  const { language, changeLanguage } = useLanguage();
  
  const handleChange = (e) => {
    changeLanguage(e.target.value);
  };
  
  return (
    <select value={language} onChange={handleChange}>
      <option value="es">Español</option>
      <option value="en">English</option>
    </select>
  );
}
```

### 4. Custom Toggle

```jsx
'use client';

import { useLanguage } from '@/lib/languageContext';

export default function CustomToggle() {
  const { language, changeLanguage } = useLanguage();
  
  return (
    <button 
      onClick={() => changeLanguage(language === 'es' ? 'en' : 'es')}
      className="custom-toggle"
    >
      {language === 'es' ? '🇬🇧 English' : '🇪🇸 Español'}
    </button>
  );
}
```

### 5. Form Usage

```jsx
'use client';

import { useState } from 'react';
import { useLanguage } from '@/lib/languageContext';

export default function SearchForm() {
  const { t } = useLanguage();
  const [query, setQuery] = useState('');
  
  return (
    <form>
      <input
        type="text"
        placeholder={t('search.inputPlaceholder')}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button type="submit">
        {t('search.searchButton')}
      </button>
    </form>
  );
}
```

### 6. Locale-Aware Date Formatting

```jsx
'use client';

import { useLanguage } from '@/lib/languageContext';

export default function DateDisplay({ date }) {
  const { language } = useLanguage();
  
  const formatDate = (dateString) => {
    const locale = language === 'en' ? 'en-US' : 'es-MX';
    return new Date(dateString).toLocaleDateString(locale, {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };
  
  return <span>{formatDate(date)}</span>;
}
```

### 7. Validated Form with Translations

```jsx
'use client';

import { useState } from 'react';
import { useLanguage } from '@/lib/languageContext';

export default function ValidatedForm() {
  const { t } = useLanguage();
  const [error, setError] = useState(null);
  
  const handleSubmit = (e) => {
    e.preventDefault();
    
    const query = e.target.query.value;
    
    if (!query.trim()) {
      setError(t('search.errors.emptyQuery'));
      return;
    }
    
    // Process form...
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <input name="query" />
      {error && <div className="error">{error}</div>}
      <button type="submit">{t('search.searchButton')}</button>
    </form>
  );
}
```

### 8. Dynamic Lists

```jsx
'use client';

import { useLanguage } from '@/lib/languageContext';

export default function FeatureList() {
  const { translations } = useLanguage();
  
  // Access full translations object for current language
  const features = translations.landing.valueProposition;
  
  return (
    <div>
      <h2>{features.title}</h2>
      <ul>
        <li>{features.analysts.title}: {features.analysts.description}</li>
        <li>{features.journalists.title}: {features.journalists.description}</li>
        <li>{features.citizens.title}: {features.citizens.description}</li>
        <li>{features.academics.title}: {features.academics.description}</li>
      </ul>
    </div>
  );
}
```

### 9. Conditional Content by Language

```jsx
'use client';

import { useLanguage } from '@/lib/languageContext';

export default function ConditionalContent() {
  const { language } = useLanguage();
  
  return (
    <div>
      {language === 'es' ? (
        <img src="/es-banner.jpg" alt="Banner en español" />
      ) : (
        <img src="/en-banner.jpg" alt="English banner" />
      )}
    </div>
  );
}
```

### 10. Side Effects on Language Change

```jsx
'use client';

import { useLanguage } from '@/lib/languageContext';
import { useEffect } from 'react';

export default function SyncComponent() {
  const { language } = useLanguage();
  
  useEffect(() => {
    // Sync with other systems when language changes
    console.log('Language changed to:', language);
    
    // Update API headers, analytics, etc.
    fetch('/api/set-language', {
      method: 'POST',
      body: JSON.stringify({ language })
    });
  }, [language]);
  
  return <div>Language: {language}</div>;
}
```

---

## 🔍 Multilingual Queries

The system accepts queries in English because:

1. **Multilingual Embeddings**: Sentence transformers capture semantics in multiple languages
2. **Shared Vector Space**: Similar concepts in different languages have close representations
3. **Backend Agnostic**: No special backend modifications needed

**Example:**
- Query in English: "What has the president said about public security?"
- Results: Relevant fragments from Spanish corpus about "seguridad pública"

**Note:** The corpus remains in Spanish (original transcripts), only the UI is translated.

---

## 💾 Language Persistence

Selected language is saved to `localStorage`:

```javascript
localStorage.setItem('vozpublica_language', 'en');
```

And automatically restored when the app loads.

---

## 🎨 Styling

The `LanguageToggle` component is styled with:
- Glassmorphism design
- Hover effects
- Active state highlighting
- Responsive positioning (repositions on mobile)

Styles in `/frontend/styles/globals.css`:
```css
.language-toggle {
  /* Container styles */
}

.lang-button {
  /* Button base styles */
}

.lang-button.active {
  /* Active state */
}
```

---

## 📦 Implementation Summary

### Files Created
- `/frontend/lib/translations.js` (450+ lines)
- `/frontend/lib/languageContext.js`
- `/frontend/components/common/LanguageToggle.jsx`

### Files Modified
- `/frontend/app/layout.jsx` - Wrapped with `<LanguageProvider>`
- `/frontend/app/page.jsx` - Landing page translations
- `/frontend/app/search/page.jsx` - Search page translations
- `/frontend/app/qa/page.jsx` - Q&A page translations
- `/frontend/styles/globals.css` - Added toggle styles

### Metrics
- **Lines added:** ~800
- **Files created:** 3
- **Files modified:** 5
- **Total translation keys:** ~150
- **Components translated:** 3/4 pages (75%)

---

## ✅ Best Practices

1. **Use consistent dot notation** in keyPaths
   ```javascript
   t('section.subsection.key')
   ```

2. **Group translations by page/section**
   ```javascript
   translations.es.search = { ... }
   translations.es.qa = { ... }
   ```

3. **Avoid hardcoded text** in components
   ```javascript
   // ❌ NO
   <h1>Semantic Search</h1>
   
   // ✅ YES
   <h1>{t('search.title')}</h1>
   ```

4. **Use formatTranslation for dynamic values**
   ```javascript
   // ❌ NO
   <p>Found {count} results</p>
   
   // ✅ YES
   <p>{tf('search.results.count', { count })}</p>
   ```

5. **Always mark client components**
   ```javascript
   'use client'; // First line of file
   ```

---

## 🐛 Troubleshooting

### Translations Not Appearing

1. **Verify context is wrapped in layout**
   ```jsx
   // app/layout.jsx
   <LanguageProvider>{children}</LanguageProvider>
   ```

2. **Confirm component uses 'use client'**
   ```javascript
   'use client'; // Must be first line
   ```

3. **Check browser console** for keyPath errors
   ```javascript
   console.log(t('nonexistent.key')); // undefined
   ```

4. **Verify localStorage**
   ```javascript
   localStorage.getItem('vozpublica_language'); // 'es' or 'en'
   ```

### Language Not Persisting

```javascript
// Check if localStorage is available
if (typeof window !== 'undefined') {
  console.log(localStorage.getItem('vozpublica_language'));
}
```

### Testing

```javascript
// Verify translation exists
const { t } = useLanguage();
console.log(t('search.title')); // Should return a string

// Verify language change
const { language, changeLanguage } = useLanguage();
console.log(language); // 'es' or 'en'
changeLanguage('en');
console.log(language); // 'en'

// Verify localStorage
localStorage.getItem('vozpublica_language'); // 'es' or 'en'
```

---

## 🎯 Roadmap

### Short Term
- [ ] Complete Narrative Evolution translation
- [ ] Add toggle to footer
- [ ] Unit tests for translations

### Medium Term
- [ ] Automatic browser language detection
- [ ] LLM response translation to selected language
- [ ] Language preference analytics

### Long Term
- [ ] Bilingual corpus (if documents in English are added)
- [ ] Support for more languages (FR, PT, etc.)
- [ ] Query translation layer for better precision

---

## 🚀 Benefits

### For Users
- Access in preferred language
- Preference persistence
- Consistent UI in both languages
- English queries work correctly

### For Developers
- Simple and direct API
- No external dependencies
- Easy to add new translations
- TypeScript-friendly (type inference)
- Simple testing

### For the Project
- International portfolio
- Broader audience reach
- Demonstrates i18n capability
- Scalable architecture

---

## 📚 Resources

- **Dictionary:** `/frontend/lib/translations.js`
- **Context:** `/frontend/lib/languageContext.js`
- **Toggle:** `/frontend/components/common/LanguageToggle.jsx`
- **Styles:** `/frontend/styles/globals.css` (search `.language-toggle`)

---

## 📊 Testing Checklist

- [x] Language switching works
- [x] localStorage persistence
- [x] Visual toggle responsive
- [x] Correct translations in Landing
- [x] Correct translations in Search
- [x] Correct translations in Q&A
- [x] No console errors
- [x] Build without errors
- [x] Correct date formatting per locale

---

**Status:** ✅ Production Ready  
**Coverage:** Landing, Search, Q&A (75%)  
**Next:** Narrative Evolution implementation
