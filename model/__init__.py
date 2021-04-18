import json
import ssl

import nltk

# Downloading the nltk data
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt')
nltk.download('wordnet')

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

words = sorted(set(words))
classes = sorted(set(classes))
