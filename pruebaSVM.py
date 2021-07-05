# STEP 1 - Añadir las Librerias necesarias para el análisis de Textos 

from typing_extensions import final
import pandas as pd
import numpy as np
import nltk
import re
import collections
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes, svm
from sklearn.metrics import accuracy_score
from IPython.core.display import Markdown, display

# STEP 2 - Importar el corpus de los mensajes a evaluar

Corpus = pd.read_csv('tweets_list//corpus.csv',encoding='latin-1')

# STEP 3 - Preprocesamiento de los datos 

def clean_tweet(tweet):

    # Eliminación de páginas web (palabras que empiezan por "http")
    tweet = re.sub('http\S+', ' ', tweet)
    # Eliminación de signos de puntuación
    regex = '[\\¡\\!\\"\\“\\”\\#\\$\\%\\&\\\'\\(\\)\\*\\+\\,\\-\\.\\..\\...\\/\\:\\;\\<\\=\\>\\¿\\?\\@\\[\\\\\\]\\^_\\`\\{\\|\\}\\~]'
    tweet = re.sub(regex , ' ', tweet)
    # Eliminación de números
    tweet = re.sub("\d+", ' ', tweet)
    # Eliminación de espacios en blanco múltiples
    tweet = re.sub("\\s+", ' ', tweet)
    
    return tweet

def clean_list(word_list):
    initial_words = list(word_list)
    final_words = [] 
    for token in word_list: # iterate over word_list
        if token not in stopwords.words("english"):
            final_words.append(token)
    return str(final_words)

# 1. Eliminación de mensajes vacios 
Corpus['text'].dropna(inplace=True)

# 2. Convertir todas las oraciones en letras minúsculas
Corpus['text'] = [entry.lower() for entry in Corpus['text']]

# 3. Limpieza de Enlaces, Signos de Puntuacion, Numeros, Espacios Dobles
Corpus['text'] = Corpus['text'].apply(lambda x: clean_tweet(x))

# 5. Tokenización de los mensajes 
Corpus['tokenize'] = [word_tokenize(entry) for entry in Corpus['text']]

# 6 - Eliminar las palabras de parada 
Corpus['clean'] = Corpus['tokenize'].apply(lambda x: clean_list(x))

# Mostrar Corpus 
display(Corpus.head())

# Guardar nuevo CSV actualizado,
Corpus.to_csv('tweets_list//corpus_cleaned.csv')

Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(Corpus['clean'],Corpus['label'],test_size=0.3)
Encoder = LabelEncoder()
Train_Y = Encoder.fit_transform(Train_Y)
Test_Y = Encoder.fit_transform(Test_Y)

Tfidf_vect = TfidfVectorizer(max_features=5000)
Tfidf_vect.fit(Corpus['clean'])
Train_X_Tfidf = Tfidf_vect.transform(Train_X)
Test_X_Tfidf = Tfidf_vect.transform(Test_X)

print("VOCABULARIO------------------------------------------------"+str(Tfidf_vect.vocabulary_))

print("VECTORIZADO------------------------------------------------"+str(Train_X_Tfidf))
