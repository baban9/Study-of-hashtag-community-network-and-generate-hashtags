"""Generate synthetic Instagram-style hashtag co-occurrence data for reproducible demos."""

from __future__ import annotations

import ast
import random
from pathlib import Path

import pandas as pd

from research.config import RANDOM_SEED, SYNTHETIC_NUM_COMMUNITIES, SYNTHETIC_NUM_POSTS

COMMUNITY_TEMPLATES = [
    ["travel", "wanderlust", "explore", "adventure", "nature", "photography", "vacation"],
    ["foodie", "foodporn", "instafood", "yummy", "delicious", "homemade", "chef"],
    ["fitness", "gym", "workout", "fitfam", "health", "motivation", "training"],
    ["fashion", "style", "ootd", "outfit", "streetstyle", "model", "beauty"],
    ["tech", "coding", "developer", "ai", "startup", "innovation", "software"],
    ["art", "artist", "creative", "design", "illustration", "drawing", "gallery"],
]

NOISE_TAGS = ["love", "instagood", "photooftheday", "happy", "life", "followme", "like4like"]


def _build_communities(num_communities: int) -> list[list[str]]:
    communities = COMMUNITY_TEMPLATES[:num_communities]
    if num_communities > len(COMMUNITY_TEMPLATES):
        for idx in range(len(COMMUNITY_TEMPLATES), num_communities):
            communities.append([f"topic{idx}", f"tag{idx}a", f"tag{idx}b", f"tag{idx}c"])
    return communities


def _sample_hashtags(communities: list[list[str]], rng: random.Random) -> list[str]:
    primary = rng.choice(communities)
    secondary = rng.choice(communities)
    tags = set(rng.sample(primary, k=rng.randint(2, min(4, len(primary)))))
    if secondary is not primary:
        tags.update(rng.sample(secondary, k=rng.randint(1, 2)))
    if rng.random() < 0.4:
        tags.add(rng.choice(NOISE_TAGS))
    return sorted(tags)


def _pairwise_combos(tags: list[str]) -> list[tuple[str, str]]:
    pairs = []
    for i in range(len(tags)):
        for j in range(i + 1, len(tags)):
            pair = tuple(sorted((tags[i], tags[j])))
            pairs.append(pair)
    return pairs


def _like_count(tags: list[str], communities: list[list[str]], rng: random.Random) -> int:
    base = rng.randint(50, 400)
    for community in communities:
        overlap = len(set(tags) & set(community))
        base += overlap * rng.randint(80, 220)
    return base


def generate_synthetic_meta_data(
    output_path: Path,
    num_posts: int = SYNTHETIC_NUM_POSTS,
    num_communities: int = SYNTHETIC_NUM_COMMUNITIES,
    seed: int = RANDOM_SEED,
) -> Path:
    """Write a CSV compatible with the real scraping schema."""
    rng = random.Random(seed)
    communities = _build_communities(num_communities)
    rows = []

    for post_idx in range(num_posts):
        tags = _sample_hashtags(communities, rng)
        combos = _pairwise_combos(tags)
        likes = _like_count(tags, communities, rng)
        rows.append(
            {
                "file_name": f"synthetic_post_{post_idx:04d}.jpg",
                "like": likes,
                "hash_combo": str(combos),
            }
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    return output_path


def resolve_input_meta_csv() -> tuple[Path, str]:
    """Return the best available meta CSV and a label describing its source."""
    from research.config import RAW_META_CSV, SYNTHETIC_META_CSV

    if RAW_META_CSV.exists() and RAW_META_CSV.stat().st_size > 0:
        return RAW_META_CSV, "scraped"
    generate_synthetic_meta_data(SYNTHETIC_META_CSV)
    return SYNTHETIC_META_CSV, "synthetic"
