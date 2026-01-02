from scraper_helpers import get_all_articles_across_pages, add_articles_metadata, save_new_metadata, get_missing_articles_meta

scraped_article_meta = get_all_articles_across_pages(max_pages=5)
scraped_article_meta_with_extra = add_articles_metadata(scraped_article_meta)
save_new_metadata(scraped_article_meta_with_extra)
print("Done scraping and saving article metadata.")








