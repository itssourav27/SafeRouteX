"""
Global configuration and constants for the J&K Evacuation System
"""

# --------------------
# Geography
# --------------------
JK_BBOX = (32.0, 73.4, 35.5, 76.6)

# --------------------
# External API Endpoints
# --------------------
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
USGS_EQ_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"

# --------------------
# Rate Limits
# --------------------
NOMINATIM_CALLS_PER_SEC = 1
WEATHER_CALLS_PER_SEC = 5
OVERPASS_CALLS_PER_SEC = 1

# --------------------
# Risk Thresholds (heuristic)
# --------------------
RAIN_BLOCK_MM = 200
RAIN_HIGH_MM = 100
RAIN_MEDIUM_MM = 50

EQ_HIGH_MAG = 6.0
EQ_MEDIUM_MAG = 5.0
EQ_LOW_MAG = 4.0

# --------------------
# Routing
# --------------------
DEFAULT_MAX_ROUTE_K = 3
