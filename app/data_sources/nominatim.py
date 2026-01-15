"""
Nominatim (OpenStreetMap) geocoding client
"""

import requests
from ratelimit import limits, sleep_and_retry

from app.config.settings import NOMINATIM_URL, NOMINATIM_CALLS_PER_SEC
from app.utils.cache import coord_cache
from app.data.districts import get_fallback_coord


@sleep_and_retry
@limits(calls=NOMINATIM_CALLS_PER_SEC, period=1)
def geocode_district(district: str):
    """
    Resolve district name to (lat, lon) using Nominatim
    """
    if coord_cache.exists(district):
        return coord_cache.get(district)

    params = {
        "q": f"{district}, Jammu and Kashmir, India",
        "format": "json",
        "limit": 1,
    }

    headers = {
        "User-Agent": "JK-Evacuation-System/1.0 (contact@example.com)"
    }

    try:
        resp = requests.get(
            NOMINATIM_URL,
            params=params,
            headers=headers,
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()

        if data:
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            coord_cache.set(district, (lat, lon))
            return lat, lon

    except Exception:
        pass

    # Fallback if API fails
    fallback = get_fallback_coord(district)
    if fallback:
        coord_cache.set(district, fallback)
        return fallback

    return None, None
