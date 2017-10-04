#!/usr/bin/env python3

"""
    The module for markov chain
"""

import random
import re
from dataloader import load_data
from textprocessor import preprocess, convert_tuples_to_string

class MarkovChain:
    def __init__(self):
        self.trie = {}

    def train_ngram(self, n, text, factor=1):
        """
            Create/Update the naive trie structure.
            For now, bigram model is used
        """
        words = filter(lambda s: len(s) > 0, re.split(r'[\s]', text))
        words  = list(map(str.lower, words))
        # generate bigrams
        #word_pairs = [(words[i], words[i + 1]) for i in range(len(words) - 1)]
        nd = n*2
        for i in range(len(words) - nd - 1):
            ngram = []
            for j in range(nd):
                ngram.append(words[i+j])

            a = tuple(ngram[:n])
            b = tuple(ngram[n : nd])
            if a not in self.trie:
                self.trie[a] = {}
            self.trie[a][b] = factor if b not in self.trie[a] \
                    else self.trie[a][b] + 1 * factor

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
    text = load_data("data/philosophy")
    text = preprocess(text.lower())
    mc = MarkovChain()
    mc.train_ngram(1, text)
    mc.train_ngram(2, text)
    mc.train_ngram(3, text)
    print(mc.trie)

    """
    start_word = ('life', 'is',  )
    words_generated = [ word for word in mc.generate(start_word, max_len=25) ]
    print(words_generated)
    print(convert_tuples_to_string(words_generated))
    """


if __name__ == "__main__":
    main()
