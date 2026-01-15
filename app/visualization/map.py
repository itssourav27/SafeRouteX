"""
Map visualization utilities using Folium
"""

from typing import List, Dict, Tuple
import folium


def build_evacuation_map(
    route_coords: List[Tuple[float, float]],
    start: str,
    end: str,
    positions: Dict[str, Tuple[float, float]],
    safehouses: List[Dict] | None = None,
) -> str:
    """
    Render evacuation route and safehouses on an interactive map.
    Returns HTML iframe string.
    """

    if safehouses is None:
        safehouses = []

    # --------------------
    # Map center
    # --------------------
    center = positions.get(start, route_coords[0] if route_coords else (34.08, 74.8))
    m = folium.Map(
        location=center,
        zoom_start=8,
        control_scale=True,
        tiles="OpenStreetMap",
    )

    # --------------------
    # District markers
    # --------------------
    for district, (lat, lon) in positions.items():
        color = "blue"
        if district == start:
            color = "green"
        elif district == end:
            color = "purple"

        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color=color,
            fill=True,
            fill_opacity=0.8,
            tooltip=district,
        ).add_to(m)

    # --------------------
    # Evacuation route
    # --------------------
    if route_coords:
        folium.PolyLine(
            route_coords,
            color="green",
            weight=6,
            opacity=0.85,
            tooltip="Evacuation Route",
        ).add_to(m)

    # --------------------
    # Safehouse markers
    # --------------------
    for entry in safehouses:
        sh = entry.get("safehouse", {})
        dist = entry.get("distance_km", None)

        tooltip = f"{sh.get('name', 'Unknown')} ({sh.get('type', '')})"
        if dist is not None:
            tooltip += f"<br>Distance: {dist:.2f} km"

        folium.Marker(
            location=[sh["lat"], sh["lon"]],
            tooltip=tooltip,
            icon=folium.Icon(color="red", icon="home"),
        ).add_to(m)

        # Optional direct line to safehouse
        route = entry.get("route_coords")
        if route:
            folium.PolyLine(
                route,
                color="blue",
                weight=4,
                opacity=0.8,
                tooltip=f"To {sh.get('name')}",
            ).add_to(m)

    # --------------------
    # Convert to iframe
    # --------------------
    html = m.get_root().render()
    iframe = (
        '<iframe srcdoc="{}" style="width:100%; height:700px; border:none;"></iframe>'
        .format(html.replace('"', "&quot;"))
    )

    return iframe
