# Soporte Bilingüe (ES/EN) - VozPública

## Descripción General

VozPública ahora cuenta con soporte completo para español e inglés, implementado con un enfoque simple y sin dependencias externas de i18n.

## Arquitectura de Traducciones

### 1. Diccionario de Traducciones (`/frontend/lib/translations.js`)

El sistema utiliza un diccionario JavaScript con la siguiente estructura:

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
    landing: { ... },
    // Traducciones completas en inglés
  }
};
```

### 2. Funciones de Ayuda

- **`getTranslation(lang, keyPath)`**: Recupera una traducción usando notación de punto
  ```javascript
  getTranslation('es', 'landing.tagline')
  // → "Plataforma de Análisis y Consulta de Discurso Político con IA"
  ```

- **`formatTranslation(text, params)`**: Reemplaza placeholders `{variable}` en el texto
  ```javascript
  formatTranslation("Found {count} results", { count: 10 })
  // → "Found 10 results"
  ```

### 3. Contexto de React (`/frontend/lib/languageContext.js`)

Proveedor de contexto para gestionar el estado del idioma:

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

**API del Contexto:**
- `language`: idioma actual ('es' o 'en')
- `changeLanguage(newLang)`: cambia el idioma y guarda en localStorage
- `t(keyPath)`: atajo para `getTranslation(language, keyPath)`
- `tf(keyPath, params)`: atajo para traducciones con formato
- `translations`: objeto de traducciones para el idioma actual

### 4. Componente de Toggle (`/frontend/components/common/LanguageToggle.jsx`)

Botón de cambio de idioma con banderas:

```jsx
import LanguageToggle from '@/components/common/LanguageToggle';

<LanguageToggle />
```

## Páginas con Soporte Bilingüe

### ✅ Implementadas

1. **Landing Page** (`/app/page.jsx`)
   - Todos los textos traducidos
   - Toggle de idioma en el header

2. **Búsqueda Semántica** (`/app/search/page.jsx`)
   - UI completamente traducida
   - Acepta queries en español e inglés
   - Resultados siempre en español (corpus original)

3. **Q&A con LLM** (`/app/qa/page.jsx`)
   - UI completamente traducida
   - Acepta preguntas en ambos idiomas
   - Respuestas generadas en el idioma del corpus (español)

### 🔄 Pendientes

- **Narrative Evolution** (`/app/narrative/*`)
  - Componentes: `NarrativeEvolutionPage.jsx`, `ConceptForm.jsx`, etc.
  - Traducciones ya disponibles en el diccionario
  - Solo falta importar contexto y usar `t()` y `tf()`

## Cómo Agregar Traducciones a una Página

### Paso 1: Importar el Contexto

```javascript
'use client';

import { useLanguage } from '@/lib/languageContext';
import LanguageToggle from '@/components/common/LanguageToggle';
```

### Paso 2: Usar el Hook

```javascript
export default function MyPage() {
  const { t, tf } = useLanguage();
  
  return (
    <div>
      <LanguageToggle />
      <h1>{t('mypage.title')}</h1>
      <p>{tf('mypage.message', { name: 'Usuario' })}</p>
    </div>
  );
}
```

### Paso 3: Agregar Traducciones al Diccionario

En `/frontend/lib/translations.js`:

```javascript
export const translations = {
  es: {
    // ... otras traducciones
    mypage: {
      title: "Mi Página",
      message: "Hola {name}, bienvenido"
    }
  },
  en: {
    // ... otras traducciones
    mypage: {
      title: "My Page",
      message: "Hello {name}, welcome"
    }
  }
};
```

## Queries en Inglés

El sistema acepta queries en inglés porque:

1. **Embeddings Multilingües**: Los embeddings de sentence-transformers capturan semántica en múltiples idiomas
2. **Espacio Vectorial Compartido**: Conceptos similares en diferentes idiomas tienen representaciones cercanas
3. **Backend Agnóstico**: El backend no necesita modificaciones especiales

**Ejemplo:**
- Query en inglés: "What has the president said about public security?"
- Resultados: Fragmentos relevantes del corpus en español sobre "seguridad pública"

## Persistencia del Idioma

El idioma seleccionado se guarda en `localStorage`:

```javascript
localStorage.setItem('vozpublica_language', 'en');
```

Y se recupera automáticamente al cargar la aplicación.

## Estilos del Toggle

El componente `LanguageToggle` está estilizado con:
- Diseño glassmorphism
- Hover effects
- Estado activo destacado
- Responsive (se reposiciona en móvil)

Ver estilos en `/frontend/styles/globals.css`:
```css
.language-toggle { ... }
.lang-button { ... }
.lang-button.active { ... }
```

## Mejores Prácticas

1. **Usa notación de punto consistente** en los keyPaths
   ```javascript
   t('section.subsection.key')
   ```

2. **Agrupa traducciones por página/sección**
   ```javascript
   translations.es.search = { ... }
   translations.es.qa = { ... }
   ```

3. **Evita hardcodear texto** en componentes
   ```javascript
   // ❌ NO
   <h1>Búsqueda Semántica</h1>
   
   // ✅ SÍ
   <h1>{t('search.title')}</h1>
   ```

4. **Usa formatTranslation para valores dinámicos**
   ```javascript
   // ❌ NO
   <p>Encontrados {count} resultados</p>
   
   // ✅ SÍ
   <p>{tf('search.results.count', { count })}</p>
   ```

## Roadmap

### Corto Plazo
- [ ] Completar traducción de Narrative Evolution
- [ ] Agregar toggle en todas las páginas
- [ ] Testing exhaustivo de cambio de idioma

### Mediano Plazo
- [ ] Detección automática de idioma del navegador
- [ ] Traducciones adicionales (francés, portugués)
- [ ] Backend: traducción automática de respuestas LLM al idioma seleccionado

### Largo Plazo
- [ ] Corpus multilingüe (transcripciones en otros idiomas)
- [ ] Query translation layer para mejor precisión
- [ ] A/B testing de preferencias de idioma por región

## Debugging

Si las traducciones no aparecen:

1. **Verifica que el contexto esté envuelto en el layout**
   ```jsx
   // app/layout.jsx
   <LanguageProvider>{children}</LanguageProvider>
   ```

2. **Confirma que el componente usa 'use client'**
   ```javascript
   'use client'; // Primera línea
   ```

3. **Revisa la consola del navegador** para errores de keyPath
   ```javascript
   console.log(t('nonexistent.key')); // undefined
   ```

4. **Verifica localStorage**
   ```javascript
   localStorage.getItem('vozpublica_language'); // 'es' o 'en'
   ```

## Recursos

- Diccionario: `/frontend/lib/translations.js`
- Contexto: `/frontend/lib/languageContext.js`
- Toggle: `/frontend/components/common/LanguageToggle.jsx`
- Estilos: `/frontend/styles/globals.css` (buscar `.language-toggle`)

---

**Última actualización**: Diciembre 2024
**Estado**: ✅ Implementado en Landing, Search y Q&A | 🔄 Pendiente en Narrative Evolution
