import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import re
import html
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
try:
    from supabase import create_client
except Exception:
    # Allow the module to be imported in test environments where supabase
    # client isn't installed. Functions that need an active client (e.g.
    # save_new_metadata) should handle supabase being None.
    create_client = None

BASE_URL = "https://www.gob.mx"
PAGE_URL_TEMPLATE = "https://www.gob.mx/presidencia/es/archivo/articulos?page={}"
HEADERS = {"User-Agent": "Mozilla/5.0"}

url = "https://yelycfehdjepwkzheumv.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InllbHljZmVoZGplcHdremhldW12Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQwMDIyMzYsImV4cCI6MjA3OTU3ODIzNn0.HSETZUpaiqzdRmjwjdFOrHesGPhrccXsRT82ClnjikA"
if create_client is not None:
    try:
        supabase = create_client(url, key)
    except Exception:
        supabase = None
else:
    supabase = None

####### Scrapping Helper Functions #######

def clean_url(url):
    """Remove escaped characters and quotes from URL"""
    if not url:
        return None
    # Remove all types of quotes and escape characters
    cleaned = url.replace('\\"', '').replace('"', '').replace('\\/', '/')
    # Remove leading/trailing spaces
    cleaned = cleaned.strip()
    return cleaned

def clean_title(title_str):
    """Extract clean title, removing HTML tags and escape characters"""
    if not title_str:
        return None
    # Remove escape characters and quotes
    cleaned = title_str.replace('\\"', '').replace('"', '').replace('\\/', '/')
    # Remove HTML tags
    cleaned = re.sub(r'<[^>]+>', '', cleaned)
    # Remove common JS patterns
    cleaned = re.sub(r'\\n|\\t', ' ', cleaned)
    cleaned = re.sub(r'Continuar leyendo.*', '', cleaned, flags=re.DOTALL)
    # Strip extra whitespace
    cleaned = ' '.join(cleaned.split())
    return cleaned.strip()

def format_date_to_timestamptz(raw_date_str, tz="America/Mexico_City"):
    """
    Convierte una fecha bruta (ej. '2025-11-25 11:42:00' o '2025-11-25T11:42:00Z')
    a un string ISO 8601 con zona horaria (TIMESTAMPTZ), p.ej. '2025-11-25T11:42:00-06:00'.
    Parámetros:
      - raw_date_str: cadena con la fecha cruda (puede incluir 'T' o ' ' y/o zona).
      - tz: nombre IANA de la zona horaria a aplicar si la fecha no tiene offset (por defecto 'America/Mexico_City').
    Retorna:
      - Cadena ISO con offset (ej. '2025-11-25T11:42:00-06:00') o None si no se puede parsear.
    """
    if not raw_date_str:
        return None

    s = raw_date_str.strip().replace('\\"', '').replace('"', '').replace('\\/', '/')

    # Intentos simples de parseo:
    dt = None
    # 1) fromisoformat (acepta 'YYYY-MM-DD HH:MM:SS' y 'YYYY-MM-DDTHH:MM:SS' con offset)
    try:
        dt = datetime.fromisoformat(s)
    except Exception:
        pass

    # 2) Si falló, probar '%Y-%m-%d %H:%M:%S'
    if dt is None:
        try:
            dt = datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
        except Exception:
            dt = None

    # 3) última salvación: extraer con regex y volver a intentar
    if dt is None:
        m = re.search(r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:?\d{2})?", s)
        if m:
            part = m.group(0)
            try:
                dt = datetime.fromisoformat(part)
            except Exception:
                try:
                    dt = datetime.strptime(part.split('Z')[0], "%Y-%m-%d %H:%M:%S")
                except Exception:
                    dt = None

    if dt is None:
        # No se pudo parsear
        return None

    # Si dt no tiene timezone, asignar la zona pedida
    if dt.tzinfo is None:
        try:
            tzinfo = ZoneInfo(tz)
        except Exception:
            tzinfo = timezone.utc
        dt = dt.replace(tzinfo=tzinfo)

    # Retornar ISO con offset (compatible con TIMESTAMPTZ)
    return dt.isoformat()

def extract_datetime_from_time_tag(tag):
    """
    Extracts date and time from a messy <time> tag like:
    <time date='"2025-11-25' 11:42:00"">martes, 25 de noviembre...</time>
    
    Returns:
        (date_str, time_str)
    """
    html = str(tag)

    # --- Extract date (YYYY-MM-DD) ---
    # Matches date='\"2025-11-25' or date="2025-11-25"
    date_match = re.search(r"date=['\"]\\?\"?(\d{4}-\d{2}-\d{2})", html)
    date_str = date_match.group(1) if date_match else None

    # --- Extract time (HH:MM:SS) ---
    # Matches the weird pattern 11:42:00\"="" or even plain 11:42:00
    time_match = re.search(r"(\d{2}:\d{2}:\d{2})", html)
    time_str = time_match.group(1) if time_match else None

    return date_str, time_str

def extract_articles_info_from_html(html):
    """
    Extrae la información de artículos (link, date, title) del HTML de una página dada.
    Retorna una lista de diccionarios con las claves: 'link', 'date', 'title'.
    """
    soup = BeautifulSoup(html, "html.parser")
    articles = []
    for article in soup.find_all("article"):
        # Link
        a = article.find("a", href=True)
        href = a["href"] if a else None
        link = clean_url(urljoin(BASE_URL, href)) if href else None
        
        # Date
        raw_date, raw_time = extract_datetime_from_time_tag(article.find("time"))
        # Si tenemos hora, combinar fecha+hora para formatear correctamente; si no, pasar solo la fecha
        if raw_date and raw_time:
            combined = f"{raw_date} {raw_time}"
        elif raw_date:
            combined = raw_date
        else:
            combined = None
        date = format_date_to_timestamptz(combined) if combined else None

        
        # Title
        h2 = article.find("h2")
        # Use inner text of h2; sometimes the content contains extra nodes, so get_text is safer
        title = clean_title(h2.get_text(" ", strip=True)) if h2 else None
        
        articles.append({"href": link, "published_at": date, "title": title})
    return articles

# Main function to get all articles across multiple pages
def get_all_articles_across_pages(max_pages=700, delay=1.0, timeout=15):
    """
    Recorre las páginas de artículos hasta max_pages o hasta que no haya más resultados.
    Retorna una lista de diccionarios con la información de los artículos encontrados.
    """
    all_articles = []
    seen_pages_without_results = 0
    print("Starting to scrape articles...")
    for page in range(1, max_pages + 1):
        url = PAGE_URL_TEMPLATE.format(page)
        print(f"Scraping page {page}: {url}")
        try:
            resp = requests.get(url, headers=HEADERS, timeout=timeout)
            if resp.status_code == 404:
                print("Page not found (404), stopping.")
                break
            resp.raise_for_status()
            articles = extract_articles_info_from_html(resp.text)
            if not articles:
                seen_pages_without_results += 1
                print(f"No articles found on page {page}.")
                if seen_pages_without_results >= 3:
                    print("No results for 3 pages in a row, stopping.")
                    break
            else:
                seen_pages_without_results = 0
                all_articles.extend(articles)
        except Exception as e:
            print(f"Error scraping page {page}: {e}")
        import time
        time.sleep(delay)
    # Deduplicate by href
    seen = set()
    dedup = []
    for art in all_articles:
        if art["href"] and art["href"] not in seen:
            seen.add(art["href"])
            dedup.append(art)
    return dedup

def add_articles_metadata(articles):
    """
    Agrega metadatos adicionales a cada artículo en la lista.
    Metadatos agregados: 'doc_id', 'scraped_at'.
    Retorna un DataFrame de pandas con los artículos y sus metadatos.
    """
    df = pd.DataFrame(articles)
    # Add current date in format timestamptz
    scraped_at = datetime.now(ZoneInfo("America/Mexico_City")).isoformat()
    df['scraped_at'] = scraped_at
    # Add document id based on  date + title substring
    def make_doc_id(row):
        # extract YYYY-MM-DD from date (fall back to today in target tz)
        try:
            date_part = pd.to_datetime(row.get('published_at')).strftime('%Y-%m-%d')
        except Exception:
            date_part = datetime.now(ZoneInfo("America/Mexico_City")).strftime('%Y-%m-%d')
        title = (row.get('title') or '').lower()
        # check the specific Spanish substring (case-insensitive)
        if "conferencia de prensa de la presidenta claudia sheinbaum pardo" in title:
            suffix = 'mananera'
        else:
            suffix = 'conference'
        return f"{date_part}-{suffix}"

    # Generate base doc_id values first
    df['doc_id'] = df.apply(make_doc_id, axis=1)

    # Ensure doc_id uniqueness within this dataframe: if duplicates exist in the
    # scraped batch (e.g. two articles producing the same base id), append
    # a numeric suffix 2,3,... to subsequent occurrences so insertions to the DB
    # won't fail due to unique constraint violations.
    counts = {}
    unique_ids = []
    for base_id in df['doc_id'].tolist():
        if base_id in counts:
            counts[base_id] += 1
            new_id = f"{base_id}{counts[base_id]}"
        else:
            counts[base_id] = 1
            new_id = base_id
        unique_ids.append(new_id)

    df['doc_id'] = unique_ids
    return df

def save_new_metadata(df_scraped: pd.DataFrame):
    """
    Take a pandas DataFrame with scraped metadata and insert only new records
    into the Supabase table 'raw_transcripts_meta', deduplicated by doc_id.
    """

    # --- 1. Fetch existing doc_ids already stored in Supabase ---
    existing = supabase.table("raw_transcripts_meta").select("doc_id").execute()
    existing_ids = {row["doc_id"] for row in existing.data}

    # --- 2. Filter the DataFrame to keep only new metadata ---
    df_new = df_scraped[~df_scraped["doc_id"].isin(existing_ids)]

    if df_new.empty:
        print("No new metadata to insert.")
        return

    # Convert to list of dicts for Supabase
    new_records = df_new.to_dict(orient="records")

    # --- 3. Insert in batches (Supabase tends to allow ~500 rows per insert) ---
    BATCH_SIZE = 500
    for i in range(0, len(new_records), BATCH_SIZE):
        batch = new_records[i : i + BATCH_SIZE]
        supabase.table("raw_transcripts_meta").insert(batch).execute()

    print(f"Inserted {len(new_records)} new metadata records.")

def get_missing_articles_meta():
    """
    Returns doc_id values that exist in `raw_transcripts_meta` but are NOT present
    in `speech_turns`.
    Returns a pandas.DataFrame with columns ['doc_id', 'href'] for missing articles. 
    This function fetches `doc_id` + `href` from `raw_transcripts_meta` so the
    caller receives the original link along with the id that needs processing.
    """

    # --- Get doc_ids + hrefs from raw_transcripts_meta ---
    meta_resp = supabase.table("raw_transcripts_meta").select("doc_id, href").execute()
    meta_rows = meta_resp.data or []

    meta_ids = {row["doc_id"] for row in meta_rows}
    # Map doc_id -> href (may be None)
    meta_href_map = {row["doc_id"]: row.get("href") for row in meta_rows}

    # --- Get doc_ids already present in speech_turns ---
    article_resp = supabase.table("speech_turns").select("doc_id").execute()
    article_rows = article_resp.data or []
    article_ids = {row["doc_id"] for row in article_rows}

    # --- Calculate missing ones ---
    missing_doc_ids = sorted(list(meta_ids - article_ids))

   
    import pandas as pd
    rows = [{"doc_id": did, "href": meta_href_map.get(did)} for did in missing_doc_ids]
    return pd.DataFrame(rows)