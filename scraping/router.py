from .static_scraper import fetch_static_page, extract_data_from_static_html
from .dynamic_scraper import fetch_dynamic_page, extract_data_from_dynamic_html
from config import Config

def scrape_page(url: str, force_dynamic: bool = False) -> str:
    """
    Scrapes a target URL and returns text content.
    If `force_dynamic` is passed or if static scraping fails to yield much content,
    it falls back to dynamic (Selenium) scraping.
    """
    if force_dynamic and Config.SCRAPER_ENABLE_SELENIUM:
        html = fetch_dynamic_page(url)
        return extract_data_from_dynamic_html(html)
        
    # Attempt static scraping first
    try:
        html = fetch_static_page(url)
        text = extract_data_from_static_html(html)
        
        # If the extracted text is suspiciously short, it might be heavily JS rendered
        if len(text) < 200 and Config.SCRAPER_ENABLE_SELENIUM:
            print(f"[Scraper] Fallback to dynamic scraping for {url} due to low text yield.")
            html = fetch_dynamic_page(url)
            text = extract_data_from_dynamic_html(html)
            
        return text
    except Exception as e:
        print(f"[Scraper] Error scraping {url}: {e}")
        return ""
