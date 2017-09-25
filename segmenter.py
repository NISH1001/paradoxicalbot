#!/usr/bin/env python3

def segment_text(text, segment_size=3, overlap=2):
    """
        Segment the given text into  n segments
    """
    words = text.split()
    return segment_words(words, segment_size, overlap)

def segment_words(words, segment_size=3, overlap=2):
    """
        Segment the given text into  n segments
    """
    if len(words) == 1 or len(words) < segment_size:
        return [ tuple(words) ]
    segments = []
    start = overlap if overlap > 0 else 0
    for i in range(start, len(words), segment_size - overlap):
        word = words[i - overlap : i + segment_size - overlap]
        if word:
            segments.append(tuple(word))
    return segments

def main():
    text = "i"
    segments = segment_text(text, segment_size = 4, overlap = 2)
    #segments = segment_words(text.split(), segment_size = 4, overlap = 2)
    print(segments)


if __name__ == "__main__":
    main()

