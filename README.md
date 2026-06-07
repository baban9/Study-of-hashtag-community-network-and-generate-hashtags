# Hashtag Community Network and Image Captioning

A dual-track research project combining graph analytics on Instagram hashtag co-occurrence networks with a Flask image captioning application for content-aware hashtag generation.

## Research questions

1. Do hashtags form stable thematic communities when modeled as a co-occurrence network?
2. Does network centrality correlate with average post engagement (likes)?
3. Can image-derived captions complement graph-based hashtag strategy?

## Repository layout

```
hashtagApp/                 Flask image captioning web app
research/                   Reproducible analysis pipeline
  data/                     Synthetic data and preparation
  run_analysis.py           Main analysis entry point
  generate_whitepaper.py    PDF report generator
hashTag_community_analysis/ Legacy notebook and scripts
outputs/
  figures/                  Saved plots (PNG)
  tables/                   CSV metrics and edge lists
  reports/                  Whitepaper PDF and JSON summary
tests/                      Pipeline smoke tests
file_downloader.py          Instagram scraping helper (optional)
scrappedData/               Place scraped CSV here (gitignored)
```

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
make setup
make analyze          # builds network, communities, figures, tables
make whitepaper       # analyze + PDF report
make test             # run smoke tests
make run              # start Flask app on port 5000
```

## Reproducing the study

### 1. Environment

```bash
make setup
```

### 2. Data sources

The pipeline auto-detects data in this order:

1. `scrappedData/hashtag_meta_data.csv` (real scraped data)
2. Synthetic demo data at `research/data/synthetic_hashtag_meta_data.csv`

Expected scraped schema:

| column      | description                          |
|-------------|--------------------------------------|
| file_name   | Post identifier                      |
| like        | Like count                           |
| hash_combo  | Python list of (tag_a, tag_b) pairs  |

To use your own scraped data, place the CSV at `scrappedData/hashtag_meta_data.csv` and rerun `make analyze`.

### 3. Analysis outputs

| Artifact | Path |
|----------|------|
| Co-occurrence edges | `outputs/tables/hashtag_cooccurrence_edges.csv` |
| Hashtag metrics | `outputs/tables/hashtag_metrics.csv` |
| Community summary | `outputs/tables/community_summary.csv` |
| Centrality correlations | `outputs/tables/centrality_like_correlations.csv` |
| Network figure | `outputs/figures/01_community_network.png` |
| Degree distribution | `outputs/figures/02_degree_distribution.png` |
| Community sizes | `outputs/figures/03_community_sizes.png` |
| Centrality vs likes | `outputs/figures/04_centrality_vs_likes.png` |
| Top hashtags | `outputs/figures/05_top_hashtags_by_degree.png` |
| Analysis summary | `outputs/reports/analysis_summary.json` |
| Whitepaper PDF | `outputs/reports/hashtag_community_whitepaper.pdf` |

### 4. Regenerate whitepaper

```bash
make whitepaper
```

Or step by step:

```bash
python -m research.run_analysis
python -m research.generate_whitepaper
```

## Methodology summary

1. Filter posts above a like threshold (default 200).
2. Build weighted edges from hashtag pair co-occurrence counts.
3. Detect communities with the Louvain algorithm.
4. Compute weighted degree, betweenness, and eigenvector centrality.
5. Correlate centrality with average likes using Pearson and Spearman tests.
6. Export figures, tables, and a PDF whitepaper.

Configuration lives in `research/config.py`.

## Flask application (Track A)

Upload an image via the web UI. The app extracts caption features and object labels using pretrained vision models.

```bash
make run
# open http://localhost:5000
```

Note: model weights under `hashtagApp/models/` are required for full captioning. The health endpoint works without them.

## Legacy notebook

The original exploratory notebook remains at:

`hashTag_community_analysis/Analyze_hashtag_communities.ipynb`

The `research/` package supersedes it for reproducible, script-based execution.

## Tech stack

Python 3, Flask, NetworkX, python-louvain, pandas, matplotlib, reportlab, scipy, pytest

## Limitations

- Scraping requires Instaloader credentials and compliance with platform terms.
- Synthetic data demonstrates pipeline behavior when scraped data is unavailable.
- Captioning models are not bundled in this repository; weights must be obtained separately.

## License

See LICENSE.
