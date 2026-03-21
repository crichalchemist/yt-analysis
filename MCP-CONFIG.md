# MCP Server Configuration Examples

This document shows how to configure the yt-analysis MCP server for Claude Desktop.

## Configuration File Location

Find the Claude Desktop configuration file on your system:

- **MacOS:** `~/.config/claude/claude.json`
- **Windows:** `%APPDATA%\Claude\claude.json`
- **Linux:** `~/.config/claude/claude.json`

## Basic Configuration

Here's a minimal MCP server configuration for yt-analysis:

```json
{
  "mcpServers": {
    "yt-analysis": {
      "command": "python",
      "args": ["-m", "yt_analysis.server"]
    }
  }
}
```

## Full Configuration with Environment Variables

For more control, include environment variables and path information:

```json
{
  "mcpServers": {
    "yt-analysis": {
      "command": "python",
      "args": ["-m", "yt_analysis.server"],
      "env": {
        "PYTHONPATH": "/Users/yourname/projects/yt-analysis",
        "LOG_LEVEL": "INFO",
        "CACHE_DIR": "/tmp/yt-analysis-cache"
      }
    }
  }
}
```

## Multiple MCP Servers

If you have multiple MCP servers, add them all to the same `mcpServers` object:

```json
{
  "mcpServers": {
    "yt-analysis": {
      "command": "python",
      "args": ["-m", "yt_analysis.server"]
    },
    "another-mcp": {
      "command": "node",
      "args": ["/path/to/another-server/index.js"]
    },
    "third-server": {
      "command": "/usr/local/bin/my-server"
    }
  }
}
```

## Configuration by Platform

### MacOS Example

```json
{
  "mcpServers": {
    "yt-analysis": {
      "command": "python3",
      "args": ["-m", "yt_analysis.server"],
      "env": {
        "PYTHONPATH": "/Users/alice/code/yt-analysis"
      }
    }
  }
}
```

### Windows Example

```json
{
  "mcpServers": {
    "yt-analysis": {
      "command": "python",
      "args": ["-m", "yt_analysis.server"],
      "env": {
        "PYTHONPATH": "C:\\Users\\alice\\projects\\yt-analysis"
      }
    }
  }
}
```

### Linux Example

```json
{
  "mcpServers": {
    "yt-analysis": {
      "command": "python3",
      "args": ["-m", "yt_analysis.server"],
      "env": {
        "PYTHONPATH": "/home/alice/projects/yt-analysis"
      }
    }
  }
}
```

## Step-by-Step Setup

1. **Locate or create** `claude.json`:
   - If file doesn't exist, create it in the locations above

2. **Add the configuration**:
   - Copy the appropriate configuration example above
   - Replace paths with your actual project path
   - Ensure JSON syntax is valid (test with a JSON validator)

3. **Save the file**

4. **Restart Claude Desktop**:
   - Close Claude Desktop completely
   - Wait a few seconds
   - Reopen Claude Desktop

5. **Verify**:
   - Click the tools button in Claude Desktop
   - Look for "yt-analysis" in the available tools
   - It should show the available resources

## Debugging

### Check Configuration Syntax

Use a JSON validator online or run:
```bash
python -m json.tool ~/.config/claude/claude.json
```

### View Claude Desktop Logs

- **MacOS/Linux:** Check system logs or use Console app
- **Windows:** Check Event Viewer

### Test MCP Server Directly

```bash
python -m yt_analysis.server
```

Should show proper MCP protocol responses.

### Common Issues

| Issue | Solution |
|-------|----------|
| Server not appearing | Restart Claude Desktop, check JSON syntax |
| "Command not found" error | Verify Python is in PATH, use full path to python |
| Connection timeout | Check if server starts without errors |
| Permission denied | Ensure script is executable, check file permissions |

## Best Practices

1. **Use absolute paths** - Don't use relative paths or `~` in JSON
2. **Validate JSON** - Invalid JSON will prevent Claude Desktop from starting
3. **Test before deploying** - Run the server manually first
4. **Keep backups** - Save a copy of your claude.json
5. **Use version control** - Track your MCP server code

## Advanced: Node.js MCP Server

If your server is in Node.js instead of Python:

```json
{
  "mcpServers": {
    "yt-analysis": {
      "command": "node",
      "args": ["/path/to/yt-analysis/server.js"]
    }
  }
}
```

## Advanced: Shell Script MCP Server

You can also use shell scripts:

```json
{
  "mcpServers": {
    "yt-analysis": {
      "command": "bash",
      "args": ["/path/to/yt-analysis/server.sh"]
    }
  }
}
```

## Reverting Changes

If something goes wrong:

1. Open `claude.json`
2. Remove the entire `yt-analysis` block from `mcpServers`
3. Save the file
4. Restart Claude Desktop

The problematic server will no longer load.
