"""End-to-end research analysis pipeline."""

from __future__ import annotations

import json
from pathlib import Path

from research.centrality import centrality_like_correlations, compute_hashtag_metrics
from research.communities import aggregate_community_stats, community_summary, detect_communities, modularity_score
from research.config import FIGURES_DIR, REPORTS_DIR, TABLES_DIR
from research.data.prepare import prepare_cooccurrence_edges
from research.data.synthetic import resolve_input_meta_csv
from research.network import build_weighted_graph, graph_summary
from research.plots import (
    plot_centrality_vs_likes,
    plot_community_network,
    plot_community_sizes,
    plot_degree_distribution,
    plot_top_hashtags,
)


def run_analysis() -> dict:
    """Execute the full analysis workflow and persist artifacts."""
    for directory in (FIGURES_DIR, TABLES_DIR, REPORTS_DIR):
        directory.mkdir(parents=True, exist_ok=True)

    meta_csv, data_source = resolve_input_meta_csv()
    edges_df = prepare_cooccurrence_edges(meta_csv)
    graph = build_weighted_graph(edges_df)
    partition = detect_communities(graph)
    modularity = modularity_score(graph, partition)
    summary_df = community_summary(graph, partition)
    community_stats = aggregate_community_stats(summary_df)
    metrics_df = compute_hashtag_metrics(graph, partition, edges_df)
    correlations_df = centrality_like_correlations(metrics_df)

    figure_paths = [
        plot_community_network(graph, partition),
        plot_degree_distribution(graph),
        plot_community_sizes(summary_df),
        plot_centrality_vs_likes(metrics_df),
        plot_top_hashtags(metrics_df),
    ]

    results = {
        "data_source": data_source,
        "meta_csv": str(meta_csv),
        "graph_summary": graph_summary(graph),
        "modularity": modularity,
        "num_communities": len(set(partition.values())) if partition else 0,
        "community_stats": community_stats.to_dict(orient="records"),
        "correlations": correlations_df.to_dict(orient="records"),
        "figures": [str(path) for path in figure_paths],
    }

    summary_path = REPORTS_DIR / "analysis_summary.json"
    summary_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    return results


if __name__ == "__main__":
    output = run_analysis()
    print(json.dumps(output, indent=2))
