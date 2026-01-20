from backend.utils.dbpool import get_pool
from backend.utils.postprocessing_helpers import embed_text

# Minimum length thresholds for meaningful content
MIN_TEXT_LENGTH = 150  # characters
MIN_WORD_COUNT = 20    # words


def is_meaningful_result(text: str) -> bool:
    """
    Filters out poor quality or too-short results that aren't meaningful.
    Args:
        text (str): The text to evaluate.
    Returns:
        bool: True if the text is meaningful enough to return.
    """
    if not text:
        return False
    
    # Check minimum character length
    if len(text.strip()) < MIN_TEXT_LENGTH:
        return False
    
    # Check minimum word count
    word_count = len(text.split())
    if word_count < MIN_WORD_COUNT:
        return False
    
    return True


async def semantic_search(query: str, top_k: int):
    """
    Performs a semantic search over the documents.
    Args:
        query (str): The search query.
        top_k (int): The number of top relevant documents to retrieve.
    Returns:
        results (list): List of relevant documents with meaningful content.
    """
    # 1️⃣ Embed query
    embedding = embed_text(query)
    embedding_str = '[' + ','.join(map(str, embedding)) + ']'

    # 2️⃣ Vector search - fetch more results to account for filtering
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

    # Fetch more results to account for filtering
    fetch_limit = max(top_k * 3, top_k + 20)
    
    async with pool.acquire() as conn:
        rows = await conn.fetch(sql, embedding_str, fetch_limit)

    if not rows:
        return []

    # 3️⃣ Filter results for meaningful content
    meaningful_results = [
        dict(row) for row in rows
        if is_meaningful_result(row['text'])
    ]

    # Return top_k meaningful results
    return meaningful_results[:top_k]
