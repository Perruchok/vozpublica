/**
 * Translation dictionaries for ES/EN support
 * Simple i18n system without external libraries
 */

export const translations = {
  es: {
    // Navigation & Common
    language: 'Idioma',
    spanish: 'Español',
    english: 'English',
    
    // Landing Page
    tagline: 'Plataforma de Análisis y Consulta de Discurso Político con IA',
    hero: {
      description: 'VozPública es una plataforma avanzada de análisis computacional del discurso político que emplea inteligencia artificial y procesamiento de lenguaje natural para extraer insights de las comunicaciones oficiales de la Presidencia de México.',
      dataSource: 'Fuente de datos:',
      dataSourceText: 'Discursos presidenciales oficiales, conferencias de prensa, entrevistas y comunicados de',
      coverage: 'Cobertura:',
      coverageText: 'Octubre 2024 en adelante (Administración Claudia Sheinbaum)'
    },
    
    // Services
    services: {
      title: 'Servicios de IA Disponibles',
      search: {
        icon: '🔍',
        title: 'Búsqueda Semántica',
        description: 'Encuentra fragmentos del discurso presidencial por significado, no solo por coincidencia de palabras.',
        cta: 'Explorar Búsqueda'
      },
      qa: {
        icon: '💬',
        title: 'Pregunta y Respuesta (LLM)',
        description: 'Formula preguntas en lenguaje natural sobre el contenido de los discursos. Respuestas generadas por IA basadas en el corpus presidencial.',
        cta: 'Hacer Preguntas'
      },
      narrative: {
        icon: '📊',
        title: 'Evolución Narrativa',
        description: 'Analiza cómo conceptos políticos específicos cambian su significado semántico a través del tiempo. Detecta drift conceptual y cambios de contexto.',
        cta: 'Ver Evolución'
      },
      topics: {
        icon: '🎯',
        title: 'Descubrimiento Automático de Tópicos',
        description: 'Identificación no supervisada de temas dominantes en el discurso presidencial usando clustering semántico y modelado de tópicos.',
        comingSoon: 'Próximamente'
      }
    },
    
    // Value Proposition
    valueProposition: {
      title: '¿Para quién es VozPública?',
      analysts: {
        title: 'Para Analistas Políticos',
        description: 'Identifica cambios en prioridades gubernamentales, evolución de narrativas y patrones discursivos con precisión cuantitativa.'
      },
      journalists: {
        title: 'Para Periodistas e Investigadores',
        description: 'Busca declaraciones específicas, verifica contextos históricos y encuentra contradicciones o consistencias en el discurso oficial.'
      },
      citizens: {
        title: 'Para Ciudadanos Informados',
        description: 'Accede a análisis basados en datos sobre cómo el gobierno comunica sus políticas y comprende la evolución del discurso público.'
      },
      academics: {
        title: 'Para Académicos',
        description: 'Utiliza herramientas de análisis semántico avanzado para investigación en ciencias políticas, comunicación y lingüística computacional.'
      }
    },
    
    // How it Works
    howItWorks: {
      title: 'Arquitectura y flujo de análisis',
      intro: 'VozPública está diseñada como una plataforma modular de análisis semántico, capaz de procesar grandes volúmenes de discurso político y convertirlos en información consultable e interpretable.',
      steps: {
        ingestion: {
          title: 'Ingesta automatizada de datos:',
          description: 'Extracción continua de transcripciones oficiales desde gob.mx/presidencia, incluyendo discursos, conferencias de prensa, entrevistas y comunicados. Los datos se actualizan de forma periódica para mantener la base de conocimiento vigente.'
        },
        processing: {
          title: 'Procesamiento y estructuración:',
          description: 'Limpieza del texto, segmentación en unidades discursivas y enriquecimiento con metadatos estructurados (fecha, tipo de evento, orador, contexto institucional).'
        },
        semantic: {
          title: 'Representación semántica:',
          description: 'Conversión de cada fragmento discursivo en representaciones vectoriales mediante modelos de lenguaje preentrenados (sentence transformers), capturando significado y contexto más allá de palabras clave.'
        },
        storage: {
          title: 'Almacenamiento e indexación vectorial:',
          description: 'Persistencia en una base de datos vectorial con índices HNSW, optimizada para consultas de similitud semántica a gran escala.'
        },
        analysis: {
          title: 'Servicios de Análisis y Consulta:',
          description: 'Exposición de capacidades analíticas mediante APIs: búsqueda semántica, preguntas y respuestas con RAG, y análisis de evolución narrativa a través de series temporales semánticas.'
        }
      }
    },
    
    // Project Context
    projectContext: {
      title: 'Contexto del Proyecto',
      description: 'VozPública es un proyecto independiente de investigación y desarrollo. Forma parte de un portafolio profesional enfocado en:',
      focus: [
        'Arquitectura de sistemas de análisis de datos a gran escala',
        'Implementación de pipelines de ML/NLP en producción',
        'Diseño de interfaces para exploración de datos complejos',
        'Aplicación de IA a problemas de ciencias sociales y análisis político'
      ],
      disclaimer: 'Nota: Este es un proyecto no partidista y sin fines de lucro. El objetivo es demostrar aplicaciones tecnológicas avanzadas para análisis de discurso público.'
    },
    
    // Contact
    contact: {
      title: 'Contacto',
      intro: 'Si te interesa el proyecto, su enfoque técnico o posibles colaboraciones, no dudes en contactarme:',
      role: 'Data Engineer & AI Developer'
    },
    
    // Footer
    footer: 'VozPública - Plataforma de Análisis de Discurso Político | Proyecto de Investigación Independiente',
    
    // Search Page
    search: {
      title: 'Búsqueda Semántica',
      description: 'Busca en el corpus de discursos presidenciales usando lenguaje natural. El sistema encuentra fragmentos relevantes basándose en el significado, no solo en coincidencias exactas de palabras.',
      placeholder: 'Ejemplo: ¿Qué ha dicho la presidenta sobre seguridad pública?',
      button: 'Buscar',
      searching: 'Buscando...',
      tip: 'Tip: Usa preguntas completas o conceptos específicos para mejores resultados',
      results: 'Resultados',
      resultsCount: 'fragmentos encontrados',
      noResults: 'No se encontraron resultados',
      noResultsText: 'Intenta reformular tu consulta o usar términos diferentes',
      analyzing: 'Analizando corpus presidencial...',
      relevance: 'relevancia',
      viewSource: 'Ver fuente original',
      errorPlaceholder: 'Por favor ingresa una consulta'
    },
    
    // Q&A Page
    qa: {
      title: 'Pregunta y Respuesta',
      description: 'Formula preguntas en lenguaje natural sobre el discurso presidencial. El sistema utiliza IA para generar respuestas basadas en el corpus oficial, proporcionando contexto y fuentes relevantes.',
      placeholder: 'Ejemplo: ¿Cuál es la posición del gobierno sobre la reforma energética?',
      button: 'Preguntar',
      processing: 'Procesando...',
      tip: 'Tip: Haz preguntas específicas sobre políticas, declaraciones o temas concretos',
      answer: 'Respuesta',
      sources: 'Fuentes consultadas',
      sourcesDescription: 'Esta respuesta fue generada basándose en {count} fragmentos del corpus presidencial',
      source: 'Fuente',
      noAnswer: 'No se pudo generar una respuesta',
      noAnswerText: 'Intenta reformular tu pregunta o ser más específico',
      analyzing: 'Analizando corpus y generando respuesta...',
      relevance: 'relevancia',
      errorPlaceholder: 'Por favor ingresa una pregunta'
    },
    
    // Narrative Evolution Page
    narrative: {
      title: 'Evolución Narrativa',
      subtitle: 'Analiza cómo cambia el significado de conceptos políticos a través del tiempo',
      backToHome: 'Volver al inicio',
      conceptLabel: 'Concepto a analizar',
      conceptPlaceholder: 'ej: seguridad pública, educación, salud',
      conceptHelp: 'Ingresa un concepto político o tema de interés público',
      conceptLanguageNotice: '⚠️ Nota: Por el momento, el análisis solo funciona con conceptos en español. Estamos trabajando para soportar inglés próximamente.',
      granularity: 'Granularidad temporal',
      dateRange: 'Rango de Fechas',
      startDate: 'Fecha Inicial:',
      endDate: 'Fecha Final:',
      analyzing: 'Analizando...',
      analyzeButton: 'Analizar Evolución',
      tip: 'Consejo: Si el análisis tarda demasiado, intenta:',
      tips: [
        'Reducir el rango de fechas (ej: 3-6 meses)',
        'Usar conceptos más específicos',
        'Cambiar granularidad a "Mensual"'
      ],
      analyzingEvolution: 'Analizando evolución semántica...',
      generatingExplanation: 'Generando explicación con IA...',
      noData: 'No se encontraron datos suficientes para este concepto. Intenta con otro término o ajusta el umbral de similitud.',
      errorEmptyConcept: 'Por favor ingresa un concepto para analizar',
      errorNoData: 'No se encontraron datos suficientes para este concepto. Intenta con otro término o ajusta el umbral de similitud.',
      errorTimeout: 'La consulta tomó demasiado tiempo. Intenta: 1) Usar un umbral de similitud más alto (0.7-0.8), 2) Reducir el rango de fechas, o 3) Usar un concepto más específico.',
      errorServiceUnavailable: 'El servicio está temporalmente no disponible. Por favor intenta de nuevo en un momento.',
      errorFetchingData: 'Error al obtener los datos de evolución',
      errorExplanation: 'Error al generar la explicación',
      dateRangeError: 'La fecha final no puede ser anterior a la fecha inicial',
      granularityOptions: {
        day: 'Diario',
        week: 'Semanal',
        month: 'Mensual'
      },
      evidence: {
        title: 'Evidencia Textual',
        description: 'Fragmentos de discursos que ejemplifican el uso del concepto en cada período',
        before: 'Antes',
        after: 'Después',
        disclaimer: 'Esta evidencia ha sido seleccionada automáticamente por su alta similitud semántica con el concepto analizado.',
        noData: 'No hay suficiente evidencia textual para comparar'
      },
      changeExplanation: {
        title: 'Cambio Narrativo Detectado',
        from: 'De',
        to: 'A',
        semanticChange: 'Cambio semántico',
        changeLow: 'bajo',
        changeMedium: 'moderado',
        changeHigh: 'significativo',
        conceptFraming: 'Encuadre del Concepto',
        firstPeriod: 'Primer Período',
        secondPeriod: 'Segundo Período',
        gainedProminence: 'Conceptos que Ganaron Prominencia',
        lostProminence: 'Conceptos que Perdieron Prominencia',
        overallAnalysis: 'Análisis del Cambio General',
        aiInterpretation: 'Interpretación de IA',
        speakerAnalysis: 'Análisis por Orador',
        speakerDescription: 'Oradores con mayor cambio en su discurso sobre este concepto:'
      },
      chart: {
        title: 'Evolución Semántica',
        noData: 'No hay datos suficientes para mostrar la evolución',
        yAxisLabel: 'Cambio Semántico',
        xAxisLabel: 'Período',
        hint: '📊 Haz clic en cualquier punto del gráfico o en el botón "Explicar" para ver la explicación del cambio semántico',
        legendLow: 'Cambio bajo (< 0.1)',
        legendMedium: 'Cambio medio (0.1 - 0.3)',
        legendHigh: 'Cambio alto (> 0.3)',
        tableTitle: 'Cambios Semánticos',
        tablePeriod: 'Período',
        tableChange: 'Cambio Semántico',
        tableAction: 'Acción',
        explainButton: 'Explicar',
        loadingButton: 'Cargando...',
        tooltipFrom: 'De',
        tooltipTo: 'A',
        tooltipChange: 'Cambio'
      }
    },
    
    // Error messages
    errors: {
      generic: 'Error al procesar la solicitud',
      timeout: 'La consulta tomó demasiado tiempo. Intenta: 1) Usar un umbral de similitud más alto (0.7-0.8), 2) Reducir el rango de fechas, o 3) Usar un concepto más específico.',
      unavailable: 'El servicio está temporalmente no disponible. Por favor intenta de nuevo en un momento.',
      network: 'Error de red. Verifica tu conexión.'
    }
  },
  
  en: {
    // Navigation & Common
    language: 'Language',
    spanish: 'Español',
    english: 'English',
    
    // Landing Page
    tagline: 'AI-Powered Political Discourse Analysis and Query Platform',
    hero: {
      description: 'VozPública is an advanced computational platform for political discourse analysis that employs artificial intelligence and natural language processing to extract insights from official communications of the Mexican Presidency.',
      dataSource: 'Data source:',
      dataSourceText: 'Official presidential speeches, press conferences, interviews, and communiqués from',
      coverage: 'Coverage:',
      coverageText: 'October 2024 onwards (Claudia Sheinbaum Administration)'
    },
    
    // Services
    services: {
      title: 'Available AI Services',
      search: {
        icon: '🔍',
        title: 'Semantic Search',
        description: 'Find presidential discourse fragments by meaning, not just word matching.',
        cta: 'Explore Search'
      },
      qa: {
        icon: '💬',
        title: 'Question & Answer (LLM)',
        description: 'Ask questions in natural language about speech content. AI-generated answers based on the presidential corpus.',
        cta: 'Ask Questions'
      },
      narrative: {
        icon: '📊',
        title: 'Narrative Evolution',
        description: 'Analyze how specific political concepts change their semantic meaning over time. Detect conceptual drift and context shifts.',
        cta: 'View Evolution'
      },
      topics: {
        icon: '🎯',
        title: 'Automatic Topic Discovery',
        description: 'Unsupervised identification of dominant themes in presidential discourse using semantic clustering and topic modeling.',
        comingSoon: 'Coming Soon'
      }
    },
    
    // Value Proposition
    valueProposition: {
      title: 'Who is VozPública for?',
      analysts: {
        title: 'For Political Analysts',
        description: 'Identify changes in government priorities, narrative evolution, and discourse patterns with quantitative precision.'
      },
      journalists: {
        title: 'For Journalists & Researchers',
        description: 'Search for specific statements, verify historical contexts, and find contradictions or consistencies in official discourse.'
      },
      citizens: {
        title: 'For Informed Citizens',
        description: 'Access data-driven analysis of how the government communicates its policies and understand the evolution of public discourse.'
      },
      academics: {
        title: 'For Academics',
        description: 'Use advanced semantic analysis tools for research in political science, communication, and computational linguistics.'
      }
    },
    
    // How it Works
    howItWorks: {
      title: 'Architecture and Analysis Flow',
      intro: 'VozPública is designed as a modular semantic analysis platform, capable of processing large volumes of political discourse and converting them into queryable and interpretable information.',
      steps: {
        ingestion: {
          title: 'Automated Data Ingestion:',
          description: 'Continuous extraction of official transcripts from gob.mx/presidencia, including speeches, press conferences, interviews, and communiqués. Data is updated periodically to maintain a current knowledge base.'
        },
        processing: {
          title: 'Processing and Structuring:',
          description: 'Text cleaning, segmentation into discourse units, and enrichment with structured metadata (date, event type, speaker, institutional context).'
        },
        semantic: {
          title: 'Semantic Representation:',
          description: 'Conversion of each discourse fragment into vector representations using pre-trained language models (sentence transformers), capturing meaning and context beyond keywords.'
        },
        storage: {
          title: 'Storage and Vector Indexing:',
          description: 'Persistence in a vector database with HNSW indexes, optimized for large-scale semantic similarity queries.'
        },
        analysis: {
          title: 'Analysis and Query Services:',
          description: 'Exposure of analytical capabilities through APIs: semantic search, questions and answers with RAG, and narrative evolution analysis through semantic time series.'
        }
      }
    },
    
    // Project Context
    projectContext: {
      title: 'Project Context',
      description: 'VozPública is an independent research and development project. It is part of a professional portfolio focused on:',
      focus: [
        'Architecture of large-scale data analysis systems',
        'Implementation of ML/NLP pipelines in production',
        'Design of interfaces for complex data exploration',
        'Application of AI to social science and political analysis problems'
      ],
      disclaimer: 'Note: This is a non-partisan, non-profit project. The goal is to demonstrate advanced technological applications for public discourse analysis.'
    },
    
    // Contact
    contact: {
      title: 'Contact',
      intro: 'If you are interested in the project, its technical approach, or potential collaborations, feel free to contact me:',
      role: 'Data Engineer & AI Developer'
    },
    
    // Footer
    footer: 'VozPública - Political Discourse Analysis Platform | Independent Research Project',
    
    // Search Page
    search: {
      title: 'Semantic Search',
      description: 'Search the presidential speech corpus using natural language. The system finds relevant fragments based on meaning, not just exact word matches.',
      placeholder: 'Example: What has the president said about public security?',
      button: 'Search',
      searching: 'Searching...',
      tip: 'Tip: Use complete questions or specific concepts for better results',
      results: 'Results',
      resultsCount: 'fragments found',
      noResults: 'No results found',
      noResultsText: 'Try rephrasing your query or using different terms',
      analyzing: 'Analyzing presidential corpus...',
      relevance: 'relevance',
      viewSource: 'View original source',
      errorPlaceholder: 'Please enter a query'
    },
    
    // Q&A Page
    qa: {
      title: 'Question & Answer',
      description: 'Ask questions in natural language about presidential discourse. The system uses AI to generate answers based on the official corpus, providing context and relevant sources.',
      placeholder: 'Example: What is the government\'s position on energy reform?',
      button: 'Ask',
      processing: 'Processing...',
      tip: 'Tip: Ask specific questions about policies, statements, or concrete topics',
      answer: 'Answer',
      sources: 'Consulted Sources',
      sourcesDescription: 'This answer was generated based on {count} fragments from the presidential corpus',
      source: 'Source',
      noAnswer: 'Could not generate an answer',
      noAnswerText: 'Try rephrasing your question or being more specific',
      analyzing: 'Analyzing corpus and generating answer...',
      relevance: 'relevance',
      errorPlaceholder: 'Please enter a question'
    },
    
    // Narrative Evolution Page
    narrative: {
      title: 'Narrative Evolution',
      subtitle: 'Analyze how the meaning of political concepts changes over time',
      backToHome: 'Back to Home',
      conceptLabel: 'Concept to analyze',
      conceptPlaceholder: 'e.g.: public security, education, health',
      conceptHelp: 'Enter a political concept or topic of public interest',
      conceptLanguageNotice: '⚠️ Note: Currently, analysis only works with concepts in Spanish. We are working on English support coming soon.',
      granularity: 'Time Granularity',
      dateRange: 'Date Range',
      startDate: 'Start Date:',
      endDate: 'End Date:',
      analyzing: 'Analyzing...',
      analyzeButton: 'Analyze Evolution',
      tip: 'Tip: If analysis takes too long, try:',
      tips: [
        'Reduce date range (e.g.: 3-6 months)',
        'Use more specific concepts',
        'Change granularity to "Monthly"'
      ],
      analyzingEvolution: 'Analyzing semantic evolution...',
      generatingExplanation: 'Generating AI explanation...',
      noData: 'Not enough data found for this concept. Try another term or adjust the similarity threshold.',
      errorEmptyConcept: 'Please enter a concept to analyze',
      errorNoData: 'Not enough data found for this concept. Try another term or adjust the similarity threshold.',
      errorTimeout: 'The query took too long. Try: 1) Using a higher similarity threshold (0.7-0.8), 2) Reducing the date range, or 3) Using a more specific concept.',
      errorServiceUnavailable: 'The service is temporarily unavailable. Please try again in a moment.',
      errorFetchingData: 'Error fetching evolution data',
      errorExplanation: 'Error generating explanation',
      dateRangeError: 'End date cannot be earlier than start date',
      granularityOptions: {
        day: 'Daily',
        week: 'Weekly',
        month: 'Monthly'
      },
      evidence: {
        title: 'Textual Evidence',
        description: 'Speech fragments that exemplify the use of the concept in each period',
        before: 'Before',
        after: 'After',
        disclaimer: 'This evidence was automatically selected based on high semantic similarity with the analyzed concept.',
        noData: 'Insufficient textual evidence for comparison'
      },
      changeExplanation: {
        title: 'Detected Narrative Change',
        from: 'From',
        to: 'To',
        semanticChange: 'Semantic change',
        changeLow: 'low',
        changeMedium: 'moderate',
        changeHigh: 'significant',
        conceptFraming: 'Concept Framing',
        firstPeriod: 'First Period',
        secondPeriod: 'Second Period',
        gainedProminence: 'Concepts that Gained Prominence',
        lostProminence: 'Concepts that Lost Prominence',
        overallAnalysis: 'Overall Change Analysis',
        aiInterpretation: 'AI Interpretation',
        speakerAnalysis: 'Speaker Analysis',
        speakerDescription: 'Speakers with the most change in their discourse on this concept:'
      },
      chart: {
        title: 'Semantic Evolution',
        noData: 'Insufficient data to show evolution',
        yAxisLabel: 'Semantic Change',
        xAxisLabel: 'Period',
        hint: '📊 Click any point on the chart or the "Explain" button to see the semantic change explanation',
        legendLow: 'Low change (< 0.1)',
        legendMedium: 'Medium change (0.1 - 0.3)',
        legendHigh: 'High change (> 0.3)',
        tableTitle: 'Semantic Changes',
        tablePeriod: 'Period',
        tableChange: 'Semantic Change',
        tableAction: 'Action',
        explainButton: 'Explain',
        loadingButton: 'Loading...',
        tooltipFrom: 'From',
        tooltipTo: 'To',
        tooltipChange: 'Change'
      }
    },
    
    // Error messages
    errors: {
      generic: 'Error processing request',
      timeout: 'Query took too long. Try: 1) Use a higher similarity threshold (0.7-0.8), 2) Reduce date range, or 3) Use a more specific concept.',
      unavailable: 'Service temporarily unavailable. Please try again in a moment.',
      network: 'Network error. Check your connection.'
    }
  }
};

/**
 * Get translation by key path (e.g., 'services.search.title')
 */
export function getTranslation(lang, keyPath) {
  const keys = keyPath.split('.');
  let value = translations[lang];
  
  for (const key of keys) {
    if (value && typeof value === 'object') {
      value = value[key];
    } else {
      return keyPath; // Return key if translation not found
    }
  }
  
  return value || keyPath;
}

/**
 * Replace placeholders in translations (e.g., {count})
 */
export function formatTranslation(text, params = {}) {
  let result = text;
  Object.keys(params).forEach(key => {
    result = result.replace(`{${key}}`, params[key]);
  });
  return result;
}
