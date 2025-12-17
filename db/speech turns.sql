-- Create speech_turns table
CREATE TABLE IF NOT EXISTS speech_turns (
    id SERIAL PRIMARY KEY,
    doc_id TEXT NOT NULL,
    sequence INTEGER,
    chunk_id INTEGER,
    type TEXT,
    speaker_raw TEXT,
    speaker_normalized TEXT,
    role TEXT,
    text TEXT NOT NULL,
    embedding vector(1536),  -- Adjust dimension based on your model
    token_count INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    speech_id TEXT UNIQUE
);