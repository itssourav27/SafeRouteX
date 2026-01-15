"""
Fallback safehouse data for emergency use
Used only when Overpass API is unavailable
"""

from typing import List, Dict


FALLBACK_SAFEHOUSES: List[Dict] = [
    {
        "name": "Srinagar Emergency Shelter A",
        "aliases": ["Srinagar Safehouse"],
        "lat": 34.0850,
        "lon": 74.8000,
        "type": "shelter",
        "capacity": 200,
    },
    {
        "name": "Baramulla Emergency Shelter",
        "aliases": ["Baramulla Safehouse"],
        "lat": 34.2105,
        "lon": 74.3490,
        "type": "shelter",
        "capacity": 150,
    },
    {
        "name": "Anantnag Central Shelter",
        "aliases": ["Anantnag Safehouse"],
        "lat": 33.7335,
        "lon": 75.1500,
        "type": "shelter",
        "capacity": 180,
    },
]


def get_fallback_safehouses():
    """Return fallback safehouse list"""
    return FALLBACK_SAFEHOUSES.copy()
