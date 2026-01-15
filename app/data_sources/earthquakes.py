"""
USGS Earthquake data client
"""

import requests
from typing import List, Dict

from app.config.settings import USGS_EQ_URL
from app.utils.cache import earthquake_cache
from app.utils.geo import haversine_km


def fetch_recent_earthquakes() -> List[Dict]:
    """
    Fetch recent earthquake events from USGS
    """
    if earthquake_cache.exists("usgs"):
        return earthquake_cache.get("usgs")

    try:
        resp = requests.get(USGS_EQ_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        quakes = []
        for f in data.get("features", []):
            props = f.get("properties", {})
            geom = f.get("geometry", {})
            coords = geom.get("coordinates", [])

            if len(coords) >= 2:
                quakes.append({
                    "mag": props.get("mag"),
                    "lat": coords[1],
                    "lon": coords[0],
                })

        earthquake_cache.set("usgs", quakes)
        return quakes

    except Exception:
        earthquake_cache.set("usgs", [])
        return []


def max_magnitude_near(lat: float, lon: float, radius_km: float = 150.0) -> float:
    """
    Return maximum earthquake magnitude within radius
    """
    quakes = fetch_recent_earthquakes()
    max_mag = 0.0

    for q in quakes:
        if q["mag"] is None:
            continue
        d = haversine_km(lat, lon, q["lat"], q["lon"])
        if d <= radius_km:
            max_mag = max(max_mag, float(q["mag"]))

    return max_mag
