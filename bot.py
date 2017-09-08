#!/usr/bin/env python3

import random
import re

from textprocessor import preprocess, convert_tuples_to_string
from dataloader import load_data
from markov import MarkovChain

REFLECTION = {
    'i' : 'you',
    'you' : 'i',
    'your' : 'my',
    'they' : 'they',
    'we' : 'we'
}

WORDS_WH = ['who', 'how', 'what', 'when', 'where', 'why', 'which', 'whom', 'whose']

FILLERS = ['do']

def process(text):
    text = preprocess(text)
    words = text.split(" ")
    words = filter(lambda w : w not in WORDS_WH, words)
    words = map(lambda w : REFLECTION[w] if w in REFLECTION else w, words)
    words = tuple(filter(lambda w : w not in FILLERS, words))
    return words

def generate_reply(markov_chain, start):
    words_generated = [ word for word in markov_chain.generate(start, max_len=25) ]
    return convert_tuples_to_string(words_generated)

def run(markov_chain):
    while True:
        try:
            you = input("You >> ")
            keywords = process(you)
            print(keywords)
            bot = generate_reply(markov_chain, keywords)
            print(bot)
        except KeyboardInterrupt:
            print("Bye. Cheers. Stay awesome...")
            break

def main():
    text = load_data("data")
    mc = MarkovChain()
    mc.train_ngram(1, text)
    mc.train_ngram(2, text)
    mc.train_ngram(3, text)
    run(mc)

if __name__ == "__main__":
    main()

