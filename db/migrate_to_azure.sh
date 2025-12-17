#!/bin/bash
# Migration script: Supabase → Azure PostgreSQL

echo "Setting up Azure PostgreSQL database..."

# Connect to Azure and set up schema
psql "host=$PGHOST port=$PGPORT dbname=$PGDATABASE user=$PGUSER password=$PGPASSWORD sslmode=require" << 'EOF'

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

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

-- Create indexes for better performance (excluding vector index for now)
CREATE INDEX IF NOT EXISTS idx_speech_turns_doc_id ON speech_turns(doc_id);
CREATE INDEX IF NOT EXISTS idx_speech_turns_speech_id ON speech_turns(speech_id);

-- Create the match_speech_turns function (same as Supabase)
CREATE OR REPLACE FUNCTION match_speech_turns(query_embedding vector, match_count int)
RETURNS TABLE(
    id int,
    doc_id text,
    sequence int,
    chunk_id int,
    type text,
    speaker_raw text,
    speaker_normalized text,
    role text,
    text text,
    embedding vector,
    token_count int,
    created_at timestamp with time zone,
    speech_id text,
    similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        st.id,
        st.doc_id,
        st.sequence,
        st.chunk_id,
        st.type,
        st.speaker_raw,
        st.speaker_normalized,
        st.role,
        st.text,
        st.embedding,
        st.token_count,
        st.created_at,
        st.speech_id,
        1 - (st.embedding <=> query_embedding) AS similarity
    FROM speech_turns st
    ORDER BY st.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

EOF

echo "Azure database setup complete!"
echo ""
echo "Now migrating data from Supabase..."

# Export data from Supabase using Python API
python3 export_supabase_data.py

# Check if export was successful
if [ ! -f "supabase_data.json" ]; then
    echo "❌ Export failed, exiting..."
    exit 1
fi

# Import data to Azure using Python
python3 import_to_azure.py

echo "Data migration complete!"

echo "Migration complete!"
echo ""
echo "Next steps:"
echo "1. Update your connection strings in the code:"
echo "   AZURE_DB_URL=postgresql://$AZURE_USER:$AZURE_PASSWORD@$AZURE_HOST:$AZURE_PORT/$AZURE_DB"
echo "2. Run: python3 update_connections.py"
echo "3. Test the application"