# Quick Start Guide

Get started with yt-analysis in 5 minutes using Claude Code skills.

## Absolute Quickest Start (5 minutes)

### 1. Understand What You Have

You now have 3 skills available:

- **`/analyze-video`** - Get full analysis of a YouTube video
- **`/download-transcript`** - Extract the transcript
- **`/compare-videos`** - Compare multiple videos

### 2. Try Your First Skill

In Claude Code, type:

```
/analyze-video https://www.youtube.com/watch?v=your_video_id
```

That's it! Claude will analyze the video for you.

### 3. Try More Skills

```
/download-transcript https://www.youtube.com/watch?v=your_video_id
```

```
/compare-videos https://www.youtube.com/watch?v=video1 https://www.youtube.com/watch?v=video2
```

## Next Steps

- **Read more:** See detailed guides below
- **Customize:** Create your own skills
- **Share:** Add these to your team's projects

---

## Understanding the Setup

### What are Skills?

Skills are custom commands that extend Claude Code. Each skill is a simple instruction file (Markdown format).

### Where are Skills Located?

```
yt-analysis/
└── .claude/
    └── commands/
        ├── analyze-video.md
        ├── download-transcript.md
        └── compare-videos.md
```

### How to Create Your Own Skill

1. Create a new `.md` file in `.claude/commands/`
2. Write instructions using the skill template
3. Save and test in Claude Code

Example: Create `.claude/commands/my-skill.md`

```markdown
# My Skill

This does something helpful.

## How to use

/my-skill [parameter]

**Example:**
/my-skill example input
```

Then use it: `/my-skill example input`

---

## Common Tasks

### Task 1: Analyze a Video

```
User: /analyze-video [YouTube URL]
Claude: Returns analysis with summary and key points
```

### Task 2: Get Just the Transcript

```
User: /download-transcript [YouTube URL]
Claude: Returns clean, formatted transcript
```

### Task 3: Compare Videos

```
User: /compare-videos [URL1] [URL2]
Claude: Shows differences and similarities
```

### Task 4: Find Specific Information

```
User: /analyze-video [URL]
Claude: [Full analysis]

User: Can you find the section about [topic]?
Claude: Extracts and highlights that section
```

---

## Available Documentation

### For Quick Users
- This file (5-minute overview)

### For Skill Users
- `SKILLS-GUIDE.md` - Learn to create skills
- `USAGE-GUIDE.md` - Detailed usage and configuration

### For Advanced Users
- `MCP-CONFIG.md` - Configure MCP servers
- `BEST-PRACTICES.md` - Best practices and patterns

---

## Troubleshooting

### Skill doesn't appear in Claude Code

1. Check files are in `.claude/commands/`
2. Check file names use `.md` extension
3. Restart Claude Code
4. Check file names use kebab-case (e.g., `my-skill.md`, not `mySkill.md`)

### Skill runs but gives wrong results

1. Check that the YouTube URL is valid
2. Verify the video has captions/transcript
3. Try with a different video
4. Read the skill's "Tips" section for best practices

### I want to modify a skill

1. Edit the `.md` file in `.claude/commands/`
2. Update the instructions
3. Save the file
4. Test in Claude Code
5. The changes take effect immediately

---

## Advanced: Creating More Skills

Once you understand the basic pattern, create skills for your specific needs:

**Examples of skills you could create:**

- `/summarize-video` - Get a one-paragraph summary
- `/extract-quotes` - Find notable quotes
- `/analyze-channel` - Analyze multiple videos from a channel
- `/find-timestamps` - Find sections by topic
- `/generate-notes` - Create study notes from a video

**Template:**

```markdown
# Skill Name

One-line description.

## What this command does

1. Step one
2. Step two
3. Result

## How to use

/command-name [parameters]

**Example:**
/command-name example

## Tips

Helpful hints here.
```

Save as `.claude/commands/command-name.md` and use it!

---

## When to Use Alternatives

### Use Skills When:
- Creating workflows and procedures
- Documenting repeatable tasks
- Quick setup needed
- No external tools required

### Use MCP Server When:
- Need persistent tools in Claude Desktop
- Integrating external services
- Complex logic required
- Want Claude Desktop integration

See `MCP-CONFIG.md` for MCP Server setup.

---

## Next: Learning More

### Read these in order:

1. **This file** - You're reading it now (overview)
2. **USAGE-GUIDE.md** - Detailed usage instructions
3. **SKILLS-GUIDE.md** - Learn to create skills
4. **BEST-PRACTICES.md** - Advanced patterns and tips

### If you want MCP Server integration:

1. **MCP-CONFIG.md** - Configuration examples
2. **BEST-PRACTICES.md** - Implementation tips

---

## Getting Help

### Common Questions

**Q: Where do I put skill files?**
A: In `.claude/commands/` directory (create it if it doesn't exist)

**Q: What format should skills use?**
A: Markdown (`.md` files with instructions)

**Q: Can I edit skills?**
A: Yes! Edit the `.md` file and changes take effect immediately.

**Q: How do I share skills with my team?**
A: Commit `.claude/commands/` to git and push to your repository.

**Q: Can I make skills do code?**
A: Skills define tasks for Claude. For actual code execution, use MCP servers.

**Q: How many skills can I have?**
A: As many as you want! Organize them logically.

---

## Summary

1. You have 3 ready-to-use skills
2. Type `/analyze-video [URL]` to get started
3. Create more skills by adding `.md` files
4. Follow the template for consistency
5. Read `SKILLS-GUIDE.md` to learn more

Happy analyzing!
