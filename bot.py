#!/usr/bin/env python3

"""
    The core module for the bot
"""

import questionparser
from textprocessor import preprocess, convert_tuples_to_string
from dataloader import load_data
from markov import MarkovChain
from segmenter import segment_words

class Bot:
    """
        The actual Bot based on the Markov Chain.
    """

    def __init__(self, markov_chain):
        if not markov_chain:
            raise ValueError("No MarkovChain supplied...")
        self.markov_chain = markov_chain

    def generate_reply(self, start, reply_len=10):
        """
            Generate a reply with markov chain process
        """
        words_generated = [ word for word in self.markov_chain.generate(start, reply_len) ]
        return words_generated

    def generate_segmented_reply(self, segment, reply_len=3):
        """
            Generate reply for the given segment.
            Every possible variations are generated for the segment
            to compensate for the grammar.

            Eg:
                doing i am => i am doing, i doing am, doing am i
        """
        bot = ""
        for keywords in questionparser.generate_variations(segment):
            keywords = questionparser.reflect(keywords)
            print("Variation : {}".format(keywords))
            reply = self.generate_reply(keywords, reply_len)
            if len(reply) == 1 and reply[0] == keywords:
                continue
            else:
                bot = convert_tuples_to_string(reply)
                break
        return bot

    def get_reply_len_for_segment(self, segment):
        length = len(segment)
        if length == 1:
            return 10
        elif length == 2:
            return 5
        else:
            return 3

    def run(self):
        while True:
            try:
                you = input("You >> ")
                words = questionparser.process(you)
                segments = segment_words(words, segment_size = 3, overlap = 1)
                replies = []

                for segment in segments:
                    print("Current segment : {}".format(segment))
                    reply_len  = self.get_reply_len_for_segment(segment)
                    bot = self.generate_segmented_reply(segment, reply_len = reply_len)
                    if bot:
                        replies.append(bot)
                print("Paradox >> {}".format(replies))
            except (KeyboardInterrupt, EOFError) as e:
                print("Bye. Cheers. Stay awesome...")
                break

def main():
    text = load_data("data/paradox")

    mc = MarkovChain()
    mc.train_ngram(1, text)
    mc.train_ngram(2, text)
    mc.train_ngram(3, text)

    bot = Bot(mc)
    bot.run()

if __name__ == "__main__":
    main()

