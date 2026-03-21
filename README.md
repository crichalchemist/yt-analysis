# yt-analysis

Claude + YouTube - Intelligent video analysis and transcription.

## Quick Start

Analyze YouTube videos in 5 minutes:

```bash
/analyze-video https://www.youtube.com/watch?v=your_video_id
```

## Documentation

Choose your path:

- **New users**: Read [QUICKSTART.md](QUICKSTART.md) (5 minutes)
- **Understanding options**: Read [USAGE-GUIDE.md](USAGE-GUIDE.md) (15 minutes)
- **Creating skills**: Read [SKILLS-GUIDE.md](SKILLS-GUIDE.md) (20 minutes)
- **Configuring MCP**: Read [MCP-CONFIG.md](MCP-CONFIG.md) (15 minutes)
- **Advanced topics**: Read [BEST-PRACTICES.md](BEST-PRACTICES.md) (30 minutes)
- **Finding your way**: Read [DOCUMENTATION-INDEX.md](DOCUMENTATION-INDEX.md)

## Available Skills

Three ready-to-use skills are included:

1. **`/analyze-video`** - Full analysis with metadata, transcript, and summary
2. **`/download-transcript`** - Extract and save video transcripts
3. **`/compare-videos`** - Compare insights from multiple videos

## Two Integration Options

### Option 1: Claude Code Skills (Simplest)
- No setup required
- Start immediately with `/analyze-video`
- Perfect for workflows and procedures
- See [QUICKSTART.md](QUICKSTART.md)

### Option 2: MCP Server (Most Powerful)
- Persistent tools in Claude Desktop
- Full system integration
- For complex workflows
- See [MCP-CONFIG.md](MCP-CONFIG.md)

## Setup Time

- **Skills only**: 2 minutes
- **With MCP Server**: 15 minutes
- **Full integration**: 30 minutes

## Key Features

- Extract YouTube video transcripts
- Analyze video content for key insights
- Compare multiple videos
- Works with manual captions for better accuracy
- Available in Claude Code and Claude Desktop

## Files

```
yt-analysis/
├── QUICKSTART.md              # Start here
├── USAGE-GUIDE.md             # Understand options
├── SKILLS-GUIDE.md            # Create skills
├── MCP-CONFIG.md              # Configure servers
├── BEST-PRACTICES.md          # Advanced reference
├── DOCUMENTATION-INDEX.md     # Navigation
├── DOCUMENTATION-MAP.md       # Visual guide
├── SETUP-SUMMARY.md           # What was created
└── .claude/
    └── commands/
        ├── analyze-video.md
        ├── download-transcript.md
        └── compare-videos.md
```

## Getting Started

1. **Read** [QUICKSTART.md](QUICKSTART.md) (5 minutes)
2. **Try** `/analyze-video [youtube-url]`
3. **Learn** [USAGE-GUIDE.md](USAGE-GUIDE.md) for more options
4. **Create** custom skills following [SKILLS-GUIDE.md](SKILLS-GUIDE.md)

## Support

- Issues with setup? See [USAGE-GUIDE.md](USAGE-GUIDE.md#troubleshooting)
- Creating skills? See [SKILLS-GUIDE.md](SKILLS-GUIDE.md)
- Advanced topics? See [BEST-PRACTICES.md](BEST-PRACTICES.md)
- Lost? See [DOCUMENTATION-INDEX.md](DOCUMENTATION-INDEX.md)
