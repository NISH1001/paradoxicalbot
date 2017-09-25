#!/usr/bin/env python3

import itertools
import re

from textprocessor import preprocess

REFLECTION_UNI = {
    'i' : 'you',
    'you' : 'i',
    'your' : 'my',
    'am' : 'are'
}

REFLECTION_BI = {
    "i are" :   "i am",
    "to i"  :   "to me",
    "for i" :   "for me",
    "by i"  :   "by me"
}

pattern = re.compile(r'\b(' + '|'.join(REFLECTION_BI.keys()) + r')\b')

WORDS_WH = ['who', 'how', 'what', 'when', 'where', 'why', 'which', 'whom', 'whose']
WORDS_AUX = ['do', 'have']
WORDS_WH_AUX = ['do']

WH_AUX = list(itertools.product(WORDS_WH, WORDS_WH_AUX))

def reflect(words):
    """
        Reflects the words from question to reply.
        Eg:
            i -> you
            you -> i
    """
    words = map(lambda w : REFLECTION_UNI[w] if w in REFLECTION_UNI else w, words)
    words = pattern.sub(lambda x : REFLECTION_BI[x.group()], ' '.join(words))
    words = tuple(words.split(" "))
    return words

def is_wh(words):
    if len(words) < 1:
        return False
    return words[0] in WORDS_WH

def is_aux_question(words):
    if len(words) < 1:
        return False
    return words[0] in WORDS_AUX


def process_wh(words):
    return words[2:] if (words[0], words[1]) in WH_AUX else words[1:]

def process_aux_question(words):
    return words

def process(text):
    text = preprocess(text.strip())
    words = tuple(text.split(" "))
    if is_wh(words):
        words = process_wh(words)
    elif is_aux_question(words):
        words = process_aux_question(words)
    #words = reflect(words)
    return words

def generate_variations(words):
    for var in itertools.permutations(words):
        yield var

def main():
    reply = process("have you gone there")
    print(reply)

if __name__ == "__main__":
    main()

