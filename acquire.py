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

_BLOCK_PATTERNS: tuple[str, ...] = (
    "This video is not available",
    "Video unavailable",
    "members-only",
    "This video requires payment",
    "has been removed",
    "account associated with this video",
    "age-restricted",
)
_WHISPER_MODEL_SIZE: str = "base"


def _detect_blocked(stderr: str) -> bool:
    return any(p in stderr for p in _BLOCK_PATTERNS)


def download_audio(video_dir: Path, video_id: str, output_dir: str) -> Optional[Path]:
    """
    Download audio-only stream for a video via yt-dlp.

    Returns path to downloaded audio file, or None on failure.
    Why: Whisper transcription requires an audio file; yt-dlp handles format negotiation.
    """
    cmd = [
        "yt-dlp",
        "--format", "bestaudio/best",
        "--extract-audio",
        "--audio-format", "mp3",
        "--output", str(video_dir / f"{video_id}.%(ext)s"),
        f"https://www.youtube.com/watch?v={video_id}",
    ]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        logger.warning(f"Audio download failed for {video_id}: {e.stderr}")
        return None

    audio_extensions = {".mp3", ".m4a", ".webm", ".opus"}
    matches = [p for p in video_dir.glob(f"{video_id}.*") if p.suffix in audio_extensions]
    return matches[0] if matches else None


def transcribe_with_whisper(audio_path: Path) -> str:
    """
    Transcribe audio file using OpenAI Whisper.

    Deferred import: whisper pulls PyTorch (~2 GB); importing at module top would
    break MCP server startup on systems where whisper isn't installed.
    """
    import whisper  # deferred — optional dependency
    model = whisper.load_model(_WHISPER_MODEL_SIZE)
    result = model.transcribe(str(audio_path))
    return result["text"]


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

    result = subprocess.run(cmd, capture_output=True, text=True, check=False)

    if result.returncode != 0:
        if _detect_blocked(result.stderr):
            logger.warning("Blocked content detected — retrying with --cookies-from-browser chrome")
            retry_cmd = cmd + ["--cookies-from-browser", "chrome"]
            result = subprocess.run(retry_cmd, capture_output=True, text=True, check=False)
            if result.returncode != 0:
                logger.warning(f"Cookie retry also failed for {channel_url}: {result.stderr[:500]}")
        else:
            logger.error(f"yt-dlp failed for {channel_url}: {result.stderr[:500]}")

    logger.debug(result.stdout)
    logger.info("yt-dlp completed")

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
            logger.info(f"No VTT found in {video_dir}, attempting Whisper transcription")
            video_id_for_audio = info.get("id")
            audio_path = download_audio(video_dir, video_id_for_audio, str(video_dir.parent))
            if audio_path is None:
                logger.warning(f"Audio download failed for {video_dir}, skipping")
                return None
            try:
                transcript = transcribe_with_whisper(audio_path)
                logger.info(f"Whisper transcription complete for {video_id_for_audio} ({len(transcript)} chars)")
            except Exception as e:
                logger.error(f"Whisper transcription failed for {video_id_for_audio}: {e}", exc_info=True)
                return None
        else:
            vtt_path = vtt_files[0]
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
