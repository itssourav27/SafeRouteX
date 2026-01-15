"""
Visualization helpers
"""

from typing import List, Tuple, Dict


def route_to_latlon(
    route: List[str],
    positions: Dict[str, Tuple[float, float]],
) -> List[Tuple[float, float]]:
    """
    Convert route (district names) to lat/lon polyline
    """
    coords: List[Tuple[float, float]] = []

    for node in route:
        if node in positions:
            coords.append(positions[node])

    return coords
