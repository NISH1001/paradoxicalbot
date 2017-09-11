#!/usr/bin/env python3

import random
import re

import questionparser
from textprocessor import preprocess, convert_tuples_to_string
from dataloader import load_data
from markov import MarkovChain

class Bot:
    def __init__(self, markov_chain):
        if not markov_chain:
            raise ValueError("No MarkovChain supplied...")
        self.markov_chain = markov_chain

    def generate_reply(self, start, reply_len=10):
        words_generated = [ word for word in self.markov_chain.generate(start, reply_len) ]
        return convert_tuples_to_string(words_generated)

    def run(self):
        while True:
            try:
                you = input("You >> ")
                words = questionparser.process(you)
                bot = ""
                for keywords in questionparser.generate_variations(words):
                    bot = self.generate_reply(keywords, reply_len=10)
                    if convert_tuples_to_string([keywords]) != bot:
                        break
                print("Paradox >> {}".format(bot))
            except KeyboardInterrupt:
                print("Bye. Cheers. Stay awesome...")
                break

def main():
    text = load_data("soulstories")

    mc = MarkovChain()
    mc.train_ngram(1, text)
    mc.train_ngram(2, text)
    mc.train_ngram(3, text)

    bot = Bot(mc)
    bot.run()

if __name__ == "__main__":
    main()

