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

class Bot:
    def __init__(self, markov_chain):
        if not markov_chain:
            raise ValueError("No MarkovChain supplied...")
        self.markov_chain = markov_chain

    def process(self, text):
        text = preprocess(text)
        words = text.split(" ")
        words = filter(lambda w : w not in WORDS_WH and w not in FILLERS, words)
        words = map(lambda w : REFLECTION[w] if w in REFLECTION else w, words)
        return tuple(words)

    def generate_reply(self, start, reply_len=10):
        words_generated = [ word for word in self.markov_chain.generate(start, reply_len) ]
        return convert_tuples_to_string(words_generated)

    def run(self):
        while True:
            try:
                you = input("You >> ")
                keywords = self.process(you)
                print(keywords)
                bot = self.generate_reply(keywords, reply_len=10)
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

    bot = Bot(mc)
    bot.run()

if __name__ == "__main__":
    main()

