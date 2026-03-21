"""
Corpus Index Module
Manages DuckDB database for video corpus indexing and querying.
"""

import duckdb
from pathlib import Path
from typing import List, Dict, Optional
import logging


logger = logging.getLogger(__name__)


def init_db(db_path: str) -> duckdb.DuckDBPyConnection:
    """
    Initialize DuckDB database with videos table.

    Args:
        db_path: Path to DuckDB database file

    Returns:
        Database connection
    """
    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)

    conn = duckdb.connect(str(db_file))

    # Create videos table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            id TEXT PRIMARY KEY,
            title TEXT,
            date TEXT,
            views INTEGER,
            duration_seconds INTEGER,
            transcript TEXT,
            thumbnail_path TEXT,
            channel_url TEXT,
            features_json TEXT
        )
    """)

    logger.info(f"Database initialized at {db_path}")

    return conn


def insert_records(conn: duckdb.DuckDBPyConnection, records: List[Dict]) -> int:
    """
    Insert or replace video records in the database.

    Args:
        conn: Database connection
        records: List of video record dictionaries

    Returns:
        Number of records inserted
    """
    inserted = 0

    for record in records:
        try:
            conn.execute("""
                INSERT OR REPLACE INTO videos (
                    id, title, date, views, duration_seconds,
                    transcript, thumbnail_path, channel_url, features_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record.get("id"),
                record.get("title"),
                record.get("date"),
                record.get("views"),
                record.get("duration_seconds"),
                record.get("transcript"),
                record.get("thumbnail_path"),
                record.get("channel_url"),
                None  # features_json starts as null
            ))
            inserted += 1
        except Exception as e:
            logger.error(f"Failed to insert record {record.get('id')}: {e}")

    conn.commit()
    logger.info(f"Inserted {inserted} records")

    return inserted


def get_top_performers(conn: duckdb.DuckDBPyConnection, min_views: int) -> List[Dict]:
    """
    Get videos with views above threshold.

    Args:
        conn: Database connection
        min_views: Minimum view count threshold

    Returns:
        List of video records
    """
    result = conn.execute("""
        SELECT id, title, date, views, duration_seconds, transcript,
               thumbnail_path, channel_url, features_json
        FROM videos
        WHERE views >= ?
        ORDER BY views DESC
    """, (min_views,)).fetchall()

    columns = ["id", "title", "date", "views", "duration_seconds",
               "transcript", "thumbnail_path", "channel_url", "features_json"]

    records = [dict(zip(columns, row)) for row in result]

    logger.info(f"Retrieved {len(records)} videos with >= {min_views} views")

    return records


def get_all_records(conn: duckdb.DuckDBPyConnection) -> List[Dict]:
    """
    Get all video records from database.

    Args:
        conn: Database connection

    Returns:
        List of all video records
    """
    result = conn.execute("""
        SELECT id, title, date, views, duration_seconds, transcript,
               thumbnail_path, channel_url, features_json
        FROM videos
        ORDER BY date DESC
    """).fetchall()

    columns = ["id", "title", "date", "views", "duration_seconds",
               "transcript", "thumbnail_path", "channel_url", "features_json"]

    records = [dict(zip(columns, row)) for row in result]

    logger.info(f"Retrieved {len(records)} total records")

    return records


def get_records_without_features(conn: duckdb.DuckDBPyConnection) -> List[Dict]:
    """
    Get all video records that don't have features extracted yet.

    Args:
        conn: Database connection

    Returns:
        List of video records without features
    """
    result = conn.execute("""
        SELECT id, title, date, views, duration_seconds, transcript,
               thumbnail_path, channel_url, features_json
        FROM videos
        WHERE features_json IS NULL
        ORDER BY views DESC
    """).fetchall()

    columns = ["id", "title", "date", "views", "duration_seconds",
               "transcript", "thumbnail_path", "channel_url", "features_json"]

    records = [dict(zip(columns, row)) for row in result]

    logger.info(f"Retrieved {len(records)} records without features")

    return records


def update_features(conn: duckdb.DuckDBPyConnection, video_id: str, features_json: str):
    """
    Update the features_json field for a video.

    Args:
        conn: Database connection
        video_id: Video ID
        features_json: JSON string of extracted features
    """
    conn.execute("""
        UPDATE videos
        SET features_json = ?
        WHERE id = ?
    """, (features_json, video_id))

    conn.commit()
