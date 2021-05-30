import random
import string

import nltk
import numpy as np
import tensorflow as tf
from nltk.stem import WordNetLemmatizer
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout


class TrainingModel:
    def __init__(self, words, classes, data_x, data_y):
        self.words = words
        self.classes = classes
        self.data_x = data_x
        self.data_y = data_y
        self.lemmatizer = WordNetLemmatizer()

    def train(self):

        words = [self.lemmatizer.lemmatize(word.lower()) for word in self.words if word not in string.punctuation]

        training = []
        out_empty = [0] * len(self.classes)

        for idx, doc in enumerate(self.data_x):
            bow = []
            text = self.lemmatizer.lemmatize(doc.lower())

            for word in words:
                bow.append(1) if word in text else bow.append(0)

            output_row = list(out_empty)
            output_row[self.classes.index(self.data_y[idx])] = 1

            training.append([bow, output_row])

        random.shuffle(training)
        training = np.array(training, dtype=object)

        train_x = np.array(list(training[:, 0]))
        train_y = np.array(list(training[:, 1]))

        input_shape = (len(train_x[0]),)
        output_shape = len(train_y[0])

        model = Sequential()
        model.add(Dense(128, input_shape=input_shape, activation="relu"))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation="relu"))
        model.add(Dropout(0.3))
        model.add(Dense(output_shape, activation="softmax"))
        adam = tf.keras.optimizers.Adam(learning_rate=0.01, decay=1e-6)
        model.compile(loss='categorical_crossentropy',
                      optimizer=adam,
                      metrics=["accuracy"])

        model.fit(x=train_x, y=train_y, epochs=200, verbose=1)

        return model

    def get_intent(self, model, command):
        bow = self.bag_of_words(command, self.words)
        result = model.predict(np.array([bow]))[0]
        thresh = 0.2

        y_pred = [[idx, res] for idx, res in enumerate(result) if res > thresh]
        y_pred.sort(key=lambda x: x[1], reverse=True)

        intent = self.classes[y_pred[0][0]]
        return intent

    def bag_of_words(self, command, words):
        tokens = self.clean_text(command)
        bow = [0] * len(words)

        for token in tokens:
            for idx, word in enumerate(words):
                if word == token:
                    bow[idx] = 1

        return np.array(bow)

    def clean_text(self, text):
        tokens = nltk.word_tokenize(text)
        tokens = [self.lemmatizer.lemmatize(word.lower()) for word in tokens]
        return tokens

    @staticmethod
    def get_response(tag, data):
        list_of_intents = data['intents']
        for intent in list_of_intents:
            if intent['tag'] == tag:
                if len(intent['response']) > 0:
                    return random.choice(intent['response'])
                else:
                    return None
