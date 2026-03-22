---
name: yt-analysis
description: Use when analyzing a YouTube channel's content catalog to extract patterns, understand top-performer characteristics, or build a content strategy reference from transcripts.
---

# yt-analysis Skill

Analyze a YouTube channel catalog end-to-end: acquire transcripts → index → extract structured features with Claude → synthesize a content constitution.

## When to Use

**Use when:**
- You have a YouTube channel URL and want to understand what content performs best
- Building a content constitution or style guide from an existing channel's catalog
- Researching a channel's topic patterns, hooks, or structural tendencies at scale
- Any analysis requiring transcripts from more than a handful of videos

**Do NOT use when:**
- Analyzing a single video (run `acquire.py` directly)
- The channel is private or requires login beyond cookie support
- You only need metadata (views, titles) without transcript content

## Quick Reference

| Phase | What it does | Failure behavior |
|-------|-------------|-----------------|
| 1 — Preflight | Checks env, tools, runtime | Hard stop on missing required tools |
| 2 — Acquire | Downloads transcripts via yt-dlp | Continues — skips blocked videos |
| 3 — Index | Inserts records into DuckDB | Hard stop if DB empty after insert |
| 4 — Extract | Calls Claude per video for features | Warns if >50% fail; writes retry_queue.jsonl |
| 5 — Synthesize | Builds constitution from top performers | Reports error; does not re-run earlier phases |

Runs **5 phases without user intervention**. The skill handles both runtimes automatically:
- **Claude Code** — shell subprocesses via `python3 -c "..."` or `python3 main.py`
- **Claude Desktop** — MCP tool calls (`pull_and_index`, `run_extraction`, `generate_constitution`)

---

## Invocation

```
Use the yt-analysis skill to analyze <channel_url> into <output_dir> with min_views=<n>
```

All arguments have defaults: `output_dir=./output`, `min_views=10000`.

---

## Phase 1 — Preflight

Check all prerequisites **before touching the network or disk**. Report all failures at once — do not stop after the first.

**Required checks:**

1. `ANTHROPIC_API_KEY` — verify env var is set and non-empty
2. `yt-dlp` — run `yt-dlp --version`; report version if found
3. `ffmpeg` — run `ffmpeg -version`; required for Whisper audio extraction
4. `whisper` — run `python3 -c "import whisper"` (optional but logged if missing; acquisition continues with VTT-only mode)
5. **Runtime detection** — attempt `python3 -c "import mcp"` and check if MCP tool `pull_and_index` is available in the current tool list
   - If `pull_and_index` is available: **Desktop mode**
   - Otherwise: **Claude Code mode**

**Report:**
```
Runtime: [Claude Code | Claude Desktop]
ANTHROPIC_API_KEY: [set | MISSING]
yt-dlp: [version | MISSING]
ffmpeg: [version | MISSING]
whisper: [available | not installed — Whisper fallback disabled]
```

**Stop condition:** Any of `ANTHROPIC_API_KEY`, `yt-dlp`, `ffmpeg` missing → report all issues, then stop. Do not proceed to Phase 2.

---

## Phase 2 — Acquire

Pull transcripts for the channel. Whisper fallback and cookie retry are **automatic inside the acquisition functions** — no manual intervention is needed.

**Claude Code:**
```bash
python3 -c "
from acquire import pull_channel, build_record
from pathlib import Path
dirs = pull_channel('<channel_url>', '<output_dir>')
records = [r for d in dirs if (r := build_record(d)) is not None]
print(f'Acquired {len(records)} records')
"
```

**Claude Desktop:**
Call MCP tool `pull_and_index` with arguments:
```json
{ "channel_url": "<channel_url>", "output_dir": "<output_dir>" }
```

**What happens automatically:**
- If a video has no VTT captions: `build_record()` calls `download_audio()` then `transcribe_with_whisper()` — no action needed
- If yt-dlp detects a blocked/monetized/members-only video: `pull_channel()` retries with `--cookies-from-browser chrome` automatically
- If cookie retry also fails: the video is logged and skipped; acquisition continues

**Partial results are acceptable.** Phase 2 never fully fails — log the count of acquired vs. skipped videos and continue.

---

## Phase 3 — Index

Insert acquired records into `corpus.db`. Already-present records are skipped (idempotent).

**Claude Code:**
```bash
python3 -c "
import duckdb
from index import init_db, insert_records
from acquire import pull_channel, build_record
from pathlib import Path

conn = duckdb.connect('<output_dir>/corpus.db')
init_db(conn)
dirs = [d for d in Path('<output_dir>').iterdir() if d.is_dir()]
records = [r for d in dirs if (r := build_record(d)) is not None]
inserted = insert_records(conn, records)
print(f'Indexed {inserted} records')
"
```

**Claude Desktop:** Already handled by `pull_and_index` in Phase 2 — skip this phase.

**Stop condition:** If zero records were indexed and the output directory has no existing `corpus.db` with rows, stop and report. There is nothing to extract from an empty corpus.

---

## Phase 4 — Extract

Extract structured features per video using Claude. Failed videos are written to `retry_queue.jsonl` and retried automatically at the end of the phase.

**Claude Code:**
```bash
python3 -c "
import os, duckdb
from anthropic import Anthropic
from extract import extract_all

conn = duckdb.connect('<output_dir>/corpus.db')
client = Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])
count = extract_all(conn, client, '<output_dir>')
print(f'Extracted features for {count} videos')
"
```

**Claude Desktop:**
Call MCP tool `run_extraction` with arguments:
```json
{ "output_dir": "<output_dir>" }
```

**After extract:** Check for `retry_queue.jsonl`:
```bash
python3 -c "
from pathlib import Path
q = Path('<output_dir>/retry_queue.jsonl')
if q.exists():
    lines = [l for l in q.read_text().splitlines() if l.strip()]
    print(f'retry_queue: {len(lines)} videos still pending')
else:
    print('retry_queue: empty (all recovered)')
"
```

Report the count of remaining unrecovered videos. These will persist across runs for future retries.

**Warning threshold:** If >50% of videos failed extraction, log a warning and continue — do not halt. The constitution will be built from what is available.

---

## Phase 5 — Synthesize

Aggregate top-performing videos into a content constitution document.

**Claude Code:**
```bash
python3 -c "
import os, duckdb
from anthropic import Anthropic
from synthesize import build_constitution

conn = duckdb.connect('<output_dir>/corpus.db')
client = Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])
result = build_constitution(conn, client, '<output_dir>', min_views=<min_views>)
print(f'Constitution written to {result}')
"
```

**Claude Desktop:**
Call MCP tool `generate_constitution` with arguments:
```json
{ "output_dir": "<output_dir>", "min_views": <min_views> }
```

**On failure:** Report the error. Do not re-run earlier phases — the data is in `corpus.db` and can be synthesized again independently.

---

## Final Summary

Query `corpus.db` to populate counts, then display:

```bash
python3 -c "
import duckdb, json
from pathlib import Path

conn = duckdb.connect('<output_dir>/corpus.db')
total   = conn.execute('SELECT COUNT(*) FROM videos').fetchone()[0]
vtt     = conn.execute(\"SELECT COUNT(*) FROM videos WHERE transcript IS NOT NULL AND transcript != ''\").fetchone()[0]
feats   = conn.execute('SELECT COUNT(*) FROM videos WHERE features_json IS NOT NULL').fetchone()[0]

retry_path = Path('<output_dir>/retry_queue.jsonl')
retry_remaining = sum(1 for l in retry_path.read_text().splitlines() if l.strip()) if retry_path.exists() else 0

print(f'Videos acquired:     {total}')
print(f'Transcripts (VTT):   {vtt}')
print(f'Features extracted:  {feats}')
print(f'Retry remaining:     {retry_remaining}')
"
```

Present as a table:

| Metric | Count |
|---|---|
| Videos acquired | `<n>` |
| VTT transcripts | `<n>` |
| Whisper fallback | `<acquired - vtt>` |
| Blocked / skipped | `<n>` |
| Features extracted | `<n>` |
| Retry recovered | `<n>` |
| Constitution path | `<output_dir>/constitution.md` |
| DB path | `<output_dir>/corpus.db` |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Channel URL uses `/c/` or `/user/` format | Use `/@handle` format — yt-dlp resolves it more reliably |
| Phase 4 extracts 0 features | Check `ANTHROPIC_API_KEY` is set; check `errors.log` for rate limit or model errors |
| `corpus.db` has rows but constitution is empty | `min_views` threshold too high — lower it or check `features_json` is populated |
| Re-running Phase 2 re-downloads everything | It won't — `pull_channel` skips dirs that already exist; Phase 3 skips already-indexed IDs |
| Whisper not installed, videos silently skipped | Install `openai-whisper` + `ffmpeg`; videos without VTT captions need it |
| `retry_queue.jsonl` never clears | Persistent API failures or truncated transcripts — inspect the queue entries manually |

## Error Escalation Rules

| Phase | Failure condition | Action |
|---|---|---|
| 1 (Preflight) | Any required tool missing | **Stop** — report all missing tools |
| 2 (Acquire) | Partial failures | **Continue** — log skipped videos |
| 3 (Index) | Zero records inserted + empty DB | **Stop** — nothing to process |
| 4 (Extract) | >50% failure rate | **Warn + continue** — synthesize what's available |
| 5 (Synthesize) | Any failure | **Report** — do not re-run earlier phases |
