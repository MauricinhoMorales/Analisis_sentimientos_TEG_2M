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

# Función utilizada para crear el archivo .csv con las predicciones del test realizado
def create_prediction(folder,testX, testY):
    
    dataFrame = pd.DataFrame()
    dataFrame['tweet_tokenized'] = pd.DataFrame(testX, columns = ['tweet_tokenized'])['tweet_tokenized']
    dataFrame['Sentiment'] = pd.DataFrame(testY, columns = ['Sentiment'])['Sentiment']
    
    dataFrame.to_csv("{}//Predicted_Tweets.csv".format(folder), index =  False)
    
# Función utilizada para actualizar el archivo .csv para cada algoritmo
def actualizar_prediction(folder, data, name):
    
    dataFrame = pd.read_csv("{}//Predicted_Tweets.csv".format(folder))
    dataFrame[name] = pd.DataFrame(data, columns = [name])[name]
    
    dataFrame.to_csv("{}//Predicted_Tweets.csv".format(folder), index = False)   
    
# Clase utilizada para el entrenamiento y clasificación de los tweets por diferentes algoritmos 
class classification():
    
    def __init__(self, user):
        self.user = user
        self.folder = user+'_folder'
        self.testing_messages = pd.DataFrame()
        self.testing_labels = pd.DataFrame()
        self.training_messages = pd.DataFrame()
        self.training_labels = pd.DataFrame()
        pass
    
    def training(self,test_size):
        
        Corpus = pd.read_csv("{}//Processed_Tweets.csv".format(self.folder))
        
        Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(Corpus['tweet_tokenized'],Corpus['Sentiment'],test_size=test_size,shuffle=False)

        create_prediction(self.folder,Test_X, Test_Y)

        Encoder = LabelEncoder()
        
        self.training_labels = Encoder.fit_transform(Train_Y)
        self.testing_labels = Encoder.fit_transform(Test_Y)

        Tfidf_vect = TfidfVectorizer(max_features=5000)
        Tfidf_vect.fit(Corpus['tweet_tokenized'])
        
        self.training_messages = Tfidf_vect.transform(Train_X)
        self.testing_messages  = Tfidf_vect.transform(Test_X)
        
    def test_naive_bayes(self):
        
        NaiveBayes = naive_bayes.MultinomialNB()
        
        # Entrenamiento del algoritmo
        NaiveBayes.fit(self.training_messages,self.training_labels)
        
        # Prediccion del algoritmo
        predictions_NB = NaiveBayes.predict(self.testing_messages)
        
        # Verificación de los resultados
        print("Naive Bayes Accuracy Score -> ",accuracy_score(predictions_NB, self.testing_labels)*100)
        
        # Guardado de los resultados
        actualizar_prediction(self.folder,predictions_NB,'NB')
        
        pass

    def test_SVM(self):

        SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
        
        # Entrenamiento del algoritmo
        SVM.fit(self.training_messages,self.training_labels)
        
        # Prediccion del algoritmo
        predictions_SVM = SVM.predict(self.testing_messages)
        
        # Verificación de los resultados
        print("SVM Accuracy Score -> ",accuracy_score(predictions_SVM,self.testing_labels)*100)
        
        # Guardado de los resultados
        actualizar_prediction(self.folder, predictions_SVM,'SVM')

        pass
    
    def test_Decision_Forest(self):
        
        DecisionForest = tree.DecisionTreeClassifier()
        
        # Entrenamiento del algoritmo
        DecisionForest.fit(self.training_messages,self.training_labels)
        
        # Prediccion del algoritmo
        predictions_DF = DecisionForest.predict(self.testing_messages)
        
        # Verificación de los resultados
        print("DecisionForest Accuracy Score -> ",accuracy_score(predictions_DF, self.testing_labels)*100)
        
        # Guardado de los resultados
        actualizar_prediction(self.folder, predictions_DF,'DF')
        
        pass
