"use client";

import { GRANULARITY_OPTIONS } from "@/lib/constants";

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
  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit();
  };

  return (
    <form className="concept-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="concept-input">Concepto a analizar</label>
        <input
          id="concept-input"
          type="text"
          placeholder="ej: seguridad pública, educación, salud"
          value={concept}
          onChange={(e) => onConceptChange(e.target.value)}
          disabled={disabled}
          className="concept-input"
        />
        <p className="help-text">
          Ingresa un concepto político o tema de interés público
        </p>
      </div>

      <div className="form-group">
        <label htmlFor="granularity-select">Granularidad temporal</label>
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
        <label>Rango de Fechas</label>
        <div style={{ display: 'flex', gap: '15px', alignItems: 'flex-start', flexWrap: 'wrap' }}>
          <div style={{ flex: '1', minWidth: '200px' }}>
            <label htmlFor="startDate" style={{ display: 'block', marginBottom: '5px', fontSize: '14px', fontWeight: 'normal' }}>
              Fecha Inicial:
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
              Fecha Final:
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

      <button
        type="submit"
        className="submit-button"
        disabled={disabled || !concept.trim()}
      >
        {disabled ? "Analizando..." : "Analizar Evolución"}
      </button>
    </form>
  );
}
