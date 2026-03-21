# yt-analysis Documentation Index

Complete reference guide for all documentation files.

## Documentation Files Overview

### For First-Time Users

**Start here:** `QUICKSTART.md`
- 5-minute overview
- Get running immediately
- Basic concepts explained
- Common tasks

**Then read:** `USAGE-GUIDE.md`
- Detailed usage instructions
- Skills vs MCP servers explained
- Setup instructions for both
- Comparison table

### For Skill Users

**Learn skills:** `SKILLS-GUIDE.md`
- What are skills
- How to create skills
- Skill file format
- Best practices
- Examples and templates
- Naming conventions

**Reference:** `.claude/commands/`
- `analyze-video.md` - Full video analysis
- `download-transcript.md` - Extract transcript
- `compare-videos.md` - Compare multiple videos

### For MCP Server Users

**Configure servers:** `MCP-CONFIG.md`
- Configuration file location
- Basic setup examples
- Platform-specific examples (MacOS/Windows/Linux)
- Multiple server setup
- Debugging guide

**Implementation patterns:** `BEST-PRACTICES.md` (MCP section)
- Server structure
- Error handling
- Performance tips
- Documentation guidelines

### For Advanced Users

**All patterns and practices:** `BEST-PRACTICES.md`
- Quick reference table
- MCP server best practices
- Claude Code skills best practices
- Common patterns
- File organization
- Testing procedures
- Troubleshooting
- Choosing between approaches

---

## Reading Paths

### Path 1: Quick Start (Recommended for most users)

1. `QUICKSTART.md` - Understand basics (5 min)
2. Try a skill in Claude Code (2 min)
3. `USAGE-GUIDE.md` - Learn about both approaches (10 min)
4. Done! You're ready to use

**Total time: 20 minutes**

### Path 2: Skill Developer

1. `QUICKSTART.md` - Get oriented (5 min)
2. `SKILLS-GUIDE.md` - Learn skill creation (15 min)
3. Create your first skill (10 min)
4. `BEST-PRACTICES.md` - Optimize your skills (10 min)

**Total time: 40 minutes**

### Path 3: Full Integration

1. `QUICKSTART.md` - Overview (5 min)
2. `USAGE-GUIDE.md` - Both approaches (10 min)
3. `SKILLS-GUIDE.md` - Skill creation (15 min)
4. `MCP-CONFIG.md` - Server setup (15 min)
5. `BEST-PRACTICES.md` - Advanced patterns (20 min)

**Total time: 65 minutes**

---

## Quick Reference

### File Locations

**Skills directory:**
```
yt-analysis/
└── .claude/
    └── commands/
        ├── analyze-video.md
        ├── download-transcript.md
        └── compare-videos.md
```

**MCP configuration:**
- MacOS/Linux: `~/.config/claude/claude.json`
- Windows: `%APPDATA%\Claude\claude.json`

### Command Invocation

**In Claude Code:**
```
/analyze-video [youtube-url]
/download-transcript [youtube-url]
/compare-videos [url1] [url2]
```

**In Claude Desktop:**
Available in tools panel if MCP server configured

### File Naming Rules

- Kebab-case for skills: `analyze-video.md` (not `analyzeVideo.md`)
- `.md` extension required
- Command name derived from filename without `.md`

---

## Document Purposes

### QUICKSTART.md
**Purpose:** Get you started immediately
**Best for:** First-time users
**Length:** 5 minutes
**Contains:** Basic concepts, common tasks, quick troubleshooting

### USAGE-GUIDE.md
**Purpose:** Complete usage instructions
**Best for:** Users deciding approach or learning in detail
**Length:** 10-15 minutes
**Contains:**
- Option 1: Claude Code Skills (simplest)
- Option 2: MCP Servers (advanced)
- Comparison table
- Setup instructions
- Step-by-step examples
- Troubleshooting

### SKILLS-GUIDE.md
**Purpose:** Create and manage Claude Code skills
**Best for:** Skill developers and creators
**Length:** 15-20 minutes
**Contains:**
- What skills are
- Creating new skills
- File format and structure
- Example skills with code
- Naming conventions
- Best practices
- Testing procedures
- Managing multiple skills

### MCP-CONFIG.md
**Purpose:** Configure MCP servers
**Best for:** Advanced users wanting Claude Desktop integration
**Length:** 10-15 minutes
**Contains:**
- Config file locations
- Basic configuration
- Full configuration with env vars
- Platform-specific examples
- Multiple server setup
- Debugging guide
- Advanced examples

### BEST-PRACTICES.md
**Purpose:** Comprehensive best practices and patterns
**Best for:** Developers and teams
**Length:** 20-30 minutes
**Contains:**
- Quick reference table
- MCP server patterns and practices
- Skills patterns and practices
- Naming conventions
- File organization
- Testing procedures
- Version control guidance
- Troubleshooting
- Choosing approaches
- Scaling strategies
- Community sharing

---

## Choosing What to Read

### "I want to analyze YouTube videos quickly"
Read: `QUICKSTART.md` → Try a skill → Done

### "I want to understand my options"
Read: `USAGE-GUIDE.md` → `QUICKSTART.md` if you choose skills

### "I want to create custom skills"
Read: `SKILLS-GUIDE.md` → Create skills → Reference `BEST-PRACTICES.md`

### "I want full Claude Desktop integration"
Read: `MCP-CONFIG.md` → Setup server → Reference `BEST-PRACTICES.md`

### "I want to understand everything"
Read all documents in this order:
1. QUICKSTART.md
2. USAGE-GUIDE.md
3. SKILLS-GUIDE.md
4. MCP-CONFIG.md
5. BEST-PRACTICES.md

---

## Key Concepts

### Skills
- Simple Markdown files in `.claude/commands/`
- Instant, no setup required
- File-based configuration
- Perfect for workflows and procedures
- Example: `.claude/commands/analyze-video.md`

### MCP Servers
- Executable programs (Python, Node, etc.)
- Configured in Claude Desktop config
- Persistent tools
- Full integration with Claude Desktop
- Better for complex logic and integrations

### Commands
- Invoked with `/` prefix in Claude Code
- Named from skill filename (without `.md`)
- Example: `/analyze-video`

### MCP Resources
- Tools and resources provided by MCP server
- Available in Claude Desktop tools panel
- Persistent across sessions

---

## Getting Help

### Skill Not Working?
1. Check `SKILLS-GUIDE.md` troubleshooting section
2. Verify file location: `.claude/commands/`
3. Verify filename format: kebab-case with `.md`
4. Restart Claude Code

### MCP Server Not Connecting?
1. Check `MCP-CONFIG.md` debugging section
2. Verify configuration file location
3. Verify JSON syntax is valid
4. Restart Claude Desktop

### Want to Learn More?
1. Check `BEST-PRACTICES.md` for your topic
2. Look at example files in `.claude/commands/`
3. Read related sections in comprehensive guides

---

## Directory Structure

```
yt-analysis/
├── README.md                          # Project overview
├── QUICKSTART.md                      # Quick start guide
├── USAGE-GUIDE.md                     # Usage instructions
├── SKILLS-GUIDE.md                    # Skill creation guide
├── MCP-CONFIG.md                      # MCP server configuration
├── BEST-PRACTICES.md                  # Best practices reference
├── DOCUMENTATION-INDEX.md             # This file
└── .claude/
    └── commands/
        ├── analyze-video.md           # Analyze single video skill
        ├── download-transcript.md     # Extract transcript skill
        └── compare-videos.md          # Compare multiple videos skill
```

---

## Using These Guides

### For Teams Sharing Skills

1. Commit all files to git
2. Share repository with team
3. Team reads `QUICKSTART.md` first
4. Share `.claude/commands/` with team
5. Team can immediately use skills

### For Distributing to Packages

1. Include all documentation files
2. Include `.claude/commands/` directory
3. Provide clear setup instructions
4. Link to appropriate documentation

### For Contributing

1. Follow patterns in `BEST-PRACTICES.md`
2. Use templates from `SKILLS-GUIDE.md`
3. Test using procedures in `BEST-PRACTICES.md`
4. Update relevant documentation

---

## Documentation Maintenance

### When Adding Skills
1. Update `.claude/commands/` with new skill
2. Update `SKILLS-GUIDE.md` with example if useful
3. Add to this index if major skill
4. Update `QUICKSTART.md` if adds major capability

### When Updating MCP Server
1. Update `MCP-CONFIG.md` with new config
2. Update `BEST-PRACTICES.md` if patterns change
3. Update implementation examples

### When Making Breaking Changes
1. Update all affected documentation
2. Add migration guide if needed
3. Update examples
4. Note in `USAGE-GUIDE.md`

---

## Summary

- **New users:** Start with `QUICKSTART.md`
- **Skill creators:** Read `SKILLS-GUIDE.md`
- **Advanced users:** Read `BEST-PRACTICES.md`
- **Config help:** Check `MCP-CONFIG.md`
- **All details:** See `USAGE-GUIDE.md`

Each document is self-contained but references others for deeper learning.
