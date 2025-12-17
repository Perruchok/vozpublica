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