import os
import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes, svm, tree, linear_model
from sklearn.metrics import accuracy_score,precision_score, recall_score, f1_score, confusion_matrix

# Función utilizada para crear el archivo .csv con las predicciones de los test realizados
def create_prediction(folder,testX, testY):

    dataFrameEstadistics = pd.DataFrame(columns=['algorithm','accuary','precision','recall','f1_score','confusion_matrix'])
    
    dataFrameEstadistics.to_csv("{}//Statistics_Tweets.csv".format(folder), index =  False)
     
    dataFrame = pd.DataFrame()
    
    dataFrame['tweet_translated_tokenized'] = pd.DataFrame(testX, columns = ['tweet_translated_tokenized'])['tweet_translated_tokenized']
    dataFrame['sentiment'] = pd.DataFrame(testY, columns = ['sentiment'])['sentiment']
    
    dataFrame.to_csv("{}//Predicted_Tweets.csv".format(folder), index =  False)
    
    dataFrame_prob = pd.DataFrame()
    
    dataFrame_prob['tweet_translated_tokenized'] = pd.DataFrame(testX, columns = ['tweet_translated_tokenized'])['tweet_translated_tokenized']
    dataFrame_prob['sentiment'] = pd.DataFrame(testY, columns = ['sentiment'])['sentiment']
    
    dataFrame_prob.to_csv("{}//Predicted_prob_Tweets.csv".format(folder), index =  False)
    
# Función utilizada para actualizar el archivo .csv de Predicciones para cada algoritmo de clasficación utilizado
def update_predictions(folder, data, name):

    dataFrame = pd.read_csv("{}//Predicted_Tweets.csv".format(folder))
    dataFrame[name] = pd.DataFrame(data)
    dataFrame.to_csv("{}//Predicted_Tweets.csv".format(folder), index = False)   
    
def update_predictions_prob(folder, data, name):

    dataFrame = pd.read_csv("{}//Predicted_prob_Tweets.csv".format(folder))
    
    # labels = { 0 : 'Negativo', 1 : 'Neutral', 2 : 'Positivo' }
    labels = { 0 : 'Negativo', 1 : 'Positivo' }
    
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
                                  'confusion_matrix': confusion_matrix(testing_labels, predicted_labels)}, 
                                 ignore_index=True)
        
    dataFrame.to_csv("{}//Statistics_Tweets.csv".format(folder), index = False)   


# Clase utilizada para el entrenamiento y prueba de diferentes algoritmos de clasficación
class tweets_classification():
    
    def __init__(self, user, type):
        
        self.user = user
        if (type == 'users'):
            self.folder = "users//"+user+"_Folder"
        elif (type == 'batch'):
            self.folder = 'batch'
        self.testing_messages = pd.DataFrame()
        self.testing_labels = pd.DataFrame()
        self.training_messages = pd.DataFrame()
        self.training_labels = pd.DataFrame()
        self.encoder = LabelEncoder()
                                                                            
    def load(self):
            
        if not os.path.exists("{}//Processed_Tweets.csv".format(self.folder)):
            df = pd.DataFrame(columns=['tweet','tweet_tokenized','tweet_translated','tweet_translated_tokenized','neg','neu','pos','sentiment'])
            df.to_csv("{}//Processed_Tweets.csv".format(self.folder), index =  False)
    
        dataFrame = pd.read_csv("{}//Processed_Tweets.csv".format(self.folder))
        dataFrame = dataFrame.append(pd.read_csv("{}//Processed_Tweets.csv".format("users//"+self.user+"_Folder")))
        dataFrame.to_csv("{}//Processed_Tweets.csv".format(self.folder), index =  False)
        
    def training(self, test_size):
        
        Corpus= pd.read_csv("{}//Processed_Tweets.csv".format(self.folder))
        
        Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(Corpus['tweet_translated_tokenized'],Corpus['sentiment'],test_size=test_size,shuffle=False)

        create_prediction(self.folder,Test_X, Test_Y)
        
        self.training_labels = self.encoder.fit_transform(Train_Y)
        self.testing_labels = self.encoder.fit_transform(Test_Y)

        Tfidf_vect = TfidfVectorizer()
        Tfidf_vect.fit(Corpus['tweet_translated_tokenized'])
        
        self.training_messages = Tfidf_vect.transform(Train_X)
        self.testing_messages  = Tfidf_vect.transform(Test_X)
        
    def test_Naive_Bayes(self):
        
        NaiveBayes = naive_bayes.MultinomialNB()
        
        # Entrenamiento del algoritmo
        NaiveBayes.fit(self.training_messages,self.training_labels)
        
        # Prediccion del algoritmo
        predictions_NB = NaiveBayes.predict(self.testing_messages)
        
        # Recopilacion de las estadisticas del modelo
        update_statistics(self.folder,'Naive Bayes', self.testing_labels, predictions_NB)
        
        # Conversion de los sentimientos basados en el codificado
        predictions_NB_labels = self.encoder.inverse_transform(predictions_NB)
        
        # Guardado de los resultados
        update_predictions(self.folder,predictions_NB_labels,'NB')
        
        predictions_NB_prob = NaiveBayes.predict_proba(self.testing_messages)
        
        print(str(predictions_NB_prob))
        
        update_predictions_prob(self.folder,predictions_NB_prob,'NB')
        

    def test_SVM(self):

        SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto',probability=True)
        
        # Entrenamiento del algoritmo
        SVM.fit(self.training_messages,self.training_labels)
        
        # Prediccion del algoritmo
        predictions_SVM = SVM.predict(self.testing_messages)
        
        # Recopilacion de las estadisticas del modelo
        update_statistics(self.folder,'Maquina de Soporte Vectorial', self.testing_labels, predictions_SVM)

        # Conversion de los sentimientos basados en el codificado
        predictions_SVM_labels = self.encoder.inverse_transform(predictions_SVM)
        
        # Guardado de los resultados
        update_predictions(self.folder,predictions_SVM_labels,'SVM')
        
        predictions_SVM_prob = SVM.predict_proba(self.testing_messages)
        
        print(str(predictions_SVM_prob))
        
        update_predictions_prob(self.folder,predictions_SVM_prob,'SVM')
    
    def test_Decision_Forest(self):
        
        DecisionForest = tree.DecisionTreeClassifier()
        
        # Entrenamiento del algoritmo
        DecisionForest.fit(self.training_messages,self.training_labels)
        
        # Prediccion del algoritmo
        predictions_DF = DecisionForest.predict(self.testing_messages)
        
        # Recopilacion de las estadisticas del modelo
        update_statistics(self.folder, 'Random Forest', self.testing_labels, predictions_DF)

        # Conversion de los sentimientos basados en el codificado
        predictions_DF_labels = self.encoder.inverse_transform(predictions_DF)
        
        # Guardado de los resultados
        update_predictions(self.folder,predictions_DF_labels,'DF')
        
        predictions_DF_prob = DecisionForest.predict_proba(self.testing_messages)
        
        print(str(predictions_DF_prob))
        
        update_predictions_prob(self.folder,predictions_DF_prob,'DF')
    
    def test_Max_Entropy(self):
        
        MaxEnt = linear_model.LogisticRegression(penalty='l2', C= 1.0)
        
        # Entrenamiento del algoritmo
        MaxEnt.fit(self.training_messages,self.training_labels)
        
        # Prediccion del algoritmo
        predictions_MaxEnt = MaxEnt.predict(self.testing_messages)
        
        # Recopilacion de las estadisticas del modelo
        update_statistics(self.folder, 'Maximun Entropy', self.testing_labels, predictions_MaxEnt)

        # Conversion de los sentimientos basados en el codificado
        predictions_MaxEnt_labels = self.encoder.inverse_transform(predictions_MaxEnt)
        
        # Guardado de los resultados
        update_predictions(self.folder,predictions_MaxEnt_labels,'MaxEnt')
        
        predictions_MaxEnt_prob = MaxEnt.predict_proba(self.testing_messages)
        
        print(str(predictions_MaxEnt_prob))
        
        update_predictions_prob(self.folder,predictions_MaxEnt_prob,'MaxEnt')
