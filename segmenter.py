#!/usr/bin/env python3

def segment_text(text, segment_size=3, overlap=2):
    """
        Segment the given text into  n segments
    """
    words = text.split()
    segments = []
    for i in range(0, len(words), segment_size - overlap):
        word = words[i - overlap : i + segment_size - overlap]
        if word:
            segments.append(tuple(word))
    return segments

def main():
    text = "hello i am paradox i am gru i am no one"
    segments = segment_text(text, segment_size = 3, overlap = -1)
    print(segments)


if __name__ == "__main__":
    main()

