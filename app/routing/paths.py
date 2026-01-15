"""
Evacuation routing algorithms
"""

import networkx as nx
from typing import List, Dict

from app.risk.scoring import total_risk_score


def find_k_routes(
    G: nx.Graph,
    start: str,
    end: str,
    k: int = 3,
) -> List[Dict]:
    """
    Find top-k evacuation routes using weighted shortest paths
    """
    routes: List[Dict] = []

    if start not in G or end not in G:
        return routes

    try:
        paths = nx.shortest_simple_paths(G, start, end, weight="weight")

        for path in paths:
            cost = float(nx.path_weight(G, path, weight="weight"))

            # Count risky districts in path
            risk_nodes = sum(
                1 for n in path
                if total_risk_score(G.nodes[n]) > 5.0
            )

            routes.append({
                "path": path,
                "cost": round(cost, 2),
                "risk_nodes": risk_nodes,
            })

            if len(routes) >= k:
                break

    except nx.NetworkXNoPath:
        return routes

    return routes
