from __future__ import print_function

from collections import defaultdict, Counter
import random
import sys
import re
from flask import Flask, request, jsonify

STATE_LEN = 5

import pickle
import os

CACHE_FILE = 'markov_model.pkl'

app = Flask(__name__)

import textwrap

def format_text(text, width=80):
    text = text.capitalize()
    text = re.sub(r'(\. )([а-яa-z])', lambda m: m.group(1) + m.group(2).upper(), text)
    return textwrap.fill(text, width=width)

def save_model(states, filename=CACHE_FILE):
    with open(filename, 'wb') as f:
        pickle.dump(states, f)

def load_model(filename=CACHE_FILE):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    return None

# def weighted_from_counter(c):
#     total = sum(c.values())
#     idx = random.randrange(total)
#     for elem, count in c.most_common():
#         idx -= count
#         if idx < 0:
#             return elem

def weighted_from_counter(c):
    items = list(c.items())
    weights = [count ** 1.2 for _, count in items]  # Поднимаем в степень, чтобы усилить частотность
    return random.choices([item[0] for item in items], weights=weights)[0]

def get_data():
    files = []
    for filename in os.listdir("files"):
        if filename.endswith(".txt"):
            files.append("files/" + filename)

    data = ""
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()
            text = re.sub(r'\s+', ' ', text)
            data += text

        data += " "
    return data

def train_model():
    data = get_data()
    states = defaultdict(Counter)
    data = data.split()

    print('Learning model...')

    states = load_model()
    if states is None:
        print('Learning model...')
        states = defaultdict(Counter)
        for i in range(len(data) - STATE_LEN - 1):
            state = tuple(data[i:i + STATE_LEN])
            next = data[i + STATE_LEN]
            states[state][next] += 1
        save_model(states)
    else:
        print('Loaded cached model with {0} states'.format(len(states)))

    for i in range(len(data) - STATE_LEN - 1):
        state = tuple(data[i:i + STATE_LEN])
        next = data[i + STATE_LEN]
        states[state][next] += 1

    print('Model has {0} states'.format(len(states)))

    save_model(states) # !
    return states

def generate_text(states, start_state=None):
    if start_state is None:
        state = random.choice(list(states))
    else:
        state = tuple(start_state.split()[:STATE_LEN])

    generated = list(state)

    for _ in range(100):
        if state not in states or not states[state]:
            state = random.choice(list(states))
            generated = list(state)
        else:
            next_word = weighted_from_counter(states[state])
            generated.append(next_word)
            state = tuple(generated[-STATE_LEN:])
    text = ' '.join(generated)
    return format_text(text)

states = train_model()

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    if 'start_state' in data:
        start_state = data['start_state']
        return jsonify({'text' : generate_text(states, start_state)})
    else:
        return jsonify({'text' : generate_text(states)})



if __name__ == '__main__':
    app.run(debug=True)