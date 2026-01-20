"""
Scraper with Playwright to bypass gob.mx anti-bot protection
Requires: pip install playwright && playwright install chromium
"""
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from backend.utils.scraper_helpers import (
    extract_articles_info_from_html,
    add_articles_metadata, 
    save_new_metadata
)
import time

load_dotenv()

def scrape_with_playwright(max_pages=3, delay=2.0):
    """
    Scrape articles using Playwright (headless browser with JavaScript)
    With enhanced anti-bot evasion and timeout handling
    """
    all_articles = []
    
    with sync_playwright() as p:
        print("🚀 Launching headless browser...")
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',  # Hide automation
                '--disable-dev-shm-usage',  # Reduce memory usage
                '--no-first-run',
                '--no-default-browser-check',
                '--disable-background-networking',
            ]
        )
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            locale='es-MX',
            timezone_id='America/Mexico_City',
            extra_http_headers={
                'Accept-Language': 'es-MX,es;q=0.9,en-US;q=0.8,en;q=0.7',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Referer': 'https://www.gob.mx/',
                'Cache-Control': 'no-cache',
            }
        )
        page = context.new_page()
        
        # Stealth measures
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)
        
        for page_num in range(1, max_pages + 1):
            url = f"https://www.gob.mx/presidencia/es/archivo/articulos?page={page_num}"
            print(f"\n📄 Scraping page {page_num}: {url}")
            
            try:
                # Navigate with extended timeout and fallback strategy
                try:
                    # First try with networkidle (more reliable)
                    page.goto(url, wait_until="networkidle", timeout=90000)
                except Exception as e1:
                    print(f"⚠️  networkidle timeout, trying domcontentloaded...")
                    # Fallback to domcontentloaded
                    page.goto(url, wait_until="domcontentloaded", timeout=90000)
                
                # Wait for articles to load with extended timeout
                try:
                    page.wait_for_selector("article", timeout=30000)
                except Exception as e:
                    print(f"⚠️  article selector timeout, trying alternative selectors...")
                    # Try alternative selectors for articles
                    page.wait_for_selector("div.article-item, article.article-card, div.contenedor-articulo", timeout=20000)
                
                # Get HTML after JavaScript execution
                html = page.content()
                
                if not html or len(html) < 1000:
                    print(f"⚠️  Page content too small, possible loading error")
                    page.screenshot(path=f"/tmp/page_{page_num}_small.png")
                    time.sleep(delay * 2)
                    continue
                
                # Use existing parser
                articles = extract_articles_info_from_html(html)
                
                if articles:
                    all_articles.extend(articles)
                    print(f"✓ Found {len(articles)} articles on page {page_num}")
                else:
                    print(f"⚠️  No articles found on page {page_num}")
                    # Don't break - try next page anyway
                    
            except Exception as e:
                print(f"❌ Error on page {page_num}: {e}")
                # Save screenshot for debugging
                page.screenshot(path=f"/tmp/page_{page_num}_error.png")
                print(f"📸 Screenshot saved to /tmp/page_{page_num}_error.png")
                
                # Retry with increased delay
                print(f"⏳ Waiting {delay * 3}s before retry...")
                time.sleep(delay * 3)
                continue
            
            # Increase delay to avoid being blocked
            time.sleep(delay)
        
        browser.close()
    
    return all_articles


if __name__ == "__main__":
    print("=" * 60)
    print("SCRAPER WITH PLAYWRIGHT - BYPASS ANTI-BOT")
    print("=" * 60)
    
    # Scrape articles with increased delay to avoid blocking
    articles = scrape_with_playwright(max_pages=5, delay=3.0)
    
    if not articles:
        print("\n❌ No articles found")
        exit(1)
    
    print(f"\n✓ Total articles scraped: {len(articles)}")
    
    # Add metadata
    print("\n🔍 Adding metadata...")
    articles_with_meta = add_articles_metadata(articles)
    
    # Save to database
    print("\n💾 Saving to database...")
    save_new_metadata(articles_with_meta)
    
    print("\n✅ Done!")
