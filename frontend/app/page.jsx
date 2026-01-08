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
          {/* <h2>Análisis Profesional del Discurso Presidencial Mexicano</h2> */}
          <p>
            VozPública es una plataforma avanzada de análisis computacional del discurso político que emplea 
            inteligencia artificial y procesamiento de lenguaje natural para extraer insights de las 
            comunicaciones oficiales de la Presidencia de México.
          </p>

        </section>

        {/* AI Services */}
        <section className="services">
          <h2>Servicios de IA Disponibles</h2>
          <div className="services-grid">
            <div className="service-card active">
              <h3>🔍 Búsqueda Semántica</h3>
              <p>
Encuentra fragmentos del discurso presidencial por significado, no solo por coincidencia de palabras.              </p>
              <Link href="/search" className="cta-button">
                Explorar Búsqueda
              </Link>
            </div>
            <div className="service-card active">
              <h3>💬 Pregunta y Respuesta (LLM)</h3>
              <p>
                Formula preguntas en lenguaje natural sobre el contenido de los discursos.<br />
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
            <p className="data-source">
            <strong>Fuente de datos:</strong> Discursos presidenciales oficiales, conferencias de prensa, 
            entrevistas y comunicados de <a href="https://www.gob.mx/presidencia" target="_blank" rel="noopener noreferrer">gob.mx/presidencia</a>
            <br />
            <strong>Cobertura:</strong> Octubre 2024 en adelante (Administración Claudia Sheinbaum)
          </p>
        </section>

        {/* Value Proposition */}
        <section className="value-proposition">
          <h2>¿Para quién es VozPública?</h2>
          <div className="value-grid">
            <div className="value-item">
              <div className="value-icon">📊</div>
              <h3>Para Analistas Políticos</h3>
              <p>
                Identifica cambios en prioridades gubernamentales, evolución de narrativas y patrones 
                discursivos con precisión cuantitativa.
              </p>
            </div>
            <div className="value-item">
              <div className="value-icon">📰</div>
              <h3>Para Periodistas e Investigadores</h3>
              <p>
                Busca declaraciones específicas, verifica contextos históricos y encuentra contradicciones 
                o consistencias en el discurso oficial.
              </p>
            </div>
            <div className="value-item">
              <div className="value-icon">👥</div>
              <h3>Para Ciudadanos Informados</h3>
              <p>
                Accede a análisis basados en datos sobre cómo el gobierno comunica sus políticas y 
                comprende la evolución del discurso público.
              </p>
            </div>
            <div className="value-item">
              <div className="value-icon">🎓</div>
              <h3>Para Académicos</h3>
              <p>
                Utiliza herramientas de análisis semántico avanzado para investigación en ciencias 
                políticas, comunicación y lingüística computacional.
              </p>
            </div>
          </div>
        </section>

        {/* How it Works */}
        <section className="how-it-works">
          <h2>Arquitectura y flujo de análisis</h2>

          <p className="section-intro">
            VozPública está diseñada como una plataforma modular de análisis semántico,
            capaz de procesar grandes volúmenes de discurso político y convertirlos en
            información consultable e interpretable.
          </p>

          <ol className="pipeline">
            <li>
              <strong>Ingesta automatizada de datos:</strong>
              Extracción continua de transcripciones oficiales desde gob.mx/presidencia,
              incluyendo discursos, conferencias de prensa, entrevistas y comunicados.
              Los datos se actualizan de forma periódica para mantener la base de conocimiento vigente.
            </li>

            <li>
              <strong>Procesamiento y estructuración:</strong>
              Limpieza del texto, segmentación en unidades discursivas y enriquecimiento con
              metadatos estructurados (fecha, tipo de evento, orador, contexto institucional).
            </li>

            <li>
              <strong>Representación semántica:</strong>
              Conversión de cada fragmento discursivo en representaciones vectoriales
              mediante modelos de lenguaje preentrenados (sentence transformers),
              capturando significado y contexto más allá de palabras clave.
            </li>

            <li>
              <strong>Almacenamiento e indexación vectorial:</strong>
              Persistencia en una base de datos vectorial con índices HNSW,
              optimizada para consultas de similitud semántica a gran escala.
            </li>

            <li>
              <strong>Servicios de Análisis y Consulta:</strong> 
              Exposición de capacidades analíticas mediante APIs: búsqueda semántica, preguntas y respuestas 
              con RAG, y análisis de evolución narrativa a través de series temporales semánticas.
            </li>

          </ol>
          </section>


        {/* Project Context */}
        <section className="project-context">
          <h2>Contexto del Proyecto</h2>
          <p>
            VozPública es un <strong>proyecto independiente de investigación y desarrollo.</strong> Forma parte de un portafolio profesional enfocado en:
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

        {/* Contact Information */}
        <section className="contact">
          <h2>Contacto</h2>
          <p className="contact-intro">
            Si te interesa el proyecto, su enfoque técnico o posibles colaboraciones,
            no dudes en contactarme:
          </p>

          <div className="contact-card">
            <div className="contact-header">
              <div className="avatar">DM</div>
              <h3>Diego Mancera</h3>
              <p className="role">Data Scientist (Applied ML / AI Systems)</p>
            </div>
            
            <div className="contact-links">
              <a href="mailto:dcmancera17@outlook.com" className="contact-link email" target="_blank" rel="noopener noreferrer">
                <span className="icon">✉️</span>
                <span className="link-text">dcmancera17@outlook.com</span>
              </a>
              <a href="https://linkedin.com/in/dcmancera17" className="contact-link linkedin" target="_blank" rel="noopener noreferrer">
                <span className="icon">💼</span>
                <span className="link-text">linkedin.com/in/dcmancera17</span>
              </a>
              <a href="https://github.com/Perruchok" className="contact-link github" target="_blank" rel="noopener noreferrer">
                <span className="icon">💻</span>
                <span className="link-text">github.com/Perruchok</span>
              </a>
            </div>
          </div>
        </section>


      </main>


      <footer>
        <p>VozPública - Plataforma de Análisis de Discurso Político | Proyecto de Investigación Independiente</p>
      </footer>
    </div>
  );
}
