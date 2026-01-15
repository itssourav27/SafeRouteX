"""
Weather data client (Open-Meteo)
"""

import requests
from ratelimit import limits, sleep_and_retry

from app.config.settings import OPEN_METEO_URL, WEATHER_CALLS_PER_SEC
from app.utils.cache import weather_cache


@sleep_and_retry
@limits(calls=WEATHER_CALLS_PER_SEC, period=1)
def fetch_precipitation_24h(lat: float, lon: float) -> float:
    """
    Return total precipitation (mm) over last 24 hours
    """
    key = (round(lat, 5), round(lon, 5))

    if weather_cache.exists(key):
        return weather_cache.get(key)

    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "precipitation",
        "past_days": 1,
        "timezone": "UTC",
    }

    try:
        resp = requests.get(OPEN_METEO_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        hourly = data.get("hourly", {}).get("precipitation", [])
        total = float(sum(hourly)) if isinstance(hourly, list) else 0.0

        weather_cache.set(key, total)
        return total

    except Exception:
        weather_cache.set(key, 0.0)
        return 0.0
