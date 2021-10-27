import os
import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes, svm, tree, linear_model
from sklearn.metrics import accuracy_score,precision_score, recall_score, f1_score, confusion_matrix

# Función utilizada para crear el archivo .csv con las predicciones de los test realizados
def create_prediction(folder,testX, testY):

    dataFrameEstadistics = pd.DataFrame(columns=['algorithm','accuary','precision','recall','f1_score','precision_all','recall_all','f1_score_all','confusion_matrix'])
    
    dataFrameEstadistics.to_csv("{}//Statistics_Tweets.csv".format(folder), index =  False)
     
    dataFrame = pd.DataFrame()
    
    dataFrame['tweet_tokenized_translated'] = pd.DataFrame(testX, columns = ['tweet_tokenized_translated'])['tweet_tokenized_translated']
    dataFrame[folder] = pd.DataFrame(testY, columns = [folder])[folder]
    
    dataFrame.to_csv("{}//Predicted_Tweets.csv".format(folder), index =  False)
    
    dataFrame_prob = pd.DataFrame()
    
    dataFrame_prob['tweet_tokenized_translated'] = pd.DataFrame(testX, columns = ['tweet_tokenized_translated'])['tweet_tokenized_translated']
    dataFrame_prob[folder] = pd.DataFrame(testY, columns = [folder])[folder]
    
    dataFrame_prob.to_csv("{}//Predicted_prob_Tweets.csv".format(folder), index =  False)

# Función utilizada para actualizar el archivo .csv de Predicciones para cada algoritmo de clasficación utilizado
def update_predictions(folder, data, name):

    dataFrame = pd.read_csv("{}//Predicted_Tweets.csv".format(folder))
    dataFrame[name] = pd.DataFrame(data)
    dataFrame.to_csv("{}//Predicted_Tweets.csv".format(folder), index = False)

# Función utilizada para actualizar el archivo .csv de distribucion de probabilidad de Predicciones para cada algoritmo de clasficación utilizado   
def update_predictions_prob(folder, data, name):

    dataFrame = pd.read_csv("{}//Predicted_prob_Tweets.csv".format(folder))
    if( folder == 'sentimiento'):
        labels = { 0 : 'Felicidad', 1 : 'Ira', 2 : 'Miedo', 3: 'Tristeza' }
    else:
        labels = { 0 : 'a favor', 1 : 'en contra', 2 : 'neutro' }
    
    list = pd.Series(np.arange(0,len(pd.DataFrame(data).columns),1))
    
    for value in list:
        dataFrame[name+'_'+labels[value]] = pd.DataFrame(data[:,value])
        
    dataFrame.to_csv("{}//Predicted_prob_Tweets.csv".format(folder), index = False)       

# Funcion utilizada para actualizar el archivo .csv de Estadisticas para cada algoritmo de clasificacion utilizado  
def update_statistics(folder,name, testing_labels, predicted_labels):
    
    dataFrame = pd.read_csv("{}//Statistics_Tweets.csv".format(folder))
    
    dataFrame = dataFrame.append({'algorithm': name,
                                  'accuary': accuracy_score(testing_labels, predicted_labels)*100,
                                  'precision': precision_score(testing_labels, predicted_labels, average=None, zero_division=0)*100,
                                  'recall': recall_score(testing_labels, predicted_labels, average=None, zero_division=0)*100,
                                  'f1_score': f1_score(testing_labels, predicted_labels, average=None, zero_division=0)*100,
                                  'precision_all': precision_score(testing_labels, predicted_labels, average='weighted', zero_division=0)*100,
                                  'recall_all': recall_score(testing_labels, predicted_labels, average='weighted', zero_division=0)*100,
                                  'f1_score_all': f1_score(testing_labels, predicted_labels, average='weighted', zero_division=0)*100,
                                  'confusion_matrix': confusion_matrix(testing_labels, predicted_labels)}, 
                                 ignore_index=True)
    dataFrame.to_csv("{}//Statistics_Tweets.csv".format(folder), index = False)   


# Clase utilizada para el entrenamiento y prueba de diferentes algoritmos de clasficación
class tweets_classification():

    def __init__(self,type,df_from_db):
        self.folder = type
        self.df_from_db = df_from_db
        self.testing_messages = pd.DataFrame()
        self.testing_labels = pd.DataFrame()
        self.training_messages = pd.DataFrame()
        self.training_labels = pd.DataFrame()
        self.encoder = LabelEncoder()
        self.tfidf_vect  = TfidfVectorizer()
        if 'tweet_sentiment' in df_from_db.columns:
            self.df_from_db = self.df_from_db.rename(columns={'tweet_sentiment': 'sentimiento'})
        elif 'tweet_opinion' in df_from_db.columns:
            self.df_from_db = self.df_from_db.rename(columns={'tweet_opinion': 'opinion'})

    # Función encargada de la preparación de los datos para la etapa de entrenamiento de los modelos
    def training(self, test_size, train_size):
        """."""
        # Lectura del archivo donde se encuentran los datos de entrenamiento y pruebas ya procesados
        # Corpus= pd.read_csv("{}//Processed_Tweets.csv".format(self.folder))
        Corpus= self.df_from_db

        # Se ejecuta la división de la data de entrenamiento y de prueba (X representa los textos procesados, Y representa las ctageorías)
        Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(
            Corpus['tweet_translated_tokenized'], Corpus[self.folder],
            test_size=test_size,train_size=train_size,shuffle=True,stratify=Corpus[self.folder],random_state=2)

        # Función para crear el archivo donde se almacenarán las predicciones realizadas
        create_prediction(self.folder,Test_X, Test_Y)

        # Se transforman las categorías a valores numéricos utidlizando un codificador
        self.training_labels = self.encoder.fit_transform(Train_Y)
        self.testing_labels = self.encoder.fit_transform(Test_Y)

        # Se crea un diccionario para asignar un valor numérico único a cada palabra de los textos procesados
        # Tfidf_vect = TfidfVectorizer()
        self.tfidf_vect.fit(Corpus['tweet_translated_tokenized'])

        # Se utiliza el diccionario para transformar todos los textos a sus equivalentes valores numéricos
        self.training_messages = self.tfidf_vect.transform(Train_X)
        self.testing_messages  = self.tfidf_vect.transform(Test_X)

    # Función para la creación del modelo basado en el algoritmo de Naive Bayes
    def test_Naive_Bayes(self):
        """."""
        # Inicialización del algoritmo de naive bayes
        NaiveBayes = naive_bayes.MultinomialNB()

        # Se le suministran los valores de entrenamiento al algoritmo de clasificación
        NaiveBayes.fit(self.training_messages,self.training_labels)

        # Se realiza la predicción de los textos de prueba utilizando el algoritmo entrenado
        predictions_NB = NaiveBayes.predict(self.testing_messages)

        # Función utilizada para almacenar los valores de las métricas de rendimiento 
        update_statistics(self.folder,'Naive Bayes', self.testing_labels, predictions_NB)

        # Conversión de los valores numéricos de la predicción a su equivalente en las categorías
        predictions_NB_labels = self.encoder.inverse_transform(predictions_NB)

        # Función utilizada para almacenar las predicciones realizadas por el modelo
        update_predictions(self.folder,predictions_NB_labels,'NB')

        # Se realiza la predicción basada en una distribución de probabilidades de las categorías
        predictions_NB_prob = NaiveBayes.predict_proba(self.testing_messages)

        # Función utilizada para almacenar la distribución de probabilidades de las predicciones realizadas
        update_predictions_prob(self.folder,predictions_NB_prob,'NB')

    # Función para la creación del modelo basado en el algoritmo de de Máquinas de Soporte Vectorial
    def test_SVM(self):
        """."""
        # Inicialización del algoritmo de Máquinas de Soporte Vectorial
        SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto',probability=True)

        # Se le suministran los valores de entrenamiento al algoritmo de clasificación 
        SVM.fit(self.training_messages,self.training_labels)

        # Se realiza la predicción de los textos de prueba utilizando el algoritmo entrenado
        predictions_SVM = SVM.predict(self.testing_messages)

        # Función utilizada para almacenar los valores de las métricas de rendimiento 
        update_statistics(self.folder,'Maquina de Soporte Vectorial', self.testing_labels, predictions_SVM)

        # Conversión de los valores numéricos de la predicción a su equivalente en las categorías
        predictions_SVM_labels = self.encoder.inverse_transform(predictions_SVM)

        # Función utilizada para almacenar las predicciones realizadas por el modelo
        update_predictions(self.folder,predictions_SVM_labels,'SVM')

        # Se realiza la predicción basada en una distribución de probabilidades de las categorías
        predictions_SVM_prob = SVM.predict_proba(self.testing_messages)

        # Función utilizada para almacenar la distribución de probabilidades de las predicciones realizadas
        update_predictions_prob(self.folder,predictions_SVM_prob,'SVM')

    # Función para la creación del modelo basado en el algoritmo de Árboles de Decisión
    def test_Decision_Tree(self):
        """."""
        # Inicialización del algoritmo de Árboles de Decisión
        DecisionTree = tree.DecisionTreeClassifier()

        # Se le suministran los valores de entrenamiento al algoritmo de clasificación 
        DecisionTree.fit(self.training_messages,self.training_labels)

        # Se realiza la predicción de los textos de prueba utilizando el algoritmo entrenado
        predictions_DT = DecisionTree.predict(self.testing_messages)

        # Función utilizada para almacenar los valores de las métricas de rendimiento 
        update_statistics(self.folder, 'Decision Tree', self.testing_labels, predictions_DT)

        # Conversión de los valores numéricos de la predicción a su equivalente en las categorías
        predictions_DT_labels = self.encoder.inverse_transform(predictions_DT)

        # Función utilizada para almacenar las predicciones realizadas por el modelo
        update_predictions(self.folder,predictions_DT_labels,'DT')

        # Se realiza la predicción basada en una distribución de probabilidades de las categorías
        predictions_DT_prob = DecisionTree.predict_proba(self.testing_messages)

        # Función utilizada para almacenar la distribución de probabilidades de las predicciones realizadas
        update_predictions_prob(self.folder,predictions_DT_prob,'DT')

    # Función para la creación del modelo basado en el algoritmo de Máxima Entropía
    def test_Max_Entropy(self):
        """."""
        # Inicialización del algoritmo de Máxima Entropía
        MaxEnt = linear_model.LogisticRegression(penalty='l2', C= 1.0)

        # Se le suministran los valores de entrenamiento al algoritmo de clasificación 
        MaxEnt.fit(self.training_messages,self.training_labels)

        # Se realiza la predicción de los textos de prueba utilizando el algoritmo entrenado
        predictions_MaxEnt = MaxEnt.predict(self.testing_messages)

        # Función utilizada para almacenar los valores de las métricas de rendimiento 
        update_statistics(self.folder, 'Maximun Entropy', self.testing_labels, predictions_MaxEnt)

        # Conversión de los valores numéricos de la predicción a su equivalente en las categorías
        predictions_MaxEnt_labels = self.encoder.inverse_transform(predictions_MaxEnt)

        # Función utilizada para almacenar las predicciones realizadas por el modelo
        update_predictions(self.folder,predictions_MaxEnt_labels,'MaxEnt')

        # Se realiza la predicción basada en una distribución de probabilidades de las categorías
        predictions_MaxEnt_prob = MaxEnt.predict_proba(self.testing_messages)

        # Función utilizada para almacenar la distribución de probabilidades de las predicciones realizadas
        update_predictions_prob(self.folder,predictions_MaxEnt_prob,'MaxEnt')

    def test_batch(self,df_to_test,category):
        """."""
        # Inicialización del algoritmo de Máquinas de Soporte Vectorial
        SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto',probability=True)

        # Se le suministran los valores de entrenamiento al algoritmo de clasificación 
        SVM.fit(self.training_messages,self.training_labels)

        # Lectura de los datos de prueba
        # Corpus= pd.read_csv("{}//Test_Tweets.csv".format(self.folder), encoding = 'unicode_escape')
        Corpus = df_to_test

        # Se codifican los mensajes de prueba
        testing_messages = self.tfidf_vect.transform(Corpus['tweet_translated_tokenized'])

        # Se realiza la predicción de los textos de prueba utilizando el algoritmo entrenado
        predictions_SVM = SVM.predict(testing_messages)

        # Se obtienen los valores correspondientes de la prediccion realizada
        predictions_SVM_labels = self.encoder.inverse_transform(predictions_SVM)

        # Se guarda en un dataframe los datos de prueba y la prediccion realizada
        dataFrame = Corpus
        if category == 'sentimiento':
            dataFrame['tweet_sentiment'] = predictions_SVM_labels
        if category == 'opinion':
            dataFrame['tweet_opinion'] = predictions_SVM_labels
        # dataFrame['predicciones'] = predictions_SVM_labels
        return dataFrame
        # Se guardan los datos del datafrme en un archivo .csv de resultados
        # dataFrame.to_csv("{}//Results_Tweets.csv".format(self.folder), index =  False)
