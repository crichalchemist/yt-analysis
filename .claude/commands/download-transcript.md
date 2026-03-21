# Download Transcript

Extract and save the transcript from a YouTube video as a formatted text file.

## What this command does

When you provide a YouTube URL, I will:
1. Fetch the video's transcript or captions
2. Clean and format the text for readability
3. Remove unnecessary timestamps if desired
4. Save the transcript to a file you can download
5. Include metadata at the top (title, duration, date)

## How to use

Type `/download-transcript` and then provide a YouTube video URL when prompted.

**Example input:**
```
/download-transcript https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

**Example output:**
```
YouTube Transcript
Title: Video Title
Channel: Channel Name
Duration: XX:XX:XX
URL: [video-url]

[Full transcript text]
```

## Options

- Include timestamps: Yes/No
- Format: Plain text or formatted with sections
- Language: Auto-detect or specify

## Requirements

- YouTube video URL
- Video must have captions or transcript available
- Transcripts work better than auto-generated captions for accuracy

## Tips

- Use this to search through large videos easily
- Great for finding specific quotes or information
- Helpful for creating notes or summaries
- Can be used with other analysis tools

## Related commands

- `/analyze-video` - Get full analysis with summary and insights
- `/search-transcript` - Search for specific keywords in transcripts
