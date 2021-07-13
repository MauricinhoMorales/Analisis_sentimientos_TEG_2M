# STEP 1 - Añadir las Librerias necesarias para el análisis de Textos 

from typing_extensions import final
import pandas as pd
import numpy as np
import re
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes, svm, tree
from sklearn.metrics import accuracy_score
from IPython.core.display import Markdown, display

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

def create_prediccion(testX, testY):
    
    dataFrame = pd.DataFrame()
    dataFrame['tokenize'] = pd.DataFrame(testX, columns = ['tokenize'])['tokenize']
    dataFrame['label'] = pd.DataFrame(testY, columns = ['label'])['label']
    dataFrame.to_csv('tweets_list//predicciones2.csv', index =  False)
    
def actualizar_prediccion(data, nombre):
    
    dataFrame = pd.read_csv('tweets_list//predicciones2.csv')
    dataFrame[nombre] = pd.DataFrame(data, columns = [nombre])[nombre]
    dataFrame.to_csv('tweets_list//predicciones2.csv',index = False)   
    

# STEP 2 - Importar el corpus de los mensajes a evaluar

Corpus = pd.read_csv('tweets_list//corpus2.csv',encoding='latin-1')

# STEP 3 - Preprocesamiento de los datos 

# 1. Eliminación de mensajes vacios 
Corpus['text'].dropna(inplace=True)

# 2. Convertir todas las oraciones en letras minúsculas
Corpus['text'] = [entry.lower() for entry in Corpus['text']]

# 3. Limpieza de Enlaces, Signos de Puntuacion, Numeros, Espacios Dobles
Corpus['text'] = Corpus['text'].apply(lambda x: clean_tweet(x))

# 5. Tokenización de los mensajes 
Corpus['tokenize'] = [word_tokenize(entry) for entry in Corpus['text']]

# 6 - Eliminar las palabras de parada 
Corpus['tokenize'] = Corpus['tokenize'].apply(lambda x: clean_list(x))

# Guardar nuevo CSV actualizado
Corpus.to_csv('tweets_list//corpus_cleaned2.csv', index = False)

# STEP 4 - Entrenamiento y prediccion de una variable a partir de un conjunto de variables

Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(Corpus['tokenize'],Corpus['label'],test_size=0.05,shuffle=False)

create_prediccion(Test_X, Test_Y)

Encoder = LabelEncoder()
Train_Y = Encoder.fit_transform(Train_Y)
Test_Y = Encoder.fit_transform(Test_Y)

Tfidf_vect = TfidfVectorizer(max_features=5000)
Tfidf_vect.fit(Corpus['tokenize'])
Train_X_Tfidf = Tfidf_vect.transform(Train_X)
Test_X_Tfidf = Tfidf_vect.transform(Test_X)

# Algoritmo Multinomial NB Classifier-----------------------------------------------------------------------------

NaiveBayes = naive_bayes.MultinomialNB()
# Entrenamiento del algoritmo
NaiveBayes.fit(Train_X_Tfidf,Train_Y)
# Prediccion del algoritmo
predictions_NB = NaiveBayes.predict(Test_X_Tfidf)
# Verificación de los resultados
print("Naive Bayes Accuracy Score -> ",accuracy_score(predictions_NB, Test_Y)*100)
# Guardado de los resultados
actualizar_prediccion(predictions_NB,'NB')

# Algoritmo SVM Classifier----------------------------------------------------------------------------------------

SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
# Entrenamiento del algoritmo
SVM.fit(Train_X_Tfidf,Train_Y)
# Prediccion del algoritmo
predictions_SVM = SVM.predict(Test_X_Tfidf)
# Verificación de los resultados
print("SVM Accuracy Score -> ",accuracy_score(predictions_SVM, Test_Y)*100)
# Guardado de los resultados
actualizar_prediccion(predictions_SVM,'SVM')

# Algoritmo Arboles de Decision Classifier----------------------------------------------------------------------------------------

DecisionForest = tree.DecisionTreeClassifier()
# Entrenamiento del algoritmo
DecisionForest.fit(Train_X_Tfidf,Train_Y)
# Prediccion del algoritmo
predictions_DF = DecisionForest.predict(Test_X_Tfidf)
# Verificación de los resultados
print("DecisionForest Accuracy Score -> ",accuracy_score(predictions_DF, Test_Y)*100)
# Guardado de los resultados
actualizar_prediccion(predictions_DF,'DF')



