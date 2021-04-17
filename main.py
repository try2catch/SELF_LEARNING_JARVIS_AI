import json
import random
import string

import nltk
import numpy as np
import tensorflow as tf
from nltk.stem import WordNetLemmatizer
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout

# import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
#
# nltk.download('punkt')
# nltk.download('wordnet')

with open('config/config.json') as file:
    data = json.load(file)

words = []
classes = []
data_x = []
data_y = []

for intent in data['intents']:
    for utterance in intent['utterances']:
        tokens = nltk.word_tokenize(utterance)
        words.extend(tokens)
        data_x.append(utterance)
        data_y.append(intent['tag'])

    if intent['tag'] not in classes:
        classes.append(intent['tag'])

lemmatizer = WordNetLemmatizer()

words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in string.punctuation]
words = sorted(set(words))
classes = sorted(set(classes))

training = []
out_empty = [0] * len(classes)

for idx, doc in enumerate(data_x):
    bow = []
    text = lemmatizer.lemmatize(doc.lower())

    for word in words:
        bow.append(1) if word in text else bow.append(0)

    output_row = list(out_empty)
    output_row[classes.index(data_y[idx])] = 1

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

model.fit(x=train_x, y=train_y, epochs=300, verbose=1)


def clean_text(text):
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word.lower()) for word in tokens]
    return tokens


def bag_of_words(command, words):
    tokens = clean_text(command)
    bow = [0] * len(words)

    for token in tokens:
        for idx, word in enumerate(words):
            if word == token:
                bow[idx] = 1

    return np.array(bow)


def get_intent(command, words, classes):
    bow = bag_of_words(command, words)
    result = model.predict(np.array([bow]))[0]
    thresh = 0.3

    y_pred = [[idx, res] for idx, res in enumerate(result) if res > thresh]
    y_pred.sort(key=lambda x: x[1], reverse=True)

    return_list = []

    for pred in y_pred:
        return_list.append(classes[pred[0]])
    return return_list


def get_response(intents, data):
    tag = intents[0]
    list_of_intents = data['intents']
    for intent in list_of_intents:
        if intent['tag'] == tag:
            return random.choice(intent['response'])


while True:
    command = input("Enter your command :")
    intents = get_intent(command, words, classes)
    response = get_response(intents, data)
    print(intents, ' : ', response)
