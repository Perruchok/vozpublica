"""
Complete scraper with Playwright to extract full transcriptions
Bypasses gob.mx anti-bot protection using headless browser
"""
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from bs4 import BeautifulSoup
import pandas as pd
import re
from backend.utils.postprocessing_helpers import reformat_transcript, embed_single_article, database_loading, build_speech_id
from backend.utils.scraper_helpers import get_missing_articles_meta
import time

load_dotenv()

def parse_article_page_playwright(page, url, max_retries=2):
    """
    Parse article page using Playwright browser
    Returns dict with url, title, subtitle, and content
    """
    for attempt in range(1, max_retries + 1):
        try:
            print(f"  Fetching (attempt {attempt}): {url}")
            page.goto(url, wait_until="networkidle", timeout=45000)
            
            # Wait for article body
            page.wait_for_selector("div.article-body", timeout=30000)
            
            html = page.content()
            soup = BeautifulSoup(html, "html.parser")
            
            # Extract Title
            title_tag = soup.find("h1")
            title = title_tag.get_text(strip=True) if title_tag else None
            
            # Extract Subtitle
            subtitle_tag = soup.find("h2")
            subtitle = subtitle_tag.get_text(strip=True) if subtitle_tag else None
            
            # Extract Article Body
            body = soup.find("div", class_="article-body")
            
            content = []
            if body:
                paragraphs = body.find_all("p")
                for p in paragraphs:
                    text = p.get_text(" ", strip=True)
                    text = re.sub(r"\s+", " ", text).strip()
                    if text and text != "·":
                        content.append(text)
            
            return {
                "url": url,
                "title": title,
                "subtitle": subtitle,
                "content": content
            }
            
        except PlaywrightTimeout as e:
            print(f"  ⚠️  Timeout on attempt {attempt}: {e}")
            if attempt < max_retries:
                time.sleep(3)
                continue
            else:
                print(f"  ❌ Failed after {max_retries} attempts")
                return {"url": url, "title": None, "subtitle": None, "content": []}
        except Exception as e:
            print(f"  ❌ Error on attempt {attempt}: {e}")
            if attempt < max_retries:
                time.sleep(3)
                continue
            else:
                return {"url": url, "title": None, "subtitle": None, "content": []}
    
    return {"url": url, "title": None, "subtitle": None, "content": []}


def scrape_transcripts_with_playwright():
    """
    Main scraping function using Playwright
    """
    # Get missing articles from database
    missing_articles_meta = get_missing_articles_meta()
    print(f"Found {len(missing_articles_meta)} articles missing full text.\n")
    
    if missing_articles_meta.empty:
        print("No articles to process!")
        return
    
    with sync_playwright() as p:
        print("🚀 Launching browser...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        
        for index, article in missing_articles_meta.iterrows():
            print(f"\n{'='*60}")
            print(f"Processing article {index+1}/{len(missing_articles_meta)}")
            print(f"doc_id: {article['doc_id']}")
            print(f"{'='*60}")
            
            try:
                # Parse article page with Playwright
                article_raw_json = parse_article_page_playwright(page, article['href'])
                transcript_lines = article_raw_json.get("content", [])
                
                if not transcript_lines:
                    print(f"⚠️  No content found in article {article['doc_id']}, skipping...")
                    continue
                
                print(f"✓ Found {len(transcript_lines)} speech turns")
                
                # Reformat and embed
                transcript_lines_structured = reformat_transcript(transcript_lines, article['doc_id'])
                print(f"✓ Structured {len(transcript_lines_structured)} speech turns")
                
                transcript_lines_embedded = embed_single_article(transcript_lines_structured, max_tokens=300)
                
                if not transcript_lines_embedded:
                    print(f"⚠️  Embedding returned empty list for {article['doc_id']}, skipping...")
                    continue
                
                print(f"✓ Generated {len(transcript_lines_embedded)} embeddings")
                
            except Exception as e:
                print(f"❌ ERROR processing article {article['doc_id']}: {str(e)}")
                print(f"Skipping to next article...")
                continue
            
            # Prepare DataFrames
            article_raw_df = pd.DataFrame([{
                "doc_id": article['doc_id'],
                "created_at": pd.Timestamp.now(),
                "raw_json": article_raw_json
            }])
            
            article_embedded_df = pd.DataFrame(transcript_lines_embedded)
            
            if article_embedded_df.empty:
                print(f"⚠️  DataFrame is empty after embedding for {article['doc_id']}, skipping...")
                continue
            
            article_embedded_df["created_at"] = pd.Timestamp.now()
            
            # Handle chunk_id column
            if "chunk_id" not in article_embedded_df.columns:
                article_embedded_df["chunk_id"] = None
            else:
                article_embedded_df["chunk_id"] = pd.to_numeric(article_embedded_df["chunk_id"], errors="coerce").astype("Int64")
            
            # Create speech_id
            article_embedded_df["speech_id"] = article_embedded_df.apply(build_speech_id, axis=1)
            
            # Save to database
            try:
                database_loading(article_raw_df, article_embedded_df)
                print(f"✅ Successfully saved {article['doc_id']} to database")
            except Exception as e:
                print(f"❌ Database error for {article['doc_id']}: {e}")
                continue
            
            # Small delay between articles
            time.sleep(2)
        
        browser.close()
        print(f"\n{'='*60}")
        print("✅ Scraping completed!")
        print(f"{'='*60}")


if __name__ == "__main__":
    print("=" * 60)
    print("TRANSCRIPT SCRAPER WITH PLAYWRIGHT")
    print("=" * 60)
    scrape_transcripts_with_playwright()
