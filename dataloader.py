#!/usr/bin/env python3

from textprocessor import preprocess

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

