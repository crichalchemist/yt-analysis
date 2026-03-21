# Claude Code Skills Guide

This guide explains how to create and use Claude Code skills for the yt-analysis project.

## What are Claude Code Skills?

Skills are simple Markdown files that define custom commands for Claude Code. They let you:
- Create reusable workflows
- Document repeatable tasks
- Define helpful commands with examples
- Share tasks with your team

## Directory Structure

All skills must be placed in `.claude/commands/` directory:

```
yt-analysis/
└── .claude/
    └── commands/
        ├── analyze-video.md
        ├── download-transcript.md
        └── search-transcript.md
```

## Skill File Format

Each skill is a Markdown file with this basic structure:

```markdown
# Skill Title

Brief description of what the skill does.

## What this command does

Detailed explanation of the steps and outcomes.

## How to use

Instructions for the user.

**Example input:**
```
/skill-name [parameters]
```

**Example output:**
```
Expected results
```

## Requirements

Prerequisites or dependencies.

## Tips

Helpful usage tips.

## Related commands

Links to other relevant skills.
```

## Creating a New Skill

### Step 1: Create the File

Create a new file in `.claude/commands/` with kebab-case naming:

```bash
touch .claude/commands/my-skill.md
```

### Step 2: Write the Skill

Copy the template above and fill in your details.

### Step 3: Test

Invoke the skill in Claude Code:

```
/my-skill [parameters]
```

### Step 4: Iterate

Refine the skill based on results.

## Example Skills

### Skill 1: Analyze Video

**File:** `.claude/commands/analyze-video.md`

```markdown
# Analyze YouTube Video

Analyze a YouTube video for insights, transcript, and metadata.

## What this command does

1. Extract video metadata (title, duration, channel, upload date)
2. Retrieve and process the video transcript
3. Generate a summary of key points
4. Identify main topics discussed

## How to use

/analyze-video [video-url]

**Example:**
/analyze-video https://www.youtube.com/watch?v=dQw4w9WgXcQ

## Requirements

- Valid YouTube URL
- Video must have captions

## Tips

- Works best with educational videos
- Manual captions are more accurate than auto-generated
```

### Skill 2: Compare Videos

**File:** `.claude/commands/compare-videos.md`

```markdown
# Compare Videos

Compare insights, topics, and themes from multiple YouTube videos.

## What this command does

1. Analyze each video separately
2. Extract key topics from each
3. Compare and contrast approaches
4. Identify common themes
5. Highlight unique perspectives

## How to use

/compare-videos [url1] [url2] [url3...]

**Example:**
/compare-videos https://youtube.com/watch?v=A https://youtube.com/watch?v=B

## Requirements

- At least 2 YouTube video URLs
- Videos in same general topic work best

## Tips

- Limit to 3-4 videos for best analysis
- Works well for comparing different perspectives on same topic
```

### Skill 3: Extract Key Points

**File:** `.claude/commands/extract-key-points.md`

```markdown
# Extract Key Points

Extract the most important points from a video transcript.

## What this command does

1. Fetch video transcript
2. Identify main concepts
3. Extract specific claims and findings
4. Format as bullet-point summary
5. Include timestamps for each point

## How to use

/extract-key-points [video-url] [max-points]

**Example:**
/extract-key-points https://youtube.com/watch?v=dQw4w9WgXcQ 10

## Parameters

- `video-url`: YouTube URL
- `max-points`: Maximum number of key points (optional, default: 5)

## Tips

- Output is best for quick summaries
- Useful for research and citations
```

## Skill Naming Conventions

Use kebab-case (lowercase with hyphens):

- Good: `analyze-video.md`, `download-transcript.md`, `compare-videos.md`
- Avoid: `AnalyzeVideo.md`, `analyze_video.md`, `analyzeVideo.md`

The command name becomes: `/analyze-video` (filename without `.md`)

## Best Practices

1. **One task per skill** - Don't make multi-purpose commands
2. **Clear titles** - Use descriptive names
3. **Brief descriptions** - Users understand quickly
4. **Show examples** - Include expected input/output
5. **Document parameters** - Explain what users need to provide
6. **Include tips** - Share helpful usage hints
7. **Link related commands** - Help users discover other skills

## Skill Structure Template

Use this template for consistency:

```markdown
# Command Title

One-line description of what this does.

## What this command does

Detailed steps that will be performed:
1. Step one
2. Step two
3. Step three

## How to use

/command-name [parameter description]

**Example input:**
```
/command-name example-input
```

**Example output:**
```
Expected output format
```

## Requirements

- Required tools or access
- Necessary file formats
- External dependencies

## Tips

- Usage tip 1
- Usage tip 2
- Common gotchas

## Related commands

- `/another-command` - Brief description
- `/related-skill` - Brief description
```

## Managing Multiple Skills

As you add more skills, keep them organized:

```
.claude/commands/
├── analyze-video.md          # Single video analysis
├── compare-videos.md         # Multiple video comparison
├── download-transcript.md    # Transcript extraction
├── extract-key-points.md     # Key point extraction
├── search-transcript.md      # Transcript search
└── generate-summary.md       # Summary generation
```

## Testing Skills

Before sharing, test each skill:

1. **Test with examples** - Use provided examples
2. **Test edge cases** - Try unusual inputs
3. **Verify output** - Check results make sense
4. **Check documentation** - Review instructions

## Sharing Skills

To share skills with your team:

1. Commit `.claude/commands/` to git
2. Push to repository
3. Share the usage guide with team
4. Document any setup requirements

## Updating Skills

When you improve a skill:

1. Edit the `.md` file
2. Update examples if behavior changed
3. Commit and push
4. Notify users of changes

## Common Patterns

### Pattern 1: Single Input Processing

```markdown
/command [input]

Processes one item and returns results
```

### Pattern 2: Multiple Parameters

```markdown
/command [param1] [param2] [param3]

Processes multiple parameters
```

### Pattern 3: File-based

```markdown
/command

Ask for file input in conversation
```

### Pattern 4: Conditional

```markdown
/command [input] [--option]

Processes input with optional flags
```

## Limitations and Capabilities

Skills can:
- Define workflows and instructions
- Provide reusable prompts
- Document procedures
- Guide multi-step processes

Skills cannot:
- Execute external programs directly
- Access files outside the project
- Run arbitrary code
- Modify system configuration

For more advanced functionality, consider an MCP server.

## Troubleshooting

### Skill doesn't appear

- Check file is in `.claude/commands/`
- Verify `.md` file extension
- Check file name uses kebab-case
- Restart Claude Code application

### Skill runs but produces poor results

- Clarify instructions in the skill
- Add more detailed examples
- Break into multiple skills
- Provide additional context

### Need more power?

- Consider creating an MCP server
- Use MCP servers for persistent tools
- Skills are best for workflows

## Next Steps

1. Create your first skill using the template
2. Test it with example inputs
3. Refine based on results
4. Share with your team
5. Build a library of useful skills
