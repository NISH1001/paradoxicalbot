#!/usr/bin/env python3

import os
import pickle

from textprocessor import preprocess_all
from dataloader import load_data

def preprocess_and_save_data(dataset_path, preprocess_path):
    data = load_data(dataset_path)
    int_text, vocab_to_int, int_to_vocab, token_dict = preprocess_all(data)
    pickle.dump((int_text, vocab_to_int, int_to_vocab, token_dict), open(preprocess_path, 'wb'))

def load_preprocess(filename):
    """
    Load the Preprocessed Training data and return them in batches of <batch_size> or less
    """
    return pickle.load(open(filename, mode='rb'))

def save_params(params, filename):
    """
    Save parameters to file
    """
    pickle.dump(params, open(filename, 'wb'))


def load_params(filename):
    """
    Load parameters from file
    """
    return pickle.load(open(filename, mode='rb'))


def main():
    pass

if __name__ == "__main__":
    main()

