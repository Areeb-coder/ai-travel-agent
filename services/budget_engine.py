from services.llm_client import generate_itinerary


def estimate_budget(destination: str, num_days: int, num_travelers: int, pref: str = "mid") -> dict:
    """
    Estimates a budget using LLM heuristics backed by general travel data.
    """
    system_prompt = """You are a travel budget estimator.
Provide a realistic daily expense estimate in USD for 1 person visiting the given destination.
Return your answer purely as JSON:
{
    "hotel_per_night": 100,
    "food_per_day": 50,
    "transport_per_day": 20,
    "activities_per_day": 30,
    "currency": "USD"
}
Adjust based on the user's travel style (budget, mid, luxury)."""

    user_prompt = f"Destination: {destination}\nStyle: {pref}"
    
    try:
        daily = generate_itinerary(system_prompt, user_prompt)
        
        hotel = int(daily.get("hotel_per_night", 100))
        food = int(daily.get("food_per_day", 50))
        trans = int(daily.get("transport_per_day", 20))
        act = int(daily.get("activities_per_day", 30))
        
        # Calculate
        # Hotel is often shared or one room for 2 people, but let's do simple naive per room
        rooms_needed = max(1, num_travelers // 2 + (num_travelers % 2))
        total_hotel = hotel * rooms_needed * num_days
        total_food = food * num_travelers * num_days
        total_trans = trans * num_travelers * num_days
        total_act = act * num_travelers * num_days
        
        overall = total_hotel + total_food + total_trans + total_act
        
        return {
            "breakdown": {
                "hotel_total": total_hotel,
                "food_total": total_food,
                "transport_total": total_trans,
                "activities_total": total_act
            },
            "daily_per_person": {
                "hotel_per_night": hotel,
                "food": food,
                "transport": trans,
                "activities": act
            },
            "total_estimated_budget": overall,
            "currency": daily.get("currency", "USD")
        }
    except Exception as e:
        print(f"Budget LLM error: {e}")
        return {
            "error": str(e),
            "total_estimated_budget": 0
        }
