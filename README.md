# YouTube Channel Corpus Analyzer

A Python tool that analyzes entire YouTube channel catalogs by extracting transcripts, metadata, and running structured analysis via the Anthropic API to generate pattern-based constitution documents.

## Features

- **Data Acquisition**: Pull complete channel video catalogs with transcripts using yt-dlp
- **Whisper Fallback**: Automatic audio transcription via OpenAI Whisper when VTT captions are unavailable
- **Block Detection**: Detects monetized/members-only videos and retries with browser cookies automatically
- **Corpus Indexing**: Store and query video data using DuckDB
- **Feature Extraction**: Analyze transcripts using Claude to extract structured patterns
- **Visual Analysis**: Analyze thumbnails for body language, facial expressions, and visual hooks
- **Retry Queue**: Failed extractions are queued and retried automatically on subsequent runs
- **Constitution Synthesis**: Generate comprehensive markdown reports of channel patterns
- **MCP Integration**: Use as an MCP server in Claude Desktop for interactive analysis
- **Claude Code Plugin**: `/analyze` slash command and autopilot skill for one-command analysis

## Requirements

- Python 3.11+
- yt-dlp
- ffmpeg (required for Whisper audio extraction)
- Anthropic API key

## Installation

See [INSTALL.md](INSTALL.md) for full instructions covering Claude Code (plugin) and Claude Desktop (MCP server).

**Quick install:**
```bash
git clone https://github.com/crichalchemist/yt-analysis.git
cd yt-analysis
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Usage

### Claude Code (plugin)

```
/analyze https://www.youtube.com/@channelname ./output --min-views 100000
```

Or invoke the autopilot skill directly:
```
Use the yt-analysis skill to analyze https://www.youtube.com/@channelname
```

### CLI

```bash
python main.py "https://www.youtube.com/@channelname" ./output --min-views 100000
```

### MCP Server (Claude Desktop)

Configure `claude_desktop_config.json` (see [INSTALL.md](INSTALL.md) Section B), then use the MCP tools:
- `pull_and_index` — pull channel and create database
- `run_extraction` — extract features from videos
- `generate_constitution` — create constitution markdown
- `query_corpus` — run SQL queries on the corpus

## Output Files

```
output/
  corpus.db              # DuckDB database
  features.jsonl         # append-only extraction log
  retry_queue.jsonl      # videos pending retry (removed when all recovered)
  constitution.md        # synthesized pattern analysis
  constitution_raw.json  # raw features used for synthesis
  errors.log             # WARNING+ level logs
  YYYYMMDD_VIDEOID/      # per-video raw files from yt-dlp
```

## Architecture

### Pipeline

```
acquire.py   → pull_channel(): yt-dlp subprocess, block detection + cookie retry
               build_record(): *.info.json + *.en.vtt → Dict
                               falls back to Whisper audio transcription if no VTT

index.py     → DuckDB single table: videos(id, title, date, views, duration_seconds,
               transcript, thumbnail_path, channel_url, features_json)

extract.py   → Per-video: Claude with transcript + optional base64 thumbnail
               → structured JSON stored in features_json
               Failed videos → retry_queue.jsonl, retried at end of each run

synthesize.py → Top-performers (>= min_views) → constitution.md + constitution_raw.json
```

### Extracted Features

**Text analysis (from transcript):**
- `hook_type`: question, stat, story, contrast, or void
- `hook_text`: first two sentences of transcript
- `structure`: array of section labels
- `cta_present`: boolean
- `emotional_arc`: flat, rise, fall, or rise-fall
- `key_claims`: list of 3–5 main claims
- `topic_category`: primary topic
- `estimated_retention_signal`: low, medium, or high

**Visual analysis (from thumbnail, when available):**
- `visual_hook_elements`, `body_language`, `visual_context`, `thumbnail_effectiveness`

Visual analysis auto-degrades to text-only if thumbnail is missing or unreadable.

### Database Schema

```sql
CREATE TABLE videos (
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
```

### Constitution Sections

1. Hook Pattern Index
2. Structural Templates
3. Topic-Performance Matrix
4. Anomalies (high-performers that break patterns)
5. High-Signal Phrasing Patterns
6. Null Hypotheses (frequent patterns with no view correlation)

## Cost Estimates

For a typical channel with ~170 videos:
- **Text-only**: ~1.04M input tokens, ~173K output tokens
- **With visual analysis**: ~1.2M input tokens, ~260K output tokens
- Synthesis: ~50K input + 4K output
- **Estimated: $8–12 USD** using Claude Sonnet with visual analysis

Consider Anthropic's batch API for 50% cost reduction on large channels.

## Troubleshooting

See [INSTALL.md](INSTALL.md) for troubleshooting Whisper, cookie retry, retry queue, and MCP configuration.

## License

MIT — see [LICENSE](LICENSE).
