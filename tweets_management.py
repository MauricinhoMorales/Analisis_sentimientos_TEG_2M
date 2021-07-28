import os
import re
import twint
import pandas as pd

from nltk.corpus import stopwords
from googletrans import Translator
from deep_translator import GoogleTranslator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Función que crea una carpeta (en caso de que no exista) con el nombre dado.
def create_folder(folder):
    
    if not os.path.exists(folder):
        os.makedirs(folder)

# Función que Recopila los tweets deseados usando diferentes filtros.
def scrape_info(user,quantity,folder):
    
    create_folder(folder)
    
    c = twint.Config()
    c.Username = user
    c.Limit = quantity
    c.Count = True
    c.Lang = "es"
    c.Store_object = True
    c.Output = "{}//Raw_Tweets.csv".format(folder)
    c.Show_cashtags = False
    c.Store_csv = True
    c.Pandas = True
    c.Pandas_clean = True
    c.Store_pandas = True
    c.Retweets = False
    c.Replies = False
    c.Native_retweets = False
    c.Hide_output = True
    
    twint.run.Search(c)
    
# Funcion que permite limpiar y tokenizar los tweets
def clean_tokenized(texto):
    
    # Se convierte todo el texto a minúsculas
    if(texto == None):
        texto = ''
    nuevo_texto = texto.lower()
    
    # Eliminación de páginas web 
    nuevo_texto = re.sub('http\S+', ' ', nuevo_texto)
    
    # Eliminación de signos de puntuación
    regex = '[\\!\\"\\“\\#\\$\\%\\&\\\'\\(\\)\\*\\+\\,\\-\\.\\/\\:\\;\\<\\=\\>\\?\\@\\[\\\\\\]\\^_\\`\\{\\|\\}\\~]'
    nuevo_texto = re.sub(regex , ' ', nuevo_texto)
    
    # Eliminación de números
    nuevo_texto = re.sub("\d+", ' ', nuevo_texto)
    
    # Eliminación de espacios en blanco múltiples
    nuevo_texto = re.sub("\\s+", ' ', nuevo_texto)
    
    # Tokenización por palabras individuales
    nuevo_texto = nuevo_texto.split(sep = ' ')
    
    # Eliminación de tokens con una longitud < 2
    nuevo_texto = [token for token in nuevo_texto if len(token) > 1]
    
    return(nuevo_texto)

# Función que permite remover las palabras que no aportar valor al analisis en un idioma dado
def remove_stopwords(word_list, language):
    
    initial_words = list(word_list)
    final_words = [] 
    for token in word_list: # iterate over word_list
        if token not in stopwords.words(language):
            final_words.append(token)
    return str(final_words)

# Función para traducir un mensaje al idioma ingles (Aun no sirve)
def googletrans_translate(text,translator):
    # return translator.translate(text).text
    translated_tex = GoogleTranslator(source='auto', target='english').translate(text)
    return translated_tex

# Función para realizar el análisis de sentimientos usando la librería Vader.
def sentiment_analysis(folder):
    df = pd.read_csv("users_folders//{}//Processed_Tweets.csv".format(folder))

    analyzer = SentimentIntensityAnalyzer()
    # sentence = df.at[0,'tweet_translated']
    
    df['neg'] = [analyzer.polarity_scores(x)['neg'] for x in df['tweet']]
    df['neu'] = [analyzer.polarity_scores(x)['neu'] for x in df['tweet']]
    df['pos'] = [analyzer.polarity_scores(x)['pos'] for x in df['tweet']]
    
    for index,row in df.iterrows():
        if row['pos'] > row['neg'] and row['pos'] > row['neu']:
            df['sentiment'] = 'Positivo'
        elif row['neg'] > row['neu']:
            df['sentiment'] = 'Negativo'
        else:
            df['sentiment'] = 'Neutral'
        pass

    df.to_csv("users_folders//{}//Processed_Tweets.csv".format(folder),index=False)

# Clase que se encarga de la recopilción, manejo y análisis de sentimientos de los tweets extraídos
class tweets_management():
    
    def __init__(self,user,dir):
        self.user = user
        self.folder = user+"_Folder"
        self.dir = dir
        self.translator = Translator()
        
    def scraping(self,amount):
        if (self.dir == 'users_folders'):
            scrape_info(self.user,amount,"{}//{}".format(self.dir,self.folder))
        elif (self.dir == 'user_one_file'):
            scrape_info(self.user,amount,self.dir)
    
    def cleaning(self):
        print('-----------------------------------------------------')
        print('empieza limpieza y traducción')
        if (self.dir == 'users_folders'):
            df = pd.read_csv("{}//{}//Raw_Tweets.csv".format(self.dir,self.folder))
        elif (self.dir == 'user_one_file'):
            df = pd.read_csv("{}//Raw_Tweets.csv".format(self.dir))
        
        df['tweet_tokenized'] = df['tweet'].apply(lambda x: clean_tokenized(x))
        df['tweet_tokenized'] = df['tweet_tokenized'].apply(lambda x: remove_stopwords(x,"spanish"))
        
        df['tweet_translated'] = df['tweet'].apply(lambda x: googletrans_translate(x,self.translator))
        df['tweet_translated_tokenized'] = df['tweet_translated'].apply(lambda x: clean_tokenized(x))
        df['tweet_translated_tokenized'] = df['tweet_translated_tokenized'].apply(lambda x: remove_stopwords(x,"english"))
        
        if (self.dir == 'users_folders'):
            df.to_csv('{}//{}//Processed_Tweets.csv'.format(self.dir,self.folder), columns=['tweet','tweet_tokenized','tweet_translated','tweet_translated_tokenized'],index=False)
            # df.to_csv('{}//{}//Processed_Tweets.csv'.format(self.dir,self.folder), columns=['tweet','tweet_tokenized'],index=False)
        elif (self.dir == 'user_one_file'):
            df.to_csv('{}//Processed_Tweets.csv'.format(self.dir), columns=['tweet','tweet_tokenized','tweet_translated','tweet_translated_tokenized'],index=False)
            # df.to_csv('{}//Processed_Tweets.csv'.format(self.dir), columns=['tweet','tweet_tokenized'],index=False)
        print('termina limpieza y traducción')
        print('-----------------------------------------------------')
    def sentiment_analysis(self):
        
        sentiment_analysis(self.folder)
        
    pass