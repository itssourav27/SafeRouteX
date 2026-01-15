"""
District graph construction
"""

import networkx as nx
from typing import Dict, Tuple

from app.data.districts import get_all_districts
from app.data_sources.nominatim import geocode_district
from app.data_sources.weather import fetch_precipitation_24h
from app.data_sources.earthquakes import max_magnitude_near
from app.utils.geo import haversine_km

MAX_EDGE_DISTANCE_KM = 120.0  # adjacency threshold


def build_district_graph() -> Tuple[nx.Graph, Dict[str, Tuple[float, float]]]:
    """
    Build graph with districts as nodes and edges based on geographic proximity
    """
    G = nx.Graph()
    positions: Dict[str, Tuple[float, float]] = {}

    # --------------------
    # Add nodes
    # --------------------
    for district in get_all_districts():
        lat, lon = geocode_district(district)
        if lat is None:
            continue

        positions[district] = (lat, lon)
        G.add_node(
            district,
            lat=lat,
            lon=lon,
            precipitation_24h=0.0,
            quake_mag=0.0,
            disaster_type="",
            blocked=False,
        )

    # --------------------
    # Add edges (distance-limited)
    # --------------------
    nodes = list(G.nodes)
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            a, b = nodes[i], nodes[j]
            la, lo = positions[a]
            lb, lo2 = positions[b]

            dist = haversine_km(la, lo, lb, lo2)
            if dist <= MAX_EDGE_DISTANCE_KM:
                G.add_edge(
                    a,
                    b,
                    base_distance_km=dist,
                    weight=dist,
                )

    return G, positions


def enrich_graph_with_live_data(G: nx.Graph) -> nx.Graph:
    """
    Attach live weather & earthquake data to nodes
    """
    for node, attrs in G.nodes(data=True):
        lat, lon = attrs["lat"], attrs["lon"]

        try:
            attrs["precipitation_24h"] = fetch_precipitation_24h(lat, lon)
        except Exception:
            attrs["precipitation_24h"] = 0.0

        try:
            attrs["quake_mag"] = max_magnitude_near(lat, lon)
        except Exception:
            attrs["quake_mag"] = 0.0

    return G

