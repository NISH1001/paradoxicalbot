#!/usr/bin/env python3

import re

def reduce_whitespaces(text):
    return re.sub(r"[\s\n]+", " ", text)

def preprocess(text):
    return reduce_whitespaces(re.sub(r"[,\.'!()]+", "", text))


def load_data(filename):
    data = ""
    with open(filename, 'r') as f:
        data = preprocess(f.read())

    return data

def main():
    data = load_data("data")
    print(data)

if __name__ == "__main__":
    main()

