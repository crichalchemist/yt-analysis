# Best Practices Guide: MCP Servers and Claude Code Skills

## Quick Reference

| Aspect | MCP Servers | Claude Code Skills |
|--------|------------|-------------------|
| **File Type** | Python/Node/any executable | Markdown `.md` |
| **Location** | Project directory + config | `.claude/commands/` |
| **Setup Time** | 10-15 minutes | 2-5 minutes |
| **Complexity** | Medium-High | Low |
| **Use When** | Persistent tools, integrations | Workflows, tasks |
| **Best For** | Claude Desktop + Code | Claude Code workflows |

## MCP Server Best Practices

### 1. Structure Your MCP Server

**Minimal Example (Python):**

```python
#!/usr/bin/env python3
"""yt-analysis MCP Server"""

import json
import sys

def handle_init(params):
    """Initialize the server"""
    return {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "serverInfo": {
            "name": "yt-analysis",
            "version": "1.0.0"
        }
    }

def handle_call_tool(name, arguments):
    """Handle tool calls"""
    tools = {
        "analyze_video": analyze_video,
        "get_transcript": get_transcript,
    }

    if name in tools:
        return tools[name](**arguments)
    return {"error": f"Unknown tool: {name}"}

def analyze_video(url):
    """Analyze a YouTube video"""
    # Implementation here
    return {"status": "success", "analysis": {...}}

def get_transcript(url):
    """Get video transcript"""
    # Implementation here
    return {"status": "success", "transcript": "..."}

def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break

        request = json.loads(line)

        if request["method"] == "initialize":
            response = handle_init(request.get("params", {}))
        elif request["method"] == "tools/call":
            response = handle_call_tool(
                request["params"]["name"],
                request["params"].get("arguments", {})
            )
        else:
            response = {"error": "Unknown method"}

        print(json.dumps(response))

if __name__ == "__main__":
    main()
```

### 2. Error Handling

Always return proper error responses:

```python
def handle_request(request):
    try:
        # Process request
        return {"success": True, "result": result}
    except ValueError as e:
        return {"error": f"Invalid input: {str(e)}"}
    except Exception as e:
        return {"error": f"Server error: {str(e)}"}
```

### 3. Configuration Best Practices

**Do:**
- Use absolute paths in configuration
- Test paths before adding to config
- Include helpful environment variables
- Document all configuration options
- Provide example configurations

**Don't:**
- Hardcode file paths in code
- Use relative paths like `./`
- Include secrets in configuration
- Mix different executable types

### 4. Performance Tips

- Minimize startup time
- Cache results when appropriate
- Return partial results for long operations
- Implement timeout handling
- Clean up resources properly

### 5. Documentation

Include with your MCP server:

```markdown
# yt-analysis MCP Server

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Add to Claude Desktop config

## Configuration

[Config section]

## Tools Provided

- `analyze_video`: Analyze YouTube video
- `get_transcript`: Extract video transcript

## Examples

[Usage examples]
```

## Claude Code Skills Best Practices

### 1. Naming Convention

Use kebab-case for all skill files:

```
Good:
- analyze-video.md
- download-transcript.md
- compare-videos.md

Avoid:
- analyzeVideo.md
- analyze_video.md
- AnalyzeVideo.md
```

### 2. Structure Template

Always use consistent structure:

```markdown
# [Clear Title]

[One-line description]

## What this command does

[Detailed steps as numbered list]

## How to use

[Usage syntax and examples]

**Example input:**
```
/command-name example
```

**Example output:**
```
Expected results
```

## Requirements

[Prerequisites]

## Tips

[Helpful hints]

## Related commands

[Links to similar skills]
```

### 3. Example Quality

Provide complete, realistic examples:

```markdown
## How to use

/analyze-video [youtube-url]

**Example input:**
```
/analyze-video https://www.youtube.com/watch?v=9bZkp7q19f0
```

**Example output:**
```
Video Analysis Report
====================
Title: Understanding Machine Learning
Duration: 15:42
Channel: TechEducation

Summary:
The video introduces fundamental ML concepts...

Topics:
- Supervised Learning
- Neural Networks
- Training Process
```
```

### 4. Keep It Focused

Each skill should do ONE thing well:

**Good:**
- `/analyze-video` - Analyzes single video
- `/download-transcript` - Extracts transcript only
- `/compare-videos` - Compares multiple videos

**Avoid:**
- `/do-everything` - Too broad
- `/video-operations` - Combines too many tasks

### 5. Progressive Disclosure

Start simple, allow complexity:

```markdown
## How to use

### Basic usage:
/analyze-video [url]

### Advanced options:
/analyze-video [url] --detailed --include-timestamps

### Examples:
[Examples here]
```

## Common Patterns

### Pattern 1: Input Processing

```markdown
# Process Input

Takes user input and processes it.

## How to use

/process [input]

**Example:**
/process "some data"
```

### Pattern 2: File Operations

```markdown
# Save Results

Processes data and saves to file.

## How to use

Provide the data, I'll save it to a file you can download.
```

### Pattern 3: Comparison

```markdown
# Compare Items

Compares multiple items and shows differences.

## How to use

/compare [item1] [item2] [item3]
```

### Pattern 4: Search/Filter

```markdown
# Search Data

Searches through data for specific items.

## How to use

/search [query] --in [domain]
```

## File Organization

### Minimal Setup

```
yt-analysis/
├── .claude/
│   └── commands/
│       ├── analyze-video.md
│       └── download-transcript.md
└── USAGE-GUIDE.md
```

### Full Setup

```
yt-analysis/
├── .claude/
│   └── commands/
│       ├── analyze-video.md
│       ├── download-transcript.md
│       ├── compare-videos.md
│       └── search-transcript.md
├── USAGE-GUIDE.md
├── SKILLS-GUIDE.md
├── MCP-CONFIG.md
└── yt_analysis/
    ├── server.py
    └── __init__.py
```

## Testing Your Skills

### Pre-launch Checklist

- [ ] Skill file in `.claude/commands/`
- [ ] File uses `.md` extension
- [ ] File name in kebab-case
- [ ] Can invoke skill in Claude Code
- [ ] Examples produce expected output
- [ ] Instructions are clear
- [ ] Related commands documented

### Testing Procedure

1. Create the skill file
2. Try example inputs
3. Verify output quality
4. Check edge cases
5. Refine instructions
6. Commit and deploy

## Version Control

### What to Commit

```
.claude/commands/         # Always commit
USAGE-GUIDE.md           # Always commit
SKILLS-GUIDE.md          # Always commit
MCP-CONFIG.md            # Always commit
yt_analysis/             # If using MCP server
```

### What to Gitignore

```
__pycache__/
*.pyc
.env
cache/
```

## Troubleshooting

### Skills Not Working

1. Check file location: `.claude/commands/filename.md`
2. Check file extension: Must be `.md`
3. Check naming: Must use kebab-case
4. Restart Claude Code
5. Check for typos in instructions

### MCP Server Connection Issues

1. Validate JSON syntax in claude.json
2. Test server manually: `python -m yt_analysis.server`
3. Verify paths are absolute
4. Check permissions on executable
5. Restart Claude Desktop

### Performance Issues

1. Optimize server startup time
2. Implement result caching
3. Provide streaming responses
4. Handle timeouts gracefully
5. Profile bottlenecks

## Choosing Between Skills and MCP Servers

### Use Skills When

- Creating workflows or procedures
- Documenting repeatable tasks
- Building on existing Claude capabilities
- No external tool integration needed
- Quick setup is priority
- Sharing with non-technical users

### Use MCP Servers When

- Need persistent tools in Claude Desktop
- Integrating external services
- Complex logic required
- Performance-critical operations
- Need data persistence
- Building plugin ecosystem

## Scaling Your Integration

### Stage 1: Single Skill

```
1. Create one .md file in .claude/commands/
2. Test with example inputs
3. Document usage
```

### Stage 2: Multiple Skills

```
1. Create skill library in .claude/commands/
2. Document each skill thoroughly
3. Create SKILLS-GUIDE.md
4. Link related skills
```

### Stage 3: MCP Server

```
1. Identify repeated patterns
2. Build MCP server with common logic
3. Configure in Claude Desktop
4. Keep skills for workflows
```

## Examples Repository

Share your skills in a public repository:

```
yt-analysis/
├── README.md              # Project overview
├── USAGE-GUIDE.md         # Quick start
├── SKILLS-GUIDE.md        # Skill documentation
├── MCP-CONFIG.md          # Server configuration
├── .claude/
│   └── commands/          # Reusable skills
├── examples/              # Example videos, outputs
└── yt_analysis/           # Implementation (if using MCP)
```

## Community Sharing

When sharing your skills:

1. Clear documentation
2. Working examples
3. Easy setup instructions
4. Troubleshooting guide
5. Contributing guidelines

## Summary

- Start with Skills for simplicity
- Use MCP Servers for persistence
- Follow naming conventions
- Document thoroughly
- Test before deploying
- Scale as needed
- Share with community
