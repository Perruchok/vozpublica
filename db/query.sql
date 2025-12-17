SELECT
  COALESCE(raw_transcripts.doc_id, raw_transcripts_meta.doc_id) AS doc_id,
  CASE
    WHEN raw_transcripts.doc_id IS NULL THEN 'only_in_b'
    WHEN raw_transcripts_meta.doc_id IS NULL THEN 'only_in_a'
  END AS location
FROM raw_transcripts
FULL OUTER JOIN raw_transcripts_meta
  ON raw_transcripts.doc_id = raw_transcripts_meta.doc_id
WHERE raw_transcripts.doc_id IS NULL OR raw_transcripts_meta.doc_id IS NULL;