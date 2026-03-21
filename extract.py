"""
Feature Extraction Module
Extracts structured features from video transcripts using Anthropic API.
"""

import json
from typing import Dict, Optional
from anthropic import Anthropic
import duckdb
import logging
from pathlib import Path


logger = logging.getLogger(__name__)


EXTRACTION_PROMPT = """Analyze this YouTube video transcript and metadata.

Title: {title}
Views: {views}
Transcript: {transcript_truncated}

Return only a JSON object with these exact keys:
- hook_type: one of (question, stat, story, contrast, void)
- hook_text: first two sentences of transcript
- structure: array of section label strings
- cta_present: boolean
- emotional_arc: one of (flat, rise, fall, rise-fall)
- key_claims: list of 3 to 5 specific claims made
- topic_category: single primary topic string
- estimated_retention_signal: one of (low, medium, high) based on pacing and structure

Return JSON only. No explanation. No markdown fencing."""


def extract_features(record: Dict, client: Anthropic) -> Optional[Dict]:
    """
    Extract structured features from a video record using Anthropic API.

    Args:
        record: Video record dictionary with transcript and metadata
        client: Anthropic API client

    Returns:
        Dictionary of extracted features or None if extraction failed
    """
    # Truncate transcript to 6000 characters
    transcript = record.get("transcript", "")
    transcript_truncated = transcript[:6000]

    # Format prompt
    prompt = EXTRACTION_PROMPT.format(
        title=record.get("title", ""),
        views=record.get("views", 0),
        transcript_truncated=transcript_truncated
    )

    try:
        # Call Anthropic API
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        # Extract response text
        response_text = response.content[0].text

        # Try to parse JSON
        try:
            features = json.loads(response_text)
            return features
        except json.JSONDecodeError:
            # Retry once if JSON parsing failed
            logger.warning(f"First attempt failed to parse JSON for video {record.get('id')}, retrying...")

            response = client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": prompt + "\n\nIMPORTANT: Return valid JSON only, no markdown formatting."
                }]
            )

            response_text = response.content[0].text

            # Try to clean up common issues
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()

            try:
                features = json.loads(response_text)
                return features
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON after retry for video {record.get('id')}: {e}")
                logger.error(f"Raw response: {response_text}")
                return None

    except Exception as e:
        logger.error(f"Failed to extract features for video {record.get('id')}: {e}", exc_info=True)
        return None


def extract_all(conn: duckdb.DuckDBPyConnection, client: Anthropic, output_dir: str) -> int:
    """
    Extract features for all videos without features in the database.

    Args:
        conn: Database connection
        client: Anthropic API client
        output_dir: Directory to write features.jsonl log

    Returns:
        Number of records processed
    """
    from index import get_records_without_features, update_features

    # Get records without features
    records = get_records_without_features(conn)

    if not records:
        logger.info("No records need feature extraction")
        return 0

    logger.info(f"Extracting features for {len(records)} videos")

    # Open jsonlines log file
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    log_file = output_path / "features.jsonl"

    processed = 0

    with open(log_file, 'a', encoding='utf-8') as f:
        for i, record in enumerate(records, 1):
            video_id = record.get("id")
            logger.info(f"Processing {i}/{len(records)}: {video_id} - {record.get('title')}")

            # Extract features
            features = extract_features(record, client)

            if features:
                # Convert to JSON string
                features_json = json.dumps(features)

                # Update database
                update_features(conn, video_id, features_json)

                # Write to log file
                log_entry = {
                    "video_id": video_id,
                    "title": record.get("title"),
                    "views": record.get("views"),
                    "features": features
                }
                f.write(json.dumps(log_entry) + "\n")
                f.flush()

                processed += 1
            else:
                logger.warning(f"Skipping video {video_id} due to extraction failure")

    logger.info(f"Feature extraction complete: {processed} videos processed")

    return processed
