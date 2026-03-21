"""
Synthesis Module
Generates constitution documents from extracted features.
"""

import json
from typing import List, Dict
from anthropic import Anthropic
import duckdb
from pathlib import Path
import logging


logger = logging.getLogger(__name__)


CONSTITUTION_PROMPT = """You have structured feature extractions from {count} YouTube videos,
filtered to those with {min_views} or more views.

Feature data:
{features_json_array}

Generate a constitution document in markdown with these sections:

1. Hook Pattern Index
   - Each hook type with frequency count and example title
2. Structural Templates
   - Recurring segment sequences with view performance correlation
3. Topic-Performance Matrix
   - Topic categories ranked by median view count
4. Anomalies
   - Videos that break identified patterns but still outperform median
5. High-Signal Phrasing Patterns
   - Specific language patterns that appear in top 20% performers
6. Null Hypotheses
   - Patterns that appear frequent but show no view correlation

Be specific. Use counts and percentages. Flag low-confidence observations."""


def build_constitution(
    conn: duckdb.DuckDBPyConnection,
    client: Anthropic,
    min_views: int,
    output_path: str
) -> str:
    """
    Generate a constitution document from video features.

    Args:
        conn: Database connection
        client: Anthropic API client
        min_views: Minimum view threshold for inclusion
        output_path: Path for output markdown file

    Returns:
        Path to the generated constitution file
    """
    from index import get_top_performers

    # Get top performing videos
    records = get_top_performers(conn, min_views)

    if not records:
        logger.warning(f"No videos found with >= {min_views} views")
        return None

    logger.info(f"Building constitution from {len(records)} videos")

    # Extract features from records
    features_array = []
    for record in records:
        if record.get("features_json"):
            try:
                features = json.loads(record["features_json"])
                features_array.append({
                    "video_id": record["id"],
                    "title": record["title"],
                    "views": record["views"],
                    "date": record["date"],
                    "features": features
                })
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse features for video {record['id']}")

    if not features_array:
        logger.error("No valid features found in top performers")
        return None

    # Format prompt
    features_json = json.dumps(features_array, indent=2)
    prompt = CONSTITUTION_PROMPT.format(
        count=len(features_array),
        min_views=min_views,
        features_json_array=features_json
    )

    logger.info("Calling Anthropic API for constitution synthesis...")

    try:
        # Call Anthropic API
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        # Extract response text
        constitution_text = response.content[0].text

        # Write constitution markdown
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(constitution_text)

        logger.info(f"Constitution written to {output_file}")

        # Write raw features JSON
        raw_json_path = output_file.parent / "constitution_raw.json"
        with open(raw_json_path, 'w', encoding='utf-8') as f:
            json.dump(features_array, f, indent=2)

        logger.info(f"Raw features written to {raw_json_path}")

        return str(output_file)

    except Exception as e:
        logger.error(f"Failed to generate constitution: {e}", exc_info=True)
        return None
