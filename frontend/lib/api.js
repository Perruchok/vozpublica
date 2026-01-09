/**
 * API client for VozPública backend
 */

import { API_BASE_URL } from './constants';

/**
 * Generic fetch wrapper with error handling
 */
async function fetchAPI(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  console.log('[API] Request:', { url, method: options.method || 'GET', body: options.body });

  try {
    const response = await fetch(url, { ...defaultOptions, ...options });
    
    console.log('[API] Response status:', response.status, response.statusText);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      console.error('[API] Error response:', errorData);
      throw new Error(
        errorData.detail || errorData.message || `HTTP error! status: ${response.status}`
      );
    }

    const data = await response.json();
    console.log('[API] Response data:', data);
    return data;
  } catch (error) {
    console.error('[API] Fetch error:', error);
    throw error;
  }
}

/**
 * Fetch semantic evolution data for a concept
 * @param {Object} params - Query parameters
 * @param {string} params.concept - The concept to analyze
 * @param {string} params.granularity - Time granularity (day, week, month)
 * @param {string} params.start_date - Start date (YYYY-MM-DD)
 * @param {string} params.end_date - End date (YYYY-MM-DD)
 * @param {number} params.similarity_threshold - Similarity threshold (0-1)
 * @returns {Promise<Object>} Evolution data with points and drift
 */
export async function fetchSemanticEvolution(params) {
  const {
    concept,
    granularity = 'month',
    start_date = '2024-01-01',
    end_date = '2024-12-31',
    similarity_threshold = 0.75
  } = params;

  return fetchAPI('/api/semantic-evolution', {
    method: 'POST',
    body: JSON.stringify({
      concept,
      granularity,
      start_date,
      end_date,
      similarity_threshold
    }),
  });
}

/**
 * Fetch explanation for semantic drift between two periods
 * @param {Object} params - Query parameters
 * @param {string} params.concept - The concept being analyzed
 * @param {string} params.from_period - Start period (YYYY-MM-DD)
 * @param {string} params.to_period - End period (YYYY-MM-DD)
 * @param {number} params.similarity_threshold - Similarity threshold (0-1)
 * @returns {Promise<Object>} Explanation with LLM analysis and evidence
 */
export async function fetchDriftExplanation(params) {
  const {
    concept,
    from_period,
    to_period,
    similarity_threshold = 0.75
  } = params;

  return fetchAPI('/api/explain-drift', {
    method: 'POST',
    body: JSON.stringify({
      concept,
      from_period,
      to_period,
      similarity_threshold
    }),
  });
}

/**
 * Fetch topic discovery data
 * @param {string} startDate - Start date (YYYY-MM-DD)
 * @param {string} endDate - End date (YYYY-MM-DD)
 * @returns {Promise<Object>} Topic analysis data
 */
export async function fetchTopicDiscovery(startDate, endDate) {
  return fetchAPI('/api/analytics/topics', {
    method: 'POST',
    body: JSON.stringify({
      start_date: startDate,
      end_date: endDate,
    }),
  });
}

/**
 * Fetch speaker profile data
 * @param {string} speakerName - Name of the speaker
 * @returns {Promise<Object>} Speaker profile data
 */
export async function fetchSpeakerProfile(speakerName) {
  return fetchAPI(`/api/speakers/${encodeURIComponent(speakerName)}`);
}

/**
 * Perform semantic search on presidential discourse corpus
 * @param {string} query - Natural language search query
 * @param {number} topK - Number of results to return (default: 5)
 * @returns {Promise<Object>} Search results with matching fragments
 */
export async function searchSemanticDocuments(query, topK = 5) {
  return fetchAPI('/api/search', {
    method: 'POST',
    body: JSON.stringify({
      question: query,
      top_k: topK
    }),
  });
}

/**
 * Ask a question about the presidential discourse corpus
 * @param {string} question - Natural language question
 * @param {number} topK - Number of source documents to use (default: 5)
 * @returns {Promise<Object>} Answer with sources
 */
export async function askQuestion(question, topK = 5) {
  return fetchAPI('/api/question', {
    method: 'POST',
    body: JSON.stringify({
      question: question,
      top_k: topK
    }),
  });
}
