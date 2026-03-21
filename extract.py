"""
Feature Extraction Module
Extracts structured features from video transcripts and visual content using Anthropic API.
"""

import json
import base64
from typing import Dict, Optional, List
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


VISUAL_EXTRACTION_PROMPT = """Analyze this YouTube video using the transcript and thumbnail image.

Title: {title}
Views: {views}
Transcript: {transcript_truncated}

Based on the thumbnail and transcript, analyze:

Return only a JSON object with these exact keys:
- hook_type: one of (question, stat, story, contrast, void)
- hook_text: first two sentences of transcript
- structure: array of section label strings
- cta_present: boolean
- emotional_arc: one of (flat, rise, fall, rise-fall)
- key_claims: list of 3 to 5 specific claims made
- topic_category: single primary topic string
- estimated_retention_signal: one of (low, medium, high) based on pacing and structure
- visual_hook_elements: list of visual elements in thumbnail (text overlays, facial expressions, objects, colors)
- body_language: description of presenter's body language and emotional state visible in thumbnail
- visual_context: description of setting, production quality, and visual storytelling elements
- thumbnail_effectiveness: one of (low, medium, high) based on visual appeal and clarity

Return JSON only. No explanation. No markdown fencing."""


def encode_image(image_path: str) -> Optional[str]:
    """
    Encode image to base64 for API submission.

    Args:
        image_path: Path to image file

    Returns:
        Base64 encoded image string or None if failed
    """
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()
        return base64.standard_b64encode(image_data).decode('utf-8')
    except Exception as e:
        logger.error(f"Failed to encode image {image_path}: {e}")
        return None


def get_image_media_type(image_path: str) -> str:
    """
    Get media type for image based on extension.

    Args:
        image_path: Path to image file

    Returns:
        Media type string
    """
    ext = Path(image_path).suffix.lower()
    if ext in ['.jpg', '.jpeg']:
        return 'image/jpeg'
    elif ext == '.png':
        return 'image/png'
    elif ext == '.webp':
        return 'image/webp'
    elif ext == '.gif':
        return 'image/gif'
    else:
        return 'image/jpeg'  # default


def extract_features(record: Dict, client: Anthropic, use_vision: bool = True) -> Optional[Dict]:
    """
    Extract structured features from a video record using Anthropic API.

    Args:
        record: Video record dictionary with transcript and metadata
        client: Anthropic API client
        use_vision: Whether to include visual analysis from thumbnail

    Returns:
        Dictionary of extracted features or None if extraction failed
    """
    # Truncate transcript to 6000 characters
    transcript = record.get("transcript", "")
    transcript_truncated = transcript[:6000]

    # Check if thumbnail is available and vision is enabled
    thumbnail_path = record.get("thumbnail_path")
    has_thumbnail = thumbnail_path and Path(thumbnail_path).exists() and use_vision

    if has_thumbnail:
        # Use visual analysis with thumbnail
        prompt_text = VISUAL_EXTRACTION_PROMPT.format(
            title=record.get("title", ""),
            views=record.get("views", 0),
            transcript_truncated=transcript_truncated
        )

        # Encode thumbnail
        image_base64 = encode_image(thumbnail_path)
        if not image_base64:
            logger.warning(f"Failed to encode thumbnail for video {record.get('id')}, falling back to text-only")
            has_thumbnail = False

    if not has_thumbnail:
        # Use text-only analysis
        prompt_text = EXTRACTION_PROMPT.format(
            title=record.get("title", ""),
            views=record.get("views", 0),
            transcript_truncated=transcript_truncated
        )

    try:
        # Build message content
        if has_thumbnail:
            content = [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": get_image_media_type(thumbnail_path),
                        "data": image_base64
                    }
                },
                {
                    "type": "text",
                    "text": prompt_text
                }
            ]
            max_tokens = 1500  # More tokens for visual analysis
        else:
            content = prompt_text
            max_tokens = 1000

        # Call Anthropic API
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=max_tokens,
            messages=[{
                "role": "user",
                "content": content
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

            retry_content = content if has_thumbnail else prompt_text
            if not has_thumbnail:
                retry_content = prompt_text + "\n\nIMPORTANT: Return valid JSON only, no markdown formatting."
            else:
                retry_content[-1]["text"] += "\n\nIMPORTANT: Return valid JSON only, no markdown formatting."

            response = client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=max_tokens,
                messages=[{
                    "role": "user",
                    "content": retry_content
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
