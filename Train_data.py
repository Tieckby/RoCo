#Importation de la bibliothèque tensorflow
import tensorflow as tf
import numpy as np

import nltk #Pour le traitement automatique du langage
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer() #Pour la recherche des racines des mots

#Module Numpy, random et json
import numpy as np
import random
import pandas as pd

tokenizer = nltk.tokenize.WordPunctTokenizer() #Permet de couper la donnée (question) en plusieurs mots: Tokenization

#On charge le fichier Data(Base de connaissances)
file = pd.read_json('Data.json', encoding='utf-8')
print(file.head()) #On affiche l'entête de nos données
print(file.shape) #La taille des données
print("_________________________________________________________\n")

""" On déclare des listes vides qui sont words (auront les racines uniques des mots)
labelsUniques (auront les noms des intentions)"""
words = []
labelsUniques = []
allWords = []

#Quelques opérations sur nos données
""" On récupère chaque question et l'intention dans allWords designée sous forme de 
tuple (question, intention) après les intentions seront stockées dans  labelsUniques.
Toutes les questions tokenizer seront dans words """
for intent in file["data"]:
    for question in intent["questions"]:
        words_token = tokenizer.tokenize(question)
        words.extend(words_token)
        allWords.append((words_token, intent["tags"]))

        if intent["tags"] not in labelsUniques:
            labelsUniques.append(intent["tags"])
print(f"{words}\n")
print(f"{allWords}\n")
print(f"{labelsUniques}")
print("__________________________________________________________\n")

stopword = ["?", "'"] #Les caractères ignorées

""" On cherche la racine de tous les mots tokenizer qui seront stockés dans words """
words = [stemmer.stem(w.lower()) for w in words if w not in stopword]
words = sorted(list(set(words))) #L'unicité et le trie
print(f"La taille des racines uniques est : {len(words)}")
print(words)
labelsUniques = sorted(list(set(labelsUniques))) #L'unicité et le trie
print(f"\nLa taille des intentions est : {len(labelsUniques)}")
print(labelsUniques)
print("_________________________________________________________\n")

#Declaration des tableaux pour les données d'entrées et de sorties
train = []
list_empty = [0] * len(labelsUniques)

for doc in allWords:
    bag = []
    wrds = doc[0]
    wrds = [stemmer.stem(word.lower()) for word in wrds]

    for word in words:
        if word in wrds:
            bag.append(1)
        else:
            bag.append(0)

        output = list(list_empty)
        output[labelsUniques.index(doc[1])] = 1
        train.append([bag, output])

random.shuffle(train) #On mélange les données
train = np.array(train) #On les met dans un autre tableau

train_X = list(train[:, 0])
train_Y = list(train[:, 1])


def create_model():
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(128, input_shape=(len(train_X[0]),), activation='relu'))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Dense(64, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Dense(len(train_Y[0]), activation='softmax'))
    return model


def modelChat():
    model = create_model()
    model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(np.array(train_X), np.array(train_Y), epochs=50, batch_size=5)
    model.summary()
    return model

def process_input(input_user):
    bag = [0] * len(words)

    input_user_words = tokenizer.tokenize(input_user)
    input_user_words = [stemmer.stem(word.lower()) for word in input_user_words if word not in stopword]

    for input_word in input_user_words:
        for i, word in enumerate(words):
            if word == input_word:
                bag[i] = 1

    return np.array(bag)