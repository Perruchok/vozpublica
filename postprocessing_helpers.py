import requests
from bs4 import BeautifulSoup
import re
import json
import numpy as np
import pandas as pd
from datetime import datetime, date
import random
import time
import psycopg2
from psycopg2.extras import Json
# Import normalized speaker helpers from shared module
from text_utils import parse_speaker_raw
import os
from openai import AzureOpenAI
import tiktoken

# Database settings from environment variables
pg_host = os.environ["PGHOST"]
pg_user = os.environ["PGUSER"]
pg_password = os.environ["PGPASSWORD"]
pg_db = os.environ["PGDATABASE"]
pg_port = os.environ.get("PGPORT", "5432")
# Embedding model settings from environment variables
azure_openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
azure_openai_api_key = os.environ["AZURE_OPENAI_API_KEY"]
azure_openai_api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")


client = AzureOpenAI(
    azure_endpoint=azure_openai_endpoint,
    api_key=azure_openai_api_key,
    api_version=azure_openai_api_version
)

# Usar el nombre de deployment/modelo (definido en la celda de configuración)
# AZURE_DEPLOYMENT debe existir en el entorno de ejecución (se definió en la celda anterior)
MODEL_FOR_ENCODING = globals().get("AZURE_DEPLOYMENT", "text-embedding-3-small")

# Intentar obtener el encoding para el modelo desplegado; si falla, caer a cl100k_base
try:
    ENCODER = tiktoken.encoding_for_model(MODEL_FOR_ENCODING)
except Exception:
    ENCODER = tiktoken.get_encoding("cl100k_base")
    
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/... Chrome/120...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/... Safari/605...",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) Gecko/20100101 Firefox/118...",
    ]

def robust_fetch(url, retries=6):
    """
    Fetches a URL with retries and random User-Agent headers.
    Implements exponential backoff on read timeouts.
    """
    for attempt in range(retries):
        try:
            headers = { "User-Agent": random.choice(USER_AGENTS) }

            # human-like delay (critical for gob.mx)
            time.sleep(random.uniform(1.0, 3.0))

            print(f"Fetching (attempt {attempt+1}): {url}")
            response = requests.get(url, headers=headers, timeout=30)
            return response.text

        except requests.exceptions.ReadTimeout:
            delay = 2 ** attempt
            print(f"Timeout. Waiting {delay}s before retrying...")
            time.sleep(delay)

    raise Exception(f"Failed after {retries} attempts: {url}")

def parse_article_page(url):
    """
    Parses the article page at the given URL and extracts the title, subtitle, and content.
    Returns a dictionary with keys: 'url', 'title', 'subtitle', and 'content'.
    """
    html = robust_fetch(url)
    soup = BeautifulSoup(html, "html.parser")

    # --- Extract Title ---
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else None

    # --- Extract Subtitle ---
    subtitle_tag = soup.find("h2")
    subtitle = subtitle_tag.get_text(strip=True) if subtitle_tag else None

    # --- Extract Article Body ---
    body = soup.find("div", class_="article-body")

    content = []
    if body:
        paragraphs = body.find_all("p")
        for p in paragraphs:
            text = p.get_text(" ", strip=True)
            text = re.sub(r"\s+", " ", text).strip()

            if text and text != "·":
                content.append(text)

    # --- Final JSON structure ---
    article_data = {
        "url": url,
        "title": title,
        "subtitle": subtitle,
        "content": content
    }

    return article_data

def classify_type_from_speaker(sraw, text):
    # specific rules: MODERADOR -> moderator_intro, otherwise speech_turn
    if sraw and sraw.upper().startswith('MODERADOR'):
        return 'moderator_intro'
    return 'speech_turn'

def reformat_transcript(lines, doc_id):
    """
    Reformats a list of transcript lines into a structured list of event dictionaries.

    Each returned entry is a dict with the following top-level keys:
      - doc_id (str)
      - sequence (int)
      - type (str): one of "stage_action", "moderator_intro", "speech_turn", or "unknown"
      - speaker_raw (str|None)
      - speaker_normalized (str|None)
      - role (str|None)
      - text (str)
      - embedding (None)  # placeholder for downstream embedding computation

    Previously a single nested 'speaker' dict was used; now we store the three speaker
    values as top-level fields, which simplifies SQL schema mapping to flat columns.
    """
    out = []
    sequence = 0
    last_entry = None

    speaker_pattern = re.compile(r'^\s*([A-ZÁÉÍÓÚÑ0-9 ,\.\'-]+):\s*(.*)$')
    stage_action_pattern = re.compile(r'^\s*\((.+)\)\s*$', re.DOTALL)

    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue

        # Stage action like "(FIRMA DE ACUERDO...)" or "(TOMA DE FOTOGRAFÍA)"
        m_stage = stage_action_pattern.match(raw)
        if m_stage:
            sequence += 1
            out.append({
                "doc_id": doc_id,
                "sequence": sequence,
                "type": "stage_action",
                "speaker_raw": None,
                "speaker_normalized": None,
                "role": None,
                "text": m_stage.group(1).strip(),
                "embedding": None
            })
            last_entry = out[-1]
            continue

        # Speaker: TEXT pattern
        m = speaker_pattern.match(raw)
        if m:
            speaker_raw = m.group(1).strip()
            text = m.group(2).strip()
            sequence += 1

            # parse into the new, flattened fields using shared helper
            s_raw, s_norm, s_role = parse_speaker_raw(speaker_raw)

            typ = classify_type_from_speaker(speaker_raw, text)
            entry = {
                "doc_id": doc_id,
                "sequence": sequence,
                "type": typ,
                "speaker_raw": s_raw,
                "speaker_normalized": s_norm,
                "role": s_role,
                "text": text,
                "embedding": None
            }
            out.append(entry)
            last_entry = entry
        else:
            # No speaker found — continuation of last turn (append)
            if last_entry is None:
                # No previous speaker -> treat as generic text
                sequence += 1
                out.append({
                    "doc_id": doc_id,
                    "sequence": sequence,
                    "type": "unknown",
                    "speaker_raw": None,
                    "speaker_normalized": None,
                    "role": None,
                    "text": raw,
                    "embedding": None
                })
                last_entry = out[-1]
            else:
                # Append to previous text (preserve order)
                last_entry['text'] = last_entry['text'] + ' ' + raw

    return out

def count_tokens(text: str) -> int:
    return len(ENCODER.encode(text))

def chunk_text(text, max_tokens=450, overlap=50):
    """Divide el texto en chunks usando el encoder del modelo.
    Usa ventana deslizante con `overlap` tokens solapados entre chunks.
    """
    tokens = ENCODER.encode(text)
    chunks = []

    if max_tokens <= 0:
        return [text]

    start = 0
    while start < len(tokens):
        chunk_tokens = tokens[start:start+max_tokens]
        chunk_text = ENCODER.decode(chunk_tokens)
        chunks.append(chunk_text)
        # avanzar con solapamiento
        start += max_tokens - overlap

    return chunks

def embed_text(text: str): # Embedding
    """
    Generates embeddings using Azure OpenAI (2025 syntax).
    Accepts a string or list of strings.
    Returns a vector (list of floats).
    """
    response = client.embeddings.create(
        model="text-embedding-3-small", 
        input=text
    )

    # For a single input, return the 1 vector
    return response.data[0].embedding

def process_speech_turn(turn, max_tokens=450):
    """
    Procesa una intervención del discurso:
    - Si es pequeña (<= max_tokens): genera embedding directamente.
    - Si es grande (> max_tokens): la divide en chunks y genera embeddings para cada chunk
    Args:
        turn (dict): Diccionario con la intervención del discurso.
        max_tokens (int): Número máximo de tokens por chunk.
    Returns:
        list: Lista de diccionarios con embeddings y metadatos.
    """
    text = turn["text"]
    token_count = count_tokens(text)

    # Extract new flattened speaker fields; keep None-safe
    s_raw = turn.get("speaker_raw")
    s_norm = turn.get("speaker_normalized")
    s_role = turn.get("role")

    # Si la intervención es pequeña, solo 1 chunk
    if token_count <= max_tokens:
        embedding = embed_text(text)
        return [{
            "doc_id": turn.get("doc_id"),
            "sequence": turn.get("sequence"),
            "chunk_id": None,                      # no hay subdivisión
            "type": turn.get("type"),
            "speaker_raw": s_raw,
            "speaker_normalized": s_norm,
            "role": s_role,
            "text": text,
            "embedding": embedding,
            "token_count": token_count
        }]

    # Si es grande → dividir en chunks
    chunks = chunk_text(text, max_tokens)
    results = []

    for idx, chunk in enumerate(chunks, start=1):
        embedding = embed_text(chunk)

        results.append({
            "doc_id": turn.get("doc_id"),
            "sequence": turn.get("sequence"),
            "chunk_id": int(idx),                     # 1, 2, 3… (ensure integer, not float)
            "type": turn.get("type"),
            "speaker_raw": s_raw,
            "speaker_normalized": s_norm,
            "role": s_role,
            "text": chunk,
            "embedding": embedding,
            "token_count": count_tokens(chunk)
        })

    return results

def embed_single_article(conference_data, max_tokens=450):
    """
    Procesa todas las intervenciones del discurso en los datos de la conferencia.
    Args:
        conference_data (list): Lista de diccionarios con las intervenciones del discurso.
        max_tokens (int): Número máximo de tokens por chunk.
    Returns:
        list: Lista de diccionarios con embeddings y metadatos para todas las intervenciones.
    """
    all_embeddings = []

    for turn in conference_data:
        embeddings = process_speech_turn(turn, max_tokens)
        all_embeddings.extend(embeddings)

    return all_embeddings

def _serialize_value(v):
    """Convert a single value into a JSON-serializable Python type.

    Handles pandas.Timestamp, numpy scalar types, datetimes, dates, numpy arrays,
    lists, tuples and nested dicts.
    """
    # Treat explicit missing values (pandas/Numpy) first
    try:
        # pandas NA / numpy nan / None
        if pd.isna(v):
            return None
    except Exception:
        pass

    # pandas timestamps
    if isinstance(v, pd.Timestamp):
        return v.isoformat()

    # datetime/date
    if isinstance(v, (datetime, date)):
        return v.isoformat()

    # numpy scalar (np.int64, np.float64, np.bool_ ...)
    if isinstance(v, (np.integer, np.floating, np.bool_)):
        val = v.item()
        # convert NaN/Inf to None to produce strict JSON
        try:
            import math
            if isinstance(val, float) and not math.isfinite(val):
                return None
        except Exception:
            pass
        return val

    # python float (may be nan/inf)
    if isinstance(v, float):
        import math
        if not math.isfinite(v):
            return None
        return v

    # numpy arrays -> list
    if isinstance(v, np.ndarray):
        return [_serialize_value(x) for x in v.tolist()]

    # lists / tuples
    if isinstance(v, (list, tuple)):
        return [_serialize_value(x) for x in v]

    # dicts -> recursively serialize
    if isinstance(v, dict):
        return {k: _serialize_value(val) for k, val in v.items()}

    # fallback: primitives JSON knows how to handle
    try:
        json.dumps(v)
        return v
    except TypeError:
        # last resort stringify
        return str(v)

def df_to_records_serializable(df):
    rows = df.to_dict(orient='records') if df is not None else []
    out = []
    for r in rows:
        nr = {k: _serialize_value(v) for k, v in r.items()}
        out.append(nr)
    # sanity-check that this is JSON-serializable
    try:
        json.dumps(out)
    except Exception:
        # if still failing, coerce everything to str as last resort
        out = [{k: str(v) for k, v in r.items()} for r in out]
    return out

def build_speech_id(row):
    doc = str(row["doc_id"])
    seq = str(row["sequence"])

    chunk = row.get("chunk_id")

    # Safe check for null
    if pd.isna(chunk) or chunk in [None, ""]:
        return f"{doc}-{seq}"

    # Convert chunk to int if it's float like 3.0
    try:
        chunk_str = str(int(chunk))
    except:
        chunk_str = str(chunk)

    return f"{doc}-{seq}-{chunk_str}"

def dedupe_records_by_field(records, field="speech_id"):
    """Deduplicate a list of record dicts by `field`, preserving first-seen.

    Returns a new list with duplicates removed based on equality of the
    field values. Records that lack the field are included (they are treated
    as unique by their dict identity).
    """
    if not records:
        return records

    seen = set()
    out = []
    for r in records:
        key = r.get(field)
        if key is None:
            # include records without the field (they're unique-ish)
            out.append(r)
            continue
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    return out

def database_loading(raw_df, embedded_df):
    # Connect to Azure PostgreSQL
    conn = psycopg2.connect(
        host=pg_host,
        database=pg_db,
        user=pg_user,
        password=pg_password,
        port=pg_port
    )
    cur = conn.cursor()

    # Payloads will be converted to JSON-serializable records with
    # the module-level helper `df_to_records_serializable`.

    raw_payload = df_to_records_serializable(raw_df)
    embedded_payload = df_to_records_serializable(embedded_df)

    # Insert raw_transcripts
    for record in raw_payload:
        # raw_json contains the parsed article (url, title, subtitle, content)
        raw_json_data = record.get('raw_json', {})
        created_at = record.get('created_at')
        
        cur.execute("""
            INSERT INTO raw_transcripts (doc_id, raw_json, created_at)
            VALUES (%s, %s, %s)
            ON CONFLICT (doc_id) DO UPDATE SET
                raw_json = EXCLUDED.raw_json,
                created_at = EXCLUDED.created_at
        """, (record['doc_id'], Json(raw_json_data), created_at))

    # Insert speech_turns
    for record in embedded_payload:
        cur.execute("""
            INSERT INTO speech_turns (speech_id, doc_id, sequence, chunk_id, type, speaker_raw, speaker_normalized, role, text, embedding, token_count, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (speech_id) DO UPDATE SET
                doc_id = EXCLUDED.doc_id,
                sequence = EXCLUDED.sequence,
                chunk_id = EXCLUDED.chunk_id,
                type = EXCLUDED.type,
                speaker_raw = EXCLUDED.speaker_raw,
                speaker_normalized = EXCLUDED.speaker_normalized,
                role = EXCLUDED.role,
                text = EXCLUDED.text,
                embedding = EXCLUDED.embedding,
                token_count = EXCLUDED.token_count,
                created_at = EXCLUDED.created_at
        """, (record['speech_id'], record['doc_id'], record['sequence'], record['chunk_id'], record['type'], 
              record['speaker_raw'], record['speaker_normalized'], record['role'], record['text'], 
              Json(record['embedding']), record['token_count'], record.get('created_at')))

    # Commit and close
    conn.commit()
    cur.close()
    conn.close()
    print("Data loaded to Azure PostgreSQL successfully.")