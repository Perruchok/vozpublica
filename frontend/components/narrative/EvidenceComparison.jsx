"use client";

export default function EvidenceComparison({ before, after }) {
  if (!before || !after || before.length === 0 || after.length === 0) {
    return (
      <div className="evidence-comparison empty">
        <p>No hay suficiente evidencia textual para comparar</p>
      </div>
    );
  }

  const formatDate = (date) => {
    if (!date) return "";
    return new Date(date).toLocaleDateString('es-MX', {
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
      <h3>📝 Evidencia Textual</h3>
      <p className="section-description">
        Fragmentos de discursos que ejemplifican el uso del concepto en cada período
      </p>
      
      <div className="evidence-grid">
        <div className="evidence-column">
          <h4 className="column-header before">Antes</h4>
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
          <h4 className="column-header after">Después</h4>
          <div className="evidence-list">
            {after.map((item, idx) => (
              <EvidenceCard key={idx} item={item} />
            ))}
          </div>
        </div>
      </div>

      <div className="evidence-footer">
        <p className="disclaimer">
          💡 Esta evidencia ha sido seleccionada automáticamente por su alta similitud semántica con el concepto analizado.
        </p>
      </div>
    </div>
  );
}
