"""
YouTube Channel Corpus Analyzer
Main entry point for CLI execution.
"""

import argparse
import logging
import os
import sys
from pathlib import Path
from anthropic import Anthropic

from acquire import pull_channel, build_record
from index import init_db, insert_records
from extract import extract_all
from synthesize import build_constitution


def setup_logging(output_dir: str):
    """Configure logging to console and error file."""
    log_path = Path(output_dir) / "errors.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )

    # File handler for errors
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(file_formatter)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


def run(channel_url: str, output_dir: str, min_views_threshold: int):
    """
    Run the full analysis pipeline.

    Args:
        channel_url: YouTube channel URL
        output_dir: Directory for all outputs
        min_views_threshold: Minimum views for constitution synthesis
    """
    logger = logging.getLogger(__name__)

    # Setup logging
    setup_logging(output_dir)

    logger.info("=" * 60)
    logger.info("YouTube Channel Corpus Analyzer")
    logger.info("=" * 60)

    # Initialize Anthropic client
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        logger.error("ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)

    client = Anthropic(api_key=api_key)
    logger.info("Anthropic client initialized")

    # Initialize database
    db_path = Path(output_dir) / "corpus.db"
    conn = init_db(str(db_path))
    logger.info(f"Database initialized at {db_path}")

    # Pull channel data
    logger.info("Pulling channel data...")
    try:
        video_dirs = pull_channel(channel_url, output_dir)
        logger.info(f"Retrieved {len(video_dirs)} videos")
    except Exception as e:
        logger.error(f"Failed to pull channel data: {e}", exc_info=True)
        sys.exit(1)

    # Build and insert records
    logger.info("Building records from video data...")
    records = []
    failed = 0

    for video_dir in video_dirs:
        try:
            record = build_record(video_dir)
            if record:
                records.append(record)
            else:
                failed += 1
        except Exception as e:
            logger.error(f"Error processing {video_dir}: {e}")
            failed += 1

    logger.info(f"Built {len(records)} records ({failed} failed)")

    if records:
        insert_records(conn, records)
    else:
        logger.error("No records to insert")
        sys.exit(1)

    # Extract features
    logger.info("Extracting features from transcripts...")
    try:
        processed = extract_all(conn, client, output_dir)
        logger.info(f"Extracted features for {processed} videos")
    except Exception as e:
        logger.error(f"Feature extraction failed: {e}", exc_info=True)
        sys.exit(1)

    # Synthesize constitution
    logger.info("Synthesizing constitution document...")
    try:
        constitution_path = Path(output_dir) / "constitution.md"
        result = build_constitution(conn, client, min_views_threshold, str(constitution_path))
        if result:
            logger.info(f"Constitution generated at {result}")
        else:
            logger.warning("Constitution generation failed or returned no results")
    except Exception as e:
        logger.error(f"Constitution synthesis failed: {e}", exc_info=True)
        sys.exit(1)

    # Close database
    conn.close()

    logger.info("=" * 60)
    logger.info(f"Analysis complete! Outputs in: {output_dir}")
    logger.info("=" * 60)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Analyze YouTube channel corpus and generate constitution"
    )
    parser.add_argument(
        "channel_url",
        help="YouTube channel URL"
    )
    parser.add_argument(
        "output_dir",
        help="Output directory for all data and results"
    )
    parser.add_argument(
        "--min-views",
        type=int,
        default=100000,
        help="Minimum view count for constitution synthesis (default: 100000)"
    )

    args = parser.parse_args()

    run(args.channel_url, args.output_dir, args.min_views)


if __name__ == "__main__":
    main()
