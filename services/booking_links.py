import urllib.parse
from datetime import datetime, timedelta

def get_booking_links(origin: str, destination: str, num_days: int) -> dict:
    """
    Generates booking links using query parameters.
    Since we don't have exact dates, we can generate a generic template or a future date.
    """
    # Assuming travel starts 30 days from now
    start_date = datetime.now() + timedelta(days=30)
    end_date = start_date + timedelta(days=num_days)
    
    s_date_str = start_date.strftime("%Y-%m-%d")
    e_date_str = end_date.strftime("%Y-%m-%d")
    
    origin_q = urllib.parse.quote(origin) if origin else ""
    dest_q = urllib.parse.quote(destination)
    
    links = {
        "google_flights": f"https://www.google.com/travel/flights?q=Flights%20to%20{dest_q}%20from%20{origin_q}%20on%20{s_date_str}%20through%20{e_date_str}",
        "booking_com": f"https://www.booking.com/searchresults.html?ss={dest_q}&checkin={s_date_str}&checkout={e_date_str}",
        "skyscanner": f"https://www.skyscanner.com/transport/flights/{origin_q}/{dest_q}/{s_date_str}/{e_date_str}/",
    }
    
    return links
