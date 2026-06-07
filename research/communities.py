"""Community detection on hashtag co-occurrence networks."""

from __future__ import annotations

from collections import Counter

import community as community_louvain
import networkx as nx
import pandas as pd

from research.config import COMMUNITY_SUMMARY_CSV


def detect_communities(graph: nx.Graph) -> dict[str, int]:
    if graph.number_of_nodes() == 0:
        return {}
    return community_louvain.best_partition(graph, weight="weight")


def modularity_score(graph: nx.Graph, partition: dict[str, int]) -> float:
    if graph.number_of_edges() == 0:
        return 0.0
    return float(community_louvain.modularity(partition, graph, weight="weight"))


def community_summary(graph: nx.Graph, partition: dict[str, int]) -> pd.DataFrame:
    rows = []
    community_sizes = Counter(partition.values())
    for node in graph.nodes():
        community_id = partition.get(node, -1)
        degree = graph.degree(node, weight="weight")
        rows.append(
            {
                "hashtag": node,
                "community_id": community_id,
                "community_size": community_sizes[community_id],
                "weighted_degree": degree,
            }
        )
    summary = pd.DataFrame(rows).sort_values(["community_id", "weighted_degree"], ascending=[True, False])
    COMMUNITY_SUMMARY_CSV.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(COMMUNITY_SUMMARY_CSV, index=False)
    return summary


def aggregate_community_stats(summary_df: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        summary_df.groupby("community_id")
        .agg(
            member_count=("hashtag", "count"),
            avg_weighted_degree=("weighted_degree", "mean"),
            top_hashtag=("hashtag", lambda s: s.iloc[0]),
        )
        .reset_index()
    )
    return grouped.sort_values("member_count", ascending=False)
