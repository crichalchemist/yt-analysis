"""
Data Acquisition Module
Pulls YouTube channel data using yt-dlp and processes transcripts.
"""

import subprocess
import json
from pathlib import Path
from typing import List, Dict, Optional
import webvtt
import logging


logger = logging.getLogger(__name__)


def pull_channel(channel_url: str, output_dir: str) -> List[Path]:
    """
    Pull all videos from a YouTube channel using yt-dlp.

    Args:
        channel_url: YouTube channel URL
        output_dir: Directory to store downloaded data

    Returns:
        List of video directories created
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    output_template = str(output_path / "%(upload_date)s_%(id)s" / "%(title)s")

    cmd = [
        "yt-dlp",
        "--write-auto-sub",
        "--sub-format", "vtt",
        "--write-thumbnail",
        "--write-info-json",
        "--skip-download",
        "--output", output_template,
        channel_url
    ]

    logger.info(f"Running yt-dlp for channel: {channel_url}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        logger.info(f"yt-dlp completed successfully")
        logger.debug(result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error(f"yt-dlp failed: {e.stderr}")
        raise

    # Find all video directories created
    video_dirs = [d for d in output_path.iterdir() if d.is_dir()]
    logger.info(f"Found {len(video_dirs)} video directories")

    return video_dirs


def vtt_to_text(vtt_path: Path) -> str:
    """
    Convert VTT subtitle file to clean text transcript.

    Args:
        vtt_path: Path to VTT file

    Returns:
        Clean transcript text
    """
    try:
        vtt = webvtt.read(str(vtt_path))
        text_blocks = [caption.text for caption in vtt]

        # Join with spaces and clean up
        transcript = " ".join(text_blocks)

        # Remove duplicate spaces
        transcript = " ".join(transcript.split())

        return transcript
    except Exception as e:
        logger.error(f"Failed to parse VTT file {vtt_path}: {e}")
        raise


def build_record(video_dir: Path) -> Optional[Dict]:
    """
    Build a record dictionary from a video directory.

    Args:
        video_dir: Directory containing video metadata and transcript

    Returns:
        Dictionary with video data or None if processing failed
    """
    try:
        # Find info.json file
        info_files = list(video_dir.glob("*.info.json"))
        if not info_files:
            logger.warning(f"No info.json found in {video_dir}")
            return None

        info_path = info_files[0]

        # Load metadata
        with open(info_path, 'r', encoding='utf-8') as f:
            info = json.load(f)

        # Find VTT file (prefer English, fall back to any)
        vtt_files = list(video_dir.glob("*.en.vtt"))
        if not vtt_files:
            vtt_files = list(video_dir.glob("*.vtt"))

        if not vtt_files:
            logger.warning(f"No VTT file found in {video_dir}, skipping")
            return None

        vtt_path = vtt_files[0]

        # Extract transcript
        transcript = vtt_to_text(vtt_path)

        # Find thumbnail
        thumbnail_files = list(video_dir.glob("*.jpg")) + list(video_dir.glob("*.webp")) + list(video_dir.glob("*.png"))
        thumbnail_path = str(thumbnail_files[0]) if thumbnail_files else None

        # Build record
        record = {
            "id": info.get("id"),
            "title": info.get("title"),
            "date": info.get("upload_date"),
            "views": info.get("view_count", 0),
            "duration_seconds": info.get("duration", 0),
            "transcript": transcript,
            "thumbnail_path": thumbnail_path,
            "channel_url": info.get("channel_url") or info.get("uploader_url")
        }

        return record

    except Exception as e:
        logger.error(f"Failed to build record for {video_dir}: {e}", exc_info=True)
        return None
