/**
 * Application constants
 */

// API Configuration
// Para desarrollo: siempre usa localhost:8000
// Para producción: configura NEXT_PUBLIC_API_URL en Vercel/etc
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Time granularity options
export const GRANULARITY_OPTIONS = [
  { value: 'day', label: 'Diario' },
  { value: 'week', label: 'Semanal' },
  { value: 'month', label: 'Mensual' },
];

// Semantic change thresholds
export const CHANGE_THRESHOLDS = {
  LOW: 0.1,
  MEDIUM: 0.3,
  HIGH: 0.5,
};

// Default date ranges
export const DEFAULT_DATE_RANGES = {
  PRE: ['2024-10-01', '2025-07-01'],
  POST: ['2025-08-01', '2025-12-01'],
};

// Chart configuration
export const CHART_CONFIG = {
  colors: {
    low: '#4ade80',
    medium: '#fbbf24',
    high: '#f87171',
  },
  minHeight: 200,
  maxHeight: 400,
};

// Similarity threshold for evidence selection
export const SIMILARITY_THRESHOLD = 0.6;

// Maximum number of evidence examples to show
export const MAX_EVIDENCE_ITEMS = 10;
