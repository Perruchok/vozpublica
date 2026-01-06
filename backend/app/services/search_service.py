from backend.utils.dbpool import get_pool
from backend.utils.postprocessing_helpers import embed_text

async def semantic_search(query: str, top_k: int):
    """
    Performs a semantic search over the documents.
    Args:
        query (str): The search query.
        top_k (int): The number of top relevant documents to retrieve.
    Returns:
        results (list): List of relevant documents.
    """
    # 1️⃣ Embed query
    embedding = embed_text(query)
    embedding_str = '[' + ','.join(map(str, embedding)) + ']'

    # 2️⃣ Vector search
    pool = await get_pool()

    sql = """
    SELECT
      st.doc_id,
      st.speech_id,
      st.text,
      st.speaker_normalized,
      st.role,
      rtm.href,
      rtm.title,
      1 - (st.embedding <=> $1::vector) AS similarity
    FROM speech_turns st
    LEFT JOIN raw_transcripts_meta rtm ON st.doc_id = rtm.doc_id
    ORDER BY st.embedding <=> $1::vector
    LIMIT $2;
    """

    async with pool.acquire() as conn:
        rows = await conn.fetch(sql, embedding_str, top_k)

    if not rows:
        return []

    return [dict(row) for row in rows]