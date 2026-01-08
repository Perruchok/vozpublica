'use client';

import { useState } from 'react';
import { searchSemanticDocuments } from '@/lib/api';
import { useLanguage } from '@/lib/languageContext';
import LanguageToggle from '@/components/common/LanguageToggle';
import Link from 'next/link';

export default function SearchPage() {
  const { t, tf, language } = useLanguage();
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!query.trim()) {
      setError(t('search.errorPlaceholder'));
      return;
    }

    setIsLoading(true);
    setError(null);
    setHasSearched(true);

    try {
      const data = await searchSemanticDocuments(query, 10);
      setResults(data.results || []);
    } catch (err) {
      setError(err.message || 'Error al realizar la búsqueda');
      setResults([]);
    } finally {
      setIsLoading(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Fecha no disponible';
    try {
      const date = new Date(dateString);
      const locale = language === 'en' ? 'en-US' : 'es-MX';
      return date.toLocaleDateString(locale, { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
      });
    } catch {
      return dateString;
    }
  };

  const formatSimilarity = (similarity) => {
    if (!similarity) return '';
    return (similarity * 100).toFixed(1) + '%';
  };

  return (
    <div className="search-page">
      <div className="search-container">
        <header className="search-header">
          <div className="search-header-top">
            <h1>🔍 {t('search.title')}</h1>
            <LanguageToggle />
          </div>
          <p className="search-description">{t('search.description')}</p>
          <Link href="/" className="back-link">← Volver al inicio</Link>
        </header>

        <form onSubmit={handleSubmit} className="search-form">
          <div className="search-input-group">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={t('search.placeholder')}
              className="search-input"
              disabled={isLoading}
            />
            <button 
              type="submit" 
              className="search-button"
              disabled={isLoading || !query.trim()}
            >
              {isLoading ? t('search.searching') : t('search.button')}
            </button>
          </div>
          
          <p className="search-hint">💡 {t('search.tip')}</p>
        </form>

        {error && (
          <div className="search-error">
            <span className="error-icon">⚠️</span>
            <span>{error}</span>
          </div>
        )}

        {isLoading && (
          <div className="search-loading">
            <div className="loading-spinner"></div>
            <p>{t('search.analyzing')}</p>
          </div>
        )}

        {!isLoading && hasSearched && results.length === 0 && !error && (
          <div className="no-results">
            <span className="no-results-icon">🔍</span>
            <h3>{t('search.noResults')}</h3>
            <p>{t('search.noResultsText')}</p>
          </div>
        )}

        {!isLoading && results.length > 0 && (
          <div className="search-results">
            <div className="results-header">
              <h2>{t('search.results')}</h2>
              <span className="results-count">{results.length} {t('search.resultsCount')}</span>
            </div>

            <div className="results-list">
              {results.map((result, index) => (
                <div key={result.doc_id + '-' + index} className="result-card">
                  <div className="result-header">
                    <div className="result-meta">
                      {result.similarity && (
                        <span className="similarity-badge">
                          {formatSimilarity(result.similarity)} {t('search.relevance')}
                        </span>
                      )}
                      {result.speaker_normalized && (
                        <span className="speaker-badge">
                          👤 {result.speaker_normalized}
                        </span>
                      )}
                    </div>
                  </div>

                  <div className="result-text">
                    {result.text}
                  </div>

                  <div className="result-footer">
                    {result.title && (
                      <div className="result-title">
                        📄 {result.title}
                      </div>
                    )}
                    {result.href && (
                      <a 
                        href={result.href} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="result-link"
                      >
                        {t('search.viewSource')} →
                      </a>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
