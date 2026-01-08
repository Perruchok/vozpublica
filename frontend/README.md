# VozPública Frontend

Frontend de la aplicación VozPública para análisis de discurso político.

## Tecnologías

- **Next.js 14** - React framework con App Router
- **React 18** - UI library
- **CSS Modules** - Estilos encapsulados

## Estructura del Proyecto

```
frontend/
├── app/                     # Next.js App Router
│   ├── page.jsx            # Landing page
│   ├── layout.jsx          # Root layout
│   └── narrative/          # Narrative evolution route
│       └── page.jsx
│
├── components/
│   ├── narrative/          # Narrative analysis components
│   │   ├── NarrativeEvolutionPage.jsx
│   │   ├── ConceptForm.jsx
│   │   ├── EvolutionChart.jsx
│   │   ├── ChangeExplanation.jsx
│   │   └── EvidenceComparison.jsx
│   │
│   └── common/             # Shared components
│       ├── LoadingSpinner.jsx
│       └── ErrorBox.jsx
│
├── lib/                    # Utilities
│   ├── api.js             # API client functions
│   └── constants.js       # App constants
│
└── styles/
    └── globals.css        # Global styles
```

## Instalación

```bash
cd frontend
npm install
```

## Configuración

Crea un archivo `.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Desarrollo

```bash
npm run dev
```

Abre [http://localhost:3000](http://localhost:3000) en tu navegador.

## Build para Producción

```bash
npm run build
npm start
```

## Arquitectura de Componentes

### Filosofía de Diseño

Los componentes siguen el patrón de **composición sobre lógica**:

- **Componentes de página**: Orquestan el estado y la lógica
- **Componentes de presentación**: Reciben props, emiten eventos
- **Sin lógica de negocio en componentes**: Todo a través de la API

### Flujo de Datos

```
User Input → Page Component → API Call → Update State → Re-render
```

### Ejemplo: NarrativeEvolutionPage

```jsx
NarrativeEvolutionPage (stateful orchestrator)
├── ConceptForm (controlled input)
├── EvolutionChart (visualization + interaction)
└── ChangeExplanation (LLM output + evidence)
    └── EvidenceComparison (before/after comparison)
```

## API Integration

El frontend se comunica con el backend Flask a través de `/api`:

- `POST /api/analytics/narrative-evolution` - Obtener evolución semántica
- `POST /api/analytics/narrative-explain` - Explicar cambios narrativos

Ver `lib/api.js` para más detalles.

## Estilos

Los estilos globales están en `styles/globals.css` usando CSS variables para temas consistentes:

```css
--primary: #2563eb;
--text-primary: #0f172a;
--bg-primary: #ffffff;
```

## Próximas Características

- [ ] Análisis de tópicos
- [ ] Perfiles de oradores
- [ ] Exportación de reportes
- [ ] Visualizaciones interactivas con D3.js
- [ ] Modo oscuro
