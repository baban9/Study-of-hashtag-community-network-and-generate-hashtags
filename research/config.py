"""Central configuration for the hashtag community research pipeline."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Raw and processed data locations
SCRAPED_DATA_DIR = PROJECT_ROOT / "scrappedData"
RAW_META_CSV = SCRAPED_DATA_DIR / "hashtag_meta_data.csv"
SYNTHETIC_META_CSV = PROJECT_ROOT / "research" / "data" / "synthetic_hashtag_meta_data.csv"
PREPARED_EDGES_CSV = PROJECT_ROOT / "outputs" / "tables" / "hashtag_cooccurrence_edges.csv"
HASHTAG_METRICS_CSV = PROJECT_ROOT / "outputs" / "tables" / "hashtag_metrics.csv"
COMMUNITY_SUMMARY_CSV = PROJECT_ROOT / "outputs" / "tables" / "community_summary.csv"
CORRELATION_CSV = PROJECT_ROOT / "outputs" / "tables" / "centrality_like_correlations.csv"

# Output directories
FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"
TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"
WHITEPAPER_PDF = REPORTS_DIR / "hashtag_community_whitepaper.pdf"

# Analysis parameters
LIKES_THRESHOLD = 200
MIN_EDGE_WEIGHT = 2
RANDOM_SEED = 42
SYNTHETIC_NUM_POSTS = 800
SYNTHETIC_NUM_COMMUNITIES = 6
