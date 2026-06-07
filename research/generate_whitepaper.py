"""Generate a PDF whitepaper from analysis artifacts."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from research.config import FIGURES_DIR, REPORTS_DIR, WHITEPAPER_PDF


def _load_summary() -> dict:
    summary_path = REPORTS_DIR / "analysis_summary.json"
    if not summary_path.exists():
        raise FileNotFoundError("Run analysis before generating the whitepaper.")
    return json.loads(summary_path.read_text(encoding="utf-8"))


def _styles():
    base = getSampleStyleSheet()
    base.add(
        ParagraphStyle(
            name="CenterTitle",
            parent=base["Title"],
            alignment=TA_CENTER,
            spaceAfter=18,
        )
    )
    base.add(
        ParagraphStyle(
            name="Abstract",
            parent=base["BodyText"],
            alignment=TA_JUSTIFY,
            leading=14,
            spaceAfter=12,
        )
    )
    base.add(
        ParagraphStyle(
            name="Section",
            parent=base["Heading1"],
            spaceBefore=12,
            spaceAfter=8,
        )
    )
    base.add(
        ParagraphStyle(
            name="Body",
            parent=base["BodyText"],
            alignment=TA_JUSTIFY,
            leading=14,
            spaceAfter=8,
        )
    )
    base.add(
        ParagraphStyle(
            name="Caption",
            parent=base["BodyText"],
            alignment=TA_CENTER,
            fontSize=9,
            textColor=colors.grey,
            spaceAfter=12,
        )
    )
    return base


def _figure_block(path: Path, caption: str, styles, max_width: float = 6.5 * inch) -> list:
    if not path.exists():
        return [Paragraph(f"Figure unavailable: {path.name}", styles["Caption"])]
    img = Image(str(path))
    scale = max_width / float(img.drawWidth)
    img.drawWidth = max_width
    img.drawHeight = img.drawHeight * scale
    return [img, Paragraph(caption, styles["Caption"]), Spacer(1, 0.15 * inch)]


def _summary_table(summary: dict, styles) -> Table:
    graph = summary.get("graph_summary", {})
    rows = [
        ["Metric", "Value"],
        ["Data source", summary.get("data_source", "unknown")],
        ["Nodes", str(graph.get("nodes", 0))],
        ["Edges", str(graph.get("edges", 0))],
        ["Graph density", f"{graph.get('density', 0):.4f}"],
        ["Average degree", f"{graph.get('avg_degree', 0):.2f}"],
        ["Connected components", str(graph.get("components", 0))],
        ["Communities detected", str(summary.get("num_communities", 0))],
        ["Modularity", f"{summary.get('modularity', 0):.4f}"],
    ]
    table = Table(rows, colWidths=[2.8 * inch, 3.2 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2F4F4F")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
            ]
        )
    )
    return table


def generate_whitepaper(output_path: Path = WHITEPAPER_PDF) -> Path:
    summary = _load_summary()
    styles = _styles()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54,
    )
    story = []
    today = datetime.utcnow().strftime("%Y-%m-%d")

    story.append(Paragraph("Hashtag Community Network Analysis", styles["CenterTitle"]))
    story.append(Paragraph("A Research Study on Instagram Hashtag Co-occurrence Structure", styles["CenterTitle"]))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(f"Generated on {today} (UTC)", styles["Caption"]))
    story.append(PageBreak())

    story.append(Paragraph("Abstract", styles["Section"]))
    story.append(
        Paragraph(
            "This study models social media engagement through hashtag co-occurrence networks. "
            "We construct a weighted undirected graph where nodes represent hashtags and edges "
            "represent joint usage in high-engagement posts. Louvain community detection reveals "
            "thematic clusters, while centrality metrics are compared against average like counts "
            "to assess whether structural prominence aligns with audience response. "
            "The pipeline is fully reproducible and supports both scraped Instagram metadata "
            "and synthetic demonstration datasets.",
            styles["Abstract"],
        )
    )

    story.append(Paragraph("1. Introduction", styles["Section"]))
    story.append(
        Paragraph(
            "Hashtags function as lightweight semantic anchors that connect posts to topics, "
            "audiences, and discovery channels. Marketers and creators often combine multiple "
            "hashtags to maximize reach, which produces stable co-usage patterns over time. "
            "Understanding these patterns as a network can reveal community structure, bridge "
            "tags that connect themes, and engagement signals tied to network position.",
            styles["Body"],
        )
    )
    story.append(
        Paragraph(
            "This repository implements two complementary tracks: a Flask image captioning "
            "application for content-aware hashtag suggestions, and a graph analytics "
            "research pipeline for community detection and centrality analysis.",
            styles["Body"],
        )
    )

    story.append(Paragraph("2. Methodology", styles["Section"]))
    story.append(
        Paragraph(
            "Data preparation begins with post-level hashtag combinations. Each post contributes "
            "unordered hashtag pairs above a configurable like threshold. Pair frequencies are "
            "aggregated into edge weights. We build a weighted NetworkX graph, apply Louvain "
            "community detection, and compute weighted degree, betweenness, and eigenvector "
            "centrality. Pearson and Spearman correlations evaluate the relationship between "
            "centrality and average likes.",
            styles["Body"],
        )
    )
    story.append(Spacer(1, 0.1 * inch))
    story.append(_summary_table(summary, styles))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("3. Results", styles["Section"]))
    story.append(
        Paragraph(
            "The following figures summarize network topology, community composition, and "
            "engagement correlations produced by the analysis pipeline.",
            styles["Body"],
        )
    )

    figure_specs = [
        ("01_community_network.png", "Figure 1. Hashtag co-occurrence network colored by Louvain community."),
        ("02_degree_distribution.png", "Figure 2. Weighted degree distribution across hashtags."),
        ("03_community_sizes.png", "Figure 3. Community size distribution."),
        ("04_centrality_vs_likes.png", "Figure 4. Centrality metrics versus average likes."),
        ("05_top_hashtags_by_degree.png", "Figure 5. Top hashtags ranked by weighted degree."),
    ]
    for filename, caption in figure_specs:
        story.extend(_figure_block(FIGURES_DIR / filename, caption, styles))

    story.append(PageBreak())
    story.append(Paragraph("4. Discussion", styles["Section"]))

    correlations = summary.get("correlations", [])
    if correlations:
        corr_text = (
            "Centrality-engagement correlations indicate whether structurally central hashtags "
            "coincide with higher average likes. "
        )
        for row in correlations:
            corr_text += (
                f"{row['metric']} shows Pearson r={row['pearson_r']:.3f} "
                f"(p={row['pearson_p']:.3f}) and Spearman rho={row['spearman_r']:.3f}. "
            )
        story.append(Paragraph(corr_text, styles["Body"]))
    else:
        story.append(
            Paragraph(
                "Correlation results were not available, likely due to insufficient sample size.",
                styles["Body"],
            )
        )

    story.append(
        Paragraph(
            "Community partitions typically align with topical clusters such as travel, food, "
            "fitness, or technology when synthetic or domain-specific seed tags are present. "
            "Bridge hashtags with high betweenness can connect otherwise separate communities "
            "and are candidates for cross-topic campaigns.",
            styles["Body"],
        )
    )

    story.append(Paragraph("5. Conclusion", styles["Section"]))
    story.append(
        Paragraph(
            "Graph-based hashtag analysis provides actionable structure beyond raw tag lists. "
            "The reproducible pipeline supports portfolio demonstrations, research replication, "
            "and integration with image captioning outputs from the Flask application. "
            "Future work includes temporal drift analysis, multilingual tag normalization, "
            "and live API scoring for recommended hashtag bundles.",
            styles["Body"],
        )
    )

    story.append(Paragraph("6. Reproducibility", styles["Section"]))
    story.append(
        Paragraph(
            "Install dependencies with make setup, run make analyze to regenerate tables and "
            "figures, then make whitepaper to rebuild this document. "
            "Artifacts are written to outputs/tables, outputs/figures, and outputs/reports.",
            styles["Body"],
        )
    )

    doc.build(story)
    return output_path


if __name__ == "__main__":
    path = generate_whitepaper()
    print(f"Whitepaper written to {path}")
