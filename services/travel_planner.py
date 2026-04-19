import json
from services.llm_client import generate_completion
from services.seasonality import rate_destination_for_dates
from services.budget_engine import estimate_budget
from services.places_engine import get_top_places
from services.booking_links import get_booking_links

def plan_trip(request_data: dict) -> dict:
    """
    Orchestrates the travel plan by combining modular engines and an LLM call.
    """
    destination = request_data.get("destination", "Unknown Destination")
    origin = request_data.get("origin", "")
    num_days = request_data.get("num_days", 7)
    travelers = request_data.get("travelers", 1)
    preferences = request_data.get("preferences", "mid")
    travel_style = request_data.get("travel_style", "any")
    dates = request_data.get("dates", "any time")
    
    # 1. Seasonality & Climate
    season_info = rate_destination_for_dates(destination, dates)
    
    # 2. Budget Estimation
    budget_info = estimate_budget(destination, num_days, travelers, preferences)
    
    # 3. Places & Map Links
    top_places = get_top_places(destination, limit=8)
    
    # 4. Booking Links
    booking_links = get_booking_links(origin, destination, num_days)
    
    # 5. Bring it all together with the LLM
    system_prompt = """You are a senior travel planner. Given context data, form a day-by-day structured itinerary.
    You MUST return the itinerary purely as a JSON object, adhering STRICTLY to the following format:
    {
       "destination": "Name of destination",
       "duration_days": 7,
       "itinerary": [
           {
               "day": 1,
               "title": "Arrival and Exploration",
               "activities": ["Activity 1", "Activity 2"]
           }
       ],
       "trip_theme_summary": "A 1-sentence catchy description"
    }
    """
    
    user_prompt_parts = [
        f"Destination: {destination}",
        f"Duration: {num_days} days",
        f"Travel Style: {travel_style}",
        f"Top Places Available (integrate these into the itinerary): {', '.join([p.get('name', '') for p in top_places])}"
    ]
        
    user_prompt = "\n".join(user_prompt_parts)
    
    assistant_text = generate_completion(
        messages=[{"role": "user", "content": user_prompt}],
        system_prompt=system_prompt,
    )
    
    if "```json" in assistant_text:
        assistant_text = assistant_text.split("```json")[1].split("```")[0].strip()
    elif "```" in assistant_text:
        assistant_text = assistant_text.split("```")[1].split("```")[0].strip()

    structured_itinerary = json.loads(assistant_text)
    
    # Combine everything into the final response
    return {
        "itinerary": structured_itinerary.get("itinerary", []),
        "trip_theme_summary": structured_itinerary.get("trip_theme_summary", ""),
        "destination": destination,
        "duration_days": num_days,
        "seasonality": season_info,
        "budget": budget_info,
        "places": top_places,
        "booking_links": booking_links
    }
