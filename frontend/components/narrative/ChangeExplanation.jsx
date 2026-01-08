"use client";

import { useLanguage } from '@/lib/languageContext';
import EvidenceComparison from "./EvidenceComparison";

export default function ChangeExplanation({ data }) {
  const { t, language } = useLanguage();
  
  if (!data) return null;

  const formatDate = (date) => {
    if (!date) return "";
    const locale = language === 'en' ? 'en-US' : 'es-MX';
    return new Date(date).toLocaleDateString(locale, {
      year: 'numeric',
      month: 'long'
    });
  };

  const getChangeDescription = (change) => {
    if (change < 0.1) return t('narrative.changeExplanation.changeLow');
    if (change < 0.3) return t('narrative.changeExplanation.changeMedium');
    return t('narrative.changeExplanation.changeHigh');
  };

  // Handle both old and new response formats
  const hasNewFormat = data.response && typeof data.response === 'object';
  const response = hasNewFormat ? data.response : null;

  // Function to parse markdown links and convert them to <a> tags
  const parseMarkdownLinks = (text) => {
    if (!text) return null;
    
    // Regex to match markdown links: [text](url)
    const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
    const parts = [];
    let lastIndex = 0;
    let match;

    while ((match = linkRegex.exec(text)) !== null) {
      // Add text before the link
      if (match.index > lastIndex) {
        parts.push(text.substring(lastIndex, match.index));
      }
      
      // Add the link as a React element
      const linkText = match[1];
      const linkUrl = match[2];
      parts.push(
        <a 
          key={match.index}
          href={linkUrl} 
          target="_blank" 
          rel="noopener noreferrer"
          style={{
            color: '#1976d2',
            textDecoration: 'none',
            fontWeight: '500',
            borderBottom: '1px dotted #1976d2'
          }}
          onMouseOver={(e) => e.target.style.borderBottom = '1px solid #1976d2'}
          onMouseOut={(e) => e.target.style.borderBottom = '1px dotted #1976d2'}
        >
          {linkText}
        </a>
      );
      
      lastIndex = match.index + match[0].length;
    }
    
    // Add remaining text
    if (lastIndex < text.length) {
      parts.push(text.substring(lastIndex));
    }
    
    return parts.length > 0 ? parts : text;
  };

  return (
    <div className="change-explanation">
      <div className="explanation-header">
        <h2>{t('narrative.changeExplanation.title')}</h2>
        <div className="period-info">
          <span className="period-label">{t('narrative.changeExplanation.from')}:</span>
          <span className="period-value">{data.from_period || formatDate(data.from)}</span>
          <span className="arrow">→</span>
          <span className="period-label">{t('narrative.changeExplanation.to')}:</span>
          <span className="period-value">{data.to_period || formatDate(data.to)}</span>
        </div>
        <div className="change-metric">
          <span className="metric-label">{t('narrative.changeExplanation.semanticChange')}:</span>
          <span className="metric-value">
            {data.semantic_change.toFixed(3)}
          </span>
          <span className="metric-description">
            ({getChangeDescription(data.semantic_change)})
          </span>
        </div>
      </div>

      {/* New format response */}
      {hasNewFormat && response && (
        <>
          <div className="llm-explanation">
            <h3>🎭 {t('narrative.changeExplanation.conceptFraming')}</h3>
            <div className="framing-comparison" style={{ 
              display: 'grid', 
              gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
              gap: '20px',
              marginTop: '15px'
            }}>
              <div className="framing-period" style={{
                padding: '15px',
                border: '1px solid #e0e0e0',
                borderRadius: '8px',
                backgroundColor: '#f8f9fa'
              }}>
                <h4 style={{ marginTop: 0, color: '#1976d2' }}>{t('narrative.changeExplanation.firstPeriod')} ({data.from_period})</h4>
                <div className="explanation-content">
                  <p style={{ margin: 0, lineHeight: '1.6' }}>
                    {parseMarkdownLinks(response.core_framing?.first_period)}
                  </p>
                </div>
              </div>
              <div className="framing-period" style={{
                padding: '15px',
                border: '1px solid #e0e0e0',
                borderRadius: '8px',
                backgroundColor: '#f8f9fa'
              }}>
                <h4 style={{ marginTop: 0, color: '#1976d2' }}>{t('narrative.changeExplanation.secondPeriod')} ({data.to_period})</h4>
                <div className="explanation-content">
                  <p style={{ margin: 0, lineHeight: '1.6' }}>
                    {parseMarkdownLinks(response.core_framing?.second_period)}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {response.gained_prominence && response.gained_prominence.length > 0 && (
            <div className="prominence-section" style={{ marginTop: '20px' }}>
              <h3>📈 {t('narrative.changeExplanation.gainedProminence')}</h3>
              <ul className="prominence-list" style={{
                listStyle: 'none',
                padding: 0,
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
                gap: '10px'
              }}>
                {response.gained_prominence.map((item, idx) => (
                  <li key={idx} style={{
                    padding: '10px 15px',
                    backgroundColor: '#e8f5e9',
                    border: '1px solid #4caf50',
                    borderRadius: '6px',
                    color: '#2e7d32'
                  }}>{item}</li>
                ))}
              </ul>
            </div>
          )}

          {response.lost_prominence && response.lost_prominence.length > 0 && (
            <div className="prominence-section" style={{ marginTop: '20px' }}>
              <h3>📉 {t('narrative.changeExplanation.lostProminence')}</h3>
              <ul className="prominence-list" style={{
                listStyle: 'none',
                padding: 0,
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
                gap: '10px'
              }}>
                {response.lost_prominence.map((item, idx) => (
                  <li key={idx} style={{
                    padding: '10px 15px',
                    backgroundColor: '#ffebee',
                    border: '1px solid #f44336',
                    borderRadius: '6px',
                    color: '#c62828'
                  }}>{item}</li>
                ))}
              </ul>
            </div>
          )}

          <div className="llm-explanation" style={{ marginTop: '20px' }}>
            <h3>🔄 {t('narrative.changeExplanation.overallAnalysis')}</h3>
            <div className="explanation-content" style={{
              padding: '15px',
              backgroundColor: '#fff9c4',
              border: '1px solid #fbc02d',
              borderRadius: '8px',
              marginTop: '10px'
            }}>
              <p style={{ margin: 0, lineHeight: '1.6', color: '#333' }}>
                {parseMarkdownLinks(response.overall_shift)}
              </p>
            </div>
          </div>
        </>
      )}

      {/* Old format fallback */}
      {!hasNewFormat && data.explanation && (
        <div className="llm-explanation">
          <h3>🤖 {t('narrative.changeExplanation.aiInterpretation')}</h3>
          <div className="explanation-content">
            {data.explanation.split('\n').map((paragraph, idx) => (
              paragraph.trim() && <p key={idx}>{paragraph}</p>
            ))}
          </div>
        </div>
      )}

      {/* Show evidence comparison if available */}
      {data.pre_sentences && data.post_sentences && (
        <EvidenceComparison
          before={data.pre_sentences}
          after={data.post_sentences}
        />
      )}

      {data.speaker_drifts && Object.keys(data.speaker_drifts).length > 0 && (
        <div className="speaker-analysis">
          <h3>📊 {t('narrative.changeExplanation.speakerAnalysis')}</h3>
          <p className="section-description">
            {t('narrative.changeExplanation.speakerDescription')}
          </p>
          <ul className="speaker-list">
            {Object.entries(data.speaker_drifts)
              .slice(0, 5)
              .map(([speaker, drift]) => (
                <li key={speaker} className="speaker-item">
                  <span className="speaker-name">{speaker}</span>
                  <span className="speaker-drift">{drift.toFixed(3)}</span>
                </li>
              ))}
          </ul>
        </div>
      )}
    </div>
  );
}
