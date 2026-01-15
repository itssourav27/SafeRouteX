"""
Authoritative district data for Jammu & Kashmir
"""

from typing import Dict, List, Tuple

# Ordered list matters for UI consistency
DISTRICT_NAMES: List[str] = [
    "Anantnag",
    "Bandipora",
    "Baramulla",
    "Budgam",
    "Ganderbal",
    "Kupwara",
    "Pulwama",
    "Shopian",
    "Kulgam",
    "Srinagar",
    "Jammu",
    "Udhampur",
    "Kathua",
    "Rajouri",
    "Poonch",
    "Reasi",
    "Doda",
    "Ramban",
    "Kishtwar",
]

# Fallback district center coordinates (lat, lon)
FALLBACK_COORDINATES: Dict[str, Tuple[float, float]] = {
    "Anantnag": (33.7327, 75.1487),
    "Bandipora": (34.4173, 74.6430),
    "Baramulla": (34.2095, 74.3482),
    "Budgam": (34.0159, 74.7644),
    "Ganderbal": (34.2294, 74.7748),
    "Kupwara": (34.5265, 74.2546),
    "Pulwama": (33.8740, 74.8994),
    "Shopian": (33.7171, 74.8346),
    "Kulgam": (33.6390, 75.0194),
    "Srinagar": (34.0837, 74.7973),
    "Jammu": (32.7266, 74.8570),
    "Udhampur": (32.9244, 75.1357),
    "Kathua": (32.3690, 75.5250),
    "Rajouri": (33.3720, 74.3152),
    "Poonch": (33.7730, 74.0923),
    "Reasi": (33.0899, 74.8293),
    "Doda": (33.1453, 75.5456),
    "Ramban": (33.2425, 75.2441),
    "Kishtwar": (33.3139, 75.7652),
}


def get_all_districts() -> List[str]:
    """Return ordered list of district names"""
    return DISTRICT_NAMES.copy()


def get_fallback_coord(district: str):
    """Return fallback coordinate if available"""
    return FALLBACK_COORDINATES.get(district)
