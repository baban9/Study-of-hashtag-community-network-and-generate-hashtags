"""Save publication-quality figures to disk."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

from research.config import FIGURES_DIR


def _ensure_dir() -> Path:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    return FIGURES_DIR


def plot_community_network(graph: nx.Graph, partition: dict[str, int], output_name: str = "01_community_network.png") -> Path:
    output_path = _ensure_dir() / output_name
    plt.figure(figsize=(12, 8))
    if graph.number_of_nodes() == 0:
        plt.text(0.5, 0.5, "No nodes available", ha="center", va="center")
    else:
        pos = nx.spring_layout(graph, seed=42, weight="weight")
        colors = [partition.get(node, 0) for node in graph.nodes()]
        sizes = [300 + 40 * graph.degree(node, weight="weight") for node in graph.nodes()]
        nx.draw_networkx_nodes(graph, pos, node_color=colors, node_size=sizes, cmap=plt.cm.tab20, alpha=0.85)
        nx.draw_networkx_edges(graph, pos, alpha=0.25, width=0.8)
        labels = {node: node for node in graph.nodes() if graph.degree(node, weight="weight") >= np.percentile(list(dict(graph.degree(weight="weight")).values()), 60)}
        nx.draw_networkx_labels(graph, pos, labels=labels, font_size=8)
    plt.title("Hashtag Co-occurrence Network Colored by Detected Community")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close()
    return output_path


def plot_degree_distribution(graph: nx.Graph, output_name: str = "02_degree_distribution.png") -> Path:
    output_path = _ensure_dir() / output_name
    degrees = [deg for _, deg in graph.degree(weight="weight")]
    plt.figure(figsize=(8, 5))
    if degrees:
        plt.hist(degrees, bins=min(20, max(5, len(set(degrees)))), color="#4C72B0", edgecolor="white")
    plt.xlabel("Weighted Degree")
    plt.ylabel("Hashtag Count")
    plt.title("Distribution of Hashtag Weighted Degree")
    plt.tight_layout()
    plt.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close()
    return output_path


def plot_community_sizes(summary_df: pd.DataFrame, output_name: str = "03_community_sizes.png") -> Path:
    output_path = _ensure_dir() / output_name
    sizes = summary_df.groupby("community_id")["hashtag"].count().sort_values(ascending=False)
    plt.figure(figsize=(8, 5))
    sizes.plot(kind="bar", color="#55A868")
    plt.xlabel("Community ID")
    plt.ylabel("Member Count")
    plt.title("Community Size Distribution")
    plt.tight_layout()
    plt.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close()
    return output_path


def plot_centrality_vs_likes(metrics_df: pd.DataFrame, output_name: str = "04_centrality_vs_likes.png") -> Path:
    output_path = _ensure_dir() / output_name
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    metrics = [
        ("weighted_degree", "Weighted Degree"),
        ("betweenness", "Betweenness Centrality"),
        ("eigenvector", "Eigenvector Centrality"),
    ]
    for ax, (column, label) in zip(axes, metrics):
        subset = metrics_df[[column, "avg_likes"]].dropna()
        if subset.empty:
            ax.set_visible(False)
            continue
        ax.scatter(subset[column], subset["avg_likes"], alpha=0.7, color="#C44E52")
        ax.set_xlabel(label)
        ax.set_ylabel("Average Likes")
        ax.set_title(f"{label} vs Engagement")
    plt.tight_layout()
    plt.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close()
    return output_path


def plot_top_hashtags(metrics_df: pd.DataFrame, output_name: str = "05_top_hashtags_by_degree.png") -> Path:
    output_path = _ensure_dir() / output_name
    top = metrics_df.nlargest(15, "weighted_degree")
    plt.figure(figsize=(9, 5))
    plt.barh(top["hashtag"], top["weighted_degree"], color="#8172B3")
    plt.xlabel("Weighted Degree")
    plt.ylabel("Hashtag")
    plt.title("Top Hashtags by Weighted Degree")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close()
    return output_path
