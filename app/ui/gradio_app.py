"""
Gradio frontend for J&K Evacuation System
"""

import json
import gradio as gr

from app.data.districts import get_all_districts
from app.graph.builder import build_district_graph, enrich_graph_with_live_data
from app.graph.filters import apply_risk_weights
from app.routing.paths import find_k_routes
from app.visualization.map import build_evacuation_map
from app.visualization.utils import route_to_latlon
from app.data_sources.safehouses import fetch_safehouses
from app.utils.geo import haversine_km


def compute_evacuation(
    start: str,
    end: str,
    blocked_disasters: list,
    k_routes: int,
):
    # --------------------
    # Build backend engine
    # --------------------
    G, positions = build_district_graph()
    G = enrich_graph_with_live_data(G)
    H = apply_risk_weights(
        G,
        blocked_disaster_types=blocked_disasters,
        start=start,
        end=end,
    )

    # --------------------
    # Routing
    # --------------------
    routes = find_k_routes(H, start, end, k=k_routes)
    if not routes:
        return "No evacuation route found.", "<p>No map</p>"

    chosen = routes[0]
    route_coords = route_to_latlon(chosen["path"], positions)

    # --------------------
    # Safehouses near destination
    # --------------------
    lat_end, lon_end = positions[end]
    safehouses = fetch_safehouses()

    ranked = []
    for sh in safehouses:
        d = haversine_km(lat_end, lon_end, sh["lat"], sh["lon"])
        ranked.append({
            "safehouse": sh,
            "distance_km": d,
            "route_coords": [(lat_end, lon_end), (sh["lat"], sh["lon"])],
        })

    ranked.sort(key=lambda x: x["distance_km"])
    top_safehouses = ranked[:3]

    # --------------------
    # Visualization
    # --------------------
    map_html = build_evacuation_map(
        route_coords=route_coords,
        start=start,
        end=end,
        positions=positions,
        safehouses=top_safehouses,
    )

    # --------------------
    # Summary
    # --------------------
    summary = {
        "route": " → ".join(chosen["path"]),
        "total_cost": chosen["cost"],
        "risk_nodes": chosen["risk_nodes"],
        "top_safehouses": [
            {
                "name": s["safehouse"]["name"],
                "distance_km": round(s["distance_km"], 2),
                "type": s["safehouse"].get("type"),
            }
            for s in top_safehouses
        ],
    }

    return json.dumps(summary, indent=2), map_html


def launch_app():
    districts = get_all_districts()

    with gr.Blocks(title="J&K Evacuation Routing System") as demo:
        gr.Markdown("# 🚨 J&K Disaster-Aware Evacuation Routing")

        with gr.Row():
            start_dd = gr.Dropdown(
                label="📍 Start District",
                choices=districts,
                value=districts[0],
            )
            end_dd = gr.Dropdown(
                label="🏁 Destination District",
                choices=districts,
                value=districts[1],
            )

        with gr.Row():
            blocked = gr.CheckboxGroup(
                label="Treat these disaster types as blocked",
                choices=["flood", "landslide", "earthquake"],
            )
            k_routes = gr.Slider(
                minimum=1,
                maximum=5,
                step=1,
                value=3,
                label="Top-k routes",
            )

        run_btn = gr.Button("🧭 Find Evacuation Route")

        out_summary = gr.Textbox(
            label="Route Summary (JSON)",
            lines=8,
        )
        out_map = gr.HTML(label="Evacuation Map")

        run_btn.click(
            compute_evacuation,
            inputs=[start_dd, end_dd, blocked, k_routes],
            outputs=[out_summary, out_map],
        )

    demo.launch(server_name="0.0.0.0",server_port=7860)
