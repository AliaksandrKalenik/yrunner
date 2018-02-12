import requests
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop
import numpy as np
import os


class TextStyleTransfer(object):

    MAX_LEN = 40

    def __init__(self, train_data_url, weight_path='./nt_weights'):
        self.weight_path = weight_path
        self.train_data_url = train_data_url
        self.__model = None
        self.__train_data = None

    @property
    def train_data(self):
        if self.__train_data is None:
            self.__train_data = self.get_file(self.train_data_url)
        return self.__train_data

    @property
    def model(self):
        if self.__model is None:
            chars = sorted(list(set(self.train_data)))
            model = Sequential()
            model.add(LSTM(128, input_shape=(self.MAX_LEN, len(chars))))
            model.add(Dense(len(chars)))
            model.add(Activation('softmax'))
            optimizer = RMSprop(lr=0.01)
            model.compile(loss='categorical_crossentropy', optimizer=optimizer)
            self.__model = model
        return self.__model

    def get_file(self, url):
        result = requests.get(url)
        if result.status_code == 200:
            return result.content.decode()
        raise ValueError("Can't load data. Status code: {}. Error: {}".format(
            result.status_code, result.content
        ))

    def train(self, epochs=5):
        chars = sorted(list(set(self.train_data)))
        char_indices = dict((c, i) for i, c in enumerate(chars))
        print('corpus length:', len(self.train_data))
        print('total chars:', len(chars))
        step = 3
        sentences = []
        next_chars = []
        for i in range(0, len(self.train_data) - self.MAX_LEN, step):
            sentences.append(self.train_data[i: i + self.MAX_LEN])
            next_chars.append(self.train_data[i + self.MAX_LEN])
        print('nb sequences:', len(sentences))

        print('Vectorization...')
        X = np.zeros((len(sentences), self.MAX_LEN, len(chars)), dtype=np.bool)
        y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
        for i, sentence in enumerate(sentences):
            for t, char in enumerate(sentence):
                X[i, t, char_indices[char]] = 1
            y[i, char_indices[next_chars[i]]] = 1

        print('Build model...')
        self.model.fit(X, y, batch_size=128, epochs=epochs)
        self.model.save_weights(self.weight_path)

    def sample(self, preds, temperature=1.0):
        # helper function to sample an index from a probability array
        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)

    def next_given_seed(self, seed):
        chars = sorted(list(set(self.train_data)))
        char_indices = dict((c, i) for i, c in enumerate(chars))
        indices_char = dict((i, c) for i, c in enumerate(chars))
        generated = ''
        i, num_spaces = 0, 0
        while num_spaces < 1:
            x = np.zeros((1, self.MAX_LEN, len(chars)))
            for t, char in enumerate(seed):
                x[0, t, char_indices[char]] = 1.

            preds = self.model.predict(x, verbose=0)[0]
            next_index = self.sample(preds, 0.2)
            next_char = indices_char[next_index]
            if next_char == ' ' and i > 0:
                num_spaces += 1
            generated += next_char
            seed = seed[1:] + next_char
            i += 1

        return generated

    def fill_blanks(self, incomplete, debug=False):
        self.model.load_weights(self.weight_path)
        words = incomplete.split(" ")
        complete = ''
        blanks = {}
        blank_i = 0
        i, step = 0, 0
        for word in words:
            if word == "_":
                seed = complete[i - self.MAX_LEN + 1:i]
                filled_word = self.next_given_seed(seed + " ")
                blanks[blank_i] = filled_word
                if debug:
                    print("seed = {0}, generated = {1}".format(seed, filled_word))
                complete = complete + " " + filled_word
                i = i + len(filled_word) + 1
                blank_i += 1
            else:
                i = i + len(word) + 1
                complete = complete + " " + word
        return blanks


def main():
    weights_path = "./nt_weights"
    train_data = 'https://s3.amazonaws.com/text-datasets/nietzsche.txt'
    tst = TextStyleTransfer(train_data, weights_path)
    if not os.path.exists(weights_path):
        tst.train(20)
    tst.model.load_weights(weights_path)
    from termcolor import colored, cprint

    # TXT = "this is a long sentence, there are many like this in the _ but this one is mine.\
    # And why _ it not be? There are little _ in life that can do without such _ hype. Perhaps I read _ too much \
    # into the ordeal of the world."#open("sample.txt").read().lower()

    TXT_ORIGINAL = "IF WINTER comes, the poet Shelley asked, \"can Spring be far behind?\"\
    For the best part of a decade the answer as far as the world economy has been\
    concerned has been an increasingly weary \"Yes it can\". Now, though, after testing\
    the faith of the most patient souls with glimmers that came to nothing, things seem\
    to be warming up. It looks likely that this year, for the first time since 2010,\
    rich-world and developing economies will put on synchronised growth spurts."

    TXT = 'IF WINTER comes, the poet Shelley asked, "can Spring be _ behind?"\
    For the best part of a decade the _ as far as the world economy has been\
    concerned has been an _ weary "Yes it can". Now, though, after testing\
    the _ of the most patient souls with _ that came to nothing, things seem\
    to be warming up. It looks likely that this year, for the _ time since 2010,\
    rich-world and developing economies will put on synchronised growth spurts.'


    TXT = TXT.lower()
    CRED = '\033[91m'
    CEND = '\033[0m'
    res = []
    blanks = tst.fill_blanks(TXT, True)
    blanks_i = 0
    for word in TXT.split(" "):
        if word == "_":
            res.append(colored(blanks[blanks_i], on_color='on_yellow', attrs=['bold']))
            blanks_i += 1
        else:
            res.append(word)
    print(" ".join(res))


if __name__ == '__main__':
    main()
