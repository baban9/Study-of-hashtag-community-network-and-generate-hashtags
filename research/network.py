"""Build weighted hashtag co-occurrence graphs."""

from __future__ import annotations

import pandas as pd
import networkx as nx

from research.config import MIN_EDGE_WEIGHT


def build_weighted_graph(edges_df: pd.DataFrame, min_weight: int = MIN_EDGE_WEIGHT) -> nx.Graph:
    """Aggregate pairwise co-occurrences into a weighted undirected graph."""
    grouped = (
        edges_df.groupby(["left", "right"], as_index=False)
        .agg(weight=("pair_count", "max"), avg_likes=("likes", "mean"), post_count=("post_id", "nunique"))
    )
    grouped = grouped[grouped["weight"] >= min_weight]

    graph = nx.Graph()
    for _, row in grouped.iterrows():
        graph.add_edge(
            row["left"],
            row["right"],
            weight=int(row["weight"]),
            avg_likes=float(row["avg_likes"]),
            post_count=int(row["post_count"]),
        )
    return graph


def graph_summary(graph: nx.Graph) -> dict:
    if graph.number_of_nodes() == 0:
        return {
            "nodes": 0,
            "edges": 0,
            "density": 0.0,
            "avg_degree": 0.0,
            "components": 0,
        }
    degrees = [deg for _, deg in graph.degree()]
    return {
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "density": float(nx.density(graph)),
        "avg_degree": float(sum(degrees) / len(degrees)),
        "components": nx.number_connected_components(graph),
    }
