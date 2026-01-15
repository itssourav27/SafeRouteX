"""
FastAPI wrapper for J&K Evacuation Engine
Thin API layer – all logic lives in app/
"""

from fastapi import FastAPI, Query
from typing import List, Optional

from app.data.districts import get_all_districts
from app.graph.builder import build_district_graph, enrich_graph_with_live_data
from app.graph.filters import apply_risk_weights
from app.routing.paths import find_k_routes
from app.visualization.utils import route_to_latlon
from app.data_sources.safehouses import fetch_safehouses
from app.utils.geo import haversine_km
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict to Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI(
    title="J&K Evacuation Routing API",
    description="Risk-aware evacuation routing backend",
    version="1.0.0",
)

# -------------------------
# Health check
# -------------------------
@app.get("/")
def health():
    return {"status": "ok"}

# -------------------------
# District list
# -------------------------
@app.get("/districts")
def get_districts():
    return {"districts": get_all_districts()}

# -------------------------
# Evacuation route
# -------------------------
@app.get("/route")
def compute_route(
    start: str,
    end: str,
    blocked: Optional[List[str]] = Query(default=[]),
    k: int = 3,
):
    G, positions = build_district_graph()
    G = enrich_graph_with_live_data(G)
    H = apply_risk_weights(
        G,
        blocked_disaster_types=blocked,
        start=start,
        end=end,
    )

    routes = find_k_routes(H, start, end, k=k)
    if not routes:
        return {"error": "No route found"}

    chosen = routes[0]
    route_coords = route_to_latlon(chosen["path"], positions)

    return {
        "route": chosen["path"],
        "cost": chosen["cost"],
        "risk_nodes": chosen["risk_nodes"],
        "coordinates": route_coords,
    }

# -------------------------
# Safehouses near district
# -------------------------
@app.get("/safehouses")
def safehouses_near(district: str, k: int = 3):
    G, positions = build_district_graph()
    lat, lon = positions.get(district, (None, None))
    if lat is None:
        return {"error": "Invalid district"}

    safehouses = fetch_safehouses()
    ranked = []

    for sh in safehouses:
        d = haversine_km(lat, lon, sh["lat"], sh["lon"])
        ranked.append({
            "name": sh["name"],
            "type": sh.get("type"),
            "lat": sh["lat"],
            "lon": sh["lon"],
            "distance_km": round(d, 2),
        })

    ranked.sort(key=lambda x: x["distance_km"])
    return {"safehouses": ranked[:k]}

