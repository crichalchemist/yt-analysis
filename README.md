# YouTube Channel Corpus Analyzer

A Python tool that analyzes entire YouTube channel catalogs by extracting transcripts, metadata, and running structured analysis via the Anthropic API to generate pattern-based constitution documents.

## Features

- **Data Acquisition**: Pull complete channel video catalogs with transcripts using yt-dlp
- **Corpus Indexing**: Store and query video data using DuckDB
- **Feature Extraction**: Analyze transcripts using Claude to extract structured patterns
- **Constitution Synthesis**: Generate comprehensive markdown reports of channel patterns
- **MCP Integration**: Use as an MCP server in Claude Desktop for interactive analysis

## Requirements

- Python 3.11+
- yt-dlp (for YouTube data)
- Anthropic API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/crichalchemist/yt-analysis.git
cd yt-analysis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set your Anthropic API key:
```bash
export ANTHROPIC_API_KEY="your_api_key_here"
```

## Usage

### CLI Mode

Run the full analysis pipeline:

```bash
python main.py "https://www.youtube.com/@channelname" ./output --min-views 100000
```

Arguments:
- `channel_url`: YouTube channel URL
- `output_dir`: Directory for outputs (database, transcripts, constitution)
- `--min-views`: Minimum view threshold for constitution (default: 100000)

### MCP Server Mode (Claude Desktop)

1. Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "youtube-corpus": {
      "command": "python",
      "args": ["/absolute/path/to/yt-analysis/mcp_server.py"],
      "env": {
        "ANTHROPIC_API_KEY": "your_key_here"
      }
    }
  }
}
```

2. Restart Claude Desktop

3. Available MCP tools:
   - `pull_and_index`: Pull channel and create database
   - `run_extraction`: Extract features from videos
   - `generate_constitution`: Create constitution markdown
   - `query_corpus`: Run SQL queries on the corpus

### Example MCP Workflow in Claude Desktop

```
1. Use pull_and_index with channel URL
2. Use run_extraction to analyze transcripts
3. Use generate_constitution to create report
4. Use query_corpus to explore data with SQL
```

## Output Files

The tool generates the following in the output directory:

- `corpus.db` - DuckDB database with all video data
- `features.jsonl` - JSONL log of feature extractions
- `constitution.md` - Synthesized pattern analysis
- `constitution_raw.json` - Raw feature data used for synthesis
- `errors.log` - Error log for troubleshooting
- `YYYYMMDD_VIDEOID/` - Individual video directories with transcripts and metadata

## Architecture

### Modules

1. **acquire.py** - Data acquisition via yt-dlp
   - `pull_channel()`: Download channel metadata and transcripts
   - `vtt_to_text()`: Convert VTT subtitles to clean text
   - `build_record()`: Create structured video records

2. **index.py** - DuckDB corpus management
   - `init_db()`: Initialize database schema
   - `insert_records()`: Add video records
   - `get_top_performers()`: Query by view threshold
   - `get_records_without_features()`: Find unprocessed videos

3. **extract.py** - Feature extraction via Anthropic API
   - `extract_features()`: Analyze single video
   - `extract_all()`: Batch process all videos

4. **synthesize.py** - Constitution generation
   - `build_constitution()`: Generate pattern analysis document

5. **main.py** - CLI entry point

6. **mcp_server.py** - MCP server wrapper

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

### Extracted Features

For each video, the following features are extracted:
- `hook_type`: question, stat, story, contrast, or void
- `hook_text`: First two sentences of transcript
- `structure`: Array of section labels
- `cta_present`: Boolean for call-to-action presence
- `emotional_arc`: flat, rise, fall, or rise-fall
- `key_claims`: List of 3-5 main claims
- `topic_category`: Primary topic
- `estimated_retention_signal`: low, medium, or high

### Constitution Sections

The generated constitution includes:
1. **Hook Pattern Index** - Hook types with frequency and examples
2. **Structural Templates** - Common segment patterns with performance correlation
3. **Topic-Performance Matrix** - Topics ranked by median views
4. **Anomalies** - High-performers that break patterns
5. **High-Signal Phrasing Patterns** - Language in top 20% performers
6. **Null Hypotheses** - Frequent patterns with no view correlation

## Error Handling

- Missing VTT files are logged and skipped
- API failures retry once before logging
- Individual video failures don't halt the pipeline
- All errors written to `errors.log` with timestamps

## Cost Estimates

For a typical channel with 173 videos:
- Input tokens: ~1.04M
- Output tokens: ~173K
- Synthesis: ~50K input + 4K output
- **Estimated cost: $6-8 USD** (using Claude Sonnet 4.5)

Note: Consider using Anthropic's batch API for 50% cost reduction on large channels.

## Advanced Usage

### Query the Corpus with SQL

```python
import duckdb

conn = duckdb.connect("output/corpus.db")

# Get top 10 videos by views
result = conn.execute("""
    SELECT title, views, date
    FROM videos
    ORDER BY views DESC
    LIMIT 10
""").fetchall()

print(result)
```

### Custom Feature Analysis

```python
from anthropic import Anthropic
from index import init_db, get_all_records

client = Anthropic(api_key="your_key")
conn = init_db("output/corpus.db")
records = get_all_records(conn)

# Custom analysis on records
for record in records:
    # Your analysis here
    pass
```

## Troubleshooting

### yt-dlp fails
- Ensure yt-dlp is up to date: `pip install -U yt-dlp`
- Check channel URL is correct
- Some videos may not have auto-generated subtitles

### No transcripts extracted
- Not all videos have auto-generated subtitles
- Check `errors.log` for specific failures
- Try a different channel with known subtitles

### API rate limits
- Add delays between API calls if needed
- Consider using batch API for large channels

## License

MIT License - See LICENSE file for details

## Contributing

Pull requests welcome! Please ensure:
- Code follows existing style
- Error handling is comprehensive
- Logging is informative

## Support

For issues and questions:
- GitHub Issues: https://github.com/crichalchemist/yt-analysis/issues
- Documentation: This README
