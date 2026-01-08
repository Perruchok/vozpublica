'use client';

import Link from 'next/link';
import { useLanguage } from '@/lib/languageContext';
import LanguageToggle from '@/components/common/LanguageToggle';

export default function Home() {
  const { t, tf, translations } = useLanguage();

  return (
    <div className="landing-page">
      <header>
        <div className="header-content">
          <h1>VozPública</h1>
          <p className="tagline">{t('tagline')}</p>
        </div>
        <LanguageToggle />
      </header>

      <main>
        {/* Hero Section */}
        <section className="hero">
          <p>{t('hero.description')}</p>
        </section>

        {/* AI Services */}
        <section className="services">
          <h2>{t('services.title')}</h2>
          <div className="services-grid">
            <div className="service-card active">
              <h3>🔍 {t('services.search.title')}</h3>
              <p>{t('services.search.description')}</p>
              <Link href="/search" className="cta-button">
                {t('services.search.cta')}
              </Link>
            </div>
            <div className="service-card active">
              <h3>💬 {t('services.qa.title')}</h3>
              <p>{t('services.qa.description')}</p>
              <Link href="/qa" className="cta-button">
                {t('services.qa.cta')}
              </Link>
            </div>

            <div className="service-card active">
              <h3>📊 {t('services.narrative.title')}</h3>
              <p>{t('services.narrative.description')}</p>
              <Link href="/narrative" className="cta-button">
                {t('services.narrative.cta')}
              </Link>
            </div>

            <div className="service-card upcoming">
              <h3>🎯 {t('services.topics.title')}</h3>
              <p>{t('services.topics.description')}</p>
              <span className="coming-soon">{t('services.topics.comingSoon')}</span>
            </div>
          </div>
          <p className="data-source">
            <strong>{t('hero.dataSource')}</strong> {t('hero.dataSourceText')} <a href="https://www.gob.mx/presidencia" target="_blank" rel="noopener noreferrer">gob.mx/presidencia</a>
            <br />
            <strong>{t('hero.coverage')}</strong> {t('hero.coverageText')}
          </p>
        </section>

        {/* Value Proposition */}
        <section className="value-proposition">
          <h2>{t('valueProposition.title')}</h2>
          <div className="value-grid">
            <div className="value-item">
              <div className="value-icon">📊</div>
              <h3>{t('valueProposition.analysts.title')}</h3>
              <p>{t('valueProposition.analysts.description')}</p>
            </div>
            <div className="value-item">
              <div className="value-icon">📰</div>
              <h3>{t('valueProposition.journalists.title')}</h3>
              <p>{t('valueProposition.journalists.description')}</p>
            </div>
            <div className="value-item">
              <div className="value-icon">👥</div>
              <h3>{t('valueProposition.citizens.title')}</h3>
              <p>{t('valueProposition.citizens.description')}</p>
            </div>
            <div className="value-item">
              <div className="value-icon">🎓</div>
              <h3>{t('valueProposition.academics.title')}</h3>
              <p>{t('valueProposition.academics.description')}</p>
            </div>
          </div>
        </section>

        {/* How it Works */}
        <section className="how-it-works">
          <h2>{t('howItWorks.title')}</h2>
          <p className="section-intro">{t('howItWorks.intro')}</p>

          <ol className="pipeline">
            <li>
              <strong>{t('howItWorks.steps.ingestion.title')}</strong>
              {t('howItWorks.steps.ingestion.description')}
            </li>
            <li>
              <strong>{t('howItWorks.steps.processing.title')}</strong>
              {t('howItWorks.steps.processing.description')}
            </li>
            <li>
              <strong>{t('howItWorks.steps.semantic.title')}</strong>
              {t('howItWorks.steps.semantic.description')}
            </li>
            <li>
              <strong>{t('howItWorks.steps.storage.title')}</strong>
              {t('howItWorks.steps.storage.description')}
            </li>
            <li>
              <strong>{t('howItWorks.steps.analysis.title')}</strong> 
              {t('howItWorks.steps.analysis.description')}
            </li>
          </ol>
        </section>

        {/* Project Context */}
        <section className="project-context">
          <h2>{t('projectContext.title')}</h2>
          <p>{t('projectContext.description')}</p>
          <ul>
            {translations.projectContext.focus.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
          <p className="disclaimer">
            <em>{t('projectContext.disclaimer')}</em>
          </p>
        </section>

        {/* Contact Information */}
        <section className="contact">
          <h2>{t('contact.title')}</h2>
          <p className="contact-intro">{t('contact.intro')}</p>

          <div className="contact-card">
            <div className="contact-header">
              <div className="avatar">DM</div>
              <h3>Diego Mancera</h3>
              <p className="role">{t('contact.role')}</p>
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
        <p>{t('footer')}</p>
      </footer>
    </div>
  );
}
