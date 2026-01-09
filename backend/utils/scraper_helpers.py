import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import re
import html
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import psycopg2
import os

BASE_URL = "https://www.gob.mx"
PAGE_URL_TEMPLATE = "https://www.gob.mx/presidencia/es/archivo/articulos?page={}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "es-MX,es;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Cache-Control": "max-age=0"
}

# Azure PostgreSQL connection settings
pg_host = os.environ.get("PGHOST")
pg_user = os.environ.get("PGUSER")
pg_password = os.environ.get("PGPASSWORD")
pg_db = os.environ.get("PGDATABASE")
pg_port = os.environ.get("PGPORT", "5432")

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
    Converts a raw date (e.g. '2025-11-25 11:42:00' or '2025-11-25T11:42:00Z')
    to an ISO 8601 string with timezone (TIMESTAMPTZ), e.g. '2025-11-25T11:42:00-06:00'.
    Parameters:
      - raw_date_str: string with raw date (may include 'T' or ' ' and/or zone).
      - tz: IANA timezone name to apply if date has no offset (default 'America/Mexico_City').
    Returns:
      - ISO string with offset (e.g. '2025-11-25T11:42:00-06:00') or None if cannot be parsed.
    """
    if not raw_date_str:
        return None

    s = raw_date_str.strip().replace('\\"', '').replace('"', '').replace('\\/', '/')

    # Simple parsing attempts:
    dt = None
    # 1) fromisoformat (accepts 'YYYY-MM-DD HH:MM:SS' and 'YYYY-MM-DDTHH:MM:SS' with offset)
    try:
        dt = datetime.fromisoformat(s)
    except Exception:
        pass

    # 2) If failed, try '%Y-%m-%d %H:%M:%S'
    if dt is None:
        try:
            dt = datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
        except Exception:
            dt = None

    # 3) last resort: extract with regex and try again
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
        # Could not parse
        return None

    # If dt has no timezone, assign the requested zone
    if dt.tzinfo is None:
        try:
            tzinfo = ZoneInfo(tz)
        except Exception:
            tzinfo = timezone.utc
        dt = dt.replace(tzinfo=tzinfo)

    # Return ISO with offset (compatible with TIMESTAMPTZ)
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
    Extracts article information (link, date, title) from HTML of a given page.
    Returns a list of dictionaries with keys: 'link', 'date', 'title'.
    
    Raises:
        RuntimeError: If anti-bot protection is detected instead of real content.
    """
    # Check for anti-bot protection FIRST
    if "Challenge Validation" in html or "sec-cpt-if" in html or "provider=\"crypto\"" in html:
        raise RuntimeError(
            "❌ ANTI-BOT PROTECTION DETECTED\n"
            "El sitio gob.mx está bloqueando el scraper con un challenge criptográfico.\n"
            "El HTML recibido contiene un challenge que requiere JavaScript para resolverse.\n\n"
            "Soluciones:\n"
            "1. Usar Selenium o Playwright para ejecutar JavaScript\n"
            "2. Usar un servicio de proxy que resuelva challenges automáticamente\n"
            "3. Contactar con gob.mx para obtener acceso a una API oficial\n\n"
            "El scraping con requests simple ya no funciona para este sitio."
        )
    
    soup = BeautifulSoup(html, "html.parser")
    articles = soup.find_all("article")
    
    # Validate we found articles
    if not articles:
        # Save sample for debugging
        sample = html[:1000].replace('\n', ' ')
        raise RuntimeError(
            f"⚠️  NO ARTICLES FOUND IN HTML\n"
            f"El HTML no contiene elementos <article>.\n"
            f"Muestra del HTML recibido:\n{sample}\n...\n\n"
            f"Esto puede indicar:\n"
            f"1. Cambio en la estructura del sitio\n"
            f"2. Protección anti-bot activa\n"
            f"3. Error en la respuesta del servidor"
        )
    
    result = []
    for article in articles:
        # Link
        a = article.find("a", href=True)
        href = a["href"] if a else None
        link = clean_url(urljoin(BASE_URL, href)) if href else None
        
        # Date
        raw_date, raw_time = extract_datetime_from_time_tag(article.find("time"))
        # If we have time, combine date+time to format correctly; if not, pass only the date
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
        
        result.append({"href": link, "published_at": date, "title": title})
    
    return result

# Main function to get all articles across multiple pages
def get_all_articles_across_pages(max_pages=10, delay=2.5, timeout=30):
    """
    Iterates through article pages up to max_pages or until no more results.
    Returns a list of dictionaries with information from found articles.
    """
    all_articles = []
    seen_pages_without_results = 0
    print("Starting to scrape articles...")
    
    # Create a session to maintain cookies/state
    import requests
    session = requests.Session()
    session.headers.update(HEADERS)
    
    for page in range(1, max_pages + 1):
        url = PAGE_URL_TEMPLATE.format(page)
        print(f"Scraping page {page}: {url}")
        try:
            resp = session.get(url, timeout=timeout, allow_redirects=True)
            
            # Check for anti-bot challenge
            if "Challenge Validation" in resp.text or "sec-container" in resp.text:
                print(f"⚠️  Anti-bot protection detected on page {page}.")
                print(f"💾 Saving HTML to /tmp/page_{page}_challenge.html for inspection")
                with open(f"/tmp/page_{page}_challenge.html", "w", encoding="utf-8") as f:
                    f.write(resp.text)
                raise RuntimeError(
                    "❌ SCRAPING BLOQUEADO\n\n"
                    "El sitio gob.mx está usando protección anti-bot que requiere JavaScript.\n"
                    "El método actual con requests NO PUEDE bypasear esta protección.\n\n"
                    "SOLUCIONES RECOMENDADAS:\n"
                    "1. Implementar Playwright/Selenium (navegador headless con JavaScript)\n"
                    "2. Usar la API oficial si existe\n"
                    "3. Ejecutar el script manualmente desde un navegador\n\n"
                    f"HTML del challenge guardado en: /tmp/page_{page}_challenge.html"
                )
            
            if resp.status_code == 404:
                print("Page not found (404), stopping.")
                break
            resp.raise_for_status()
            
            # This will raise RuntimeError if no articles found
            articles = extract_articles_info_from_html(resp.text)
            
            seen_pages_without_results = 0
            all_articles.extend(articles)
            print(f"✓ Found {len(articles)} articles on page {page}")
            
        except RuntimeError as e:
            # Re-raise our custom errors (anti-bot, no articles)
            print(f"\n{str(e)}")
            raise
        except Exception as e:
            print(f"❌ Error scraping page {page}: {e}")
            raise
        
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
    Adds additional metadata to each article in the list.
    Added metadata: 'doc_id', 'scraped_at'.
    Returns a pandas DataFrame with articles and their metadata.
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
    into the Azure PostgreSQL table 'raw_transcripts_meta', deduplicated by doc_id.
    """
    # Connect to Azure PostgreSQL
    conn = psycopg2.connect(
        host=pg_host,
        database=pg_db,
        user=pg_user,
        password=pg_password,
        port=pg_port
    )
    cur = conn.cursor()

    try:
        # --- 1. Fetch existing doc_ids already stored in Azure ---
        cur.execute("SELECT doc_id FROM raw_transcripts_meta")
        existing_ids = {row[0] for row in cur.fetchall()}

        # --- 2. Filter the DataFrame to keep only new metadata ---
        df_new = df_scraped[~df_scraped["doc_id"].isin(existing_ids)]

        if df_new.empty:
            print("No new metadata to insert.")
            return

        # --- 3. Insert new records ---
        inserted_count = 0
        for _, row in df_new.iterrows():
            cur.execute("""
                INSERT INTO raw_transcripts_meta (doc_id, href, title, published_at, scraped_at)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (doc_id) DO NOTHING
            """, (row['doc_id'], row['href'], row['title'], row['published_at'], row['scraped_at']))
            inserted_count += 1

        conn.commit()
        print(f"Inserted {inserted_count} new metadata records.")
    
    finally:
        cur.close()
        conn.close()

def get_missing_articles_meta():
    """
    Returns doc_id values that exist in `raw_transcripts_meta` but are NOT present
    in `speech_turns`.
    Returns a pandas.DataFrame with columns ['doc_id', 'href'] for missing articles. 
    This function fetches `doc_id` + `href` from `raw_transcripts_meta` so the
    caller receives the original link along with the id that needs processing.
    """
    # Connect to Azure PostgreSQL
    conn = psycopg2.connect(
        host=pg_host,
        database=pg_db,
        user=pg_user,
        password=pg_password,
        port=pg_port
    )
    cur = conn.cursor()

    try:
        # --- Get doc_ids + hrefs from raw_transcripts_meta ---
        cur.execute("SELECT doc_id, href FROM raw_transcripts_meta")
        meta_rows = cur.fetchall()
        
        meta_ids = {row[0] for row in meta_rows}
        # Map doc_id -> href (may be None)
        meta_href_map = {row[0]: row[1] for row in meta_rows}

        # --- Get doc_ids already present in speech_turns ---
        cur.execute("SELECT DISTINCT doc_id FROM speech_turns")
        article_rows = cur.fetchall()
        article_ids = {row[0] for row in article_rows}

        # --- Calculate missing ones ---
        missing_doc_ids = sorted(list(meta_ids - article_ids))

        import pandas as pd
        rows = [{"doc_id": did, "href": meta_href_map.get(did)} for did in missing_doc_ids]
        return pd.DataFrame(rows)
    
    finally:
        cur.close()
        conn.close()