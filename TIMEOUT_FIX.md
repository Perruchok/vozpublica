# Semantic Evolution Timeout Optimization

## Problem
Users were experiencing `TimeoutError` when querying semantic evolution for complex concepts over long date ranges.

## Root Cause
- Database query timeout set to 60 seconds
- Vector similarity queries on large datasets can exceed this limit
- The query was loading all matching rows without limits

## Solutions Implemented

### 1. Increased Database Timeout ✅
**File:** `backend/utils/dbpool.py`
- Changed `command_timeout` from 60 to 180 seconds
- Allows more time for complex vector operations

### 2. Optimized SQL Query ✅
**File:** `backend/app/services/semantic_evolution_service.py`

**Changes:**
- Added `LIMIT 10000` to prevent unbounded result sets
- Changed similarity filter to use distance operator (`<=>`) for better index usage
- Ordered by similarity DESC to get most relevant results first
- Converted similarity threshold to distance threshold for proper indexing

**Before:**
```sql
WHERE 1 - (st.embedding <=> $1::vector) > $4
ORDER BY period;
```

**After:**
```sql
WHERE (st.embedding <=> $1::vector) < $5  -- Distance-based filter
ORDER BY similarity DESC
LIMIT 10000;
```

### 3. Better Error Handling ✅
**File:** `backend/app/api/semantic_evolution.py`

Added specific error handlers for:
- `TimeoutError` → Returns 504 with helpful message
- `QueryCanceledError` → Returns 504 with retry suggestion
- `TooManyConnectionsError` → Returns 503 with retry message

Added performance logging:
- Request parameters logged
- Query execution time tracked
- Result counts reported

### 4. User-Friendly Frontend Messages ✅
**File:** `frontend/components/narrative/NarrativeEvolutionPage.jsx`

- Detect timeout errors (504)
- Provide actionable suggestions:
  - Use higher similarity threshold (0.7-0.8)
  - Reduce date range
  - Use more specific concepts

### 5. UI Guidance ✅
**File:** `frontend/components/narrative/ConceptForm.jsx`

Added help box with tips:
- Reduce date range (3-6 months)
- Use specific concepts
- Switch to monthly granularity

## Performance Improvements

### Expected Results:
- **Queries under 2 months**: < 10 seconds
- **Queries 2-6 months**: 10-30 seconds  
- **Queries 6-12+ months**: 30-120 seconds (may timeout)

### Recommendations for Users:
1. Start with **3-month date ranges**
2. Use **monthly granularity** for longer periods
3. Use **specific concepts** (avoid very broad terms)
4. Default threshold (0.6) is good, but 0.7-0.8 for faster results

## Testing
To verify the fix works:

1. Try the problematic query again:
   ```
   Concept: "intervención militar de estados unidos a mexico"
   Date range: 2024-10-01 to 2026-01-08
   Granularity: month
   Threshold: 0.6
   ```

2. If still timing out, try:
   - Shorter range: 2024-10-01 to 2024-12-31
   - Higher threshold: 0.7 or 0.75

## Future Optimizations (if needed)

1. **Implement pagination** - Process data in chunks
2. **Add result caching** - Cache frequently requested analyses
3. **Pre-compute popular concepts** - Background jobs for common queries
4. **Database indexes** - Ensure proper indexes on `published_at` + embedding columns
5. **Query parallelization** - Split by date ranges and merge results
