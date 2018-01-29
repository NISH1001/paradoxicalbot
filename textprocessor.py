#!/usr/bin/env python3

import re
from collections import Counter

def reduce_whitespaces(text):
    return re.sub(r"[\s\n]+", " ", text)

def preprocess(text):
    #return reduce_whitespaces(re.sub(r"[\[\],\"'!()?]+", "", text))
    return reduce_whitespaces(re.sub(r"[()]+", "", text))

def split_text(text):
    regex = "[A-Za-z]+(?:'[A-Za-z]+)*"
    return re.compile(regex).findall(text)

def convert_tuples_to_string(tuples):
    tuples_str = map(lambda tup : ' '.join(tup), tuples)
    return ' '.join(tuples_str)

def create_lookup_tables(text):
    counts = Counter(text)
    vocab = sorted(counts, key=counts.get, reverse=True)
    vocab_to_int = {  word: ii for ii, word in enumerate(vocab, 1) }
    int_to_vocab = {  ii: word for ii, word in enumerate(vocab, 1) }
    return vocab_to_int, int_to_vocab

def token_lookup():
    """
    Generate a dict to turn punctuation into a token.
    :return: Tokenize dictionary where the key is the punctuation and the value is the token
    """
    punc_map = {'.': '||period||',
                  ',': '||comma||',
                  '"': '||quotation_mark||',
                  ';': '||semicolon||',
                  '!': '||exclamation_mark||',
                  '?': '||question_mark||',
                  '(': '||left_parentheses||',
                  ')': '||right_parentheses||',
                  '--': '||dash||',
                  '\n': '||return||'}
    return punc_map

def preprocess_all(text):
    data = reduce_whitespaces(text)
    data = preprocess(text)

    token_dict = token_lookup()
    for key, token in token_dict.items():
        data = data.replace(key, ' {} '.format(token))

    data = data.lower()
    data = data.split()
    vocab_to_int, int_to_vocab = create_lookup_tables(data)
    int_text = [ vocab_to_int[word] for word in data ]
    return int_text, vocab_to_int, int_to_vocab, token_dict

def main():
    text = "hello i am nishan. i'm good. dog'"
    print(split_text(text))

if __name__ == "__main__":
    main()

