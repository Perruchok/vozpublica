"use client";

import { useLanguage } from '@/lib/languageContext';

export default function EvidenceComparison({ before, after }) {
  const { t, language } = useLanguage();
  
  if (!before || !after || before.length === 0 || after.length === 0) {
    return (
      <div className="evidence-comparison empty">
        <p>{t('narrative.evidence.noData')}</p>
      </div>
    );
  }

  const formatDate = (date) => {
    if (!date) return "";
    const locale = language === 'en' ? 'en-US' : 'es-MX';
    return new Date(date).toLocaleDateString(locale, {
      day: 'numeric',
      month: 'short',
      year: 'numeric'
    });
  };

  const EvidenceCard = ({ item }) => (
    <div className="evidence-card">
      <div className="evidence-meta">
        <span className="speaker">{item.speaker}</span>
        <span className="date">{formatDate(item.date)}</span>
        {item.similarity && (
          <span className="similarity" title="Similitud con el concepto">
            {(item.similarity * 100).toFixed(0)}%
          </span>
        )}
      </div>
      <p className="evidence-text">"{item.text}"</p>
    </div>
  );

  return (
    <div className="evidence-comparison">
      <h3>📝 {t('narrative.evidence.title')}</h3>
      <p className="section-description">
        {t('narrative.evidence.description')}
      </p>
      
      <div className="evidence-grid">
        <div className="evidence-column">
          <h4 className="column-header before">{t('narrative.evidence.before')}</h4>
          <div className="evidence-list">
            {before.map((item, idx) => (
              <EvidenceCard key={idx} item={item} />
            ))}
          </div>
        </div>

        <div className="evidence-divider">
          <div className="divider-line"></div>
          <span className="divider-icon">→</span>
        </div>

        <div className="evidence-column">
          <h4 className="column-header after">{t('narrative.evidence.after')}</h4>
          <div className="evidence-list">
            {after.map((item, idx) => (
              <EvidenceCard key={idx} item={item} />
            ))}
          </div>
        </div>
      </div>

      <div className="evidence-footer">
        <p className="disclaimer">
          💡 {t('narrative.evidence.disclaimer')}
        </p>
      </div>
    </div>
  );
}
