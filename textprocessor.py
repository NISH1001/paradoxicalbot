#!/usr/bin/env python3
import re

def reduce_whitespaces(text):
    return re.sub(r"[\s\n]+", " ", text)

def preprocess(text):
    return reduce_whitespaces(re.sub(r"[,\.\"'!()?]+", "", text))

def convert_tuples_to_string(tuples):
    tuples_str = map(lambda tup : ' '.join(tup), tuples)
    return ' '.join(tuples_str)

def main():
    pass

if __name__ == "__main__":
    main()

