import Link from 'next/link';

export default function Home() {
  return (
    <div className="landing-page">
      <header>
        <h1>VozPública</h1>
          <p className="tagline">Plataforma de Análisis y Consulta de Discurso Político con IA</p>
      </header>

      <main>
        {/* Hero Section */}
        <section className="hero">
          <h2>Análisis Profesional del Discurso Presidencial Mexicano</h2>
          <p>
            VozPública es una plataforma avanzada de análisis computacional del discurso político que emplea 
            inteligencia artificial y procesamiento de lenguaje natural para extraer insights de las 
            comunicaciones oficiales de la Presidencia de México.
          </p>
          <p className="data-source">
            <strong>Fuente de datos:</strong> Discursos presidenciales oficiales, conferencias de prensa, 
            entrevistas y comunicados de <a href="https://www.gob.mx/presidencia" target="_blank" rel="noopener noreferrer">gob.mx/presidencia</a>
            <br />
            <strong>Cobertura:</strong> Octubre 2024 en adelante (Administración Claudia Sheinbaum)
          </p>
        </section>

        {/* Value Proposition */}
        <section className="value-proposition">
          <h2>¿Por qué es relevante?</h2>
          <div className="value-grid">
            <div className="value-item">
              <h3>Para Analistas Políticos</h3>
              <p>
                Identifica cambios en prioridades gubernamentales, evolución de narrativas y patrones 
                discursivos con precisión cuantitativa.
              </p>
            </div>
            <div className="value-item">
              <h3>Para Periodistas e Investigadores</h3>
              <p>
                Busca declaraciones específicas, verifica contextos históricos y encuentra contradicciones 
                o consistencias en el discurso oficial.
              </p>
            </div>
            <div className="value-item">
              <h3>Para Ciudadanos Informados</h3>
              <p>
                Accede a análisis basados en datos sobre cómo el gobierno comunica sus políticas y 
                comprende la evolución del discurso público.
              </p>
            </div>
            <div className="value-item">
              <h3>Para Académicos</h3>
              <p>
                Utiliza herramientas de análisis semántico avanzado para investigación en ciencias 
                políticas, comunicación y lingüística computacional.
              </p>
            </div>
          </div>
        </section>

        {/* AI Services */}
        <section className="services">
          <h2>Servicios de IA Disponibles</h2>
          <div className="services-grid">
            <div className="service-card active">
              <h3>🔍 Búsqueda Semántica</h3>
              <p>
                Encuentra fragmentos de discursos por significado, no solo por palabras clave. 
                Utiliza embeddings vectoriales para búsqueda por similitud conceptual.
              </p>
              <Link href="/search" className="cta-button">
                Explorar Búsqueda
              </Link>
            </div>

            <div className="service-card active">
              <h3>💬 Pregunta y Respuesta (LLM)</h3>
              <p>
                Formula preguntas en lenguaje natural sobre el contenido de los discursos. 
                Respuestas generadas por IA basadas en el corpus presidencial.
              </p>
              <Link href="/qa" className="cta-button">
                Hacer Preguntas
              </Link>
            </div>

            <div className="service-card active">
              <h3>📊 Evolución Narrativa</h3>
              <p>
                Analiza cómo conceptos políticos específicos cambian su significado semántico 
                a través del tiempo. Detecta drift conceptual y cambios de contexto.
              </p>
              <Link href="/narrative" className="cta-button">
                Ver Evolución
              </Link>
            </div>

            <div className="service-card upcoming">
              <h3>🎯 Descubrimiento Automático de Tópicos</h3>
              <p>
                Identificación no supervisada de temas dominantes en el discurso presidencial 
                usando clustering semántico y modelado de tópicos.
              </p>
              <span className="coming-soon">Próximamente</span>
            </div>
          </div>
        </section>

        {/* How it Works */}
        <section className="how-it-works">
          <h2>¿Cómo funciona?</h2>
          <p className="intro">Pipeline de procesamiento de datos y análisis:</p>
          <ol className="pipeline">
            <li>
              <strong>Extracción de Datos:</strong> Scraping automatizado de transcripciones oficiales 
              desde gob.mx/presidencia. Recopilación diaria de discursos, conferencias de prensa y comunicados.
            </li>
            <li>
              <strong>Preprocesamiento:</strong> Limpieza de texto, segmentación en unidades discursivas 
              (speech turns), normalización y estructuración de metadatos (fecha, tipo de evento, orador).
            </li>
            <li>
              <strong>Vectorización Semántica:</strong> Generación de embeddings usando modelos de lenguaje 
              pre-entrenados (sentence transformers). Cada fragmento de discurso se representa como un vector 
              en espacio semántico de alta dimensionalidad.
            </li>
            <li>
              <strong>Indexación Vectorial:</strong> Almacenamiento en base de datos vectorial con índices 
              HNSW (Hierarchical Navigable Small World) para búsqueda eficiente por similitud.
            </li>
            <li>
              <strong>Análisis y Consulta:</strong> APIs de búsqueda semántica, Q&A con RAG (Retrieval-Augmented 
              Generation), y análisis de drift temporal usando técnicas de series de tiempo sobre representaciones vectoriales.
            </li>
            <li>
              <strong>Interpretación con LLM:</strong> Generación de explicaciones en lenguaje natural de 
              patrones detectados usando modelos de lenguaje grandes para síntesis y contextualización.
            </li>
          </ol>
        </section>

        {/* Project Context */}
        <section className="project-context">
          <h2>Contexto del Proyecto</h2>
          <p>
            VozPública es un <strong>proyecto independiente de investigación y desarrollo</strong> creado 
            como demostración de capacidades técnicas en ingeniería de datos, NLP y sistemas de IA aplicados 
            a análisis político.
          </p>
          <p>
            Este proyecto forma parte de un portafolio profesional enfocado en:
          </p>
          <ul>
            <li>Arquitectura de sistemas de análisis de datos a gran escala</li>
            <li>Implementación de pipelines de ML/NLP en producción</li>
            <li>Diseño de interfaces para exploración de datos complejos</li>
            <li>Aplicación de IA a problemas de ciencias sociales y análisis político</li>
          </ul>
          <p className="disclaimer">
            <em>Nota: Este es un proyecto no partidista y sin fines de lucro. El objetivo es demostrar 
            aplicaciones tecnológicas avanzadas para análisis de discurso público.</em>
          </p>
        </section>
      </main>

      <footer>
        <p>VozPública - Plataforma de Análisis de Discurso Político | Proyecto de Investigación Independiente</p>
      </footer>
    </div>
  );
}
