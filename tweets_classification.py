import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes, svm, tree, linear_model
from sklearn.metrics import accuracy_score,precision_score, recall_score, f1_score, confusion_matrix

# Función utilizada para crear el archivo .csv con las predicciones de los test realizados
def create_prediction(folder,testX, testY):

    dataFrame = pd.DataFrame()
    dataFrame['tweet_translated_tokenized'] = pd.DataFrame(testX, columns = ['tweet_translated_tokenized'])['tweet_translated_tokenized']
    dataFrame['sentiment'] = pd.DataFrame(testY, columns = ['sentiment'])['sentiment']
    
    dataFrame.to_csv("{}//Predicted_Tweets.csv".format(folder), index =  False)
    
# Función utilizada para actualizar el archivo .csv para cada algoritmo de clasficación utilizado
def actualizar_prediction(folder, data, name):

    dataFrame = pd.read_csv("{}//Predicted_Tweets.csv".format(folder))
    dataFrame[name] = pd.DataFrame(data, columns = [name])[name]
    dataFrame.to_csv("{}//Predicted_Tweets.csv".format(folder), index = False)   
    
# Clase utilizada para el entrenamiento y prueba de diferentes algoritmos de clasficación
class tweets_classification():
    
    def __init__(self, user):
        
        self.folder = user+"_Folder"
        self.testing_messages = pd.DataFrame()
        self.testing_labels = pd.DataFrame()
        self.training_messages = pd.DataFrame()
        self.training_labels = pd.DataFrame()
        self.encoder = LabelEncoder()
        
        pass
    
    def training(self,test_size):
        
        Corpus = pd.read_csv("{}//Processed_Tweets.csv".format(self.folder))
        
        Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(Corpus['tweet_translated_tokenized'],Corpus['sentiment'],test_size=test_size,shuffle=False)

        create_prediction(self.folder,Test_X, Test_Y)
        
        self.training_labels = self.encoder.fit_transform(Train_Y)
        self.testing_labels = self.encoder.fit_transform(Test_Y)
        
        print(self.encoder.classes_)

        Tfidf_vect = TfidfVectorizer(max_features=5000)
        Tfidf_vect.fit(Corpus['tweet_translated_tokenized'])
        
        self.training_messages = Tfidf_vect.transform(Train_X)
        self.testing_messages  = Tfidf_vect.transform(Test_X)
        
    def test_Naive_Bayes(self):
        
        NaiveBayes = naive_bayes.MultinomialNB()
        
        # Entrenamiento del algoritmo
        NaiveBayes.fit(self.training_messages,self.training_labels)
        
        # Prediccion del algoritmo
        predictions_NB = NaiveBayes.predict(self.testing_messages)
        
        # Verificación de los resultados
        print("Naive Bayes Accuracy Score -> ",accuracy_score(predictions_NB, self.testing_labels)*100)
        
        predictions_NB_labels = self.encoder.inverse_transform(predictions_NB)
        
        # Guardado de los resultados
        actualizar_prediction(self.folder,predictions_NB_labels,'NB')
        
        pass

    def test_SVM(self):

        SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
        
        # Entrenamiento del algoritmo
        SVM.fit(self.training_messages,self.training_labels)
        
        # Prediccion del algoritmo
        predictions_SVM = SVM.predict(self.testing_messages)
        
        # Verificación de los resultados
        print("SVM Accuracy Score -> ",accuracy_score(predictions_SVM,self.testing_labels)*100)
        
        predictions_SVM_labels = self.encoder.inverse_transform(predictions_SVM)
        
        # Guardado de los resultados
        actualizar_prediction(self.folder,predictions_SVM_labels,'SVM')

        pass
    
    def test_Decision_Forest(self):
        
        DecisionForest = tree.DecisionTreeClassifier()
        
        # Entrenamiento del algoritmo
        DecisionForest.fit(self.training_messages,self.training_labels)
        
        # Prediccion del algoritmo
        predictions_DF = DecisionForest.predict(self.testing_messages)
        
        # Verificación de los resultados
        print("DecisionForest Accuracy Score -> ",accuracy_score(predictions_DF, self.testing_labels)*100)
        
        predictions_DF_labels = self.encoder.inverse_transform(predictions_DF)
        
        # Guardado de los resultados
        actualizar_prediction(self.folder,predictions_DF_labels,'DF')
        
        pass
    
    def test_Max_Entropy(self):
        
        MaxEnt = linear_model.LogisticRegression(penalty='l2', C= 1.0)
        
        # Entrenamiento del algoritmo
        MaxEnt.fit(self.training_messages,self.training_labels)
        
        # Prediccion del algoritmo
        predictions_MaxEnt = MaxEnt.predict(self.testing_messages)
        
        # Verificación de los resultados
        print("Max Entropy Accuracy Score -> ",accuracy_score(predictions_MaxEnt, self.testing_labels)*100)
        
        predictions_MaxEnt_labels = self.encoder.inverse_transform(predictions_MaxEnt)
        
        # Guardado de los resultados
        actualizar_prediction(self.folder,predictions_MaxEnt_labels,'MaxEnt')
        
        pass