from postprocessing_helpers import parse_article_page, reformat_transcript, embed_single_article, database_loading, build_speech_id
import pandas as pd

missing_articles_meta = get_missing_articles_meta()
print(f"Found {len(missing_articles_meta)} articles missing full text.")

# I will test with a small list first
sample_missing = missing_articles_meta

for index, article in sample_missing.iterrows():
    print(f"Processing article with doc_id: {article['doc_id']}")
    # Parse article and extract raw content
    article_raw_json = parse_article_page(article['href'])
    transcript_lines = article_raw_json.get("content", [])
    transcript_lines_structured = reformat_transcript(transcript_lines, article['doc_id'])
    transcript_lines_embedded = embed_single_article(transcript_lines_structured, max_tokens=300)

    article_raw_df = pd.DataFrame([{
        "doc_id": article['doc_id'],
        "created_at": pd.Timestamp.now(),
        "raw_json": article_raw_json
    }])
    # Embedded is a list of dicts where each dict must be a row, and the keys their columns
    article_embedded_df = pd.DataFrame(transcript_lines_embedded)
    article_embedded_df["created_at"] = pd.Timestamp.now()
    # Hotfix for chunk_id to be int — ensure the column exists (may be missing if no chunking occurred)
    if "chunk_id" not in article_embedded_df.columns:
        article_embedded_df["chunk_id"] = None
        print("chunk_id column missing; created with None values:", article_embedded_df["doc_id"])
    else:
        article_embedded_df["chunk_id"] = pd.to_numeric(article_embedded_df["chunk_id"], errors="coerce").astype("Int64")
    # Need to create new id to avoid conflicts
    article_embedded_df["speech_id"] = article_embedded_df.apply(build_speech_id, axis=1)

    # Attempt to save entries to supabase
    database_loading(article_raw_df, article_embedded_df)