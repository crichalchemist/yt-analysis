# Compare Videos

Compare insights, topics, and themes from multiple YouTube videos.

## What this command does

When you provide multiple YouTube video URLs, I will:
1. Analyze each video's transcript and content
2. Extract key topics and themes from each video
3. Identify common ground and overlapping topics
4. Highlight unique perspectives or differences
5. Create a comparison table or summary
6. Synthesize insights across all videos

## How to use

Type `/compare-videos` and provide multiple YouTube video URLs when prompted.

**Example input:**
```
/compare-videos https://www.youtube.com/watch?v=video1 https://www.youtube.com/watch?v=video2
```

**Example output:**
```
Video Comparison Analysis
==========================

Video 1: Title
Duration: XX:XX
Key Topics: Topic A, Topic B, Topic C

Video 2: Title
Duration: YY:YY
Key Topics: Topic A, Topic D, Topic E

Common Topics:
- Topic A (covered in both)
- [analysis of how each approaches it]

Unique Perspectives:
- Video 1: Topic B and C (not in Video 2)
- Video 2: Topic D and E (not in Video 1)

Synthesis:
[Comprehensive analysis comparing approaches and insights]
```

## Requirements

- At least 2 YouTube video URLs
- All videos must have transcripts or captions available
- Videos on related topics work best (optional but recommended)

## Tips

- Best results with 2-4 videos (more gets complex)
- Videos on the same topic show clearest comparisons
- Different presenters on same topic highlight varied approaches
- Works well for research and comparative analysis
- Great for identifying which video explains a concept better

## Tips for Best Results

1. **Topic Alignment**: Videos on same topic yield better comparisons
2. **Quality Transcripts**: Manual captions better than auto-generated
3. **Optimal Count**: 2-4 videos is the sweet spot (3 is ideal)
4. **Similar Length**: Videos of similar duration compare more easily
5. **Different Perspectives**: Videos from different creators show varied approaches

## Use Cases

- **Research**: Compare how different experts approach same topic
- **Learning**: See multiple explanations of the same concept
- **Product Reviews**: Compare different reviewers' perspectives
- **News Analysis**: Compare coverage of same event from different sources
- **Tutorial Selection**: Compare different teaching approaches

## Related commands

- `/analyze-video` - Detailed analysis of a single video
- `/extract-key-points` - Get main points from a video
- `/download-transcript` - Extract and save video transcript
