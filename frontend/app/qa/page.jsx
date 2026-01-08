'use client';

import { useState } from 'react';
import { askQuestion } from '@/lib/api';
import { useLanguage } from '@/lib/languageContext';
import LanguageToggle from '@/components/common/LanguageToggle';
import Link from 'next/link';

export default function QAPage() {
  const { t, tf } = useLanguage();
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState(null);
  const [sources, setSources] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [hasAsked, setHasAsked] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!question.trim()) {
      setError(t('qa.errorPlaceholder'));
      return;
    }

    setIsLoading(true);
    setError(null);
    setHasAsked(true);

    try {
      const data = await askQuestion(question, 5);
      setAnswer(data.answer || '');
      setSources(data.sources || []);
    } catch (err) {
      setError(err.message || 'Error al procesar la pregunta');
      setAnswer(null);
      setSources([]);
    } finally {
      setIsLoading(false);
    }
  };

  // Convert markdown links to HTML
  const renderAnswerWithLinks = (text) => {
    if (!text) return '';
    
    // Replace markdown links [text](url) with HTML links
    const htmlText = text.replace(
      /\[([^\]]+)\]\(([^)]+)\)/g,
      '<a href="$2" target="_blank" rel="noopener noreferrer" class="answer-link">$1</a>'
    );
    
    return <div dangerouslySetInnerHTML={{ __html: htmlText }} />;
  };

  return (
    <div className="qa-page">
      <div className="qa-container">
        <header className="qa-header">
          <div className="qa-header-top">
            <h1>💬 {t('qa.title')}</h1>
            <LanguageToggle />
          </div>
          <p className="qa-description">{t('qa.description')}</p>
          <Link href="/" className="back-link">← Volver al inicio</Link>
        </header>

        <form onSubmit={handleSubmit} className="qa-form">
          <div className="qa-input-group">
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder={t('qa.placeholder')}
              className="qa-textarea"
              disabled={isLoading}
              rows={4}
            />
          </div>
          
          <button 
            type="submit" 
            className="qa-button"
            disabled={isLoading || !question.trim()}
          >
            {isLoading ? t('qa.processing') : t('qa.button')}
          </button>
          
          <p className="qa-hint">💡 {t('qa.tip')}</p>
        </form>

        {error && (
          <div className="qa-error">
            <span className="error-icon">⚠️</span>
            <span>{error}</span>
          </div>
        )}

        {isLoading && (
          <div className="qa-loading">
            <div className="loading-spinner"></div>
            <p>{t('qa.analyzing')}</p>
          </div>
        )}

        {!isLoading && hasAsked && !answer && !error && (
          <div className="no-answer">
            <span className="no-answer-icon">🤔</span>
            <h3>{t('qa.noAnswer')}</h3>
            <p>{t('qa.noAnswerText')}</p>
          </div>
        )}

        {!isLoading && answer && (
          <div className="qa-results">
            <div className="answer-section">
              <h2>{t('qa.answer')}</h2>
              <div className="answer-content">
                {renderAnswerWithLinks(answer)}
              </div>
            </div>

            {sources && sources.length > 0 && (
              <div className="sources-section">
                <h3>{t('qa.sources')}</h3>
                <p className="sources-description">
                  {t('qa.sourcesDescription').replace('{count}', sources.length)}
                </p>
                <div className="sources-list">
                  {sources.map((source, index) => (
                    <div key={source.doc_id + '-' + index} className="source-item">
                      <div className="source-badge">
                        {t('qa.source')} {index + 1}
                      </div>
                      <div className="source-details">
                        {source.href ? (
                          <a 
                            href={source.href} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="source-link"
                          >
                            {source.title || `Doc ID: ${source.doc_id}`}
                          </a>
                        ) : (
                          <span className="source-id">
                            {source.title || `Doc ID: ${source.doc_id}`}
                          </span>
                        )}
                        {source.similarity && (
                          <span className="source-similarity">
                            {(source.similarity * 100).toFixed(1)}% {t('qa.relevance')}
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
