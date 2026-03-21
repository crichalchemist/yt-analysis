# Analyze YouTube Video

Analyze a YouTube video for key insights, transcript, and metadata.

## What this command does

When you provide a YouTube URL, I will:
1. Extract video metadata (title, duration, channel, upload date)
2. Retrieve and process the video transcript
3. Generate a concise summary of key points
4. Identify main topics and themes discussed
5. Extract any notable quotes or statistics

## How to use

Type `/analyze-video` and then provide a YouTube video URL when prompted.

**Example input:**
```
/analyze-video https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

**Example output:**
```
Video Analysis Report
=====================
Title: [Video Title]
Duration: [Duration]
Channel: [Channel Name]

Summary:
[Key points from the video]

Topics Covered:
- Topic 1
- Topic 2
- Topic 3

Notable Quotes:
"..." - [Timestamp]

Overall Insights:
[Analysis summary]
```

## Requirements

- YouTube video URL (full URL or watch ID)
- Video must have captions or transcript available
- Internet connection to fetch video metadata

## Tips

- Work better with educational or informational videos
- Transcripts provide more accurate analysis than auto-generated captions
- Longer videos may take more time to analyze

## Related commands

- `/download-transcript` - Extract and save just the transcript
- `/compare-videos` - Compare insights from multiple videos
