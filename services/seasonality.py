import json
from services.llm_client import generate_itinerary
from services.open_data import fetch_wikivoyage_page
from scraping.static_scraper import extract_data_from_static_html

def get_best_seasons_for_destination(destination: str) -> dict:
    """
    Determines best seasons for a destination using Wikivoyage data and LLM parsing.
    """
    html = fetch_wikivoyage_page(destination)
    if not html:
        return {"error": "Could not fetch data for this destination."}
        
    text_content = extract_data_from_static_html(html)
    # Give the LLM a chunk of the text (up to 4000 characters to process quickly)
    content_sample = text_content[:4000]

    system_prompt = """You are a seasonality and climate expert for travel.
Given text from a travel guide, determine the best time to visit this destination.
Return your answer strictly as JSON with this schema format:
{
    "best_months": ["Month", "Month"],
    "decent_months": ["Month", "Month"],
    "avoid_months": ["Month"],
    "rationale": "A short sentence explaining why."
}
If there's not enough data, use your general knowledge of the world.
"""
    user_prompt = f"Destination: {destination}\n\nContext:\n{content_sample}"
    
    try:
        result = generate_itinerary(system_prompt, user_prompt)
        return result
    except Exception as e:
        print(f"Seasonality LLM error: {e}")
        return {
            "best_months": [], "decent_months": [], "avoid_months": [],
            "rationale": "Data not available at the moment."
        }

def rate_destination_for_dates(destination: str, dates: str) -> dict:
    """
    Based on best seasons, rates the destination for the given dates.
    """
    seasons = get_best_seasons_for_destination(destination)
    # Simple logic (can be LLM based too, but structured is better)
    return {
        "season_info": seasons,
        "note": f"Check the seasons above to see if it matches your dates: {dates}"
    }
