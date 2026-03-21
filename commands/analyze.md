---
description: Full-autopilot YouTube channel analysis — pull transcripts, extract features, synthesize a content constitution.
disable-model-invocation: true
---

# /analyze

Run the full yt-analysis pipeline end-to-end in autopilot mode.

Delegates to the `yt-analysis` skill, which handles preflight checks, acquisition, indexing, feature extraction, and constitution synthesis across both Claude Code (shell subprocess) and Claude Desktop (MCP tools) runtimes — without requiring manual intervention at any phase.

## Usage

```
/analyze <channel_url> [output_dir] [--min-views <n>]
```

## Arguments

| Argument | Required | Default | Description |
|---|---|---|---|
| `channel_url` | yes | — | YouTube channel URL (e.g. `https://www.youtube.com/@mkbhd`) |
| `output_dir` | no | `./output` | Directory for raw data, database, and constitution |
| `--min-views` | no | `10000` | Minimum view count threshold for constitution synthesis |

## What it does

1. **Preflight** — verifies `ANTHROPIC_API_KEY`, `yt-dlp`, `ffmpeg`, and `whisper` are available; reports all failures at once
2. **Acquire** — pulls channel transcripts via yt-dlp; falls back to Whisper audio transcription when VTT captions are unavailable; retries blocked/monetized videos with browser cookies automatically
3. **Index** — inserts records into `corpus.db` (DuckDB), skipping videos already present
4. **Extract** — calls Claude to extract structured features per video; failed extractions are queued in `retry_queue.jsonl` and retried at the end of the phase
5. **Synthesize** — aggregates top-performing videos into a `constitution.md` content strategy document

## Example

```
/analyze https://www.youtube.com/@hubermanlab ./huberman-output --min-views 500000
```

Analyzes the Huberman Lab channel, stores data in `./huberman-output/`, and synthesizes a constitution from videos with at least 500 000 views.

## Output files

```
<output_dir>/
  corpus.db              # DuckDB database — query directly
  features.jsonl         # append-only extraction log
  retry_queue.jsonl      # videos pending retry (removed when all recovered)
  constitution.md        # synthesized content strategy
  constitution_raw.json  # raw feature set used for synthesis
  YYYYMMDD_VIDEOID/      # per-video raw files from yt-dlp
```

## Notes

- Each phase is **idempotent** — re-running `/analyze` on the same output directory only processes what's missing.
- Whisper model download (~150 MB for `base`) happens on first use; subsequent runs use the cached model.
- Cookie retry uses the Chrome profile on the current machine. If Chrome is unavailable, blocked videos are logged and skipped.
