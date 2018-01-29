#!/usr/bin/env python3

import numpy as np

import helper

from dataloader import load_data
from textprocessor import preprocess_all

import sys
import tensorflow as tf
from tensorflow.contrib import seq2seq

data_dir = "data/paradox"
save_dir = "models/"
num_epochs = 50
batch_size = 128
rnn_size = 1024
seq_length = 16
learning_rate = 0.001
show_every_n_batches = 11

# Check for a GPU
if not tf.test.gpu_device_name():
    print('WARNING!! No GPU found. Please use a GPU to train your neural network.')
else:
    print('WARNING!! Default GPU Device: {}'.format(tf.test.gpu_device_name()))

def get_tensors(loaded_graph):
    """
        Get input, initial state, final state, and probabilities tensor from <loaded_graph>
    """
    inputs = loaded_graph.get_tensor_by_name("inputs:0")
    initial_state = loaded_graph.get_tensor_by_name("initial_state:0")
    final_state = loaded_graph.get_tensor_by_name("final_state:0")
    probs = loaded_graph.get_tensor_by_name("probabilities:0")

    return (inputs, initial_state, final_state, probs)

def get_inputs():
    """
        Create Tensorflow Placeholders for:
            inputs, targets and learning rate
    """
    inputs = tf.placeholder(tf.int32, [None, None], name='inputs')
    targets = tf.placeholder(tf.int32, [None, None], name='targets')
    learning_rate = tf.placeholder(tf.float32, name='learning_rate')
    return (inputs, targets, learning_rate)

def get_init_cell(batch_size, rnn_size):
    """
        Initialize a RNN cell.
    """
    lstm = tf.contrib.rnn.BasicLSTMCell(rnn_size)
    cell = tf.contrib.rnn.MultiRNNCell([lstm]*2)

    initial_state = cell.zero_state(batch_size, tf.float32)
    initial_state = tf.identity(initial_state, name='initial_state')

    return (cell, initial_state)

def get_embed(input_data, vocab_size, embed_dim):
    """
        Create word embedding for input text
    """
    embedding = tf.Variable(tf.truncated_normal((vocab_size, embed_dim), stddev=0.25))
    embed = tf.nn.embedding_lookup(embedding, input_data)
    return embed

def build_rnn(cell, inputs):
    """
        Create RNN using RNN cell
    """
    outputs, final_state = tf.nn.dynamic_rnn(cell, inputs, dtype=tf.float32)
    final_state = tf.identity(final_state, name='final_state')
    return outputs, final_state

def build_nn(cell, rnn_size, input_data, vocab_size):
    """
        Create the neural netowrk with fully connected layer and activation
    """
    inputs = get_embed(input_data, vocab_size, rnn_size)
    outputs, final_state = build_rnn(cell, inputs)
    logits = tf.contrib.layers.fully_connected(outputs, vocab_size, activation_fn=None)
    return logits, final_state

def get_batches(int_text, batch_size, seq_length):
    """
        Return batches of input and target
    """
    slice_size = batch_size * seq_length
    n_batches = len(int_text) // slice_size

    # Slicing for making batches equal in size
    used_data = int_text[0:n_batches * slice_size + 1]
    batches = []

    for i in range(n_batches):
        input_batch = []
        target_batch = []

        for j in range(batch_size):
            start_idx = i * batch_size + j * seq_length
            end_idx = i * batch_size + (j + 1) * seq_length

            input_batch.append(used_data[start_idx: end_idx])
            target_batch.append(used_data[start_idx + 1: end_idx + 1])

        batches.append([input_batch, target_batch])

    return np.array(batches)

def pick_word(probabilities, int_to_vocab):
    """
        Pick the next word in the generated text
    """
    return int_to_vocab[np.argmax(probabilities)]

def train():
    print("Training...\nKeep calm and do other shit...")
    helper.preprocess_and_save_data(data_dir, save_dir + 'preprocess.p')
    int_text, vocab_to_int, int_to_vocab, token_dict = helper.load_preprocess(save_dir + 'preprocess.p')
    print("int_text size :: {}".format(len(int_text)))

    train_graph = tf.Graph()
    with train_graph.as_default():
        vocab_size = len(int_to_vocab)
        input_text, targets , lr = get_inputs()
        input_data_shape = tf.shape(input_text)
        cell, initial_state = get_init_cell(input_data_shape[0], rnn_size)
        logits, final_state = build_nn(cell, rnn_size, input_text, vocab_size)

        probabilities = tf.nn.softmax(logits, name='probabilities')

        cost = seq2seq.sequence_loss(
                logits,
                targets,
                tf.ones([input_data_shape[0], input_data_shape[1]])
            )
        optimizer = tf.train.AdamOptimizer(lr)

        # gradient clipping
        gradients = optimizer.compute_gradients(cost)
        capped_gradients = [(tf.clip_by_value(grad, -1., 1.), var) for grad, var in gradients]
        train_op = optimizer.apply_gradients(capped_gradients)

    batches = get_batches(int_text, batch_size, seq_length)

    with tf.Session(graph=train_graph) as sess:
        sess.run(tf.global_variables_initializer())
        for epoch_i in range(num_epochs):
            state = sess.run(initial_state, {input_text: batches[0][0]})

            for batch_i, (x, y) in enumerate(batches):
                feed = {
                    input_text: x,
                    targets: y,
                    initial_state: state,
                    lr: learning_rate}
                train_loss, state, _ = sess.run([cost, final_state, train_op], feed)

                # Show every <show_every_n_batches> batches
                if (epoch_i * len(batches) + batch_i) % show_every_n_batches == 0:
                    print('Epoch {:>3} Batch {:>4}/{}   train_loss = {:.3f}'.format(
                        epoch_i,
                        batch_i,
                        len(batches),
                        train_loss))
        # Save Model
        saver = tf.train.Saver()
        saver.save(sess, save_dir)
        print('Model Trained and Saved')

    helper.save_params((seq_length, save_dir), save_dir + 'params.p')

def generate(initial_words):
    print("Generating text from trained model...")
    print("Initial Words are :: {}".format(initial_words))
    _, vocab_to_int, int_to_vocab, token_dict = helper.load_preprocess(save_dir + 'preprocess.p')
    seq_length, load_dir = helper.load_params(save_dir + 'params.p')

    gen_length = 50
    gen_sentences = initial_words

    loaded_graph = tf.Graph()
    with tf.Session(graph=loaded_graph) as sess:
        # Load saved model
        loader = tf.train.import_meta_graph(load_dir + '.meta')
        loader.restore(sess, load_dir)

        # Get Tensors from loaded model
        input_text, initial_state, final_state, probs = get_tensors(loaded_graph)

        # Sentences generation setup
        prev_state = sess.run(initial_state, {input_text: np.array([[1]])})

        # Generate sentences
        for n in range(gen_length):
            # Dynamic Input
            dyn_input = [[vocab_to_int[word] for word in gen_sentences[-seq_length:]]]
            print("dyn_input :: {}".format(dyn_input))
            dyn_seq_length = len(dyn_input[0])
            print("dyn_seq_length :: {}".format(dyn_seq_length))

            # Get Prediction
            probabilities, prev_state = sess.run(
                [probs, final_state],
                {input_text: dyn_input, initial_state: prev_state})

            pred_word = pick_word(probabilities[0, dyn_seq_length-1, :], int_to_vocab)

            gen_sentences.append(pred_word)

        # Remove tokens
        generated_text = ' '.join(gen_sentences)
        for key, token in token_dict.items():
            ending = ' ' if key in ['\n', '(', '"'] else ''
            generated_text = generated_text.replace(' ' + token.lower(), key)
        generated_text = generated_text.replace('\n ', '\n')
        generated_text = generated_text.replace('( ', '(')

        print(generated_text)

def main():
    mode = sys.argv[1]
    if mode == "train":
        train()
    elif mode == "generate" and len(sys.argv[1:])>1:
        initial_words = sys.argv[2:]
        generate(initial_words)
    else:
        print("Oh shit! Invalid mode...")


if __name__ == "__main__":
    main()

