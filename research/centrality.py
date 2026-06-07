"""Centrality metrics and correlation with engagement."""

from __future__ import annotations

import networkx as nx
import numpy as np
import pandas as pd
from scipy import stats

from research.config import CORRELATION_CSV, HASHTAG_METRICS_CSV


def compute_hashtag_metrics(graph: nx.Graph, partition: dict[str, int], edges_df: pd.DataFrame) -> pd.DataFrame:
    if graph.number_of_nodes() == 0:
        return pd.DataFrame()

    degree = dict(graph.degree(weight="weight"))
    betweenness = nx.betweenness_centrality(graph, weight="weight")
    eigenvector = nx.eigenvector_centrality_numpy(graph, weight="weight")

    likes_by_tag = {}
    for tag_col in ("left", "right"):
        grouped = edges_df.groupby(tag_col)["likes"].mean()
        for tag, value in grouped.items():
            likes_by_tag.setdefault(tag, []).append(value)
    avg_likes = {tag: float(np.mean(values)) for tag, values in likes_by_tag.items()}

    rows = []
    for node in graph.nodes():
        rows.append(
            {
                "hashtag": node,
                "community_id": partition.get(node, -1),
                "weighted_degree": degree.get(node, 0.0),
                "betweenness": betweenness.get(node, 0.0),
                "eigenvector": float(eigenvector.get(node, 0.0)),
                "avg_likes": avg_likes.get(node, np.nan),
            }
        )

    metrics = pd.DataFrame(rows).sort_values("weighted_degree", ascending=False)
    HASHTAG_METRICS_CSV.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(HASHTAG_METRICS_CSV, index=False)
    return metrics


def centrality_like_correlations(metrics_df: pd.DataFrame) -> pd.DataFrame:
    if metrics_df.empty:
        return pd.DataFrame(columns=["metric", "pearson_r", "pearson_p", "spearman_r", "spearman_p"])

    rows = []
    for metric in ("weighted_degree", "betweenness", "eigenvector"):
        subset = metrics_df[[metric, "avg_likes"]].dropna()
        if len(subset) < 3:
            continue
        pearson_r, pearson_p = stats.pearsonr(subset[metric], subset["avg_likes"])
        spearman_r, spearman_p = stats.spearmanr(subset[metric], subset["avg_likes"])
        rows.append(
            {
                "metric": metric,
                "pearson_r": float(pearson_r),
                "pearson_p": float(pearson_p),
                "spearman_r": float(spearman_r),
                "spearman_p": float(spearman_p),
            }
        )

    correlations = pd.DataFrame(rows)
    CORRELATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    correlations.to_csv(CORRELATION_CSV, index=False)
    return correlations
