"""
MCP Server Wrapper
Exposes YouTube corpus analyzer tools via MCP for Claude Desktop integration.
"""

import os
import json
import logging
from pathlib import Path
from typing import Optional

from mcp.server import Server
from mcp.types import Tool, TextContent
from anthropic import Anthropic

from acquire import pull_channel, build_record
from index import init_db, insert_records, get_all_records
from extract import extract_all
from synthesize import build_constitution


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize MCP server
app = Server("youtube-corpus")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="pull_and_index",
            description="Pull all videos from a YouTube channel and index them in DuckDB",
            inputSchema={
                "type": "object",
                "properties": {
                    "channel_url": {
                        "type": "string",
                        "description": "YouTube channel URL"
                    },
                    "output_dir": {
                        "type": "string",
                        "description": "Output directory for data and database"
                    }
                },
                "required": ["channel_url", "output_dir"]
            }
        ),
        Tool(
            name="run_extraction",
            description="Extract features from all videos without features using Anthropic API",
            inputSchema={
                "type": "object",
                "properties": {
                    "output_dir": {
                        "type": "string",
                        "description": "Directory containing corpus.db"
                    }
                },
                "required": ["output_dir"]
            }
        ),
        Tool(
            name="generate_constitution",
            description="Generate constitution markdown from extracted features",
            inputSchema={
                "type": "object",
                "properties": {
                    "output_dir": {
                        "type": "string",
                        "description": "Directory containing corpus.db"
                    },
                    "min_views": {
                        "type": "integer",
                        "description": "Minimum view count threshold",
                        "default": 100000
                    }
                },
                "required": ["output_dir"]
            }
        ),
        Tool(
            name="query_corpus",
            description="Run a SQL query against the corpus database",
            inputSchema={
                "type": "object",
                "properties": {
                    "output_dir": {
                        "type": "string",
                        "description": "Directory containing corpus.db"
                    },
                    "sql_query": {
                        "type": "string",
                        "description": "SQL query to execute"
                    }
                },
                "required": ["output_dir", "sql_query"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    try:
        if name == "pull_and_index":
            return await handle_pull_and_index(arguments)
        elif name == "run_extraction":
            return await handle_run_extraction(arguments)
        elif name == "generate_constitution":
            return await handle_generate_constitution(arguments)
        elif name == "query_corpus":
            return await handle_query_corpus(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        logger.error(f"Tool {name} failed: {e}", exc_info=True)
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_pull_and_index(args: dict) -> list[TextContent]:
    """Handle pull_and_index tool call."""
    channel_url = args["channel_url"]
    output_dir = args["output_dir"]

    logger.info(f"Pulling channel: {channel_url}")

    # Pull channel data
    video_dirs = pull_channel(channel_url, output_dir)

    # Initialize database
    db_path = Path(output_dir) / "corpus.db"
    conn = init_db(str(db_path))

    # Build records
    records = []
    for video_dir in video_dirs:
        try:
            record = build_record(video_dir)
            if record:
                records.append(record)
        except Exception as e:
            logger.error(f"Failed to build record for {video_dir}: {e}")

    # Insert records
    count = insert_records(conn, records)
    conn.close()

    result = f"Successfully indexed {count} videos from channel"
    logger.info(result)

    return [TextContent(type="text", text=result)]


async def handle_run_extraction(args: dict) -> list[TextContent]:
    """Handle run_extraction tool call."""
    output_dir = args["output_dir"]

    # Get API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return [TextContent(type="text", text="Error: ANTHROPIC_API_KEY not set")]

    client = Anthropic(api_key=api_key)

    # Initialize database
    db_path = Path(output_dir) / "corpus.db"
    conn = init_db(str(db_path))

    # Run extraction
    count = extract_all(conn, client, output_dir)
    conn.close()

    result = f"Extracted features for {count} videos"
    logger.info(result)

    return [TextContent(type="text", text=result)]


async def handle_generate_constitution(args: dict) -> list[TextContent]:
    """Handle generate_constitution tool call."""
    output_dir = args["output_dir"]
    min_views = args.get("min_views", 100000)

    # Get API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return [TextContent(type="text", text="Error: ANTHROPIC_API_KEY not set")]

    client = Anthropic(api_key=api_key)

    # Initialize database
    db_path = Path(output_dir) / "corpus.db"
    conn = init_db(str(db_path))

    # Generate constitution
    constitution_path = Path(output_dir) / "constitution.md"
    result_path = build_constitution(conn, client, min_views, str(constitution_path))
    conn.close()

    if result_path:
        result = f"Constitution generated at: {result_path}"
    else:
        result = "Constitution generation failed"

    logger.info(result)

    return [TextContent(type="text", text=result)]


async def handle_query_corpus(args: dict) -> list[TextContent]:
    """Handle query_corpus tool call."""
    output_dir = args["output_dir"]
    sql_query = args["sql_query"]

    # Initialize database
    db_path = Path(output_dir) / "corpus.db"
    conn = init_db(str(db_path))

    try:
        # Execute query
        result = conn.execute(sql_query).fetchall()

        # Format as JSON
        result_json = json.dumps(result, indent=2, default=str)

        conn.close()

        return [TextContent(type="text", text=result_json)]
    except Exception as e:
        conn.close()
        return [TextContent(type="text", text=f"Query error: {str(e)}")]


async def main():
    """Run the MCP server."""
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
