#!/usr/bin/env python3

"""
    The module for markov chain
"""

import random
import re
from dataloader import load_data

class MarkovChain:
    def __init__(self):
        self.trie = {}

    def train(self, text, factor=1):
        """
            Create/Update the naive trie structure.
            For now, bigram model is used
        """
        words = filter(lambda s: len(s) > 0, re.split(r'[\s]', text))
        words  = list(map(str.lower, words))
        # generate bigrams
        word_pairs = [(words[i], words[i + 1]) for i in range(len(words) - 1)]
        for a, b in word_pairs:
            if a not in self.trie:
                self.trie[a] = {}
            self.trie[a][b] = factor if b not in self.trie[a] \
                    else self.trie[a][b] + self.trie[a][b] * factor

    def generate(self, start_with=None, max_len=5):
        """
            Yield a sequence of words
            until dead end is found or max length is exceeded
        """
        if len(self.trie) == 0:
            return
        # either start with a word or randomize it
        word = start_with if start_with is not None \
                else random.choice(list(self.trie.keys()))
        yield word

        #gen = (  (i for i in range(max_len)) or max_len == 0 )

        rand = lambda x : random.random() * x
        i = 0
        while max_len == 0 or i < max_len:
            # dead end
            i += 1
            if word not in self.trie:
                return

            # Otherwise, randomize against the weight of each leaf word divided
            # by the number of leaves.
            dist = sorted([(w, rand(self.trie[word][w] / len(self.trie[word]))) \
                           for w in self.trie[word]],
                          key=lambda k: 1-k[1])
            word = dist[0][0]
            yield word

def main():
    text = load_data("data")
    markov_chain = MarkovChain()
    markov_chain.train(text)
    start_word = "life"
    words_generated = [ word for word in markov_chain.generate(start_word, max_len=25) ]
    print(' '.join(words_generated))


if __name__ == "__main__":
    main()
