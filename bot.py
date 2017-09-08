#!/usr/bin/env python3

from textprocessor import preprocess

REFLECTION = {
    'i' : 'you',
    'you' : 'i',
    'your' : 'my',
    'they' : 'they',
    'we' : 'we'
}

WORDS_WH = ['who', 'how', 'when', 'where', 'why', 'which', 'whom', 'whose']

FILLERS = ['do']

def process(text):
    text = preprocess(text)
    words = text.split(" ")
    words = list(filter(lambda w : w not in WORDS_WH, words))
    words = list(map(lambda w : REFLECTION[w] if w in REFLECTION else w, words))
    words = list(filter(lambda w : w not in FILLERS, words))
    return words

def run():
    while True:
        try:
            you = input("You >> ")
            bot = process(you)
            print(bot)
        except KeyboardInterrupt:
            print("Bye. Cheers. Stay awesome...")
            break

def main():
    run()

if __name__ == "__main__":
    main()

