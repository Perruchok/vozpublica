BEGIN;

CREATE TABLE IF NOT EXISTS public.raw_transcripts (
  doc_id text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  raw_json jsonb NOT NULL,

  CONSTRAINT raw_transcripts_pkey PRIMARY KEY (doc_id),
  CONSTRAINT raw_transcripts_doc_id_fkey
    FOREIGN KEY (doc_id)
    REFERENCES public.raw_transcripts_meta (doc_id)
    ON DELETE CASCADE
);

COMMIT;
