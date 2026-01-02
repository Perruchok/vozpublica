-- analytics/queries.sql
SELECT
  date_trunc('month', published_at) AS period,
  embedding
FROM speech_turns
WHERE
  published_at IS NOT NULL
  AND 1 - (embedding <=> $1::vector) > $2
ORDER BY period;
