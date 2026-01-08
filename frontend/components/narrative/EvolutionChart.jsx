"use client";

import { useState } from "react";

export default function EvolutionChart({ concept, points, onSelectChange, disabled = false }) {
  const [selectedIndex, setSelectedIndex] = useState(null);
  const [hoveredIndex, setHoveredIndex] = useState(null);

  if (!points || points.length === 0) {
    return (
      <div className="evolution-chart empty">
        <p>No hay datos suficientes para mostrar la evolución</p>
      </div>
    );
  }

  const handlePointClick = (idx) => {
    if (disabled) return;
    
    setSelectedIndex(idx);
    const current = points[idx];
    
    // Send only YYYY-MM format to API
    onSelectChange(
      formatPeriodForAPI(current.from),
      formatPeriodForAPI(current.to)
    );
  };

  const formatPeriod = (period) => {
    if (!period) return "";
    const date = new Date(period);
    return date.toISOString().split('T')[0];
  };

  const formatPeriodForAPI = (period) => {
    if (!period) return "";
    const date = new Date(period);
    const isoString = date.toISOString();
    // Extract only YYYY-MM
    return isoString.substring(0, 7);
  };

  const getChangeLevel = (change) => {
    if (change < 0.1) return "low";
    if (change < 0.3) return "medium";
    return "high";
  };

  // SVG dimensions
  const width = 900;
  const height = 400;
  const padding = { top: 30, right: 40, bottom: 80, left: 70 };
  const chartWidth = width - padding.left - padding.right;
  const chartHeight = height - padding.top - padding.bottom;

  // Calculate scales
  const maxChange = Math.max(...points.map(p => p.semantic_change), 0.1);
  const minChange = Math.min(...points.map(p => p.semantic_change), 0);
  const yRange = maxChange - minChange || 0.1;
  const yScale = (value) => chartHeight - ((value - minChange) / yRange) * chartHeight;
  const xScale = (idx) => (idx / Math.max(points.length - 1, 1)) * chartWidth;

  // Generate path for the line
  const linePath = points
    .map((point, idx) => {
      const x = padding.left + xScale(idx);
      const y = padding.top + yScale(point.semantic_change);
      return `${idx === 0 ? 'M' : 'L'} ${x} ${y}`;
    })
    .join(' ');
  
  // Generate area path (filled area under the line)
  const areaPath = points.length > 0 ? 
    linePath + 
    ` L ${padding.left + xScale(points.length - 1)} ${height - padding.bottom}` +
    ` L ${padding.left} ${height - padding.bottom} Z` 
    : '';

  return (
    <div className="evolution-chart">
      <h2>Evolución Semántica: "{concept}"</h2>
      
      <div className="chart-container" style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        marginBottom: '30px',
        overflow: 'auto'
      }}>
        <svg 
          viewBox={`0 0 ${width} ${height}`}
          style={{ 
            width: '100%',
            maxWidth: '900px',
            height: 'auto',
            border: '1px solid #e0e0e0', 
            borderRadius: '8px', 
            background: 'linear-gradient(to bottom, #fafafa 0%, #ffffff 100%)',
            boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
          }}
          preserveAspectRatio="xMidYMid meet"
        >
          <defs>
            <linearGradient id="areaGradient" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" style={{ stopColor: '#4a90e2', stopOpacity: 0.3 }} />
              <stop offset="100%" style={{ stopColor: '#4a90e2', stopOpacity: 0.05 }} />
            </linearGradient>
            <filter id="shadow">
              <feDropShadow dx="0" dy="1" stdDeviation="2" floodOpacity="0.3"/>
            </filter>
          </defs>
          
          {/* Grid lines */}
          {[0, 0.25, 0.5, 0.75, 1].map((fraction) => {
            const value = minChange + yRange * fraction;
            const y = padding.top + yScale(value);
            return (
              <line
                key={`grid-${fraction}`}
                x1={padding.left}
                y1={y}
                x2={width - padding.right}
                y2={y}
                stroke="#e0e0e0"
                strokeWidth="1"
                strokeDasharray="4,4"
              />
            );
          })}
          
          {/* Y-axis */}
          <line
            x1={padding.left}
            y1={padding.top}
            x2={padding.left}
            y2={height - padding.bottom}
            stroke="#333"
            strokeWidth="2"
          />
          {/* X-axis */}
          <line
            x1={padding.left}
            y1={height - padding.bottom}
            x2={width - padding.right}
            y2={height - padding.bottom}
            stroke="#333"
            strokeWidth="2"
          />
          
          {/* Y-axis label */}
          <text
            x={15}
            y={height / 2}
            transform={`rotate(-90, 15, ${height / 2})`}
            fontSize="14"
            fontWeight="600"
            fill="#555"
            textAnchor="middle"
          >
            Cambio Semántico
          </text>
          
          {/* X-axis label */}
          <text
            x={width / 2}
            y={height - 15}
            fontSize="14"
            fontWeight="600"
            fill="#555"
            textAnchor="middle"
          >
            Período
          </text>
          
          {/* Y-axis ticks */}
          {[0, 0.25, 0.5, 0.75, 1].map((fraction) => {
            const value = minChange + yRange * fraction;
            const y = padding.top + yScale(value);
            return (
              <g key={fraction}>
                <line
                  x1={padding.left - 6}
                  y1={y}
                  x2={padding.left}
                  y2={y}
                  stroke="#333"
                  strokeWidth="2"
                />
                <text
                  x={padding.left - 12}
                  y={y + 4}
                  fontSize="12"
                  fill="#555"
                  textAnchor="end"
                  fontWeight="500"
                >
                  {value.toFixed(2)}
                </text>
              </g>
            );
          })}
          
          {/* Area under the line */}
          <path
            d={areaPath}
            fill="url(#areaGradient)"
          />
          
          {/* Line path */}
          <path
            d={linePath}
            fill="none"
            stroke="#4a90e2"
            strokeWidth="3"
            strokeLinecap="round"
            strokeLinejoin="round"
            filter="url(#shadow)"
          />
          
          {/* Data points */}
          {points.map((point, idx) => {
            const x = padding.left + xScale(idx);
            const y = padding.top + yScale(point.semantic_change);
            const isSelected = selectedIndex === idx;
            const isHovered = hoveredIndex === idx;
            const changeLevel = getChangeLevel(point.semantic_change);
            
            const colorMap = {
              low: '#4caf50',
              medium: '#ff9800',
              high: '#f44336'
            };
            
            return (
              <g key={idx}>
                {/* Outer ring on hover/select */}
                {(isHovered || isSelected) && (
                  <circle
                    cx={x}
                    cy={y}
                    r={12}
                    fill="none"
                    stroke={colorMap[changeLevel]}
                    strokeWidth="2"
                    opacity="0.3"
                  />
                )}
                
                {/* Data point */}
                <circle
                  cx={x}
                  cy={y}
                  r={isSelected ? 7 : isHovered ? 6 : 5}
                  fill={colorMap[changeLevel]}
                  stroke="white"
                  strokeWidth="2.5"
                  style={{ 
                    cursor: disabled ? 'default' : 'pointer',
                    transition: 'all 0.2s ease'
                  }}
                  onClick={() => handlePointClick(idx)}
                  onMouseEnter={() => setHoveredIndex(idx)}
                  onMouseLeave={() => setHoveredIndex(null)}
                  filter={isSelected || isHovered ? "url(#shadow)" : "none"}
                />
                
                {/* Tooltip on hover */}
                {isHovered && (
                  <g>
                    <rect
                      x={x > chartWidth / 2 ? x - 160 : x + 15}
                      y={y - 50}
                      width={150}
                      height={60}
                      fill="rgba(0, 0, 0, 0.9)"
                      rx="6"
                      filter="url(#shadow)"
                    />
                    <text 
                      x={x > chartWidth / 2 ? x - 155 : x + 20} 
                      y={y - 32} 
                      fontSize="11" 
                      fill="white"
                      fontWeight="500"
                    >
                      De: {formatPeriod(point.from)}
                    </text>
                    <text 
                      x={x > chartWidth / 2 ? x - 155 : x + 20} 
                      y={y - 18} 
                      fontSize="11" 
                      fill="white"
                      fontWeight="500"
                    >
                      A: {formatPeriod(point.to)}
                    </text>
                    <text 
                      x={x > chartWidth / 2 ? x - 155 : x + 20} 
                      y={y - 4} 
                      fontSize="12" 
                      fill="#ffd700" 
                      fontWeight="bold"
                    >
                      Cambio: {point.semantic_change.toFixed(3)}
                    </text>
                  </g>
                )}
                
                {/* X-axis labels */}
                {(idx % Math.max(1, Math.floor(points.length / 5)) === 0 || idx === points.length - 1) && (
                  <text
                    x={x}
                    y={height - padding.bottom + 20}
                    fontSize="10"
                    fill="#555"
                    textAnchor="middle"
                    transform={`rotate(-35, ${x}, ${height - padding.bottom + 20})`}
                    fontWeight="500"
                  >
                    {formatPeriod(point.to).substring(0, 7)}
                  </text>
                )}
              </g>
            );
          })}
        </svg>
      </div>

      <div className="chart-legend">
        <p className="hint">
          📊 Haz clic en cualquier punto del gráfico o en el botón "Explicar" para ver la explicación del cambio semántico
        </p>
        <div className="legend-items">
          <span className="legend-item">
            <span className="dot" style={{ backgroundColor: '#4caf50' }}></span> Cambio bajo (&lt; 0.1)
          </span>
          <span className="legend-item">
            <span className="dot" style={{ backgroundColor: '#ff9800' }}></span> Cambio medio (0.1 - 0.3)
          </span>
          <span className="legend-item">
            <span className="dot" style={{ backgroundColor: '#f44336' }}></span> Cambio alto (&gt; 0.3)
          </span>
        </div>
      </div>

      <div className="data-table" style={{ overflowX: 'auto' }}>
        <h3>Cambios Semánticos</h3>
        <table style={{ width: '100%', minWidth: '500px' }}>
          <thead>
            <tr>
              <th>Período</th>
              <th>Cambio Semántico</th>
              <th>Acción</th>
            </tr>
          </thead>
          <tbody>
            {points.map((point, idx) => (
              <tr
                key={idx}
                className={selectedIndex === idx ? 'selected' : ''}
                style={{ 
                  backgroundColor: selectedIndex === idx ? '#e3f2fd' : 'transparent',
                  transition: 'background-color 0.2s ease'
                }}
              >
                <td>
                  {formatPeriod(point.from)} → {formatPeriod(point.to)}
                </td>
                <td>
                  <span 
                    className={`change-badge ${getChangeLevel(point.semantic_change)}`}
                    style={{
                      padding: '4px 12px',
                      borderRadius: '12px',
                      fontSize: '13px',
                      fontWeight: '600',
                      backgroundColor: 
                        getChangeLevel(point.semantic_change) === 'low' ? '#e8f5e9' :
                        getChangeLevel(point.semantic_change) === 'medium' ? '#fff3e0' : '#ffebee',
                      color:
                        getChangeLevel(point.semantic_change) === 'low' ? '#2e7d32' :
                        getChangeLevel(point.semantic_change) === 'medium' ? '#e65100' : '#c62828'
                    }}
                  >
                    {point.semantic_change.toFixed(3)}
                  </span>
                </td>
                <td>
                  <button
                    onClick={() => handlePointClick(idx)}
                    disabled={disabled}
                    className="explain-button"
                    style={{
                      padding: '6px 16px',
                      borderRadius: '6px',
                      border: 'none',
                      backgroundColor: disabled && selectedIndex === idx ? '#90caf9' : '#2196f3',
                      color: 'white',
                      fontWeight: '500',
                      cursor: disabled ? 'wait' : 'pointer',
                      transition: 'all 0.2s ease',
                      opacity: disabled && selectedIndex !== idx ? 0.6 : 1
                    }}
                    onMouseOver={(e) => !disabled && (e.target.style.backgroundColor = '#1976d2')}
                    onMouseOut={(e) => !disabled && (e.target.style.backgroundColor = '#2196f3')}
                  >
                    {disabled && selectedIndex === idx ? 'Cargando...' : 'Explicar'}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
