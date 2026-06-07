"""Smoke tests for the hashtag community research pipeline."""

from __future__ import annotations

import json
from pathlib import Path

import networkx as nx
import pandas as pd
import pytest

from research.centrality import centrality_like_correlations, compute_hashtag_metrics
from research.communities import detect_communities, modularity_score
from research.config import PROJECT_ROOT
from research.data.prepare import build_edge_records
from research.data.synthetic import generate_synthetic_meta_data
from research.network import build_weighted_graph, graph_summary


@pytest.fixture
def synthetic_meta_csv(tmp_path: Path) -> Path:
    path = tmp_path / "meta.csv"
    generate_synthetic_meta_data(path, num_posts=120, num_communities=4, seed=7)
    return path


def test_synthetic_data_schema(synthetic_meta_csv: Path):
    df = pd.read_csv(synthetic_meta_csv)
    assert {"file_name", "like", "hash_combo"}.issubset(df.columns)
    assert len(df) == 120


def test_build_edge_records(synthetic_meta_csv: Path):
    df = pd.read_csv(synthetic_meta_csv)
    edges = build_edge_records(df, likes_threshold=100)
    assert not edges.empty
    assert {"left", "right", "likes", "pair_count"}.issubset(edges.columns)


def test_graph_and_communities(synthetic_meta_csv: Path):
    df = pd.read_csv(synthetic_meta_csv)
    edges = build_edge_records(df, likes_threshold=100)
    graph = build_weighted_graph(edges, min_weight=1)
    assert graph.number_of_nodes() > 0
    partition = detect_communities(graph)
    assert len(partition) == graph.number_of_nodes()
    assert modularity_score(graph, partition) >= 0.0


def test_centrality_correlations(synthetic_meta_csv: Path):
    df = pd.read_csv(synthetic_meta_csv)
    edges = build_edge_records(df, likes_threshold=100)
    graph = build_weighted_graph(edges, min_weight=1)
    partition = detect_communities(graph)
    metrics = compute_hashtag_metrics(graph, partition, edges)
    correlations = centrality_like_correlations(metrics)
    assert not metrics.empty
    assert "pearson_r" in correlations.columns


def test_graph_summary_empty():
    graph = nx.Graph()
    summary = graph_summary(graph)
    assert summary["nodes"] == 0


def test_run_analysis_integration():
    from research.run_analysis import run_analysis

    results = run_analysis()
    assert results["graph_summary"]["nodes"] > 0
    assert Path(results["figures"][0]).exists()
    summary_file = PROJECT_ROOT / "outputs" / "reports" / "analysis_summary.json"
    assert summary_file.exists()
    payload = json.loads(summary_file.read_text(encoding="utf-8"))
    assert "modularity" in payload
