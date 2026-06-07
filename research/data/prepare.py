"""Prepare hashtag co-occurrence edge list from raw metadata."""

from __future__ import annotations

import ast
from collections import Counter
from pathlib import Path

import pandas as pd

from research.config import LIKES_THRESHOLD, PREPARED_EDGES_CSV


def load_meta_data(meta_csv: Path) -> pd.DataFrame:
    return pd.read_csv(meta_csv)


def build_edge_records(df: pd.DataFrame, likes_threshold: int = LIKES_THRESHOLD) -> pd.DataFrame:
    """Expand post-level hashtag pairs into an edge list with like counts."""
    combo_counter = Counter()
    parsed_rows = []

    for _, row in df.iterrows():
        combos = ast.literal_eval(row["hash_combo"])
        parsed_rows.append((row["file_name"], row["like"], combos))
        combo_counter.update(combos)

    records = []
    for file_name, likes, combos in parsed_rows:
        if likes <= likes_threshold:
            continue
        for left, right in combos:
            records.append(
                {
                    "post_id": file_name,
                    "likes": likes,
                    "pair_count": combo_counter[(left, right)],
                    "left": left,
                    "right": right,
                }
            )

    return pd.DataFrame(records)


def prepare_cooccurrence_edges(
    meta_csv: Path,
    output_csv: Path = PREPARED_EDGES_CSV,
    likes_threshold: int = LIKES_THRESHOLD,
) -> pd.DataFrame:
    df = load_meta_data(meta_csv)
    edges = build_edge_records(df, likes_threshold=likes_threshold)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    edges.to_csv(output_csv, index=False)
    return edges
