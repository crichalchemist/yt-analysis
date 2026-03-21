# yt-analysis Usage Guide

This guide shows you how to integrate yt-analysis with Claude Desktop and Claude Code in the simplest ways possible.

## Option 1: Using Claude Code Skills (Recommended for Simplicity)

Claude Code skills are the easiest way to get started. They're just Markdown files that define commands.

### Step 1: Create the Skills Directory

```bash
mkdir -p .claude/commands
```

### Step 2: Create Your First Skill

Create a file: `.claude/commands/analyze-video.md`

```markdown
# Analyze YouTube Video

Analyze a YouTube video for key insights, transcript, and metadata.

## Usage

Provide a YouTube URL and I will:
1. Extract video metadata (title, duration, channel)
2. Retrieve and analyze the transcript
3. Generate a concise summary of key points
4. Identify main topics discussed

## Example

Input: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
Output: Video analysis with summary and key insights

## Requirements

- YouTube video URL
- Video should have captions or transcript available
```

### Step 3: Create Additional Skills

Create a file: `.claude/commands/download-transcript.md`

```markdown
# Download Video Transcript

Extract and save the transcript from a YouTube video.

## Usage

Provide a YouTube URL and I will:
1. Fetch the video's transcript
2. Format it for readability
3. Save it to a text file

## Example

Input: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
Output: Formatted transcript file with timestamps
```

### Step 4: Use the Skills in Claude Code

Simply type `/analyze-video` and provide the YouTube URL when prompted.

---

## Option 2: Using MCP Server (For Advanced Integration)

An MCP (Model Context Protocol) server provides deeper integration with Claude Desktop.

### Step 1: Set Up the MCP Server

Your yt-analysis project should have a server implementation. If using Python:

File: `yt_analysis/server.py`

```python
#!/usr/bin/env python3
"""
MCP Server for YouTube Analysis
Provides tools for analyzing YouTube videos via Model Context Protocol
"""

import json
import sys

def list_resources():
    """List available analysis tools"""
    return {
        "resources": [
            {
                "uri": "yt://analyze",
                "name": "Analyze Video",
                "description": "Analyze a YouTube video"
            },
            {
                "uri": "yt://transcript",
                "name": "Get Transcript",
                "description": "Extract video transcript"
            }
        ]
    }

def handle_request(request):
    """Handle MCP requests"""
    if request.get("method") == "list_resources":
        return list_resources()
    return {"error": "Unknown method"}

if __name__ == "__main__":
    for line in sys.stdin:
        request = json.loads(line.strip())
        response = handle_request(request)
        print(json.dumps(response))
```

### Step 2: Configure Claude Desktop

Edit the Claude Desktop configuration file:

**MacOS/Linux:** `~/.config/claude/claude.json`
**Windows:** `%APPDATA%\Claude\claude.json`

```json
{
  "mcpServers": {
    "yt-analysis": {
      "command": "python",
      "args": ["-m", "yt_analysis.server"],
      "env": {
        "PYTHONPATH": "/path/to/yt-analysis"
      }
    }
  }
}
```

Replace `/path/to/yt-analysis` with your actual project path.

### Step 3: Restart Claude Desktop

Close and reopen Claude Desktop to load the new MCP server.

---

## Comparison: Skills vs MCP Server

| Feature | Skills | MCP Server |
|---------|--------|-----------|
| **Setup Time** | ~2 minutes | ~10 minutes |
| **Complexity** | Simple markdown | Requires code |
| **Integration** | Claude Code only | Claude Desktop + Code |
| **Capabilities** | Instructions/prompts | Full tooling |
| **Best For** | Workflows & tasks | Persistent tools |

---

## Quick Start Examples

### Using Skills

```
User: /analyze-video https://www.youtube.com/watch?v=VIDEO_ID
Claude: [Analyzes video and returns summary]
```

### Using MCP Server

Once configured, Claude Desktop will automatically offer yt-analysis tools in the tool palette.

---

## Directory Structure

For the simplest setup using skills:

```
yt-analysis/
├── README.md
├── USAGE-GUIDE.md
└── .claude/
    └── commands/
        ├── analyze-video.md
        └── download-transcript.md
```

For MCP server setup:

```
yt-analysis/
├── README.md
├── USAGE-GUIDE.md
├── yt_analysis/
│   └── server.py
└── .claude/
    └── commands/
        └── ... (optional skills)
```

---

## Best Practices

1. **Skills First**: Start with skills for simplicity
2. **Clear Names**: Use kebab-case for all file names
3. **Simple Instructions**: Write clear, concise descriptions
4. **One Task Per Skill**: Don't overload a single command
5. **Test Locally**: Test each skill before sharing
6. **Document Examples**: Show expected inputs and outputs

---

## Troubleshooting

### Skills Not Appearing

- Ensure `.claude/commands/` directory exists
- Check file names use `.md` extension
- Restart Claude Code application
- Verify folder structure matches exactly

### MCP Server Not Connecting

- Verify configuration file path is correct
- Ensure Python/executable is in PATH
- Check JSON syntax in claude.json
- Look for error messages in Claude Desktop logs
- Restart Claude Desktop completely

---

## Next Steps

1. Choose Skills or MCP Server based on your needs
2. Create the configuration files
3. Test with a sample YouTube URL
4. Customize the commands for your workflow
5. Share the setup with your team

For more information about MCP servers, visit the [Anthropic MCP documentation](https://modelcontextprotocol.io/).
