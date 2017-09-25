#!/usr/bin/env python3

def segment_text(text, segment_size=3, overlap=2):
    """
        Segment the given text into  n segments
    """
    words = text.split()
    segments = []
    start = overlap if overlap > 0 else 0
    for i in range(start, len(words), segment_size - overlap):
        word = words[i - overlap : i + segment_size - overlap]
        if word:
            segments.append(tuple(word))
    return segments

def segment_words(words, segment_size=3, overlap=2):
    """
        Segment the given text into  n segments
    """
    segments = []
    start = overlap if overlap > 0 else 0
    for i in range(start, len(words), segment_size - overlap):
        word = words[i - overlap : i + segment_size - overlap]
        if word:
            segments.append(tuple(word))
    return segments

def main():
    text = "what are you doing in your life"
    segments = segment_text(text, segment_size = 4, overlap = 2)
    print(segments)


if __name__ == "__main__":
    main()

