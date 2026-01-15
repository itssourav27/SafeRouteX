"""
Graph filtering & risk-aware edge weighting
"""

import networkx as nx
from typing import List

from app.risk.scoring import total_risk_score, is_blocked


def apply_risk_weights(
    G: nx.Graph,
    blocked_disaster_types: List[str] | None = None,
    remove_blocked_nodes: bool = False,
    start: str | None = None,
    end: str | None = None,
) -> nx.Graph:
    """
    Apply risk-based penalties to edges and optionally remove blocked nodes
    """
    if blocked_disaster_types is None:
        blocked_disaster_types = []

    H = G.copy()

    # --------------------
    # Remove blocked nodes
    # --------------------
    if remove_blocked_nodes:
        for node, attrs in list(H.nodes(data=True)):
            if is_blocked(attrs) and node not in {start, end}:
                H.remove_node(node)

    # --------------------
    # Reweight edges
    # --------------------
    for u, v, attrs in H.edges(data=True):
        ru = total_risk_score(H.nodes[u])
        rv = total_risk_score(H.nodes[v])

        penalty = 0.1 * (ru + rv)

        if H.nodes[u].get("disaster_type") in blocked_disaster_types:
            penalty += 25.0
        if H.nodes[v].get("disaster_type") in blocked_disaster_types:
            penalty += 25.0

        attrs["weight"] = attrs["base_distance_km"] + penalty

    return H
