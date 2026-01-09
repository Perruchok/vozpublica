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

def scrape_with_playwright(max_pages=1, delay=2.0):
    """
    Scrape articles using Playwright (headless browser with JavaScript)
    """
    all_articles = []
    
    with sync_playwright() as p:
        print("🚀 Launching headless browser...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        
        for page_num in range(1, max_pages + 1):
            url = f"https://www.gob.mx/presidencia/es/archivo/articulos?page={page_num}"
            print(f"\n📄 Scraping page {page_num}: {url}")
            
            try:
                # Navigate and wait for content
                page.goto(url, wait_until="networkidle", timeout=60000)
                
                # Wait for articles to load
                page.wait_for_selector("article", timeout=30000)
                
                # Get HTML after JavaScript execution
                html = page.content()
                
                # Use existing parser
                articles = extract_articles_info_from_html(html)
                
                if articles:
                    all_articles.extend(articles)
                    print(f"✓ Found {len(articles)} articles on page {page_num}")
                else:
                    print(f"⚠️  No articles found on page {page_num}")
                    break
                    
            except Exception as e:
                print(f"❌ Error on page {page_num}: {e}")
                # Save screenshot for debugging
                page.screenshot(path=f"/tmp/page_{page_num}_error.png")
                print(f"📸 Screenshot saved to /tmp/page_{page_num}_error.png")
                break
            
            time.sleep(delay)
        
        browser.close()
    
    return all_articles

if __name__ == "__main__":
    print("=" * 60)
    print("SCRAPER WITH PLAYWRIGHT - BYPASS ANTI-BOT")
    print("=" * 60)
    
    # Scrape articles
    articles = scrape_with_playwright(max_pages=5)
    
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
