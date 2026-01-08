"use client";

import { GRANULARITY_OPTIONS } from "@/lib/constants";
import { useLanguage } from '@/lib/languageContext';

export default function ConceptForm({
  concept,
  granularity,
  onConceptChange,
  onGranularityChange,
  onSubmit,
  disabled = false,
  startDate,
  endDate,
  onStartDateChange,
  onEndDateChange,
  dateRangeError,
  getTodayDate,
}) {
  const { t, translations } = useLanguage();
  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit();
  };

  return (
    <form className="concept-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="concept-input">{t('narrative.conceptLabel')}</label>
        <input
          id="concept-input"
          type="text"
          placeholder={t('narrative.conceptPlaceholder')}
          value={concept}
          onChange={(e) => onConceptChange(e.target.value)}
          disabled={disabled}
          className="concept-input"
        />
        <p className="help-text">
          {t('narrative.conceptHelp')}
        </p>
        <div style={{ 
          marginTop: '8px', 
          padding: '10px', 
          backgroundColor: 'rgba(251, 191, 36, 0.1)',
          border: '1px solid rgba(251, 191, 36, 0.3)',
          borderRadius: '6px',
          fontSize: '13px',
          color: '#92400e',
          lineHeight: '1.5'
        }}>
          {t('narrative.conceptLanguageNotice')}
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="granularity-select">{t('narrative.granularity')}</label>
        <select
          id="granularity-select"
          value={granularity}
          onChange={(e) => onGranularityChange(e.target.value)}
          disabled={disabled}
          className="granularity-select"
        >
          {GRANULARITY_OPTIONS.map(option => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label>{t('narrative.dateRange')}</label>
        <div style={{ display: 'flex', gap: '15px', alignItems: 'flex-start', flexWrap: 'wrap' }}>
          <div style={{ flex: '1', minWidth: '200px' }}>
            <label htmlFor="startDate" style={{ display: 'block', marginBottom: '5px', fontSize: '14px', fontWeight: 'normal' }}>
              {t('narrative.startDate')}
            </label>
            <input
              type="date"
              id="startDate"
              value={startDate}
              min="2024-10-01"
              max={getTodayDate()}
              onChange={onStartDateChange}
              disabled={disabled}
              style={{ padding: '8px', fontSize: '14px', borderRadius: '4px', border: '1px solid #ccc', width: '100%' }}
            />
          </div>
          <div style={{ flex: '1', minWidth: '200px' }}>
            <label htmlFor="endDate" style={{ display: 'block', marginBottom: '5px', fontSize: '14px', fontWeight: 'normal' }}>
              {t('narrative.endDate')}
            </label>
            <input
              type="date"
              id="endDate"
              value={endDate}
              min="2024-10-01"
              max={getTodayDate()}
              onChange={onEndDateChange}
              disabled={disabled}
              style={{ padding: '8px', fontSize: '14px', borderRadius: '4px', border: '1px solid #ccc', width: '100%' }}
            />
          </div>
        </div>
        {dateRangeError && (
          <div style={{ marginTop: '10px', padding: '8px', backgroundColor: '#fee', color: '#c33', borderRadius: '4px', fontSize: '14px' }}>
            {dateRangeError}
          </div>
        )}
      </div>

      <div className="help-box" style={{ 
        marginTop: '15px', 
        padding: '12px', 
        background: 'linear-gradient(to right, rgba(102, 126, 234, 0.08), rgba(118, 75, 162, 0.08))',
        borderRadius: '6px',
        border: '1px solid rgba(102, 126, 234, 0.2)',
        fontSize: '14px',
        lineHeight: '1.6'
      }}>
        <strong style={{ color: '#667eea' }}>💡 {t('narrative.tip')}</strong>
        <ul style={{ marginTop: '8px', marginLeft: '20px', color: '#475569' }}>
          {translations.narrative.tips.map((tip, index) => (
            <li key={index}>{tip}</li>
          ))}
        </ul>
      </div>

      <button
        type="submit"
        className="submit-button"
        disabled={disabled || !concept.trim()}
      >
        {disabled ? t('narrative.analyzing') : t('narrative.analyzeButton')}
      </button>
    </form>
  );
}
