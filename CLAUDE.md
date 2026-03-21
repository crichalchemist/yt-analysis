# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run full pipeline (CLI)
export ANTHROPIC_API_KEY="your_key"
python main.py "https://www.youtube.com/@channelname" ./output --min-views 100000

# Run MCP server (for Claude Desktop)
python mcp_server.py

# Direct module use (resumable — each step only processes what's missing)
python -c "from acquire import pull_channel; pull_channel('URL', './output')"
python -c "from extract import extract_all; ..."
python -c "from synthesize import build_constitution; ..."

# Query the corpus directly
python -c "import duckdb; conn = duckdb.connect('output/corpus.db'); print(conn.execute('SELECT * FROM videos LIMIT 5').fetchall())"
```

There is no test suite. No linter config. Python 3.11+ required.

## Architecture

The codebase is a linear pipeline with two runtime modes (CLI via `main.py`, MCP server via `mcp_server.py`):

```
acquire.py     → pull_channel() uses yt-dlp subprocess, writes YYYYMMDD_VIDEOID/ dirs
                  _detect_blocked() checks stderr for paywall/members-only patterns;
                  retries with --cookies-from-browser chrome on match
                  build_record() reads *.info.json + *.en.vtt → Dict
                  if no VTT: download_audio() + transcribe_with_whisper() (deferred import)

index.py       → DuckDB single table: videos(id, title, date, views, duration_seconds,
                  transcript, thumbnail_path, channel_url, features_json)
                  features_json starts NULL, updated by extract stage

extract.py     → Per-video: calls claude-sonnet-4-5-20250929 with transcript + optional
                  base64-encoded thumbnail → structured JSON stored in features_json
                  get_records_without_features() makes extraction idempotent/resumable
                  Failures written to retry_queue.jsonl; process_retry_queue() runs after
                  main loop and rewrites queue with only unrecovered entries

synthesize.py  → Aggregates all features_json from top-performers (>= min_views),
                  sends to Claude in one batch prompt → constitution.md + constitution_raw.json
```

### Key design decisions

- **features_json stored as TEXT in DuckDB** — features schema is deliberately flexible (visual fields only present when thumbnail available), so JSON blob avoids schema migrations when the extraction prompt changes.
- **Transcript truncated to 6000 chars** in `extract.py:118` — balances API cost vs. coverage. Constitution synthesis is untruncated.
- **Visual analysis auto-degrades** — if thumbnail path missing or encode fails, falls back to text-only prompt silently.
- **Whisper import is deferred** — `import whisper` lives inside `transcribe_with_whisper()`, not at module top. This keeps `acquire.py` importable on systems without PyTorch, preventing MCP server startup failures.
- **MCP server is synchronous wrappers** around the same module functions; `mcp_server.py` does not add business logic.

### Model in use

`claude-sonnet-4-5-20250929` is hardcoded in both `extract.py:172` and `synthesize.py:103`. Update both when upgrading.

## Environment

```bash
ANTHROPIC_API_KEY   # required for extraction and synthesis stages
```

Output directory layout (generated at runtime, gitignored):
```
output/
  corpus.db              # DuckDB database
  features.jsonl         # append-only extraction log
  retry_queue.jsonl      # videos pending retry (absent when queue is clear)
  constitution.md        # synthesized pattern analysis
  constitution_raw.json  # raw features used for synthesis
  errors.log             # WARNING+ level logs
  YYYYMMDD_VIDEOID/      # per-video raw files from yt-dlp
```
