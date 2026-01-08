"use client";

import { useState } from "react";
import ConceptForm from "./ConceptForm";
import EvolutionChart from "./EvolutionChart";
import ChangeExplanation from "./ChangeExplanation";
import LoadingSpinner from "@/components/common/LoadingSpinner";
import ErrorBox from "@/components/common/ErrorBox";
import { fetchSemanticEvolution, fetchDriftExplanation } from "@/lib/api";

export default function NarrativeEvolutionPage() {
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
      return 'La fecha final no puede ser anterior a la fecha inicial';
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
      setError("Por favor ingresa un concepto para analizar");
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
        setError("No se encontraron datos suficientes para este concepto. Intenta con otro término o ajusta el umbral de similitud.");
      } else {
        setEvolutionData(data);
      }
    } catch (err) {
      console.error('[NarrativeEvolution] Error:', err);
      setError(err.message || "Error al obtener los datos de evolución");
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
      setExplanationError(err.message || "Error al generar la explicación");
    } finally {
      setLoadingExplanation(false);
    }
  }

  return (
    <div className="page narrative-evolution-page">
      <header className="page-header">
        <h1>Evolución Narrativa</h1>
        <p className="subtitle">
          Analiza cómo cambia el significado de conceptos políticos a través del tiempo
        </p>
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
        <LoadingSpinner message="Analizando evolución semántica..." />
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
            <div style={{ marginTop: '20px' }}>
              <LoadingSpinner message="Generando explicación con IA..." />
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
