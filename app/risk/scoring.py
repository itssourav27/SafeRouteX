"""
Risk scoring logic for evacuation routing

IMPORTANT:
- This is a heuristic risk estimator, not a predictive model.
- Scores are designed for relative comparison, not absolute danger levels.
"""

from typing import Dict

from app.config.settings import (
    RAIN_BLOCK_MM,
    RAIN_HIGH_MM,
    RAIN_MEDIUM_MM,
    EQ_HIGH_MAG,
    EQ_MEDIUM_MAG,
    EQ_LOW_MAG,
)


def rainfall_risk_score(precip_mm: float) -> float:
    """
    Risk contribution from rainfall in last 24h
    """
    if precip_mm >= RAIN_BLOCK_MM:
        return 30.0
    if precip_mm >= RAIN_HIGH_MM:
        return 18.0
    if precip_mm >= RAIN_MEDIUM_MM:
        return 8.0
    if precip_mm >= 20:
        return 3.0
    return 0.0


def earthquake_risk_score(max_magnitude: float) -> float:
    """
    Risk contribution from nearby seismic activity
    """
    if max_magnitude >= EQ_HIGH_MAG:
        return 30.0
    if max_magnitude >= EQ_MEDIUM_MAG:
        return 18.0
    if max_magnitude >= EQ_LOW_MAG:
        return 8.0
    return 0.0


def contextual_multiplier(disaster_type: str) -> float:
    """
    Amplify risk based on known disaster context
    """
    disaster_type = (disaster_type or "").lower()

    if "flood" in disaster_type:
        return 1.2
    if "landslide" in disaster_type:
        return 1.1
    return 1.0


def total_risk_score(node_attrs: Dict) -> float:
    """
    Compute total risk score for a district node
    """
    precip = float(node_attrs.get("precipitation_24h", 0.0))
    quake_mag = float(node_attrs.get("quake_mag", 0.0))
    disaster_type = node_attrs.get("disaster_type", "")

    base_score = (
        rainfall_risk_score(precip)
        + earthquake_risk_score(quake_mag)
    )

    return base_score * contextual_multiplier(disaster_type)


def is_blocked(node_attrs: Dict) -> bool:
    """
    Determine if a district should be treated as blocked
    """
    precip = float(node_attrs.get("precipitation_24h", 0.0))
    return precip >= RAIN_BLOCK_MM
