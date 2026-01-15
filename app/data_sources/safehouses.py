"""
Safehouse discovery via Overpass API (OpenStreetMap)
"""

import requests
from ratelimit import limits, sleep_and_retry

from app.config.settings import OVERPASS_URL, JK_BBOX, OVERPASS_CALLS_PER_SEC
from app.utils.cache import safehouse_cache
from app.utils.geo import haversine_km
from app.data.fallback_safehouses import get_fallback_safehouses


@sleep_and_retry
@limits(calls=OVERPASS_CALLS_PER_SEC, period=1)
def fetch_safehouses():
    """
    Fetch shelters, hospitals, police, fire stations from OSM
    """
    if safehouse_cache.exists("safehouses"):
        return safehouse_cache.get("safehouses")

    lat1, lon1, lat2, lon2 = JK_BBOX

    query = f"""
    [out:json][timeout:60];
    (
      node["amenity"~"hospital|police|fire_station|shelter"]({lat1},{lon1},{lat2},{lon2});
      node["emergency"="shelter"]({lat1},{lon1},{lat2},{lon2});
      way["amenity"~"hospital|police|fire_station|shelter"]({lat1},{lon1},{lat2},{lon2});
    );
    out center;
    """

    try:
        resp = requests.post(OVERPASS_URL, data={"data": query}, timeout=60)
        resp.raise_for_status()
        data = resp.json()

        points = []
        for el in data.get("elements", []):
            lat = el.get("lat") or el.get("center", {}).get("lat")
            lon = el.get("lon") or el.get("center", {}).get("lon")

            if lat is None or lon is None:
                continue

            tags = el.get("tags", {})
            points.append({
                "name": tags.get("name", "Unknown"),
                "lat": float(lat),
                "lon": float(lon),
                "type": tags.get("amenity") or tags.get("emergency", "shelter"),
            })

        # Deduplicate by proximity
        deduped = []
        for p in points:
            merged = False
            for q in deduped:
                if haversine_km(p["lat"], p["lon"], q["lat"], q["lon"]) < 0.25:
                    merged = True
                    break
            if not merged:
                deduped.append(p)

        safehouse_cache.set("safehouses", deduped)
        return deduped

    except Exception:
        fallback = get_fallback_safehouses()
        safehouse_cache.set("safehouses", fallback)
        return fallback
