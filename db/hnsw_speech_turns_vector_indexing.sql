-- IMPORTANT:
-- 1. Do NOT wrap in BEGIN/COMMIT
-- 2. Must run alone

-- CONCURRENTLY prevents read/write blocking
-- F NOT EXISTS makes it safe to rerun
-- No transaction allowed (Postgres restriction)

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_speech_turns_embedding_hnsw
ON public.speech_turns
USING hnsw (embedding vector_cosine_ops)
WITH (
  m = 16,
  ef_construction = 200
);