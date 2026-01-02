BEGIN;

CREATE TABLE IF NOT EXISTS public.raw_transcripts_meta (
  doc_id text NOT NULL,
  href text NOT NULL,
  title text,
  scraped_at timestamptz DEFAULT now(),
  published_at timestamptz,
  CONSTRAINT raw_transcripts_meta_pkey PRIMARY KEY (doc_id)
);

COMMIT;
