import requests
import urllib.parse
from config import Config

def geocode_place(name: str, country: str = None) -> dict:
    """
    Use OpenStreetMap Nominatim to get lat/lon for a place.
    Provides free geocoding.
    """
    query = name
    if country:
        query += f", {country}"
        
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(query)}&format=json&limit=1"
    headers = {
        "User-Agent": Config.SCRAPER_USER_AGENT
    }
    try:
        response = requests.get(url, headers=headers, timeout=Config.SCRAPER_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        if data and len(data) > 0:
            return {
                "lat": data[0].get("lat"),
                "lon": data[0].get("lon"),
                "display_name": data[0].get("display_name"),
            }
        return None
    except Exception as e:
        print(f"Geocoding error for {name}: {e}")
        return None

def fetch_wikivoyage_page(destination: str) -> str:
    """
    Fetches the raw HTML from Wikivoyage for a given destination.
    """
    url = f"https://en.wikivoyage.org/wiki/{urllib.parse.quote(destination)}"
    headers = {
        "User-Agent": Config.SCRAPER_USER_AGENT
    }
    try:
        response = requests.get(url, headers=headers, timeout=Config.SCRAPER_TIMEOUT)
        if response.status_code == 200:
            return response.text
        return None
    except Exception as e:
        print(f"Wikivoyage fetch error for {destination}: {e}")
        return None
