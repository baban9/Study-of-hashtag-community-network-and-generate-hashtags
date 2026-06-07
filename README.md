# Hashtag Community Network and Image Captioning

Two-track NLP and graph analytics project: a Flask app for image-to-text captioning with hashtag generation, and Instagram hashtag co-occurrence network analysis.

## Problem

1. **Product track**: Help users generate relevant hashtags from image content.
2. **Research track**: Model hashtag communities from co-occurrence networks to inform content strategy.

## Approach

### Track A: Image captioning app (`hashtagApp/`)

- Upload RGB image via Flask UI
- Extract text/caption features with a pretrained vision model
- Return original, grayscale, and B&W variants for downstream augmentation

### Track B: Community analysis (`hashTag_community_analysis/`)

- Scrape and prepare Instagram hashtag co-occurrence data
- Build network graph and detect communities
- Analyze like counts vs hashtag cluster membership

## Repository structure

```
hashtagApp/
  app.py              Flask web application
  model.py            Vision model wrapper
  utils.py            Image and text utilities
  templates/          Web UI
hashTag_community_analysis/
  Analyze_hashtag_communities.ipynb
  prepare_likes_occurence_data.py
  config.py
file_downloader.py    Data ingestion helper
model/                Model artifacts and class index
```

## Reproducibility

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make setup
make run
```

Community analysis:

```bash
jupyter lab hashTag_community_analysis/Analyze_hashtag_communities.ipynb
```

## Tech stack

Python 3, Flask, PIL, PyTorch/TensorFlow (model-dependent), NetworkX, Jupyter

## Limitations and next steps

- Containerize app and model with Docker Compose
- Add API endpoint for programmatic hashtag suggestions
- Document scraping compliance and data retention policy
- Version model weights separately from source code
