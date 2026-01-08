# Ejemplos de Uso - Sistema de Traducciones

## 1. Uso Básico en un Componente

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

## 2. Traducciones con Variables

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
        query: 'seguridad pública' 
      })}</p>
    </div>
  );
}
```

Diccionario correspondiente:
```javascript
// translations.js
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

## 3. Cambio de Idioma Programático

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

## 4. Toggle de Idioma Personalizado

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

## 5. Uso en Formularios

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

## 6. Traducciones con HTML

```jsx
'use client';

import { useLanguage } from '@/lib/languageContext';

export default function RichTextComponent() {
  const { t } = useLanguage();
  
  // Si el texto contiene HTML
  return (
    <div 
      dangerouslySetInnerHTML={{ 
        __html: t('landing.projectContext.intro') 
      }} 
    />
  );
}
```

Diccionario correspondiente:
```javascript
es: {
  landing: {
    projectContext: {
      intro: "VozPública es un <strong>proyecto independiente</strong>..."
    }
  }
}
```

## 7. Formateo de Fechas según Idioma

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

## 8. Condicionalmente según Idioma

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

## 9. Validación de Formularios Traducida

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

## 10. Usar Traducciones en Meta Tags

```jsx
import { useLanguage } from '@/lib/languageContext';

export default function PageWithMeta() {
  const { t } = useLanguage();
  
  // Note: For actual meta tags, you'd use Next.js metadata API
  return (
    <>
      <title>{t('search.meta.title')}</title>
      <div className="page-content">
        {/* ... */}
      </div>
    </>
  );
}
```

## 11. Listas Dinámicas Traducidas

```jsx
'use client';

import { useLanguage } from '@/lib/languageContext';

export default function FeatureList() {
  const { translations } = useLanguage();
  
  // Access the full translations object for the current language
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

## 12. Integración con Estado Global

```jsx
'use client';

import { useLanguage } from '@/lib/languageContext';
import { useEffect } from 'react';

export default function SyncComponent() {
  const { language } = useLanguage();
  
  useEffect(() => {
    // Sincronizar con otros sistemas cuando cambie el idioma
    console.log('Language changed to:', language);
    
    // Actualizar API headers, analytics, etc.
    fetch('/api/set-language', {
      method: 'POST',
      body: JSON.stringify({ language })
    });
  }, [language]);
  
  return <div>Language: {language}</div>;
}
```

---

## Agregar Nuevas Traducciones

### 1. Editar el Diccionario

```javascript
// /frontend/lib/translations.js

export const translations = {
  es: {
    // ... traducciones existentes
    newSection: {
      title: "Nuevo Título",
      description: "Nueva descripción con {variable}"
    }
  },
  en: {
    // ... traducciones existentes
    newSection: {
      title: "New Title",
      description: "New description with {variable}"
    }
  }
};
```

### 2. Usar en el Componente

```jsx
'use client';

import { useLanguage } from '@/lib/languageContext';

export default function NewComponent() {
  const { t, tf } = useLanguage();
  
  return (
    <div>
      <h1>{t('newSection.title')}</h1>
      <p>{tf('newSection.description', { variable: 'valor' })}</p>
    </div>
  );
}
```

---

## Testing

```javascript
// Verificar que la traducción existe
const { t } = useLanguage();
console.log(t('search.title')); // Debe devolver un string

// Verificar cambio de idioma
const { language, changeLanguage } = useLanguage();
console.log(language); // 'es' o 'en'
changeLanguage('en');
console.log(language); // 'en'

// Verificar localStorage
localStorage.getItem('vozpublica_language'); // 'es' o 'en'
```
