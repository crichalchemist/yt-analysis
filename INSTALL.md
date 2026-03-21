# Installation

Three sections depending on your runtime. Complete Section C regardless of which runtime you use.

---

## Section A — Claude Code (plugin install)

### Option 1: Plugin marketplace (recommended)

```bash
/plugin marketplace add crichalchemist/yt-analysis
/plugin install yt-analysis@crichalchemist
```

### Option 2: Manual install from source

```bash
git clone https://github.com/crichalchemist/yt-analysis.git ~/yt-analysis
pip install -r ~/yt-analysis/requirements.txt
```

Then in Claude Code:
```bash
/plugin install ~/yt-analysis
```

After installing, the `/analyze` slash command and the `yt-analysis` skill are immediately available.

---

## Section B — Claude Desktop (MCP server)

### Step 1: Clone and install dependencies

```bash
git clone https://github.com/crichalchemist/yt-analysis.git ~/yt-analysis
pip install -r ~/yt-analysis/requirements.txt
```

> **Note:** `openai-whisper` pulls PyTorch as a transitive dependency (~2 GB). The install may take 5–10 minutes on first run.

### Step 2: Configure MCP server

Open `claude_desktop_config.json`. On macOS it lives at:
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

Add the following entry inside `"mcpServers"` (replace `/Users/YOUR_USERNAME` with your actual home directory):

```json
{
  "mcpServers": {
    "yt-analysis": {
      "command": "python3",
      "args": ["/Users/YOUR_USERNAME/yt-analysis/mcp_server.py"],
      "env": {
        "ANTHROPIC_API_KEY": "sk-ant-..."
      }
    }
  }
}
```

Do not use `~` in the path — Claude Desktop requires an absolute path.

### Step 3: Restart Claude Desktop

Quit and relaunch Claude Desktop. The MCP tools (`pull_and_index`, `run_extraction`, `generate_constitution`) will appear in the tool list.

---

## Section C — Both runtimes

Complete these steps regardless of which runtime you installed.

### Step 1: Set ANTHROPIC_API_KEY

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

Add to `~/.zshrc` or `~/.bashrc` to persist across sessions.

### Step 2: Verify system dependencies

**yt-dlp**
```bash
yt-dlp --version
# if missing:
pip install yt-dlp
# or: brew install yt-dlp
```

**ffmpeg** (required for Whisper audio extraction)
```bash
ffmpeg -version
# if missing:
brew install ffmpeg          # macOS
# sudo apt install ffmpeg    # Debian/Ubuntu
```

**whisper** (optional — enables transcription when VTT captions are unavailable)
```bash
python3 -c "import whisper; print('ok')"
# if missing:
pip install openai-whisper
```

### Step 3: Smoke test

```bash
python3 -c "from acquire import pull_channel, build_record; print('ok')"
```

Expected output: `ok`

If you see `ModuleNotFoundError`, run `pip install -r requirements.txt` again.

### Step 4: First run

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
python3 ~/yt-analysis/main.py "https://www.youtube.com/@mkbhd" ./output --min-views 100000
```

Or in Claude Code / Claude Desktop:
```
/analyze https://www.youtube.com/@mkbhd ./output --min-views 100000
```

---

## Troubleshooting

**Whisper model download is slow or fails**
The `base` model (~150 MB) downloads on first use to `~/.cache/whisper/`. If it fails mid-download, delete the partial file and retry:
```bash
rm -rf ~/.cache/whisper/
python3 -c "import whisper; whisper.load_model('base')"
```

**Blocked/monetized videos not retrying**
The cookie retry uses `--cookies-from-browser chrome`. If Chrome is not installed or the profile is locked (Chrome is open), retry manually:
```bash
yt-dlp --cookies-from-browser firefox <video_url>
```

**retry_queue.jsonl is not emptying**
Some videos may permanently fail extraction (deleted, private, or API quota exhausted). Inspect the queue:
```bash
cat output/retry_queue.jsonl | python3 -c "import sys,json; [print(json.loads(l).get('video_id'), json.loads(l).get('title')) for l in sys.stdin]"
```

Remove entries you no longer want to retry by editing the file directly. The queue is plain JSONL — one entry per line.

**MCP tools not appearing in Claude Desktop**
1. Confirm the path in `claude_desktop_config.json` is absolute (no `~`)
2. Confirm `ANTHROPIC_API_KEY` is set inside the `"env"` block of the config, not just in your shell
3. Check the MCP server starts cleanly: `python3 ~/yt-analysis/mcp_server.py`
4. Restart Claude Desktop after any config change
