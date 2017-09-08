#!/usr/bin/env python3
import re

def reduce_whitespaces(text):
    return re.sub(r"[\s\n]+", " ", text)

def preprocess(text):
    return reduce_whitespaces(re.sub(r"[,\.'!()]+", "", text))

def main():
    pass

if __name__ == "__main__":
    main()

