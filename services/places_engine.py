import urllib.parse
from services.llm_client import generate_itinerary
from services.open_data import geocode_place


def get_top_places(destination: str, limit: int = 5) -> list:
    """
    Identifies top attractions for a destination and attaches map URLs.
    """
    system_prompt = f"""You are a travel expert. List the top {limit} attractions/places to visit in the given destination.
Return your answer strictly as a JSON array of objects with schema:
[
  {{"name": "Place Name", "description": "Short summary", "category": "nature/culture/food/etc"}}
]
"""
    try:
        places = generate_itinerary(system_prompt, f"Destination: {destination}")
        if not isinstance(places, list):
            places = places.get("places", []) or []
            
        enhanced_places = []
        for p in places[:limit]:
            name = p.get("name")
            if not name: continue
            
            geo = geocode_place(name, destination)
            if geo:
                p["lat"] = geo["lat"]
                p["lon"] = geo["lon"]
                p["osm_url"] = f"https://www.openstreetmap.org/?mlat={geo['lat']}&mlon={geo['lon']}#map=16/{geo['lat']}/{geo['lon']}"
            else:
                p["osm_url"] = f"https://www.openstreetmap.org/search?query={urllib.parse.quote(name + ' ' + destination)}"
                
            p["google_maps_url"] = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(name + ' ' + destination)}"
            enhanced_places.append(p)
            
        return enhanced_places
    except Exception as e:
        print(f"Places engine error: {e}")
        return []
