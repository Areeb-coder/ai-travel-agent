import requests
from bs4 import BeautifulSoup
from config import Config

def fetch_static_page(url: str) -> str:
    """
    Fetches the HTML of a static page using basic requests.
    """
    headers = {
        "User-Agent": Config.SCRAPER_USER_AGENT
    }
    
    response = requests.get(url, headers=headers, timeout=Config.SCRAPER_TIMEOUT)
    response.raise_for_status()
    
    return response.text

def extract_data_from_static_html(html: str) -> str:
    """
    Extracts purely textual data from the static HTML using BeautifulSoup.
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    # Remove script and style elements
    for script_or_style in soup(['script', 'style', 'header', 'footer', 'nav']):
        script_or_style.decompose()

    text = soup.get_text(separator=' ', strip=True)
    return text
