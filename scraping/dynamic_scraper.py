from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from config import Config

def fetch_dynamic_page(url: str) -> str:
    """
    Fetches the HTML of a page using a headless Selenium Chrome instance.
    Wait times or expected elements could be added here if needed.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(f"user-agent={Config.SCRAPER_USER_AGENT}")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = None
    try:
        # Install or find the chromedriver
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # We can implement a longer explicit wait if we knew the page logic, but an implicit is okay
        driver.implicitly_wait(Config.SCRAPER_TIMEOUT)
        
        driver.get(url)
        return driver.page_source
    finally:
        if driver:
            driver.quit()

def extract_data_from_dynamic_html(html: str) -> str:
    """
    Extracts text from the fully rendered HTML using BeautifulSoup.
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    # Remove clutter
    for block in soup(['script', 'style', 'noscript', 'meta']):
        block.decompose()

    text = soup.get_text(separator=' ', strip=True)
    return text
