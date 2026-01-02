BEGIN;

-- 1. Drop dependent constraints & indexes
ALTER TABLE public.speech_turns
  DROP CONSTRAINT IF EXISTS speech_turns_pkey;

ALTER TABLE public.speech_turns
  DROP CONSTRAINT IF EXISTS speech_turns_speech_id_key;

DROP INDEX IF EXISTS idx_speech_turns_speech_id;

-- 2. Remove the surrogate id column
ALTER TABLE public.speech_turns
  DROP COLUMN id;

-- 3. Enforce NOT NULL on speech_id
ALTER TABLE public.speech_turns
  ALTER COLUMN speech_id SET NOT NULL;

-- 4. Promote speech_id to PRIMARY KEY
ALTER TABLE public.speech_turns
  ADD CONSTRAINT speech_turns_pkey PRIMARY KEY (speech_id);

-- 5. Ensure correct indexes remain
CREATE INDEX IF NOT EXISTS idx_speech_turns_doc_id
  ON public.speech_turns (doc_id);

CREATE INDEX IF NOT EXISTS idx_speech_turns_doc_id_sequence
  ON public.speech_turns (doc_id, sequence);

COMMIT;
