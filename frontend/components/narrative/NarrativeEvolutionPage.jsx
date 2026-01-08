"use client";

import { useState } from "react";
import { useLanguage } from '@/lib/languageContext';
import LanguageToggle from '@/components/common/LanguageToggle';
import ConceptForm from "./ConceptForm";
import EvolutionChart from "./EvolutionChart";
import ChangeExplanation from "./ChangeExplanation";
import ErrorBox from "@/components/common/ErrorBox";
import { fetchSemanticEvolution, fetchDriftExplanation } from "@/lib/api";
import Link from 'next/link';

export default function NarrativeEvolutionPage() {
  const { t, translations } = useLanguage();
  const [concept, setConcept] = useState("");
  const [granularity, setGranularity] = useState("month");
  const [evolutionData, setEvolutionData] = useState(null);
  const [selectedChange, setSelectedChange] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [loadingExplanation, setLoadingExplanation] = useState(false);
  const [explanationError, setExplanationError] = useState(null);
  
  // Helper function to get today's date in YYYY-MM-DD format
  const getTodayDate = () => {
    const today = new Date();
    return today.toISOString().split('T')[0];
  };
  
  // Date range state
  const [startDate, setStartDate] = useState('2024-10-01');
  const [endDate, setEndDate] = useState(getTodayDate());
  const [dateRangeError, setDateRangeError] = useState(null);
  
  // Validate date range
  const validateDateRange = (start, end) => {
    if (new Date(end) < new Date(start)) {
      return t('narrative.dateRangeError');
    }
    return null;
  };
  
  // Handle date changes
  const handleStartDateChange = (e) => {
    const newStartDate = e.target.value;
    setStartDate(newStartDate);
    const error = validateDateRange(newStartDate, endDate);
    setDateRangeError(error);
  };
  
  const handleEndDateChange = (e) => {
    const newEndDate = e.target.value;
    setEndDate(newEndDate);
    const error = validateDateRange(startDate, newEndDate);
    setDateRangeError(error);
  };

  async function runAnalysis() {
    if (!concept.trim()) {
      setError(t('narrative.errorEmptyConcept'));
      return;
    }
    
    // Validate date range before making API call
    const rangeError = validateDateRange(startDate, endDate);
    if (rangeError) {
      setError(rangeError);
      return;
    }

    setLoading(true);
    setError(null);
    setEvolutionData(null);
    setSelectedChange(null);

    try {
      console.log('[NarrativeEvolution] Fetching semantic evolution for:', concept);
      
      const data = await fetchSemanticEvolution({
        concept,
        granularity,
        start_date: startDate,
        end_date: endDate,
        similarity_threshold: 0.6
      });
      
      console.log('[NarrativeEvolution] Received data:', data);
      
      if (!data.drift || data.drift.length === 0) {
        setError(t('narrative.errorNoData'));
      } else {
        setEvolutionData(data);
      }
    } catch (err) {
      console.error('[NarrativeEvolution] Error:', err);
      
      // Handle timeout errors specifically
      if (err.message.includes('timeout') || err.message.includes('504')) {
        setError(t('narrative.errorTimeout'));
      } else if (err.message.includes('503')) {
        setError(t('narrative.errorServiceUnavailable'));
      } else {
        setError(err.message || t('narrative.errorFetchingData'));
      }
    } finally {
      setLoading(false);
    }
  }

  async function explainChange(from, to) {
    setLoadingExplanation(true);
    setExplanationError(null);
    setSelectedChange(null);

    try {
      const data = await fetchDriftExplanation({
        concept,
        from_period: from,
        to_period: to,
        similarity_threshold: 0.6
      });
      setSelectedChange(data);
    } catch (err) {
      console.error('[NarrativeEvolution] Error fetching explanation:', err);
      setExplanationError(err.message || t('narrative.errorExplanation'));
    } finally {
      setLoadingExplanation(false);
    }
  }

  return (
    <div className="page narrative-evolution-page">
      <header className="page-header">
        <div className="page-header-top">
          <h1>📊 {t('narrative.title')}</h1>
          <LanguageToggle />
        </div>
        <p className="subtitle">{t('narrative.subtitle')}</p>
        <Link href="/" className="back-link">← {t('narrative.backToHome')}</Link>
      </header>

      <ConceptForm
        concept={concept}
        granularity={granularity}
        onConceptChange={setConcept}
        onGranularityChange={setGranularity}
        onSubmit={runAnalysis}
        disabled={loading}
        startDate={startDate}
        endDate={endDate}
        onStartDateChange={handleStartDateChange}
        onEndDateChange={handleEndDateChange}
        dateRangeError={dateRangeError}
        getTodayDate={getTodayDate}
      />

      {error && <ErrorBox message={error} onDismiss={() => setError(null)} />}

      {loading && (
        <div className="narrative-loading">
          <div className="loading-spinner"></div>
          <p>{t('narrative.analyzingEvolution')}</p>
        </div>
      )}

      {evolutionData && !loading && (
        <>
          <EvolutionChart
            concept={concept}
            points={evolutionData.drift}
            onSelectChange={explainChange}
            disabled={loadingExplanation}
          />
          
          {loadingExplanation && (
            <div className="narrative-loading" style={{ marginTop: '20px' }}>
              <div className="loading-spinner"></div>
              <p>{t('narrative.generatingExplanation')}</p>
            </div>
          )}

          {explanationError && !loadingExplanation && (
            <div style={{ 
              marginTop: '20px', 
              padding: '15px', 
              border: '1px solid #f44336', 
              borderRadius: '4px', 
              backgroundColor: '#ffebee',
              color: '#c62828'
            }}>
              <strong>Error:</strong> {explanationError}
            </div>
          )}

          {selectedChange && !loadingExplanation && !explanationError && (
            <div style={{ marginTop: '20px' }}>
              <ChangeExplanation data={selectedChange} />
            </div>
          )}
        </>
      )}
    </div>
  );
}
